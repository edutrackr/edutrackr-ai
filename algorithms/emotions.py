import os
import cv2
import imutils
import numpy as np
from decimal import Decimal
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from api.models.emotions import EmotionDetail

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Tipos de emociones del detector
classes = ['angry','disgust','fear','happy','neutral','sad','surprise']

# Cargamos el  modelo de detección de rostros

prototxtPath = "resources/face_detector/deploy.prototxt"
weightsPath = "resources/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# Carga el detector de clasificación de emociones
emotionModel = load_model("resources/modelFEC.h5")

# Se crea la captura de video

# Toma la imagen, los modelos de detección de rostros y mascarillas 
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
		
		# Fija un umbral para determinar que la detección es confiable
		# Tomando la probabilidad asociada en la deteccion

		if detections[0, 0, i, 2] > 0.4:
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

def analyze_emotions(videopath:str):
	cam = cv2.VideoCapture(videopath)
	# Se toma un frame de la cámara y se redimensiona
	ret, frame = cam.read()
	frame = imutils.resize(frame, width=640)
	(locs, preds) = __predict_emotion(frame,faceNet,emotionModel)
	
	if len(preds)==0:
		return []

	pred=preds[0]
	result = []

	for i in range(0, len(pred)):
		roundedConfidence = "{:.2f}".format(pred[i])
		result.append(EmotionDetail(
			label=classes[i],
			confidence=Decimal(roundedConfidence)
		))

	# Muestra el resultado para la emoción más predominante
	# label = "{}: {:.2f}%".format(classes[np.argmax(pred)], max(angry,disgust,fear,happy,neutral,sad,surprise) * 100)
		
	cam.release()
	return result