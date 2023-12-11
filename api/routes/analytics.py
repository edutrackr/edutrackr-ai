from fastapi import APIRouter, status
from api.common.exceptions import AppException
from api.models.base import BaseResponse
from api.services.videos import get_video_metadata
from api.services.analytics import analyze_emotions, analyze_attention_level
from api.models.attention_level import AttentionLevelRequest, AttentionLevelResponse
from api.models.emotions import EmotionsRequest, EmotionsResponse


router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.post("/emotions")
def emotions(request: EmotionsRequest) -> BaseResponse[EmotionsResponse]:
    try:
        video_metadata = get_video_metadata(request.video_id)
        if video_metadata is None:
            raise AppException("Video not found", status_code=status.HTTP_404_NOT_FOUND)
        result = analyze_emotions(video_metadata)
        return BaseResponse(
            success=True, 
            message="Emotions analyzed successfully",
            data=result
        )
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))


@router.post("/attentionLevel")
def blinks(request: AttentionLevelRequest) -> BaseResponse[AttentionLevelResponse]:
    try:
        video_metadata = get_video_metadata(request.video_id)
        if video_metadata is None:
            raise AppException("Video not found", status_code=status.HTTP_404_NOT_FOUND)
        result = analyze_attention_level(video_metadata)
        return BaseResponse(
            success=True, 
            message="Attention level analyzed successfully",
            data=result
        )
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))
