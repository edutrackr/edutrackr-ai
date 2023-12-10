from typing import Annotated
from fastapi import APIRouter, Form, UploadFile
from api.common.exceptions import AppException
from api.services.videos import upload_video


router = APIRouter(prefix="/videos")

@router.post("/upload")
def upload(video: UploadFile):
    try:
        result = upload_video(video)
        return result
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))

@router.delete("/delete")
def delete_video(video_id: str):
    try:
        delete_video(video_id)
    except AppException as e:
        raise e
    except Exception as e:
        raise AppException(str(e))
