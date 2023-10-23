from dotenv import load_dotenv
from common.utils import get_env

load_dotenv()

class AppConfig:
    PORT = int(get_env("PORT", 8000))
