from typing import Annotated
from fastapi import APIRouter, Form, UploadFile
from api.common.exceptions import AppException
from api.services.videos import upload_video


router = APIRouter(prefix="/videos")

@router.post("/upload")
def upload(video: UploadFile, skip_conversion: Annotated[bool, Form()] = False):
    try:
        video_path = upload_video(video, skip_conversion)
        return {"message": "Video uploaded successfully", "video_path": video_path}
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))

@router.delete("/delete")
def delete_video(file_id: str):
    try:
        delete_video(file_id)
        return {"message": "Video deleted successfully"}
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))
