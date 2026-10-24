from errors import (
    LexicalError,
    TahaSyntaxError,
    TahaRuntimeError,
    TahaLangError
)
import pytest

def test_lexical_error_string():
    error = LexicalError.unexpected_character("@", 3, 7)

    assert str(error) == (
        "LexicalError at line 3, column 7: "
        "Unexpected character '@'."
    )


def test_syntax_error_string():
    error = TahaSyntaxError.invalid_expression(5, 2)

    assert str(error) == (
        "TahaSyntaxError at line 5, column 2: Invalid expression."
    )


def test_runtime_error_string():
    error = TahaRuntimeError.division_by_zero(8, 4)

    assert str(error) == (
        "TahaRuntimeError at line 8, column 4: Division by zero."
    )

def test_error_attributes():
    error = LexicalError.unexpected_character("@", 3, 7)

    assert error.message == "Unexpected character '@'."
    assert error.line == 3
    assert error.column == 7

def test_error_inheritance():
    assert issubclass(LexicalError, Exception)
    assert issubclass(TahaSyntaxError, Exception)
    assert issubclass(TahaRuntimeError, Exception)

    assert issubclass(LexicalError, TahaLangError)
    assert issubclass(TahaSyntaxError, TahaLangError)
    assert issubclass(TahaRuntimeError, TahaLangError)

@pytest.mark.parametrize(
    ("error", "expected_message"),
    [
        (
            LexicalError.unexpected_number(1, 2),
             "Unexpected number."
        ),

        (
            LexicalError.unexpected_character("@", 1, 2),
            "Unexpected character '@'.",
        ),

        (
            LexicalError.unexpected_escape(1, 2),
            "Unexpected escape sequence.",
        ),

        (
            LexicalError.newline_in_string(1, 2),
            "Newline inside string literal.",
        ),

        (
            LexicalError.unterminated_string(1, 2),
            "Unterminated string.",
        ),

    ],

)

def test_lexical_error_factories(error, expected_message):
    assert error.message == expected_message
    assert error.line == 1
    assert error.column == 2



@pytest.mark.parametrize(
    ("error", "expected_message"),
    [
        (
            TahaSyntaxError.unexpected_token_type(1, 2, expected="EQUAL", got="FALSE"),
              "Unexpected token type: FALSE, expected: EQUAL"
        ),

        (
            TahaSyntaxError.invalid_expression(1, 2),
            "Invalid expression.",
        ),

        (
            TahaSyntaxError.unexpected_eof(1, 2, "IDENTIFIER"),
            "Unexpected EOF, expected: IDENTIFIER",
        )

    ],

)
def test_syntax_error_factories(error, expected_message):
    assert error.message == expected_message
    assert error.line == 1
    assert error.column == 2


@pytest.mark.parametrize(
    ("error", "expected_message"),
    [
        (
            TahaRuntimeError.division_by_zero(1, 2),
              "Division by zero."
        ),

        (
            TahaRuntimeError.undefined_variable(1, 2, "BRUH"),
            "Undefined variable 'BRUH'",
        ),

        (
            TahaRuntimeError.type_error("Invalid type for using plus operator", 1, 2),
            "Invalid type for using plus operator",
        ),

        (
            TahaRuntimeError.variable_already_defined("BRUH2", 1, 2),
            "'BRUH2' is already defined.",
        )

    ],

)
def test_runtime_error_factories(error, expected_message):
    assert error.message == expected_message
    assert error.line == 1
    assert error.column == 2

