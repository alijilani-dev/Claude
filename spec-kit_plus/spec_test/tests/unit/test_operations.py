"""Unit tests for arithmetic operations."""

import pytest

from calculator.operations import add, divide, multiply, subtract


class TestAdd:
    """Tests for the add function."""

    def test_add_integers(self) -> None:
        """Test adding two positive integers."""
        assert add(5.0, 3.0) == 8.0
        assert add(10.0, 20.0) == 30.0
        assert add(0.0, 0.0) == 0.0

    def test_add_with_zero(self) -> None:
        """Test adding zero."""
        assert add(5.0, 0.0) == 5.0
        assert add(0.0, 5.0) == 5.0


class TestSubtract:
    """Tests for the subtract function."""

    def test_subtract_integers(self) -> None:
        """Test subtracting two positive integers."""
        assert subtract(10.0, 4.0) == 6.0
        assert subtract(20.0, 5.0) == 15.0
        assert subtract(5.0, 5.0) == 0.0

    def test_subtract_to_negative(self) -> None:
        """Test subtraction resulting in negative."""
        assert subtract(5.0, 10.0) == -5.0


class TestMultiply:
    """Tests for the multiply function."""

    def test_multiply_integers(self) -> None:
        """Test multiplying two positive integers."""
        assert multiply(6.0, 7.0) == 42.0
        assert multiply(5.0, 5.0) == 25.0
        assert multiply(1.0, 10.0) == 10.0

    def test_multiply_by_zero(self) -> None:
        """Test multiplication by zero."""
        assert multiply(5.0, 0.0) == 0.0
        assert multiply(0.0, 5.0) == 0.0


class TestDivide:
    """Tests for the divide function."""

    def test_divide_integers(self) -> None:
        """Test dividing two positive integers (valid division only)."""
        result = divide(20.0, 4.0)
        assert isinstance(result, float)
        assert result == 5.0

        result = divide(10.0, 2.0)
        assert isinstance(result, float)
        assert result == 5.0

    def test_divide_to_fraction(self) -> None:
        """Test division resulting in a fraction."""
        result = divide(10.0, 3.0)
        assert isinstance(result, float)
        assert abs(result - 3.3333333333333335) < 1e-10

    def test_divide_by_zero(self) -> None:
        """Test division by zero returns error message."""
        result = divide(10.0, 0.0)
        assert isinstance(result, str)
        assert result == "Error: Division by zero is not allowed"


class TestDecimalOperations:
    """Tests for decimal number handling in operations."""

    def test_add_decimals(self) -> None:
        """Test adding decimal numbers."""
        assert add(5.5, 2.3) == 7.8
        assert add(0.1, 0.2) == 0.30000000000000004  # Floating point precision
        assert add(3.14, 2.86) == 6.0

    def test_subtract_decimals(self) -> None:
        """Test subtracting decimal numbers."""
        assert subtract(10.5, 4.2) == 6.3
        assert subtract(5.75, 2.25) == 3.5
        assert subtract(0.3, 0.1) == 0.19999999999999998  # Floating point precision

    def test_multiply_decimals(self) -> None:
        """Test multiplying decimal numbers."""
        assert multiply(7.5, 2.0) == 15.0
        assert multiply(3.5, 2.5) == 8.75
        assert multiply(0.5, 0.5) == 0.25

    def test_divide_decimals(self) -> None:
        """Test dividing decimal numbers."""
        result = divide(10.0, 3.0)
        assert isinstance(result, float)
        assert abs(result - 3.3333333333333335) < 1e-10

        result2 = divide(7.5, 2.5)
        assert isinstance(result2, float)
        assert result2 == 3.0


class TestNegativeNumbers:
    """Tests for negative number handling in operations."""

    def test_add_negative_numbers(self) -> None:
        """Test adding negative numbers."""
        assert add(-5.0, 3.0) == -2.0
        assert add(5.0, -3.0) == 2.0
        assert add(-5.0, -3.0) == -8.0
        assert add(-0.0, 5.0) == 5.0

    def test_subtract_negative_numbers(self) -> None:
        """Test subtracting negative numbers."""
        assert subtract(-6.0, -7.0) == 1.0
        assert subtract(-10.0, 5.0) == -15.0
        assert subtract(10.0, -5.0) == 15.0
        assert subtract(-5.0, -5.0) == 0.0

    def test_multiply_negative_numbers(self) -> None:
        """Test multiplying negative numbers."""
        assert multiply(-6.0, -7.0) == 42.0  # neg * neg = pos
        assert multiply(-6.0, 7.0) == -42.0  # neg * pos = neg
        assert multiply(6.0, -7.0) == -42.0  # pos * neg = neg
        assert multiply(-1.0, -1.0) == 1.0

    def test_divide_negative_numbers(self) -> None:
        """Test dividing negative numbers."""
        result1 = divide(-20.0, 4.0)  # neg / pos = neg
        assert isinstance(result1, float)
        assert result1 == -5.0

        result2 = divide(-20.0, -4.0)  # neg / neg = pos
        assert isinstance(result2, float)
        assert result2 == 5.0

        result3 = divide(20.0, -4.0)  # pos / neg = neg
        assert isinstance(result3, float)
        assert result3 == -5.0
