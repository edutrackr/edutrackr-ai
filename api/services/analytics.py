from api.algorithms.attention_level import AttentionLevelAnalyzer
from api.algorithms.emotions import EmotionsAnalyzer
from api.algorithms.settings.attention_level import AttentionLevelSettings
from api.algorithms.settings.emotions import EmotionsSettings

__emotions_analyzer = EmotionsAnalyzer(EmotionsSettings())
__attention_level_analyzer = AttentionLevelAnalyzer(AttentionLevelSettings())

def analyze_emotions(video_path: str):
    """
    Analyzes the emotions in a video.
    """
    return __emotions_analyzer.run(video_path)
    

def analyze_attention_level(video_path: str):
    """
    Analyzes the attention level in a video.
    """
    return __attention_level_analyzer.run(video_path)
