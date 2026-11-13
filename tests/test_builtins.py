# test_builtins.py

import taha_builtins

def test_register():
    builtins = taha_builtins.BuiltinRegistry()
    builtins.register(name="print", function=print)

    assert "print" in builtins.functions
    assert print in builtins.functions.values()

    builtins.register(name="len", function=len)

    assert "len" in builtins.functions
    assert len in builtins.functions.values()

    builtins.register(name="filter", function=filter)

    assert "filter" in builtins.functions
    assert filter in builtins.functions.values()

def test_exists():
    builtins = taha_builtins.BuiltinRegistry()
    builtins.register("print", print)
    builtins.register("any", any)
    

    assert builtins.exists("print")
    assert builtins.exists("any")
    assert not builtins.exists("filter")

def test_get():
    builtins = taha_builtins.BuiltinRegistry()
    builtins.register("print", print)
    builtins.register("any", any)
    builtins.register("filter", filter)
    builtins.register("abs", abs)
    builtins.register("slice", slice)

    assert builtins.get("print") == print
    assert builtins.get("any") == any
    assert builtins.get("filter") == filter
    assert builtins.get("abs") == abs
    assert builtins.get("slice") == slice