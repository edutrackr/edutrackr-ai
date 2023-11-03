import os
import cv2
import imutils
import numpy as np
from decimal import Decimal
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from api.algorithms.tools import new_video_size
from api.models.emotions import EmotionDetail
from config import AIConfig

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Tipos de emociones del detector
classes = ['angry','disgust','fear','happy','neutral','sad','surprise']

# Cargamos el  modelo de detección de rostros
faceNet = cv2.dnn.readNet(AIConfig.Emotions.PROTOTXT_PATH, AIConfig.Emotions.WEIGHTS_PATH)

# Carga el detector de clasificación de emociones
emotionModel = load_model(AIConfig.Emotions.CLASSIFICATION_MODEL_PATH)


# Retorna las localizaciones de los rostros y las predicciones de emociones de cada rostro
def __predict_emotion(frame,faceNet,emotionModel):
	# Construye un blob de la imagen
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),(104.0, 177.0, 123.0))
	
	# Realiza las detecciones de rostros a partir de la imagen
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# Listas para guardar rostros, ubicaciones y predicciones
	faces = []
	locs = []
	preds = []
	
	# Recorre cada una de las detecciones
	for i in range(0, detections.shape[2]):
		
		# Fija un umbral para determinar que la detección de rostro es confiable
		# Tomando la probabilidad asociada en la deteccion
		if detections[0, 0, i, 2] > 0.4: # TODO: Use from configuration
			# Toma el bounding box de la detección escalado
			# de acuerdo a las dimensiones de la imagen
			box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
			(Xi, Yi, Xf, Yf) = box.astype("int")

			# Valida las dimensiones del bounding box
			if Xi < 0: Xi = 0
			if Yi < 0: Yi = 0
			
			# Se extrae el rostro y se convierte BGR a GRAY
			# Finalmente se escala a 224x244
			face = frame[Yi:Yf, Xi:Xf]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
			face = cv2.resize(face, (48, 48))
			face2 = img_to_array(face)
			face2 = np.expand_dims(face2,axis=0)

			# Se agrega los rostros y las localizaciones a las listas
			faces.append(face2)
			locs.append((Xi, Yi, Xf, Yf))

			pred = emotionModel.predict(face2, verbose=0)
			preds.append(pred[0])

	return (locs,preds)

def analyze_emotions(videopath: str):
    # Iniatialize the video capture object
    video = cv2.VideoCapture(videopath)
    
    # Get the video properties
	new_width, new_height = new_video_size(video)

	totals = {}
	counts = {}
	
	while video.isOpened():

        # Read each frame from the video
        is_processing, frame = video.read()

        if not is_processing:
            break

        # Resize the frame
		frame = cv2.resize(frame, (new_width, new_height))

        # Detect faces and predict emotions
		locs, preds = __predict_emotion(frame, faceNet, emotionModel)
		
        # If not predictions were made, continue
		if len(preds) == 0:
			continue
        
        # Take the first prediction
		pred=preds[0]
		
		for i in range(0, len(pred)):
			label = classes[i]
			confidence = pred[i]

			if label in totals:
				totals[label] += confidence
				counts[label] += 1
			else:
				totals[label] = confidence
				counts[label] = 1	

	result = []
	for label, total in totals.items():
		count = counts[label]
		average = total / count
		roundedConfidence = f"{average:.3f}"
		result.append(EmotionDetail(
			label=label,
			confidence=Decimal(roundedConfidence)
		))
	video.release()
	return result
