from fastapi import APIRouter
from api.auth import APIKeyValidation
from api.common.constants.attention_level import AttentionLevelStatus
from config import AppConfig
from api.common.utils.os import get_path
from api.models.attention_level import AttentionLevelRequest, AttentionLevelResponse
from api.models.emotions import EmotionsRequest, EmotionsResponse
from api.algorithms.blinking import analyze_blinks
from api.algorithms.emotions import analyze_emotions

def __calculate_attention_level(blink_rate_per_minute):
    if blink_rate_per_minute >= 50:
        status = AttentionLevelStatus.HIGH
    elif 36 <= blink_rate_per_minute < 50:
        status = AttentionLevelStatus.MEDIUM
    else:
        status = AttentionLevelStatus.LOW
    return status


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
    blink_rate_per_minute = blink_rate * 60

    response_data = AttentionLevelResponse(
        blinks=blinks,
        duration=duration,
        blink_rate=blink_rate_per_minute,
        level=__calculate_attention_level(blink_rate_per_minute)
    )
    return response_data
