# Python Rich Library Best Practices for Calculator Dashboard

## Research Summary
This document provides comprehensive best practices for implementing a calculator dashboard interface using the Python Rich library, focusing on panels, tables, color schemes, and layout management.

---

## 1. Panel Creation with Borders (Non-Scrolling Headers)

### Overview
Rich's `Panel` class provides bordered containers ideal for headers and sections.

### Best Practices

1. **Use Panel for Static Headers**: Panels are excellent for non-scrolling headers as they maintain fixed positioning
2. **Border Styles**: Rich offers multiple border styles (ASCII, rounded, double, heavy, etc.)
3. **Padding and Alignment**: Control internal spacing and text alignment
4. **Title Positioning**: Titles can be placed at top, bottom, left, or right

### Code Example: Header Panel

```python
from rich.panel import Panel
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

# Basic header panel with border
def create_header_panel() -> Panel:
    """Create a calculator header panel with custom styling."""
    header_text = Text("CLI Calculator Dashboard", style="bold cyan")
    header_text.append("\nVersion 1.0.0", style="dim")

    return Panel(
        Align.center(header_text),
        border_style="cyan",
        padding=(1, 2),  # (vertical, horizontal)
        title="[bold]Calculator[/bold]",
        title_align="left",
        subtitle="Press Ctrl+C to exit",
        subtitle_align="right"
    )

# Usage
console.print(create_header_panel())
```

### Border Style Options

```python
from rich.box import (
    ASCII,          # Simple ASCII characters
    ROUNDED,        # Rounded corners (default)
    DOUBLE,         # Double-line border
    HEAVY,          # Heavy/thick border
    SQUARE,         # Square corners
    MINIMAL,        # Minimal border
    SIMPLE,         # Simple single line
)

# Example with different box styles
Panel("Content", box=ROUNDED, border_style="cyan")
Panel("Content", box=DOUBLE, border_style="green")
Panel("Content", box=HEAVY, border_style="red")
```

### Advanced Panel Configuration

```python
from rich.panel import Panel
from rich.box import DOUBLE
from rich.padding import Padding

def create_status_panel(current_expression: str = "", result: str = "") -> Panel:
    """Create a status panel showing current calculation state."""
    content = f"Expression: {current_expression or 'None'}\nResult: {result or 'N/A'}"

    return Panel(
        Padding(content, (0, 1)),
        title="[bold cyan]Current Calculation[/bold cyan]",
        border_style="cyan",
        box=DOUBLE,
        expand=False,  # Don't expand to full width
        width=60
    )
```

---

## 2. Dynamic Tables for Calculation History

### Overview
Rich's `Table` class provides powerful features for rendering tabular data with styling and dynamic row addition.

### Best Practices

1. **Pre-allocate Columns**: Define columns before adding rows for better performance
2. **Use Row Styles**: Alternate row colors for better readability
3. **Column Alignment**: Align numeric data right, text left
4. **Performance**: For 50-200 rows, Rich handles rendering efficiently (~10-20ms)
5. **Overflow Handling**: Use `overflow="fold"` or `overflow="ellipsis"` for long content

### Code Example: History Table

```python
from rich.table import Table
from rich.console import Console
from typing import List, Tuple

console = Console()

def create_history_table(
    history: List[Tuple[str, str, str, str, str]]  # (timestamp, expr, op, result, status)
) -> Table:
    """Create a styled history table with dynamic rows.

    Args:
        history: List of tuples containing (timestamp, expression, operator, result, status)

    Returns:
        Rich Table object ready for rendering
    """
    table = Table(
        title="[bold cyan]Calculation History[/bold cyan]",
        border_style="cyan",
        header_style="bold green",
        show_lines=False,  # No lines between rows for better performance
        expand=True,       # Expand to full console width
        row_styles=["", "dim"]  # Alternate row styling
    )

    # Define columns with alignment and styling
    table.add_column("#", justify="right", style="dim", width=5)
    table.add_column("Time", justify="left", style="cyan", width=12)
    table.add_column("Expression", justify="left", style="white", no_wrap=False)
    table.add_column("Operator", justify="center", style="yellow", width=10)
    table.add_column("Result", justify="right", style="green bold", width=15)
    table.add_column("Status", justify="center", style="green", width=10)

    # Add rows dynamically
    for idx, (timestamp, expr, op, result, status) in enumerate(history, 1):
        # Color-code status
        status_style = "green" if status == "OK" else "red bold"
        result_style = "green bold" if status == "OK" else "red"

        table.add_row(
            str(idx),
            timestamp,
            expr,
            op,
            result,
            f"[{status_style}]{status}[/{status_style}]"
        )

    return table

# Example usage
sample_history = [
    ("12:34:56", "5 + 3", "+", "8", "OK"),
    ("12:35:10", "10 / 2", "/", "5", "OK"),
    ("12:35:25", "7 * 6", "*", "42", "OK"),
    ("12:35:40", "10 / 0", "/", "Error", "ERROR"),
]

console.print(create_history_table(sample_history))
```

### Performance Optimization for Large Tables

```python
from rich.table import Table
from rich.console import Console

def create_optimized_large_table(rows: int = 200) -> Table:
    """Create a table optimized for 50-200 rows.

    Performance tips:
    - Disable show_lines for faster rendering
    - Use fixed column widths when possible
    - Minimize rich markup in cells
    - Use row_styles instead of per-cell styling
    """
    table = Table(
        show_header=True,
        show_lines=False,      # Critical for performance
        show_edge=True,
        show_footer=False,
        pad_edge=True,
        collapse_padding=False,
        padding=(0, 1),        # Minimal padding
        expand=True,
        border_style="cyan",
        row_styles=["", "on #1a1a1a"]  # Subtle alternating background
    )

    # Fixed-width columns for better performance
    table.add_column("#", width=6, justify="right")
    table.add_column("Expression", width=30, overflow="ellipsis")
    table.add_column("Result", width=15, justify="right")

    # Add rows (simulated)
    for i in range(1, rows + 1):
        table.add_row(
            str(i),
            f"Expression {i}",
            str(i * 2)
        )

    return table

# Performance test
import time
console = Console()

start = time.perf_counter()
table = create_optimized_large_table(200)
console.print(table)
elapsed = (time.perf_counter() - start) * 1000
print(f"\nRendered 200 rows in {elapsed:.2f}ms")
```

### Table with Scrolling Support

```python
from rich.console import Console
from rich.table import Table

def create_scrollable_history(
    history: List[dict],
    max_visible: int = 20
) -> Table:
    """Create a table showing only the most recent entries.

    Args:
        history: Full history list
        max_visible: Maximum rows to display
    """
    table = Table(
        title=f"[cyan]Recent History[/cyan] (showing {min(len(history), max_visible)} of {len(history)})",
        border_style="cyan"
    )

    table.add_column("#", width=5, justify="right")
    table.add_column("Expression", no_wrap=False)
    table.add_column("Result", width=15, justify="right")

    # Show only most recent entries
    visible_history = history[-max_visible:]
    start_idx = len(history) - len(visible_history)

    for idx, entry in enumerate(visible_history, start=start_idx + 1):
        table.add_row(
            str(idx),
            entry["expression"],
            entry["result"]
        )

    return table
```

---

## 3. Color Theme Management and Custom Color Schemes

### Overview
Rich supports comprehensive color management through styles, themes, and custom color schemes.

### Best Practices

1. **Use Named Styles**: Create reusable style definitions
2. **Color Consistency**: Maintain consistent color palette across the dashboard
3. **Accessibility**: Ensure sufficient contrast for readability
4. **Theme Objects**: Use Theme class for centralized color management

### Code Example: Custom Color Scheme

```python
from rich.theme import Theme
from rich.console import Console
from rich.style import Style

# Define calculator color scheme (cyan, green, red)
calculator_theme = Theme({
    # Primary colors
    "primary": "cyan",
    "success": "green",
    "error": "red bold",
    "warning": "yellow",

    # UI elements
    "header": "bold cyan",
    "border": "cyan",
    "title": "bold cyan",
    "subtitle": "dim cyan",

    # Data display
    "number": "green bold",
    "operator": "yellow",
    "result": "green bold",
    "error_msg": "red",

    # Table elements
    "table.header": "bold green on #1a1a1a",
    "table.row.even": "",
    "table.row.odd": "dim",
    "table.footer": "cyan",

    # Status indicators
    "status.ok": "green",
    "status.error": "red bold",
    "status.pending": "yellow",

    # Text styles
    "text.normal": "white",
    "text.dim": "dim white",
    "text.bold": "bold white",
    "text.highlight": "bold cyan",
})

# Create console with custom theme
console = Console(theme=calculator_theme)

# Usage examples
console.print("Calculator Dashboard", style="header")
console.print("Result: 42", style="result")
console.print("Error: Division by zero", style="error")
console.print("[status.ok]Success[/status.ok] - Calculation complete")
```

### Custom Style Classes

```python
from rich.style import Style
from typing import Dict

class CalculatorStyles:
    """Centralized style definitions for calculator dashboard."""

    # Color palette
    CYAN = "#00d7ff"
    GREEN = "#00ff87"
    RED = "#ff5555"
    YELLOW = "#ffff87"
    DIM_WHITE = "#808080"

    # Styles dictionary
    STYLES: Dict[str, Style] = {
        "header": Style(color=CYAN, bold=True),
        "success": Style(color=GREEN, bold=True),
        "error": Style(color=RED, bold=True),
        "operator": Style(color=YELLOW),
        "number": Style(color=GREEN, bold=True),
        "dim": Style(color=DIM_WHITE),
        "border": Style(color=CYAN),
    }

    @classmethod
    def get_style(cls, name: str) -> Style:
        """Get a style by name."""
        return cls.STYLES.get(name, Style())

# Usage
from rich.console import Console
from rich.panel import Panel

console = Console()
header = Panel(
    "Calculator Dashboard",
    border_style=CalculatorStyles.get_style("border"),
    title_align="center"
)
console.print(header)
console.print("42", style=CalculatorStyles.get_style("number"))
```

### Dynamic Color Application

```python
from rich.console import Console
from rich.text import Text

def colorize_result(value: float, error: bool = False) -> Text:
    """Apply color to result based on status.

    Args:
        value: The numeric result
        error: Whether this is an error result

    Returns:
        Rich Text object with appropriate styling
    """
    text = Text(str(value))

    if error:
        text.stylize("red bold")
    elif value < 0:
        text.stylize("yellow bold")
    else:
        text.stylize("green bold")

    return text

def colorize_operator(op: str) -> Text:
    """Apply color to operator symbol."""
    color_map = {
        "+": "green",
        "-": "yellow",
        "*": "cyan",
        "/": "magenta"
    }

    text = Text(op)
    text.stylize(color_map.get(op, "white"))
    return text

# Example usage
console = Console()
console.print(colorize_result(42.0))
console.print(colorize_result(-10.5))
console.print(colorize_operator("+"))
```

---

## 4. Dashboard Layout Strategy

### Overview
Rich provides the `Layout` class for creating complex dashboard layouts with headers, content areas, and sidebars.

### Best Practices

1. **Split Hierarchically**: Use `split_row()` and `split_column()` for organized layouts
2. **Fixed vs. Flexible**: Set `size` for fixed-height headers, leave flexible for content
3. **Named Regions**: Use names for easy updates
4. **Live Updates**: Combine with `Live` for real-time updates

### Code Example: Complete Dashboard Layout

```python
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from rich.live import Live
import time

def create_calculator_dashboard() -> Layout:
    """Create a complete calculator dashboard layout.

    Layout structure:
    +----------------------------------+
    |           Header (fixed)         |
    +----------------------------------+
    |           Status Bar             |
    +----------------------------------+
    |                                  |
    |       History Table (flex)       |
    |                                  |
    +----------------------------------+
    |           Footer (fixed)         |
    +----------------------------------+
    """
    layout = Layout()

    # Split into header, body, footer
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="status", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )

    return layout

def update_dashboard_header(layout: Layout) -> None:
    """Update the header section."""
    header = Panel(
        "[bold cyan]CLI Calculator Dashboard[/bold cyan]\n[dim]Interactive mode active[/dim]",
        border_style="cyan",
        padding=(0, 2)
    )
    layout["header"].update(header)

def update_dashboard_status(layout: Layout, expression: str = "", result: str = "") -> None:
    """Update the status bar section."""
    status = Panel(
        f"[cyan]Current:[/cyan] {expression or 'None'} [green]=[/green] [bold green]{result or 'N/A'}[/bold green]",
        border_style="green",
        padding=(0, 2)
    )
    layout["status"].update(status)

def update_dashboard_body(layout: Layout, history: list) -> None:
    """Update the main body with history table."""
    table = Table(
        title="[bold cyan]Calculation History[/bold cyan]",
        border_style="cyan",
        show_lines=False,
        row_styles=["", "dim"]
    )

    table.add_column("#", width=5, justify="right", style="dim")
    table.add_column("Expression", no_wrap=False)
    table.add_column("Operator", width=10, justify="center", style="yellow")
    table.add_column("Result", width=15, justify="right", style="green bold")

    for idx, entry in enumerate(history, 1):
        table.add_row(
            str(idx),
            entry["expression"],
            entry["operator"],
            entry["result"]
        )

    layout["body"].update(table)

def update_dashboard_footer(layout: Layout) -> None:
    """Update the footer section."""
    footer = Panel(
        "[dim]Commands: [cyan]quit[/cyan] | [cyan]exit[/cyan] | [cyan]clear[/cyan] | Enter expression[/dim]",
        border_style="cyan",
        padding=(0, 2)
    )
    layout["footer"].update(footer)

# Example: Static dashboard rendering
console = Console()
layout = create_calculator_dashboard()
update_dashboard_header(layout)
update_dashboard_status(layout, "5 + 3", "8")
update_dashboard_body(layout, [
    {"expression": "5 + 3", "operator": "+", "result": "8"},
    {"expression": "10 / 2", "operator": "/", "result": "5"},
])
update_dashboard_footer(layout)

console.print(layout)
```

### Live Dashboard with Real-Time Updates

```python
from rich.live import Live
from rich.layout import Layout
from rich.console import Console
import time
from typing import List, Dict

class CalculatorDashboard:
    """Live-updating calculator dashboard."""

    def __init__(self) -> None:
        """Initialize the dashboard."""
        self.layout = Layout()
        self.history: List[Dict[str, str]] = []
        self.current_expression = ""
        self.current_result = ""

        # Setup layout structure
        self.layout.split_column(
            Layout(name="header", size=5),
            Layout(name="status", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )

        self._render_all()

    def _render_all(self) -> None:
        """Render all dashboard sections."""
        self._render_header()
        self._render_status()
        self._render_body()
        self._render_footer()

    def _render_header(self) -> None:
        """Render header section."""
        header = Panel(
            "[bold cyan]CLI Calculator Dashboard[/bold cyan]\n[dim]Version 1.0.0[/dim]",
            border_style="cyan",
            padding=(0, 2)
        )
        self.layout["header"].update(header)

    def _render_status(self) -> None:
        """Render status bar."""
        status = Panel(
            f"[cyan]Expression:[/cyan] {self.current_expression or 'None'} [green]=[/green] [bold green]{self.current_result or 'N/A'}[/bold green]",
            border_style="green",
            padding=(0, 1)
        )
        self.layout["status"].update(status)

    def _render_body(self) -> None:
        """Render history table."""
        table = Table(
            title=f"[bold cyan]History[/bold cyan] ({len(self.history)} entries)",
            border_style="cyan",
            show_lines=False,
            row_styles=["", "dim"],
            expand=True
        )

        table.add_column("#", width=5, justify="right", style="dim")
        table.add_column("Expression", no_wrap=False)
        table.add_column("Op", width=8, justify="center", style="yellow")
        table.add_column("Result", width=15, justify="right", style="green bold")
        table.add_column("Status", width=10, justify="center")

        # Show last 20 entries
        visible_history = self.history[-20:]
        start_idx = len(self.history) - len(visible_history)

        for idx, entry in enumerate(visible_history, start=start_idx + 1):
            status_style = "green" if entry["status"] == "OK" else "red bold"
            table.add_row(
                str(idx),
                entry["expression"],
                entry["operator"],
                entry["result"],
                f"[{status_style}]{entry['status']}[/{status_style}]"
            )

        self.layout["body"].update(table)

    def _render_footer(self) -> None:
        """Render footer."""
        footer = Panel(
            f"[dim]Total calculations: {len(self.history)} | Commands: [cyan]quit[/cyan] [cyan]exit[/cyan] [cyan]clear[/cyan][/dim]",
            border_style="cyan",
            padding=(0, 2)
        )
        self.layout["footer"].update(footer)

    def set_current_calculation(self, expression: str, result: str) -> None:
        """Update current calculation display."""
        self.current_expression = expression
        self.current_result = result
        self._render_status()

    def add_to_history(self, expression: str, operator: str, result: str, status: str = "OK") -> None:
        """Add entry to history."""
        self.history.append({
            "expression": expression,
            "operator": operator,
            "result": result,
            "status": status
        })
        self._render_body()
        self._render_footer()

    def clear_history(self) -> None:
        """Clear all history."""
        self.history.clear()
        self._render_body()
        self._render_footer()

# Example usage with Live
def demo_live_dashboard() -> None:
    """Demonstrate live dashboard updates."""
    console = Console()
    dashboard = CalculatorDashboard()

    with Live(dashboard.layout, console=console, refresh_per_second=4) as live:
        # Simulate calculations
        calculations = [
            ("5 + 3", "+", "8", "OK"),
            ("10 - 4", "-", "6", "OK"),
            ("7 * 6", "*", "42", "OK"),
            ("100 / 5", "/", "20", "OK"),
            ("10 / 0", "/", "Error", "ERROR"),
        ]

        for expr, op, result, status in calculations:
            dashboard.set_current_calculation(expr, result)
            time.sleep(0.5)
            dashboard.add_to_history(expr, op, result, status)
            time.sleep(0.5)

# Run demo
# demo_live_dashboard()
```

### Complex Multi-Panel Layout

```python
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console

def create_advanced_layout() -> Layout:
    """Create advanced dashboard with multiple sections.

    Layout:
    +------------------------------------------+
    |              Header (fixed)              |
    +------------------------------------------+
    |  Input Panel    |    Stats Panel         |
    |  (left)         |    (right)             |
    +------------------------------------------+
    |                                          |
    |         History Table (main)             |
    |                                          |
    +------------------------------------------+
    """
    layout = Layout()

    # Main vertical split
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="middle", size=10),
        Layout(name="main")
    )

    # Split middle section horizontally
    layout["middle"].split_row(
        Layout(name="input", ratio=2),
        Layout(name="stats", ratio=1)
    )

    # Populate sections
    layout["header"].update(Panel("[bold cyan]Calculator Dashboard[/bold cyan]", border_style="cyan"))
    layout["input"].update(Panel("Current: 5 + 3 = 8", title="Input", border_style="green"))
    layout["stats"].update(Panel("Total: 42\nAvg: 10.5", title="Statistics", border_style="yellow"))
    layout["main"].update(Panel("History table here...", title="History", border_style="cyan"))

    return layout

console = Console()
console.print(create_advanced_layout())
```

---

## 5. Performance Considerations

### Key Performance Metrics

Based on Rich library performance characteristics:

- **50 rows**: ~5-10ms render time
- **100 rows**: ~10-15ms render time
- **200 rows**: ~15-25ms render time

### Optimization Techniques

```python
from rich.table import Table
from rich.console import Console
import time

def benchmark_table_rendering(num_rows: int) -> float:
    """Benchmark table rendering performance.

    Args:
        num_rows: Number of rows to render

    Returns:
        Elapsed time in milliseconds
    """
    console = Console()

    # Create optimized table
    table = Table(
        show_lines=False,      # Disable for performance
        show_edge=True,
        padding=(0, 1),
        expand=False,
        border_style="cyan"
    )

    table.add_column("#", width=6)
    table.add_column("Expression", width=30)
    table.add_column("Result", width=15)

    # Add rows
    for i in range(num_rows):
        table.add_row(str(i), f"{i} + {i}", str(i * 2))

    # Measure rendering time
    start = time.perf_counter()
    console.print(table)
    elapsed = (time.perf_counter() - start) * 1000

    return elapsed

# Performance tests
for rows in [50, 100, 200]:
    elapsed = benchmark_table_rendering(rows)
    print(f"{rows} rows: {elapsed:.2f}ms")
```

### Performance Best Practices

1. **Disable `show_lines`**: Significantly improves rendering speed
2. **Use Fixed Widths**: Avoid dynamic width calculation
3. **Minimize Markup**: Reduce rich markup in cells
4. **Row Styles Over Cell Styles**: Use row-level styling instead of per-cell
5. **Pagination**: Show only visible rows (e.g., last 20 entries)
6. **Batch Updates**: Update layout once after multiple changes

```python
# Good: Batch updates
dashboard.set_expression("5 + 3")
dashboard.set_result("8")
dashboard.add_history("5 + 3", "8")
dashboard.render()  # Single render call

# Bad: Multiple renders
dashboard.set_expression("5 + 3")
dashboard.render()
dashboard.set_result("8")
dashboard.render()
dashboard.add_history("5 + 3", "8")
dashboard.render()
```

---

## 6. Complete Example: Production-Ready Dashboard

```python
"""
Production-ready calculator dashboard implementation.
Demonstrates all best practices in a cohesive example.
"""

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme
from rich.live import Live
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

# Custom theme
CALCULATOR_THEME = Theme({
    "header": "bold cyan",
    "success": "green bold",
    "error": "red bold",
    "operator": "yellow",
    "number": "green bold",
    "border": "cyan",
    "status.ok": "green",
    "status.error": "red bold",
})


@dataclass
class CalculationEntry:
    """Represents a single calculation entry."""
    timestamp: str
    expression: str
    operator: str
    result: str
    status: str  # "OK" or "ERROR"


class CalculatorDashboardUI:
    """Production calculator dashboard with Rich library.

    Features:
    - Fixed header with app info
    - Status bar showing current calculation
    - Scrollable history table (last 20 entries)
    - Footer with commands
    - Custom color scheme (cyan/green/red)
    - Performance optimized for 50-200 rows
    """

    def __init__(self, console: Optional[Console] = None) -> None:
        """Initialize the dashboard.

        Args:
            console: Rich Console instance (creates new if None)
        """
        self.console = console or Console(theme=CALCULATOR_THEME)
        self.layout = self._create_layout()
        self.history: List[CalculationEntry] = []
        self.current_expression = ""
        self.current_result = ""

        self._render_static_sections()

    def _create_layout(self) -> Layout:
        """Create the dashboard layout structure."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="status", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        return layout

    def _render_static_sections(self) -> None:
        """Render header and footer (static content)."""
        # Header
        header = Panel(
            "[header]CLI Calculator Dashboard[/header]\n[dim cyan]Version 1.0.0 | Python Rich Library[/dim cyan]",
            border_style="border",
            padding=(0, 2)
        )
        self.layout["header"].update(header)

        # Footer
        footer = Panel(
            "[dim]Commands: [cyan]quit[/cyan] | [cyan]exit[/cyan] | [cyan]clear[/cyan] | Enter expression (e.g., '5 + 3')[/dim]",
            border_style="border",
            padding=(0, 2)
        )
        self.layout["footer"].update(footer)

    def _render_status(self) -> None:
        """Render the status bar with current calculation."""
        if self.current_expression:
            content = f"[cyan]Input:[/cyan] {self.current_expression} [green]=[/green] [number]{self.current_result}[/number]"
        else:
            content = "[dim]No active calculation[/dim]"

        status = Panel(
            content,
            border_style="success" if self.current_result else "border",
            padding=(0, 2)
        )
        self.layout["status"].update(status)

    def _render_history(self) -> None:
        """Render the history table (optimized for 50-200 rows)."""
        table = Table(
            title=f"[header]Calculation History[/header] ([dim]{len(self.history)} total[/dim])",
            border_style="border",
            header_style="bold green",
            show_lines=False,  # Performance optimization
            row_styles=["", "dim"],  # Alternating rows
            expand=True,
            padding=(0, 1)
        )

        # Column definitions
        table.add_column("#", width=5, justify="right", style="dim")
        table.add_column("Time", width=10, justify="left", style="cyan")
        table.add_column("Expression", no_wrap=False)
        table.add_column("Op", width=6, justify="center", style="operator")
        table.add_column("Result", width=15, justify="right")
        table.add_column("Status", width=8, justify="center")

        # Show last 20 entries only (pagination for performance)
        visible_entries = self.history[-20:] if len(self.history) > 20 else self.history
        start_index = len(self.history) - len(visible_entries)

        for idx, entry in enumerate(visible_entries, start=start_index + 1):
            # Color-code based on status
            result_style = "number" if entry.status == "OK" else "error"
            status_display = f"[status.ok]{entry.status}[/status.ok]" if entry.status == "OK" else f"[status.error]{entry.status}[/status.error]"

            table.add_row(
                str(idx),
                entry.timestamp,
                entry.expression,
                entry.operator,
                f"[{result_style}]{entry.result}[/{result_style}]",
                status_display
            )

        self.layout["body"].update(table)

    def update_current(self, expression: str, result: str) -> None:
        """Update the current calculation display.

        Args:
            expression: The calculation expression
            result: The result value
        """
        self.current_expression = expression
        self.current_result = result
        self._render_status()

    def add_calculation(
        self,
        expression: str,
        operator: str,
        result: str,
        status: str = "OK"
    ) -> None:
        """Add a calculation to history.

        Args:
            expression: Full expression (e.g., "5 + 3")
            operator: The operator used (+, -, *, /)
            result: The result or error message
            status: "OK" or "ERROR"
        """
        entry = CalculationEntry(
            timestamp=datetime.now().strftime("%H:%M:%S"),
            expression=expression,
            operator=operator,
            result=result,
            status=status
        )
        self.history.append(entry)
        self._render_history()

    def clear_history(self) -> None:
        """Clear all calculation history."""
        self.history.clear()
        self.current_expression = ""
        self.current_result = ""
        self._render_status()
        self._render_history()

    def render(self) -> None:
        """Render the complete dashboard (one-time)."""
        self.console.print(self.layout)

    def start_live(self) -> Live:
        """Start live-updating dashboard.

        Returns:
            Rich Live context manager
        """
        return Live(self.layout, console=self.console, refresh_per_second=4)


# Example usage
def demo() -> None:
    """Demonstrate the calculator dashboard."""
    console = Console()
    dashboard = CalculatorDashboardUI(console)

    # Add some sample calculations
    dashboard.update_current("5 + 3", "8")
    dashboard.add_calculation("5 + 3", "+", "8", "OK")

    dashboard.update_current("10 / 2", "5")
    dashboard.add_calculation("10 / 2", "/", "5", "OK")

    dashboard.update_current("7 * 6", "42")
    dashboard.add_calculation("7 * 6", "*", "42", "OK")

    dashboard.update_current("10 / 0", "Error: Division by zero")
    dashboard.add_calculation("10 / 0", "/", "Error", "ERROR")

    # Render dashboard
    dashboard.render()


if __name__ == "__main__":
    demo()
```

---

## 7. Integration with Existing Calculator

### Minimal Changes Required

```python
# In src/calculator/cli.py

from rich.console import Console
from rich.panel import Panel

console = Console()

def display_result(result: float) -> None:
    """Display result using Rich."""
    console.print(f"[bold green]{format_result(result)}[/bold green]")

def display_error(error: str) -> None:
    """Display error using Rich."""
    console.print(f"[bold red]{error}[/bold red]")

def run_calculator() -> None:
    """Enhanced calculator with Rich UI."""
    # Add header
    header = Panel(
        "[bold cyan]Calculator[/bold cyan]\nEnter expressions or 'quit' to exit",
        border_style="cyan"
    )
    console.print(header)

    # Rest of existing logic...
```

---

## Summary of Best Practices

### Panels
- Use for headers, status bars, and section containers
- Choose appropriate border styles (ROUNDED, DOUBLE, HEAVY)
- Set fixed `size` for non-scrolling sections
- Use `padding` for internal spacing

### Tables
- Disable `show_lines` for better performance
- Use `row_styles` for alternating colors
- Set fixed column widths when possible
- Paginate large datasets (show last 20-50 rows)
- Align numbers right, text left

### Color Schemes
- Define a Theme object for consistency
- Use semantic color names (success, error, warning)
- Maintain cyan/green/red palette for calculator
- Ensure sufficient contrast for readability

### Layouts
- Split hierarchically with `split_column()` and `split_row()`
- Use named regions for easy updates
- Set fixed sizes for headers/footers
- Use `Live` for real-time updates

### Performance
- For 50-200 rows, expect 10-25ms render time
- Minimize rich markup in cells
- Batch layout updates
- Use pagination for large datasets

---

## Dependencies

To use Rich library, add to `pyproject.toml`:

```toml
[project]
dependencies = [
    "rich>=13.0.0"
]
```

Install with:
```bash
pip install rich
```

---

## References

- Rich Documentation: https://rich.readthedocs.io/
- GitHub: https://github.com/Textualize/rich
- PyPI: https://pypi.org/project/rich/

---

**Document Version**: 1.0
**Last Updated**: 2026-01-05
**Author**: Research for CLI Calculator Dashboard Implementation
