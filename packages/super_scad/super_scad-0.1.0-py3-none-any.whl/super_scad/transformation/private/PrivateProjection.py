from super_scad.private.PrivateSingleChildScadCommand import PrivateSingleChildScadCommand
from super_scad.ScadObject import ScadObject


class PrivateProjection(PrivateSingleChildScadCommand):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, cut: bool, child: ScadObject) -> None:
        PrivateSingleChildScadCommand.__init__(self, command='projection', args=locals(), child=child)

# ----------------------------------------------------------------------------------------------------------------------
