import uuid
from fastapi import UploadFile, status
from api.common.exceptions import AppException

from api.common.utils.file import check_file, get_file_extension, remove_file, write_file
from api.common.utils.os import make_dirs, join_path
from api.common.persistence import LocalObjectStore
from api.common.utils.video import convert_video
from config import AppConfig


videos_db = LocalObjectStore(AppConfig.Videos.DB_PATH)

def upload_video(video: UploadFile, skip_conversion: bool) -> str:
    # Validate video extension
    video_extension = get_file_extension(video.filename)
    src_video_extension = ".webm"
    if video_extension != src_video_extension:
        raise AppException(f"Video must be in '{src_video_extension}' format", status_code=status.HTTP_400_BAD_REQUEST)
    
    # Save video
    file_name = uuid.uuid4()
    make_dirs(AppConfig.Videos.TEMP_PATH)
    src_file_path = join_path(
        AppConfig.Videos.TEMP_PATH, 
        f"{file_name}{src_video_extension}"
    )
    video_content = video.file.read()
    write_file(src_file_path, video_content, binary=True)

    # Convert video
    dst_video_extension = ".mp4"
    make_dirs(AppConfig.Videos.STORAGE_PATH)
    dst_file_path = join_path(
        AppConfig.Videos.STORAGE_PATH, 
        f"{file_name}{dst_video_extension}"
    )
    convert_video(src_file_path, dst_file_path, quiet=AppConfig.IS_DEV)

    # Remove source video
    remove_file(src_file_path)

    return f"{file_name}{dst_video_extension}"


def delete_video(file_id: str):
    file_path = check_file(f"{AppConfig.Videos.STORAGE_PATH}", f"{file_id}")
    remove_file(file_path)


def clear_videos():
    videos_db.clear()
