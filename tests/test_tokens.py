from tokens import TokenType, Token


def test_tokens():
    token = Token(TokenType.INTEGER ,"12" ,2 , 3)

    assert token.type == TokenType.INTEGER
    assert token.value == "12"
    assert token.line == 2
    assert token.column == 3

    token = Token(TokenType.STAR, "*", 8, 13)

    assert token.type == TokenType.STAR
    assert token.value == "*"
    assert token.line == 8
    assert token.column == 13

def test_tokens_equality():
    token_1 = Token(TokenType.IDENTIFIER, "name", 9, 3)
    token_2 = Token(TokenType.IDENTIFIER, "name", 113, 15)

    assert token_1 != token_2
    assert token_1.value == token_2.value

    token_1 = Token(TokenType.INTEGER, "1", 1, 3)
    token_2 = Token(TokenType.INTEGER, "1", 1, 3)

    assert token_1 == token_2
