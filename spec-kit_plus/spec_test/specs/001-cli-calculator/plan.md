# Implementation Plan: CLI Calculator

**Branch**: `001-cli-calculator` | **Date**: 2026-01-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-calculator/spec.md`

## Summary

Build a command-line calculator supporting four basic arithmetic operations (addition, subtraction, multiplication, division) with robust error handling for decimal numbers, negative numbers, division by zero, and invalid input. The calculator runs in interactive mode, prompting users for calculations until they exit.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: No external runtime dependencies (stdlib only); pytest, pytest-cov, mypy, ruff for development
**Storage**: N/A (stateless calculator, no persistence)
**Testing**: pytest with pytest-cov for coverage reporting (≥95% target)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single project (simple CLI application)
**Performance Goals**: Calculation response < 5 seconds (interactive input to result display)
**Constraints**:
  - Must handle Python float precision limits gracefully
  - Must display up to 10 decimal places with trailing zeros removed
  - Functions must not exceed 20 lines (Single Responsibility principle)
**Scale/Scope**: Single-user interactive CLI, ~200-300 lines of implementation code

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle Compliance

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Type Safety** | ✅ PASS | All functions will use type hints; mypy strict mode in quality gates |
| **II. Error Handling First** | ✅ PASS | Spec explicitly requires division by zero, invalid input, overflow handling |
| **III. Test-Driven Development** | ✅ PASS | TDD workflow mandatory; tests written before implementation |
| **IV. Edge Case Completeness** | ✅ PASS | Spec covers all required edge cases: decimals, division by zero, negatives, invalid input, overflow/underflow |
| **V. Single Responsibility & Simplicity** | ✅ PASS | Four separate operation functions; separate validation, parsing, computation; no unnecessary complexity |
| **VI. UV Package Management** | ✅ PASS | Project will use uv for all dependency management |

### Quality Gates Verification

- ✅ Unit tests with ≥95% coverage (pytest + pytest-cov)
- ✅ Type checking with mypy strict mode
- ✅ Linting with ruff check
- ✅ Edge case tests for all Principle IV scenarios
- ✅ Functions < 20 lines each

**Gate Status**: ✅ **APPROVED** - All constitution principles satisfied by design

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-calculator/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (research findings)
├── data-model.md        # Phase 1 output (data structures)
├── quickstart.md        # Phase 1 output (user guide)
├── contracts/           # Phase 1 output (function contracts)
│   └── calculator_api.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── calculator/
│   ├── __init__.py
│   ├── operations.py    # add, subtract, multiply, divide functions
│   ├── validator.py     # input validation and parsing
│   └── cli.py          # interactive CLI loop and display
└── __main__.py         # Entry point: python -m src.calculator

tests/
├── unit/
│   ├── test_operations.py     # Unit tests for each operation
│   ├── test_validator.py      # Input validation tests
│   └── test_edge_cases.py     # Edge case scenarios
└── integration/
    └── test_cli_workflows.py  # End-to-end user story tests

pyproject.toml          # UV project configuration
uv.lock                 # Locked dependencies
README.md               # Installation and usage guide
```

**Structure Decision**: Single project structure selected because this is a simple CLI application with no web/mobile components. The calculator module separates concerns (operations, validation, CLI) while keeping the codebase simple and testable.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitution principles are satisfied by the planned design.

---

## Phase 0: Research & Technology Decisions

### Research Areas

All technical decisions are straightforward for this simple CLI calculator. No external research needed.

### Key Decisions

**Decision 1: No External Dependencies for Runtime**

- **Rationale**: Python's built-in `float` type and standard library provide everything needed for basic arithmetic. Adding dependencies would violate the Simplicity principle without adding value.
- **Alternatives Considered**:
  - `decimal.Decimal` for arbitrary precision - Rejected: Overkill for basic calculator; float precision (15-17 significant figures) exceeds spec requirement (6 decimal places)
  - `numpy` for numerical operations - Rejected: Massive dependency for simple arithmetic; violates Simplicity
- **Trade-offs**: Standard float has precision limits (~15-17 significant figures) and binary representation quirks (e.g., 0.1 + 0.2), but these are acceptable for a basic calculator and will be handled through proper formatting

**Decision 2: Input Format**

- **Rationale**: Space-separated format `<num1> <operator> <num2>` is simple to parse and intuitive for users
- **Implementation**: `str.split()` for tokenization, avoiding complex parsing libraries
- **Edge Cases**: Leading/trailing whitespace handled by `split()`, multiple spaces between tokens handled automatically

**Decision 3: Decimal Display Precision**

- **Rationale**: Display up to 10 decimal places with trailing zeros removed balances precision with readability
- **Implementation**: Python's built-in formatting with `:.10f` then strip trailing zeros
- **Handles**: Repeating decimals (10/3 = 3.3333333333), whole number results (7.5 * 2.0 = 15.0 → display "15")

**Decision 4: Error Handling Strategy**

- **Rationale**: Return error messages as strings rather than raising exceptions keeps the REPL running
- **Implementation**: Validation functions return `Result[float, str]` pattern (or use Optional with error messages)
- **User Experience**: Clear error messages without stack traces, calculator continues accepting input

### Technology Stack Summary

| Component | Technology | Justification |
|-----------|-----------|---------------|
| Language | Python 3.11+ | Specified in constitution; type hints, match statements |
| Package Manager | uv | Constitution requirement; fast, reliable |
| Runtime Deps | None (stdlib only) | Simplicity principle; built-in float sufficient |
| Test Framework | pytest | Constitution requirement; industry standard |
| Coverage | pytest-cov | Constitution requirement; ≥95% target |
| Type Checker | mypy (strict) | Constitution requirement |
| Linter/Formatter | ruff | Constitution requirement; fast, comprehensive |
| Entry Point | `python -m src.calculator` | Standard Python module execution |

---

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](./data-model.md) for complete data structure definitions.

**Core Types**:

```python
from typing import Union, Literal

# Operator type
Operator = Literal['+', '-', '*', '/']

# Result type (success or error message)
CalculationResult = Union[float, str]

# Parsed input
class ParsedInput:
    operand1: float
    operator: Operator
    operand2: float
```

**Key Design Principles**:
- Immutable data structures (no state mutation)
- Type-safe operator validation using Literal types
- Clear separation between parsed input and calculation result

### API Contracts

See [contracts/calculator_api.md](./contracts/calculator_api.md) for complete function signatures.

**Core Operations** (operations.py):
```python
def add(a: float, b: float) -> float
def subtract(a: float, b: float) -> float
def multiply(a: float, b: float) -> float
def divide(a: float, b: float) -> str | float  # Returns error message if b == 0
```

**Validation & Parsing** (validator.py):
```python
def parse_input(user_input: str) -> ParsedInput | str  # Returns error message if invalid
def validate_operator(op: str) -> Operator | str
def parse_number(num_str: str) -> float | str
```

**CLI Interface** (cli.py):
```python
def run_calculator() -> None  # Main REPL loop
def format_result(result: float) -> str  # Format with precision rules
def display_error(error: str) -> None
def display_result(result: float) -> None
```

### User Journey: Quick Start

See [quickstart.md](./quickstart.md) for complete user guide.

**Installation**:
```bash
# Clone repository
git clone <repo-url>
cd spec_test

# Install dependencies
uv sync

# Run calculator
uv run python -m src.calculator
```

**Basic Usage**:
```
$ uv run python -m src.calculator
Calculator ready. Type 'quit' or 'exit' to exit.
> 5 + 3
8
> 10.5 / 2
5.25
> 10 / 0
Error: Division by zero is not allowed
> quit
Goodbye!
```

---

## Phase 2: Implementation Strategy

**Phase 2 is handled by the `/sp.tasks` command**, which generates the detailed task breakdown in `tasks.md`.

### High-Level Implementation Order

1. **Setup Phase**: Project initialization with uv, pyproject.toml, directory structure
2. **Foundational Phase**: Core operations module (blocking prerequisite for all user stories)
3. **User Story 1 (P1)**: Basic arithmetic operations with integer inputs
4. **User Story 4 (P1)**: Error handling and validation (division by zero, invalid input)
5. **User Story 2 (P2)**: Decimal number handling with precision
6. **User Story 3 (P2)**: Negative number support
7. **Polish Phase**: Documentation, edge case validation, quality gate verification

### Constitution Re-Check (Post-Design)

| Principle | Status | Implementation Notes |
|-----------|--------|---------------------|
| **I. Type Safety** | ✅ PASS | All functions have complete type hints; Operator uses Literal type; mypy strict mode enforced |
| **II. Error Handling First** | ✅ PASS | divide() checks for zero before computation; parse_input() validates before parsing; all error paths return clear messages |
| **III. Test-Driven Development** | ✅ PASS | Each user story phase begins with writing failing tests |
| **IV. Edge Case Completeness** | ✅ PASS | Test coverage includes: decimals (0.1+0.2), division by zero, all negative combinations, invalid input (alphabets, empty, invalid operators), overflow (sys.float_info.max) |
| **V. Single Responsibility** | ✅ PASS | add/subtract/multiply/divide do one operation each; parse_input separated from validation; format_result separated from display; no function exceeds 20 lines |
| **VI. UV Package Management** | ✅ PASS | pyproject.toml with uv, no direct pip usage |

**Final Gate Status**: ✅ **APPROVED** - Design maintains constitution compliance

---

## Risks & Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Floating-point precision edge cases (0.1 + 0.2 ≠ 0.3) | Medium | High | Document expected behavior; test with known edge cases; format output to hide binary representation artifacts |
| User confusion with input format | Medium | Medium | Clear error messages with examples; quickstart.md with usage guide |
| Platform differences (Windows/Linux/Mac) | Low | Low | Using stdlib only eliminates platform-specific dependencies; uv handles cross-platform Python |

---

## Next Steps

1. ✅ Phase 0 complete (research decisions documented above)
2. ✅ Phase 1 complete (design artifacts generated)
3. ⏭️ Run `/sp.tasks` to generate detailed implementation tasks
4. ⏭️ Execute tasks following TDD workflow (tests → implementation → quality gates)

**Readiness**: Plan is complete and ready for task generation.
