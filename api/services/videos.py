import uuid
from fastapi import UploadFile, status
from api.common.exceptions import AppException

from api.common.utils.file import get_file_extension, remove_file, write_file
from api.common.utils.os import get_path
from api.common.utils.video import convert_video
from config import AppConfig


def upload_video(video: UploadFile, skip_conversion: bool) -> str:
    # Validate video extension
    video_extension = get_file_extension(video.filename)
    src_video_extension = ".webm"
    if video_extension != src_video_extension:
        raise AppException(f"Video must be in '{src_video_extension}' format", status_code=status.HTTP_400_BAD_REQUEST)
    
    # Save video
    file_name = uuid.uuid4()
    src_file_path = get_path(
        f"{AppConfig.STORAGE_PATH}/temp", 
        f"{file_name}{src_video_extension}",
        ignore_exists=True,
        create_dir=True
    )
    video_content = video.file.read()
    write_file(src_file_path, video_content, binary=True)

    # Convert video
    dst_video_extension = ".mp4"
    dst_file_path = get_path(
        f"{AppConfig.STORAGE_PATH}", 
        f"{file_name}{dst_video_extension}",
        ignore_exists=True,
        create_dir=True
    )
    convert_video(src_file_path, dst_file_path, quiet=AppConfig.IS_DEV)

    # Remove source video
    remove_file(src_file_path)

    return f"{file_name}{dst_video_extension}"


def delete_video(file_id: str):
    file_path = get_path(f"{AppConfig.STORAGE_PATH}", f"{file_id}")
    remove_file(file_path)
