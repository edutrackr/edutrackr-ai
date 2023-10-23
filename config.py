import os
from dotenv import load_dotenv
from common.utils import get_env


load_dotenv()

class AppConfig:
    PORT = int(get_env("PORT", 8000))
    STORAGE_PATH = get_env("STORAGE_PATH", os.path.join(os.getcwd(), "video_samples"))

class AIConfig:
    class Blinking:
        SHAPE_PREDICTOR_PATH = "resources/blinking/shape_predictor_68_face_landmarks.dat"

    class Emotions:
        PROTOTXT_PATH = "resources/emotions/face_detector/deploy.prototxt"
        WEIGHTS_PATH = "resources/emotions/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
        CLASSIFICATION_MODEL_PATH = "resources/emotions/modelFEC.h5"
