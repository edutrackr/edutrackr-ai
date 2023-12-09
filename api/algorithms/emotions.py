import os
import cv2
import numpy as np
from decimal import Decimal
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from api.algorithms.video_analyzer import BaseVideoAnalyzer
from api.algorithms.settings.emotions import EmotionsSettings
from api.common.constants.emotions import EMOTION_TYPES
from api.models.emotions import EmotionDetail, EmotionsResponse
from config import AIConfig


# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

face_model = cv2.dnn.readNet(AIConfig.Emotions.PROTOTXT_PATH, AIConfig.Emotions.WEIGHTS_PATH)
"""
The face detector model (based on FaceNet).
"""

emotion_model: any = load_model(AIConfig.Emotions.CLASSIFICATION_MODEL_PATH) # type: ignore
"""
The emotion classification model.
"""


class EmotionsAnalyzer(BaseVideoAnalyzer[EmotionsResponse]):
    """
    Analyzer for the emotions algorithm.
    """
    
    _settings: EmotionsSettings
    """
    The settings for the analyzer.
    """

    _total_confidence_by_emotion: dict[str, float]
    """
    The total confidence for each emotion.
    """

    _prediction_count_by_emotion: dict[str, int]
    """
    The number of predictions for each emotion.
    """


    def __init__(self, settings: EmotionsSettings):
        super().__init__(settings.video)
        self._settings = settings


    def _reset_state(self) -> None:
        self._total_confidence_by_emotion = {}
        self._prediction_count_by_emotion = {}


    def _analyze_frame(self, frame: np.ndarray) -> None:
        # Predict emotion
        prediction = self.__predict_emotion(frame)
        
        # Skip if no prediction was made
        if prediction is None:
            return
        
        for i in range(0, len(prediction)):
            label = EMOTION_TYPES[i]
            confidence = prediction[i]

            if label in self._total_confidence_by_emotion:
                self._total_confidence_by_emotion[label] += confidence
                self._prediction_count_by_emotion[label] += 1
            else:
                self._total_confidence_by_emotion[label] = confidence
                self._prediction_count_by_emotion[label] = 1    
    
    
    def _get_final_result(self) -> EmotionsResponse:
        emotions_detail = []
        for label, total in self._total_confidence_by_emotion.items():
            # Calculate the average confidence
            count = self._prediction_count_by_emotion[label]
            average = total / count
            emotions_detail.append(EmotionDetail(
                label=label,
                confidence=Decimal(f"{average:.3f}")
            ))
        result = EmotionsResponse(
            result=emotions_detail,
            video_duration=Decimal(str(self._video_metadata.duration))
        )
        return result


    def __predict_emotion(self, frame: np.ndarray) -> np.ndarray | None:
        """
        Detect faces in the frame and predict the emotion of each face.
        """

        # Convert the frame to a blob
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))
        
        # Detect faces in the frame
        face_model.setInput(blob)
        detections = face_model.forward()

        # Skip if no faces were detected
        total_detected_faces = detections.shape[2]
        if total_detected_faces == 0:
            return None

        # Take the first face
        first_face = detections[0, 0, 0]

        # Check if the confidence of the first detection is enough
        confidence = first_face[2] # Face detection confidence/probability
        if confidence < self._settings.face_detection_confidence:
            return None
        
        # Extract the face from the frame
        face_array = self.__extract_face(frame, first_face)

        # Predict the emotion
        prediction = emotion_model.predict(face_array, verbose=0)[0] # The prediction is a matrix (only take the first row)
        return prediction


    def __extract_face(self, frame: np.ndarray, face: np.ndarray) -> np.ndarray:
        """
        Extracts the face from the frame.
        """
        # Use the bounding box of the detection scaled to the dimensions of the image
        box = face[3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
        (Xi, Yi, Xf, Yf) = box.astype("int")

        # Normalize the bounding box coordinates
        if Xi < 0: Xi = 0
        if Yi < 0: Yi = 0
            
        # Extract the face from the frame, convert it to grayscale and resize it to 48x48
        extracted_face = frame[Yi:Yf, Xi:Xf]
        extracted_face = cv2.cvtColor(extracted_face, cv2.COLOR_BGR2GRAY)
        extracted_face = cv2.resize(extracted_face, (48, 48))
        face_array = img_to_array(extracted_face)
        face_array = np.expand_dims(face_array, axis=0)
        return face_array
