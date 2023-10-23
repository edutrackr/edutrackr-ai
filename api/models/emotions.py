from decimal import Decimal
from typing_extensions import Annotated
from pydantic import BaseModel, PlainSerializer


class EmotionsRequest(BaseModel):
    path: str


class EmotionDetail(BaseModel):
    label: str
    confidence: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used='json'),
    ]


class EmotionsResponse(BaseModel):
    result: list[EmotionDetail] = []
