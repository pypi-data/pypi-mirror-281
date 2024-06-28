from typing import Tuple

from super_scad.Context import Context
from super_scad.ScadObject import ScadObject
from super_scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.transformation.private.PrivateResize import PrivateResize
from super_scad.type.Size3 import Size3


class Resize3D(ScadSingleChildParent):
    """
    Modifies the size of the child object to match the given width, depth, and height. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#resize.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 new_size: Size3 | None = None,
                 new_width: float | None = None,
                 new_depth: float | None = None,
                 new_height: float | None = None,
                 auto: bool | Tuple[bool, bool, bool] = False,
                 child: ScadObject) -> None:
        """
        Object constructor.

        :param new_size: The new_size along all two axes.
        :param new_width: The new width (the new size along the x-axis).
        :param new_depth: The new depth (the new size along the y-axis).
        :param new_height: The new height size (the new size along the z-axis).
        :param auto: Whether to auto-scale any 0-dimensions to match.
        :param child: The child object to be resized.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def new_size(self) -> Size3:
        """
        Returns the new_size along all three axes.
        """
        return Size3(self.new_width, self.new_depth, self.new_height)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def new_width(self) -> float:
        """
        Returns new width (the new size along the x-axis).
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
    @property
    def new_height(self) -> float:
        """
        Returns the new height (the new size along the z-axis).
        """
        if 'new_size' in self._args:
            return self.uc(self._args['new_size'].height)

        return self.uc(self._args['new_height'])

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateResize(new_size=self.new_size, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
