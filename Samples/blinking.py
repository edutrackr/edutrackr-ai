import cv2
import dlib
from scipy.spatial import distance
from imutils import face_utils


def eye_aspect_ratio(eye):
    # Calcula la distancia euclidiana entre los puntos verticales de los ojos
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    
    # Calcula la distancia euclidiana entre los puntos horizontalmente
    C = distance.euclidean(eye[0], eye[3])
    
    # Calcula el ratio de aspecto del ojo
    ear = (A + B) / (2.0 * C)
    
    return ear

# Umbral de parpadeo
EAR_THRESHOLD = 0.3

# Inicializa la captura de video
cap = cv2.VideoCapture(0)

# Carga el detector de caras y el predictor de puntos faciales
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Inicializa el contador de parpadeos
blink_count = 0

while True:
    # Lee un fotograma del video
    ret, frame = cap.read()

    if not ret:
        break

    # Convierte el fotograma a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecta caras en el fotograma
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        left_eye = shape[42:48]
        right_eye = shape[36:42]

        # Calcula el ratio de aspecto de ambos ojos
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        # Calcula el promedio de los ratios de aspecto de ambos ojos
        ear = (left_ear + right_ear) / 2.0

        # Dibuja los puntos faciales en el fotograma
        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        # Comprueba si el ratio de aspecto indica parpadeo
        if ear < EAR_THRESHOLD:
            cv2.putText(frame, "Parpadeo detectado", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
             # Incrementa el contador de parpadeos
            blink_count += 1
        # Muestra el conteo de parpadeos en el fotograma
        cv2.putText(frame, f"Parpadeos: {blink_count}", (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Muestra el fotograma
    cv2.imshow("Detección de Parpadeo", frame)

    # Sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpia y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
