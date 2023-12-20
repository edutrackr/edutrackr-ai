from pydantic import BaseModel
from api.common.annotations import DecimalField


class EmotionsRequest(BaseModel):
    video_id: str


class EmotionDetail(BaseModel):
    label: str
    confidence: DecimalField


class EmotionsPipeResponse(BaseModel):
    result: list[EmotionDetail] = []


class EmotionsResponse(BaseModel):
    result: list[EmotionDetail] = []
    video_duration: DecimalField 


class PartialEmotionsResult(BaseModel):
    total_confidence_by_emotion: dict[str, float]
    """
    The total confidence for each emotion.
    """

    prediction_count_by_emotion: dict[str, int]
    """
    The number of predictions for each emotion.
    """
