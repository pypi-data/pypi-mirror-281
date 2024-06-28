import re
from typing import Any, Dict, List, Set

from super_scad.Context import Context
from super_scad.ScadObject import ScadObject
from super_scad.type.Point2 import Point2
from super_scad.type.Point3 import Point3
from super_scad.type.Size2 import Size2
from super_scad.type.Size3 import Size3


class PrivateScadCommand(ScadObject):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, command: str, args: Dict[str, Any]):
        """
        Object constructor.

        :param command: The name of the OpenSCAD command.
        :param args: The arguments of the OpenSCAD command.
        """
        ScadObject.__init__(self, args=args)

        self._command: str = command
        """
        The name of the OpenSCAD command.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return self

    # ------------------------------------------------------------------------------------------------------------------
    def children(self):
        """
        Returns the children of this OpenSCAD command.

        :rtype: List[ScadObject]|ScadObject|None
        """
        return None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def command(self) -> str:
        """
        Returns the name of the OpenSCAD command.
        """
        return self._command

    # ------------------------------------------------------------------------------------------------------------------
    def argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {}

    # ------------------------------------------------------------------------------------------------------------------
    def argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return set()

    # ------------------------------------------------------------------------------------------------------------------
    def generate_args(self, context: Context) -> str:
        """
        Returns the arguments of the OpenSCAD command.
        """
        argument_map = self.argument_map()
        argument_lengths = self.argument_lengths()

        args_as_str = '('
        first = True
        for key, value in self._args.items():
            if not first:
                args_as_str += ', '
            else:
                first = False

            real_name = argument_map.get(key, key)
            real_value = self.uc(value) if real_name in argument_lengths else value

            real_value = self.__format_argument(context, real_value)

            args_as_str += '{} = {}'.format(real_name, real_value)
        args_as_str += ')'

        return args_as_str

    # ------------------------------------------------------------------------------------------------------------------
    def __format_argument(self, context: Context, argument: Any) -> str:
        """
        Returns an argument of the OpenSCAD command.

        :param context: The build context.
        :param argument: The argument of OpenSCAD command.
        """
        if isinstance(argument, float):
            argument = context.round_length(argument)

        elif isinstance(argument, Point2) or isinstance(argument, Point3):
            argument = argument.build(context)

        elif isinstance(argument, Size2) or isinstance(argument, Size3):
            argument = argument.build(context)

        elif isinstance(argument, bool):
            argument = str(argument).lower()

        elif isinstance(argument, str):
            argument = '"{}"'.format(re.sub(r'([\\\"])', r'\\\1', argument))

        elif isinstance(argument, List):
            parts = []
            for element in argument:
                parts.append(self.__format_argument(context, element))

            argument = '[{}]'.format(', '.join(parts))

        return argument

# ----------------------------------------------------------------------------------------------------------------------
