from super_scad.Context import Context
from super_scad.ScadObject import ScadObject
from super_scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.transformation.private.PrivateTranslate import PrivateTranslate
from super_scad.type.Point3 import Point3


class Translate3D(ScadSingleChildParent):
    """
    Translates (moves) its child object along the specified vector. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#translate.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, x: float = 0.0, y: float = 0.0, z: float = 0.0, child: ScadObject):
        """
        Object constructor.

        :param x: The distance the child object is translated to along the x-axis.
        :param y: The distance the child object is translated to along the y-axis.
        :param z: The distance the child object is translated to along the z-axis.
        :param child: The child object to be translated.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def x(self) -> float:
        """
        Returns distance the child object is translated to along the x-axis.
        """
        return self.uc(self._args['x'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def y(self) -> float:
        """
        Returns distance the child object is translated to along the y-axis.
        """
        return self.uc(self._args['y'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def z(self) -> float:
        """
        Returns distance the child object is translated to along the z-axis.
        """
        return self.uc(self._args['z'])

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateTranslate(vector=Point3(x=self.x, y=self.y, z=self.z), child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
