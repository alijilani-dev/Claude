# Data Model: CLI Calculator

**Feature**: CLI Calculator
**Date**: 2026-01-04
**Status**: Complete

## Overview

Data structures and types for the CLI calculator. The calculator is stateless (no persistence), so the data model focuses on runtime types for input parsing, validation, and computation.

## Core Types

### Operator Type

**Purpose**: Type-safe representation of valid arithmetic operators

```python
from typing import Literal

Operator = Literal['+', '-', '*', '/']
```

**Rationale**:
- Restricts operator values to exactly four valid choices
- Enables exhaustive pattern matching in type checker
- Self-documenting: function signature shows valid operators

**Usage**:
```python
def validate_operator(op: str) -> Operator | str:
    if op in ('+', '-', '*', '/'):
        return op  # type: Operator
    return f"Error: Invalid operator - use +, -, *, or /"
```

---

### Calculation Result Type

**Purpose**: Represents the result of a calculation or an error message

```python
CalculationResult = float | str
```

**Rationale**:
- Union type allows functions to return either a success value (float) or error message (str)
- Type-safe alternative to exceptions for error handling
- Caller must check type before using result

**Usage**:
```python
def divide(a: float, b: float) -> CalculationResult:
    if b == 0:
        return "Error: Division by zero is not allowed"
    return a / b

# Caller pattern:
result = divide(10, 2)
if isinstance(result, str):
    print(result)  # Error message
else:
    print(f"Result: {result}")  # float value
```

---

### Parsed Input Structure

**Purpose**: Structured representation of validated user input

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ParsedInput:
    """Represents a validated and parsed calculation input.

    Attributes:
        operand1: First numeric operand
        operator: Arithmetic operator (+, -, *, /)
        operand2: Second numeric operand
    """
    operand1: float
    operator: Operator
    operand2: float
```

**Rationale**:
- Immutable (`frozen=True`) prevents accidental modification
- Type-safe: all fields have strict types
- Self-documenting: clear field names and docstring
- Separates parsing from computation

**Usage**:
```python
def parse_input(user_input: str) -> ParsedInput | str:
    tokens = user_input.strip().split()
    if len(tokens) != 3:
        return "Error: Please provide two numbers and an operator"

    num1_str, op_str, num2_str = tokens

    # Parse first operand
    num1 = parse_number(num1_str)
    if isinstance(num1, str):
        return num1  # Error message

    # Validate operator
    operator = validate_operator(op_str)
    if isinstance(operator, str):
        return operator  # Error message

    # Parse second operand
    num2 = parse_number(num2_str)
    if isinstance(num2, str):
        return num2  # Error message

    return ParsedInput(operand1=num1, operator=operator, operand2=num2)
```

---

## Type Aliases (Optional Clarity)

For improved readability in function signatures:

```python
from typing import TypeAlias

# Error message type
ErrorMessage: TypeAlias = str

# Parsing result
ParseResult: TypeAlias = ParsedInput | ErrorMessage

# Number parsing result
NumberParseResult: TypeAlias = float | ErrorMessage

# Operator validation result
OperatorValidationResult: TypeAlias = Operator | ErrorMessage

# Calculation result
CalculationResult: TypeAlias = float | ErrorMessage
```

**Usage**:
```python
def parse_number(num_str: str) -> NumberParseResult:
    ...

def validate_operator(op: str) -> OperatorValidationResult:
    ...

def parse_input(user_input: str) -> ParseResult:
    ...

def calculate(parsed: ParsedInput) -> CalculationResult:
    ...
```

---

## Data Flow

### Input to Result Flow

```
User Input (str)
    ↓
[parse_input]
    ↓
ParsedInput | ErrorMessage
    ↓ (if ParsedInput)
[calculate]
    ↓
CalculationResult (float | ErrorMessage)
    ↓
[format_result or display_error]
    ↓
Display to User (str)
```

### Parsing Flow Detail

```
"5 + 3"
    ↓ split()
["5", "+", "3"]
    ↓ validate count
len == 3 ✓
    ↓ parse_number("5")
5.0 ✓
    ↓ validate_operator("+")
'+' (Operator) ✓
    ↓ parse_number("3")
3.0 ✓
    ↓ construct
ParsedInput(operand1=5.0, operator='+', operand2=3.0)
```

### Error Flow Detail

```
"abc + 5"
    ↓ split()
["abc", "+", "5"]
    ↓ validate count
len == 3 ✓
    ↓ parse_number("abc")
"Error: Invalid input - please enter valid numbers" ✗
    ↓ early return
Return error message
```

---

## State Management

### No Persistent State

The calculator is **stateless**:
- No calculation history
- No memory functions (M+, M-, MR, MC)
- No user preferences or configuration
- Each calculation is independent

**Rationale**:
- Simplicity principle: no state means no bugs from state management
- Spec explicitly excludes history and memory functions
- Easier to test: pure functions with no side effects

### Session State (CLI Loop Only)

The only "state" is the running REPL loop:

```python
def run_calculator() -> None:
    """Main REPL loop - only state is loop continuation."""
    print("Calculator ready. Type 'quit' or 'exit' to exit.")

    while True:
        user_input = input("> ").strip()

        # Check exit commands
        if user_input.lower() in ('quit', 'exit'):
            print("Goodbye!")
            break

        # Parse and calculate (stateless)
        parsed = parse_input(user_input)
        if isinstance(parsed, str):
            display_error(parsed)
            continue

        result = calculate(parsed)
        if isinstance(result, str):
            display_error(result)
        else:
            display_result(result)
```

**Loop State**:
- `while True`: Loop runs until exit command
- No variables carry over between iterations
- Each calculation starts fresh

---

## Type Safety Guarantees

### Mypy Strict Mode Compliance

All types support strict mypy checking:

```python
# No implicit Any types
def add(a: float, b: float) -> float:  # Explicit return type
    return a + b

# No untyped parameters
def parse_input(user_input: str) -> ParsedInput | str:  # All params typed
    ...

# Exhaustive pattern matching (Python 3.10+)
def calculate(parsed: ParsedInput) -> CalculationResult:
    match parsed.operator:
        case '+':
            return add(parsed.operand1, parsed.operand2)
        case '-':
            return subtract(parsed.operand1, parsed.operand2)
        case '*':
            return multiply(parsed.operand1, parsed.operand2)
        case '/':
            return divide(parsed.operand1, parsed.operand2)
    # Mypy knows all cases covered (exhaustive Literal matching)
```

### Runtime Type Checking

Error handling validates types at runtime:

```python
# Check for error messages
result = divide(10, 0)
if isinstance(result, str):  # Runtime type check
    print(result)  # mypy knows this is str
else:
    print(f"{result:.2f}")  # mypy knows this is float
```

---

## Edge Case Handling in Data Model

### Division by Zero

Handled in `divide()` function, returns error message:
```python
def divide(a: float, b: float) -> CalculationResult:
    if b == 0:
        return "Error: Division by zero is not allowed"
    return a / b
```

### Invalid Numbers

Handled in `parse_number()` function:
```python
def parse_number(num_str: str) -> NumberParseResult:
    try:
        return float(num_str)
    except ValueError:
        return "Error: Invalid input - please enter valid numbers"
```

### Invalid Operators

Handled in `validate_operator()` function:
```python
def validate_operator(op: str) -> OperatorValidationResult:
    if op in ('+', '-', '*', '/'):
        return op  # type: Operator
    return f"Error: Invalid operator - use +, -, *, or /"
```

### Overflow/Underflow

Python floats naturally handle overflow/underflow:
- Overflow: Returns `inf` or `-inf`
- Underflow: Returns `0.0` for very small numbers
- Can add explicit checks if needed:

```python
import sys

def check_overflow(value: float) -> float | str:
    if abs(value) > sys.float_info.max:
        return "Error: Result too large to represent"
    if value != 0 and abs(value) < sys.float_info.min:
        return "Error: Result too small to represent"
    return value
```

---

## Summary

### Core Data Structures

1. **Operator**: `Literal['+', '-', '*', '/']` - Type-safe operator constraint
2. **ParsedInput**: `dataclass(operand1: float, operator: Operator, operand2: float)` - Validated input structure
3. **CalculationResult**: `float | str` - Success or error pattern
4. **No persistent state** - Stateless calculator, pure functions

### Design Principles Applied

- ✅ **Type Safety**: All functions fully typed, mypy strict mode compatible
- ✅ **Immutability**: ParsedInput is frozen, no mutable state
- ✅ **Error Handling**: Union types for explicit error handling
- ✅ **Simplicity**: Minimal data structures, no over-engineering
- ✅ **Single Responsibility**: Each type has one clear purpose

**Data model complete and ready for implementation.**
