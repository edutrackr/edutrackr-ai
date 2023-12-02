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
import dlib
import numpy as np
from config import AIConfig
from api.common.constants.attention_level import FacialLandmarksIndexes
from api.algorithms.eye_aspect_ratio import original_ear

def extract_landmarks(landmarks, landmarks_indexes):
    (start, end) = landmarks_indexes
    return np.array(
        [(landmarks.part(i).x, landmarks.part(i).y) for i in range(start, end)]
    )

# Umbral de parpadeo
EAR_THRESHOLD = 0.2

# Inicializa la captura de video
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo acceder a la cámara")
    exit()

# Carga el detector de caras y el predictor de puntos faciales
detector = dlib.get_frontal_face_detector() # type: ignore
predictor = dlib.shape_predictor(AIConfig.Blinking.SHAPE_PREDICTOR_PATH) # type: ignore

# Inicializa el contador de parpadeos
blink_count = 0
eye_closed = False

while True:
    # Lee un fotograma del video
    ret, frame = cap.read()

    if not ret:
        break

    # Convierte el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta caras en el fotograma
    faces = detector(gray)[:1]
    if len(faces) == 0:
        continue

    for face in faces:
        shape = predictor(gray, face)

        left_eye = extract_landmarks(shape, FacialLandmarksIndexes.LEFT_EYE)
        right_eye = extract_landmarks(shape, FacialLandmarksIndexes.RIGHT_EYE)

        # Calcula el ratio de aspecto de ambos ojos
        left_ear = original_ear(left_eye)
        right_ear = original_ear(right_eye)

        # Calcula el promedio de los ratios de aspecto de ambos ojos
        ear = (left_ear + right_ear) / 2.0

        # Dibuja los puntos oculares en el fotograma
        for (x, y) in left_eye:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
        for (x, y) in right_eye:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        # Comprueba si el ratio de aspecto indica parpadeo
        if ear < EAR_THRESHOLD:
            # Indica que el ojo está cerrado
            eye_closed = True
        elif ear >= EAR_THRESHOLD and eye_closed:
            # Incrementa el contador de parpadeos
            blink_count += 1
            eye_closed = False
        # Muestra el conteo de parpadeos en el fotograma
        cv2.putText(frame, f"Parpadeos: {blink_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Muestra el fotograma
    cv2.imshow("Detección de Parpadeo", frame)

    # Sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpia y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
