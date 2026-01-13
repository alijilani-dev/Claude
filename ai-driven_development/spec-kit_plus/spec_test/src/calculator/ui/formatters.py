"""Result formatting utilities for the calculator UI."""


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
