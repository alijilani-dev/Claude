"""Interactive CLI interface for the calculator."""


def format_result(value: float) -> str:
    """Format a float result for display.

    Formats to 10 decimal places, then removes trailing zeros and decimal point if integer.

    Args:
        value: Float value to format

    Returns:
        Formatted string representation

    Examples:
        >>> format_result(8.0)
        '8'
        >>> format_result(5.25)
        '5.25'
        >>> format_result(3.333333333333)
        '3.3333333333'
        >>> format_result(0.1 + 0.2)
        '0.3'
    """
    formatted = f"{value:.10f}"
    formatted = formatted.rstrip("0")
    formatted = formatted.rstrip(".")
    return formatted


def display_result(result: float) -> None:
    """Display a calculation result to the user.

    Args:
        result: Float result to display

    Examples:
        >>> display_result(8.0)
        8
        >>> display_result(3.333333333333)
        3.3333333333
    """
    print(format_result(result))


def display_error(error: str) -> None:
    """Display an error message to the user.

    Args:
        error: Error message to display

    Examples:
        >>> display_error("Error: Division by zero is not allowed")
        Error: Division by zero is not allowed
    """
    print(error)


def run_calculator() -> None:
    """Run the interactive calculator REPL.

    Continuously prompts for input, parses and calculates, displays results,
    until user enters 'quit' or 'exit'.

    Returns:
        None

    Side effects:
        - Reads from stdin (input())
        - Writes to stdout (print(), display_result(), display_error())
        - Loops until exit command
    """
    from calculator.operations import add, divide, multiply, subtract
    from calculator.validator import parse_input

    print("Welcome to Calculator! Enter expressions like '5 + 3' or type 'quit' to exit.")

    while True:
        user_input = input("> ").strip()

        # Check for exit commands (case-insensitive)
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        # Parse the input
        parsed = parse_input(user_input)
        if isinstance(parsed, str):
            display_error(parsed)
            continue

        # Calculate the result based on operator
        result: float | str
        if parsed.operator == "+":
            result = add(parsed.operand1, parsed.operand2)
        elif parsed.operator == "-":
            result = subtract(parsed.operand1, parsed.operand2)
        elif parsed.operator == "*":
            result = multiply(parsed.operand1, parsed.operand2)
        elif parsed.operator == "/":
            result = divide(parsed.operand1, parsed.operand2)
        else:
            result = f"Error: Unknown operator '{parsed.operator}'"

        # Display result or error
        if isinstance(result, str):
            display_error(result)
        else:
            display_result(result)
