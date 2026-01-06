"""
Rich Library Code Examples for Calculator Dashboard

Production-ready examples demonstrating:
1. Panel creation with borders
2. Dynamic tables for calculation history
3. Color scheme implementation
4. Dashboard layouts
5. Performance optimization

All examples are standalone and runnable.
"""

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme
from rich.live import Live
from rich.text import Text
from rich.box import ROUNDED, DOUBLE, HEAVY, SQUARE, MINIMAL, ASCII
from rich.align import Align
from rich.padding import Padding
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import time


# ==============================================================================
# EXAMPLE 1: Panel Creation with Different Border Styles
# ==============================================================================

def example_1_panels() -> None:
    """Demonstrate various panel styles and configurations."""
    console = Console()

    console.print("\n[bold cyan]Example 1: Panel Styles[/bold cyan]\n")

    # Basic panel with rounded border (default)
    panel1 = Panel(
        "Calculator Dashboard v1.0",
        title="Header",
        border_style="cyan",
        box=ROUNDED
    )
    console.print(panel1)
    console.print()

    # Panel with double border
    panel2 = Panel(
        "Current Expression: 5 + 3 = 8",
        title="Status",
        border_style="green",
        box=DOUBLE,
        padding=(1, 2)
    )
    console.print(panel2)
    console.print()

    # Panel with heavy border and subtitle
    panel3 = Panel(
        "Error: Division by zero is not allowed",
        title="Error",
        subtitle="Press any key to continue",
        border_style="red",
        box=HEAVY
    )
    console.print(panel3)
    console.print()

    # Panel with custom alignment and padding
    content = Text("CLI Calculator", style="bold cyan")
    content.append("\nVersion 1.0.0\n", style="dim")
    content.append("Ready to calculate", style="green")

    panel4 = Panel(
        Align.center(content),
        border_style="cyan",
        padding=(2, 4),
        title="[bold]Welcome[/bold]",
        title_align="center"
    )
    console.print(panel4)


# ==============================================================================
# EXAMPLE 2: Dynamic Tables for Calculation History
# ==============================================================================

def example_2_basic_table() -> None:
    """Demonstrate basic table creation with dynamic rows."""
    console = Console()

    console.print("\n[bold cyan]Example 2: Basic Dynamic Table[/bold cyan]\n")

    # Create table
    table = Table(
        title="Calculation History",
        border_style="cyan",
        header_style="bold green",
        show_lines=False,
        expand=True
    )

    # Add columns
    table.add_column("#", width=5, justify="right", style="dim")
    table.add_column("Expression", no_wrap=False)
    table.add_column("Operator", width=10, justify="center", style="yellow")
    table.add_column("Result", width=15, justify="right", style="green bold")
    table.add_column("Status", width=10, justify="center")

    # Add rows dynamically
    calculations = [
        ("5 + 3", "+", "8", "OK"),
        ("10 - 4", "-", "6", "OK"),
        ("7 * 6", "*", "42", "OK"),
        ("100 / 5", "/", "20", "OK"),
        ("10 / 0", "/", "Error", "ERROR"),
    ]

    for idx, (expr, op, result, status) in enumerate(calculations, 1):
        status_style = "green" if status == "OK" else "red bold"
        result_style = "green bold" if status == "OK" else "red"

        table.add_row(
            str(idx),
            expr,
            op,
            f"[{result_style}]{result}[/{result_style}]",
            f"[{status_style}]{status}[/{status_style}]"
        )

    console.print(table)


def example_2_alternating_rows() -> None:
    """Demonstrate table with alternating row colors."""
    console = Console()

    console.print("\n[bold cyan]Example 2b: Alternating Row Styles[/bold cyan]\n")

    table = Table(
        title="History with Alternating Rows",
        border_style="cyan",
        show_lines=False,
        row_styles=["", "dim"],  # Alternate between normal and dim
        expand=True
    )

    table.add_column("#", width=5, justify="right")
    table.add_column("Time", width=10, style="cyan")
    table.add_column("Expression", no_wrap=False)
    table.add_column("Result", width=15, justify="right", style="green bold")

    # Sample data
    for i in range(1, 11):
        table.add_row(
            str(i),
            f"12:3{i:01d}:00",
            f"{i} + {i}",
            str(i * 2)
        )

    console.print(table)


# ==============================================================================
# EXAMPLE 3: Color Scheme Implementation
# ==============================================================================

# Define custom theme
CALCULATOR_THEME = Theme({
    # Primary colors
    "primary": "cyan",
    "success": "green",
    "error": "red bold",
    "warning": "yellow",

    # UI elements
    "header": "bold cyan",
    "border": "cyan",
    "title": "bold cyan",

    # Data display
    "number": "green bold",
    "operator": "yellow",
    "result": "green bold",
    "error_msg": "red",

    # Table elements
    "table.header": "bold green",
    "table.row.even": "",
    "table.row.odd": "dim",

    # Status indicators
    "status.ok": "green",
    "status.error": "red bold",
    "status.pending": "yellow",
})


def example_3_custom_theme() -> None:
    """Demonstrate custom color theme usage."""
    console = Console(theme=CALCULATOR_THEME)

    console.print("\n[bold cyan]Example 3: Custom Color Scheme[/bold cyan]\n")

    # Using theme colors
    console.print("[header]Calculator Dashboard[/header]")
    console.print("[number]Result: 42[/number]")
    console.print("[error]Error: Division by zero[/error]")
    console.print("[operator]Operator: +[/operator]")
    console.print()

    # Panel with theme colors
    panel = Panel(
        "[header]Current Calculation[/header]\n[number]5 + 3 = 8[/number]",
        border_style="border"
    )
    console.print(panel)
    console.print()

    # Table with theme colors
    table = Table(border_style="border", header_style="table.header")
    table.add_column("Item", style="primary")
    table.add_column("Value", style="number")
    table.add_row("Expression", "5 + 3")
    table.add_row("Result", "8")
    table.add_row("Status", "[status.ok]Success[/status.ok]")

    console.print(table)


def example_3_dynamic_coloring() -> None:
    """Demonstrate dynamic color application based on values."""
    console = Console()

    console.print("\n[bold cyan]Example 3b: Dynamic Color Application[/bold cyan]\n")

    def colorize_number(value: float) -> Text:
        """Apply color based on number properties."""
        text = Text(str(value))
        if value < 0:
            text.stylize("yellow bold")
        elif value == 0:
            text.stylize("dim")
        else:
            text.stylize("green bold")
        return text

    def colorize_operator(op: str) -> Text:
        """Apply color based on operator type."""
        color_map = {
            "+": "green",
            "-": "yellow",
            "*": "cyan",
            "/": "magenta"
        }
        text = Text(op)
        text.stylize(color_map.get(op, "white"))
        return text

    # Demonstrate dynamic coloring
    numbers = [42.0, -10.5, 0.0, 3.14159]
    operators = ["+", "-", "*", "/"]

    console.print("Numbers with dynamic colors:")
    for num in numbers:
        console.print(f"  {colorize_number(num)}")

    console.print("\nOperators with dynamic colors:")
    for op in operators:
        console.print(f"  {colorize_operator(op)}")


# ==============================================================================
# EXAMPLE 4: Dashboard Layouts
# ==============================================================================

def example_4_basic_layout() -> None:
    """Demonstrate basic dashboard layout structure."""
    console = Console()

    console.print("\n[bold cyan]Example 4: Basic Dashboard Layout[/bold cyan]\n")

    # Create layout
    layout = Layout()

    # Split into header, body, footer
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )

    # Populate sections
    layout["header"].update(
        Panel(
            "[bold cyan]CLI Calculator Dashboard[/bold cyan]\n[dim]Version 1.0.0[/dim]",
            border_style="cyan"
        )
    )

    layout["body"].update(
        Panel(
            "Main content area\n" * 5,
            title="History",
            border_style="cyan"
        )
    )

    layout["footer"].update(
        Panel(
            "[dim]Commands: quit | exit | clear[/dim]",
            border_style="cyan"
        )
    )

    console.print(layout)


def example_4_complex_layout() -> None:
    """Demonstrate complex multi-section layout."""
    console = Console()

    console.print("\n[bold cyan]Example 4b: Complex Multi-Section Layout[/bold cyan]\n")

    layout = Layout()

    # Main vertical split
    layout.split_column(
        Layout(name="header", size=5),
        Layout(name="middle", size=8),
        Layout(name="main")
    )

    # Split middle section horizontally
    layout["middle"].split_row(
        Layout(name="input", ratio=2),
        Layout(name="stats", ratio=1)
    )

    # Populate all sections
    layout["header"].update(
        Panel(
            "[bold cyan]Calculator Dashboard[/bold cyan]",
            border_style="cyan"
        )
    )

    layout["input"].update(
        Panel(
            "[cyan]Current:[/cyan] 5 + 3\n[green]Result:[/green] [bold green]8[/bold green]",
            title="Input",
            border_style="green"
        )
    )

    layout["stats"].update(
        Panel(
            "Total: 42\nAverage: 10.5\nErrors: 2",
            title="Statistics",
            border_style="yellow"
        )
    )

    layout["main"].update(
        Panel(
            "Calculation history table would go here...",
            title="History",
            border_style="cyan"
        )
    )

    console.print(layout)


# ==============================================================================
# EXAMPLE 5: Performance Testing with Large Tables
# ==============================================================================

def example_5_performance_test() -> None:
    """Demonstrate performance with 50-200 rows."""
    console = Console()

    console.print("\n[bold cyan]Example 5: Performance Testing[/bold cyan]\n")

    def create_table(num_rows: int, show_lines: bool = False) -> Table:
        """Create a table with specified number of rows."""
        table = Table(
            title=f"Performance Test ({num_rows} rows)",
            border_style="cyan",
            show_lines=show_lines,
            row_styles=["", "dim"],
            expand=False
        )

        table.add_column("#", width=6, justify="right")
        table.add_column("Expression", width=20)
        table.add_column("Operator", width=10, justify="center")
        table.add_column("Result", width=12, justify="right")

        for i in range(num_rows):
            table.add_row(
                str(i + 1),
                f"{i} + {i}",
                "+",
                str(i * 2)
            )

        return table

    # Test different row counts
    test_cases = [50, 100, 200]

    for num_rows in test_cases:
        # Test without lines (faster)
        start = time.perf_counter()
        table = create_table(num_rows, show_lines=False)
        with console.capture() as capture:
            console.print(table)
        elapsed_no_lines = (time.perf_counter() - start) * 1000

        # Test with lines (slower)
        start = time.perf_counter()
        table = create_table(num_rows, show_lines=True)
        with console.capture() as capture:
            console.print(table)
        elapsed_with_lines = (time.perf_counter() - start) * 1000

        console.print(f"[cyan]{num_rows} rows:[/cyan]")
        console.print(f"  Without lines: [green]{elapsed_no_lines:.2f}ms[/green]")
        console.print(f"  With lines:    [yellow]{elapsed_with_lines:.2f}ms[/yellow]")
        console.print(f"  Speedup:       [bold]{elapsed_with_lines / elapsed_no_lines:.2f}x[/bold]")
        console.print()


def example_5_pagination() -> None:
    """Demonstrate pagination for large datasets."""
    console = Console()

    console.print("\n[bold cyan]Example 5b: Pagination Strategy[/bold cyan]\n")

    # Simulate large history
    full_history = [
        (f"Expression {i}", "+", str(i), "OK")
        for i in range(1, 101)  # 100 entries
    ]

    max_visible = 20

    table = Table(
        title=f"Recent History (showing {max_visible} of {len(full_history)})",
        border_style="cyan",
        show_lines=False,
        row_styles=["", "dim"]
    )

    table.add_column("#", width=5, justify="right", style="dim")
    table.add_column("Expression", no_wrap=False)
    table.add_column("Result", width=12, justify="right", style="green bold")

    # Show only last 20 entries
    visible_history = full_history[-max_visible:]
    start_idx = len(full_history) - len(visible_history)

    for idx, (expr, _, result, _) in enumerate(visible_history, start=start_idx + 1):
        table.add_row(str(idx), expr, result)

    console.print(table)


# ==============================================================================
# EXAMPLE 6: Complete Production Dashboard
# ==============================================================================

@dataclass
class CalculationEntry:
    """Represents a calculation entry."""
    timestamp: str
    expression: str
    operator: str
    result: str
    status: str


class ProductionDashboard:
    """Production-ready calculator dashboard."""

    def __init__(self) -> None:
        """Initialize the dashboard."""
        self.console = Console(theme=CALCULATOR_THEME)
        self.layout = self._create_layout()
        self.history: List[CalculationEntry] = []
        self.current_expression = ""
        self.current_result = ""
        self._render_static()

    def _create_layout(self) -> Layout:
        """Create layout structure."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="status", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        return layout

    def _render_static(self) -> None:
        """Render static sections (header, footer)."""
        # Header
        self.layout["header"].update(
            Panel(
                "[header]CLI Calculator Dashboard[/header]\n[dim]Python Rich Library Demo[/dim]",
                border_style="border",
                padding=(0, 2)
            )
        )

        # Footer
        self.layout["footer"].update(
            Panel(
                "[dim]Commands: [cyan]quit[/cyan] | [cyan]exit[/cyan] | [cyan]clear[/cyan][/dim]",
                border_style="border",
                padding=(0, 2)
            )
        )

    def _render_status(self) -> None:
        """Render status bar."""
        if self.current_expression:
            content = f"[primary]Expression:[/primary] {self.current_expression} [success]=[/success] [number]{self.current_result}[/number]"
        else:
            content = "[dim]No active calculation[/dim]"

        self.layout["status"].update(
            Panel(content, border_style="success", padding=(0, 2))
        )

    def _render_history(self) -> None:
        """Render history table."""
        table = Table(
            title=f"[header]History[/header] ([dim]{len(self.history)} entries[/dim])",
            border_style="border",
            header_style="table.header",
            show_lines=False,
            row_styles=["table.row.even", "table.row.odd"],
            expand=True
        )

        table.add_column("#", width=5, justify="right", style="dim")
        table.add_column("Time", width=10, style="primary")
        table.add_column("Expression", no_wrap=False)
        table.add_column("Op", width=6, justify="center", style="operator")
        table.add_column("Result", width=15, justify="right")
        table.add_column("Status", width=8, justify="center")

        # Show last 20 entries
        visible = self.history[-20:]
        start_idx = len(self.history) - len(visible)

        for idx, entry in enumerate(visible, start=start_idx + 1):
            result_style = "number" if entry.status == "OK" else "error"
            status_display = (
                f"[status.ok]{entry.status}[/status.ok]"
                if entry.status == "OK"
                else f"[status.error]{entry.status}[/status.error]"
            )

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
        """Update current calculation."""
        self.current_expression = expression
        self.current_result = result
        self._render_status()

    def add_calculation(
        self, expression: str, operator: str, result: str, status: str = "OK"
    ) -> None:
        """Add calculation to history."""
        entry = CalculationEntry(
            timestamp=datetime.now().strftime("%H:%M:%S"),
            expression=expression,
            operator=operator,
            result=result,
            status=status
        )
        self.history.append(entry)
        self._render_history()

    def render(self) -> None:
        """Render the dashboard."""
        self.console.print(self.layout)


def example_6_production_dashboard() -> None:
    """Demonstrate complete production dashboard."""
    console = Console()
    console.print("\n[bold cyan]Example 6: Production Dashboard[/bold cyan]\n")

    dashboard = ProductionDashboard()

    # Add sample calculations
    calculations = [
        ("5 + 3", "+", "8", "OK"),
        ("10 - 4", "-", "6", "OK"),
        ("7 * 6", "*", "42", "OK"),
        ("100 / 5", "/", "20", "OK"),
        ("15.5 + 2.5", "+", "18", "OK"),
        ("10 / 0", "/", "Error", "ERROR"),
    ]

    for expr, op, result, status in calculations:
        dashboard.update_current(expr, result)
        dashboard.add_calculation(expr, op, result, status)

    # Render final dashboard
    dashboard.render()


# ==============================================================================
# EXAMPLE 7: Live Dashboard with Updates
# ==============================================================================

def example_7_live_dashboard() -> None:
    """Demonstrate live-updating dashboard."""
    console = Console()
    console.print("\n[bold cyan]Example 7: Live Dashboard Updates[/bold cyan]\n")
    console.print("[dim]Watch the dashboard update in real-time...[/dim]\n")

    dashboard = ProductionDashboard()

    calculations = [
        ("5 + 3", "+", "8", "OK"),
        ("10 - 4", "-", "6", "OK"),
        ("7 * 6", "*", "42", "OK"),
        ("100 / 5", "/", "20", "OK"),
        ("10 / 0", "/", "Error", "ERROR"),
        ("15 * 3", "*", "45", "OK"),
    ]

    with Live(dashboard.layout, console=console, refresh_per_second=4) as live:
        for expr, op, result, status in calculations:
            dashboard.update_current(expr, result)
            time.sleep(0.5)
            dashboard.add_calculation(expr, op, result, status)
            time.sleep(0.5)

        # Hold final state
        time.sleep(2)


# ==============================================================================
# Main Demo Runner
# ==============================================================================

def main() -> None:
    """Run all examples."""
    console = Console()

    console.clear()
    console.print("\n[bold cyan]Rich Library Examples for Calculator Dashboard[/bold cyan]")
    console.print("[dim]Comprehensive code examples and demonstrations[/dim]\n")

    examples = [
        ("1. Panel Styles", example_1_panels),
        ("2. Basic Table", example_2_basic_table),
        ("2b. Alternating Rows", example_2_alternating_rows),
        ("3. Custom Theme", example_3_custom_theme),
        ("3b. Dynamic Coloring", example_3_dynamic_coloring),
        ("4. Basic Layout", example_4_basic_layout),
        ("4b. Complex Layout", example_4_complex_layout),
        ("5. Performance Test", example_5_performance_test),
        ("5b. Pagination", example_5_pagination),
        ("6. Production Dashboard", example_6_production_dashboard),
        ("7. Live Dashboard", example_7_live_dashboard),
    ]

    for name, func in examples:
        console.print(f"\n[bold yellow]Running Example: {name}[/bold yellow]")
        console.print("[dim]" + "=" * 60 + "[/dim]")
        func()
        console.print("\n[dim]" + "=" * 60 + "[/dim]")
        time.sleep(1)

    console.print("\n[bold green]All examples completed![/bold green]\n")


if __name__ == "__main__":
    main()
