from pydantic import BaseModel


class AttentionLevelRequest(BaseModel):
    path: str


class AttentionLevelResponse(BaseModel):
    blinks: int
    duration: float
    blink_rate_min: float
    estado: str
