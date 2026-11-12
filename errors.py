#errors.py

class TahaLangError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(message)


    def __str__(self):
        return f"{type(self).__name__} at line {self.line}, column {self.column}: {self.message}"


class LexicalError(TahaLangError):
    def __init__(self, message, line, column):
        super().__init__(message, line, column)


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


class TahaSyntaxError(TahaLangError):
    def __init__(self, message, line, column):
        super().__init__(message, line, column)


    @classmethod
    def unexpected_token_type(cls, line, column, expected, got):
        return cls(f"Unexpected token type: {got}, expected: {expected}", line, column)


    @classmethod
    def expected_primary(cls, line, column, got):
        return cls(f"Expected INTEGER, FLOAT, STRING, TRUE, FALSE, IDENTIFIER , got: {got}", line, column)


    @classmethod
    def unexpected_eof(cls, line, column, expected):
        return cls(f"Unexpected EOF, expected: {expected}", line, column)

    @classmethod
    def invalid_expression(cls, line, column):
        return cls("Invalid expression.", line, column)

    @classmethod
    def expected_eof_or_newline(cls, line, column, got):
        return cls(f"Expected EOF or NEWLINE, got: {got}", line, column)

    @classmethod
    def unexpected_comma_in_list_expression(cls, line, column):
        return cls("Unexpected COMMA in list expression", line, column)

    @classmethod
    def expected_expression_after_comma(cls, line, column, got):
        return cls(f"Expected Expression after COMMA. got: {got}", line, column)

    @classmethod
    def expected_list_or_identifier_for_postfix(cls, line, column, got):
        return cls(f"Expected list or identifier for locating index. got: {got}", line, column)


class TahaRuntimeError(TahaLangError):
    def __init__(self, message, line, column):
        super().__init__(message, line, column)


    @classmethod
    def division_by_zero(cls, line, column):
        return cls("Division by zero.", line, column)


    @classmethod
    def undefined_variable(cls, line, column, name):
        return cls(f"Undefined variable {name!r}", line, column)


    @classmethod
    def type_error(cls, message, line, column):
        return cls(message, line, column)


    @classmethod
    def variable_already_defined(cls, name, line, column):
        return cls(f"{name!r} is already defined.", line, column)


    @classmethod
    def nested_list(cls, line, column):
        return cls("Nested list. Can't define list expression in another one.", line, column)

    @classmethod
    def invalid_object_for_index_expression(cls, line, column, got):
        return cls(f"Invalid object for index expression, expected iterable got {got}", line, column)

    @classmethod
    def invalid_index(cls, max_index, got_index, line, column):
        return cls(f"Iterable's max index is {max_index}, got: {got_index}", line, column)

    @classmethod
    def negative_index(cls, got, line, column):
        return cls(f"Iterable's index couldn't be negative. index: {got}", line, column)

    @classmethod
    def invalid_type_index(cls, got, line, column):
        return cls(f"Iterable's index must be int. got: {got}", line, column)

    @classmethod
    def zero_index(cls, line, column):
        return cls("Iterable dosen't have any items.", line, column)