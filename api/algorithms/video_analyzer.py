from typing import Any
import cv2
import numpy as np
from vidgear.gears import VideoGear
import concurrent.futures
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

    _frames: list[np.ndarray]
    """
    The list of frames to analyze.
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

        # Reset the state of the analyzer
        self._reset()

        # Validate the video path
        video_path = self._video_settings.metadata.video_path
        if not path_exists(video_path):
            raise FileNotFoundError(f"File not found: '{video_path}'")

        # Initialize the video capture object
        video = VideoGear(source=video_path) # type: ignore
        stream = video.start() 

        skipped_frames = 0
        while True:
            # Read each frame from the video
            frame = stream.read()
            if frame is None:
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
            self._frames.append(frame)

        stream.stop()

        # Analyze the frames
        if self._video_settings.multithreaded:
            final_result = self._analyze_multithreaded()
        else:
            final_result = self._analyze()
        return final_result

    
    def _reset(self) -> None:
        """
        Reset the state of the analyzer.
        """
        self._frames = []
        for pipe in self._pipes.values():
            pipe.reset_state()


    def _analyze(self) -> AnalysisResult:
        """
        Analyze frames from the video.
        """
        results = {}
        for pipe_key, pipe_value in self._pipes.items():
            pipe_key, result = self._analyze_and_get_result(
                pipe_key, 
                pipe_value, 
                self._frames
            )
            results[pipe_key] = result
        return results


    def _analyze_multithreaded(self) -> AnalysisResult:
        """
        Analyze frames from the video in multiple threads.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for pipe_key, pipe_value in self._pipes.items():
                future = executor.submit(self._analyze_and_get_result, pipe_key, pipe_value, self._frames)
                futures.append(future)
            results = {}
            for future in concurrent.futures.as_completed(futures):
                future_result = future.result()
                if future_result is None:
                    continue
                pipe_key, result = future_result
                results[pipe_key] = result
            return results


    def _analyze_and_get_result(
            self, 
            pipe_key: str, 
            pipe_value: BaseAnalysisPipe[Any],
            frames: list[np.ndarray]
        ) -> tuple[str, Any]:
        """
        Analyze frames from the video and get the final result.
        """
        pipe_value.analyze_frames(frames)
        final_result = pipe_value.get_final_result()
        return (pipe_key, final_result)


    def _get_result(self) -> AnalysisResult:
        """
        Get the final result from the analysis.
        """
        result = {}
        for pipe_key, pipe_value in self._pipes.items():
            result[pipe_key] = pipe_value.get_final_result()        
        return result
        

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
