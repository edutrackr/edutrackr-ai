from pydantic import BaseModel


class UploadVideoResponse(BaseModel):
    
    video_id: str


class DeleteVideoRequest(BaseModel):
    
    video_id: str


class BaseVideoMetadata(BaseModel):

    video_path: str
    """Path to the video."""

    frame_count: int
    """Number of frames in the video."""

    width: int
    """Original width of the video in pixels."""

    height: int
    """Original height of the video in pixels."""

    aspect_ratio: str
    """Aspect ratio of the video in the format of "width:height" (e.g. "16:9")."""


class FullVideoMetadata(BaseVideoMetadata):

    avg_fps: float
    """Average FPS of the video (rounded to 2 decimal places)."""

    duration: float
    """Duration of the video in seconds (rounded to 2 decimal places)."""


class VideoOptimalSize(BaseModel):

    width: int
    """Optimal width of the video in pixels based on its aspect ratio."""

    height: int
    """Optimal height of the video in pixels based on its aspect ratio."""
    
    resolution: str
    """Video resolution based on the constants in `api.common.constants.video.VideoResolution`."""
