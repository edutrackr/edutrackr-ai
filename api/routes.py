from api.models.emotion_response  import EmotionResponse
from api.models.blink_response  import BlinkResponse 
from algorithms.attention_level.attention import detect_blinks
from algorithms.emotion_detection.emotion import emotionR
from fastapi import APIRouter
from pydantic import BaseModel

class EmotionRequest (BaseModel):
    path :str

class AttentionRequest(BaseModel):
    path : str

router = APIRouter()

@router.post("/emotions")
def emotions(request : EmotionRequest) -> EmotionResponse:
    root=f"video_samples/emotion/{request.path}.mp4"
    result =emotionR(root)
    response_data = EmotionResponse(result=result)
    return response_data
    

@router.post("/attention")
def blinks(request: AttentionRequest)->BlinkResponse:
    root=f"video_samples/attention/{request.path}.mp4"
    blinks, duration, blink_rate = detect_blinks(root)
    blink_rate_min= (blink_rate)*60
    if blink_rate_min >= 50:
        estado = "Atento"
    elif 36 <= blink_rate_min < 50:
        estado = "Cansado"
    else:
        estado = "Muy cansado"

    response_data = BlinkResponse(
        blinks=blinks,
        duration=duration,
        blink_rate_min=blink_rate_min,
        estado=estado
    )
    return response_data