#test_parser.py

import pytest

from lexer import Lexer
from parser import Parser
from errors import TahaSyntaxError
from ast_nodes import (
    Program,
    SourceLocation,
    LetStatement,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    Identifier,
    BinaryExpression,
    UnaryExpression,
    IfStatement,
    BlockStatement,
    ListExpression,
    IndexExpression,
    CallExpression,
    CallStatement,
    AssignmentStatement,
    CompoundAssignmentStatement,
    WhileStatement,
    ForStatement
)
from tokens import TokenType


def parse_source(source):
    tokens = Lexer(source).scan_tokens()
    return Parser(tokens).parse()

def get_call_argument(program, statement_index=0, argument_index=0):
    statement = program.statements[statement_index]
    return statement.call.arguments[argument_index]


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
    assert isinstance(program.statements[1], CallStatement)


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
# Function Call Statements
# -------------------------

def test_print_string():
    program = parse_source('print("Hello")')
    statement = program.statements[0]

    assert isinstance(statement, CallStatement)
    assert isinstance(statement.call, CallExpression)

    assert isinstance(statement.call.callee, Identifier)
    assert statement.call.callee.name == "print"

    assert len(statement.call.arguments) == 1
    assert isinstance(statement.call.arguments[0], StringLiteral)
    assert statement.call.arguments[0].value == "Hello"


def test_print_number():
    program = parse_source("print(42)")
    statement = program.statements[0]

    assert isinstance(statement, CallStatement)
    assert isinstance(statement.call, CallExpression)
    assert isinstance(statement.call.arguments[0], NumberLiteral)
    assert statement.call.arguments[0].value == 42


def test_print_binary_expression():
    program = parse_source("print(2 + 3)")
    expression = program.statements[0].call.arguments[0]

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
        TokenType.EQUAL_EQUAL,
        TokenType.BANG_EQUAL,
        TokenType.LESS,
        TokenType.LESS_EQUAL,
        TokenType.GREATER,
        TokenType.GREATER_EQUAL,
    ],
)
def test_all_binary_operators(operator):
    symbols = {
        TokenType.PLUS: "+",
        TokenType.MINUS: "-",
        TokenType.STAR: "*",
        TokenType.SLASH: "/",
        TokenType.PERCENT: "%",
        TokenType.EQUAL_EQUAL: "==",
        TokenType.BANG_EQUAL: "!=",
        TokenType.LESS: "<",
        TokenType.LESS_EQUAL: "<=",
        TokenType.GREATER: ">",
        TokenType.GREATER_EQUAL: ">=",
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
# Unary expressions
# -------------------------

@pytest.mark.parametrize(
    ("source", "operator", "operand_type", "operand_value"),
    [
        ("-5", TokenType.MINUS, NumberLiteral, 5),
        ("!True", TokenType.BANG, BooleanLiteral, True),
    ],
)
def test_unary_expression(source, operator, operand_type, operand_value):
    expression = parse_expression(source)

    assert isinstance(expression, UnaryExpression)
    assert expression.operator == operator
    assert isinstance(expression.operand, operand_type)
    assert expression.operand.value == operand_value


def test_chained_unary_expressions():
    expression = parse_expression("!-5")

    assert isinstance(expression, UnaryExpression)
    assert expression.operator == TokenType.BANG
    assert isinstance(expression.operand, UnaryExpression)
    assert expression.operand.operator == TokenType.MINUS
    assert isinstance(expression.operand.operand, NumberLiteral)
    assert expression.operand.operand.value == 5


def test_unary_expression_has_higher_precedence_than_binary():
    expression = parse_expression("-2 * 3")

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == TokenType.STAR
    assert isinstance(expression.left, UnaryExpression)
    assert expression.left.operator == TokenType.MINUS
    assert expression.left.operand.value == 2
    assert expression.right.value == 3


@pytest.mark.parametrize("source", ["-", "!"])
def test_unary_operator_without_operand_is_invalid(source):
    with pytest.raises(TahaSyntaxError):
        parse_expression(source)


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
        "print(2",
        "print 2)",
        "let a = 3 abc",
        "a = ",
        "a += ",
        "a -= ",
        "a *= ",
        "a /= ",
        "a %= "
    ]
)
def test_invalid_syntax_raises_error(source):
    with pytest.raises(TahaSyntaxError):
        parse_source(source)


def parse_expression(source):
    tokens = Lexer(source).scan_tokens()
    parser = Parser(tokens)

    expression = parser.parse_expression()

    parser.consume(TokenType.EOF)

    return expression


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


def test_comparison_has_lower_precedence_than_addition():
    expr = parse_expression("2 + 3 < 8")

    assert isinstance(expr, BinaryExpression)
    assert expr.operator == TokenType.LESS
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.PLUS
    assert expr.left.left.value == 2
    assert expr.left.right.value == 3
    assert expr.right.value == 8

def test_nested_expression_precedence():
    expr = parse_expression("1 + 2 < 5 == True")

    assert isinstance(expr, BinaryExpression)
    assert expr.operator == TokenType.EQUAL_EQUAL
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.LESS
    assert expr.left.left.operator == TokenType.PLUS
    assert expr.left.right.value == 5
    assert isinstance(expr.right, BooleanLiteral)
    assert expr.right.value is True

def test_equality_has_lower_precedence_than_relational_operators():
    expr = parse_expression("1 < 2 == True")

    assert isinstance(expr, BinaryExpression)
    assert expr.operator == TokenType.EQUAL_EQUAL
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.LESS
    assert expr.left.left.value == 1
    assert expr.left.right.value == 2
    assert isinstance(expr.right, BooleanLiteral)
    assert expr.right.value is True


def test_invalid_binary_expression_raises_syntax_error():
    with pytest.raises(TahaSyntaxError):
        parse_expression("2 + * 3")

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
    assert isinstance(block.statements[0], CallStatement)


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
    assert isinstance(block.statements[0], CallStatement)
    assert isinstance(block.statements[1], CallStatement)
    assert isinstance(block.statements[2], LetStatement)


def test_block_with_multiple_blank_lines():
    program = parse_source("""
if (True) {


    print(1)


}
""")

    block = program.statements[0].then_branch

    assert len(block.statements) == 1
    assert isinstance(block.statements[0], CallStatement)


def test_block_last_statement_can_be_immediately_followed_by_closing_brace():
    program = parse_source("if (True) { print(1)}")

    block = program.statements[0].then_branch
    assert len(block.statements) == 1
    assert isinstance(block.statements[0], CallStatement)


@pytest.mark.parametrize(
    "source",
    [
        "if (True) { print(1) print(2) }",
        "if (True) { let x = 1 let y = 2 }",
    ],
)
def test_block_requires_newline_between_statements(source):
    with pytest.raises(TahaSyntaxError):
        parse_source(source)


def test_block_allows_multiple_blank_lines_before_closing_brace():
    program = parse_source("""if (True) {
print(1)



}""")

    block = program.statements[0].then_branch
    assert len(block.statements) == 1

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

def test_number_literal_location():
    program = parse_source("print(123)")

    expression = get_call_argument(program)

    assert expression.location == SourceLocation(1, 7)


def test_binary_expression_location():
    program = parse_source("print(10 + 20)")

    expression = get_call_argument(program)

    assert expression.location == SourceLocation(1, 7)


def test_unary_expression_location():
    program = parse_source("print(-10)")

    expression = get_call_argument(program)

    assert expression.location == SourceLocation(1, 7)


# =========================
# Additional precedence tests
# =========================

def test_equality_has_lower_precedence_than_relational():
    expr = parse_expression("1 == 2 < 3")

    assert isinstance(expr, BinaryExpression)
    assert expr.operator == TokenType.EQUAL_EQUAL

    assert isinstance(expr.left, NumberLiteral)
    assert expr.left.value == 1

    assert isinstance(expr.right, BinaryExpression)
    assert expr.right.operator == TokenType.LESS
    assert expr.right.left.value == 2
    assert expr.right.right.value == 3


def test_relational_operators_are_left_associative():
    expr = parse_expression("1 < 2 > 3")

    assert expr.operator == TokenType.GREATER
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.LESS

    assert expr.left.left.value == 1
    assert expr.left.right.value == 2
    assert expr.right.value == 3


def test_equality_operators_are_left_associative():
    expr = parse_expression("1 == 2 != 3")

    assert expr.operator == TokenType.BANG_EQUAL
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.EQUAL_EQUAL

    assert expr.left.left.value == 1
    assert expr.left.right.value == 2
    assert expr.right.value == 3


def test_multiplication_operators_are_left_associative():
    expr = parse_expression("2 * 3 / 4")

    assert expr.operator == TokenType.SLASH
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.STAR

    assert expr.left.left.value == 2
    assert expr.left.right.value == 3
    assert expr.right.value == 4


# =========================
# Parenthesized expressions
# =========================

def test_parentheses_override_precedence():
    expr = parse_expression("(2 + 3) * 4")

    assert expr.operator == TokenType.STAR
    assert isinstance(expr.left, BinaryExpression)
    assert expr.left.operator == TokenType.PLUS

    assert expr.left.left.value == 2
    assert expr.left.right.value == 3
    assert expr.right.value == 4


def test_nested_parentheses():
    expr = parse_expression("((2 + 3) * (4 - 1))")

    assert expr.operator == TokenType.STAR
    assert expr.left.operator == TokenType.PLUS
    assert expr.right.operator == TokenType.MINUS


def test_unary_expression_with_parenthesized_operand():
    expr = parse_expression("-(2 + 3)")

    assert isinstance(expr, UnaryExpression)
    assert expr.operator == TokenType.MINUS
    assert isinstance(expr.operand, BinaryExpression)
    assert expr.operand.operator == TokenType.PLUS


def test_unary_expression_inside_parentheses():
    expr = parse_expression("(-2) * 3")

    assert isinstance(expr, BinaryExpression)
    assert expr.operator == TokenType.STAR
    assert isinstance(expr.left, UnaryExpression)
    assert expr.left.operand.value == 2


def test_multiple_unary_operators():
    expr = parse_expression("---5")

    assert isinstance(expr, UnaryExpression)
    assert expr.operator == TokenType.MINUS

    assert isinstance(expr.operand, UnaryExpression)
    assert expr.operand.operator == TokenType.MINUS

    assert isinstance(expr.operand.operand, UnaryExpression)
    assert expr.operand.operand.operator == TokenType.MINUS

    assert expr.operand.operand.operand.value == 5


# =========================
# Expression edge cases
# =========================

@pytest.mark.parametrize(
    "source",
    [
        "()",
        "(1 + 2",
        "1 + 2)",
        "((1 + 2)",
        "1 + (2 * 3",
        "1 + ()",
        "1 ** 2",
    ],
)
def test_invalid_parenthesized_expressions(source):
    with pytest.raises(TahaSyntaxError):
        parse_expression(source)


# =========================
# Program statement boundaries
# =========================

def test_multiple_statements_with_blank_lines():
    program = parse_source(
        "let a = 1\n\n\nlet b = 2\n\nprint(a + b)"
    )

    assert len(program.statements) == 3


def test_trailing_newlines_are_allowed():
    program = parse_source("let a = 1\n\n\n")

    assert len(program.statements) == 1


@pytest.mark.parametrize(
    "source",
    [
        "print(1) print(2)",
        "let a = 1 let b = 2",
        "print(1) let a = 2",
        "}",
        "else {}",
    ],
)
def test_invalid_top_level_statement_boundaries(source):
    with pytest.raises(TahaSyntaxError):
        parse_source(source)


# =========================
# Block edge cases
# =========================

def test_empty_block_on_single_line():
    program = parse_source("if (True) {}")

    block = program.statements[0].then_branch

    assert isinstance(block, BlockStatement)
    assert block.statements == []


def test_block_with_trailing_newlines():
    program = parse_source("""
if (True) {
    print(1)


}
""")

    block = program.statements[0].then_branch

    assert len(block.statements) == 1


def test_nested_blocks():
    program = parse_source("""
if (True) {
    if (False) {
        print(1)
    }
}
""")

    outer = program.statements[0]
    inner = outer.then_branch.statements[0]

    assert isinstance(outer.then_branch, BlockStatement)
    assert isinstance(inner.then_branch, BlockStatement)


# =========================
# If / Else edge cases
# =========================

@pytest.mark.parametrize(
    "source",
    [
        "if () {}",
        "if (True) {",
        "if (True) {} else",
        "if (True) {} else print(1)",
        "if (True) {} else {} else {}",
        "if (True) {}\nelse {}",
    ],
)
def test_invalid_if_else_syntax(source):
    with pytest.raises(TahaSyntaxError):
        parse_source(source)


def test_else_belongs_to_nearest_if():
    program = parse_source("""
if (True) {
    if (False) {
        print(1)
    } else {
        print(2)
    }
} else {
    print(3)
}
""")

    outer = program.statements[0]
    inner = outer.then_branch.statements[0]

    assert isinstance(outer, IfStatement)
    assert isinstance(inner, IfStatement)

    assert inner.else_branch is not None
    assert outer.else_branch is not None


# =========================
# Source location edge cases
# =========================

def test_string_literal_location():
    program = parse_source('print("hello")')

    expression = get_call_argument(program)

    assert expression.location == SourceLocation(1, 7)


def test_boolean_literal_location():
    program = parse_source("print(True)")

    expression = get_call_argument(program)

    assert expression.location == SourceLocation(1, 7)


def test_identifier_location():
    program = parse_source("print(value)")

    expression = get_call_argument(program)

    assert expression.location == SourceLocation(1, 7)


def test_nested_unary_location():
    program = parse_source("print(!-5)")

    expression = get_call_argument(program)

    assert expression.location == SourceLocation(1, 7)
    assert expression.operand.location == SourceLocation(1, 8)


def test_binary_expression_with_unary_left_location():
    program = parse_source("print(-1 * 2)")

    expression = get_call_argument(program)

    assert expression.location == SourceLocation(1, 7)
    assert expression.left.location == SourceLocation(1, 7)

# =========================
# Statement source locations
# =========================

def test_let_statement_location():
    program = parse_source("let value = 10")

    statement = program.statements[0]

    assert isinstance(statement, LetStatement)
    assert statement.location == SourceLocation(1, 1)


def test_call_statement_location():
    program = parse_source("print(10)")

    statement = program.statements[0]

    assert isinstance(statement, CallStatement)
    assert statement.call.location == SourceLocation(1, 1)


def test_if_statement_location():
    program = parse_source("if (True) {}")

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert statement.location == SourceLocation(1, 1)


def test_block_statement_location():
    program = parse_source("if (True) {}")

    block = program.statements[0].then_branch

    assert isinstance(block, BlockStatement)
    assert block.location == SourceLocation(1, 11)


def test_else_block_statement_location():
    program = parse_source("if (True) {} else {}")

    statement = program.statements[0]

    assert statement.then_branch.location == SourceLocation(1, 11)
    assert statement.else_branch.location == SourceLocation(1, 19)


def test_nested_statement_locations():
    program = parse_source(
        "if (True) {\n"
        "    print(1)\n"
        "}"
    )

    if_statement = program.statements[0]
    block = if_statement.then_branch
    print_statement = block.statements[0]

    assert if_statement.location == SourceLocation(1, 1)
    assert block.location == SourceLocation(1, 11)
    assert print_statement.call.location == SourceLocation(2, 5)

def test_list_expression():
    lexer = Lexer("[10, 20, 30]")
    parser = Parser(tokens=lexer.scan_tokens())

    list_expr = parser.parse_expression()

    assert len(list_expr.elements) == 3
    assert list_expr.location.line == 1
    assert list_expr.location.column == 1
    assert list_expr.elements[0].value == 10
    assert list_expr.elements[1].value == 20
    assert list_expr.elements[2].value == 30
    assert isinstance(list_expr.elements[0], NumberLiteral)
    assert isinstance(list_expr.elements[1], NumberLiteral)
    assert isinstance(list_expr.elements[2], NumberLiteral)
    assert list_expr.elements[0].location.line == 1
    assert list_expr.elements[0].location.column == 2
    assert list_expr.elements[1].location.line == 1
    assert list_expr.elements[1].location.column == 6
    assert list_expr.elements[2].location.line == 1
    assert list_expr.elements[2].location.column == 10

def test_empty_list_expression():
    lexer = Lexer("[]")
    parser = Parser(tokens=lexer.scan_tokens())

    result = parser.parse_expression()

    assert isinstance(result, ListExpression)
    assert result.elements == []
    assert result.location.line == 1
    assert result.location.column == 1

def test_single_element_list_expression():
    lexer = Lexer("[42]")
    parser = Parser(tokens=lexer.scan_tokens())

    result = parser.parse_expression()

    assert isinstance(result, ListExpression)
    assert len(result.elements) == 1
    assert isinstance(result.elements[0], NumberLiteral)
    assert result.elements[0].value == 42

def test_list_expression_with_binary_expressions():
    lexer = Lexer("[10 + 5, 20 * 2]")
    parser = Parser(tokens=lexer.scan_tokens())

    result = parser.parse_expression()

    assert isinstance(result, ListExpression)
    assert len(result.elements) == 2

    first = result.elements[0]
    second = result.elements[1]

    assert isinstance(first, BinaryExpression)
    assert first.left.value == 10
    assert first.right.value == 5
    assert first.operator == TokenType.PLUS

    assert isinstance(second, BinaryExpression)
    assert second.left.value == 20
    assert second.right.value == 2
    assert second.operator == TokenType.STAR

def test_heterogeneous_list_expression():
    lexer = Lexer('[19, "Taha", True]')
    parser = Parser(tokens=lexer.scan_tokens())

    result = parser.parse_expression()

    assert isinstance(result, ListExpression)
    assert len(result.elements) == 3

    assert isinstance(result.elements[0], NumberLiteral)
    assert isinstance(result.elements[1], StringLiteral)
    assert isinstance(result.elements[2], BooleanLiteral)

    assert result.elements[0].value == 19
    assert result.elements[1].value == "Taha"
    assert result.elements[2].value is True

@pytest.mark.parametrize("source", [
    "[10,]",
    "[10,,20]",
    "[,10]",
    "[10 20]",
    "[10, 20",
])
def test_invalid_list_expression(source):
    lexer = Lexer(source)
    parser = Parser(tokens=lexer.scan_tokens())

    with pytest.raises(TahaSyntaxError):
        parser.parse_expression()

def test_parse_postfix():
    # Identifier Indexing
    lexer = Lexer("number[0]")
    parser = Parser(lexer.scan_tokens())
    ast_nodes = parser.parse_postfix()

    assert isinstance(ast_nodes, IndexExpression)
    assert isinstance(ast_nodes.object, Identifier)
    assert ast_nodes.object.name == "number"
    assert ast_nodes.location.line == 1
    assert ast_nodes.location.column == 1
    assert ast_nodes.index.value == 0
    assert isinstance(ast_nodes.index, NumberLiteral)
    assert ast_nodes.index.location.line == 1
    assert ast_nodes.index.location.column == 8

    # List Expression Indexing
    lexer = Lexer("[1, 2, 3][1]")
    parser = Parser(lexer.scan_tokens())
    ast_nodes = parser.parse_postfix()

    assert isinstance(ast_nodes, IndexExpression)
    assert isinstance(ast_nodes.object, ListExpression)
    assert ast_nodes.object.elements[0].value == 1
    assert ast_nodes.object.elements[1].value == 2
    assert ast_nodes.object.elements[2].value == 3
    assert isinstance(ast_nodes.index, NumberLiteral)
    assert ast_nodes.index.value == 1
    assert ast_nodes.location.line == 1
    assert ast_nodes.location.column == 1
    assert ast_nodes.object.location.line == 1
    assert ast_nodes.object.location.column == 1
    assert ast_nodes.index.location.line == 1
    assert ast_nodes.index.location.column == 11

    # Expression Indexing
    lexer = Lexer("numbers[1 + 5]")
    parser = Parser(lexer.scan_tokens())
    ast_nodes = parser.parse_postfix()

    assert isinstance(ast_nodes, IndexExpression)
    assert isinstance(ast_nodes.object, Identifier)
    assert isinstance(ast_nodes.index, BinaryExpression)
    assert ast_nodes.object.name == "numbers"
    assert ast_nodes.object.location.line == 1
    assert ast_nodes.object.location.column == 1
    assert ast_nodes.index.left.value == 1
    assert ast_nodes.index.left.location.line == 1
    assert ast_nodes.index.left.location.column == 9
    assert ast_nodes.index.operator == TokenType.PLUS
    assert ast_nodes.index.right.value == 5
    assert ast_nodes.index.right.location.line == 1
    assert ast_nodes.index.right.location.column == 13

@pytest.mark.parametrize("source", [
    "numbers[10",
    "numbers[]",
    "numbers[1 +]"
])
def test_invalid_postfix_expression(source):
    lexer = Lexer(source)
    parser = Parser(tokens=lexer.scan_tokens())

    with pytest.raises(TahaSyntaxError):
        parser.parse_postfix()

# Next Updates
@pytest.mark.parametrize("source", [
    "let result = numbers[1][9]",
])
def test_chained_indexing_is_invalid(source):
    lexer = Lexer(source)
    parser = Parser(tokens=lexer.scan_tokens())

    with pytest.raises(TahaSyntaxError):
        parser.parse()

# =========================
# Function Call Expressions
# =========================

def test_call_expression():
    expression = parse_expression('len("Hello")')

    assert isinstance(expression, CallExpression)
    assert isinstance(expression.callee, Identifier)
    assert expression.callee.name == "len"

    assert len(expression.arguments) == 1
    assert isinstance(expression.arguments[0], StringLiteral)
    assert expression.arguments[0].value == "Hello"


def test_call_expression_with_multiple_arguments():
    expression = parse_expression("some_function(10, 20, 30)")

    assert isinstance(expression, CallExpression)
    assert len(expression.arguments) == 3

    assert expression.arguments[0].value == 10
    assert expression.arguments[1].value == 20
    assert expression.arguments[2].value == 30


def test_call_expression_with_no_arguments():
    expression = parse_expression("some_function()")

    assert isinstance(expression, CallExpression)
    assert expression.callee.name == "some_function"
    assert expression.arguments == []


def test_call_expression_inside_binary_expression():
    expression = parse_expression('len("Hello") + 5')

    assert isinstance(expression, BinaryExpression)
    assert expression.operator == TokenType.PLUS

    assert isinstance(expression.left, CallExpression)
    assert expression.left.callee.name == "len"
    assert expression.left.arguments[0].value == "Hello"

    assert isinstance(expression.right, NumberLiteral)
    assert expression.right.value == 5


def test_call_expression_inside_let_statement():
    program = parse_source('let result = len("Hello")')

    statement = program.statements[0]

    assert isinstance(statement, LetStatement)
    assert isinstance(statement.value, CallExpression)
    assert statement.value.callee.name == "len"


def test_nested_call_expression():
    expression = parse_expression('outer(inner("Hello"))')

    assert isinstance(expression, CallExpression)
    assert expression.callee.name == "outer"

    inner_call = expression.arguments[0]

    assert isinstance(inner_call, CallExpression)
    assert inner_call.callee.name == "inner"
    assert inner_call.arguments[0].value == "Hello"


# =========================
# Invalid Function Calls
# =========================

@pytest.mark.parametrize(
    "source",
    [
        "some_function(,)",
        "some_function(10,,20)",
        "some_function(10,)",
        "some_function(10 20)",
        "some_function(10",
    ],
)
def test_invalid_function_call(source):
    with pytest.raises(TahaSyntaxError):
        parse_expression(source)


def test_parse_assignment():
    source = parse_source("a = 9")
    assignment = source.statements[0]

    assert isinstance(assignment, AssignmentStatement)
    assert isinstance(assignment.value, NumberLiteral)

    assert assignment.location == SourceLocation(1, 1)
    assert assignment.value.location == SourceLocation(1, 5)

    assert assignment.name == "a"

    assert assignment.value.value == 9

def test_parse_assignment_with_binarsy_expression():
    source = parse_source("age = 9 + 10")
    assignment = source.statements[0]

    assert isinstance(assignment, AssignmentStatement)
    assert isinstance(assignment.value, BinaryExpression)

    assert assignment.location == SourceLocation(1, 1)
    assert assignment.value.location == SourceLocation(1, 7)

    assert assignment.name == "age"

    assert assignment.value.left.value == 9
    assert assignment.value.right.value == 10

def test_parse_compound_assignment_plus_equal():
    source = parse_source("a += 9")
    assignment = source.statements[0]

    assert isinstance(assignment, CompoundAssignmentStatement)
    assert isinstance(assignment.value, NumberLiteral)

    assert assignment.location == SourceLocation(1, 1)
    assert assignment.value.location == SourceLocation(1, 6)

    assert assignment.operator == TokenType.PLUS_EQUAL

    assert assignment.name == "a"

    assert assignment.value.value == 9

@pytest.mark.parametrize(
    ("source", "token_type"),
    [
        ("a += 9", TokenType.PLUS_EQUAL),
        ("a -= 9", TokenType.MINUS_EQUAL),
        ("a *= 9", TokenType.STAR_EQUAL),
        ("a /= 9", TokenType.SLASH_EQUAL),
        ("a %= 9", TokenType.PERCENT_EQUAL)
    ]
)
def test_parse_compound_assignment_numbers(source, token_type):
    source = parse_source(source)
    assignment = source.statements[0]

    assert isinstance(assignment, CompoundAssignmentStatement)
    assert isinstance(assignment.value, NumberLiteral)

    assert assignment.location == SourceLocation(1, 1)
    assert assignment.value.location == SourceLocation(1, 6)

    assert assignment.operator == token_type

    assert assignment.name == "a"

    assert assignment.value.value == 9

@pytest.mark.parametrize(
    ("source", "token_type"),
    [
        ('a += "string"', TokenType.PLUS_EQUAL),
        ('a -= "string"', TokenType.MINUS_EQUAL),
        ('a *= "string"', TokenType.STAR_EQUAL),
        ('a /= "string"', TokenType.SLASH_EQUAL),
        ('a %= "string"', TokenType.PERCENT_EQUAL)
    ]
)
def test_parse_compound_assignment_strings(source, token_type):
    source = parse_source(source)
    assignment = source.statements[0]

    assert isinstance(assignment, CompoundAssignmentStatement)
    assert isinstance(assignment.value, StringLiteral)

    assert assignment.location == SourceLocation(1, 1)
    assert assignment.value.location == SourceLocation(1, 6)

    assert assignment.operator == token_type

    assert assignment.name == "a"

    assert assignment.value.value == "string"

def test_parse_while_statement():
    source = "while (a != 9){\n a += 1 \n}"
    result = parse_source(source).statements[0]

    assert isinstance(result, WhileStatement)
    assert isinstance(result.condition, BinaryExpression)
    assert isinstance(result.body, BlockStatement)
    assert len(result.body.statements) == 1
    assert result.location == SourceLocation(1, 1)

    assert result.condition.left.name == "a"
    assert result.condition.right.value == 9
    assert result.condition.operator == TokenType.BANG_EQUAL
    assert result.condition.location == SourceLocation(1, 8)

    assert isinstance(result.body.statements[0], CompoundAssignmentStatement)
    assert result.body.statements[0].name == "a"
    assert result.body.statements[0].operator == TokenType.PLUS_EQUAL
    assert result.body.statements[0].value.value == 1
    assert result.body.statements[0].location == SourceLocation(2, 2)

def test_parse_for_statement():
    source = "for (let i = 1; i <= 5; i += 1) {\n print(i) \n}"
    for_ast = parse_source(source).statements[0]

    assert isinstance(for_ast, ForStatement)
    assert isinstance(for_ast.init, LetStatement)
    assert isinstance(for_ast.init.value, NumberLiteral)
    assert isinstance(for_ast.condition, BinaryExpression)
    assert isinstance(for_ast.condition.left, Identifier)
    assert isinstance(for_ast.condition.right, NumberLiteral)
    assert isinstance(for_ast.update, CompoundAssignmentStatement)
    assert isinstance(for_ast.update.value, NumberLiteral)
    assert isinstance(for_ast.body, BlockStatement)
    assert isinstance(for_ast.body.statements[0], CallStatement)
    assert isinstance(for_ast.body.statements[0].call, CallExpression)
    assert isinstance(for_ast.body.statements[0].call.callee, Identifier)
    assert isinstance(for_ast.body.statements[0].call.arguments[0], Identifier)

    assert for_ast.location == SourceLocation(1, 1)
    assert for_ast.init.location == SourceLocation(1, 6)
    assert for_ast.init.value.location == SourceLocation(1, 14)
    assert for_ast.condition.location == SourceLocation(1, 17)
    assert for_ast.condition.left.location == SourceLocation(1, 17)
    assert for_ast.condition.right.location == SourceLocation(1, 22)
    assert for_ast.update.location == SourceLocation(1, 25)
    assert for_ast.update.value.location == SourceLocation(1, 30)
    assert for_ast.body.location == SourceLocation(1, 33)
    assert for_ast.body.statements[0].call.location == SourceLocation(2, 2)
    assert for_ast.body.statements[0].call.callee.location == SourceLocation(2, 2)
    assert for_ast.body.statements[0].call.arguments[0].location == SourceLocation(2, 8)

    assert len(for_ast.body.statements) == 1

    assert for_ast.init.value.value == 1
    assert for_ast.init.name == "i"

    assert for_ast.condition.left.name == "i"
    assert for_ast.condition.operator == TokenType.LESS_EQUAL
    assert for_ast.condition.right.value == 5

    assert for_ast.update.name == "i"
    assert for_ast.update.operator == TokenType.PLUS_EQUAL
    assert for_ast.update.value.value == 1

    assert for_ast.body.statements[0].call.callee.name == "print"
    assert for_ast.body.statements[0].call.arguments[0].name == "i"

def test_parse_for_statement_with_boolean_condition():
    source = "for (let i = 1; True; i += 1) {\n print(i) \n}"
    for_ast = parse_source(source).statements[0]

    assert isinstance(for_ast, ForStatement)
    assert isinstance(for_ast.init, LetStatement)
    assert isinstance(for_ast.init.value, NumberLiteral)
    assert isinstance(for_ast.condition, BooleanLiteral)
    assert isinstance(for_ast.update, CompoundAssignmentStatement)
    assert isinstance(for_ast.update.value, NumberLiteral)
    assert isinstance(for_ast.body, BlockStatement)
    assert isinstance(for_ast.body.statements[0], CallStatement)
    assert isinstance(for_ast.body.statements[0].call, CallExpression)
    assert isinstance(for_ast.body.statements[0].call.callee, Identifier)
    assert isinstance(for_ast.body.statements[0].call.arguments[0], Identifier)

    assert for_ast.location == SourceLocation(1, 1)
    assert for_ast.init.location == SourceLocation(1, 6)
    assert for_ast.init.value.location == SourceLocation(1, 14)
    assert for_ast.condition.location == SourceLocation(1, 17)
    assert for_ast.update.location == SourceLocation(1, 23)
    assert for_ast.update.value.location == SourceLocation(1, 28)
    assert for_ast.body.location == SourceLocation(1, 31)
    assert for_ast.body.statements[0].call.location == SourceLocation(2, 2)
    assert for_ast.body.statements[0].call.callee.location == SourceLocation(2, 2)
    assert for_ast.body.statements[0].call.arguments[0].location == SourceLocation(2, 8)

    assert len(for_ast.body.statements) == 1

    assert for_ast.init.value.value == 1
    assert for_ast.init.name == "i"

    assert for_ast.condition.value is True

    assert for_ast.update.name == "i"
    assert for_ast.update.operator == TokenType.PLUS_EQUAL
    assert for_ast.update.value.value == 1

    assert for_ast.body.statements[0].call.callee.name == "print"
    assert for_ast.body.statements[0].call.arguments[0].name == "i"

def test_parse_for_statement_with_empty_body():
    source = "for (let i = 1; True; i += 1) {}"
    for_ast = parse_source(source).statements[0]

    assert isinstance(for_ast, ForStatement)
    assert isinstance(for_ast.init, LetStatement)
    assert isinstance(for_ast.init.value, NumberLiteral)
    assert isinstance(for_ast.condition, BooleanLiteral)
    assert isinstance(for_ast.update, CompoundAssignmentStatement)
    assert isinstance(for_ast.update.value, NumberLiteral)
    assert isinstance(for_ast.body, BlockStatement)

    assert for_ast.location == SourceLocation(1, 1)
    assert for_ast.init.location == SourceLocation(1, 6)
    assert for_ast.init.value.location == SourceLocation(1, 14)
    assert for_ast.condition.location == SourceLocation(1, 17)
    assert for_ast.update.location == SourceLocation(1, 23)
    assert for_ast.update.value.location == SourceLocation(1, 28)
    assert for_ast.body.location == SourceLocation(1, 31)

    assert len(for_ast.body.statements) == 0

    assert for_ast.init.value.value == 1
    assert for_ast.init.name == "i"

    assert for_ast.condition.value is True

    assert for_ast.update.name == "i"
    assert for_ast.update.operator == TokenType.PLUS_EQUAL
    assert for_ast.update.value.value == 1

def test_parse_for_statement_with_assignment_update():
    source = "for (let i = 1; i <= 5; i = 5) {\n print(i) \n}"
    for_ast = parse_source(source).statements[0]

    assert isinstance(for_ast, ForStatement)
    assert isinstance(for_ast.init, LetStatement)
    assert isinstance(for_ast.init.value, NumberLiteral)
    assert isinstance(for_ast.condition, BinaryExpression)
    assert isinstance(for_ast.condition.left, Identifier)
    assert isinstance(for_ast.condition.right, NumberLiteral)
    assert isinstance(for_ast.update, AssignmentStatement)
    assert isinstance(for_ast.update.value, NumberLiteral)
    assert isinstance(for_ast.body, BlockStatement)
    assert isinstance(for_ast.body.statements[0], CallStatement)
    assert isinstance(for_ast.body.statements[0].call, CallExpression)
    assert isinstance(for_ast.body.statements[0].call.callee, Identifier)
    assert isinstance(for_ast.body.statements[0].call.arguments[0], Identifier)

    assert for_ast.location == SourceLocation(1, 1)
    assert for_ast.init.location == SourceLocation(1, 6)
    assert for_ast.init.value.location == SourceLocation(1, 14)
    assert for_ast.condition.location == SourceLocation(1, 17)
    assert for_ast.condition.left.location == SourceLocation(1, 17)
    assert for_ast.condition.right.location == SourceLocation(1, 22)
    assert for_ast.update.location == SourceLocation(1, 25)
    assert for_ast.update.value.location == SourceLocation(1, 29)
    assert for_ast.body.location == SourceLocation(1, 32)
    assert for_ast.body.statements[0].call.location == SourceLocation(2, 2)
    assert for_ast.body.statements[0].call.callee.location == SourceLocation(2, 2)
    assert for_ast.body.statements[0].call.arguments[0].location == SourceLocation(2, 8)

    assert len(for_ast.body.statements) == 1

    assert for_ast.init.value.value == 1
    assert for_ast.init.name == "i"

    assert for_ast.condition.left.name == "i"
    assert for_ast.condition.operator == TokenType.LESS_EQUAL
    assert for_ast.condition.right.value == 5

    assert for_ast.update.name == "i"
    assert for_ast.update.value.value == 5

    assert for_ast.body.statements[0].call.callee.name == "print"
    assert for_ast.body.statements[0].call.arguments[0].name == "i"

@pytest.mark.parametrize(
    ("source", "error_msg"),
    [
        (
            "for (let i = 10; i > 0;) {}",
            "TahaSyntaxError at line 1, column 24: Unexpected token type: RIGHT_PAREN, expected: Statement"
        ),

        (
            "for (let i = 10;; i += 1) {}", 
            "TahaSyntaxError at line 1, column 17: Invalid expression."
        ),

        (
            "for (; i < 0; i += 1) {}",
            "TahaSyntaxError at line 1, column 10: Unexpected token type: LESS, expected: EQUAL"
        ),

        (
            "for (let i = 10; i < 0; i += 1)", 
            "TahaSyntaxError at line 1, column 32: Unexpected token type: EOF, expected: LEFT_BRACE"
        ),

        (
            "for (let i = 10; i < 0; i += 1 {}", 
            "TahaSyntaxError at line 1, column 32: Unexpected token type: LEFT_BRACE, expected: RIGHT_PAREN"
        ),

        (
            "for let i = 10; i < 0; i += 1) {}", 
            "TahaSyntaxError at line 1, column 5: Unexpected token type: LET, expected: LEFT_PAREN"
        ),

        (
            "for (let i = 10 i < 0; i += 1) {}", 
            "TahaSyntaxError at line 1, column 17: Unexpected token type: IDENTIFIER, expected: SEMICOLON"
        ),

        (
            "for (let i = 10; i < 0 i += 1) {}", 
            "TahaSyntaxError at line 1, column 24: Unexpected token type: IDENTIFIER, expected: SEMICOLON"
        ),

        (
            "for (let i  10; i < 0 i += 1) {}", 
            "TahaSyntaxError at line 1, column 13: Unexpected token type: INTEGER, expected: EQUAL"
        ),

        (
            "for (let i = 10; i  0 i += 1) {}", 
            "TahaSyntaxError at line 1, column 21: Unexpected token type: INTEGER, expected: SEMICOLON"
        ),

    ]
)
def test_for_statement_syntax_errors(source, error_msg):
    with pytest.raises(TahaSyntaxError) as exc:
        parse_source(source)

    assert str(exc.value) == error_msg