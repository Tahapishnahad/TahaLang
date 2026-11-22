#builtins.py

from errors import TahaRuntimeError
import pyfiglet


class BuiltinRegistry:
    def __init__(self):
        """
        Init function for registry.

        Arguments:
            functions: a dict who stores built-in datas.
        """
        self.functions = {}

    def register(self, name, function, args_count):
        """
        Registers functions in 'self.functions' with this format -> (name, function, args_count)

        Arguments:
            name: function name like; "print", "len".
            function: function who runs function name.
            args_count: count of arguments for function arguments.
        """
        self.functions[name] = (function, args_count)

    def get(self, name, location):
        """
        Gets a function data by its name from 'self.functions'.

        Arguments:
            name: Function name who we want to search.
            location: Location in case of invalid function name.
        """

        if name not in self.functions:
            raise TahaRuntimeError.trying_for_accessing_to_an_invalid_function_in_registry(
                line=location.line,
                column=location.column,
                function_name=name
            )

        return self.functions[name]

    def exists(self, name):
        """
        Returns is function exsists in 'self.functions' by its name as a bool.

        Arguments:
            name: Function name who we want to check for existants.
        """

        return name in self.functions

def builtin_len(value, location):
    if type(value) not in (list, str):
        raise TahaRuntimeError.unexpected_type_for_len_function_argument(
            line=location.line,
            column=location.column,
            argument_type=type(value).__name__
        )

    return len(value)

def builtin_print(value, location):
    print(value)

def block_print(value, location):
    if type(value) != str:
        raise TahaRuntimeError.type_error(
            f"'block_print' value must be str not {type(value).__name__}",
            line=location.line,
            column=location.column
        )
    
    font = pyfiglet.figlet_format(value, font="block")
    print(font)