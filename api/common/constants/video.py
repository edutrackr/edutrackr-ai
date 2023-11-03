class VideoResolution:
    ORIGINAL = "original"
    MEDIUM = "medium"
    LOW = "low"


class VideoAspectRatio:
    _4_3 = "4:3"
    _16_9 = "16:9"
    _1_1 = "1:1"
    OTHER = "other"


# Configuration for the optimal size of the video
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
