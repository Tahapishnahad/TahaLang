#ast_nodes.py

from dataclasses import dataclass
from tokens import TokenType

class Expression:
    pass

class Statement:
    pass

@dataclass
class Program:
    statements: list[Statement]

@dataclass
class SourceLocation:
    line: int
    column: int

@dataclass
class LetStatement(Statement):
    name: str
    value: Expression
    location: SourceLocation

@dataclass
class BlockStatement(Statement):
    statements: list[Statement]
    location: SourceLocation

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_branch: BlockStatement
    location: SourceLocation
    else_branch: BlockStatement | None = None

@dataclass
class AssignmentStatement(Statement):
    name: str
    value: Expression
    location: SourceLocation

@dataclass
class CompoundAssignmentStatement(Statement):
    name: str
    operator: TokenType
    value: Expression
    location: SourceLocation

@dataclass
class NumberLiteral(Expression):
    value: int | float
    location: SourceLocation

@dataclass
class StringLiteral(Expression):
    value: str
    location: SourceLocation

@dataclass
class BooleanLiteral(Expression):
    value: bool
    location: SourceLocation

@dataclass
class Identifier(Expression):
    name: str
    location: SourceLocation

@dataclass
class IndexExpression(Expression):
    object: Expression
    index: Expression
    location: SourceLocation

@dataclass
class ListExpression(Expression):
    elements: list[Expression]
    location: SourceLocation

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: TokenType
    right: Expression
    location: SourceLocation

@dataclass
class UnaryExpression(Expression):
    operand: Expression
    operator: TokenType
    location: SourceLocation

@dataclass
class CallExpression(Expression):
    callee: Identifier
    arguments: list[Expression]
    location: SourceLocation

@dataclass
class CallStatement(Statement):
    call: CallExpression