# Data Model: Professional Calculator Interface

**Feature**: 002-rich-calculator-ui
**Date**: 2026-01-05

## Overview

This document defines the data structures required for the professional calculator UI. All entities follow the project's type safety requirements (Constitution Principle I).

---

## Entity 1: CalculationRecord

### Purpose
Represents a single calculation entry in the session history.

### Structure

```python
from dataclasses import dataclass
from typing import Literal

Operator = Literal['+', '-', '*', '/']

@dataclass(frozen=True)
class CalculationRecord:
    """Immutable record of a single calculation.

    Attributes:
        operand1: First number in the calculation
        operator: Arithmetic operator (+, -, *, /)
        operand2: Second number in the calculation
        result: Calculated result (float) or error message (str)
        timestamp: Unix timestamp when calculation was performed
    """
    operand1: float
    operator: Operator
    operand2: float
    result: float | str
    timestamp: float
```

### Validation Rules

1. **operand1**: Must be valid float (including negative and decimal)
2. **operator**: Must be one of: '+', '-', '*', '/'
3. **operand2**: Must be valid float (including negative and decimal)
4. **result**:
   - `float` when calculation succeeds
   - `str` (error message) when calculation fails (e.g., division by zero)
5. **timestamp**: Unix timestamp (seconds since epoch), auto-generated

### Display Format

For table rendering:
- **Expression**: f"{operand1} {operator} {operand2}"
- **Result**: `format_result(result)` if float, else display error message
- **Status**: "OK" if result is float, "ERROR" if result is string
- **Time**: `datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")`

### Example Instances

```python
from time import time

# Successful calculation
calc1 = CalculationRecord(
    operand1=5.0,
    operator='+',
    operand2=3.0,
    result=8.0,
    timestamp=time()
)

# Decimal calculation
calc2 = CalculationRecord(
    operand1=10.5,
    operator='*',
    operand2=2.0,
    result=21.0,
    timestamp=time()
)

# Error case (division by zero)
calc3 = CalculationRecord(
    operand1=10.0,
    operator='/',
    operand2=0.0,
    result="Error: Division by zero is not allowed",
    timestamp=time()
)

# Negative numbers
calc4 = CalculationRecord(
    operand1=-5.0,
    operator='-',
    operand2=-3.0,
    result=-2.0,
    timestamp=time()
)
```

---

## Entity 2: ColorScheme

### Purpose
Centralized color definitions matching the cyan/green/red palette specified in requirements.

### Structure

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class ColorScheme:
    """UI color scheme constants.

    Attributes:
        prompt_color: Color for user input prompts (cyan)
        success_color: Color for successful results (green)
        error_color: Color for error messages (red)
        operator_color: Color for operator symbols (yellow)
        border_color: Color for panel borders (cyan)
        header_color: Color for header text (cyan)
        dim_color: Color for secondary/dim text (dim white)
    """
    prompt_color: str = "cyan"
    success_color: str = "green bold"
    error_color: str = "red bold"
    operator_color: str = "yellow"
    border_color: str = "cyan"
    header_color: str = "bold cyan"
    dim_color: str = "dim"

# Singleton instance
DEFAULT_COLOR_SCHEME = ColorScheme()
```

### Usage Pattern

```python
from rich.console import Console
from rich.theme import Theme

# Convert to Rich Theme
CALCULATOR_THEME = Theme({
    "prompt": DEFAULT_COLOR_SCHEME.prompt_color,
    "success": DEFAULT_COLOR_SCHEME.success_color,
    "error": DEFAULT_COLOR_SCHEME.error_color,
    "operator": DEFAULT_COLOR_SCHEME.operator_color,
    "border": DEFAULT_COLOR_SCHEME.border_color,
    "header": DEFAULT_COLOR_SCHEME.header_color,
})

console = Console(theme=CALCULATOR_THEME)
```

---

## Entity 3: MenuOption

### Purpose
Represents a selectable operation in the interactive menu.

### Structure

```python
from dataclasses import dataclass
from typing import Literal, Callable

Operator = Literal['+', '-', '*', '/']

@dataclass(frozen=True)
class MenuOption:
    """Menu option for operation selection.

    Attributes:
        display_name: Human-readable name shown in menu
        operator: Corresponding operator symbol
        description: Optional description of the operation
    """
    display_name: str
    operator: Operator
    description: str = ""
```

### Predefined Options

```python
MENU_OPTIONS = [
    MenuOption(
        display_name="Addition",
        operator='+',
        description="Add two numbers together"
    ),
    MenuOption(
        display_name="Subtraction",
        operator='-',
        description="Subtract second number from first"
    ),
    MenuOption(
        display_name="Multiplication",
        operator='*',
        description="Multiply two numbers"
    ),
    MenuOption(
        display_name="Division",
        operator='/',
        description="Divide first number by second"
    ),
]
```

### Menu Display Format

For questionary.select():
```python
choices = [option.display_name for option in MENU_OPTIONS]
```

### Operator Mapping

```python
from typing import Dict

# Map display names to operators
OPERATION_MAP: Dict[str, Operator] = {
    option.display_name: option.operator
    for option in MENU_OPTIONS
}

# Usage:
selected = "Addition"  # From questionary
operator = OPERATION_MAP[selected]  # '+'
```

---

## Entity 4: CalculationHistory

### Purpose
Manages the collection of calculation records for the current session.

### Structure

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class CalculationHistory:
    """Mutable collection of calculation records.

    Attributes:
        records: List of calculation records (chronological order)
        max_displayed: Maximum records to display in table (for performance)
    """
    records: List[CalculationRecord] = field(default_factory=list)
    max_displayed: int = 20

    def add(self, record: CalculationRecord) -> None:
        """Add a calculation record to history."""
        self.records.append(record)

    def clear(self) -> None:
        \"\"\" Clear all history records.\"\"\"
        self.records.clear()

    def get_recent(self, count: int | None = None) -> List[CalculationRecord]:
        \"\"\"Get most recent records.

        Args:
            count: Number of records to retrieve (defaults to max_displayed)

        Returns:
            List of most recent records (newest last)
        \"\"\"
        n = count if count is not None else self.max_displayed
        return self.records[-n:] if len(self.records) > n else self.records

    def count(self) -> int:
        \"\"\"Get total number of records.\"\"\"
        return len(self.records)

    def is_empty(self) -> bool:
        \"\"\"Check if history is empty.\"\"\"
        return len(self.records) == 0
```

### Usage Example

```python
from time import time

history = CalculationHistory(max_displayed=20)

# Add successful calculation
history.add(CalculationRecord(
    operand1=5.0,
    operator='+',
    operand2=3.0,
    result=8.0,
    timestamp=time()
))

# Add error calculation
history.add(CalculationRecord(
    operand1=10.0,
    operator='/',
    operand2=0.0,
    result="Error: Division by zero",
    timestamp=time()
))

# Get recent for display
recent = history.get_recent()  # Last 20
total = history.count()        # Total count

# Clear history
history.clear()
```

---

## State Transitions

### CalculationRecord State
- **Created**: When calculation is performed (immutable, no transitions)

### CalculationHistory State
1. **Empty** → **Populated**: When first calculation added
2. **Populated** → **Empty**: When `clear()` called
3. **Populated** → **Populated**: When new calculations added (growing list)

---

## Validation Summary

| Entity | Required Validations |
|--------|---------------------|
| **CalculationRecord** | operand1/operand2 are valid floats, operator is valid Operator, result is float XOR str |
| **ColorScheme** | All color values are valid Rich color strings (compile-time via type hints) |
| **MenuOption** | operator is valid Operator, display_name is non-empty string |
| **CalculationHistory** | max_displayed > 0, records list type-validated |

---

## Type Safety Compliance

All entities use:
- ✅ Type hints on all attributes
- ✅ `@dataclass` for automatic `__init__`, `__repr__`, `__eq__`
- ✅ `frozen=True` for immutable entities (CalculationRecord, ColorScheme, MenuOption)
- ✅ `Literal` types for restricted string values (Operator)
- ✅ Union types (`float | str`) for result field
- ✅ Generic types (`List[CalculationRecord]`)

Passes strict mypy with no `type: ignore` comments required.

---

## Performance Considerations

1. **CalculationHistory.get_recent()**: O(1) slice operation, efficient for 50-200 records
2. **CalculationRecord immutability**: Prevents accidental mutations, enables safe caching
3. **List-based storage**: Simple, fast append operation for adding records
4. **No database overhead**: Session-only storage (spec requirement)

---

## Integration Points

### With Existing Calculator Logic
- Reuses existing `Operator` type from `src/calculator/__init__.py`
- Compatible with existing `operations.py` functions (add, subtract, multiply, divide)
- Integrates with existing `validator.py` for input validation

### With UI Components
- `CalculationRecord` → `ui/history.py` for table rendering
- `ColorScheme` → `ui/colors.py` for consistent styling
- `MenuOption` → `ui/menu.py` for operation selection
- `CalculationHistory` → `rich_cli.py` for session state management

---

**Data Model Complete**: 2026-01-05
**Type Safety**: ✅ Full mypy compliance
**Constitution Compliance**: ✅ All principles satisfied
