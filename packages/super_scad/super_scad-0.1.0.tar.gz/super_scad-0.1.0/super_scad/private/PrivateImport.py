from abc import ABC
from typing import Dict

from super_scad.private.PrivateScadCommand import PrivateScadCommand


class PrivateImport(PrivateScadCommand, ABC):
    """
    Abstract parent class for Import2D and Import3D. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Importing_Geometry#import.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 file: str,
                 convexity: int | None = None,
                 layer: str | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 id: str | None = None):
        """
        Object constructor.

        :param file: See `OpenSCAD import documentation`_.
        :param convexity: See `OpenSCAD import documentation`_.
        :param layer: See `OpenSCAD import documentation`_.
        :param fa: See `OpenSCAD import documentation`_.
        :param fs: See `OpenSCAD import documentation`_.
        :param fn: See `OpenSCAD import documentation`_.
        :param id: See `OpenSCAD import documentation`_.

        .. _OpenSCAD import documentation: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Importing_Geometry#import
        """
        PrivateScadCommand.__init__(self, command='import', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

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

    # ------------------------------------------------------------------------------------------------------------------
    def argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'fa': '$fa', 'fs': '$fs', 'fn': '$fn'}

# ----------------------------------------------------------------------------------------------------------------------
