from fastapi import APIRouter, UploadFile
from api.common.exceptions import AppException
from api.models.base import BaseResponse, EmptyResponse
from api.models.videos import DeleteVideoRequest, UploadVideoResponse
from api.services.videos import upload_video, delete_video, clear_videos


router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/upload")
def upload(video: UploadFile) -> BaseResponse[UploadVideoResponse]:
    try:
        result = upload_video(video)
        return BaseResponse(
            success=True, 
            message="Video uploaded successfully",
            data=result
        ) 
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))

@router.post("/delete")
def delete(request: DeleteVideoRequest) -> EmptyResponse:
    try:
        delete_video(request.video_id)
        return EmptyResponse(
            success=True, 
            message="Video deleted successfully"
        )
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))

@router.delete("/clear")
def clear() -> EmptyResponse:
    """
    Clears all videos from the database and the storage (use with caution).
    """
    try:
        clear_videos()
        return EmptyResponse(
            success=True, 
            message="Videos cleared successfully"
        )
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))

