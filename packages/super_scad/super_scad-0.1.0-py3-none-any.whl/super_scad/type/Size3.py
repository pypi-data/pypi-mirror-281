from dataclasses import dataclass

from super_scad.Context import Context


@dataclass
class Size3:
    """
    Size in a 3D space.
    """
    width: float
    """
    The width.
    """

    depth: float
    """
    The depth.
    """

    height: float
    """
    The height.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f"[{self.width}, {self.depth}, {self.height}]"

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> str:
        return f"[{context.round_length(self.width)}, {context.round_length(self.depth)}, {context.round_length(self.height)}]"

# ----------------------------------------------------------------------------------------------------------------------
