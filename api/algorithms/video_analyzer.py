import cv2
import numpy as np
from typing import Generic, TypeVar
from api.algorithms.settings.video_analyzer import VideoAnalyzerSettings
from api.common.utils.os import path_exists
from api.common.utils.video import VideoMetadata, get_video_metadata
from api.common.constants.video import DEFAULT_DISCARDED_FRAMES_RATE, DEFAULT_DISCARDED_FRAMES_VALUE


TResult = TypeVar("TResult")

class BaseVideoAnalyzer(Generic[TResult]):
    """
    Base class for AI video analyzers.
    """

    _video_settings: VideoAnalyzerSettings
    """
    The video settings for the analyzer.
    """

    _video_metadata: VideoMetadata
    """
    The video metadata. Available after the video is opened (in the run method).
    """


    def __init__(self, video_settings: VideoAnalyzerSettings):
        self._video_settings = video_settings


    def run(self, video_path: str) -> TResult:
        """
        Run the analysis on the video.
        """

        # Validate the video path
        if not path_exists(video_path):
            raise FileNotFoundError(f"Video file not found: '{video_path}'")

        # Initialize the video capture object
        video = cv2.VideoCapture(video_path)

        # Get the video metadata
        video_metadata = get_video_metadata(video_path, self._video_settings.video_resolution)
        if video_metadata is None:
            raise Exception("Unable to get video metadata")
        self._video_metadata = video_metadata

        discarded_frames = self._calculate_discarded_frames()

        skipped_frames = 0
        self._reset_state()
        while video.isOpened():
            # Read each frame from the video
            is_processing, frame = video.read()
            if not is_processing:
                break

            # Validate skipped frames
            if skipped_frames < discarded_frames:
                skipped_frames += 1
                continue
            else:
                skipped_frames = 0

            # Resize the frame
            frame = cv2.resize(frame, (
                self._video_metadata.optimal_width,
                self._video_metadata.optimal_height
            ))

            # Analyze the frame
            self._analyze_frame(frame)

        video.release()
        # Get the final result
        return self._get_final_result()


    def _calculate_discarded_frames(self) -> int:
        """
        Calculate the number of frames to discard
        """
        if self._video_settings.discarded_frames == DEFAULT_DISCARDED_FRAMES_VALUE:
            return int(self._video_metadata.avg_fps * DEFAULT_DISCARDED_FRAMES_RATE)
        else:
            return self._video_settings.discarded_frames


    def _reset_state(self) -> None:
        """
        Reset the analyzer state.
        """
        raise NotImplementedError("Must be implemented in a child class")


    def _analyze_frame(self, frame: np.ndarray) -> None:
        """
        Analyze a frame from the video.
        """
        raise NotImplementedError("Must be implemented in a child class")


    def _get_final_result(self) -> TResult:
        """
        Get the final result from the analysis.
        """
        raise NotImplementedError("Must be implemented in a child class")
