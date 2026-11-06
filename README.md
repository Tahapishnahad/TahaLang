# TahaLang

**A small, custom programming language and interpreter built with Python.**

<p align="center">
  <strong>Version 1.0.0</strong>
  <br>
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="Version 1.0.0">
  <img src="https://img.shields.io/badge/python-3.11+-blue" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/tests-passing-brightgreen" alt="Tests Passing">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

---

## Overview

**TahaLang** is a lightweight, interpreted programming language developed from scratch using Python.

The project implements the fundamental stages of a programming language implementation, including lexical analysis, parsing, Abstract Syntax Tree (AST) construction, environment management, and interpretation.

TahaLang was designed as both a practical programming language project and an exploration of how programming languages work internally.

Rather than relying on existing interpreter frameworks, its core components were implemented independently.

## Features

### Language Features

- Variable declarations
- Integer, string, and boolean literals
- Arithmetic operations
- Comparison operators
- Unary operators
- Operator precedence
- Parenthesized expressions
- Conditional statements (`if` / `else`)
- Block statements
- Lexical scoping
- Runtime type checking
- Runtime error handling

### Interpreter Architecture

TahaLang includes its own implementation of:

- **Lexer:** Converts source code into tokens.
- **Parser:** Converts tokens into an Abstract Syntax Tree.
- **AST:** Represents the program's syntactic structure.
- **Environment:** Stores variables and manages nested scopes.
- **Interpreter:** Evaluates expressions and executes statements.
- **Error Handling:** Provides structured lexical, syntax, and runtime errors.
- **CLI:** Allows users to execute `.taha` source files from the command line.

## Project Architecture

The execution pipeline follows this structure:

```text
Source Code (.taha)
       |
       v
     Lexer
       |
       v
     Tokens
       |
       v
     Parser
       |
       v
      AST
       |
       v
  Interpreter
       |
       v
   Environment
       |
       v
     Output
```

### Project Structure

```text
TahaLang/
│
├── main.py
├── lexer.py
├── parser.py
├── interpreter.py
├── ast_nodes.py
├── tokens.py
├── errors.py
│
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_ast_nodes.py
│   ├── test_interpreter.py
│   ├── test_errors.py
│   └── test_main.py
│
└── README.md
```

*The structure above illustrates the main components; individual test filenames may vary.*

## Getting Started

### Requirements

- Python 3.11 or newer
- pip
- Git (optional, for cloning the repository)

### Installation

Clone the repository:

```bash
git clone https://github.com/Tahapishnahad/TahaLang.git
```

Navigate to the project directory:

```bash
cd TahaLang
```

Install the development dependency:

```bash
pip install pytest
```

## Running TahaLang

TahaLang source files use the `.taha` extension.

Create a file named `hello.taha`:

```taha
print("Hello, TahaLang!")
```

Run it using:

```bash
python main.py hello.taha
```

Expected output:

```text
Hello, TahaLang!
```

## Language Syntax

### Variables

Declare variables using `let`:

```taha
let age = 13
let name = "Taha"
let is_programmer = True

print(name)
print(age)
print(is_programmer)
```

### Arithmetic Operations

TahaLang supports arithmetic expressions:

```taha
let a = 10
let b = 5

print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a % b)
```

### Comparison Operators

Supported comparison operators include:

```text
==
!=
<
<=
>
>=
```

Example:

```taha
let age = 18

print(age >= 18)
print(age == 18)
```

### Unary Operators

TahaLang supports unary operators:

```taha
let number = 10

print(-number)
print(!true)
```

### Conditional Statements

Use `if` and `else` to control program execution:

```taha
let age = 18

if (age >= 18) {
    print("Adult")
} else {
    print("Minor")
}
```

### Block Scope

Blocks create their own local environments.

Variables declared inside a block belong to that block's scope.

```taha
let value = 10

if (True) {
    let local_value = 20
    print(local_value)
}

print(value)
```

## Error Handling

TahaLang provides structured errors for different stages of execution.

### Lexical Errors

Raised when the lexer encounters invalid characters or malformed literals.

### Syntax Errors

Raised when the parser encounters invalid program syntax.

### Runtime Errors

Raised when an error occurs during program execution, such as:

- Division by zero
- Undefined variables
- Invalid operand types
- Duplicate variable declarations

Errors include source location information to help identify where a problem occurred.

## Testing

TahaLang uses **pytest** for automated testing.

Run the complete test suite:

```bash
pytest -v
```

Run a specific test module:

```bash
pytest tests/test_main.py -v
```

The test suite covers the language components and CLI behavior, including successful execution and error handling.

## Version 1.0.0

**TahaLang 1.0.0** represents the first stable milestone of the project.

The initial release includes:

- A complete lexer and parser
- AST-based program representation
- Variable and environment management
- Expression evaluation
- Statement and conditional execution
- Nested block scopes
- Structured error handling
- Command-line execution
- Automated tests

## Future Development

Potential directions for future versions include:

- Additional language constructs
- Improved diagnostics and error messages
- Expanded standard functionality
- More comprehensive language tests
- Further interpreter optimizations

These are possible future improvements, not features promised by version 1.0.0.

## Author

**Taha Pishnahad**

GitHub: [@Tahapishnahad](https://github.com/Tahapishnahad)

## Acknowledgements

This project was designed and implemented by **Taha Pishnahad**.

AI assistance was used during development for technical discussions, code reviews, debugging guidance, and assistance with writing some of the automated tests.

**The README documentation was written by ChatGPT (OpenAI), and some of the project's tests were developed with ChatGPT's assistance.**

The project architecture, implementation decisions, and final development work were directed and carried out by the author.

---

<p align="center">
  <strong>TahaLang 1.0.0</strong>
  <br>
  Built from scratch with Python.
</p>
