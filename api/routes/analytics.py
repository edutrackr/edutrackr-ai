from fastapi import APIRouter, status
from api.common.exceptions import AppException
from config import AppConfig
from api.services.analytics import analyze_emotions, analyze_attention_level
from api.common.utils.os import get_path
from api.models.attention_level import AttentionLevelRequest, AttentionLevelResponse
from api.models.emotions import EmotionsRequest, EmotionsResponse


router = APIRouter(prefix="/analytics")

@router.post("/emotions")
def emotions(request: EmotionsRequest) -> EmotionsResponse:
    try:
        full_path = get_path(AppConfig.STORAGE_PATH, request.path)
        result = analyze_emotions(full_path)
        return result
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))

@router.post("/attentionLevel")
def blinks(request: AttentionLevelRequest) -> AttentionLevelResponse:
    try:
        full_path = get_path(AppConfig.STORAGE_PATH, request.path)
        result = analyze_attention_level(full_path)
        return result
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))
