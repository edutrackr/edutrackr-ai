"""
Utility functions for video processing.
"""

import math
from typing import Union
import ffmpeg
from api.common.constants.video import OPTIMAL_SIZE_BY_ASPECT_RATIO, VideoAspectRatio


class VideoMetadata:
    avg_fps: float
    """Average FPS of the video (rounded to 2 decimal places)."""

    frame_count: int
    """Number of frames in the video."""

    duration: float
    """Duration of the video in seconds (rounded to 2 decimal places)."""

    original_width: int
    """Original width of the video in pixels."""

    optimal_width: int
    """Optimal width of the video in pixels based on its aspect ratio."""

    original_height: int
    """Original height of the video in pixels."""

    optimal_height: int
    """Optimal height of the video in pixels based on its aspect ratio."""

    aspect_ratio: str
    """Aspect ratio of the video in the format of "width:height" (e.g. "16:9")."""

    video_resolution: str
    """Video resolution based on the constants in `api.common.constants.video.VideoResolution`."""

    def __init__(self, raw_metadata: dict, resolution: str):
        """
        Initialize a new VideoMetadata object from a dictionary containing the raw metadata of a video using FFmpeg.
        """

        self.avg_fps = round(self.__parse_video_fps(raw_metadata['avg_frame_rate']), 2)
        self.frame_count = int(raw_metadata['nb_frames'])
        self.duration = round(float(raw_metadata['duration']), 2)
        self.original_width = int(raw_metadata['width'])
        self.original_height = int(raw_metadata['height'])
        self.aspect_ratio = self.__get_aspect_ratio(raw_metadata, 'display_aspect_ratio')
        self.video_resolution = resolution
        self.optimal_width, self.optimal_height = self.__calculate_optimal_size()

    def __get_aspect_ratio(self, raw_metadata: dict, aspect_ratio_key: str) -> str:
        """
        Get the aspect ratio of the video in the format of "width:height" (e.g. "16:9").
        """

        if raw_metadata.get(aspect_ratio_key) is not None:
            return raw_metadata[aspect_ratio_key]
        else:
            gcd = math.gcd(self.original_width, self.original_height)
            return f"{self.original_width // gcd}:{self.original_height // gcd}"
        
    def __calculate_optimal_size(self) -> tuple[int, int]:
        """
        Determine the new optimal width and height of the video based on its aspect ratio.
        """

        if self.video_resolution == "original" or self.video_resolution not in OPTIMAL_SIZE_BY_ASPECT_RATIO:
            return self.original_width, self.original_height

        config = OPTIMAL_SIZE_BY_ASPECT_RATIO[self.video_resolution]
        if self.aspect_ratio in config:
            return config[self.aspect_ratio]
        else:
            return config[VideoAspectRatio.OTHER]

    def __parse_video_fps(self, fps: str) -> float:
        fps_str = fps.split('/')
        if len(fps_str) == 1:
            return float(fps)
        else:
            return float(fps_str[0]) / float(fps_str[1])

    def to_dict(self) -> dict:
        return {
            "avg_fps": self.avg_fps,
            "frame_count": self.frame_count,
            "duration": self.duration,
            "original_width": self.original_width,
            "optimal_width": self.optimal_width,
            "original_height": self.original_height,
            "optimal_height": self.optimal_height,
            "aspect_ratio": self.aspect_ratio,
            "video_resolution": self.video_resolution
        }
    
    def __repr__(self) -> str:
        return f"VideoMetadata({self.to_dict()})"


def get_video_metadata(
    path: str, 
    resolution: str
) -> VideoMetadata | None:
    """
    Get the metadata of a video using FFmpeg.

    Parameters:
        - path: The path to the video file.
        - resolution: The resolution of the video. Use the constants available in `api.common.constants.video.VideoResolution`.
    """

    probe = ffmpeg.probe(path)
    raw_metadata = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    if raw_metadata is None:
        return None

    return VideoMetadata(
        raw_metadata=raw_metadata,
        resolution=resolution
    )

def convert_video(
    input_path: str, 
    output_path: str, 
    fps: int = 30, 
    crf: Union[int, None] = None,
) -> None:
    """
    Convert a video to a different resolution using FFmpeg.

    Parameters:
        - input_path: The path to the input video file.
        - output_path: The path to the output video file.
        - fps: The frame rate of the video. The default value is 30.
        - crf: The constant rate factor (CRF) value used for the video encoding. The value ranges from 0 to 51, where 0 is lossless, 23 is the default, and 51 is the worst quality possible. The recommended value is 18.
    """

    stream = ffmpeg.input(input_path)
    if crf is None:
        stream = stream.output(output_path, r=fps)
    else:
        stream = stream.output(output_path, r=fps, crf=crf)
    stream.run()
