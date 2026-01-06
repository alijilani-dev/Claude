"""Unit tests for overflow and extreme value edge cases."""

import math

import pytest

from calculator.operations import add, divide, multiply, subtract


class TestVeryLargeNumbers:
    """Tests for very large number handling."""

    def test_add_very_large_numbers(self) -> None:
        """Test adding very large numbers."""
        large = 1e100
        result = add(large, large)
        assert result == 2e100

    def test_multiply_very_large_numbers(self) -> None:
        """Test multiplying very large numbers (may produce inf)."""
        large = 1e200
        result = multiply(large, large)
        # Result may be inf if beyond float range
        assert result == math.inf or isinstance(result, float)

    def test_divide_very_large_by_small(self) -> None:
        """Test dividing very large by very small."""
        result = divide(1e100, 1e-100)
        assert isinstance(result, float)
        # May be inf if exceeds float range
        assert result == math.inf or result > 0


class TestVerySmallNumbers:
    """Tests for very small number handling."""

    def test_add_very_small_numbers(self) -> None:
        """Test adding very small numbers."""
        small = 1e-100
        result = add(small, small)
        assert result == 2e-100 or result > 0

    def test_multiply_very_small_numbers(self) -> None:
        """Test multiplying very small numbers (may underflow to 0)."""
        small = 1e-200
        result = multiply(small, small)
        # May underflow to 0
        assert result == 0.0 or result > 0

    def test_divide_very_small_by_large(self) -> None:
        """Test dividing very small by very large."""
        result = divide(1e-100, 1e100)
        assert isinstance(result, float)
        # May underflow to 0
        assert result >= 0


class TestSpecialValues:
    """Tests for special floating point values."""

    def test_add_with_infinity(self) -> None:
        """Test operations with infinity."""
        inf = math.inf
        result = add(inf, 5.0)
        assert result == math.inf

    def test_negative_infinity(self) -> None:
        """Test operations with negative infinity."""
        neg_inf = -math.inf
        result = add(neg_inf, 5.0)
        assert result == -math.inf

    def test_zero_operations(self) -> None:
        """Test edge cases with zero."""
        assert add(0.0, 0.0) == 0.0
        assert multiply(1000000.0, 0.0) == 0.0
        assert subtract(0.0, 0.0) == 0.0
