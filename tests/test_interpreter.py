# test_interpreter.py

import pytest
from types import SimpleNamespace
from interpreter import Interpreter, Environment
from errors import TahaRuntimeError
from ast_nodes import *
from tokens import TokenType

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



# -------------------------
# Helpers
# -------------------------

def make_node(cls, **kwargs):
    node = cls.__new__(cls)

    for key, value in kwargs.items():
        setattr(node, key, value)

    return node


def make_location(line=1, column=1):
    return SimpleNamespace(line=line, column=column)


def number(value):
    return make_node(
        NumberLiteral,
        value=value,
        location=make_location()
    )


def string(value):
    return make_node(
        StringLiteral,
        value=value,
        location=make_location()
    )


def boolean(value):
    return make_node(
        BooleanLiteral,
        value=value,
        location=make_location()
    )


def binary(left, operator, right):
    return make_node(
        BinaryExpression,
        left=left,
        operator=operator,
        right=right,
        location=make_location()
    )


def unary(operator, operand):
    return make_node(
        UnaryExpression,
        operator=operator,
        operand=operand,
        location=make_location()
    )


@pytest.fixture
def env():
    return Environment()

@pytest.fixture
def interpreter(env):
    return Interpreter(env)


# -------------------------
# Literal Tests
# -------------------------

@pytest.mark.parametrize(
    "expr, expected",
    [
        (number(10), 10),
        (number(3.5), 3.5),
        (string("Hello"), "Hello"),
        (boolean(True), True),
        (boolean(False), False),
    ]
)
def test_literal_evaluation(interpreter, expr, expected, env):
    assert interpreter.execute_expression(expr, env) == expected


# -------------------------
# PLUS
# -------------------------

@pytest.mark.parametrize(
    "left, right, expected",
    [
        (number(5), number(3), 8),
        (number(5), number(2.5), 7.5),
        (string("Hello "), string("World"), "Hello World"),
    ]
)
def test_plus(interpreter, left, right, expected, env):
    expr = binary(left, TokenType.PLUS, right)

    assert interpreter.execute_expression(expr, env) == expected


def test_plus_invalid_types(interpreter, env):
    expr = binary(number(5), TokenType.PLUS, string("5"))

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_expression(expr, env)


# -------------------------
# MINUS
# -------------------------

@pytest.mark.parametrize(
    "left, right, expected",
    [
        (number(10), number(3), 7),
        (number(5), number(2.5), 2.5),
        (number(-5), number(3), -8),
    ]
)
def test_minus(interpreter, left, right, expected, env):
    expr = binary(left, TokenType.MINUS, right)

    assert interpreter.execute_expression(expr, env) == expected


def test_minus_invalid_types(interpreter, env):
    expr = binary(string("10"), TokenType.MINUS, number(5))

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_expression(expr, env)


# -------------------------
# STAR
# -------------------------

@pytest.mark.parametrize(
    "left, right, expected",
    [
        (number(5), number(3), 15),
        (number(2.5), number(2), 5.0),
        (number(-4), number(3), -12),
    ]
)
def test_star(interpreter, left, right, expected, env):
    expr = binary(left, TokenType.STAR, right)

    assert interpreter.execute_expression(expr, env) == expected


def test_star_invalid_types(interpreter, env):
    expr = binary(boolean(True), TokenType.STAR, number(5))

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_expression(expr, env)


# -------------------------
# SLASH
# -------------------------

@pytest.mark.parametrize(
    "left, right, expected",
    [
        (number(10), number(2), 5.0),
        (number(7), number(2), 3.5),
        (number(-10), number(2), -5.0),
    ]
)
def test_slash(interpreter, left, right, expected, env):
    expr = binary(left, TokenType.SLASH, right)

    assert interpreter.execute_expression(expr, env) == expected


def test_slash_by_zero(interpreter, env):
    expr = binary(number(10), TokenType.SLASH, number(0))

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_expression(expr, env)


def test_slash_invalid_types(interpreter, env):
    expr = binary(number(10), TokenType.SLASH, boolean(False))

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_expression(expr, env)


# -------------------------
# PERCENT
# -------------------------

@pytest.mark.parametrize(
    "left, right, expected",
    [
        (number(10), number(3), 1),
        (number(10.5), number(3), 1.5),
        (number(20), number(5), 0),
        (number(-10), number(3), 2),
    ]
)
def test_percent(interpreter, left, right, expected, env):
    expr = binary(left, TokenType.PERCENT, right)

    assert interpreter.execute_expression(expr, env) == expected


def test_percent_by_zero(interpreter, env):
    expr = binary(number(10), TokenType.PERCENT, number(0))

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_expression(expr, env)


def test_percent_invalid_types(interpreter, env):
    expr = binary(number(10), TokenType.PERCENT, string("3"))

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_expression(expr, env)


# -------------------------
# EQUAL_EQUAL and BANG_EQUAL
# -------------------------

@pytest.mark.parametrize(
    "left, right, expected",
    [
        (number(5), number(5), True),
        (number(5), number(3), False),
        (number(5), number(5.0), True),
        (number(5), string("5"), False),
        (boolean(True), boolean(True), True),
        (boolean(True), boolean(False), False),
        (boolean(True), number(1), False),
        (string("Hello"), string("Hello"), True),
        (string("Hello"), string("World"), False),
    ]
)
def test_equal_equal(interpreter, left, right, expected, env):
    expr = binary(left, TokenType.EQUAL_EQUAL, right)

    assert interpreter.execute_expression(expr, env) is expected


@pytest.mark.parametrize(
    "left, right, expected",
    [
        (number(5), number(3), True),
        (number(5), number(5.0), False),
        (boolean(True), number(1), True),
        (boolean(True), boolean(True), False),
        (string("Hello"), string("World"), True),
    ]
)
def test_bang_equal(interpreter, left, right, expected, env):
    expr = binary(left, TokenType.BANG_EQUAL, right)

    assert interpreter.execute_expression(expr, env) is expected


# -------------------------
# Relational Operators
# -------------------------

@pytest.mark.parametrize(
    "operator, left, right, expected",
    [
        (TokenType.LESS, number(3), number(5), True),
        (TokenType.LESS, number(5), number(3), False),

        (TokenType.GREATER, number(5), number(3), True),
        (TokenType.GREATER, number(3), number(5), False),

        (TokenType.LESS_EQUAL, number(3), number(3), True),
        (TokenType.LESS_EQUAL, number(4), number(3), False),

        (TokenType.GREATER_EQUAL, number(3), number(3), True),
        (TokenType.GREATER_EQUAL, number(2), number(3), False),

        (TokenType.LESS, string("apple"), string("banana"), True),
        (TokenType.GREATER, string("banana"), string("apple"), True),
    ]
)
def test_relational_operators(
    interpreter, operator, left, right, expected
, env):
    expr = binary(left, operator, right)

    assert interpreter.execute_expression(expr, env) is expected


@pytest.mark.parametrize(
    "operator",
    [
        TokenType.LESS,
        TokenType.GREATER,
        TokenType.LESS_EQUAL,
        TokenType.GREATER_EQUAL,
    ]
)
def test_relational_operators_invalid_types(interpreter, operator, env):
    expr = binary(number(5), operator, string("5"))

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_expression(expr, env)


# -------------------------
# Unary Operators
# -------------------------

@pytest.mark.parametrize(
    "operand, expected",
    [
        (number(5), -5),
        (number(-10), 10),
        (number(2.5), -2.5),
    ]
)
def test_unary_minus(interpreter, operand, expected, env):
    expr = unary(TokenType.MINUS, operand)

    assert interpreter.execute_expression(expr, env) == expected


def test_unary_minus_invalid_type(interpreter, env):
    expr = unary(TokenType.MINUS, string("Hello"))

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_expression(expr, env)


@pytest.mark.parametrize(
    "operand, expected",
    [
        (boolean(True), False),
        (boolean(False), True),
    ]
)
def test_unary_bang(interpreter, operand, expected, env):
    expr = unary(TokenType.BANG, operand)

    assert interpreter.execute_expression(expr, env) is expected


def test_unary_bang_invalid_type(interpreter, env):
    expr = unary(TokenType.BANG, number(5))

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_expression(expr, env)


LOC = SourceLocation(line=1, column=1)


# -------------------------
# LetStatement
# -------------------------

def test_let_statement_defines_variable(interpreter, env):
    statement = LetStatement(
        name="x",
        value=NumberLiteral(10, LOC),
        location=LOC
    )

    interpreter.execute_statement(statement, env)

    assert env.get("x", LOC) == 10


def test_let_statement_evaluates_expression(interpreter, env):
    statement = LetStatement(
        name="x",
        value=BinaryExpression(
            left=NumberLiteral(5, LOC),
            operator=TokenType.PLUS,
            right=NumberLiteral(3, LOC),
            location=LOC
        ),
        location=LOC
    )

    interpreter.execute_statement(statement, env)

    assert env.get("x", LOC) == 8


def test_let_statement_can_use_existing_variable(interpreter, env):
    env.define("x", 10, LOC)

    statement = LetStatement(
        name="y",
        value=Identifier("x", LOC),
        location=LOC
    )

    interpreter.execute_statement(statement, env)

    assert env.get("y", LOC) == 10


# -------------------------
# PrintStatement
# -------------------------

def test_print_statement(capsys, interpreter, env):
    statement = PrintStatement(
        expression=NumberLiteral(42, LOC),
        location=LOC
    )

    interpreter.execute_statement(statement, env)

    assert capsys.readouterr().out == "42\n"


def test_print_statement_prints_identifier(capsys, interpreter, env):
    env.define("x", 25, LOC)

    statement = PrintStatement(
        expression=Identifier("x", LOC),
        location=LOC
    )

    interpreter.execute_statement(statement, env)

    assert capsys.readouterr().out == "25\n"


# -------------------------
# BlockStatement
# -------------------------

def test_block_statement_executes_all_statements(capsys, interpreter, env):
    block = BlockStatement(
        statements=[
            PrintStatement(NumberLiteral(10, LOC), LOC),
            PrintStatement(NumberLiteral(20, LOC), LOC),
        ],
        location=LOC
    )

    interpreter.execute_statement(block, env)

    assert capsys.readouterr().out == "10\n20\n"


def test_block_can_access_parent_variables(capsys, interpreter, env):
    env.define("x", 100, LOC)

    block = BlockStatement(
        statements=[
            PrintStatement(Identifier("x", LOC), LOC)
        ],
        location=LOC
    )

    interpreter.execute_statement(block, env)

    assert capsys.readouterr().out == "100\n"


def test_block_variable_does_not_leak(interpreter, env):
    block = BlockStatement(
        statements=[
            LetStatement(
                "x",
                NumberLiteral(10, LOC),
                LOC
            )
        ],
        location=LOC
    )

    interpreter.execute_statement(block, env)

    with pytest.raises(TahaRuntimeError):
        env.get("x", LOC)


def test_block_can_shadow_parent_variable(capsys, interpreter, env):
    env.define("x", 10, LOC)

    block = BlockStatement(
        statements=[
            LetStatement("x", NumberLiteral(20, LOC), LOC),
            PrintStatement(Identifier("x", LOC), LOC)
        ],
        location=LOC
    )

    interpreter.execute_statement(block, env)

    assert capsys.readouterr().out == "20\n"
    assert env.get("x", LOC) == 10


# -------------------------
# IfStatement
# -------------------------

def test_if_true_executes_then_branch(capsys, interpreter, env):
    statement = IfStatement(
        condition=BooleanLiteral(True, LOC),
        then_branch=BlockStatement(
            [PrintStatement(NumberLiteral(1, LOC), LOC)],
            LOC
        ),
        location=LOC
    )

    interpreter.execute_statement(statement, env)

    assert capsys.readouterr().out == "1\n"


def test_if_false_executes_else_branch(capsys, interpreter, env):
    statement = IfStatement(
        condition=BooleanLiteral(False, LOC),
        then_branch=BlockStatement(
            [PrintStatement(NumberLiteral(1, LOC), LOC)],
            LOC
        ),
        location=LOC,
        else_branch=BlockStatement(
            [PrintStatement(NumberLiteral(2, LOC), LOC)],
            LOC
        )
    )

    interpreter.execute_statement(statement, env)

    assert capsys.readouterr().out == "2\n"


def test_if_false_without_else_does_nothing(capsys, interpreter, env):
    statement = IfStatement(
        condition=BooleanLiteral(False, LOC),
        then_branch=BlockStatement(
            [PrintStatement(NumberLiteral(1, LOC), LOC)],
            LOC
        ),
        location=LOC
    )

    interpreter.execute_statement(statement, env)

    assert capsys.readouterr().out == ""


def test_if_rejects_non_boolean_condition(interpreter, env):
    statement = IfStatement(
        condition=NumberLiteral(10, LOC),
        then_branch=BlockStatement([], LOC),
        location=LOC
    )

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_statement(statement, env)


def test_if_branch_has_independent_scope(interpreter, env):
    statement = IfStatement(
        condition=BooleanLiteral(True, LOC),
        then_branch=BlockStatement(
            [
                LetStatement(
                    "x",
                    NumberLiteral(10, LOC),
                    LOC
                )
            ],
            LOC
        ),
        location=LOC
    )

    interpreter.execute_statement(statement, env)

    with pytest.raises(TahaRuntimeError):
        env.get("x", LOC)


def test_if_can_read_parent_variables(capsys, interpreter, env):
    env.define("x", 50, LOC)

    statement = IfStatement(
        condition=BooleanLiteral(True, LOC),
        then_branch=BlockStatement(
            [
                PrintStatement(Identifier("x", LOC), LOC)
            ],
            LOC
        ),
        location=LOC
    )

    interpreter.execute_statement(statement, env)

    assert capsys.readouterr().out == "50\n"

# -------------------------
# Program Execution
# -------------------------

def test_execute_program_executes_all_statements(capsys, interpreter, env):
    program = Program(
        statements=[
            PrintStatement(NumberLiteral(10, LOC), LOC),
            PrintStatement(NumberLiteral(20, LOC), LOC),
            PrintStatement(NumberLiteral(30, LOC), LOC),
        ]
    )

    interpreter.execute_program(program, env)

    assert capsys.readouterr().out == "10\n20\n30\n"


def test_execute_program_preserves_statement_order(capsys, interpreter, env):
    program = Program(
        statements=[
            LetStatement("x", NumberLiteral(10, LOC), LOC),
            LetStatement(
                "y",
                BinaryExpression(
                    Identifier("x", LOC),
                    TokenType.PLUS,
                    NumberLiteral(5, LOC),
                    LOC
                ),
                LOC
            ),
            PrintStatement(Identifier("y", LOC), LOC),
        ]
    )

    interpreter.execute_program(program, env)

    assert capsys.readouterr().out == "15\n"


def test_execute_program_uses_shared_environment(interpreter, env):
    program = Program(
        statements=[
            LetStatement("x", NumberLiteral(100, LOC), LOC),
            LetStatement("y", NumberLiteral(200, LOC), LOC),
        ]
    )

    interpreter.execute_program(program, env)

    assert env.get("x", LOC) == 100
    assert env.get("y", LOC) == 200


def test_execute_program_stops_after_runtime_error(capsys, interpreter, env):
    program = Program(
        statements=[
            PrintStatement(NumberLiteral(10, LOC), LOC),
            PrintStatement(Identifier("undefined", LOC), LOC),
            PrintStatement(NumberLiteral(30, LOC), LOC),
        ]
    )

    with pytest.raises(TahaRuntimeError):
        interpreter.execute_program(program, env)

    assert capsys.readouterr().out == "10\n"


def test_execute_empty_program(interpreter, env):
    program = Program(statements=[])

    interpreter.execute_program(program, env)

    assert env.variables == {}