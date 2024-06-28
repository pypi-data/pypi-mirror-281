from super_scad.boolean.Difference import Difference
from super_scad.boolean.Intersection import Intersection
from super_scad.boolean.Union import Union
from super_scad.Context import Context
from super_scad.d2.Circle import Circle
from super_scad.d2.Square import Square
from super_scad.ScadObject import ScadObject
from super_scad.transformation.Rotate2D import Rotate2D
from super_scad.transformation.Translate2D import Translate2D


class PieSlice2D(ScadObject):
    """
    Class for 2D pie slices.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 angle: float | None = None,
                 start_angle: float | None = None,
                 end_angle: float | None = None,
                 radius: float | None = None,
                 inner_radius: float | None = None,
                 outer_radius: float | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None):
        """
        Object constructor.

        :param angle:
        :param start_angle:
        :param end_angle:
        :param radius:
        :param inner_radius:
        :param outer_radius:
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """
        ScadObject.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the angle of the pie slice.
        """
        return self.end_angle - self.start_angle

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def start_angle(self) -> float:
        """
        Returns the start angle of the pie slice.
        """
        return self._args.get('start_angle', 0.0)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def end_angle(self) -> float:
        """
        Returns the end angle of the pie slice.
        """
        return self._args.get('end_angle', self._args.get('angle', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the outer radius of the pie slice.
        """
        return self.uc(self.outer_radius)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_radius(self) -> float:
        """
        Returns the inner radius of the pie slice.
        """
        return self.uc(self._args.get('inner_radius', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_radius(self) -> float:
        """
        Returns the outer radius of the pie slice.
        """
        return self.uc(self._args.get('outer_radius', self._args.get('radius', 0.0)))

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
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        size = self.outer_radius + 2 * context.eps
        trans = self.outer_radius + context.eps
        angle = self.angle

        if angle <= 90.0:
            return Intersection(children=[
                Difference(children=[Circle(radius=self.outer_radius, fa=self.fa, fs=self.fs, fn=self.fn),
                                     Circle(radius=self.inner_radius, fa=self.fa, fs=self.fs, fn=self.fn)]),
                Rotate2D(angle=self.end_angle - 90, child=Square(size=size)),
                Rotate2D(angle=self.start_angle, child=Square(size=size))])

        children = []
        if self.start_angle < 0.0 and self.end_angle > 90.0:
            children.append(Square(size=size))
        if self.start_angle < 90.0 and self.end_angle > 180.0:
            children.append(Translate2D(x=-trans, child=Square(size=size)))
        if self.start_angle < 180.0 and self.end_angle > 270.0:
            children.append(Translate2D(x=-trans, y=-trans, child=Square(size=size)))
        children.append(Rotate2D(angle=self.end_angle - 90, child=Square(size=size)))
        children.append(Rotate2D(angle=self.start_angle, child=Square(size=size)))

        return Intersection(children=[
            Difference(children=[Circle(radius=self.outer_radius, fa=self.fa, fs=self.fs, fn=self.fn),
                                 Circle(radius=self.inner_radius, fa=self.fa, fs=self.fs, fn=self.fn)]),
            Union(children=children)])

# ----------------------------------------------------------------------------------------------------------------------
