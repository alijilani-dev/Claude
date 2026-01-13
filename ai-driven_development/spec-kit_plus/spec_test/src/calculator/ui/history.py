"""History display component for calculator UI."""

from datetime import datetime

from rich.table import Table
from rich.text import Text

from calculator.models import CalculationHistory
from calculator.ui.formatters import format_result


def render_history_table(history: CalculationHistory) -> Table:
    """
    Render calculation history as a Rich table.

    Args:
        history: CalculationHistory instance containing calculation records.

    Returns:
        Rich Table object with formatted history.
    """
    # Create table with title
    table = Table(
        title="[bold cyan]Calculation History[/bold cyan]",
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
        row_styles=["", "dim"],  # Alternating row styles
    )

    # Add columns
    table.add_column("#", justify="right", style="dim", width=4)
    table.add_column("Time", justify="left", style="cyan", width=8)
    table.add_column("Expression", justify="left", width=20)
    table.add_column("Operator", justify="center", style="yellow", width=8)
    table.add_column("Result", justify="right", width=15)
    table.add_column("Status", justify="center", width=8)

    # Get recent records (paginated to last 20)
    records = history.get_recent()

    # Add rows for each record
    for idx, record in enumerate(records, start=1):
        # Format timestamp
        dt = datetime.fromtimestamp(record.timestamp)
        time_str = dt.strftime("%H:%M:%S")

        # Format expression
        expression = f"{format_result(record.operand1)} {record.operator} {format_result(record.operand2)}"

        # Format operator
        operator_str = record.operator

        # Format result and status
        if isinstance(record.result, str):
            # Error case
            result_str = "Error"
            status = Text("ERROR", style="red bold")
        else:
            # Success case
            result_str = format_result(record.result)
            status = Text("OK", style="green bold")

        # Add row
        table.add_row(
            str(idx),
            time_str,
            expression,
            operator_str,
            result_str,
            status
        )

    return table
