# TahaLang

**A small, custom programming language and interpreter built with Python.**

<p align="center">
  <strong>Version 1.1.0</strong>
  <br>
  <img src="https://img.shields.io/badge/version-1.1.0-blue" alt="Version 1.1.0">
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
- Numbers (integers and floats), string, list, and boolean literals
- Arithmetic operations
- Comparison operators
- Assignment operators
- Unary operators
- While loops
- For Loops
- Repeat Loops
- Built-ins and Builtin Registry
- Operator precedence
- Parenthesized expressions
- Conditional statements (`if` / `else`)
- Block statements
- Single-Line Comments
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
├── .gitignore
├── main.py
├── lexer.py
├── parser.py
├── interpreter.py
├── ast_nodes.py
├── tokens.py
├── errors.py
├── taha_builtins.py
├── diagnostics.py (IN DEVELOPMENT)
│
├── tests/
│   ├── __init__.py
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_ast_nodes.py
│   ├── test_tokens.py
│   ├── test_interpreter.py
│   ├── test_errors.py
│   ├── test_builtins.py
│   ├── test_main.py
│   └── test_diagnostics.py (IN DEVELOPMENT)
│
├── README.md
├── requirements.txt
└── LICENSE
```

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
pip install -r requirements.txt
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

The syntax of this language can be considered a combination of the syntax of Python, C, and JavaScript. Some syntactic elements are also unique and novel—for instance, defining comments using `@`.

### Variables

Declare variables using `let`:

```taha
let age = 18
let name = "Jack"
let is_programmer = True

print(name)
print(age)
print(is_programmer)
```

Result:

```taha
Jack
18
True
```

Variables can also store computational values, such as `2 + 2`.

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

Result:

```taha
15
5
50
2
0
```

Operator Descriptions:

- `+` -> Adds the left and right operands. It supports both numeric addition and string concatenation.

For Example:

```taha
let string = "String"

print(string + " Yes")
```

Result:

```taha
String Yes
```

- `-` -> Subtracts the right operand from the left operand.

- `*` -> Multiplies the left operand by the right operand.

- `/` -> Divides the left operand by the right operand.

- `%` -> Divides the left operand by the right operand and returns the remainder of the division.

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

Operator Descriptions:

- `==` (`EQUAL_EQUAL`): Returns `True` only if the left and right operands are equal.

- `!=` (`BANG_EQUAL`): Returns `True` only if the left and right operands are not equal.

- `<` (`LESS`): Returns `True` only if the left operand is less than the right operand.

- `<=` (`LESS_EQUAL`): Returns `True` only if the left operand is less than or equal to the right operand.

- `>` (`GREATER`): Returns `True` only if the left operand is greater than the right operand.

- `>=` (`GREATER_EQUAL`): Returns `True` only if the left operand is greater than or equal to the right operand.

- In case the inputs are strings, the language uses Lexicographical Comparison to compare them.


Example:

```taha
let age = 18
let animal = "cat"

print(age >= 18)
print(age == 18)
print(animal > "dog")
```

Result:
```taha
True
True
False
```

### Assignment Operators (NEW in 1.1.0)

Supported assignment operators include:

```text
=
+=
-=
*=
/=
%=
```

Operator Descriptions:

- `=`: Assigns the right-hand value to the variable on the left.

- `+=`: Adds the right operand to the variable's current value and assigns the result to that variable.

- `-=`: Subtracts the right operand from the variable's current value and assigns the result to that variable.

- `*=`: Multiplies the variable's current value by the right operand and assigns the result to that variable.

- `/=`: Divides the variable's current value by the right operand and assigns the result to that variable.

- `%=`: Calculates the remainder when the variable's current value is divided by the right operand and assigns the result to that variable.

Example:

```taha
let age = 18
let name = "Sarah"

age += 10
name += " Jane"
age *= 2

print(age)
print(name)

```

Result:
```taha
56
Sarah Jane
```

Note: TahaLang can assign float and int to each other, because both are NumberLiteral.

### Unary Operators

Supported unary operators include:

```text
-
!
```

Operator Descriptions:

- `-`: Returns the negated value of a number.

- `!`: Calculates and returns the inverse of Boolean values.

Example:
```taha
print(-20)
print(!True)
```

Result:
```
-20
False
```

### Conditional Statements

Use `if` and `else` to control program execution:

Example:

```taha
let age = 18

if (age >= 18) {
    print("Adult")
} else {
    print("Minor")
}
```

Result:

```
Adult
```

- `else` must come after the closing curly brace of the `if`.
- Parentheses are mandatory for writing conditions.

### Block Scope

Blocks create their own local environments.

A block can access variables declared in its parent scopes, but variables declared inside the block are not accessible outside it.

Example:

```taha
let value = 10

if (True) {
    let local_value = 20
    print(local_value)
}

print(value)
```

Result:

```
20
10
```

### Lists and Indexing (NEW in 1.1.0)

TahaLang supports lists.

Defining a list:
```taha
let list = [1, 2, 3]
```

Getting list / string element:
```taha
list[0]
list[1]
"StringString"[4]
```

Result:
```
1
2
n
```

A list can contain different types.
TahaLang has zero-based indexes.

### Builtins (NEW in 1.1.0)

TahaLang has built-in functions:

Available Built-in Functions:

```text
print(value)
len(value)
block_print(value)
```

- `print` -> Prints the value to the terminal.
- `len` ->  Returns the length of a list or a string.
- `block_print` -> Prints the value as an ascii art with block font to the terminal. It just supports string type for the value.

```taha
print("Something")
print(len([1, 2, 3]))
```

Result:

```taha
Something
3
```

`block_print` Example:
```taha
block_print("Hi!")
```

Result:
```taha

_|    _|  _|  _|  
_|    _|      _|  
_|_|_|_|  _|  _|  
_|    _|  _|      
_|    _|  _|  _| 

```

### While loop (NEW in 1.1.0)

The while loop repeatedly executes a block of statements as long as its condition evaluates to True.

- The condition must evaluate to a Boolean value.
- The condition is re-evaluated in each iteration.
- If the condition is `False` from the start, the body is not executed.
- The loop continues as long as the condition is `True`.
- If the condition never becomes `False`, the loop becomes infinite.
- While body can access variables declared in its parent scopes, but variables declared inside the block are not accessible outside it.

```taha
while (condition) {
  statement
}
```

Example:
```taha
let counter = 0

while (counter < 5) {
  print(counter)
  counter += 1
}

```

Result:
```
0
1
2
3
4
```

### For Loop (NEW in 1.1.0)

The `for` loop declares a variable and repeatedly executes a block of statements as long as its condition evaluates to `True`.

The loop consists of three parts:

- **Init:** Declares and initializes the loop variable. It executes only once, before the loop starts.
- **Condition:** Must evaluate to a Boolean value. The loop continues while the condition is `True`.
- **Update:** Executes once after the entire loop body has finished. It must be an assignment or compound assignment statement.

#### Features

- The condition must evaluate to a Boolean value.
- If the condition is `False` initially, the loop body is never executed.
- The loop continues until the condition becomes `False`.
- If the condition never becomes `False`, the loop runs indefinitely.
- The loop variable is scoped to the loop and cannot be accessed outside it.
- The loop body has its own scope.

#### Syntax

```taha
for (init; condition; update) {
    statements
}
```

#### Execution Order

1. Execute Init once.
2. Evaluate Condition.
3. If Condition is `False`, exit the loop.
4. Execute the body statements.
5. Execute Update.
6. Return to step 2.

#### Example

```taha
for (let i = 1; i <= 10; i += 1) {
    print(i)
}
```

**Output:**

```text
1
2
3
4
5
6
7
8
9
10
```

## Repeat Loop (NEW in 1.1.0)

The `repeat` loop executes a block of statements a specified number of times.

### Syntax

```taha
repeat (times) {
    statements
}
```

The `times` expression determines how many times the loop body is executed.

### Examples

**1. Numeric value**

```taha
repeat (3) {
    print("Hello")
}
```

Output:

```text
Hello
Hello
Hello
```

**2. Arithmetic expression**

```taha
repeat (2 + 3) {
    print("TahaLang")
}
```

The expression is evaluated once before the loop starts.

**3. Variable**

```taha
let count = 4

repeat (count) {
    print("Running")
}
```

### Behavior

- The `times` expression is evaluated only once before execution.
- The expression must evaluate to an integer.
- Positive integers determine the number of iterations.
- A value of `0` skips the loop body entirely.
- Negative values cause a runtime error.
- Non-integer values cause a runtime error.
- The loop body is executed once per iteration.

### Runtime Errors

The `repeat` loop raises a runtime error when:

- The `times` expression evaluates to a non-integer value.
- The `times` expression evaluates to a negative integer.

For example:

```taha
repeat (-2) {
    print("Hello")
}
```

This produces a runtime error because negative iteration counts are not allowed.

```taha
repeat (2.5) {
    print("Hello")
}
```

This also produces a runtime error because the iteration count must be an integer.

### Zero Iterations

A zero iteration count is valid:

```taha
repeat (0) {
    print("This will not be printed")
}
```

The loop body is skipped completely.


### Single Line Comments (NEW in 1.1.0)

TahaLang supports single-line comments.
Comments are ignored by the interpreter.
`@` is used to start a comment.

```taha
let a = 10 @ Defining a variable
@ Comment
print(a) @ Printing
```

## Error Handling

TahaLang provides a structured error-handling system to identify and report errors during different stages of program execution.

All language errors inherit from the base `TahaLangError` class.

### Error Types

TahaLang defines three main categories of errors:

#### 1. Lexical Errors

`LexicalError` is raised when the lexer encounters invalid characters, malformed escape sequences, or invalid string literals.

Examples include:

- Unexpected characters
- Malformed numeric literals, such as `12.` and `.33`
- Unexpected escape sequences
- Newlines inside string literals
- Unterminated strings

#### 2. Syntax Errors

`TahaSyntaxError` is raised when the parser encounters invalid syntax or unexpected tokens while parsing a program.

Examples include:

- Unexpected token types
- Unexpected end of file (EOF)
- Invalid expressions
- Unexpected commas in lists or function arguments
- Missing expressions after commas
- Invalid expressions used for indexing

#### 3. Runtime Errors

`TahaRuntimeError` is raised when an error occurs during program execution.

Examples include:

- Division by zero
- Undefined variables
- Assignments to undefined variables
- Invalid assignment types
- Duplicate variable declarations
- Invalid operand types
- Invalid objects or indexes in index expressions
- Invalid function calls or argument counts
- Invalid built-in function arguments
- Invalid `while` loop condition types
- Invalid `for` loop condition types
- Invalid `for` loop update types
- The `times` expression evaluates to a non-integer value.
- The `times` expression evaluates to a negative integer.

### Error Information

Every TahaLang error contains the following information:

- **Error Type:** The name of the error class.
- **Line:** The line number where the error occurred.
- **Column:** The column number where the error occurred.
- **Message:** A description of the error.

Errors are formatted using the following structure:

```text
ErrorType at line LINE, column COLUMN: MESSAGE
```

### Example

Consider the following TahaLang code:

```taha
let result = 10 / 0
```

This code raises a runtime error because division by zero is not allowed.

Example error output:

```text
TahaRuntimeError at line 1, column 19: Division by zero.
```

TahaLang provides structured errors for different stages of execution.

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
- Assignment to variables
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
- Adding User-defined Functions

## Author

**Taha Pishnahad**

GitHub: [@Tahapishnahad](https://github.com/Tahapishnahad)

## Acknowledgements

This project was designed and implemented by **Taha Pishnahad**.

AI assistance was used during development for technical discussions, code reviews, debugging guidance, and assistance with writing some of the automated tests.

The project architecture, implementation decisions, and final development work were directed and carried out by the author.

---

<p align="center">
  <strong>TahaLang 1.1.0</strong>
  <br>
  Built from scratch with Python. No frameworks.
</p>
