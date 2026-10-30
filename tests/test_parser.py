#test_parser.py

import pytest

from lexer import Lexer
from parser import Parser
from errors import TahaSyntaxError
from ast_nodes import (
    Program,
    LetStatement,
    PrintStatement,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    Identifier,
    BinaryExpression,
    IfStatement,
    BlockStatement
)
from tokens import TokenType


def parse_source(source):
    tokens = Lexer(source).scan_tokens()
    return Parser(tokens).parse()


# -------------------------
# Program
# -------------------------

def test_empty_program():
    program = parse_source("")

    assert isinstance(program, Program)
    assert program.statements == []


def test_multiple_statements():
    program = parse_source('let a = 3\nprint("Hello")')

    assert len(program.statements) == 2
    assert isinstance(program.statements[0], LetStatement)
    assert isinstance(program.statements[1], PrintStatement)


def test_blank_lines_between_statements():
    program = parse_source('\nlet a = 3\n\nprint("Hello")\n')

    assert len(program.statements) == 2


# -------------------------
# let statements
# -------------------------

def test_let_integer():
    program = parse_source("let a = 3")
    statement = program.statements[0]

    assert isinstance(statement, LetStatement)
    assert statement.name == "a"
    assert isinstance(statement.value, NumberLiteral)
    assert statement.value.value == 3


def test_let_float():
    program = parse_source("let pi = 3.14")
    value = program.statements[0].value

    assert isinstance(value, NumberLiteral)
    assert value.value == pytest.approx(3.14)


def test_let_string():
    program = parse_source('let message = "Hello"')
    value = program.statements[0].value

    assert isinstance(value, StringLiteral)
    assert value.value == "Hello"


def test_let_true():
    program = parse_source("let active = True")
    value = program.statements[0].value

    assert isinstance(value, BooleanLiteral)
    assert value.value is True


def test_let_false():
    program = parse_source("let active = False")
    value = program.statements[0].value

    assert isinstance(value, BooleanLiteral)
    assert value.value is False


def test_let_identifier():
    program = parse_source("let b = a")
    value = program.statements[0].value

    assert isinstance(value, Identifier)
    assert value.name == "a"


# -------------------------
# print statements
# -------------------------

def test_print_string():
    program = parse_source('print("Hello")')
    statement = program.statements[0]

    assert isinstance(statement, PrintStatement)
    assert isinstance(statement.expression, StringLiteral)
    assert statement.expression.value == "Hello"


def test_print_number():
    program = parse_source("print(42)")
    statement = program.statements[0]

    assert isinstance(statement, PrintStatement)
    assert isinstance(statement.expression, NumberLiteral)
    assert statement.expression.value == 42


def test_print_binary_expression():
    program = parse_source("print(2 + 3)")
    expression = program.statements[0].expression

    assert isinstance(expression, BinaryExpression)
    assert isinstance(expression.left, NumberLiteral)
    assert expression.left.value == 2
    assert expression.operator == TokenType.PLUS
    assert isinstance(expression.right, NumberLiteral)
    assert expression.right.value == 3


# -------------------------
# Binary expressions
# -------------------------

@pytest.mark.parametrize(
    "operator",
    [
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.STAR,
        TokenType.SLASH,
        TokenType.PERCENT,
    ],
)
def test_all_binary_operators(operator):
    symbols = {
        TokenType.PLUS: "+",
        TokenType.MINUS: "-",
        TokenType.STAR: "*",
        TokenType.SLASH: "/",
        TokenType.PERCENT: "%",
    }

    source = f"let result = 8 {symbols[operator]} 3"
    program = parse_source(source)
    expression = program.statements[0].value

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == operator
    assert expression.left.value == 8
    assert expression.right.value == 3


def test_binary_expression_with_identifier():
    program = parse_source("let result = 2 + x")
    expression = program.statements[0].value

    assert isinstance(expression, BinaryExpression)
    assert isinstance(expression.left, NumberLiteral)
    assert isinstance(expression.right, Identifier)
    assert expression.right.name == "x"


# -------------------------
# Invalid syntax
# -------------------------

@pytest.mark.parametrize(
    "source",
    [
        "let = 3",
        "let a 3",
        "let a =",
        "let a = + 3",
        "let a = 2 +",
        "let a = -5",
        "print()",
        "print(2",
        "print 2)",
        "unknown(3)",
        "let a = 3 abc",
    ],
)
def test_invalid_syntax_raises_error(source):
    with pytest.raises(TahaSyntaxError):
        parse_source(source)


def parse_expression(source):
    tokens = Lexer(source).scan_tokens()
    parser = Parser(tokens)
    return parser.parse_expression()


def test_multiplication_has_higher_precedence_than_addition():
    expr = parse_expression("2 + 3 * 4")

    assert isinstance(expr, BinaryExpression)
    assert expr.operator == TokenType.PLUS

    assert isinstance(expr.left, NumberLiteral)
    assert expr.left.value == 2

    assert isinstance(expr.right, BinaryExpression)
    assert expr.right.operator == TokenType.STAR
    assert expr.right.left.value == 3
    assert expr.right.right.value == 4


def test_multiplication_before_addition():
    expr = parse_expression("8 * 3 + 2")

    assert expr.operator == TokenType.PLUS
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.STAR

    assert expr.left.left.value == 8
    assert expr.left.right.value == 3
    assert expr.right.value == 2


def test_subtraction_is_left_associative():
    expr = parse_expression("10 - 3 - 2")

    assert expr.operator == TokenType.MINUS
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.MINUS

    assert expr.left.left.value == 10
    assert expr.left.right.value == 3
    assert expr.right.value == 2


def test_division_and_multiplication_have_same_precedence():
    expr = parse_expression("12 / 3 * 2")

    assert expr.operator == TokenType.STAR
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.SLASH

    assert expr.left.left.value == 12
    assert expr.left.right.value == 3
    assert expr.right.value == 2


def test_addition_and_subtraction_have_same_precedence():
    expr = parse_expression("10 - 3 + 2")

    assert expr.operator == TokenType.PLUS
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.MINUS

    assert expr.left.left.value == 10
    assert expr.left.right.value == 3
    assert expr.right.value == 2


def test_invalid_binary_expression_raises_syntax_error():
    from errors import TahaSyntaxError

    with pytest.raises(TahaSyntaxError):
        parse_expression("2 + * 3")

def parse_source(source):
    tokens = Lexer(source).scan_tokens()
    return Parser(tokens).parse()

def test_empty_block():
    program = parse_source("""
if (True) {
}
""")

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert isinstance(statement.then_branch, BlockStatement)
    assert statement.then_branch.statements == []


def test_block_with_one_statement():
    program = parse_source("""
if (True) {
    print(1)
}
""")

    block = program.statements[0].then_branch

    assert len(block.statements) == 1
    assert isinstance(block.statements[0], PrintStatement)


def test_block_with_multiple_statements():
    program = parse_source("""
if (True) {
    print(1)
    print(2)
    let x = 3
}
""")

    block = program.statements[0].then_branch

    assert len(block.statements) == 3
    assert isinstance(block.statements[0], PrintStatement)
    assert isinstance(block.statements[1], PrintStatement)
    assert isinstance(block.statements[2], LetStatement)


def test_block_with_multiple_blank_lines():
    program = parse_source("""
if (True) {


    print(1)


}
""")

    block = program.statements[0].then_branch

    assert len(block.statements) == 1
    assert isinstance(block.statements[0], PrintStatement)


def test_missing_closing_brace():
    with pytest.raises(TahaSyntaxError):
        parse_source("""
if (True) {
    print(1)
""")


def test_if_without_else():
    program = parse_source("""
if (10 > 5) {
    print(1)
}
""")

    assert isinstance(program, Program)
    assert len(program.statements) == 1

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert isinstance(statement.condition, BinaryExpression)
    assert isinstance(statement.then_branch, BlockStatement)
    assert statement.else_branch is None


def test_if_condition_literal():
    program = parse_source("""
if (True) {
    print(1)
}
""")

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert statement.condition.value is True


def test_if_missing_left_parenthesis():
    with pytest.raises(TahaSyntaxError):
        parse_source("""
if True) {
    print(1)
}
""")


def test_if_missing_right_parenthesis():
    with pytest.raises(TahaSyntaxError):
        parse_source("""
if (True {
    print(1)
}
""")


def test_if_missing_block():
    with pytest.raises(TahaSyntaxError):
        parse_source("""
if (True)
    print(1)
""")


# ---------- Else tests ----------

def test_if_else():
    program = parse_source("""
if (True) {
    print(1)
} else {
    print(2)
}
""")

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert isinstance(statement.then_branch, BlockStatement)
    assert isinstance(statement.else_branch, BlockStatement)

    assert len(statement.then_branch.statements) == 1
    assert len(statement.else_branch.statements) == 1


def test_if_else_with_empty_else_block():
    program = parse_source("""
if (True) {
    print(1)
} else {
}
""")

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert statement.else_branch.statements == []


def test_else_without_if_is_invalid():
    with pytest.raises(TahaSyntaxError):
        parse_source("""
else {
    print(1)
}
""")


# ---------- Nested if/block tests ----------

def test_nested_if():
    program = parse_source("""
if (True) {
    if (False) {
        print(1)
    }
}
""")

    outer = program.statements[0]
    inner = outer.then_branch.statements[0]

    assert isinstance(outer, IfStatement)
    assert isinstance(inner, IfStatement)
    assert inner.else_branch is None


def test_nested_if_else():
    program = parse_source("""
if (True) {
    if (False) {
        print(1)
    } else {
        print(2)
    }
}
""")

    outer = program.statements[0]
    inner = outer.then_branch.statements[0]

    assert isinstance(outer, IfStatement)
    assert isinstance(inner, IfStatement)
    assert isinstance(inner.else_branch, BlockStatement)
 # 