from pydantic import BaseModel
from api.common.annotations import DecimalField


class AttentionLevelRequest(BaseModel):
    video_id: str


class AttentionLevelPipeResponse(BaseModel):
    blinks: int
    blink_rate: DecimalField
    level: str

class AttentionLevelResponse(BaseModel):
    blinks: int
    blink_rate: DecimalField
    level: str
    video_duration: DecimalField 
