from super_scad.Context import Context
from super_scad.ScadObject import ScadObject
from super_scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.transformation.private.PrivateRotate import PrivateRotate
from super_scad.type.Point3 import Point3


class Rotate3D(ScadSingleChildParent):
    """
    Rotates its child degrees about the axis of the coordinate system or around an arbitrary axis. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#rotate.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 angle: Point3 | None = None,
                 angle_x: float | None = None,
                 angle_y: float | None = None,
                 angle_z: float | None = None,
                 child: ScadObject) -> None:
        """
        Object constructor.

        :param angle: The angle of rotation around all three axes.
        :param angle_x: The angle of rotation around the x-axis.
        :param angle_y: The angle of rotation around the y-axis.
        :param angle_z: The angle of rotation around the z-axis.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> Point3:
        """
        Returns the angle around all three axes.
        """
        return Point3(self.angle_x, self.angle_y, self.angle_z)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle_x(self) -> float:
        """
        Returns the angle of rotation around the x-axis.
        """
        if 'angle' in self._args:
            return self.uc(self._args['angle'].x)

        return self.uc(self._args.get('angle_x', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle_y(self) -> float:
        """
        Returns the angle of rotation around the y-axis.
        """
        if 'angle' in self._args:
            return self.uc(self._args['angle'].y)

        return self.uc(self._args.get('angle_y', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle_z(self) -> float:
        """
        Returns the angle of rotation around the z-axis.
        """
        if 'angle' in self._args:
            return self.uc(self._args['angle'].z)

        return self.uc(self._args.get('angle_z', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateRotate(angle=self.angle, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
