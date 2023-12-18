from pydantic import BaseModel
from api.common.annotations import DecimalField
from api.models.attention_level import AttentionLevelPipeResponse
from api.models.emotions import EmotionsPipeResponse


class UnifiedRequest(BaseModel):
    video_id: str


class UnifiedResponse(BaseModel):
    emotions: EmotionsPipeResponse
    attention_level: AttentionLevelPipeResponse
    video_duration: DecimalField 
