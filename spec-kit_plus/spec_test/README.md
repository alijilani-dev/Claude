# Panaversity Calculator v2.0

A professional command-line calculator with an interactive Rich UI, featuring arrow-key navigation, color-coded output, and calculation history tracking.

## Features

### Core Functionality
- **Four arithmetic operations**: Addition, Subtraction, Multiplication, Division
- **Decimal number support** with precise formatting (up to 10 decimal places)
- **Negative number handling** for all operations
- **Robust error handling** (division by zero, invalid input)
- **Type-safe Python 3.11+** implementation with strict mypy compliance

### Rich Interactive UI (v2.0)
- **🎨 Professional branded header** with "Panaversity Calculator v2.0"
- **⌨️ Arrow-key menu navigation** for operation selection
- **🎯 Interactive number input** with real-time validation
- **🌈 Color-coded feedback**:
  - Cyan prompts and menu selections
  - Green bold for successful results
  - Red bold for error messages
- **📊 Calculation history table** showing all session calculations
- **✨ Status tracking** with color-coded OK/ERROR indicators

## Prerequisites

- Python 3.11 or higher
- `uv` package manager

**Installing uv** (if not already installed):
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd spec_test
   ```

2. **Install dependencies**:
   ```bash
   uv sync --dev
   ```

## Usage

**Start the Rich UI calculator** (v2.0, recommended):
```bash
uv run python -m calculator
```

You'll see the professional interface with:
1. **Panaversity Calculator v2.0** header
2. **Interactive menu** with arrow-key navigation:
   - ➕ Addition
   - ➖ Subtraction
   - ✖️  Multiplication
   - ➗ Division
   - 🚪 Exit

### How to Use

1. **Navigate** the menu using **↑** and **↓** arrow keys
2. **Select** an operation by pressing **Enter**
3. **Enter** the first number (supports decimals and negatives)
4. **Enter** the second number
5. **View** the result and updated history table
6. **Repeat** or select **Exit** to quit

### Example Session

```
╭─────────────────────────────────────╮
│  Panaversity Calculator v2.0        │
╰─────────────────────────────────────╯

? Select an operation:
  ➕ Addition
❯ ➖ Subtraction
  ✖️  Multiplication
  ➗ Division
  ───────────────
  🚪 Exit

? Enter first number: 10
? Enter second number: 3

Result: 7

╭─────────────────── Calculation History ───────────────────╮
│  #  │  Time    │  Expression  │ Operator │  Result │ Status │
├─────┼──────────┼──────────────┼──────────┼─────────┼────────┤
│  1  │ 14:23:15 │ 10 - 3       │    -     │    7    │   OK   │
╰────────────────────────────────────────────────────────────╯
```

### Keyboard Shortcuts

- **↑/↓ Arrow Keys**: Navigate menu
- **Enter**: Select operation/confirm input
- **Ctrl+C**: Exit gracefully at any time
- **Exit Option**: Select from menu to quit

### Legacy CLI (v1.0)

The original text-based CLI is still available:
```bash
uv run python -m calculator.cli
```

## Development

### Run Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=src --cov-report=term-missing

# Specific test file
uv run pytest tests/unit/test_operations.py
```

### Type Checking

```bash
uv run mypy src/ --strict
```

### Linting and Formatting

```bash
# Check linting
uv run ruff check src/

# Format code
uv run ruff format src/
```

### Quality Gates

All of the following must pass before committing:

```bash
uv run pytest --cov=src --cov-report=term-missing  # ≥95% coverage
uv run mypy src/ --strict                           # No type errors
uv run ruff check src/                              # No linting errors
```

## Project Structure

```
src/calculator/
├── __init__.py         # Type imports and exports
├── __main__.py         # Entry point (runs Rich UI)
├── operations.py       # Core arithmetic operations
├── validator.py        # Input validation and parsing
├── models.py           # Data models (CalculationRecord, ColorScheme, etc.)
├── cli.py              # Legacy text-based CLI (v1.0)
├── rich_cli.py         # Rich UI calculator runner (v2.0)
└── ui/                 # Rich UI components
    ├── __init__.py
    ├── colors.py       # Color scheme constants
    ├── formatters.py   # Result formatting utilities
    ├── header.py       # Header panel rendering
    ├── menu.py         # Operation selection menu
    ├── input.py        # Number input with validation
    ├── output.py       # Result/error display
    └── history.py      # Calculation history table

tests/
├── unit/               # Unit tests for individual components
│   ├── test_operations.py
│   ├── test_validator.py
│   └── ui/             # UI component tests
│       ├── test_header.py
│       ├── test_input.py
│       ├── test_menu.py
│       ├── test_output.py
│       └── test_history.py
└── integration/        # End-to-end workflow tests
    ├── test_cli_workflows.py
    └── test_rich_cli.py

pyproject.toml          # Project configuration and dependencies
```

## Troubleshooting

### Terminal Compatibility

**Requirement**: The Rich UI requires a terminal with ANSI color support and at least 80 characters width.

**Supported Terminals**:
- ✅ Windows Terminal (recommended for Windows)
- ✅ WSL / Linux terminal
- ✅ macOS Terminal.app
- ✅ iTerm2
- ✅ VS Code integrated terminal
- ⚠️  CMD (limited color support)
- ⚠️  PowerShell (may need configuration for emoji support)

**If colors don't display**:
- Windows: Use Windows Terminal instead of CMD
- Check terminal supports ANSI escape codes
- Verify terminal width is ≥80 characters
- Fallback: Use legacy CLI with `uv run python -m calculator.cli`

**Terminal too narrow**:
- You'll see a warning: "⚠️  Warning: Terminal width is less than 80 characters"
- Resize terminal window or use fullscreen mode
- Some UI elements may not display correctly in narrow terminals

## License

MIT
