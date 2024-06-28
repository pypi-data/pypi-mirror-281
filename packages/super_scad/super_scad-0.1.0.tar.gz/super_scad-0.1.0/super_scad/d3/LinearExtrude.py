from typing import Dict, Set

from super_scad.private.PrivateSingleChildScadCommand import PrivateSingleChildScadCommand
from super_scad.ScadObject import ScadObject


class LinearExtrude(PrivateSingleChildScadCommand):
    """
    Linear Extrusion is an operation that takes a 2D object as input and generates a 3D object as a result. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#linear_extrude.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 center: bool = False,
                 convexity: int | None = None,
                 twist: float = 0.0,
                 scale: float = 1.0,
                 slices: float | None = None,
                 segments: float | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 child: ScadObject):
        """
        Object constructor.

        :param height: See `OpenSCAD linear_extrude documentation`_.
        :param center: See `OpenSCAD linear_extrude documentation`_.
        :param convexity: See `OpenSCAD linear_extrude documentation`_.
        :param twist: See `OpenSCAD linear_extrude documentation`_.
        :param scale: See `OpenSCAD linear_extrude documentation`_.
        :param slices: See `OpenSCAD linear_extrude documentation`_.
        :param segments: See `OpenSCAD linear_extrude documentation`_.
        :param fa: See `OpenSCAD linear_extrude documentation`_.
        :param fs: See `OpenSCAD linear_extrude documentation`_.
        :param fn: See `OpenSCAD linear_extrude documentation`_.

        .. _OpenSCAD linear_extrude documentation: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#linear_extrude
        """
        PrivateSingleChildScadCommand.__init__(self, command='linear_extrude', args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'fa': '$fa', 'fs': '$fs', 'fn': '$fn'}

    # ------------------------------------------------------------------------------------------------------------------
    def argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'fs'}

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the extruded object is centered along the z-as.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the extruded object.
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
