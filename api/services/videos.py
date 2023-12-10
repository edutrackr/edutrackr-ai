import uuid
from fastapi import UploadFile, status
from api.common.constants.video import VALID_VIDEO_EXTENSIONS, VideoExtension
from api.common.exceptions import AppException
from api.common.utils.file import get_file_extension, remove_file, write_file
from api.common.utils.os import make_dirs, join_path
from api.common.persistence import LocalObjectStore
from api.common.utils.video import convert_video, extract_metadata
from api.models.videos import UploadVideoResponse, VideoMetadata
from config import AppConfig


videos_db = LocalObjectStore(AppConfig.Videos.DB_PATH)


def _convert_video(src_file_path: str, dst_file_path: str, video_content: bytes) -> None:
    # Save temporal video
    write_file(src_file_path, video_content, binary=True)
    # Convert video
    convert_video(src_file_path, dst_file_path, quiet=AppConfig.IS_DEV)
    # Remove temporal video
    remove_file(src_file_path)


def upload_video(video: UploadFile) -> UploadVideoResponse:
    # Validate video extension
    video_extension = get_file_extension(video.filename)
    if video_extension not in VALID_VIDEO_EXTENSIONS:
        raise AppException(
            f"The file must have one of the following extensions: {', '.join(VALID_VIDEO_EXTENSIONS)}",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    file_name = uuid.uuid4()
    video_content = video.file.read()
    dst_file_path = join_path(
        AppConfig.Videos.STORAGE_PATH, 
        f"{file_name}{VideoExtension.MP4}"
    )
    make_dirs(AppConfig.Videos.STORAGE_PATH)

    needs_conversion = video_extension != VideoExtension.MP4
    if needs_conversion:
        src_file_path = join_path(
            AppConfig.Videos.TEMP_PATH, 
            f"{file_name}{video_extension}"
        )
        make_dirs(AppConfig.Videos.TEMP_PATH)
        _convert_video(src_file_path, dst_file_path, video_content)
    else:
        write_file(dst_file_path, video_content, binary=True)

    # Save video metadata
    video_metadata = extract_metadata(dst_file_path)
    if video_metadata is None:
        raise AppException("Unable to extract video metadata")
    video_id = videos_db.add(dict(video_metadata))

    return UploadVideoResponse(
        video_id=video_id
    )


def get_video_metadata(video_id: str) -> VideoMetadata | None:
    video_metadata = videos_db.get_by_id(video_id)
    if video_metadata is None:
        return None
    return VideoMetadata(**video_metadata)


def delete_video(video_id: str) -> None:
    video_metadata = get_video_metadata(video_id)
    if video_metadata is None:
        raise AppException("Video not found", status_code=status.HTTP_404_NOT_FOUND)
    remove_file(video_metadata.video_path)
    videos_db.delete(video_id)


def clear_videos() -> None:
    videos_db.clear()
