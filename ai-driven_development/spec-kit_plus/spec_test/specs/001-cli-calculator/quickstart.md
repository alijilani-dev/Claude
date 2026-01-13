# Quick Start Guide: CLI Calculator

**Version**: 1.0
**Date**: 2026-01-04
**For**: End users

## What is CLI Calculator?

A simple command-line calculator for performing basic arithmetic operations (addition, subtraction, multiplication, division). Runs in your terminal with interactive prompts.

## Prerequisites

- Python 3.11 or higher
- `uv` package manager installed

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
   uv sync
   ```

   This creates a virtual environment and installs all required packages.

## Running the Calculator

**Start the calculator**:
```bash
uv run python -m calculator
```

You should see:
```
Calculator ready. Type 'quit' or 'exit' to exit.
>
```

## Basic Usage

### Simple Calculations

Enter calculations in the format: `<number> <operator> <number>`

**Examples**:
```
> 5 + 3
8

> 10 - 4
6

> 6 * 7
42

> 20 / 4
5
```

### Decimal Numbers

The calculator handles decimal numbers with precision:

```
> 5.5 + 2.3
7.8

> 10.0 / 3.0
3.3333333333

> 7.5 * 2.0
15
```

### Negative Numbers

Negative numbers are fully supported:

```
> -5 + 3
-2

> 10 - 15
-5

> -6 * -7
42

> -20 / 4
-5
```

## Error Handling

The calculator provides clear error messages for invalid inputs:

### Division by Zero
```
> 5 / 0
Error: Division by zero is not allowed
```

### Invalid Numbers
```
> abc + 5
Error: Invalid input - please enter valid numbers
```

### Invalid Operators
```
> 10 $ 5
Error: Invalid operator - use +, -, *, or /
```

### Incomplete Input
```
> 5 +
Error: Please provide two numbers and an operator
```

## Exiting the Calculator

Type `quit` or `exit` (case-insensitive) to close the calculator:

```
> quit
Goodbye!
```

or

```
> exit
Goodbye!
```

## Input Format Rules

✅ **Correct formats**:
- `5 + 3` - spaces between numbers and operator
- `  10  -  4  ` - extra spaces are OK
- `-5 + 3` - negative numbers supported
- `10.5 / 2` - decimal numbers supported

❌ **Incorrect formats**:
- `5+3` - missing spaces (will be treated as invalid number)
- `5 plus 3` - operator must be symbol (+, -, *, /)
- `2 + 3 + 4` - only two numbers allowed per calculation
- `(5 + 3) * 2` - parentheses not supported

## Tips

1. **Always use spaces**: `5 + 3` not `5+3`
2. **One operation at a time**: The calculator handles one operation per line
3. **Decimals are OK**: You can use decimal points freely
4. **Negative numbers**: Put the minus sign directly before the number (no space)
5. **Error recovery**: If you get an error, just try again - the calculator keeps running

## Common Questions

**Q: Can I do multiple operations like `2 + 3 * 4`?**
A: No, the calculator handles one operation at a time. Calculate `3 * 4` first, then add 2.

**Q: How many decimal places does it show?**
A: Up to 10 decimal places, with trailing zeros removed. For example, `10 / 3` shows `3.3333333333`.

**Q: What's the largest number I can use?**
A: Python floats support very large numbers (up to about 10^308), but extremely large results may show as "inf".

**Q: Does it remember previous calculations?**
A: No, each calculation is independent. There's no history or memory feature.

## Example Session

```
$ uv run python -m calculator
Calculator ready. Type 'quit' or 'exit' to exit.
> 100 + 50
150
> 150 / 3
50
> 50 * 2
100
> 100 - 25
75
> quit
Goodbye!
```

## Troubleshooting

**Problem**: `command not found: uv`
**Solution**: Install uv using the installation command in Prerequisites section

**Problem**: `ModuleNotFoundError: No module named 'calculator'`
**Solution**: Make sure you're in the project root directory and ran `uv sync`

**Problem**: Calculator shows `Error: Invalid input` for valid-looking input
**Solution**: Check that you're using spaces between numbers and operators, e.g., `5 + 3` not `5+3`

**Problem**: `SyntaxError` or other Python errors
**Solution**: Ensure Python 3.11+ is installed: `python --version`

## Support

For issues or questions, please open an issue in the project repository.

---

**Happy calculating!** 🧮
