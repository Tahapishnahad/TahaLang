# test_ast_nodes.py

from tokens import TokenType
from ast_nodes import (
    Program,
    Statement,
    Expression,
    LetStatement,
    PrintStatement,
    BlockStatement,
    IfStatement,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    Identifier,
    BinaryExpression,
    UnaryExpression,
)


def test_program_stores_statements():
    statement = PrintStatement(expression=NumberLiteral(value=10))
    program = Program(statements=[statement])

    assert len(program.statements) == 1
    assert program.statements[0] is statement


def test_let_statement():
    value = NumberLiteral(value=13)
    statement = LetStatement(name="age", value=value)

    assert statement.name == "age"
    assert statement.value is value


def test_print_statement():
    expression = StringLiteral(value="Hello")
    statement = PrintStatement(expression=expression)

    assert statement.expression is expression


def test_block_statement():
    statements = [
        LetStatement(name="x", value=NumberLiteral(value=5)),
        PrintStatement(expression=Identifier(name="x")),
    ]
    block = BlockStatement(statements=statements)

    assert len(block.statements) == 2
    assert block.statements == statements


def test_if_statement_with_else():
    condition = BooleanLiteral(value=True)
    then_branch = BlockStatement(statements=[])
    else_branch = BlockStatement(statements=[])

    statement = IfStatement(
        condition=condition,
        then_branch=then_branch,
        else_branch=else_branch,
    )

    assert statement.condition is condition
    assert statement.then_branch is then_branch
    assert statement.else_branch is else_branch


def test_if_statement_without_else():
    statement = IfStatement(
        condition=BooleanLiteral(value=False),
        then_branch=BlockStatement(statements=[]),
    )

    assert statement.else_branch is None


def test_number_literal_integer():
    node = NumberLiteral(value=13)

    assert node.value == 13
    assert type(node.value) is int


def test_number_literal_float():
    node = NumberLiteral(value=3.5)

    assert node.value == 3.5
    assert type(node.value) is float


def test_string_literal():
    node = StringLiteral(value="Hello\nTahaLang")

    assert node.value == "Hello\nTahaLang"


def test_boolean_literal():
    true_node = BooleanLiteral(value=True)
    false_node = BooleanLiteral(value=False)

    assert true_node.value is True
    assert false_node.value is False


def test_identifier():
    node = Identifier(name="total")

    assert node.name == "total"


def test_binary_expression():
    left = Identifier(name="age")
    right = NumberLiteral(value=5)

    expression = BinaryExpression(
        left=left,
        operator=TokenType.PLUS,
        right=right,
    )

    assert expression.left is left
    assert expression.operator is TokenType.PLUS
    assert expression.right is right


def test_unary_expression():
    operand = NumberLiteral(value=5)

    expression = UnaryExpression(
        operand=operand,
        operator=TokenType.MINUS,
    )

    assert expression.operand is operand
    assert expression.operator is TokenType.MINUS


def test_ast_node_inheritance():
    assert isinstance(NumberLiteral(value=1),Expression)

    assert isinstance(LetStatement(name="x", value=NumberLiteral(value=1)),Statement)
