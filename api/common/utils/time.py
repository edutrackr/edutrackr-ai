import time
from typing import Callable, TypeVar, Generic


TData = TypeVar("TData")
class TimerResult(Generic[TData]):
    """
    The result of the timer function.
    """

    data: TData
    """
    The data returned by the function.
    """

    time: float
    """
    The time it took to execute the function.
    """

    def __init__(self, data: TData, time: float):
        self.data = data
        self.time = time


def timer(callback: Callable[[], TData], precision: int = 3) -> TimerResult[TData]:
    """
    Calculate the time it takes to execute a function.
    """

    # Start the timer
    start = time.time()

    # Execute the callback function
    data = callback()

    # Stop the timer
    end = time.time()

    # Return the result
    return TimerResult(
        data=data,
        time=round(end - start, precision)
    )
