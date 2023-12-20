import numpy as np
from typing import Generic, TypeVar


TResult = TypeVar("TResult")

class BaseAnalysisPipe(Generic[TResult]):
    """
    Base class for AI analysis pipes.
    """

    def __init__(self):
        pass


    def reset_state(self) -> None:
        """
        Reset the pipe state.
        """
        raise NotImplementedError("Must be implemented in a child class")


    def analyze_frames(self, frames: list[np.ndarray]) -> None:
        """
        Analyze all the frames.
        """
        for frame in frames:
            self._analyze_frame(frame)


    def _analyze_frame(self, frame: np.ndarray) -> None:
        """
        Analyze a frame.
        """
        raise NotImplementedError("Must be implemented in a child class")


    def get_final_result(self) -> TResult:
        """
        Get the final result from the analysis.
        """
        raise NotImplementedError("Must be implemented in a child class")
