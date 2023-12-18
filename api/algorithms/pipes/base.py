import numpy as np
from typing import Generic, TypeVar


TResult = TypeVar("TResult")

class BaseAnalysisPipe(Generic[TResult]):
    """
    Base class for AI analysis pipes.
    """

    def __init__(self):
        self._reset_state()


    def _reset_state(self) -> None:
        """
        Reset the pipe state.
        """
        raise NotImplementedError("Must be implemented in a child class")


    def analyze_frame(self, frame: np.ndarray) -> None:
        """
        Analyze a frame.
        """
        raise NotImplementedError("Must be implemented in a child class")


    def get_final_result(self) -> TResult:
        """
        Get the final result from the analysis.
        """
        raise NotImplementedError("Must be implemented in a child class")
