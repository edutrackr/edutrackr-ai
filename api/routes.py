from api.models.emotion_response  import EmotionResponse
from api.models.blink_response  import BlinkResponse 
from algorithms.attention_level.attention import detect_blinks
from algorithms.emotion_detection.emotion import emotionR
from fastapi import APIRouter

router = APIRouter()

@router.get("/emotions/{path}")
def emotions(path:str):
    root=f"video_samples/emotion/{path}.mp4"
    emotion,percentage =emotionR(root)
    response_data = EmotionResponse(emotion=emotion, percentage=percentage)
    return response_data
    

@router.get("/blinks/{path}")
def blinks(path:str):
    root=f"video_samples/attention/{path}.mp4"
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