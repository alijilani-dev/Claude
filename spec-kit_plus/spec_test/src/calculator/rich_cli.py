"""Rich-based CLI interface for the calculator."""

import time

from rich.console import Console

from calculator.models import CalculationHistory, CalculationRecord
from calculator.operations import add, divide, multiply, subtract
from calculator.ui.header import render_header
from calculator.ui.history import render_history_table
from calculator.ui.input import get_number
from calculator.ui.menu import select_operation
from calculator.ui.output import display_error, display_result

# Initialize Rich console
console = Console()


def run_rich_calculator() -> None:
    """
    Run the enhanced Rich-based calculator with interactive menu.

    This is the main entry point for the professional calculator interface
    featuring arrow-key navigation, color-coded output, and visual branding.
    """
    # Check terminal width
    if console.width < 80:
        console.print(
            "⚠️  Warning: Terminal width is less than 80 characters. "
            "Some elements may not display correctly.",
            style="yellow"
        )
        console.print()

    # Initialize calculation history
    history = CalculationHistory()

    # Display header
    console.print(render_header())
    console.print()  # Add spacing

    while True:
        # Select operation
        operation = select_operation()

        # User cancelled or selected Exit
        if operation is None:
            console.print("\n👋 Thanks for using Panaversity Calculator!", style="cyan")
            break

        # Get first number
        num1 = get_number("Enter first number: ")
        if num1 is None:
            console.print("\n👋 Thanks for using Panaversity Calculator!", style="cyan")
            break

        # Get second number (for division, don't allow zero)
        allow_zero = operation != "/"
        num2 = get_number("Enter second number: ", allow_zero=allow_zero)
        if num2 is None:
            console.print("\n👋 Thanks for using Panaversity Calculator!", style="cyan")
            break

        # Perform calculation
        result: float | str
        if operation == "+":
            result = add(num1, num2)
        elif operation == "-":
            result = subtract(num1, num2)
        elif operation == "*":
            result = multiply(num1, num2)
        elif operation == "/":
            result = divide(num1, num2)
        else:
            console.print(f"Error: Unknown operation {operation}", style="red bold")
            continue

        # Create calculation record
        record = CalculationRecord(
            operand1=num1,
            operator=operation,
            operand2=num2,
            result=result,
            timestamp=time.time()
        )

        # Add to history
        history.add(record)

        # Display result
        if isinstance(result, str):
            # Error message
            display_error(result)
        else:
            # Successful calculation
            display_result(result)

        # Display history table
        console.print()
        console.print(render_history_table(history))
        console.print()  # Add spacing between calculations
