from pydantic import BaseModel


class AttentionLevelRequest(BaseModel):
    path: str


class AttentionLevelResponse(BaseModel):
    blinks: int
    duration: float
    blink_rate: float
    status: str
