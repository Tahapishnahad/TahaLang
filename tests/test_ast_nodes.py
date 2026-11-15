from tokens import TokenType
from ast_nodes import (
    Program,
    Statement,
    Expression,
    SourceLocation,
    LetStatement,
    BlockStatement,
    IfStatement,
    NumberLiteral,
    StringLiteral,
    BooleanLiteral,
    Identifier,
    BinaryExpression,
    UnaryExpression,
    ListExpression,
    IndexExpression,
    CallExpression,
    CallStatement,
    AssignmentStatement
)

LOC = SourceLocation(1, 1)

def test_program_stores_statements():
    statement = Identifier(
        name="print",
        location=LOC
    )

    program = Program(statements=[statement])

    assert len(program.statements) == 1
    assert program.statements[0] is statement
    assert statement.location == LOC


def test_let_statement():
    value = NumberLiteral(
        value=13,
        location=LOC
    )
    statement = LetStatement(
        name="age",
        value=value,
        location=SourceLocation(1, 2)
    )

    assert statement.name == "age"
    assert statement.value is value
    assert statement.location == SourceLocation(1, 2)


def test_block_statement():
    statements = [
        LetStatement(
            name="x",
            value=NumberLiteral(
                value=5,
                location=SourceLocation(2, 6)
            ),
            location=SourceLocation(1, 2)
        ),

        Identifier(
            name="print",
            location=SourceLocation(3, 2)
        ),
    ]

    block = BlockStatement(
        statements=statements,
        location=SourceLocation(1, 15)
    )

    assert len(block.statements) == 2
    assert block.statements == statements
    assert block.location == SourceLocation(1, 15)


def test_if_statement_with_else():
    condition = BooleanLiteral(
        value=True,
        location=SourceLocation(1, 5)
    )
    then_branch = BlockStatement(
        statements=[],
        location=SourceLocation(1, 12)
    )
    else_branch = BlockStatement(
        statements=[],
        location=SourceLocation(2, 7)
    )

    statement = IfStatement(
        condition=condition,
        then_branch=then_branch,
        location=SourceLocation(1, 1),
        else_branch=else_branch
    )

    assert statement.condition is condition
    assert statement.then_branch is then_branch
    assert statement.else_branch is else_branch
    assert statement.location == SourceLocation(1, 1)


def test_if_statement_without_else():
    condition = BooleanLiteral(
        value=False,
        location=SourceLocation(1, 5)
    )
    then_branch = BlockStatement(
        statements=[],
        location=SourceLocation(1, 13)
    )

    statement = IfStatement(
        condition=condition,
        then_branch=then_branch,
        location=SourceLocation(1, 1)
    )

    assert statement.else_branch is None
    assert statement.location == SourceLocation(1, 1)


def test_number_literal_integer():
    node = NumberLiteral(
        value=13,
        location=SourceLocation(2, 6)
    )

    assert node.value == 13
    assert type(node.value) is int


def test_number_literal_float():
    node = NumberLiteral(
        value=3.5,
        location=SourceLocation(2, 6)
    )

    assert node.value == 3.5
    assert type(node.value) is float


def test_string_literal():
    node = StringLiteral(
        value="Hello\nTahaLang",
        location=SourceLocation(2, 6)
    )

    assert node.value == "Hello\nTahaLang"


def test_boolean_literal():
    true_node = BooleanLiteral(
        value=True,
        location=SourceLocation(2, 6)
    )
    false_node = BooleanLiteral(
        value=False,
        location=SourceLocation(2, 6)
    )

    assert true_node.value is True
    assert false_node.value is False


def test_identifier():
    node = Identifier(
        name="total",
        location=SourceLocation(2, 6)
    )

    assert node.name == "total"
    assert node.location.line == 2
    assert node.location.column == 6

    node = Identifier(
        name="print",
        location=SourceLocation(9, 7)
    )

    assert node.name == "print"
    assert node.location.line == 9
    assert node.location.column == 7


def test_binary_expression():
    left = Identifier(
        name="age",
        location=SourceLocation(2, 6)
    )
    right = NumberLiteral(
        value=5,
        location=SourceLocation(2, 12)
    )

    expression = BinaryExpression(
        left=left,
        operator=TokenType.PLUS,
        right=right,
        location=SourceLocation(2, 6)
    )

    assert expression.left is left
    assert expression.operator is TokenType.PLUS
    assert expression.right is right


def test_unary_expression():
    operand = NumberLiteral(
        value=5,
        location=SourceLocation(2, 7)
    )

    expression = UnaryExpression(
        operand=operand,
        operator=TokenType.MINUS,
        location=SourceLocation(2, 6)
    )

    assert expression.operand is operand
    assert expression.operator is TokenType.MINUS


def test_ast_node_inheritance():
    number = NumberLiteral(
        value=1,
        location=SourceLocation(2, 6)
    )
    statement = LetStatement(
        name="x",
        value=number,
        location=SourceLocation(1, 1)
    )

    assert isinstance(number, Expression)
    assert isinstance(statement, Statement)


def test_source_location():
    location = SourceLocation(line=1, column=3)

    assert location.line == 1
    assert location.column == 3


def test_source_location_in_expression():
    expression = BinaryExpression(
        left=NumberLiteral(
            2,
            SourceLocation(3, 4)
        ),
        operator=TokenType.PLUS,
        right=NumberLiteral(
            4,
            SourceLocation(3, 8)
        ),
        location=SourceLocation(3, 4)
    )

    assert expression.location == SourceLocation(3, 4)

def test_list_expression():
    temp_location = SourceLocation(1, 1)

    list_expr = ListExpression(
        elements=[NumberLiteral(19, temp_location)],
        location=temp_location
    )

    assert len(list_expr.elements) == 1
    assert list_expr.elements[0].value == 19
    assert list_expr.elements[0].location == temp_location

    list_expr = ListExpression(
        elements=[NumberLiteral(19, temp_location), NumberLiteral(23, temp_location)],
        location=temp_location
    )

    assert len(list_expr.elements) == 2
    assert list_expr.elements[0].value == 19
    assert list_expr.elements[0].location == temp_location
    assert list_expr.elements[1].value == 23
    assert list_expr.elements[1].location == temp_location

    list_expr = ListExpression(
        elements=[NumberLiteral(19, temp_location), BinaryExpression(
            left=NumberLiteral(20, temp_location), operator=TokenType.PLUS, right=NumberLiteral(10, temp_location), location=temp_location
        )],
        location=temp_location
    )

    assert len(list_expr.elements) == 2
    assert list_expr.elements[0].value == 19
    assert list_expr.elements[0].location == temp_location
    assert list_expr.elements[1].left.value == 20
    assert list_expr.elements[1].right.value == 10
    assert list_expr.elements[1].operator == TokenType.PLUS
    assert list_expr.elements[1].location == temp_location

    list_expr = ListExpression(
        elements=[NumberLiteral(19, temp_location), StringLiteral("Taha", location=temp_location), BooleanLiteral(True, temp_location)],
        location=temp_location
    )

    assert len(list_expr.elements) == 3
    assert list_expr.elements[0].value == 19
    assert list_expr.elements[0].location == temp_location
    assert list_expr.elements[1].value == "Taha"
    assert list_expr.elements[1].location == temp_location
    assert list_expr.elements[2].value == True
    assert list_expr.elements[2].location == temp_location

    list_expr = ListExpression(
        elements=[],
        location=temp_location
    )

    assert len(list_expr.elements) == 0

def test_index_expression():
    temp_location = SourceLocation(1, 1)

    list_expr = ListExpression(
        elements=[NumberLiteral(10, temp_location), NumberLiteral(20, temp_location), NumberLiteral(30, temp_location)],
        location=temp_location
    )

    index_expr = IndexExpression(
        object=list_expr,
        index=NumberLiteral(1, temp_location),
        location=temp_location
    )

    assert index_expr.object == list_expr
    assert index_expr.location == temp_location
    assert index_expr.index.value == 1
    assert index_expr.index.location == temp_location

    identifier = Identifier("list", temp_location)
    index_expr = IndexExpression(
        object=identifier,
        index=NumberLiteral(1, temp_location),
        location=temp_location
    )

    assert index_expr.index.value == 1
    assert index_expr.index.location == temp_location
    assert index_expr.object.name == "list"
    assert index_expr.object.location == temp_location
    assert index_expr.location == temp_location

# -------------------------
# CallExpression
# -------------------------

def test_call_expression():
    callee = Identifier(
        name="len",
        location=SourceLocation(1, 1)
    )

    argument = StringLiteral(
        value="Hello",
        location=SourceLocation(1, 5)
    )

    expression = CallExpression(
        callee=callee,
        arguments=[argument],
        location=SourceLocation(1, 1)
    )

    assert isinstance(expression, Expression)
    assert expression.callee is callee
    assert expression.arguments == [argument]
    assert expression.location == SourceLocation(1, 1)


def test_call_expression_with_multiple_arguments():
    callee = Identifier(
        name="calculate",
        location=SourceLocation(1, 1)
    )

    arguments = [
        NumberLiteral(value=10, location=SourceLocation(1, 11)),
        NumberLiteral(value=20, location=SourceLocation(1, 15)),
    ]

    expression = CallExpression(
        callee=callee,
        arguments=arguments,
        location=SourceLocation(1, 1)
    )

    assert len(expression.arguments) == 2
    assert expression.arguments[0].value == 10
    assert expression.arguments[1].value == 20


def test_call_expression_without_arguments():
    expression = CallExpression(
        callee=Identifier(
            name="some_function",
            location=SourceLocation(1, 1)
        ),
        arguments=[],
        location=SourceLocation(1, 1)
    )

    assert expression.arguments == []

# -------------=------------
# CallStatement
# -------------------------

def test_call_statement():
    call = CallExpression(
        callee=Identifier(
            name="print",
            location=SourceLocation(1, 1)
        ),
        arguments=[
            StringLiteral(
                value="Hello",
                location=SourceLocation(1, 7)
            )
        ],
        location=SourceLocation(1, 1)
    )

    statement = CallStatement(call=call)

    assert isinstance(statement, Statement)
    assert statement.call is call
    assert isinstance(statement.call, CallExpression)


def test_call_statement_with_no_arguments():
    call = CallExpression(
        callee=Identifier(
            name="print",
            location=SourceLocation(1, 1)
        ),
        arguments=[],
        location=SourceLocation(1, 1)
    )

    statement = CallStatement(call=call)

    assert statement.call.arguments == []

def test_assignment_statement():
    assignment = AssignmentStatement(
        "age",
        value=NumberLiteral(17, LOC),
        location=LOC
    )

    assert assignment.name == "age"
    assert isinstance(assignment.value, NumberLiteral)
    assert assignment.value.value == 17
    assert assignment.value.location == LOC
    assert assignment.location == LOC