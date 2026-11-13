#builtins.py

class BuiltinRegistry:
    def __init__(self):
        self.functions = {}

    def register(self, name, function):
        self.functions[name] = function

    def get(self, name):
        return self.functions[name]

    def exists(self, name):
        return name in self.functions
