from api.algorithms.settings.video_analyzer import VideoAnalyzerSettings


class EmotionsSettings:
    """
    Settings for the emotions analyzer.
    """

    face_detection_confidence: float
    """The minimum confidence threshold to use for face detection."""

    def __init__(
        self, 
        video_settings: VideoAnalyzerSettings,
        face_detection_confidence: float = 0.4
    ):
        self.video_settings = video_settings
        self.face_detection_confidence = face_detection_confidence
