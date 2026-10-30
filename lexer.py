#lexer.py

from tokens import Token, TokenType
from errors import LexicalError

SINGLE_CHAR_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "%": TokenType.PERCENT,
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE
}

COMPOUND_OPERATOR_STARTS = {"=", "<", ">", "!"}

KEYWORDS = {
    "let": TokenType.LET,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "print": TokenType.PRINT,
    "True": TokenType.TRUE,
    "False": TokenType.FALSE
}

ESCAPE_ALLOWED = {"n", "t", "\\", "\""}

class Lexer:

    def __init__(self, source):
        self.source = source
        self.position = 0
        self.tokens = []
        self.line = 1
        self.column = 1


    def scan_tokens(self):
        while not self.is_at_end():
            self.skip_whitespace()

            if self.is_at_end():
                break

            if self.is_digit():
                self.scan_number()

            elif self.peek() == "\n":
                self.scan_token(TokenType.NEWLINE, "\n")

            elif self.is_alpha():
                self.scan_identifier()

            elif self.peek() in SINGLE_CHAR_TOKENS or self.peek() in COMPOUND_OPERATOR_STARTS:
                self.scan_operator()

            elif self.peek() == "\"":
                self.scan_string()

            else:
                raise LexicalError.unexpected_character(
                    self.peek(),
                    self.line,
                    self.column
                )
                

        self.tokens.append(
            Token(
                type=TokenType.EOF,
                value="",
                line=self.line,
                column=self.column
            )
        )

        return self.tokens


    def scan_number(self):
        line = self.line
        column = self.column
        number = self.read_number()

        if "." in number:
            self.add_token(
                TokenType.FLOAT,
                number,
                line,
                column
            )
        else:
            self.add_token(
                TokenType.INTEGER,
                number,
                line,
                column
            )


    def scan_operator(self):
        if self.peek() in SINGLE_CHAR_TOKENS:
            self.scan_token(
                SINGLE_CHAR_TOKENS[self.peek()],
                self.peek(),
            )
        else:
            match self.peek():
                case "=":
                    if self.peek_next() == "=":
                        self.scan_two_tokens(TokenType.EQUAL_EQUAL, "==")
                    else:
                        self.scan_token(TokenType.EQUAL, "=")

                case "<":
                    if self.peek_next() == "=":
                        self.scan_two_tokens(TokenType.LESS_EQUAL, "<=")
                    else:
                        self.scan_token(TokenType.LESS, "<")

                case ">":
                    if self.peek_next() == "=":
                        self.scan_two_tokens(TokenType.GREATER_EQUAL, ">=")
                    else:
                        self.scan_token(TokenType.GREATER, ">")

                case "!":
                    if self.peek_next() == "=":
                        self.scan_two_tokens(TokenType.BANG_EQUAL, "!=")
                    else:
                        self.scan_token(TokenType.BANG, "!")


    def scan_identifier(self):
        line = self.line
        column = self.column
        start = self.position

        while self.is_alphanumeric():
            self.advance()

        word = self.source[start:self.position]

        if word in KEYWORDS:
            self.add_token(KEYWORDS[word], word, line, column)

        else:
            self.add_token(
                TokenType.IDENTIFIER,
                word,
                line,
                column
            )


    def scan_string(self):
        line = self.line
        column = self.column

        string = self.read_string()

        self.add_token(
            TokenType.STRING,
            string,
            line,
            column
        )


    def scan_token(self, token_type, value):
        line = self.line
        column = self.column

        self.advance()
        self.add_token(token_type, value, line, column)


    def scan_two_tokens(self, token_type, value):
        line = self.line
        column = self.column

        self.advance()
        self.advance()

        self.add_token(token_type, value, line, column)


    def read_number(self):
        start = self.position

        while self.is_digit() or self.peek() == ".":
            if self.peek() == ".":

                if self.peek_next() is None:
                    raise LexicalError.unexpected_number(

                        self.line,
                        self.column
                    )

                if self.is_digit(self.peek_next()) and "." not in self.source[start:self.position]:
                    self.advance()

                else:
                    raise LexicalError.unexpected_number(

                        self.line,
                        self.column
                    )

            elif self.is_digit():
                self.advance()

        final_num = self.source[start:self.position]
        return final_num


    def read_string(self):
        string = ""

        if self.peek() == "\"":
            self.advance()

        while not self.is_at_end():
            if self.peek() == "\"":
                self.advance()
                return string

            elif self.peek() == "\\":
                if self.peek_next() is None:
                    raise LexicalError.unterminated_string(
                        line=self.line,
                        column=self.column
                    )

                if self.peek_next() in ESCAPE_ALLOWED:
                    string += "\\"
                    self.advance()
                    string += self.advance()
                else:
                    raise LexicalError.unexpected_escape(
                        line=self.line,
                        column=self.column
                    )

            elif self.peek() == "\n":
                raise LexicalError.newline_in_string(
                    line=self.line,
                    column=self.column
                )

            else:
                string += self.peek()
                self.advance()

        raise LexicalError.unterminated_string(
            self.line,
            self.column
        )


    def add_token(self, token_type, value, line, column):
        self.tokens.append(
            Token(
                type=token_type,
                value=value,
                line=line,
                column=column
            )
        )


    def advance(self):
        if self.is_at_end():
            return None

        char = self.source[self.position]
        self.position += 1

        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return char


    def peek(self):
        return None if self.is_at_end() else self.source[self.position]


    def peek_next(self):
        if self.position + 1 >= len(self.source):
            return None
        return self.source[self.position + 1]


    def skip_whitespace(self):
        while not self.is_at_end() and self.peek() in [" ", "\t"]:
            self.advance()


    def is_alpha(self):
        char = self.peek()

        return (
            char is not None
            and (
                "a" <= char <= "z"
                or "A" <= char <= "Z"
                or char == "_"
            )
        )


    def is_alphanumeric(self):
        char = self.peek()
        return char is not None and (
            self.is_alpha() or self.is_digit()
        )


    def is_digit(self, char=None):
        char = self.peek() if char is None else char
        return char is not None and "0" <= char <= "9"


    def is_at_end(self):
        return self.position == len(self.source)

