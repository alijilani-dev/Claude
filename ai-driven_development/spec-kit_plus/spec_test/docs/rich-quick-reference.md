# Rich Library Quick Reference for Calculator Dashboard

Quick reference guide for implementing calculator dashboard features with Python Rich library.

---

## Installation

```bash
pip install rich
```

Add to `pyproject.toml`:
```toml
[project]
dependencies = [
    "rich>=13.0.0"
]
```

---

## 1. Basic Imports

```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.theme import Theme
from rich.live import Live
from rich.text import Text
from rich.box import ROUNDED, DOUBLE, HEAVY, SQUARE
```

---

## 2. Quick Panel Examples

### Basic Header Panel
```python
from rich.panel import Panel
from rich.console import Console

console = Console()
header = Panel(
    "Calculator Dashboard",
    border_style="cyan",
    title="Header"
)
console.print(header)
```

### Panel with Custom Border
```python
from rich.box import DOUBLE

panel = Panel(
    "Content",
    box=DOUBLE,
    border_style="green",
    padding=(1, 2)  # (vertical, horizontal)
)
```

### Panel with Title and Subtitle
```python
panel = Panel(
    "Main content here",
    title="[bold cyan]Title[/bold cyan]",
    subtitle="Press Ctrl+C to exit",
    subtitle_align="right"
)
```

---

## 3. Quick Table Examples

### Basic Table
```python
from rich.table import Table

table = Table(
    title="History",
    border_style="cyan",
    show_lines=False  # Performance optimization
)

table.add_column("#", width=5, justify="right")
table.add_column("Expression", no_wrap=False)
table.add_column("Result", width=15, justify="right", style="green bold")

table.add_row("1", "5 + 3", "8")
table.add_row("2", "10 / 2", "5")

console.print(table)
```

### Table with Alternating Rows
```python
table = Table(
    row_styles=["", "dim"],  # Alternate normal and dim
    expand=True
)
```

### Performance-Optimized Table (50-200 rows)
```python
table = Table(
    show_lines=False,      # Critical for performance
    show_edge=True,
    padding=(0, 1),
    expand=True,
    row_styles=["", "dim"]
)

# Add fixed-width columns
table.add_column("#", width=6)
table.add_column("Expression", width=30, overflow="ellipsis")
table.add_column("Result", width=15)
```

---

## 4. Color Scheme Implementation

### Define Custom Theme
```python
from rich.theme import Theme
from rich.console import Console

theme = Theme({
    "header": "bold cyan",
    "success": "green bold",
    "error": "red bold",
    "number": "green bold",
    "operator": "yellow",
    "border": "cyan",
})

console = Console(theme=theme)
```

### Use Theme Colors
```python
console.print("Result: 42", style="number")
console.print("Error message", style="error")
console.print("[header]Dashboard[/header]")
```

### Dynamic Color Application
```python
from rich.text import Text

def colorize_result(value: float, is_error: bool = False) -> Text:
    text = Text(str(value))
    if is_error:
        text.stylize("red bold")
    else:
        text.stylize("green bold")
    return text
```

---

## 5. Layout Quick Reference

### Basic Layout (Header + Body + Footer)
```python
from rich.layout import Layout

layout = Layout()

layout.split_column(
    Layout(name="header", size=5),    # Fixed height
    Layout(name="body"),               # Flexible
    Layout(name="footer", size=3)     # Fixed height
)

# Update sections
layout["header"].update(Panel("Header", border_style="cyan"))
layout["body"].update(Panel("Body", border_style="cyan"))
layout["footer"].update(Panel("Footer", border_style="cyan"))

console.print(layout)
```

### Complex Layout with Horizontal Split
```python
layout = Layout()

layout.split_column(
    Layout(name="header", size=5),
    Layout(name="middle", size=10),
    Layout(name="body")
)

# Split middle horizontally
layout["middle"].split_row(
    Layout(name="left", ratio=2),
    Layout(name="right", ratio=1)
)
```

---

## 6. Live Dashboard

### Basic Live Dashboard
```python
from rich.live import Live

layout = Layout()
# ... setup layout ...

with Live(layout, console=console, refresh_per_second=4) as live:
    # Update layout sections
    layout["body"].update(new_content)
    # Updates happen automatically
```

### Dashboard Class with Live Updates
```python
class Dashboard:
    def __init__(self):
        self.layout = Layout()
        # ... setup ...

    def start_live(self):
        return Live(self.layout, refresh_per_second=4)

# Usage
dashboard = Dashboard()
with dashboard.start_live():
    dashboard.update_content()
```

---

## 7. Complete Minimal Example

```python
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

console = Console()

# Create layout
layout = Layout()
layout.split_column(
    Layout(name="header", size=5),
    Layout(name="body"),
    Layout(name="footer", size=3)
)

# Header
layout["header"].update(
    Panel("[bold cyan]Calculator Dashboard[/bold cyan]", border_style="cyan")
)

# Body (History Table)
table = Table(border_style="cyan", show_lines=False)
table.add_column("#", width=5, justify="right")
table.add_column("Expression")
table.add_column("Result", width=15, justify="right", style="green bold")
table.add_row("1", "5 + 3", "8")
table.add_row("2", "10 / 2", "5")
layout["body"].update(table)

# Footer
layout["footer"].update(
    Panel("[dim]Type 'quit' to exit[/dim]", border_style="cyan")
)

# Render
console.print(layout)
```

---

## 8. Performance Tips

### DO (Fast)
```python
# Disable show_lines
table = Table(show_lines=False)

# Fixed column widths
table.add_column("Col", width=10)

# Row-level styling
table = Table(row_styles=["", "dim"])

# Pagination (show only last 20)
visible = history[-20:]
```

### DON'T (Slow)
```python
# Enable show_lines
table = Table(show_lines=True)  # Slower

# Dynamic widths everywhere
table.add_column("Col")  # No width specified

# Per-cell styling
for row in rows:
    table.add_row(f"[red]{row[0]}[/red]", ...)  # Slower

# Render all 1000+ rows
for row in all_history:
    table.add_row(...)
```

---

## 9. Border Styles Reference

```python
from rich.box import ASCII, ROUNDED, DOUBLE, HEAVY, SQUARE, MINIMAL, SIMPLE

Panel("Content", box=ROUNDED)   # Default, rounded corners
Panel("Content", box=DOUBLE)    # Double lines
Panel("Content", box=HEAVY)     # Thick lines
Panel("Content", box=SQUARE)    # Square corners
Panel("Content", box=MINIMAL)   # Minimal border
Panel("Content", box=ASCII)     # ASCII only (+-|)
```

---

## 10. Common Patterns

### Non-Scrolling Header with Scrolling Content
```python
layout = Layout()
layout.split_column(
    Layout(name="header", size=5),  # Fixed, won't scroll
    Layout(name="content")          # Scrollable
)
```

### Status Bar
```python
status = Panel(
    f"Current: {expression} = {result}",
    border_style="green",
    padding=(0, 2)
)
```

### Error Display
```python
error = Panel(
    f"[red bold]Error:[/red bold] {error_message}",
    border_style="red"
)
```

### Paginated Table
```python
max_visible = 20
visible_entries = history[-max_visible:]
start_idx = len(history) - len(visible_entries)

for idx, entry in enumerate(visible_entries, start=start_idx + 1):
    table.add_row(str(idx), entry.data)
```

---

## 11. Calculator-Specific Patterns

### Colorize Numbers by Value
```python
def colorize_number(value: float) -> Text:
    text = Text(str(value))
    if value < 0:
        text.stylize("yellow")
    elif value == 0:
        text.stylize("dim")
    else:
        text.stylize("green bold")
    return text
```

### Colorize Operators
```python
def colorize_operator(op: str) -> Text:
    colors = {"+": "green", "-": "yellow", "*": "cyan", "/": "magenta"}
    text = Text(op)
    text.stylize(colors.get(op, "white"))
    return text
```

### Status Indicator
```python
def format_status(status: str) -> str:
    if status == "OK":
        return "[green]OK[/green]"
    else:
        return "[red bold]ERROR[/red bold]"
```

---

## 12. Typical Performance Metrics

Based on Rich library benchmarks:

| Rows | show_lines=False | show_lines=True | Speedup |
|------|------------------|-----------------|---------|
| 50   | ~5-10ms         | ~15-25ms        | 2-3x    |
| 100  | ~10-15ms        | ~30-50ms        | 3x      |
| 200  | ~15-25ms        | ~60-100ms       | 4x      |

**Recommendation**: Always use `show_lines=False` for tables with 50+ rows.

---

## 13. Integration with Existing Calculator

### Minimal Changes to cli.py

```python
# Before
def display_result(result: float) -> None:
    print(format_result(result))

# After (with Rich)
from rich.console import Console
console = Console()

def display_result(result: float) -> None:
    console.print(f"[bold green]{format_result(result)}[/bold green]")

# Before
def display_error(error: str) -> None:
    print(error)

# After (with Rich)
def display_error(error: str) -> None:
    console.print(f"[bold red]{error}[/bold red]")
```

---

## 14. Common Pitfalls

### Pitfall 1: Not Using Console Instance
```python
# Wrong
from rich import print
print("[red]Error[/red]")  # Limited features

# Correct
from rich.console import Console
console = Console()
console.print("[red]Error[/red]")  # Full features
```

### Pitfall 2: Forgetting to Disable show_lines
```python
# Slow for large tables
table = Table(show_lines=True)  # Default is False, but explicit is better

# Fast
table = Table(show_lines=False)
```

### Pitfall 3: Using Variable Width Columns
```python
# Slower (needs width calculation)
table.add_column("Name")

# Faster (fixed width)
table.add_column("Name", width=20)
```

### Pitfall 4: Not Using row_styles
```python
# Slower (per-cell styling)
for i, row in enumerate(rows):
    style = "dim" if i % 2 else ""
    table.add_row(f"[{style}]{row[0]}[/{style}]", ...)

# Faster (row-level styling)
table = Table(row_styles=["", "dim"])
for row in rows:
    table.add_row(row[0], ...)
```

---

## 15. Debugging Tips

### Print Layout Structure
```python
layout = Layout()
# ... setup ...
print(layout.tree)  # Shows layout structure
```

### Measure Render Time
```python
import time
start = time.perf_counter()
console.print(table)
elapsed = (time.perf_counter() - start) * 1000
print(f"Rendered in {elapsed:.2f}ms")
```

### Capture Output (for testing)
```python
from io import StringIO
from rich.console import Console

output = StringIO()
console = Console(file=output)
console.print("Test")
result = output.getvalue()
```

---

## 16. Resources

- **Documentation**: https://rich.readthedocs.io/
- **GitHub**: https://github.com/Textualize/rich
- **Examples**: https://github.com/Textualize/rich/tree/master/examples
- **Live Demo**: `python -m rich` (in terminal)

---

**Document Version**: 1.0
**Last Updated**: 2026-01-05
