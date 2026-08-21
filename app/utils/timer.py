"""
timer.py

Simple performance timer.
"""

from time import perf_counter


class Timer:
    """
    Utility class for measuring execution time.
    """

    def __init__(self):

        self.start = perf_counter()

    @property
    def elapsed(
        self,
    ) -> float:

        return perf_counter() - self.start

    def reset(
        self,
    ) -> None:

        self.start = perf_counter()