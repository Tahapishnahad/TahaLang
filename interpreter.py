# interpreter.py

from errors import TahaRuntimeError
from ast_nodes import (
    SourceLocation
)

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent


    def define(self, name : str, value : object, source_location : SourceLocation):
        if name in self.variables:
            raise TahaRuntimeError.variable_already_defined(
                name=name,
                line=source_location.line,
                column=source_location.column
            )

        self.variables[name] = value


    def get(self, name : str, source_location : SourceLocation):
        if name in self.variables:
            return self.variables[name]
        else:
            current_environment : Environment = self.parent

            while current_environment is not None:
                if name in current_environment.variables:
                    return current_environment.variables[name]
                
                current_environment = current_environment.parent

        raise TahaRuntimeError.undefined_variable(
            name=name,
            line=source_location.line,
            column=source_location.column
        )


    def exists(self, name: str) -> bool:
        current_environment = self

        while current_environment is not None:
            if name in current_environment.variables:
                return True

            current_environment = current_environment.parent

        return False