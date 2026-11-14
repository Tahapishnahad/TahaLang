#builtins.py

from errors import TahaRuntimeError
from ast_nodes import SourceLocation

class BuiltinRegistry:
    def __init__(self):
        self.functions = {}

    def register(self, name, function, args_count):
        self.functions[name] = (function, args_count)

    def get(self, name, location):
        if name not in self.functions:
            raise TahaRuntimeError.trying_for_accessing_to_an_invalid_function_in_registry(
                line=location.line,
                column=location.column,
                function_name=name
            )

        return self.functions[name]

    def exists(self, name):
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