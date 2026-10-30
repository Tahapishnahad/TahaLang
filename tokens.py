#tokens.py

from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    EOF = "EOF"
    NEWLINE = "NEWLINE"

    LET = "LET"
    IF = "IF"
    ELSE = "ELSE"
    PRINT = "PRINT"
    TRUE = "TRUE"
    FALSE = "FALSE"

    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"

    PLUS = "PLUS" # +
    MINUS = "MINUS" # -
    STAR = "STAR" # *
    SLASH = "SLASH" # /
    PERCENT = "PERCENT" # %
    BANG = "BANG" # !

    EQUAL_EQUAL = "EQUAL_EQUAL" # ==
    BANG_EQUAL = "BANG_EQUAL" # !=
    LESS = "LESS" # <
    LESS_EQUAL = "LESS_EQUAL" # <=
    GREATER = "GREATER" # >
    GREATER_EQUAL = "GREATER_EQUAL" # >=

    EQUAL = "EQUAL" # =

    LEFT_PAREN = "LEFT_PAREN" # (
    RIGHT_PAREN = "RIGHT_PAREN" # )
    LEFT_BRACE = "LEFT_BRACE" # {
    RIGHT_BRACE = "RIGHT_BRACE" # }

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
