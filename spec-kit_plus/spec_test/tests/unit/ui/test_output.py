"""Unit tests for output display component."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from calculator.ui.output import display_result, display_error


class TestDisplayResult:
    """Test cases for display_result function."""

    @patch("calculator.ui.output.console")
    def test_display_result_calls_console_print(self, mock_console: MagicMock) -> None:
        """Test that display_result calls console.print."""
        display_result(42.5)
        assert mock_console.print.called

    @patch("calculator.ui.output.console")
    def test_display_result_formats_integer(self, mock_console: MagicMock) -> None:
        """Test that display_result formats integer results."""
        display_result(8.0)

        # Check that print was called with result
        call_args = mock_console.print.call_args
        assert call_args is not None
        # The result should be in the printed text
        printed_text = str(call_args[0][0])
        assert '8' in printed_text or '8.0' in printed_text

    @patch("calculator.ui.output.console")
    def test_display_result_formats_decimal(self, mock_console: MagicMock) -> None:
        """Test that display_result formats decimal results."""
        display_result(3.14159)

        call_args = mock_console.print.call_args
        assert call_args is not None
        printed_text = str(call_args[0][0])
        assert '3.14159' in printed_text

    @patch("calculator.ui.output.console")
    def test_display_result_uses_green_style(self, mock_console: MagicMock) -> None:
        """Test that display_result uses green styling."""
        display_result(42.0)

        call_kwargs = mock_console.print.call_args[1]
        assert 'style' in call_kwargs
        style = call_kwargs['style']
        assert 'green' in style.lower()

    @patch("calculator.ui.output.console")
    def test_display_result_uses_bold_style(self, mock_console: MagicMock) -> None:
        """Test that display_result uses bold styling."""
        display_result(42.0)

        call_kwargs = mock_console.print.call_args[1]
        assert 'style' in call_kwargs
        style = call_kwargs['style']
        assert 'bold' in style.lower()

    @patch("calculator.ui.output.console")
    def test_display_result_handles_negative_numbers(self, mock_console: MagicMock) -> None:
        """Test that display_result handles negative numbers."""
        display_result(-5.5)

        call_args = mock_console.print.call_args
        assert call_args is not None
        printed_text = str(call_args[0][0])
        assert '-5.5' in printed_text or '-5.5' in printed_text

    @patch("calculator.ui.output.console")
    def test_display_result_handles_zero(self, mock_console: MagicMock) -> None:
        """Test that display_result handles zero."""
        display_result(0.0)

        call_args = mock_console.print.call_args
        assert call_args is not None
        printed_text = str(call_args[0][0])
        assert '0' in printed_text


class TestDisplayError:
    """Test cases for display_error function."""

    @patch("calculator.ui.output.console")
    def test_display_error_calls_console_print(self, mock_console: MagicMock) -> None:
        """Test that display_error calls console.print."""
        display_error("Test error")
        assert mock_console.print.called

    @patch("calculator.ui.output.console")
    def test_display_error_includes_message(self, mock_console: MagicMock) -> None:
        """Test that display_error includes the error message."""
        error_msg = "Division by zero"
        display_error(error_msg)

        call_args = mock_console.print.call_args
        assert call_args is not None
        printed_text = str(call_args[0][0])
        assert error_msg in printed_text

    @patch("calculator.ui.output.console")
    def test_display_error_uses_red_style(self, mock_console: MagicMock) -> None:
        """Test that display_error uses red styling."""
        display_error("Test error")

        call_kwargs = mock_console.print.call_args[1]
        assert 'style' in call_kwargs
        style = call_kwargs['style']
        assert 'red' in style.lower()

    @patch("calculator.ui.output.console")
    def test_display_error_uses_bold_style(self, mock_console: MagicMock) -> None:
        """Test that display_error uses bold styling."""
        display_error("Test error")

        call_kwargs = mock_console.print.call_args[1]
        assert 'style' in call_kwargs
        style = call_kwargs['style']
        assert 'bold' in style.lower()

    @patch("calculator.ui.output.console")
    def test_display_error_displays_message(self, mock_console: MagicMock) -> None:
        """Test that display_error displays the message correctly."""
        display_error("Something went wrong")

        call_args = mock_console.print.call_args
        assert call_args is not None
        printed_text = str(call_args[0][0])
        # The message should be displayed (error prefix may already be in input)
        assert 'Something went wrong' in printed_text

    @patch("calculator.ui.output.console")
    def test_display_error_handles_division_by_zero_message(self, mock_console: MagicMock) -> None:
        """Test that display_error handles division by zero message."""
        error_msg = "Error: Division by zero is not allowed"
        display_error(error_msg)

        call_args = mock_console.print.call_args
        assert call_args is not None
        printed_text = str(call_args[0][0])
        assert "Division by zero" in printed_text
