import os
import cv2
import numpy as np
from decimal import Decimal
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from api.common.constants.emotions import EMOTION_TYPES
from api.common.utils.video import get_video_metadata
from api.models.emotions import EmotionDetail
from config import AIConfig

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Load the face detector model and the emotion classification model
faceModel = cv2.dnn.readNet(AIConfig.Emotions.PROTOTXT_PATH, AIConfig.Emotions.WEIGHTS_PATH) # FaceNet
emotionModel = load_model(AIConfig.Emotions.CLASSIFICATION_MODEL_PATH)

def __predict_emotion(frame, max_faces = 1): #TODO: max_faces
    """
    Detect faces in the frame and predict the emotion of each face
    """

    # Convert the frame to a blob
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))
    
    # Detect faces in the frame
    faceModel.setInput(blob)
    detections = faceModel.forward()

    # Predict emotions for each face detected
    predictions = []
    for i in range(0, detections.shape[2]):
        
        confidence = detections[0, 0, i, 2] # Face detection probability
        if confidence >= AIConfig.VideoProcessing.FACE_DETECTION_CONFIDENCE_THRESHOLD:
            # Toma el bounding box de la detección escalado de acuerdo a las dimensiones de la imagen
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
            prediction = emotionModel.predict(face_array, verbose=0)
            predictions.append(prediction[0])

    return predictions

def analyze_emotions(video_path: str) -> list[EmotionDetail]:
    # Initialize the video capture object
    video = cv2.VideoCapture(video_path)
    
    # Get the video properties
    video_metadata = get_video_metadata(video_path)

    totals = {}
    counts = {}
    while video.isOpened():

        # Read each frame from the video
        is_processing, frame = video.read()
        if not is_processing:
            break

        # Resize the frame
        frame = cv2.resize(frame, (video_metadata.optimal_width, video_metadata.optimal_height))

        # Detect faces and predict emotions
        predictions = __predict_emotion(frame)
        
        # Skip if no faces were detected
        if len(predictions) == 0:
            continue
        
        # Take the first prediction (only one face)
        pred=predictions[0]
        
        for i in range(0, len(pred)):
            label = EMOTION_TYPES[i]
            confidence = pred[i]

            if label in totals:
                totals[label] += confidence
                counts[label] += 1
            else:
                totals[label] = confidence
                counts[label] = 1    

    video.release()

    # Calculate the average confidence for each emotion
    result = []
    for label, total in totals.items():
        count = counts[label]
        average = total / count
        roundedConfidence = f"{average:.3f}"
        result.append(EmotionDetail(
            label=label,
            confidence=Decimal(roundedConfidence)
        ))
    return result
