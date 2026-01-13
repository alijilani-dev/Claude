"""Unit tests for edge cases and formatting."""

import pytest

from calculator.cli import format_result
from calculator.operations import add, divide


class TestFloatingPointPrecision:
    """Tests for floating point precision edge cases."""

    def test_floating_point_precision(self) -> None:
        """Test that 0.1 + 0.2 is handled correctly."""
        result = add(0.1, 0.2)
        # Floating point gives 0.30000000000000004
        assert result == 0.30000000000000004
        # But format_result should clean it up to "0.3"
        formatted = format_result(result)
        assert formatted == "0.3"

    def test_repeating_decimals(self) -> None:
        """Test division resulting in repeating decimals."""
        result = divide(10.0, 3.0)
        assert isinstance(result, float)
        # Should be 3.3333333333333335
        assert abs(result - 3.3333333333333335) < 1e-10
        # format_result should show 10 decimal places
        formatted = format_result(result)
        assert formatted == "3.3333333333"


class TestFormatResult:
    """Tests for the format_result function."""

    def test_format_result_integer(self) -> None:
        """Test formatting integer-valued floats."""
        assert format_result(8.0) == "8"
        assert format_result(100.0) == "100"
        assert format_result(0.0) == "0"

    def test_format_result_decimals(self) -> None:
        """Test formatting decimal numbers."""
        assert format_result(5.25) == "5.25"
        assert format_result(3.14159) == "3.14159"
        assert format_result(0.5) == "0.5"

    def test_format_result_trailing_zeros(self) -> None:
        """Test that trailing zeros are removed."""
        assert format_result(5.50) == "5.5"
        assert format_result(10.000) == "10"
        assert format_result(3.1000000) == "3.1"

    def test_format_result_max_precision(self) -> None:
        """Test formatting with maximum 10 decimal places."""
        assert format_result(3.333333333333) == "3.3333333333"
        # More than 10 decimals gets truncated, trailing zeros removed
        assert format_result(1.123456789012345) == "1.123456789"

    def test_format_result_scientific_edge_cases(self) -> None:
        """Test very small and very large numbers."""
        assert format_result(0.0000000001) == "0.0000000001"
        assert format_result(0.00000000001) == "0"  # Beyond 10 decimal places
        assert format_result(1000000000.0) == "1000000000"
