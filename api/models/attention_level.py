from pydantic import BaseModel,PlainSerializer
from decimal import Decimal
from typing_extensions import Annotated


class AttentionLevelRequest(BaseModel):
    path: str


class AttentionLevelResponse(BaseModel):
    blinks: int
    duration: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used='json'),
    ]
    blink_rate: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used='json'),
    ]
    status: str
