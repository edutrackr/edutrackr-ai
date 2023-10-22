from typing_extensions import Annotated
from pydantic import BaseModel, PlainSerializer
from decimal import Decimal



class EmotionDetail(BaseModel):
    label: str
    confidence : Annotated[
        Decimal,
        PlainSerializer( lambda x: float(x), return_type=float, when_used='json'),
    ] 
class EmotionResponse(BaseModel):
    result : list[EmotionDetail]= []