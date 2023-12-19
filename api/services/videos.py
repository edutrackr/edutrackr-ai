import uuid
from fastapi import UploadFile, status
from api.common.constants.video import VALID_VIDEO_EXTENSIONS, VideoExtension
from api.common.exceptions import AppException
from api.common.utils.file import get_file_extension, remove_dir_contents, remove_file, write_file
from api.common.utils.os import make_dirs, join_path
from api.persistence.factory import get_object_store
from api.common.utils.video import convert_video, extract_metadata, extract_stream_metadata
from api.models.videos import UploadVideoResponse, FullVideoMetadata
from config import AppConfig


videos_db = get_object_store(AppConfig.Videos.DB_STRATEGY, AppConfig.Videos.DB_PATH)


def _convert_video(src_file_path: str, dst_file_path: str, video_content: bytes) -> None:
    # Save temporal video
    write_file(src_file_path, video_content, binary=True)
    # Convert video
    convert_video(src_file_path, dst_file_path, quiet=AppConfig.IS_DEV)
    # Remove temporal video
    remove_file(src_file_path)


def _get_stream_metadata(dst_file_path: str, tmp_file_path: str) -> FullVideoMetadata | None:
    # Convert video
    convert_video(dst_file_path, tmp_file_path, crf=50, quiet=AppConfig.IS_DEV)
    # Extract destination video metadata
    dst_video_metadata = extract_stream_metadata(dst_file_path)
    # Extract temporal video metadata
    tmp_video_metadata = extract_metadata(tmp_file_path)
    # Remove temporal video
    remove_file(tmp_file_path)

    if dst_video_metadata is None or tmp_video_metadata is None:
        return None
    
    avg_fps = round(dst_video_metadata.frame_count / tmp_video_metadata.duration, 2)
    return FullVideoMetadata(
        video_path=dst_file_path,
        avg_fps=avg_fps,
        frame_count=dst_video_metadata.frame_count,
        duration=tmp_video_metadata.duration,
        width=dst_video_metadata.width,
        height=dst_video_metadata.height,
        aspect_ratio=dst_video_metadata.aspect_ratio
    )


def upload_video(video: UploadFile, convert_video: bool) -> UploadVideoResponse:
    # Validate video extension
    video_extension = get_file_extension(video.filename)
    if video_extension not in VALID_VIDEO_EXTENSIONS:
        raise AppException(
            f"The file must have one of the following extensions: {', '.join(VALID_VIDEO_EXTENSIONS)}",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    needs_conversion = convert_video and video_extension != VideoExtension.MP4

    file_name = uuid.uuid4()
    video_content = video.file.read()
    dst_file_extension = VideoExtension.MP4 if needs_conversion else video_extension

    dst_file_path = join_path(
        AppConfig.Videos.STORAGE_PATH, 
        f"{file_name}{dst_file_extension}"
    )
    make_dirs(AppConfig.Videos.STORAGE_PATH)

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
    if dst_file_extension == VideoExtension.WEBM:
        tmp_file_path = join_path(
            AppConfig.Videos.TEMP_PATH, 
            f"{file_name}{VideoExtension.MP4}"
        )
        video_metadata = _get_stream_metadata(dst_file_path, tmp_file_path)
    else:
        video_metadata = extract_metadata(dst_file_path)
    if video_metadata is None:
        raise AppException("Unable to extract video metadata")
    video_id = videos_db.add(dict(video_metadata))
    if video_id is None:
        raise AppException("Unable to save video metadata")

    return UploadVideoResponse(
        video_id=video_id
    )


def get_video_metadata(video_id: str) -> FullVideoMetadata | None:
    video_metadata = videos_db.get_by_id(video_id)
    if video_metadata is None:
        return None
    return FullVideoMetadata(**video_metadata)


def delete_video(video_id: str) -> None:
    video_metadata = get_video_metadata(video_id)
    if video_metadata is None:
        raise AppException("Video not found", status_code=status.HTTP_404_NOT_FOUND)
    remove_file(video_metadata.video_path)
    videos_db.delete(video_id)


def clear_videos() -> None:
    videos_db.clear()
    remove_dir_contents(AppConfig.Videos.STORAGE_PATH)
    remove_dir_contents(AppConfig.Videos.TEMP_PATH)
