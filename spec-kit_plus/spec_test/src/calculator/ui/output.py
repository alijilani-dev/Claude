"""Output display components for calculator UI."""

from rich.console import Console

from calculator.ui.formatters import format_result

# Shared console instance
console = Console()


def display_result(result: float) -> None:
    """
    Display a successful calculation result with green styling.

    Args:
        result: The calculation result to display.
    """
    formatted = format_result(result)
    console.print(f"\nResult: {formatted}", style="green bold")


def display_error(error_message: str) -> None:
    """
    Display an error message with red styling.

    Args:
        error_message: The error message to display. Should include "Error:" prefix
                      if not already present.
    """
    # Ensure the message is displayed prominently
    console.print(f"\n{error_message}", style="red bold")
