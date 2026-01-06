# Research: CLI Calculator

**Feature**: CLI Calculator
**Date**: 2026-01-04
**Status**: Complete

## Overview

Research phase for designing a basic CLI calculator in Python with robust error handling. All technical decisions are straightforward given the simple scope and stdlib-only approach.

## Research Questions & Findings

### Q1: Numeric Type Selection

**Question**: Should we use `float`, `Decimal`, or `int` for calculations?

**Research Findings**:
- **`float`**: Python's built-in floating-point type provides 15-17 significant figures of precision (IEEE 754 double precision)
- **`Decimal`**: Arbitrary precision decimal arithmetic, designed for financial applications
- **`int`**: Exact integer arithmetic, no decimal support

**Decision**: Use `float`

**Rationale**:
- Spec requires minimum 6 decimal places; float provides 15-17 significant figures (exceeds requirement)
- Stdlib only (no external dependencies); Decimal is stdlib but adds unnecessary complexity
- Binary representation quirks (0.1 + 0.2 = 0.30000000000000004) are acceptable and will be hidden via formatting
- Follows Simplicity principle: don't add complexity without clear benefit

**Alternatives Considered**:
- `Decimal` - Rejected: Overkill for basic calculator; adds complexity; requires import and explicit construction
- `int` with custom decimal tracking - Rejected: Reinventing the wheel; violates Simplicity

**Trade-offs Accepted**:
- Float precision limits (~1e-15 relative error) - Acceptable for basic calculator
- Binary representation artifacts - Mitigated by output formatting (10 decimal places, strip trailing zeros)

---

### Q2: Input Parsing Strategy

**Question**: How should we parse user input `"5 + 3"` into components?

**Research Findings**:
- **`str.split()`**: Simple whitespace tokenization
- **Regular expressions**: More powerful pattern matching
- **Parsing libraries (pyparsing, lark)**: Full parser generators

**Decision**: Use `str.split()`

**Rationale**:
- Input format is simple: `<num> <op> <num>` with whitespace separation
- `split()` handles multiple spaces, leading/trailing whitespace automatically
- No need for complex parsing (no parentheses, order of operations, multi-operator expressions)
- Stdlib only; follows Simplicity principle

**Implementation**:
```python
tokens = user_input.strip().split()
if len(tokens) != 3:
    return "Error: Please provide two numbers and an operator"
num1_str, operator, num2_str = tokens
```

**Alternatives Considered**:
- Regex `r'(-?\d+\.?\d*)\s*([+\-*/])\s*(-?\d+\.?\d*)'` - Rejected: Overkill; harder to maintain; doesn't add value for simple format
- Parsing library - Rejected: External dependency; massive overkill; violates Simplicity

---

### Q3: Error Handling Pattern

**Question**: Should errors raise exceptions or return error values?

**Research Findings**:
- **Exceptions**: Python's standard error mechanism; interrupts control flow
- **Return values**: Explicit error handling; keeps control flow linear
- **Result/Option types**: Functional pattern; requires custom types or library

**Decision**: Return error messages as strings; use union types `float | str`

**Rationale**:
- Interactive REPL must continue running after errors
- Exceptions would require try/except at top level or crash the calculator
- Union types (`float | str`) provide type safety without complexity
- Clear error messages without stack traces improves user experience

**Implementation Pattern**:
```python
def divide(a: float, b: float) -> float | str:
    if b == 0:
        return "Error: Division by zero is not allowed"
    return a / b

# Caller checks type:
result = divide(10, 0)
if isinstance(result, str):
    print(result)  # Error message
else:
    print(f"Result: {result}")
```

**Alternatives Considered**:
- Exceptions - Rejected: Requires try/except boilerplate; can crash REPL if unhandled
- Result[T, E] type - Rejected: Requires external library or custom implementation; adds complexity

---

### Q4: Decimal Precision Display

**Question**: How should we format decimal results for display?

**Research Findings**:
- Spec requires: "up to 10 decimal places with trailing zeros removed"
- Examples: `10/3 = 3.3333333333`, `7.5 * 2.0 = 15` (not `15.0`)

**Decision**: Format with `:.10f` then strip trailing zeros and decimal point if integer

**Rationale**:
- Balances precision (10 decimals) with readability (no trailing zeros)
- Handles repeating decimals gracefully
- Makes whole number results look clean

**Implementation**:
```python
def format_result(value: float) -> str:
    formatted = f"{value:.10f}"
    # Strip trailing zeros and decimal point if integer
    formatted = formatted.rstrip('0').rstrip('.')
    return formatted
```

**Test Cases**:
- `format_result(3.333333333333)` → `"3.3333333333"`
- `format_result(15.0)` → `"15"`
- `format_result(0.1 + 0.2)` → `"0.3"` (after rounding)

**Alternatives Considered**:
- Fixed decimal places (always show `.00`) - Rejected: Spec requires trailing zeros removed
- String manipulation during calculation - Rejected: Violates separation of concerns

---

### Q5: Negative Number Parsing

**Question**: How should we handle negative numbers in input like `"-5 + 3"`?

**Research Findings**:
- Python's `float()` constructor handles negative signs: `float("-5")` → `-5.0`
- `str.split()` preserves minus sign with number: `"-5 + 3".split()` → `["-5", "+", "3"]`

**Decision**: Use `float()` directly on token strings; minus sign is part of the number

**Rationale**:
- Python's built-in parsing handles negative numbers correctly
- No special logic needed for negative operands
- Distinction between unary minus (negative number) and binary minus (subtraction) is clear from context

**Implementation**:
```python
def parse_number(num_str: str) -> float | str:
    try:
        return float(num_str)
    except ValueError:
        return "Error: Invalid input - please enter valid numbers"
```

**Edge Cases Handled**:
- `"-5 + 3"` → operand1=-5, operator=+, operand2=3
- `"-6 * -7"` → operand1=-6, operator=*, operand2=-7
- `"- 5 + 3"` → Invalid (space between minus and number)

---

## Technology Stack (Final)

| Component | Choice | Source |
|-----------|--------|--------|
| Language | Python 3.11+ | Constitution + modern type hints |
| Package Manager | uv | Constitution requirement |
| Numeric Type | `float` (stdlib) | Q1 research |
| Input Parsing | `str.split()` (stdlib) | Q2 research |
| Error Handling | Union types `float \| str` | Q3 research |
| Formatting | `f"{x:.10f}".rstrip('0').rstrip('.')` | Q4 research |
| Negative Numbers | `float()` constructor | Q5 research |
| Test Framework | pytest | Constitution requirement |
| Coverage | pytest-cov | Constitution requirement |
| Type Checker | mypy (strict) | Constitution requirement |
| Linter/Formatter | ruff | Constitution requirement |

**Runtime Dependencies**: None (stdlib only)
**Development Dependencies**: pytest, pytest-cov, mypy, ruff

---

## Best Practices Applied

### Python 3.11+ Features
- **Union types with `|`**: `float | str` instead of `Union[float, str]`
- **Type hints**: All function signatures fully typed
- **Match statements**: Can be used for operator selection (optional optimization)

### Error Handling Patterns
- **Defensive validation**: Check inputs before computation
- **Clear error messages**: Include what went wrong and how to fix it
- **No silent failures**: Every error condition returns explicit message

### Testing Strategy
- **Unit tests**: Each function (add, subtract, multiply, divide, parse_number, parse_input)
- **Edge case tests**: Division by zero, overflow, underflow, 0.1+0.2, negative combinations
- **Integration tests**: Full REPL workflows for each user story

### Code Organization
- **Separation of concerns**: operations.py, validator.py, cli.py
- **Single Responsibility**: Each function does one thing (≤20 lines)
- **Type safety**: Literal types for operators, strict mypy mode

---

## Open Questions / Assumptions

**Assumption 1**: Input format is always `<num> <op> <num>` (space-separated)
- **Justification**: Spec example shows this format; simplest to parse
- **Impact**: Users must use spaces; error message will guide them

**Assumption 2**: Exit commands are "quit" or "exit" (case-insensitive)
- **Justification**: Common convention for CLI tools
- **Impact**: Users need to know exit command; will be shown in prompt

**Assumption 3**: Overflow/underflow display as "inf"/"-inf" or raise error
- **Justification**: Python float naturally produces inf for overflow; explicit error message preferred
- **Impact**: Very large numbers (>1e308) will trigger error or show "inf"

**Assumption 4**: Scientific notation input (1e10) is not supported initially
- **Justification**: Spec doesn't mention it; `float()` would parse it anyway
- **Impact**: If users try "1e10 + 5" it will work; if issues arise, can be restricted

---

## Research Complete

All technical decisions made. Ready to proceed to Phase 1 (Design & Contracts).

**No blocking questions remain.** All NEEDS CLARIFICATION items from plan.md are resolved.
