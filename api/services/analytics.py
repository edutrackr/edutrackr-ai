from api.algorithms.attention_level import AttentionLevelAnalyzer
from api.algorithms.emotions import EmotionsAnalyzer
from api.algorithms.settings.attention_level import AttentionLevelSettings
from api.algorithms.settings.emotions import EmotionsSettings
from api.algorithms.settings.video_analyzer import VideoAnalyzerSettings
from api.models.videos import VideoMetadata


def analyze_emotions(video_metadata: VideoMetadata):
    """
    Analyzes the emotions in a video.
    """
    settings = EmotionsSettings(
        video_settings=VideoAnalyzerSettings(metadata=video_metadata)
    )
    emotions_analyzer = EmotionsAnalyzer(settings)
    return emotions_analyzer.run()
    

def analyze_attention_level(video_metadata: VideoMetadata):
    """
    Analyzes the attention level in a video.
    """
    settings = AttentionLevelSettings(
        video_settings=VideoAnalyzerSettings(metadata=video_metadata)
    )
    attention_level_analyzer = AttentionLevelAnalyzer(settings)
    return attention_level_analyzer.run()
