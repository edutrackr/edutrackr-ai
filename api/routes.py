from fastapi import APIRouter
from api.auth import APIKeyValidation
from config import AppConfig
from api.common.utils import get_path
from api.models.attention_level import AttentionLevelRequest, AttentionLevelResponse
from api.models.emotions import EmotionsRequest, EmotionsResponse
from api.algorithms.blinking import analyze_blinks
from api.algorithms.emotions import analyze_emotions


router = APIRouter(prefix="/analytics", dependencies=[APIKeyValidation])

@router.post("/emotions")
def emotions(request: EmotionsRequest) -> EmotionsResponse:
    full_path = get_path(AppConfig.STORAGE_PATH, request.path)
    result = analyze_emotions(full_path)
    response_data = EmotionsResponse(result=result)
    return response_data

@router.post("/attentionLevel")
def blinks(request: AttentionLevelRequest) -> AttentionLevelResponse:
    full_path = get_path(AppConfig.STORAGE_PATH, request.path)
    blinks, duration, blink_rate = analyze_blinks(full_path)
    blink_rate_min = (blink_rate)*60
    if blink_rate_min >= 50:
        estado = "Atento"
    elif 36 <= blink_rate_min < 50:
        estado = "Cansado"
    else:
        estado = "Muy cansado"

    response_data = AttentionLevelResponse(
        blinks=blinks,
        duration=duration,
        blink_rate_min=blink_rate_min,
        estado=estado
    )
    return response_data
