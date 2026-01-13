# Changelog

All notable changes to Panaversity Calculator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-01-06

### Added - Rich Interactive UI

#### Visual Branding & Navigation
- **Professional branded header** with "Panaversity Calculator v2.0"
- **Arrow-key menu navigation** for operation selection (↑/↓ to navigate, Enter to select)
- **Emoji-enhanced menu**: ➕ Addition, ➖ Subtraction, ✖️ Multiplication, ➗ Division, 🚪 Exit
- **Graceful exit handling** (Ctrl+C or Exit selection)

#### Interactive Input & Validation
- **Smart number input** with real-time validation
- **Support for integers, decimals, and negative numbers**
- **Automatic zero-prevention** for division denominator
- **Cyan-themed prompts** for visual consistency
- **Error messages with re-prompting** on invalid input

#### Color-Coded Feedback System
- **Cyan**: Prompts and menu selections
- **Green bold**: Successful calculation results
- **Red bold**: Error messages
- **Consistent theming** across all interactions

#### Calculation History Tracking
- **Session-based history** with Rich formatted table
- **Table columns**: #, Time (HH:MM:SS), Expression, Operator, Result, Status
- **Color-coded status**: Green OK, Red ERROR
- **Pagination**: Last 20 calculations displayed for performance
- **Alternating row styles** for readability
- **Real-time updates** after each calculation

#### Quality & Polish
- **Terminal width validation** (warns if < 80 characters)
- **Comprehensive integration tests** for complete workflows
- **Edge case handling** (large numbers, many decimals, rapid input)
- **Type-safe implementation** with strict mypy compliance
- **95%+ test coverage** maintained

### Changed
- **Default interface**: `python -m calculator` now launches Rich UI (v2.0)
- **Entry point**: Updated `__main__.py` to use `run_rich_calculator()`
- **Dependencies**: Added `rich>=13.0.0` and `questionary>=2.0.0`
- **Version**: Bumped to 0.2.0 for new major feature set

### Backward Compatibility
- **Legacy CLI preserved**: Text-based interface (v1.0) still available via `python -m calculator.cli`
- **Core logic unchanged**: All arithmetic operations maintain same behavior
- **Existing tests valid**: Original test suite remains functional

### New Dependencies
- `rich>=13.0.0` - Terminal UI framework for panels, tables, and styling
- `questionary>=2.0.0` - Interactive prompts with arrow-key navigation

## [0.1.0] - 2026-01-04

### Added

- **Basic Arithmetic Operations**: Support for addition (+), subtraction (-), multiplication (*), and division (/)
- **Decimal Number Handling**: Precise decimal calculations with up to 10 decimal places, trailing zeros automatically removed
- **Negative Number Support**: Full support for negative numbers in all operations
- **Robust Error Handling**:
  - Division by zero detection with clear error message
  - Invalid number input validation
  - Invalid operator detection
  - Incomplete input detection
- **Interactive REPL**: Command-line interface with continuous prompt for calculations
- **Exit Commands**: Type 'quit' or 'exit' (case-insensitive) to close calculator
- **Type Safety**: Full Python 3.11+ type hints with strict mypy compliance
- **Comprehensive Test Suite**:
  - Unit tests for all operations and validators
  - Integration tests for end-to-end workflows
  - Edge case tests for overflow, precision, and special values
  - 95%+ code coverage

### Features

- Single-operation calculator: `<number> <operator> <number>` format
- Input parsing with whitespace handling
- Formatted output with intelligent decimal display
- Error recovery: Calculator continues running after errors
- Clean separation of concerns: operations, validation, CLI layers

### Technical

- **Python**: 3.11+ required
- **Package Manager**: UV for dependency management
- **Testing**: pytest with coverage reporting
- **Type Checking**: mypy in strict mode
- **Linting**: ruff for code quality
- **Quality Gates**: 95% coverage minimum, strict type checking, zero linting errors

### Documentation

- README.md with installation and usage instructions
- Quick Start Guide with examples and troubleshooting
- API contracts documentation
- Comprehensive inline docstrings with examples

### Project Structure

```
src/calculator/
├── __init__.py      # Type exports
├── operations.py    # Arithmetic operations (add, subtract, multiply, divide)
├── validator.py     # Input parsing and validation
└── cli.py          # Interactive CLI interface

tests/
├── unit/           # Unit tests for individual components
├── integration/    # End-to-end workflow tests
└── __init__.py
```

### Constitution Compliance

- ✅ Type Safety: All functions fully typed
- ✅ Error Handling First: Validation before computation
- ✅ Test-Driven Development: Tests written before implementation
- ✅ Single Responsibility: All functions <20 lines
- ✅ Edge Case Completeness: Comprehensive edge case coverage
- ✅ UV Package Management: Standard uv-based workflow

[1.0.0]: https://github.com/yourusername/calculator/releases/tag/v1.0.0
