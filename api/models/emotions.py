from pydantic import BaseModel
from api.common.annotations import DecimalField


class EmotionsRequest(BaseModel):
    path: str


class EmotionDetail(BaseModel):
    label: str
    confidence: DecimalField


class EmotionsResponse(BaseModel):
    result: list[EmotionDetail] = []
