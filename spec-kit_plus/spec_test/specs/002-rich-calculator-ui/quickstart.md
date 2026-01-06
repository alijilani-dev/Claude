# Quickstart Guide: Professional Calculator Interface

**Feature**: 002-rich-calculator-ui
**Date**: 2026-01-05

## For Developers

### Prerequisites

- Python 3.11+
- uv package manager
- Terminal with ANSI color support (80+ character width recommended)

### Installation

```bash
# Clone/navigate to project
cd /path/to/calculator

# Install dependencies
uv sync

# Verify installation
uv run python --version  # Should show Python 3.11+
```

### Running the Enhanced Calculator

```bash
# Run new Rich-based interface (default)
uv run python -m calculator

# Run legacy text-based interface (backward compatibility)
uv run python -m calculator.cli
```

### Development Workflow

#### 1. Setup Development Environment

```bash
# Install dev dependencies
uv sync

# Verify tools installed
uv run mypy --version
uv run pytest --version
uv run ruff --version
```

#### 2. Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/ui/test_header.py

# Run with verbose output
uv run pytest -v
```

#### 3. Type Checking

```bash
# Check all source code
uv run mypy src/ --strict

# Check specific file
uv run mypy src/calculator/rich_cli.py --strict
```

#### 4. Linting

```bash
# Check code style
uv run ruff check src/

# Auto-fix issues
uv run ruff check src/ --fix

# Format code
uv run ruff format src/
```

#### 5. Quality Gates (Must Pass Before Commit)

```bash
# Run all quality checks
uv run pytest --cov=src --cov-report=term-missing && \
uv run mypy src/ --strict && \
uv run ruff check src/

# Verify 95%+ coverage
uv run pytest --cov=src --cov-report=term --cov-fail-under=95
```

### Visual Testing

After making UI changes, manually verify:

```bash
# Run calculator
uv run python -m calculator

# Check:
# ✓ Header displays "Panaversity Calculator v2.0" with cyan border
# ✓ Arrow keys navigate operation menu
# ✓ Prompts display in cyan
# ✓ Results display in green
# ✓ Errors display in red
# ✓ History table shows with proper columns
# ✓ Multiple calculations accumulate in history
```

### Project Structure

```
src/calculator/
├── __init__.py          # Existing: types and exports
├── __main__.py          # Updated: now uses rich_cli
├── operations.py        # Existing: arithmetic functions
├── validator.py         # Existing: input validation
├── cli.py               # Existing: legacy text interface
├── rich_cli.py          # NEW: enhanced Rich interface
├── models.py            # NEW: data classes
└── ui/                  # NEW: UI components
    ├── __init__.py
    ├── header.py        # Header panel rendering
    ├── menu.py          # Operation selection
    ├── input.py         # Number input with validation
    ├── output.py        # Result/error display
    ├── history.py       # History table rendering
    └── colors.py        # Color scheme constants

tests/
├── unit/
│   ├── test_operations.py      # Existing
│   ├── test_validator.py       # Existing
│   ├── test_models.py           # NEW
│   └── ui/                      # NEW
│       ├── test_header.py
│       ├── test_menu.py
│       ├── test_input.py
│       ├── test_output.py
│       └── test_history.py
└── integration/
    ├── test_cli.py              # Existing
    └── test_rich_cli.py         # NEW
```

### Adding New Features

Follow TDD workflow (Constitution Principle III):

```bash
# 1. Write failing test
cat > tests/unit/ui/test_new_feature.py << 'EOF'
def test_new_feature():
    # Arrange
    ...
    # Act
    result = new_feature()
    # Assert
    assert result == expected
EOF

# 2. Verify test fails
uv run pytest tests/unit/ui/test_new_feature.py
# Should see: FAILED

# 3. Implement feature
# Edit src/calculator/ui/new_feature.py

# 4. Verify test passes
uv run pytest tests/unit/ui/test_new_feature.py
# Should see: PASSED

# 5. Run all quality gates
uv run pytest --cov=src --cov-fail-under=95 && \
uv run mypy src/ --strict && \
uv run ruff check src/
```

### Debugging

```bash
# Run with Python debugger
uv run python -m pdb -m calculator

# Run tests with debugging
uv run pytest tests/unit/ui/test_menu.py --pdb

# Verbose pytest output
uv run pytest -vv --tb=long

# Print coverage report
uv run pytest --cov=src --cov-report=html
# Open htmlcov/index.html in browser
```

---

## For End Users

### Installation

```bash
# Install with pip
pip install calculator

# Or use uv
uv pip install calculator
```

### Running the Calculator

```bash
# Start calculator
calculator

# Or with python module
python -m calculator
```

### Using the Calculator

#### 1. Launch

```bash
$ calculator

╭─────────────────────────────────────╮
│  Panaversity Calculator v2.0        │
│  Interactive Mode                   │
╰─────────────────────────────────────╯
```

#### 2. Select Operation

Use arrow keys (↑/↓) to navigate menu:

```
? Choose an operation:
❯ Addition
  Subtraction
  Multiplication
  Division
  Exit
```

Press **Enter** to select.

#### 3. Enter Numbers

```
Enter first number: 10
Enter second number: 5
```

#### 4. View Result

```
╭─────────────────────────────────────╮
│ Input: 10 + 5 = 15                  │
╰─────────────────────────────────────╯

╭───────────── Calculation History ─────────────╮
│ # │ Time     │ Expression │ Op │ Result │ Status │
├───┼──────────┼────────────┼────┼────────┼────────┤
│ 1 │ 12:34:56 │ 10 + 5     │ +  │ 15     │ OK     │
╰───┴──────────┴────────────┴────┴────────┴────────╯
```

#### 5. Continue or Exit

- **Continue**: Menu appears again for next calculation
- **Exit**: Select "Exit" from menu or press **Ctrl+C**

### Supported Operations

| Operation      | Symbol | Example       | Result |
|----------------|--------|---------------|--------|
| Addition       | +      | 5 + 3         | 8      |
| Subtraction    | -      | 10 - 4        | 6      |
| Multiplication | *      | 7 * 6         | 42     |
| Division       | /      | 20 / 4        | 5      |

### Number Format Support

- **Integers**: 5, 10, 100
- **Decimals**: 3.14, 0.5, 10.75
- **Negatives**: -5, -10.5
- **Large numbers**: 999999.123456789

### Error Handling

#### Division by Zero
```
Enter first number: 10
Enter second number: 0

Error: Division by zero is not allowed
```

#### Invalid Input
```
Enter first number: abc
❌ Please enter a valid number
Enter first number: _
```

### Keyboard Shortcuts

| Key         | Action                    |
|-------------|---------------------------|
| ↑/↓         | Navigate menu             |
| Enter       | Select/Confirm            |
| Ctrl+C      | Cancel/Exit               |
| Backspace   | Edit input                |

### History Features

- **Automatic Recording**: All calculations saved to session history
- **Scrolling**: Shows last 20 calculations (performance optimized)
- **Status Indicators**:
  - **Green OK**: Successful calculation
  - **Red ERROR**: Failed calculation (e.g., division by zero)

### Troubleshooting

#### Terminal Too Narrow
```
⚠ Warning: Terminal width is 70 characters
Recommended: 80+ characters for best layout
Press Enter to continue anyway...
```

**Solution**: Resize terminal window to at least 80 characters wide.

#### No Color Support
```
Error: This application requires ANSI color support
```

**Solutions**:
- **Windows**: Use Windows Terminal or PowerShell (not CMD)
- **Linux/macOS**: Most terminals support ANSI by default
- **SSH**: Ensure `TERM` environment variable is set (e.g., `TERM=xterm-256color`)

#### Import Errors
```
ModuleNotFoundError: No module named 'rich'
```

**Solution**: Reinstall with dependencies:
```bash
pip install --upgrade calculator
```

### Examples

#### Basic Calculation
```bash
$ calculator
? Choose an operation: Addition
Enter first number: 15
Enter second number: 27
Result: 42
```

#### Multiple Calculations
```bash
? Choose an operation: Multiplication
Enter first number: 6
Enter second number: 7
Result: 42

? Choose an operation: Division
Enter first number: 84
Enter second number: 2
Result: 42
```

#### Decimal Precision
```bash
? Choose an operation: Division
Enter first number: 10
Enter second number: 3
Result: 3.3333333333
```

#### Negative Numbers
```bash
? Choose an operation: Subtraction
Enter first number: 5
Enter second number: 10
Result: -5
```

---

## Quick Reference

### Development Commands

```bash
uv sync                          # Install dependencies
uv run python -m calculator      # Run enhanced UI
uv run pytest                    # Run tests
uv run mypy src/ --strict        # Type check
uv run ruff check src/           # Lint
```

### User Commands

```bash
calculator                       # Start calculator
↑/↓ arrows                       # Navigate menu
Enter                            # Select
Ctrl+C                           # Exit
```

### Quality Standards

- **Test Coverage**: ≥ 95%
- **Type Checking**: 100% (strict mypy)
- **Linting**: 0 errors (ruff)
- **Performance**: < 1s response to user actions

---

**Quickstart Guide Complete**: 2026-01-05
**Ready for**: Development and end-user use
**Constitution Compliant**: ✅
