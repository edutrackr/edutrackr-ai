from fastapi import APIRouter
from api.models.attention_level import AttentionLevelRequest, AttentionLevelResponse
from api.models.emotions import EmotionsRequest, EmotionsResponse
from algorithms.blinking import analyze_blinks
from algorithms.emotions import analyze_emotions


router = APIRouter(prefix="/analytics")


@router.post("/emotions")
def emotions(request: EmotionsRequest) -> EmotionsResponse:
    root = f"video_samples/emotion/{request.path}.mp4"
    result = analyze_emotions(root)
    response_data = EmotionsResponse(result=result)
    return response_data


@router.post("/attentionLevel")
def blinks(request: AttentionLevelRequest) -> AttentionLevelResponse:
    root = f"video_samples/attention/{request.path}.mp4"
    blinks, duration, blink_rate = analyze_blinks(root)
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
