from pydantic import BaseModel
from api.common.annotations import DecimalField


class AttentionLevelRequest(BaseModel):
    path: str


class AttentionLevelResponse(BaseModel):
    blinks: int
    blink_rate: DecimalField
    level: str
    video_duration: DecimalField 
