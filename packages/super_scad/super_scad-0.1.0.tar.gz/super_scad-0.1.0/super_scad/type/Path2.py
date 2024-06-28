from dataclasses import dataclass
from typing import List


@dataclass
class Path2:
    """
    A path in 2D space.
    """
    points: List[int]
    """
    The points of the path.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
