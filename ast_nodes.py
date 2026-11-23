#ast_nodes.py

from dataclasses import dataclass
from tokens import TokenType

class Expression:
    """Base class for AST nodes that represent expressions which can be evaluated to produce a value."""
    
    pass

class Statement:
    """Base class for AST nodes that represent executable statements in a program."""
    
    pass

@dataclass
class Program:
    """
    Represents the root node of the Abstract Syntax Tree.

    Attributes:
        statements: A list of all top-level statements in the program.
    """

    statements: list[Statement]

@dataclass
class SourceLocation:
    """
    Represents the location of an AST node in the source code.

    Attributes:
        line: The line number where the node appears.
        column: The column number where the node appears.
    """
    
    line: int
    column: int

@dataclass
class LetStatement(Statement):
    """
    Represents a variable declaration statement.

    Attributes:
        name: The name of the variable being declared.
        value: The expression whose result initializes the variable.
        location: The source location of the declaration.
    """

    name: str
    value: Expression
    location: SourceLocation

@dataclass
class BlockStatement(Statement):
    """
    Represents a block of statements.

    Attributes:
        statements: A list of statements contained in the block.
        location: The source location of the block.
    """

    statements: list[Statement]
    location: SourceLocation

@dataclass
class IfStatement(Statement):
    """
    Represents an if/else statement.

    Attributes:
        condition: Condition of if statement.
        then_branch: A block whose statements are executed when the condition is true.
        location: The source location of the if statement.
        else_branch: An optional block whose statements are executed when the condition is false.
    """

    condition: Expression
    then_branch: BlockStatement
    location: SourceLocation
    else_branch: BlockStatement | None = None

@dataclass
class AssignmentStatement(Statement):
    """
    Represents an assignment statement.

    Attributes:
        name: The name of the variable whose value is being updated.
        value: The expression evaluated to determine the new value.
        location: The source location of the assignment statement.
    """

    name: str
    value: Expression
    location: SourceLocation

@dataclass
class CompoundAssignmentStatement(Statement):
    """
    Represents a compound assignment statement.

    Attributes:
        name: The name of the variable whose value is being updated.
        operator: The TokenType that identifies the assignment operator.
        value: The expression evaluated as part of the compound assignment.
        location: The source location of the compound assignment statement.
    """

    name: str
    operator: TokenType
    value: Expression
    location: SourceLocation

@dataclass
class WhileStatement(Statement):
    """
    Represents a while loop statement.

    Attributes:
        condition: An expression that determines whether the loop body should execute.
        body: The block of statements executed while the condition evaluates to True.
        location: The source location of the while statement.
    """

    condition: Expression
    body: BlockStatement
    location: SourceLocation

@dataclass
class NumberLiteral(Expression):
    """
    Represents a numeric literal (integer or floating-point number).

    Attributes:
        value: The numeric value represented by the literal.
        location: The source location of the number literal.
    """
    
    value: int | float
    location: SourceLocation

@dataclass
class StringLiteral(Expression):
    """
    Represents a string literal.

    Attributes:
        value: The string value represented by the literal.
        location: The source location of the string literal.
    """
        
    value: str
    location: SourceLocation

@dataclass
class BooleanLiteral(Expression):
    """
    Represents a boolean literal.

    Attributes:
        value: The boolean value represented by the literal.
        location: The source location of the boolean literal.
    """

    value: bool
    location: SourceLocation

@dataclass
class Identifier(Expression):
    """
    Represents an identifier expression.

    Attributes:
        name: The name of the identifier used to reference a variable.
        location: The source location of the identifier.
    """
    
    name: str
    location: SourceLocation

@dataclass
class IndexExpression(Expression):
    """
    Represents an index expression used to access an element of an object.

    Attributes:
        object: The expression representing the object being indexed.
        index: The expression representing the index used to access an element.
        location: The source location of the index expression.
    """

    object: Expression
    index: Expression
    location: SourceLocation

@dataclass
class ListExpression(Expression):
    """
    Represents a list expression.

    Attributes:
        elements: A list of expressions contained in the list.
        location: The source location of the list expression.
    """

    elements: list[Expression]
    location: SourceLocation

@dataclass
class BinaryExpression(Expression):
    """
    Represents a binary expression involving two operands and an operator.

    Attributes:
        left: The expression representing the left operand.
        operator: The operator applied to the two operands.
        right: The expression representing the right operand.
        location: The source location of the binary expression.
    """

    left: Expression
    operator: TokenType
    right: Expression
    location: SourceLocation

@dataclass
class UnaryExpression(Expression):
    """
    Represents a unary expression involving an operand and an operator.

    Attributes:
        operand: The expression representing the operand.
        operator: The operator applied to the operand.
        location: The source location of the unary expression.
    """

    operand: Expression
    operator: TokenType
    location: SourceLocation

@dataclass
class CallExpression(Expression):
    """
    Represents a call expression used for calling functions.

    Attributes:
        callee: The identifier representing the function name.
        arguments: A list of expressions representing the function arguments.
        location: The source location of the call expression.
    """

    callee: Identifier
    arguments: list[Expression]
    location: SourceLocation

@dataclass
class CallStatement(Statement):
    """
    Represents a function call used as a statement.

    Attributes:
        call: The call expression representing the function invocation.
    """

    call: CallExpression

@dataclass
class ForStatement(Statement):
    """
    Represents a for loop statement. format: for(init ; condition ; update) {}

    Arguments:
        init: A part of for loop statement who defines loop variable.
        condition: A (Expresison) part of for loop statement who will be checked every time the body got runed.
        update: A part of for loop statement who will be executed every time the body got runed and updates variable.
        body: A part of for loop statament who contains statements and they will got executed every time who condition returns true. 
        location: The source location of the for loop statement.
    """

    init: LetStatement
    condition: Expression
    update: Statement
    body: BlockStatement
    location: SourceLocation