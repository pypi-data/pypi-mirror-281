from typing import Tuple

from super_scad.Context import Context
from super_scad.ScadObject import ScadObject
from super_scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.transformation.private.PrivateResize import PrivateResize
from super_scad.type.Size2 import Size2


class Resize2D(ScadSingleChildParent):
    """
    Modifies the size of the child object to match the given width and depth. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#resize.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 new_size: Size2 | None = None,
                 new_width: float | None = None,
                 new_depth: float | None = None,
                 auto: bool | Tuple[bool, bool] = False,
                 child: ScadObject):
        """
        Object constructor.

        :param new_size: The new_size along all two axes.
        :param new_width: The new width (the new size along the x-axis).
        :param new_depth: The new depth (the new size along the y-axis).
        :param auto: Whether to auto-scale any 0-dimensions to match.
        :param child: The child object to be resized.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def new_size(self) -> Size2:
        """
        Returns the new_size along both axes.
        """
        return Size2(self.new_width, self.new_depth)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def new_width(self) -> float:
        """
        Returns the new width (the new size along the x-axis).
        """
        if 'new_size' in self._args:
            return self.uc(self._args['new_size'].width)

        return self.uc(self._args['new_width'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def new_depth(self) -> float:
        """
        Returns the new depth (the new size along the y-axis).
        """
        if 'new_size' in self._args:
            return self.uc(self._args['new_size'].depth)

        return self.uc(self._args['new_depth'])

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateResize(new_size=self.new_size, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
