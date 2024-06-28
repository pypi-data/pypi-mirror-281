from typing import Dict

from super_scad.private.PrivateScadCommand import PrivateScadCommand


class Cylinder(PrivateScadCommand):
    """
    Class for cylinders.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 radius: float | None = None,
                 diameter: float | None = None,
                 center: bool = False,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None):
        """
        Object constructor.

        :param height: The height of the cylinder.
        :param radius: The radius of the cylinder.
        :param diameter: The diameter of the cylinder.
        :param center: Whether the cylinder is centered along the z-as.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """
        PrivateScadCommand.__init__(self, command='cylinder', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cylinder is centered along the z-as.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    def argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'height': 'h', 'radius': 'r', 'diameter': 'd', 'fa': '$fa', 'fs': '$fs', 'fn': '$fn'}

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the radius of the cylinder.
        """
        return self.uc(self._args.get('radius', 0.5 * self._args.get('diameter', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter(self) -> float:
        """
        Returns the diameter of the cylinder.
        """
        return self.uc(self._args.get('diameter', 2.0 * self._args.get('radius', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the cylinder.
        """
        return self.uc(self._args.get('height', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._args.get('fa')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self.uc(self._args.get('fs'))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._args.get('fn')

# ----------------------------------------------------------------------------------------------------------------------
