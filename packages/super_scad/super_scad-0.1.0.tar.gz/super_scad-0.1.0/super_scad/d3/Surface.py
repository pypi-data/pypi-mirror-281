from super_scad.private.PrivateScadCommand import PrivateScadCommand


class Surface(PrivateScadCommand):
    """
    Surface reads Heightmap information from text or image files. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#surface.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, file: str, center: bool = False, invert: bool = False, convexity: int | None = None):
        """
        Object constructor.

        :param file: See `OpenSCAD surface documentation`_.
        :param center: See `OpenSCAD surface documentation`_.
        :param invert: See `OpenSCAD surface documentation`_.
        :param convexity: See `OpenSCAD surface documentation`_.

        .. _OpenSCAD surface documentation: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#surface
        """
        PrivateScadCommand.__init__(self, command='surface', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

# ----------------------------------------------------------------------------------------------------------------------
