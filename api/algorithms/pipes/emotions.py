import os
import cv2
import numpy as np
from decimal import Decimal
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from api.algorithms.pipes.base import BaseAnalysisPipe
from api.algorithms.settings.emotions import EmotionsSettings
from api.common.constants.emotions import EMOTION_TYPES
from api.models.emotions import EmotionDetail, EmotionsPipeResponse, PartialEmotionsResult
from config import AIConfig


# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

emotion_model: any = load_model(AIConfig.Emotions.CLASSIFICATION_MODEL_PATH) # type: ignore
"""
The emotion classification model.
"""


class EmotionsPipe(BaseAnalysisPipe[EmotionsPipeResponse]):
    """
    Pipe for the emotions algorithm.
    """
    
    _settings: EmotionsSettings
    """
    The settings for the pipe.
    """

    _face_model: cv2.dnn.Net
    """
    The face detector model (based on FaceNet).
    """

    _extracted_faces: np.ndarray
    """
    The extracted faces from each frame of the video. Only the first face of each frame is extracted.
    """


    def __init__(self, settings: EmotionsSettings):
        super().__init__()
        self._settings = settings
        self._face_model = cv2.dnn.readNet(AIConfig.Emotions.PROTOTXT_PATH, AIConfig.Emotions.WEIGHTS_PATH)


    def reset_state(self) -> None:
        self._extracted_faces = np.array([])


    def _analyze_frame(self, frame: np.ndarray) -> None:
        extracted_face = self.__predict_face(frame)
        if extracted_face is None or extracted_face.size == 0: # Skip if no face was detected
            return
        self._extracted_faces = extracted_face if self._extracted_faces.size == 0 \
            else np.concatenate((self._extracted_faces, extracted_face), axis=0)
    
    
    def get_final_result(self) -> EmotionsPipeResponse:
        emotions_detail = []
        partial_result = self.__predict_emotions()
        for label, total in partial_result.total_confidence_by_emotion.items():
            # Calculate the average confidence
            count = partial_result.prediction_count_by_emotion[label]
            average = total / count
            emotions_detail.append(EmotionDetail(
                label=label,
                confidence=Decimal(f"{average:.3f}")
            ))
        result = EmotionsPipeResponse(
            result=emotions_detail,
        )
        return result


    def __predict_face(self, frame: np.ndarray) -> np.ndarray | None:
        """
        Detect faces in the frame and extract the first one.
        """

        # Convert the frame to a blob
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))
        
        # Detect faces in the frame
        self._face_model.setInput(blob)
        detections = self._face_model.forward()

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
        return face_array


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
    

    def __predict_emotions(self) -> PartialEmotionsResult:
        """
        Predict the emotion of all the extracted faces.
        """
        
        partial_result = PartialEmotionsResult(
            total_confidence_by_emotion={},
            prediction_count_by_emotion={}
        )
        if self._extracted_faces.size == 0:
            return partial_result

        # Predict emotions
        predictions = emotion_model.predict(self._extracted_faces, verbose=0)
       
        for prediction in predictions:
            for i in range(0, len(prediction)):
                label = EMOTION_TYPES[i]
                confidence = prediction[i]
                if label in partial_result.total_confidence_by_emotion:
                    partial_result.total_confidence_by_emotion[label] += confidence
                    partial_result.prediction_count_by_emotion[label] += 1
                else:
                    partial_result.total_confidence_by_emotion[label] = confidence
                    partial_result.prediction_count_by_emotion[label] = 1

        return partial_result
