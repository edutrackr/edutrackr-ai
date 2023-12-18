from typing import Any
import cv2
import numpy as np
from api.algorithms.pipes.base import BaseAnalysisPipe
from api.algorithms.settings.video_analyzer import VideoAnalyzerSettings
from api.common.utils.os import path_exists
from api.common.constants.video import DEFAULT_DISCARDED_FRAMES_RATE, DEFAULT_DISCARDED_FRAMES_VALUE
from api.common.utils.video import calculate_optimal_size
from api.models.videos import VideoOptimalSize


PipeDict = dict[str, BaseAnalysisPipe[Any]]
AnalysisResult = dict[str, Any]

class VideoAnalyzer:
    """
    Base class for AI video analyzers.
    """

    _video_settings: VideoAnalyzerSettings
    """
    The video settings for the analyzer.
    """

    _video_optimal_size: VideoOptimalSize
    """
    The optimal size for the video.
    """

    _discarded_frames: int
    """
    The number of frames to discard.
    """

    _pipes: PipeDict
    """
    The list of pipes to use in the analysis.
    """


    def __init__(self, video_settings: VideoAnalyzerSettings, pipes: PipeDict):
        self._video_settings = video_settings
        self._video_optimal_size = self._calculate_optimal_size()
        self._discarded_frames = self._calculate_discarded_frames()
        self._pipes = pipes


    def run(self) -> AnalysisResult:
        """
        Run the analysis on the video. Returns a dictionary with the results (one for each pipe).
        """

        # Validate the video path
        video_path = self._video_settings.metadata.video_path
        if not path_exists(video_path):
            raise FileNotFoundError(f"File not found: '{video_path}'")

        # Initialize the video capture object
        video = cv2.VideoCapture(video_path)

        skipped_frames = 0
        while video.isOpened():
            # Read each frame from the video
            is_processing, frame = video.read()
            if not is_processing:
                break

            # Validate skipped frames
            if skipped_frames < self._discarded_frames:
                skipped_frames += 1
                continue
            else:
                skipped_frames = 0

            # Resize the frame
            frame = cv2.resize(frame, (
                self._video_optimal_size.width,
                self._video_optimal_size.height
            ))

            # Analyze the frame
            self._analyze(frame)

        video.release()
        # Get the final result
        return self._get_result()

    
    def _calculate_optimal_size(self) -> VideoOptimalSize:
        """
        Calculate the optimal size for the video.
        """
        return calculate_optimal_size(
            self._video_settings.metadata, 
            self._video_settings.video_resolution
        )


    def _calculate_discarded_frames(self) -> int:
        """
        Calculate the number of frames to discard.
        """
        if self._video_settings.discarded_frames == DEFAULT_DISCARDED_FRAMES_VALUE:
            return int(self._video_settings.metadata.avg_fps * DEFAULT_DISCARDED_FRAMES_RATE)
        else:
            return self._video_settings.discarded_frames


    def _analyze(self, frame: np.ndarray) -> None:
        """
        Analyze a frame from the video.
        """
        for pipe in self._pipes.values():
            pipe.analyze_frame(frame)


    def _get_result(self) -> AnalysisResult:
        """
        Get the final result from the analysis.
        """
        result = {}
        for pipe_key, pipe_value in self._pipes.items():
            result[pipe_key] = pipe_value.get_final_result()        
        return result
        
