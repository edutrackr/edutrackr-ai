import dlib
import cv2
import numpy as np
from numpy.linalg import norm
from api.algorithms.video_analyzer import BaseVideoAnalyzer
from api.algorithms.settings.attention_level import AttentionLevelSettings
from api.common.constants.attention_level import AttentionLevelStatus
from api.models.attention_level import AttentionLevelResponse
from config import AIConfig
from decimal import Decimal


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
        rects = face_detector(gray, 0)

        # Loop over the face detections
        # TODO: Algorithm is using all the available faces
        for rect in rects:
            landmarks = face_predictor(gray, rect)

            # Use the coordinates of each eye to compute the eye aspect ratio.
            left_aspect_ratio = self.__eye_aspect_ratio(landmarks, range(42, 48))
            right_aspect_ratio = self.__eye_aspect_ratio(landmarks, range(36, 42))
            ear = (left_aspect_ratio + right_aspect_ratio) / 2.0 # Eye Aspect Ratio

            # If the eye aspect ratio is below the blink threshold, set the eye_closed flag to True.
            if ear < self._settings.eye_ratio_threshold:
                self._eye_closed = True

            # If the eye aspect ratio is above the blink threshold and 
            # the eye_closed flag is True, increment the number of blinks.
            elif ear >= self._settings.eye_ratio_threshold and self._eye_closed:
                self._blinks_count += 1
                self._eye_closed = False



    def _get_final_result(self) -> AttentionLevelResponse:
        blink_rate = self._blinks_count / self._video_metadata.duration * 60 # Blinks per minute
        result = AttentionLevelResponse(
            blinks=self._blinks_count,
            blink_rate=Decimal(f"{blink_rate:.3f}"),
            level=self.__calculate_attention_level(blink_rate)
        )
        return result


    def __eye_aspect_ratio(self, landmarks, eye_range):
        """
        Compute the eye aspect ratio (EAR) given the eye landmarks.
        """

        # Get the eye coordinates
        eye = np.array(
            [np.array([landmarks.part(i).x, landmarks.part(i).y]) for i in eye_range]
        )

        # Compute the euclidean distances
        B = norm(eye[0] - eye[3])
        A = self.__mid_line_distance(eye[1], eye[2], eye[5], eye[4])

        # Use the euclidean distance to compute the aspect ratio
        ear = A / B
        return ear
    

    def __mid_line_distance(self, p1 ,p2, p3, p4):
        """
        Compute the euclidean distance between the midpoints of the two sets of points.
        """
        p5 = np.array([int((p1[0] + p2[0])/2), int((p1[1] + p2[1])/2)])
        p6 = np.array([int((p3[0] + p4[0])/2), int((p3[1] + p4[1])/2)])
        return norm(p5 - p6)
    
    
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
