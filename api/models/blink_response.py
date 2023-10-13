from pydantic import BaseModel

class BlinkResponse(BaseModel):
    blinks: int
    duration: float
    blink_rate_min: float
    estado: str