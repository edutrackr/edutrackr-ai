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

    __face_model: any
    """
    The face detector model (based on FaceNet).
    """

    __emotion_model: any
    """
    The emotion classification model.
    """


    def __init__(self, settings: EmotionsSettings):
        super().__init__(settings.video)
        self._settings = settings
        self.__face_model = cv2.dnn.readNet(AIConfig.Emotions.PROTOTXT_PATH, AIConfig.Emotions.WEIGHTS_PATH)
        self.__emotion_model = load_model(AIConfig.Emotions.CLASSIFICATION_MODEL_PATH)


    def _reset_state(self) -> None:
        self._total_confidence_by_emotion = {}
        self._prediction_count_by_emotion = {}


    def _analyze_frame(self, frame: np.ndarray) -> None:
        # Detect faces and predict emotions
        predictions = self.__predict_emotion(frame)
        
        # Skip if no faces were detected
        if len(predictions) == 0:
            return
        
        # Take the first prediction (only one face)
        pred = predictions[0]
        
        for i in range(0, len(pred)):
            label = EMOTION_TYPES[i]
            confidence = pred[i]

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
            result=emotions_detail
        )
        return result


    def __predict_emotion(self, frame, max_faces = 1): #TODO: max_faces
        """
        Detect faces in the frame and predict the emotion of each face.
        """

        # Convert the frame to a blob
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))
        
        # Detect faces in the frame
        self.__face_model.setInput(blob)
        detections = self.__face_model.forward()

        # Predict emotions for each face detected
        predictions = []
        for i in range(0, detections.shape[2]): # TODO: Replace with max_faces
            
            confidence = detections[0, 0, i, 2] # Face detection probability
            if confidence >= self._settings.face_detection_confidence:
                
                # Use the bounding box of the detection scaled to the dimensions of the image
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (Xi, Yi, Xf, Yf) = box.astype("int")

                # Normalize the bounding box coordinates
                if Xi < 0: Xi = 0
                if Yi < 0: Yi = 0
                
                # Extract the face from the frame, convert it to grayscale and resize it to 48x48
                face = frame[Yi:Yf, Xi:Xf]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (48, 48))
                face_array = img_to_array(face)
                face_array = np.expand_dims(face_array, axis=0)

                # Predict the emotion
                prediction = self.__emotion_model.predict(face_array, verbose=0)
                predictions.append(prediction[0])

        return predictions
