from abc import ABC
from typing import Any, Dict

from super_scad.ScadObject import ScadObject


class ScadSingleChildParent(ScadObject, ABC):
    """
    Class for OpenSCAD objects that have a single-child.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, args: Dict[str, Any], child: ScadObject):
        """
        Object constructor.

        :param child: The child SuperSCAD object of this single-child parent.
        """
        ScadObject.__init__(self, args=args)

        self.__child = child
        """
        The child SuperSCAD object of this single-child parent.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def child(self) -> ScadObject:
        """
        Returns the child of this single-child parent.

        :rtype: List[ScadObject]|ScadObject|None
        """
        return self.__child

    # ------------------------------------------------------------------------------------------------------------------
    def children(self) -> ScadObject:
        """
        Returns the child of this single-child parent.

        :rtype: List[ScadObject]|ScadObject|None
        """
        return self.__child

# ----------------------------------------------------------------------------------------------------------------------
