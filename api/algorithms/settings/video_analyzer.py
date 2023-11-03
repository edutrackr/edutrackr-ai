from typing import Literal
from api.common.constants.video import DEFAULT_DISCARDED_FRAMES_VALUE, VideoResolution


class VideoAnalyzerSettings:
    """
    Settings for the video analyzer.
    """
    
    video_resolution: str
    """The resolution to use for the video analysis. This affects the performance of the analysis."""

    discarded_frames: int | Literal["auto"]
    """The number of frames to discard in a second. This affects the performance of the analysis (default: `auto`)."""

    def __init__(
        self,
        video_resolution: str = VideoResolution.LOW,
        discarded_frames: int | Literal["auto"] = DEFAULT_DISCARDED_FRAMES_VALUE,
    ):
        self.video_resolution = video_resolution
        self.discarded_frames = discarded_frames
