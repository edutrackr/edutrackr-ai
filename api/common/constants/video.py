class VideoResolution:
    ORIGINAL = "original"
    MEDIUM = "medium"
    LOW = "low"


class VideoAspectRatio:
    _4_3 = "4:3"
    _16_9 = "16:9"
    _1_1 = "1:1"
    OTHER = "other"


class VideoExtension:
    MP4 = ".mp4"
    WEBM = ".webm"


VALID_VIDEO_EXTENSIONS = [VideoExtension.MP4, VideoExtension.WEBM]
"""Valid video extensions."""


OPTIMAL_SIZE_BY_ASPECT_RATIO: dict[str, dict[str, tuple[int, int]]] = {
    VideoResolution.MEDIUM: {
        VideoAspectRatio._4_3: (600, 450),
        VideoAspectRatio._16_9: (640, 360),
        VideoAspectRatio._1_1: (600, 600),
        VideoAspectRatio.OTHER: (600, 450)
    },
    VideoResolution.LOW: {
        VideoAspectRatio._4_3: (480, 360),
        VideoAspectRatio._16_9: (480, 270),
        VideoAspectRatio._1_1: (480, 480),
        VideoAspectRatio.OTHER: (480, 360)
    }
}
"""
Configuration for the optimal size of the video based on the aspect ratioa and the resolution.
"""


DEFAULT_DISCARDED_FRAMES_VALUE = "auto"
"""The default value for the number of frames to discard in a second."""

DEFAULT_DISCARDED_FRAMES_RATE = 0.1
"""The sample rate should not be higher than 10% of FPS to avoid loosing analysis quality."""
