from api.algorithms.settings.video_analyzer import VideoAnalyzerSettings
from api.common.constants.attention_level import EyeRatioAlgorithm


class AttentionLevelSettings:
    """
    Settings for the attention level analyzer.
    """

    eye_ratio_threshold: float
    """The minimum eye aspect ratio for a blink."""

    eye_ratio_algorithm: str
    """
    The algorithm to use for computing the eye aspect ratio.
    Use values from `api.common.constants.attention_level.EyeRatioAlgorithm`.
    """

    def __init__(
        self, 
        video: VideoAnalyzerSettings = VideoAnalyzerSettings(),
        eye_ratio_threshold: float = 0.2,
        eye_ratio_algorithm: str = EyeRatioAlgorithm.OPTIMIZED
    ):
        self.video = video
        self.eye_ratio_threshold = eye_ratio_threshold
        self.eye_ratio_algorithm = eye_ratio_algorithm
