import pytest

from diagnostics import SourceFile

def source_file(content: str, name: str="test.taha") -> SourceFile:
    return SourceFile(name=name, content=content)

def test_source_file():
    source = source_file(
        content="let a = 9\nlet b = 6",
        name="code.taha"
    )

    assert source.name == "code.taha"
    assert source.content == "let a = 9\nlet b = 6"

def test_source_file_is_frozen():
    source = source_file(
        content="something",
        name="code.taha"
    )

    with pytest.raises(AttributeError):
        source.name = "somthing_else.taha"

    with pytest.raises(AttributeError):
        source.content = "somthing_else"

    assert source.name == "code.taha"
    assert source.content == "something"

def test_get_line():
    source = source_file(
        content="let a = 9\nprint(a)"
    )

    assert source.get_line(1) == "let a = 9"
    assert source.get_line(2) == "print(a)"

def test_get_line_with_zero_value():
    source = source_file(
        content="let a = 9\nprint(a)"
    )

    assert source.get_line(0) is None

def test_get_line_with_negative_value():
    source = source_file(
        content="let a = 9\nprint(a)"
    )

    assert source.get_line(-1) is None

def test_get_line_with_out_of_range_value():
    source = source_file(
        content="let a = 9\nprint(a)"
    )

    assert source.get_line(3) is None

def test_get_line_with_empty_file_content():
    source = source_file(
        content=""
    )

    assert source.get_line(2) is None
    assert source.get_line(200) is None

def test_get_line_with_single_line_file_content():
    source = source_file(
        content='print("Hello, TahaLang!")'
    )

    assert source.get_line(1) == 'print("Hello, TahaLang!")'
    assert source.get_line(2) is None