#parser.py

from tokens import Token, TokenType
from errors import TahaSyntaxError
from ast_nodes import (
    Program,
    Statement,
    SourceLocation,
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

UNARY_OPERATORS = {
    TokenType.MINUS,
    TokenType.BANG
}

PRECEDENCE = {
    TokenType.EQUAL_EQUAL: 1,
    TokenType.BANG_EQUAL: 1,

    TokenType.LESS: 2,
    TokenType.LESS_EQUAL: 2,
    TokenType.GREATER: 2,
    TokenType.GREATER_EQUAL: 2,

    TokenType.PLUS: 3,
    TokenType.MINUS: 3,

    TokenType.STAR: 4,
    TokenType.SLASH: 4,
    TokenType.PERCENT: 4,
}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        statements = []

        while self.current.type != TokenType.EOF:
            self.skip_newlines()
                

            if self.current.type == TokenType.EOF:
                break
            
            statements.append(
                self.parse_statement()
            )

            if self.current.type not in (TokenType.EOF, TokenType.NEWLINE):
                raise TahaSyntaxError.expected_eof_or_newline(
                    self.current.line,
                    self.current.column,
                    self.current.type.name
                )

        return Program(statements)
        

    def parse_statement(self):
        match self.current.type:
            case TokenType.LET:
                return self.parse_let_statement()

            case TokenType.PRINT:
                return self.parse_print_statement()

            case TokenType.IF:
                return self.parse_if_statement()

            case _:
                raise TahaSyntaxError.unexpected_token_type(
                    self.current.line,
                    self.current.column,
                    Statement.__name__,
                    self.current.type.name
                )

    
    def parse_let_statement(self):
        location = SourceLocation(self.current.line, self.current.column)
        self.advance() # Use 'let'

        identifier = self.consume(
            TokenType.IDENTIFIER
        )

        self.consume(TokenType.EQUAL)

        value = self.parse_expression()

        return LetStatement(name=identifier.value, value=value, location=location)

    def parse_print_statement(self):
        location = SourceLocation(self.current.line, self.current.column)
        self.advance()

        self.consume(TokenType.LEFT_PAREN)

        expression = self.parse_expression()

        self.consume(TokenType.RIGHT_PAREN)

        return PrintStatement(expression, location=location)

    def parse_if_statement(self):
        location = SourceLocation(self.current.line, self.current.column)
        self.advance()

        self.consume(TokenType.LEFT_PAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RIGHT_PAREN)

        then_block = self.parse_block_statement()

        if self.current.type == TokenType.ELSE:
            self.advance()
            else_block = self.parse_block_statement()

            return IfStatement(
                condition=condition,
                then_branch=then_block,
                location=location,
                else_branch=else_block
            )

        return IfStatement(
            condition=condition,
            then_branch=then_block,
            location=location
        )

    def parse_block_statement(self):
        location = self.get_location(self.current)
        self.consume(TokenType.LEFT_BRACE)

        statements = []

        while True:
            self.skip_newlines()

            if self.check(TokenType.EOF):
                raise TahaSyntaxError.unexpected_token_type(
                    self.current.line,
                    self.current.column,
                    expected=TokenType.RIGHT_BRACE,
                    got=TokenType.EOF
                )

            if self.check(TokenType.RIGHT_BRACE):
                break

            statements.append(self.parse_statement())

            if not self.check(TokenType.RIGHT_BRACE):
                self.consume(TokenType.NEWLINE)

        self.consume(TokenType.RIGHT_BRACE)

        return BlockStatement(
            statements=statements,
            location=location
        )

    def parse_expression(self):
        return self.parse_binary_expression(1)


    def parse_primary(self):
        token = self.current
        location = self.get_location(token)

        match token.type:
            case TokenType.INTEGER:
                return self._parse_literal(token, int(token.value), NumberLiteral)

            case TokenType.FLOAT:
                return self._parse_literal(token, float(token.value), NumberLiteral)

            case TokenType.STRING:
                return self._parse_literal(token, token.value, StringLiteral)

            case TokenType.TRUE:
                return self._parse_literal(token, True, BooleanLiteral)

            case TokenType.FALSE:
                return self._parse_literal(token, False, BooleanLiteral)
            
            case TokenType.IDENTIFIER:
                self.advance()
                return Identifier(
                    token.value,
                    location
                )

            case TokenType.LEFT_PAREN:
                self.advance()
                expression = self.parse_expression()
                self.consume(TokenType.RIGHT_PAREN)
                return expression

            case _:
                raise TahaSyntaxError.invalid_expression(
                    location.line,
                    location.column
                )

    def _parse_literal(self, token, value, literal_class):
        self.advance()

        return literal_class(
            value,
            self.get_location(token)
        )

    def parse_binary_expression(self, min_precedence: int):
        left = self.parse_unary()

        while True:
            current_token = self.current

            if current_token.type not in PRECEDENCE:
                break

            precedence = PRECEDENCE[current_token.type]

            if precedence < min_precedence:
                break

            operator_token = self.advance()
            right = self.parse_binary_expression(precedence + 1)

            left = BinaryExpression(
                left=left, 
                operator=operator_token.type, 
                right=right,
                location=left.location
            )

        return left

    def parse_unary(self):
        current_token = self.current
        location = self.get_location(current_token)

        if current_token.type in UNARY_OPERATORS:
            self.advance()
            operand = self.parse_unary()

            return UnaryExpression(
                operand=operand,
                operator=current_token.type,
                location=location
            )

        return self.parse_primary()
    
    @property
    def current(self) -> Token:
        return self.tokens[self.position]

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, tokens):

        validate_eof_count = sum(
            token.type == TokenType.EOF
            for token in tokens
        ) == 1
        
        if len(tokens) == 0:
            raise ValueError("Inner Error: Empty tokens is invalid. checkout lexer.py")

        validate_types = all(
            isinstance(token, Token)
            for token in tokens
        )

        if not validate_types:
            raise ValueError("Inner Error: 'tokens' members must be Token.")


        validate_eof_position = tokens[-1].type == TokenType.EOF

        if not validate_eof_count or not validate_eof_position:
            raise ValueError("Inner Error: EOF not found or It's at incorrect position. checkout lexer.py")

        self._tokens = list(tokens)

    def advance(self) -> Token:

        if self.position > len(self.tokens)-1 or self.position < 0:
            raise ValueError("Inner Error: Invalid position for current tokens list.")

        if self.current.type == TokenType.EOF:
            return self.current

        current_token = self.current
        self.position += 1

        return current_token

    def check(self, token_type:TokenType) -> bool:
        return self.current.type == token_type

    def consume(self, token_type:TokenType):
        current_token = self.current

        if current_token.type != token_type:
            raise TahaSyntaxError.unexpected_token_type(
                line=current_token.line,
                column=current_token.column,
                expected=token_type.name,
                got=current_token.type.name
            )

        self.advance()
        return current_token

    def get_location(self, token: Token) -> SourceLocation:
        return SourceLocation(
            line=token.line,
            column=token.column
        )

    def skip_newlines(self):
        while self.check(TokenType.NEWLINE):
            self.advance()
