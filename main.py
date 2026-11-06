# main.py

import argparse
import sys
from pathlib import Path

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Environment
from errors import TahaLangError

def main():
    arg_parser = argparse.ArgumentParser(
        description="TahaLang Interpreter"
    )

    arg_parser.add_argument(
        "file",
        help="Path to the TahaLang source file"
    )

    args = arg_parser.parse_args()
    file_path = Path(args.file)

    if validate_file_suffix(file_path):
        try:
            source = file_path.read_text(encoding="utf-8")

        except UnicodeDecodeError:
            print("File is not valid UTF-8.", file=sys.stderr)
            sys.exit(1)

        except OSError as e:
            print(f"File error: {e}", file=sys.stderr)
            sys.exit(1)

        else:
            try:
                run_source(source)
            except TahaLangError as e:
                print(e, file=sys.stderr)
                sys.exit(1)
    else:
        print("Invalid file name. file suffix should be '.taha' for Tahalang sources.", file=sys.stderr)
        sys.exit(1)


def validate_file_suffix(file_path: Path) -> bool:
    return file_path.suffix == ".taha"

def run_source(source: str):
    lexer = Lexer(source=source)
    syntax_parser = Parser(lexer.scan_tokens())
    env = Environment()
    interpreter = Interpreter(env)
    interpreter.execute_program(syntax_parser.parse(), env)

if __name__ == "__main__":
    main()