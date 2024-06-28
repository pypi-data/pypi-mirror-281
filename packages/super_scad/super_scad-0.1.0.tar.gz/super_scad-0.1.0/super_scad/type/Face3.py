from dataclasses import dataclass
from typing import List


@dataclass
class Face3:
    """
    A face in 3D space.
    """
    points: List[int]
    """
    The points of the face.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
