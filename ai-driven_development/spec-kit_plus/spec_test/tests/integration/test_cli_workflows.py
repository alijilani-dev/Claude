"""Integration tests for CLI workflows."""

from io import StringIO
from unittest.mock import patch

import pytest

from calculator.cli import run_calculator


class TestBasicCalculationFlow:
    """Tests for basic calculation workflows."""

    def test_basic_calculation_flow(self) -> None:
        """Test a sequence of basic calculations."""
        # Simulate user input: 5 + 3, 10 - 4, 6 * 7, 20 / 4, quit
        user_inputs = ["5 + 3", "10 - 4", "6 * 7", "20 / 4", "quit"]
        expected_outputs = ["8", "6", "42", "5"]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                run_calculator()
                output = mock_stdout.getvalue()

                # Verify all expected results appear in output
                for expected in expected_outputs:
                    assert expected in output

                # Verify welcome and goodbye messages
                assert "Calculator" in output or "Welcome" in output
                assert "Goodbye" in output or "exit" in output.lower()

    def test_decimal_calculation_flow(self) -> None:
        """Test calculations with decimal numbers."""
        user_inputs = ["5.5 + 2.3", "10.0 / 3.0", "quit"]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                run_calculator()
                output = mock_stdout.getvalue()

                # 5.5 + 2.3 = 7.8
                assert "7.8" in output
                # 10.0 / 3.0 = 3.3333333333 (10 decimal places)
                assert "3.3333333333" in output

    def test_negative_number_flow(self) -> None:
        """Test calculations with negative numbers."""
        user_inputs = ["-5 + 3", "-6 * -7", "exit"]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                run_calculator()
                output = mock_stdout.getvalue()

                # -5 + 3 = -2
                assert "-2" in output
                # -6 * -7 = 42
                assert "42" in output


class TestErrorRecoveryFlow:
    """Tests for error handling and recovery."""

    def test_error_recovery_flow(self) -> None:
        """Test that calculator recovers from errors and continues."""
        # Invalid input followed by valid input
        user_inputs = [
            "abc + 5",  # Invalid number
            "10 $ 5",  # Invalid operator
            "5 +",  # Incomplete input
            "5 / 0",  # Division by zero
            "10 + 5",  # Valid input
            "quit",
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                run_calculator()
                output = mock_stdout.getvalue()

                # Verify error messages appear
                assert "Error" in output
                assert "Invalid input" in output or "invalid" in output.lower()
                assert "Invalid operator" in output or "operator" in output.lower()
                assert "Division by zero" in output or "zero" in output.lower()

                # Verify calculator continued and processed valid input
                assert "15" in output  # 10 + 5 = 15

    def test_multiple_errors_in_sequence(self) -> None:
        """Test handling multiple consecutive errors."""
        user_inputs = ["abc", "xyz + 10", "5 $ 3", "6 * 7", "quit"]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                run_calculator()
                output = mock_stdout.getvalue()

                # Multiple errors should all be caught
                assert output.count("Error") >= 3
                # But valid calculation should still work
                assert "42" in output


class TestExitCommand:
    """Tests for exit command handling."""

    def test_exit_command_lowercase(self) -> None:
        """Test that 'exit' command terminates calculator."""
        user_inputs = ["5 + 3", "exit"]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                run_calculator()
                output = mock_stdout.getvalue()

                # Calculation should have run
                assert "8" in output
                # Should have exited cleanly
                assert "Goodbye" in output or "exit" in output.lower()

    def test_quit_command_lowercase(self) -> None:
        """Test that 'quit' command terminates calculator."""
        user_inputs = ["10 - 4", "quit"]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                run_calculator()
                output = mock_stdout.getvalue()

                assert "6" in output
                assert "Goodbye" in output or "quit" in output.lower()

    def test_exit_command_uppercase(self) -> None:
        """Test that 'EXIT' and 'QUIT' work (case-insensitive)."""
        user_inputs = ["EXIT"]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                run_calculator()
                output = mock_stdout.getvalue()

                # Should exit immediately
                assert "Goodbye" in output or "exit" in output.lower()

    def test_quit_command_uppercase(self) -> None:
        """Test QUIT in uppercase."""
        user_inputs = ["QUIT"]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                run_calculator()
                output = mock_stdout.getvalue()

                assert "Goodbye" in output or "quit" in output.lower()
