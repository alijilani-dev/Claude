# API Contracts: CLI Calculator

**Feature**: CLI Calculator
**Date**: 2026-01-04
**Status**: Complete

## Overview

Complete function signatures and contracts for the CLI calculator. All functions follow constitution principles: type safety, error handling first, single responsibility.

---

## Module: `operations.py`

**Purpose**: Core arithmetic operations (add, subtract, multiply, divide)

### Function: `add`

```python
def add(a: float, b: float) -> float:
    """Add two numbers.

    Args:
        a: First operand
        b: Second operand

    Returns:
        Sum of a and b

    Examples:
        >>> add(5.0, 3.0)
        8.0
        >>> add(-5.0, 3.0)
        -2.0
        >>> add(0.1, 0.2)
        0.30000000000000004
    """
```

**Contract**:
- **Preconditions**: None (all floats are valid)
- **Postconditions**: Returns `a + b`
- **Side effects**: None (pure function)
- **Error handling**: Cannot fail (addition always succeeds for finite floats)

---

### Function: `subtract`

```python
def subtract(a: float, b: float) -> float:
    """Subtract b from a.

    Args:
        a: First operand (minuend)
        b: Second operand (subtrahend)

    Returns:
        Difference of a and b (a - b)

    Examples:
        >>> subtract(10.0, 4.0)
        6.0
        >>> subtract(5.0, 10.0)
        -5.0
        >>> subtract(-6.0, -7.0)
        1.0
    """
```

**Contract**:
- **Preconditions**: None
- **Postconditions**: Returns `a - b`
- **Side effects**: None (pure function)
- **Error handling**: Cannot fail

---

### Function: `multiply`

```python
def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a: First operand
        b: Second operand

    Returns:
        Product of a and b

    Examples:
        >>> multiply(6.0, 7.0)
        42.0
        >>> multiply(-6.0, -7.0)
        42.0
        >>> multiply(7.5, 2.0)
        15.0
    """
```

**Contract**:
- **Preconditions**: None
- **Postconditions**: Returns `a * b`
- **Side effects**: None (pure function)
- **Error handling**: Cannot fail (may produce inf for very large results)

---

### Function: `divide`

```python
def divide(a: float, b: float) -> float | str:
    """Divide a by b.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Quotient of a / b, or error message if b is zero

    Examples:
        >>> divide(20.0, 4.0)
        5.0
        >>> divide(10.0, 3.0)
        3.3333333333333335
        >>> divide(10.0, 0.0)
        'Error: Division by zero is not allowed'
        >>> divide(-20.0, 4.0)
        -5.0
    """
```

**Contract**:
- **Preconditions**: None
- **Postconditions**:
  - If `b == 0`: Returns `"Error: Division by zero is not allowed"`
  - Otherwise: Returns `a / b`
- **Side effects**: None (pure function)
- **Error handling**: Checks for zero division **before** computation (error handling first principle)

---

## Module: `validator.py`

**Purpose**: Input validation and parsing

### Function: `parse_number`

```python
def parse_number(num_str: str) -> float | str:
    """Parse a string into a float number.

    Args:
        num_str: String representation of a number

    Returns:
        Parsed float value, or error message if invalid

    Examples:
        >>> parse_number("5")
        5.0
        >>> parse_number("-3.14")
        -3.14
        >>> parse_number("abc")
        'Error: Invalid input - please enter valid numbers'
        >>> parse_number("")
        'Error: Invalid input - please enter valid numbers'
    """
```

**Contract**:
- **Preconditions**: None (any string accepted)
- **Postconditions**:
  - If `num_str` is valid float representation: Returns parsed float
  - Otherwise: Returns error message
- **Side effects**: None (pure function)
- **Error handling**: Validates **before** conversion; catches `ValueError`

---

### Function: `validate_operator`

```python
from typing import Literal

Operator = Literal['+', '-', '*', '/']

def validate_operator(op: str) -> Operator | str:
    """Validate an operator string.

    Args:
        op: String to validate as operator

    Returns:
        Validated Operator literal, or error message if invalid

    Examples:
        >>> validate_operator("+")
        '+'
        >>> validate_operator("*")
        '*'
        >>> validate_operator("$")
        'Error: Invalid operator - use +, -, *, or /'
        >>> validate_operator("add")
        'Error: Invalid operator - use +, -, *, or /'
    """
```

**Contract**:
- **Preconditions**: None (any string accepted)
- **Postconditions**:
  - If `op` in `('+', '-', '*', '/')`: Returns `op` as Operator type
  - Otherwise: Returns error message listing valid operators
- **Side effects**: None (pure function)
- **Error handling**: Validates against whitelist

---

### Function: `parse_input`

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ParsedInput:
    operand1: float
    operator: Operator
    operand2: float

def parse_input(user_input: str) -> ParsedInput | str:
    """Parse user input into validated components.

    Args:
        user_input: Raw user input string (e.g., "5 + 3")

    Returns:
        ParsedInput with validated operands and operator, or error message

    Examples:
        >>> parse_input("5 + 3")
        ParsedInput(operand1=5.0, operator='+', operand2=3.0)
        >>> parse_input("-6 * -7")
        ParsedInput(operand1=-6.0, operator='*', operand2=-7.0)
        >>> parse_input("abc + 5")
        'Error: Invalid input - please enter valid numbers'
        >>> parse_input("5 $ 3")
        'Error: Invalid operator - use +, -, *, or /'
        >>> parse_input("5 +")
        'Error: Please provide two numbers and an operator'
    """
```

**Contract**:
- **Preconditions**: None (any string accepted)
- **Postconditions**:
  - If input format valid and components parse successfully: Returns `ParsedInput`
  - If token count ≠ 3: Returns "Error: Please provide two numbers and an operator"
  - If first number invalid: Returns error from `parse_number`
  - If operator invalid: Returns error from `validate_operator`
  - If second number invalid: Returns error from `parse_number`
- **Side effects**: None (pure function)
- **Error handling**: Validates format, then each component; returns first error encountered

**Implementation Notes**:
- Uses `str.strip().split()` for tokenization
- Checks token count before parsing
- Short-circuits on first error (fail-fast)

---

## Module: `cli.py`

**Purpose**: Interactive CLI interface and display formatting

### Function: `format_result`

```python
def format_result(value: float) -> str:
    """Format a float result for display.

    Formats to 10 decimal places, then removes trailing zeros and decimal point if integer.

    Args:
        value: Float value to format

    Returns:
        Formatted string representation

    Examples:
        >>> format_result(8.0)
        '8'
        >>> format_result(5.25)
        '5.25'
        >>> format_result(3.333333333333)
        '3.3333333333'
        >>> format_result(0.1 + 0.2)
        '0.3'
    """
```

**Contract**:
- **Preconditions**: None (any float accepted, including inf/-inf)
- **Postconditions**: Returns string with up to 10 decimal places, trailing zeros removed
- **Side effects**: None (pure function)
- **Error handling**: None needed (formatting always succeeds)

**Implementation Notes**:
- Format with `f"{value:.10f}"`
- Strip trailing zeros: `.rstrip('0')`
- Strip decimal point if no decimals: `.rstrip('.')`

---

### Function: `display_result`

```python
def display_result(result: float) -> None:
    """Display a calculation result to the user.

    Args:
        result: Float result to display

    Examples:
        >>> display_result(8.0)
        8
        >>> display_result(3.333333333333)
        3.3333333333
    """
```

**Contract**:
- **Preconditions**: None
- **Postconditions**: Prints formatted result to stdout
- **Side effects**: Writes to stdout
- **Error handling**: None needed

---

### Function: `display_error`

```python
def display_error(error: str) -> None:
    """Display an error message to the user.

    Args:
        error: Error message to display

    Examples:
        >>> display_error("Error: Division by zero is not allowed")
        Error: Division by zero is not allowed
    """
```

**Contract**:
- **Preconditions**: None
- **Postconditions**: Prints error message to stdout
- **Side effects**: Writes to stdout
- **Error handling**: None needed

---

### Function: `run_calculator`

```python
def run_calculator() -> None:
    """Run the interactive calculator REPL.

    Continuously prompts for input, parses and calculates, displays results,
    until user enters 'quit' or 'exit'.

    Returns:
        None

    Side effects:
        - Reads from stdin (input())
        - Writes to stdout (print(), display_result(), display_error())
        - Loops until exit command
    """
```

**Contract**:
- **Preconditions**: None
- **Postconditions**: Returns when user exits
- **Side effects**: I/O operations (stdin read, stdout write)
- **Error handling**: Catches all errors from parsing/calculation; displays error and continues

**Implementation Flow**:
1. Print welcome message
2. Loop:
   a. Read user input
   b. Check for exit commands ("quit", "exit", case-insensitive)
   c. Parse input
   d. If parse error: display error, continue
   e. Calculate result
   f. If calculation error: display error, continue
   g. Otherwise: display result
3. Print goodbye message

---

## Module: `__main__.py`

**Purpose**: Entry point for running calculator as module

### Code:

```python
"""CLI Calculator entry point."""
from calculator.cli import run_calculator

if __name__ == "__main__":
    run_calculator()
```

**Usage**:
```bash
python -m calculator
# or with uv:
uv run python -m calculator
```

---

## Function Call Graph

```
run_calculator()
    ├─→ input() [stdlib]
    ├─→ parse_input()
    │   ├─→ parse_number() [x2]
    │   └─→ validate_operator()
    ├─→ calculate()
    │   ├─→ add()
    │   ├─→ subtract()
    │   ├─→ multiply()
    │   └─→ divide()
    ├─→ format_result()
    ├─→ display_result()
    └─→ display_error()
```

---

## Error Message Catalog

All error messages for consistency:

| Error Condition | Message |
|----------------|---------|
| Division by zero | `"Error: Division by zero is not allowed"` |
| Invalid number | `"Error: Invalid input - please enter valid numbers"` |
| Invalid operator | `"Error: Invalid operator - use +, -, *, or /"` |
| Wrong token count | `"Error: Please provide two numbers and an operator"` |

---

## Type Safety Summary

All functions satisfy constitution Type Safety principle:

- ✅ All parameters have type hints
- ✅ All return types are explicit
- ✅ No `Any` types (mypy strict mode compatible)
- ✅ Union types used for error handling (`float | str`)
- ✅ Literal types used for operator validation
- ✅ Dataclass used for structured data (`ParsedInput`)

---

## Single Responsibility Verification

All functions satisfy constitution Single Responsibility principle:

| Function | Single Responsibility | Lines (est.) |
|----------|----------------------|--------------|
| `add` | Add two numbers | 2 |
| `subtract` | Subtract two numbers | 2 |
| `multiply` | Multiply two numbers | 2 |
| `divide` | Divide with zero check | 4 |
| `parse_number` | Parse string to float | 5 |
| `validate_operator` | Validate operator string | 4 |
| `parse_input` | Parse and validate input | 15-18 |
| `format_result` | Format float for display | 3 |
| `display_result` | Print result to stdout | 2 |
| `display_error` | Print error to stdout | 2 |
| `run_calculator` | Main REPL loop | 15-18 |

✅ All functions ≤ 20 lines

---

## Contracts Complete

All function signatures defined and ready for TDD implementation. Next step: `/sp.tasks` to generate detailed implementation tasks.
