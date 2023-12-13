"""
Utilities for video processing.
"""

import math
import logging
import ffmpeg
from typing import Union
from api.common.constants.video import OPTIMAL_SIZE_BY_ASPECT_RATIO, VideoAspectRatio, VideoResolution
from api.models.videos import VideoMetadata, VideoOptimalSize


logger = logging.getLogger(__name__)

def _parse_video_fps(fps: str) -> float:
    """
    Parse the frame rate of the video (e.g. "30/1").
    """
    fps_str = fps.split('/')
    if len(fps_str) == 1:
        return float(fps)
    else:
        return float(fps_str[0]) / float(fps_str[1])


def _calculate_aspect_ratio(width: int, height: int) -> str:
    """
    Get the aspect ratio of the video in the format of "width:height" (e.g. "16:9").
    """
    gcd = math.gcd(width, height)
    return f"{width // gcd}:{height // gcd}"

     
def extract_metadata(path: str) -> VideoMetadata | None:
    """
    Extract the metadata of a video using FFmpeg.

    Parameters:
        - path: The path to the video file.
    """

    probe = ffmpeg.probe(path)
    raw_metadata = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    if raw_metadata is None:
        return None

    avg_fps = _parse_video_fps(raw_metadata['avg_frame_rate'])
    frame_count = int(raw_metadata['nb_frames'])
    duration = float(raw_metadata['duration'])
    width = int(raw_metadata['width'])
    height = int(raw_metadata['height'])
    aspect_ratio = raw_metadata['display_aspect_ratio'] \
        if 'display_aspect_ratio' in raw_metadata \
        else _calculate_aspect_ratio(width, height)
    
    video_metadata = VideoMetadata(
        video_path=path,
        avg_fps=round(avg_fps, 2),
        frame_count=frame_count,
        duration=round(duration, 2),
        width=width,
        height=height,
        aspect_ratio=aspect_ratio
    )
    return video_metadata


def calculate_optimal_size(video_metadata: VideoMetadata, resolution: str) -> VideoOptimalSize:
    """
    Determine the new optimal width and height of the video based on its aspect ratio.

    Parameters:
        - video_metadata: The video metadata.
        - resolution: The resolution of the video. Use the constants available in `api.common.constants.video.VideoResolution`.
    """

    if resolution == VideoResolution.ORIGINAL or resolution not in OPTIMAL_SIZE_BY_ASPECT_RATIO:
        return VideoOptimalSize(
        width=video_metadata.width,
        height=video_metadata.height,
        resolution=resolution
    )

    config = OPTIMAL_SIZE_BY_ASPECT_RATIO[resolution]
    optimal_width, optimal_height = \
        config[video_metadata.aspect_ratio] if video_metadata.aspect_ratio in config \
        else config[VideoAspectRatio.OTHER]
    
    return VideoOptimalSize(
        width=optimal_width,
        height=optimal_height,
        resolution=resolution
    )


def convert_video(
    input_path: str, 
    output_path: str, 
    fps: int = 30, 
    crf: Union[int, None] = None,
    quiet: bool = True
) -> None:
    """
    Convert a video to a different resolution using FFmpeg.

    Parameters:
        - input_path: The path to the input video file.
        - output_path: The path to the output video file.
        - fps: The frame rate of the video.
        - crf: The constant rate factor (CRF) value used for the video encoding. The value ranges from `0` to `51`, where `0` is lossless, `23` is the default, and `51` is the worst quality possible. The recommended value is `18`.
        - quiet: Whether to hide the FFmpeg output.
    """
    stream = ffmpeg.input(input_path)
    if crf is None:
        stream = stream.output(output_path, r=fps)
    else:
        stream = stream.output(output_path, r=fps, crf=crf)
        
    try:
        stream.run(quiet=quiet, capture_stderr=True)
    except ffmpeg.Error as e:
        logger.error('Error occurred while converting video: %s', e.stderr.decode('utf-8'))
        raise e

