# test_builtins.py

import taha_builtins
import pytest
from ast_nodes import SourceLocation

from errors import TahaRuntimeError

LOC = SourceLocation(1, 1)

def test_register():
    builtins = taha_builtins.BuiltinRegistry()
    builtins.register(name="print", function=print, args_count=1)

    assert "print" in builtins.functions
    assert (print, 1) in builtins.functions.values()

    builtins.register(name="len", function=len, args_count=1)

    assert "len" in builtins.functions
    assert (len, 1) in builtins.functions.values()

    builtins.register(name="filter", function=filter, args_count=2)

    assert "filter" in builtins.functions
    assert (filter, 2) in builtins.functions.values()

def test_exists():
    builtins = taha_builtins.BuiltinRegistry()
    builtins.register("print", print, 1)
    builtins.register("any", any, 1)

    assert builtins.exists("print")
    assert builtins.exists("any")
    assert not builtins.exists("filter")

def test_get():
    builtins = taha_builtins.BuiltinRegistry()
    builtins.register("print", print, 1)
    builtins.register("any", any, 1)
    builtins.register("filter", filter, 2)
    builtins.register("abs", abs, 1)
    builtins.register("slice", slice, 3)

    assert builtins.get("print", LOC) == (print, 1)
    assert builtins.get("any", LOC) == (any, 1)
    assert builtins.get("filter", LOC) == (filter, 2)
    assert builtins.get("abs", LOC) == (abs, 1)
    assert builtins.get("slice", LOC) == (slice, 3)

    with pytest.raises(TahaRuntimeError):
        builtins.get("unknown", LOC)