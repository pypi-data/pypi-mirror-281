from super_scad.Context import Context
from super_scad.d2.Circle4n import Circle4n
from super_scad.d2.Rectangle import Rectangle
from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.ScadObject import ScadObject
from super_scad.transformation.Rotate3D import Rotate3D
from super_scad.transformation.Translate3D import Translate3D


class PieSlice3D4n(ScadObject):
    """
    Class for 3D pie slices.
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
                 height: float,
                 convexity: int | None = None):
        """
        Object constructor.

        :param angle:
        :param start_angle:
        :param end_angle:
        :param radius:
        :param inner_radius:
        :param outer_radius:
        :param height:
        :param convexity: See `OpenSCAD rotate_extrude documentation`_.
        """
        ScadObject.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the angle of the pie slice.
        """
        if 'start_angle' in self._args and 'end_angle' in self._args:
            return self._args['end_angle'] - self._args['start_angle']

        return self.end_angle

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
    def height(self) -> float:
        """
        Returns the height of the pie slice.
        """
        return self.uc(self._args.get('height', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        rectangle = Rectangle(width=self.outer_radius - self.inner_radius, depth=self.height)
        translate = Translate3D(x=self.inner_radius, child=rectangle)
        extrude = RotateExtrude(angle=self.end_angle - self.start_angle,
                                child=translate,
                                fn=Circle4n.r2sides4n(self.radius, context))

        return Rotate3D(angle_x=self.start_angle, child=extrude)

# ----------------------------------------------------------------------------------------------------------------------
