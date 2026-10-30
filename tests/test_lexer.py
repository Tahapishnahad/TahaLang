#test_lexer.py
import pytest
from lexer import Lexer
from tokens import TokenType
from errors import LexicalError


def test_advance():
    lexer = Lexer("abc")

    assert lexer.advance() == "a"
    assert lexer.position == 1

    assert lexer.advance() == "b"
    assert lexer.position == 2


def test_advance_at_end():
    lexer = Lexer("a")
    lexer.advance()

    assert lexer.advance() is None
    assert lexer.position == 1


def test_peek():
    lexer = Lexer("abc")

    assert lexer.peek() == "a"
    assert lexer.position == 0


def test_peek_at_end():
    lexer = Lexer("")

    assert lexer.peek() is None


def test_skip_whitespace():
    lexer = Lexer("  \t13")

    lexer.skip_whitespace()

    assert lexer.position == 3
    assert lexer.peek() == "1"


def test_skip_whitespace_preserves_newline():
    lexer = Lexer(" \t\n13")

    lexer.skip_whitespace()

    assert lexer.peek() == "\n"


def test_is_digit():
    lexer = Lexer("7a")

    assert lexer.is_digit() is True

    lexer.advance()

    assert lexer.is_digit() is False


def test_is_digit_at_end():
    lexer = Lexer("")

    assert lexer.is_digit() is False


def test_read_number():
    lexer = Lexer("12345")

    assert lexer.read_number() == "12345"
    assert lexer.position == 5


def test_read_number_stops_at_non_digit():
    lexer = Lexer("7abc")

    assert lexer.read_number() == "7"
    assert lexer.peek() == "a"
    assert lexer.position == 1


def test_read_number_without_digits():
    lexer = Lexer("abc")

    assert lexer.read_number() == ""
    assert lexer.position == 0


def test_line_and_column_initial_values():
    lexer = Lexer("abc")

    assert lexer.line == 1
    assert lexer.column == 1


def test_line_and_column_after_regular_characters():
    lexer = Lexer("abc")

    lexer.advance()
    lexer.advance()

    assert lexer.line == 1
    assert lexer.column == 3


def test_line_and_column_after_newline():
    lexer = Lexer("12\n34")

    lexer.advance()
    lexer.advance()

    assert lexer.line == 1
    assert lexer.column == 3

    lexer.advance()

    assert lexer.line == 2
    assert lexer.column == 1
    assert lexer.peek() == "3"


def test_scan_number():
    lexer = Lexer("123")

    lexer.scan_number()

    token = lexer.tokens[0]

    assert token.type == TokenType.INTEGER
    assert token.value == "123"
    assert token.line == 1
    assert token.column == 1
    assert lexer.position == 3


def test_scan_tokens_with_numbers_and_newlines():
    lexer = Lexer("123\n45")
    tokens = lexer.scan_tokens()

    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == "123"

    assert tokens[1].type == TokenType.NEWLINE
    assert tokens[1].value == "\n"
    assert tokens[1].line == 1
    assert tokens[1].column == 4

    assert tokens[2].type == TokenType.INTEGER
    assert tokens[2].value == "45"
    assert tokens[2].line == 2
    assert tokens[2].column == 1

    assert tokens[-1].type == TokenType.EOF
    assert tokens[-1].value == ""
    assert tokens[-1].line == 2
    assert tokens[-1].column == 3

    lexer = Lexer("")
    tokens = lexer.scan_tokens()

    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF
    assert tokens[0].value == ""
    assert tokens[0].line == 1
    assert tokens[0].column == 1


def test_scan_operators():
    lexer = Lexer("+ -*")
    tokens = lexer.scan_tokens()

    assert tokens[0].type == TokenType.PLUS
    assert tokens[0].value == "+"

    assert tokens[1].type == TokenType.MINUS
    assert tokens[1].value == "-"

    assert tokens[2].type == TokenType.STAR
    assert tokens[2].value == "*"

    assert tokens[-1].type == TokenType.EOF


def test_all_single_character_operators():
    source = "+ - * / % ( ) { } = < > !"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()

    expected = [
        (TokenType.PLUS, "+"),
        (TokenType.MINUS, "-"),
        (TokenType.STAR, "*"),
        (TokenType.SLASH, "/"),
        (TokenType.PERCENT, "%"),
        (TokenType.LEFT_PAREN, "("),
        (TokenType.RIGHT_PAREN, ")"),
        (TokenType.LEFT_BRACE, "{"),
        (TokenType.RIGHT_BRACE, "}"),
        (TokenType.EQUAL, "="),
        (TokenType.LESS, "<"),
        (TokenType.GREATER, ">"),
        (TokenType.BANG, "!")
    ]

    actual = [(token.type, token.value) for token in tokens[:-1]]

    assert actual == expected
    assert tokens[-1].type == TokenType.EOF

def test_all_two_character_operators():
    source = "== != <= >= = < >"

    lexer = Lexer(source)
    tokens = lexer.scan_tokens()

    expected = [
        (TokenType.EQUAL_EQUAL, "=="),
        (TokenType.BANG_EQUAL, "!="),
        (TokenType.LESS_EQUAL, "<="),
        (TokenType.GREATER_EQUAL, ">="),
        (TokenType.EQUAL, "="),
        (TokenType.LESS, "<"),
        (TokenType.GREATER, ">")
    ]

    actual = [(token.type, token.value) for token in tokens[:-1]]

    assert actual == expected
    assert tokens[-1].type == TokenType.EOF

def test_scan_identifier():
    source = "let user123 = 20\nprint(user123)"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()

    expected = [
        ("let", TokenType.LET),
        ("user123", TokenType.IDENTIFIER),
        ("=", TokenType.EQUAL),
        ("20", TokenType.INTEGER),
        ("\n", TokenType.NEWLINE),
        ("print", TokenType.PRINT),
        ("(", TokenType.LEFT_PAREN),
        ("user123", TokenType.IDENTIFIER),
        (")", TokenType.RIGHT_PAREN)
    ]

    
    actual = [(token.value, token.type) for token in tokens[:-1]]

    assert actual == expected
    assert tokens[-1].type == TokenType.EOF

def test_scan_identifier_keywords():

    expected = [
            ("let", TokenType.LET),
            ("if", TokenType.IF),
            ("else", TokenType.ELSE),
            ("print", TokenType.PRINT),
            ("True", TokenType.TRUE),
            ("False", TokenType.FALSE)
    ]


    source = "let if else print True False"
    lexer = Lexer(source)
    tokens = lexer.scan_tokens()

    actual = [(token.value, token.type) for token in tokens[:-1]]

    assert actual == expected
    assert tokens[-1].type == TokenType.EOF

def test_read_float():
    lexer = Lexer("12.34")

    assert lexer.read_number() == "12.34"
    assert lexer.position == 5


def test_scan_float():
    lexer = Lexer("12.34")
    tokens = lexer.scan_tokens()

    assert tokens[0].type == TokenType.FLOAT
    assert tokens[0].value == "12.34"
    assert tokens[0].line == 1
    assert tokens[0].column == 1
    assert tokens[-1].type == TokenType.EOF


def test_scan_integer_and_float():
    lexer = Lexer("12 + 3.14")
    tokens = lexer.scan_tokens()

    actual = [(token.type, token.value) for token in tokens]

    assert actual == [
        (TokenType.INTEGER, "12"),
        (TokenType.PLUS, "+"),
        (TokenType.FLOAT, "3.14"),
        (TokenType.EOF, ""),
    ]


def test_float_without_fraction_digits():
    lexer = Lexer("4.")

    with pytest.raises(LexicalError) as exc_info:
        lexer.scan_tokens()

    error = exc_info.value
    assert error.line == 1
    assert error.column == 2


def test_float_with_multiple_decimal_points():
    lexer = Lexer("12..34")

    with pytest.raises(LexicalError) as exc_info:
        lexer.scan_tokens()

    error = exc_info.value
    assert error.line == 1
    assert error.column == 3


def test_unexpected_character():
    lexer = Lexer("@")

    with pytest.raises(LexicalError) as exc_info:
        lexer.scan_tokens()

    error = exc_info.value
    assert error.line == 1
    assert error.column == 1
    assert "@" in error.message

def test_bang_equal_is_valid():
    lexer = Lexer("!=")
    tokens = lexer.scan_tokens()

    assert tokens[0].type == TokenType.BANG_EQUAL
    assert tokens[0].value == "!="
    assert tokens[-1].type == TokenType.EOF


def test_empty_string():
    tokens = Lexer('""').scan_tokens()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == ""


def test_string_with_escape():
    tokens = Lexer(r'"Hi\nTaha"').scan_tokens()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == r"Hi\nTaha"


def test_string_with_escaped_quotes():
    tokens = Lexer(r'"Say \"Hi\""').scan_tokens()

    assert tokens[0].value == r"Say \"Hi\""


def test_unterminated_string():
    with pytest.raises(LexicalError):
        Lexer('"Hello').scan_tokens()


def test_invalid_escape():
    with pytest.raises(LexicalError):
        Lexer(r'"Hello\q"').scan_tokens()

def test_newline_string():
    with pytest.raises(LexicalError):
        Lexer('"Hello\nTaha"').scan_tokens()

#Edge Cases

@pytest.mark.parametrize(
    "source",
    [
        "3.14.5",
        "1..2",
        "12.",
        ".5",
    ],
)
def test_invalid_number_formats(source):
    with pytest.raises(LexicalError):
        Lexer(source).scan_tokens()


def test_string_with_backslash_escape():
    tokens = Lexer(r'"A\\B"').scan_tokens()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == r"A\\B"


def test_string_with_tab_escape():
    tokens = Lexer(r'"A\tB"').scan_tokens()

    assert tokens[0].value == r"A\tB"


def test_string_with_backslash_at_eof():
    with pytest.raises(LexicalError):
        Lexer('"Hello\\').scan_tokens()


def test_string_with_actual_newline():
    with pytest.raises(LexicalError):
        Lexer('"Hello\nWorld"').scan_tokens()


def test_keyword_prefix_is_identifier():
    tokens = Lexer("letter printing trueValue").scan_tokens()

    actual = [(token.type, token.value) for token in tokens[:-1]]

    assert actual == [
        (TokenType.IDENTIFIER, "letter"),
        (TokenType.IDENTIFIER, "printing"),
        (TokenType.IDENTIFIER, "trueValue"),
    ]


def test_operator_positions():
    tokens = Lexer("a == 3").scan_tokens()

    assert (tokens[0].line, tokens[0].column) == (1, 1)
    assert tokens[1].type == TokenType.EQUAL_EQUAL
    assert (tokens[1].line, tokens[1].column) == (1, 3)
    assert tokens[2].type == TokenType.INTEGER
    assert (tokens[2].line, tokens[2].column) == (1, 6)


def test_multiline_token_positions():

    tokens = Lexer("let x = 1\nprint(x)").scan_tokens()

    print_token = next(
        token for token in tokens
        if token.type == TokenType.PRINT
    )

    assert print_token.line == 2
    assert print_token.column == 1
