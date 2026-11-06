# test_main.py

import pytest

from main import main

def test_main_success(tmp_path, monkeypatch, capsys):
    path = tmp_path / "hello.taha"

    path.write_text('print("Hello Tahalang!")')

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", str(path)]
    )

    main()

    captured = capsys.readouterr()

    assert captured.out == "Hello Tahalang!\n"
    assert captured.err == ""

def test_main_invalid_suffix(tmp_path, monkeypatch, capsys):
    path = tmp_path / "taha.py"

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", str(path)]
    )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1

    captured = capsys.readouterr()

    assert captured.out == ""
    assert captured.err == "Invalid file name. file suffix should be '.taha' for Tahalang sources.\n"

def test_main_file_not_found(monkeypatch, capsys):
    monkeypatch.setattr(
            "sys.argv",
            ["main.py", "unknown.taha"]
        )
    
    with pytest.raises(SystemExit) as exc_info:
            main()

    assert exc_info.value.code == 1
    
    captured = capsys.readouterr()
    
    assert captured.out == ""
    assert "File error:" in captured.err
    assert "unknown.taha" in captured.err

def test_main_invalid_encoding(tmp_path, monkeypatch, capsys):
    path = tmp_path / "invalid.taha"

    path.write_bytes(b'\xc3')

    monkeypatch.setattr(
            "sys.argv",
            ["main.py", str(path)]
        )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    
    assert captured.out == ""
    assert captured.err == "File is not valid UTF-8.\n"

def test_main_lexer_error(tmp_path, monkeypatch, capsys):
    path = tmp_path / "invalid_lexing.taha"

    path.write_text("print(@)")

    monkeypatch.setattr(
            "sys.argv",
            ["main.py", str(path)]
        )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    
    assert captured.out == ""
    assert "LexicalError" in captured.err
    assert "'@'" in captured.err

def test_main_parser_error(tmp_path, monkeypatch, capsys):
    path = tmp_path / "invalid_parsing.taha"

    path.write_text("let a =")

    monkeypatch.setattr(
            "sys.argv",
            ["main.py", str(path)]
        )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    
    assert captured.out == ""
    assert "TahaSyntaxError" in captured.err
    assert "Invalid expression." in captured.err

def test_main_interpreter_error(tmp_path, monkeypatch, capsys):
    path = tmp_path / "invalid_interpreting.taha"

    path.write_text("print(8 / 0)")

    monkeypatch.setattr(
            "sys.argv",
            ["main.py", str(path)]
        )

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    
    assert captured.out == ""
    assert "TahaRuntimeError" in captured.err
    assert "Division by zero." in captured.err
