import os
import sys
from dotenv import load_dotenv
from api.common.constants.runtime import RuntimeArgs
from api.common.utils.os import get_env, get_path
from api.common.utils.runtime import has_arg


app_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(app_path)

IS_DEV = has_arg(RuntimeArgs.DEV_MODE)
if IS_DEV:
    load_dotenv(override=True)

class AppConfig:
    IS_DEV = IS_DEV
    PORT = int(get_env("PORT", 8000))
    STORAGE_PATH = get_env("STORAGE_PATH", os.path.join(os.getcwd(), "tests/videos"))

    class Auth:
        API_KEY = get_env("API_KEY")
        API_KEY_NAME = "api_key"

class AIConfig:
    class Blinking:
        SHAPE_PREDICTOR_PATH = get_path(app_path, "resources/blinking/shape_predictor_68_face_landmarks.dat")

    class Emotions:
        PROTOTXT_PATH = get_path(app_path, "resources/emotions/face_detector/deploy.prototxt")
        WEIGHTS_PATH = get_path(app_path, "resources/emotions/face_detector/res10_300x300_ssd_iter_140000.caffemodel")
        CLASSIFICATION_MODEL_PATH = get_path(app_path, "resources/emotions/modelFEC.h5")
