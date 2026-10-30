#ast_nodes.py

from dataclasses import dataclass
from tokens import TokenType

@dataclass
class Program:
    statements: list

class Expression:
    pass

class Statement:
    pass

@dataclass
class LetStatement(Statement):
    name: str
    value: Expression

@dataclass
class PrintStatement(Statement):
    expression: Expression

@dataclass
class BlockStatement(Statement):
    statements: list

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_branch: BlockStatement
    else_branch: BlockStatement | None = None

@dataclass
class NumberLiteral(Expression):
    value: int | float

@dataclass
class StringLiteral(Expression):
    value: str

@dataclass
class BooleanLiteral(Expression):
    value: bool

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: TokenType
    right: Expression

@dataclass
class UnaryExpression(Expression):
    operand: Expression
    operator: TokenType