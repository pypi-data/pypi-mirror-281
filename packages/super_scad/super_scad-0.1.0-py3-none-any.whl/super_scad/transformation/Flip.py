from super_scad.Context import Context
from super_scad.ScadObject import ScadObject
from super_scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.transformation.private.PrivateRotate import PrivateRotate
from super_scad.type.Point3 import Point3


class Flip(ScadSingleChildParent):
    """
    Flips its child about the x, y, or z-axis.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, flip_x: bool = False, flip_y: bool = False, flip_z: bool = False, child: ScadObject) -> None:
        """
        Object constructor.

        :param flip_x: Whether to flip the child object around the x-asis (i.e. vertical flip).
        :param flip_y: Whether to flip the child object around the y-asis (i.e. horizontal flip).
        :param flip_z: Whether to flip the child object around the z-asis (i.e. horizontal and vertical flip).
        :param child: The child object to be flipped.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def flip_x(self) -> bool:
        """
        Returns to flip the child object around the x-asis (i.e. vertical flip).
        """
        return self._args['flip_x']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def flip_y(self) -> bool:
        """
        Returns to flip the child object around the y-asis (i.e. horizontal flip).
        """
        return self._args['flip_y']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def flip_z(self) -> bool:
        """
        Returns to flip the child object around the z-asis (i.e. horizontal and vertical flip).
        """
        return self._args['flip_z']

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        angle = Point3(x=180.0 if self.flip_x else 0.0,
                       y=180.0 if self.flip_y else 0.0,
                       z=180.0 if self.flip_z else 0.0)
        return PrivateRotate(angle=angle, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
