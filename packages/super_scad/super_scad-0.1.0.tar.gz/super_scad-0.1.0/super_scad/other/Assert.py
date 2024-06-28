from super_scad.private.PrivateScadCommand import PrivateScadCommand


class Assert(PrivateScadCommand):
    """
    Assert evaluates a logical expression. If the expression evaluates to false, the generation of the preview/render is
    stopped, and an error condition is reported via the console. The report consists of a string representation of the
    expression and an additional string (optional) that is specified in the assert command. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#assert.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, condition: str, message: str):
        """
        Object constructor.

        :param condition:
        :param message:
        """
        PrivateScadCommand.__init__(self, command='assert', args=locals())

# ----------------------------------------------------------------------------------------------------------------------
