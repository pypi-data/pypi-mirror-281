from typing import Dict, Set, Tuple

from super_scad.private.PrivateSingleChildScadCommand import PrivateSingleChildScadCommand
from super_scad.ScadObject import ScadObject
from super_scad.type.Size2 import Size2
from super_scad.type.Size3 import Size3


class PrivateResize(PrivateSingleChildScadCommand):
    """
    Modifies the size of the child object to match the given x and y. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#resize.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 new_size: Size2 | Size3,
                 auto: bool | Tuple[bool, bool] = False,
                 convexity: int | None = None,
                 child: ScadObject) -> None:
        """
        Object constructor.

        :param new_size: The new_size along all two axes.
        :param auto: Whether to auto-scale any 0-dimensions to match.
        :param convexity:
        """
        PrivateSingleChildScadCommand.__init__(self, command='resize', args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'new_size': 'newsize'}

    # ------------------------------------------------------------------------------------------------------------------
    def argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'newsize'}

# ----------------------------------------------------------------------------------------------------------------------
