from fastapi import APIRouter, UploadFile
from api.common.exceptions import AppException
from api.models.videos import DeleteVideoRequest
from api.services.videos import upload_video, delete_video


router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/upload")
def upload(video: UploadFile):
    try:
        result = upload_video(video)
        return result
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))

@router.post("/delete")
def delete(request: DeleteVideoRequest):
    try:
        delete_video(request.video_id)
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))
