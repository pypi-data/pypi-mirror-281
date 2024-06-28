import math
from dataclasses import dataclass

from super_scad.Context import Context


@dataclass
class Point2:
    """
    A point in 2D space.
    """
    x: float
    """
    The x-coordinate of this point.
    """

    y: float
    """
    The y-coordinate of this point.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f"[{self.x}, {self.y}]"

    # ------------------------------------------------------------------------------------------------------------------
    def __add__(self, other):
        return Point2(self.x + other.x, self.y + other.y)

    # ------------------------------------------------------------------------------------------------------------------
    def __sub__(self, other):
        return Point2(self.x - other.x, self.y - other.y)

    # ------------------------------------------------------------------------------------------------------------------
    def __truediv__(self, other: float):
        return Point2(self.x / other, self.y / other)

    # ------------------------------------------------------------------------------------------------------------------
    def length(self) -> float:
        """
        Returns the length of this vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> str:
        return f"[{context.round_length(self.x)}, {context.round_length(self.y)}]"

# ----------------------------------------------------------------------------------------------------------------------
