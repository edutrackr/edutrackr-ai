from api.algorithms.attention_level import AttentionLevelAnalyzer
from api.algorithms.emotions import EmotionsAnalyzer
from api.algorithms.settings.attention_level import AttentionLevelSettings
from api.algorithms.settings.emotions import EmotionsSettings


def analyze_emotions(video_path: str):
    """
    Analyzes the emotions in a video.
    """
    emotions_analyzer = EmotionsAnalyzer(EmotionsSettings())
    return emotions_analyzer.run(video_path)
    

def analyze_attention_level(video_path: str):
    """
    Analyzes the attention level in a video.
    """
    attention_level_analyzer = AttentionLevelAnalyzer(AttentionLevelSettings())
    return attention_level_analyzer.run(video_path)
