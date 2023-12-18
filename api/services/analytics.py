from decimal import Decimal
from api.algorithms.pipes.attention_level import AttentionLevelPipe
from api.algorithms.pipes.emotions import EmotionsPipe
from api.algorithms.video_analyzer import PipeDict, VideoAnalyzer
from api.algorithms.settings.attention_level import AttentionLevelSettings
from api.algorithms.settings.emotions import EmotionsSettings
from api.algorithms.settings.video_analyzer import VideoAnalyzerSettings
from api.models.attention_level import AttentionLevelPipeResponse, AttentionLevelResponse
from api.models.emotions import EmotionsPipeResponse, EmotionsResponse
from api.models.unified import UnifiedResponse
from api.models.videos import VideoMetadata


def analyze_emotions(video_metadata: VideoMetadata):
    """
    Analyzes the emotions in a video.
    """
    video_settings = VideoAnalyzerSettings(metadata=video_metadata)
    pipes: PipeDict = {
        "emotions": EmotionsPipe(
            EmotionsSettings(video_settings=video_settings)
        )
    }
    video_analyzer = VideoAnalyzer(video_settings, pipes)
    emotions_analysis: EmotionsPipeResponse = video_analyzer.run()["emotions"]
    return EmotionsResponse(
        result=emotions_analysis.result,
        video_duration=Decimal(str(video_settings.metadata.duration)),
    )
    

def analyze_attention_level(video_metadata: VideoMetadata):
    """
    Analyzes the attention level in a video.
    """
    video_settings = VideoAnalyzerSettings(metadata=video_metadata)
    pipes: PipeDict = {
        "attentionLevel": AttentionLevelPipe(
            AttentionLevelSettings(video_settings=video_settings)
        )
    }
    video_analyzer = VideoAnalyzer(video_settings, pipes)
    attention_level_analysis: AttentionLevelPipeResponse = video_analyzer.run()["attentionLevel"]
    return AttentionLevelResponse(
        blink_rate=attention_level_analysis.blink_rate,
        blinks=attention_level_analysis.blinks,
        level=attention_level_analysis.level,
        video_duration=Decimal(str(video_settings.metadata.duration)),
    )


def analyze_unified(video_metadata: VideoMetadata):
    """
    Analyzes all in a video.
    """
    video_settings = VideoAnalyzerSettings(metadata=video_metadata, multithreaded=True)
    pipes: PipeDict = {
        "emotions": EmotionsPipe(
            EmotionsSettings(video_settings=video_settings)
        ),
        "attentionLevel": AttentionLevelPipe(
            AttentionLevelSettings(video_settings=video_settings)
        )
    }
    video_analyzer = VideoAnalyzer(video_settings, pipes)
    video_analysis = video_analyzer.run()
    emotions_analysis: EmotionsPipeResponse | None = video_analysis.get("emotions", None)
    attention_level_analysis: AttentionLevelPipeResponse | None = video_analysis.get("attentionLevel", None)
    return UnifiedResponse(
        emotions=emotions_analysis,
        attention_level=attention_level_analysis,
        video_duration=Decimal(str(video_metadata.duration)),   
    )
