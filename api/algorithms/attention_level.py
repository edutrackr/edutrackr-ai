import dlib
import cv2
import numpy as np
from decimal import Decimal
from config import AIConfig
from api.algorithms.eye_aspect_ratio import optimized_ear, original_ear
from api.algorithms.video_analyzer import BaseVideoAnalyzer
from api.algorithms.settings.attention_level import AttentionLevelSettings
from api.common.constants.attention_level import AttentionLevelStatus, FacialLandmarksIndexes
from api.models.attention_level import AttentionLevelResponse


face_detector = dlib.get_frontal_face_detector() # type: ignore
"""
Dlib's face detector.
"""

face_predictor = dlib.shape_predictor(AIConfig.Blinking.SHAPE_PREDICTOR_PATH) # type: ignore
"""
Dlib's face landmark predictor.
"""


class AttentionLevelAnalyzer(BaseVideoAnalyzer[AttentionLevelResponse]):
    """
    Analyzer for the attention level algorithm.
    """
    
    _settings: AttentionLevelSettings
    """
    The settings for the analyzer.
    """

    _blinks_count: int
    """
    The number of blinks.
    """

    _eye_closed: bool
    """
    Flag indicating if the eye is closed.
    """


    def __init__(self, settings: AttentionLevelSettings):
        super().__init__(settings.video)
        self._settings = settings


    def _reset_state(self) -> None:
        self._blinks_count = 0
        self._eye_closed = False


    def _analyze_frame(self, frame: np.ndarray) -> None:
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        faces = face_detector(gray, 0)
        if len(faces) == 0:
            return
        
        # Get the landmarks of the first face
        first_face = faces[0]
        landmarks = face_predictor(gray, first_face)

        # Use the coordinates of each eye to compute the eye aspect ratio (EAR)
        left_eye = self.__extract_landmarks(landmarks, FacialLandmarksIndexes.LEFT_EYE)
        right_eye = self.__extract_landmarks(landmarks, FacialLandmarksIndexes.RIGHT_EYE)
        avg_ear = np.mean([
            self.__eye_aspect_ratio(left_eye),
            self.__eye_aspect_ratio(right_eye)
        ])

        # If eye aspect ratio is below the blink threshold, the eye is closed
        if avg_ear < self._settings.eye_ratio_threshold:
            self._eye_closed = True

        # If eye aspect ratio is above the blink threshold and eye is closed,
        # the eye is open and a blink is registered
        elif avg_ear >= self._settings.eye_ratio_threshold and self._eye_closed:
            self._blinks_count += 1
            self._eye_closed = False


    def _get_final_result(self) -> AttentionLevelResponse:
        blink_rate = self._blinks_count / self._video_metadata.duration * 60 # Blinks per minute
        result = AttentionLevelResponse(
            blinks=self._blinks_count,
            blink_rate=Decimal(f"{blink_rate:.3f}"),
            level=self.__calculate_attention_level(blink_rate),
            video_duration=self._video_metadata.duration
        )
        return result


    def __extract_landmarks(self, landmarks, landmarks_indexes: tuple[int, int]) -> np.ndarray:
        """
        Extract coordinates (x, y) from the provided face landmarks given the start and end indexes.

        Returns a 2-dimensional integer numpy array with the coordinates of each eye landmark.
        """
        (start, end) = landmarks_indexes
        return np.array(
            [(landmarks.part(i).x, landmarks.part(i).y) for i in range(start, end)],
            dtype=np.int32
        )


    def __eye_aspect_ratio(self, eye_landmarks: np.ndarray) -> float:
        """
        Compute the eye aspect ratio (EAR) given the eye landmarks.
        """
        if self._settings.eye_ratio_algorithm == "optimized":
            return optimized_ear(eye_landmarks)
        return original_ear(eye_landmarks)
        

    def __calculate_attention_level(self, blink_rate_per_minute):
        """
        Calculate the attention level based on the blink rate per minute.
        """
        if blink_rate_per_minute >= 50:
            status = AttentionLevelStatus.HIGH
        elif 36 <= blink_rate_per_minute < 50:
            status = AttentionLevelStatus.MEDIUM
        else:
            status = AttentionLevelStatus.LOW
        return status
