"""Core arithmetic operations for the calculator."""


def add(a: float, b: float) -> float:
    """Add two numbers.

    Args:
        a: First operand
        b: Second operand

    Returns:
        Sum of a and b

    Examples:
        >>> add(5.0, 3.0)
        8.0
        >>> add(-5.0, 3.0)
        -2.0
        >>> add(0.1, 0.2)
        0.30000000000000004
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a.

    Args:
        a: First operand (minuend)
        b: Second operand (subtrahend)

    Returns:
        Difference of a and b (a - b)

    Examples:
        >>> subtract(10.0, 4.0)
        6.0
        >>> subtract(5.0, 10.0)
        -5.0
        >>> subtract(-6.0, -7.0)
        1.0
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a: First operand
        b: Second operand

    Returns:
        Product of a and b

    Examples:
        >>> multiply(6.0, 7.0)
        42.0
        >>> multiply(-6.0, -7.0)
        42.0
        >>> multiply(7.5, 2.0)
        15.0
    """
    return a * b


def divide(a: float, b: float) -> float | str:
    """Divide a by b.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Quotient of a / b, or error message if b is zero

    Examples:
        >>> divide(20.0, 4.0)
        5.0
        >>> divide(10.0, 3.0)
        3.3333333333333335
        >>> divide(10.0, 0.0)
        'Error: Division by zero is not allowed'
        >>> divide(-20.0, 4.0)
        -5.0
    """
    if b == 0:
        return "Error: Division by zero is not allowed"
    return a / b
