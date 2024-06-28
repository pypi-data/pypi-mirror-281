from super_scad.private.PrivateScadCommand import PrivateScadCommand


class Echo(PrivateScadCommand):
    """
    The echo() module prints the contents to the compilation window (aka Console). See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#Echo_module.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, **kwargs):
        """
        Object constructor.
        """
        PrivateScadCommand.__init__(self, command='echo', args=locals())

# ----------------------------------------------------------------------------------------------------------------------
