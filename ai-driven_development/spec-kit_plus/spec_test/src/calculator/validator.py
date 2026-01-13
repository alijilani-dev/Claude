"""Input validation and parsing for the calculator."""

from dataclasses import dataclass

from calculator import Operator


@dataclass(frozen=True)
class ParsedInput:
    """Represents a validated and parsed calculation input.

    Attributes:
        operand1: First numeric operand
        operator: Arithmetic operator (+, -, *, /)
        operand2: Second numeric operand
    """

    operand1: float
    operator: Operator
    operand2: float


def parse_number(num_str: str) -> float | str:
    """Parse a string into a float number.

    Args:
        num_str: String representation of a number

    Returns:
        Parsed float value, or error message if invalid

    Examples:
        >>> parse_number("5")
        5.0
        >>> parse_number("-3.14")
        -3.14
        >>> parse_number("abc")
        'Error: Invalid input - please enter valid numbers'
        >>> parse_number("")
        'Error: Invalid input - please enter valid numbers'
    """
    try:
        return float(num_str)
    except ValueError:
        return "Error: Invalid input - please enter valid numbers"


def validate_operator(op: str) -> Operator | str:
    """Validate an operator string.

    Args:
        op: String to validate as operator

    Returns:
        Validated Operator literal, or error message if invalid

    Examples:
        >>> validate_operator("+")
        '+'
        >>> validate_operator("*")
        '*'
        >>> validate_operator("$")
        'Error: Invalid operator - use +, -, *, or /'
        >>> validate_operator("add")
        'Error: Invalid operator - use +, -, *, or /'
    """
    if op in ("+", "-", "*", "/"):
        return op  # type: ignore[return-value]
    return "Error: Invalid operator - use +, -, *, or /"


def parse_input(user_input: str) -> ParsedInput | str:
    """Parse user input into validated components.

    Args:
        user_input: Raw user input string (e.g., "5 + 3")

    Returns:
        ParsedInput with validated operands and operator, or error message

    Examples:
        >>> parse_input("5 + 3")
        ParsedInput(operand1=5.0, operator='+', operand2=3.0)
        >>> parse_input("-6 * -7")
        ParsedInput(operand1=-6.0, operator='*', operand2=-7.0)
        >>> parse_input("abc + 5")
        'Error: Invalid input - please enter valid numbers'
        >>> parse_input("5 $ 3")
        'Error: Invalid operator - use +, -, *, or /'
        >>> parse_input("5 +")
        'Error: Please provide two numbers and an operator'
    """
    tokens = user_input.split()
    if len(tokens) != 3:
        return "Error: Please provide two numbers and an operator"

    num1_result = parse_number(tokens[0])
    if isinstance(num1_result, str):
        return num1_result

    op_result = validate_operator(tokens[1])
    # Check if it's an error message (starts with "Error:")
    if isinstance(op_result, str) and op_result.startswith("Error:"):
        return op_result

    num2_result = parse_number(tokens[2])
    if isinstance(num2_result, str):
        return num2_result

    return ParsedInput(operand1=num1_result, operator=op_result, operand2=num2_result)
