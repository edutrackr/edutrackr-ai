from api.algorithms.settings.video_analyzer import VideoAnalyzerSettings


class AttentionLevelSettings:
    """
    Settings for the attention level analyzer.
    """

    eye_ratio_threshold: float
    """The minimum eye aspect ratio for a blink."""

    def __init__(
        self, 
        video: VideoAnalyzerSettings = VideoAnalyzerSettings(),
        eye_ratio_threshold: float = 0.2
    ):
        self.video = video
        self.eye_ratio_threshold = eye_ratio_threshold
