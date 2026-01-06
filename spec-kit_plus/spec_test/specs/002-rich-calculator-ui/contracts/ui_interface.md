# UI Component Contracts

**Feature**: 002-rich-calculator-ui
**Date**: 2026-01-05

## Overview

This document defines the interfaces (contracts) for all UI components in the professional calculator interface. Each component has clear inputs, outputs, and error conditions.

---

## Component 1: Header Display

### Module
`src/calculator/ui/header.py`

### Function Signature
```python
def render_header() -> Panel:
    """Render the calculator header panel."""
```

### Contract

**Input**: None (static content)

**Output**:
- `rich.panel.Panel` object containing:
  - Title: "Panaversity Calculator v2.0"
  - Border style: cyan
  - Box style: DOUBLE
  - Padding: (0, 2)

**Errors**: None (pure function, no failure modes)

**Side Effects**: None

**Example**:
```python
from calculator.ui.header import render_header
from rich.console import Console

console = Console()
header = render_header()
console.print(header)
```

---

## Component 2: Operation Menu

### Module
`src/calculator/ui/menu.py`

### Function Signature
```python
def select_operation() -> Operator | None:
    """Display operation selection menu and get user choice."""
```

### Contract

**Input**: None (displays predefined menu options)

**Output**:
- `Operator` ('+', '-', '*', '/') if user selects an operation
- `None` if user cancels (Ctrl+C)

**Errors**:
- `KeyboardInterrupt`: User presses Ctrl+C (converted to `None` return)

**Side Effects**:
- Displays interactive menu in terminal
- Waits for user arrow key navigation and Enter

**Behavior**:
1. Display menu with options: "Addition", "Subtraction", "Multiplication", "Division", "Exit"
2. User navigates with arrow keys
3. User presses Enter to select
4. Returns corresponding operator or None

**Example**:
```python
from calculator.ui.menu import select_operation

operator = select_operation()
if operator is None:
    print("User cancelled")
elif operator == '+':
    print("Addition selected")
```

---

## Component 3: Number Input

### Module
`src/calculator/ui/input.py`

### Function Signature
```python
def get_number(prompt: str, allow_zero: bool = True) -> float | None:
    """Get validated numeric input from user."""
```

### Contract

**Input**:
- `prompt`: Display message for the input (e.g., "Enter first number:")
- `allow_zero`: Whether to accept 0 as valid input (default: True)

**Output**:
- `float`: Valid number entered by user
- `None`: User cancelled (Ctrl+C)

**Errors**:
- Re-prompts automatically on invalid input (not a number)
- Displays red error message: "Please enter a valid number"

**Side Effects**:
- Displays prompt in cyan color
- Waits for user text input
- Shows inline error if validation fails
- Re-prompts until valid input or cancellation

**Validation**:
1. Must parse as float
2. Can be negative
3. Can be decimal
4. Can be zero (if `allow_zero=True`)

**Example**:
```python
from calculator.ui.input import get_number

# Get first number
num1 = get_number("Enter first number:")
if num1 is None:
    return  # User cancelled

# Get divisor (non-zero)
num2 = get_number("Enter divisor:", allow_zero=False)
if num2 is None:
    return  # User cancelled
```

---

## Component 4: Result Display

### Module
`src/calculator/ui/output.py`

### Function Signature
```python
def display_result(result: float) -> None:
    """Display successful calculation result."""

def display_error(error: str) -> None:
    \"\"\"Display error message.\"\"\"
```

### Contract

**`display_result` Input**:
- `result`: Numeric result to display

**`display_result` Output**: None

**`display_result` Side Effects**:
- Prints result in green bold color
- Formatted to 10 decimal places (trailing zeros removed)

**`display_error` Input**:
- `error`: Error message string

**`display_error` Output**: None

**`display_error` Side Effects**:
- Prints error message in red bold color
- Prefixed with "Error:" if not already present

**Example**:
```python
from calculator.ui.output import display_result, display_error

# Successful result
display_result(42.5)  # Prints "[green bold]42.5[/green bold]"

# Error
display_error("Division by zero is not allowed")  # Prints "[red bold]Error: Division by zero is not allowed[/red bold]"
```

---

## Component 5: History Table

### Module
`src/calculator/ui/history.py`

### Function Signature
```python
def render_history_table(history: CalculationHistory) -> Table:
    \"\"\"Render calculation history as a Rich table.\"\"\"
```

### Contract

**Input**:
- `history`: CalculationHistory object containing calculation records

**Output**:
- `rich.table.Table` object ready for rendering

**Errors**: None (handles empty history gracefully)

**Side Effects**: None (pure function)

**Behavior**:
1. Shows last 20 entries (pagination for performance)
2. Displays columns: #, Time, Expression, Operator, Result, Status
3. Color-codes status: green for "OK", red for "ERROR"
4. Alternating row styles for readability

**Example**:
```python
from calculator.ui.history import render_history_table
from calculator.models import CalculationHistory
from rich.console import Console

console = Console()
history = CalculationHistory()
# ... add calculations ...

table = render_history_table(history)
console.print(table)
```

---

## Component 6: Dashboard Layout

### Module
`src/calculator/rich_cli.py`

### Function Signature
```python
def create_dashboard_layout() -> Layout:
    \"\"\"Create the main calculator dashboard layout.\"\"\"

def update_dashboard(layout: Layout, history: CalculationHistory, current_expr: str, current_result: str) -> None:
    \"\"\"Update all dashboard sections.\"\"\"
```

### Contract

**`create_dashboard_layout` Input**: None

**`create_dashboard_layout` Output**:
- `rich.layout.Layout` with named regions:
  - "header" (fixed, size=5)
  - "status" (fixed, size=3)
  - "body" (flexible)
  - "footer" (fixed, size=3)

**`update_dashboard` Input**:
- `layout`: Layout object to update
- `history`: Current calculation history
- `current_expr`: Current expression (e.g., "5 + 3")
- `current_result`: Current result (e.g., "8")

**`update_dashboard` Output**: None

**`update_dashboard` Side Effects**:
- Modifies layout regions with updated content
- Renders header, status bar, history table, footer

**Example**:
```python
from calculator.rich_cli import create_dashboard_layout, update_dashboard
from calculator.models import CalculationHistory
from rich.console import Console

console = Console()
layout = create_dashboard_layout()
history = CalculationHistory()

# Initial render
update_dashboard(layout, history, "", "")
console.print(layout)

# After calculation
update_dashboard(layout, history, "5 + 3", "8")
console.print(layout)
```

---

## Integration Contract: Main Calculator Loop

### Module
`src/calculator/rich_cli.py`

### Function Signature
```python
def run_rich_calculator() -> None:
    \"\"\"Main entry point for enhanced calculator with Rich UI.\"\"\"
```

### Contract

**Input**: None (reads from stdin via questionary)

**Output**: None (writes to stdout via Rich)

**Errors**:
- Handles all user input errors gracefully
- Catches KeyboardInterrupt for clean exit
- Never crashes on invalid input

**Side Effects**:
- Displays interactive UI in terminal
- Maintains session state (calculation history)
- Runs until user selects "Exit" or presses Ctrl+C

**Flow**:
1. Validate terminal requirements
2. Create dashboard layout
3. Loop:
   a. Display operation menu
   b. Get user selection
   c. If Exit or None: break
   d. Get first number (with validation)
   e. Get second number (with validation, check zero for division)
   f. Perform calculation
   g. Display result or error
   h. Add to history
   i. Update dashboard
4. Display goodbye message

**Example**:
```python
from calculator.rich_cli import run_rich_calculator

if __name__ == "__main__":
    run_rich_calculator()
```

---

## Testing Contract

### Unit Test Requirements

Each component must have:
1. **Happy path tests**: Valid inputs produce expected outputs
2. **Edge case tests**: Boundary conditions (empty history, zero, negative numbers)
3. **Error handling tests**: Invalid inputs handled gracefully
4. **Type safety tests**: mypy passes with strict mode

### Integration Test Requirements

Full calculator workflow must test:
1. **Complete calculation**: Menu → numbers → result → history
2. **Error scenarios**: Division by zero, invalid input
3. **Cancellation**: Ctrl+C at each input stage
4. **Multiple calculations**: History accumulation
5. **Performance**: 50+ calculations without degradation

---

## Performance Contracts

| Component | Performance Requirement |
|-----------|------------------------|
| `render_header()` | < 1ms (static content) |
| `select_operation()` | Instant response to arrow keys |
| `get_number()` | Instant validation feedback |
| `display_result()` | < 1ms (direct print) |
| `render_history_table()` | < 25ms for 200 rows |
| `update_dashboard()` | < 50ms total update |

---

## Backward Compatibility Contract

### Existing CLI (`src/calculator/cli.py`)

**Preserved**:
- All existing functions remain functional
- Can still be run with `python -m calculator.cli`
- No breaking changes to existing API

**Enhanced**:
- `display_result()` and `display_error()` enhanced with colors
- Existing tests continue to pass

---

## Component Dependencies

```
rich_cli.py
  ├── ui/header.py → render_header()
  ├── ui/menu.py → select_operation()
  ├── ui/input.py → get_number()
  ├── ui/output.py → display_result(), display_error()
  └── ui/history.py → render_history_table()

All UI components depend on:
  - rich (Console, Panel, Table, Layout)
  - questionary (select, text)
  - models.py (CalculationRecord, CalculationHistory)
  - operations.py (add, subtract, multiply, divide)
```

---

**Contracts Complete**: 2026-01-05
**All Interfaces Defined**: Yes
**Type Safe**: ✅ Full mypy compliance
**Testable**: ✅ Clear inputs/outputs for all components
