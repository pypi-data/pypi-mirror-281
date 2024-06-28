from dataclasses import dataclass

from super_scad.Context import Context


@dataclass
class Size2:
    """
    Size in a 2D space.
    """
    width: float
    """
    The width.
    """

    depth: float
    """
    The depth.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f"[{round(self.width)}, {self.depth}]"

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> str:
        return f"[{context.round_length(self.width)}, {context.round_length(self.depth)}]"

# ----------------------------------------------------------------------------------------------------------------------
