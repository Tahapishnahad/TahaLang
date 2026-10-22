
class LexicalError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(message)

    def __str__(self):
        return f"LexicalError at line {self.line}, column {self.column}: {self.message}"

    @classmethod
    def unexpected_number(cls, line, column):
        return cls(f"Unexpected number.", line, column)

    @classmethod
    def unexpected_character(cls, char, line, column):
        return cls(f"Unexpected character {char!r}.", line, column)

    @classmethod
    def unexpected_escape(cls, line, column):
        return cls(f"Unexpected escape sequence.", line, column)

    @classmethod
    def newline_in_string(cls, line, column):
        return cls("Newline inside string literal.", line, column)

    @classmethod
    def unterminated_string(cls, line, column):
        return cls("Unterminated string.", line, column)