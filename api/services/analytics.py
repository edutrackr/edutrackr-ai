from decimal import Decimal
from fastapi import status
from api.algorithms.pipes.attention_level import AttentionLevelPipe
from api.algorithms.pipes.emotions import EmotionsPipe
from api.algorithms.video_analyzer import PipeDict, VideoAnalyzer
from api.algorithms.settings.attention_level import AttentionLevelSettings
from api.algorithms.settings.emotions import EmotionsSettings
from api.algorithms.settings.video_analyzer import VideoAnalyzerSettings
from api.common.exceptions import AppException
from api.models.attention_level import AttentionLevelPipeResponse, AttentionLevelResponse
from api.models.emotions import EmotionsPipeResponse, EmotionsResponse
from api.models.unified import UnifiedResponse
from api.models.videos import FullVideoMetadata


def analyze_emotions(video_metadata: FullVideoMetadata):
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
    

def analyze_attention_level(video_metadata: FullVideoMetadata):
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


def analyze_unified(video_metadata: FullVideoMetadata):
    """
    Analyzes all in a video.
    """
    video_settings = VideoAnalyzerSettings(metadata=video_metadata, multithreaded=True)
    pipes: PipeDict = {
        "emotions": EmotionsPipe(
            EmotionsSettings(video_settings=video_settings)
        ),
    }
    video_analyzer = VideoAnalyzer(video_settings, pipes)
    video_analysis = video_analyzer.run()
    emotions_analysis: EmotionsPipeResponse | None = video_analysis.get("emotions", None)
    if emotions_analysis is None:
        raise AppException(
            description="Unable to analyze video (all pipes failed)",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return UnifiedResponse(
        emotions=emotions_analysis,
        video_duration=Decimal(str(video_metadata.duration)),   
    )
