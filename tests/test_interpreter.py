# test_interpreter.py

from interpreter import Environment
from errors import TahaRuntimeError
from ast_nodes import *
import pytest

# --------- Test Environment -----------
def test_define():
    env = Environment()
    num =  NumberLiteral(
        value=3,
        location=SourceLocation(3, 7)
    )

    env.define(
        name="num", 
        value=num,
        source_location=num.location
    )

    assert isinstance(env.variables["num"], NumberLiteral)
    assert env.variables["num"].value == 3

    env = Environment()
    string =  StringLiteral(
        value="Taha",
        location=SourceLocation(4, 16)
    )

    env.define(
        name="name", 
        value=string,
        source_location=string.location
    )

    assert isinstance(env.variables["name"], StringLiteral)
    assert env.variables["name"].value == "Taha"

def test_define_in_parent():
    temp_location = SourceLocation(1, 1)

    env_parent = Environment()
    env_parent.define(
        "num",
        2,
        temp_location
    )

    env = Environment(env_parent)
    env.define(
        "num",
        4,
        temp_location
    )

    assert env_parent.get("num", temp_location) == 2
    assert env.get("num", temp_location) == 4
    assert env.get("num", temp_location) != env_parent.get("num", temp_location)

def test_define_raises_error():

    env = Environment()
    num =  NumberLiteral(
        value=3,
        location=SourceLocation(3, 7)
    )

    env.define(
        name="num", 
        value=num,
        source_location=num.location
    )
    
    with pytest.raises(TahaRuntimeError):
        env.define(
        name="num", 
        value=9,
        source_location=SourceLocation(34, 5)
    )

def test_get():
    env = Environment()
    num =  NumberLiteral(
        value=3,
        location=SourceLocation(3, 7)
    )

    env.define(
        name="num",
        value=num,
        source_location=num.location
    )

    assert env.get("num", num.location) == num

    env = Environment()
    string =  StringLiteral(
        value="Taha",
        location=SourceLocation(4, 16)
    )

    env.define(
        name="name", 
        value=string,
        source_location=string.location
    )

    assert env.get("name", string.location) == string

def test_get_raises_error():
    env = Environment()

    with pytest.raises(TahaRuntimeError):
        env.get("undefined", SourceLocation(100, 100))

def test_get_with_parent():
    temp_location = SourceLocation(1, 1)
    
    env_parent = Environment()
    env_parent.define(
        "num",
        2,
        temp_location
    )
    
    env = Environment(env_parent)

    assert env.get("num", temp_location) == 2

    with pytest.raises(TahaRuntimeError):
        env.get("undefined", temp_location)

def test_exists():
    env = Environment()
    num =  NumberLiteral(
        value=3,
        location=SourceLocation(3, 7)
    )

    env.define(
        name="num",
        value=num,
        source_location=num.location
    )

    assert not env.exists("undefined")
    assert env.exists("num")

    env = Environment()
    string =  StringLiteral(
        value="Taha",
        location=SourceLocation(4, 16)
    )

    env.define(
        name="name", 
        value=string,
        source_location=string.location
    )

    assert not env.exists("undefined")
    assert env.exists("name")

def test_exists_with_parent():
    temp_location = SourceLocation(1, 1)
    
    env_parent = Environment()
    env_parent.define(
        "num",
        2,
        temp_location
    )
    
    env = Environment(env_parent)

    assert env.exists("num")
    assert not env.exists("undefined")
