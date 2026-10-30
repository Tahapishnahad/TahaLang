#parser.py

from tokens import Token, TokenType
from errors import TahaSyntaxError
from lexer import Lexer
from ast_nodes import (
    Program,
    Statement,
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

BINARY_OPERATORS = {
    TokenType.PLUS,
    TokenType.MINUS,
    TokenType.STAR,
    TokenType.SLASH,
    TokenType.PERCENT,
}

UNARY_OPERATORS = {
    TokenType.MINUS,
    TokenType.BANG
}

PRECEDENCE = {
    TokenType.EQUAL_EQUAL: 1,
    TokenType.BANG_EQUAL: 1,
    TokenType.LESS: 1,
    TokenType.LESS_EQUAL: 1,
    TokenType.GREATER: 1,
    TokenType.GREATER_EQUAL: 1,

    TokenType.PLUS: 2,
    TokenType.MINUS: 2,

    TokenType.STAR: 3,
    TokenType.SLASH: 3,
    TokenType.PERCENT: 3,
}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        statements = []

        while self.current.type != TokenType.EOF:
            while self.current.type == TokenType.NEWLINE:
                self.advance()

            if self.current.type == TokenType.EOF:
                break
            
            statements.append(
                self.parse_statement()
            )

            if self.current.type not in [TokenType.EOF, TokenType.NEWLINE]:
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
        self.advance() # Use 'let'

        identifier = self.consume(
            TokenType.IDENTIFIER
        )

        self.consume(TokenType.EQUAL)

        value = self.parse_expression()

        return LetStatement(name=identifier.value, value=value)

    def parse_print_statement(self):
        self.advance()

        self.consume(TokenType.LEFT_PAREN)

        expression = self.parse_expression()

        self.consume(TokenType.RIGHT_PAREN)

        return PrintStatement(expression)

    def parse_if_statement(self):
        self.advance()

        self.consume(TokenType.LEFT_PAREN)

        condition = self.parse_expression()

        self.consume(TokenType.RIGHT_PAREN)

        then_block = self.parse_block_statement()

        if self.current.type == TokenType.ELSE: # Can not use after NEWLINE(s), just after '}' for IF block.
            self.advance()
            else_block = self.parse_block_statement()
            return IfStatement(condition, then_block, else_block)

        return IfStatement(condition, then_block)

    def parse_block_statement(self):
        self.consume(TokenType.LEFT_BRACE)

        statements = []

        while self.current.type != TokenType.RIGHT_BRACE:
            if self.current.type == TokenType.EOF:
                raise TahaSyntaxError.unexpected_token_type(
                    self.current.line,
                    self.current.column,
                    expected=TokenType.RIGHT_BRACE,
                    got=TokenType.EOF
                )

            while self.current.type == TokenType.NEWLINE:
                self.advance()

            if self.current.type != TokenType.RIGHT_BRACE:
                statements.append(self.parse_statement())
            else:
                break

        self.consume(TokenType.RIGHT_BRACE)

        return BlockStatement(statements)

    def parse_expression(self):
        return self.parse_binary_expression(1)


    def parse_primary(self):
        current_token = self.current

        match current_token.type:
            case TokenType.INTEGER:
                self.advance()
                return NumberLiteral(int(current_token.value))

            case TokenType.FLOAT:
                self.advance()
                return NumberLiteral(float(current_token.value))

            case TokenType.STRING:
                self.advance()
                return StringLiteral(current_token.value)

            case TokenType.TRUE:
                self.advance()
                return BooleanLiteral(True)

            case TokenType.FALSE:
                self.advance()
                return BooleanLiteral(False)

            case TokenType.IDENTIFIER:
                self.advance()
                return Identifier(current_token.value)

            case TokenType.LEFT_PAREN:
                self.advance()
                expression = self.parse_expression()
                self.consume(TokenType.RIGHT_PAREN)
                return expression

            case _:
                raise TahaSyntaxError.invalid_expression(
                    current_token.line,
                    current_token.column
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

            op = self.advance()
            right = self.parse_binary_expression(precedence + 1)

            left = BinaryExpression(left, op.type, right)

        return left

    def parse_unary(self):
        left = self.current


        if left.type in UNARY_OPERATORS:
            self.advance()
            operand = self.parse_unary()

            return UnaryExpression(operand=operand, operator=left.type)

        return self.parse_primary()
    
    @property
    def current(self) -> Token:
        return self.tokens[self.position]

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, tokens):

        types = []    

        if len(tokens) == 0:
            raise ValueError("Inner Error: Empty tokens is invalid. checkout lexer.py")

        for token in tokens:
            types.append(token.type)
        
        if (not TokenType.EOF in types) or (types.count(TokenType.EOF) > 1) or types[-1] != TokenType.EOF:
            raise ValueError("Inner Error: EOF need to check. checkout lexer.py")

        self._tokens = tokens

    def advance(self) -> Token:
        if self.current.type == TokenType.EOF:
            return self.current

        if self.position > len(self.tokens)-1 or self.position < 0:
            raise ValueError("Inner Error: Invalid position for current tokens list.")

        current_token = self.current
        self.position += 1

        return current_token

    def check(self, token_type:TokenType) -> bool:
        return self.current.type == token_type

    def match(self, token_types:list):
        if self.current.type in token_types:
            self.advance()
            return True

        return False

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

def main():
    p = Parser(
        Lexer(
            'print(10 * --5)'
        ).scan_tokens()
    )

    print(p.parse())


if __name__ == "__main__":
    main()