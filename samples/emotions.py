import os
import sys


# Initial setup

app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_path) # This is to allow the import of config.py and any static resource file
os.chdir(app_path) # This is to allow the import any api module

from api.common.constants.runtime import Environment
os.environ[Environment.DEV_MODE] = "true"


###


import cv2
import time
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from config import AIConfig


# Variables para calcular FPS
time_actualframe = 0
time_prevframe = 0

# Tipos de emociones del detector
classes = ['angry','disgust','fear','happy','neutral','sad','surprise']

# Cargamos el  modelo de detección de rostros
faceNet = cv2.dnn.readNet(AIConfig.Emotions.PROTOTXT_PATH, AIConfig.Emotions.WEIGHTS_PATH)

# Carga el detector de clasificación de emociones
emotionModel = load_model(AIConfig.Emotions.CLASSIFICATION_MODEL_PATH)

# Se crea la captura de video
cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

if not cam.isOpened():
    print("No se pudo acceder a la cámara")
    exit()

# Toma la imagen, los modelos de detección de rostros y mascarillas 
# Retorna las localizaciones de los rostros y las predicciones de emociones de cada rostro
def predict_emotion(frame,faceNet,emotionModel):
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
    total_detected_faces = detections.shape[2]
    for i in range(0, total_detected_faces):
        
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

            pred = emotionModel.predict(face2)
            preds.append(pred[0])

    return (locs,preds)

while True:
    # Se toma un frame de la cámara y se redimensiona
    ret, frame = cam.read()
    frame = cv2.resize(frame, (640, 480))

    (locs, preds) = predict_emotion(frame,faceNet,emotionModel)
    
    # Para cada hallazgo se dibuja en la imagen el bounding box y la clase
    for (box, pred) in zip(locs, preds):
        
        (Xi, Yi, Xf, Yf) = box
        (angry,disgust,fear,happy,neutral,sad,surprise) = pred


        label = ''
        # Se agrega la probabilidad en el label de la imagen
        label = "{}: {:.0f}%".format(classes[np.argmax(pred)], max(angry,disgust,fear,happy,neutral,sad,surprise) * 100)

        cv2.rectangle(frame, (Xi, Yi-40), (Xf, Yi), (255,0,0), -1)
        cv2.putText(frame, label, (Xi+5, Yi-15),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        cv2.rectangle(frame, (Xi, Yi), (Xf, Yf), (255,0,0), 3)


    time_actualframe = time.time()

    fps = 0
    if time_actualframe>time_prevframe:
        fps = 1/(time_actualframe-time_prevframe)
    
    time_prevframe = time_actualframe

    cv2.putText(frame, str(int(fps))+" FPS", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3, cv2.LINE_AA)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break

cv2.destroyAllWindows()
cam.release()
