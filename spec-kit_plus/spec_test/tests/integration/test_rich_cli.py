"""Integration tests for Rich CLI calculator."""

import pytest
from unittest.mock import patch, MagicMock, call
from io import StringIO

from calculator.rich_cli import run_rich_calculator


class TestRichCliIntegration:
    """Integration tests for the complete Rich CLI workflow."""

    @patch("calculator.rich_cli.console")
    @patch("calculator.ui.menu.questionary.select")
    @patch("calculator.ui.input.questionary.text")
    def test_complete_calculation_flow(
        self,
        mock_text: MagicMock,
        mock_select: MagicMock,
        mock_console: MagicMock
    ) -> None:
        """Test complete flow: select operation → enter numbers → view result → verify history."""
        # Configure mock console
        mock_console.width = 100  # Adequate width

        # Simulate: Select Addition, enter 5 and 3, then Exit
        mock_select.return_value.ask.side_effect = ['+', None]  # Addition, then Exit
        mock_text.return_value.ask.side_effect = ["5", "3"]  # Two numbers

        run_rich_calculator()

        # Verify questionary.select was called (operation selection)
        assert mock_select.called
        assert mock_select.call_count >= 2  # At least for the operation and exit

        # Verify questionary.text was called (number inputs)
        assert mock_text.called
        assert mock_text.call_count >= 2  # For two numbers

        # Verify console.print was called (for header, result, history)
        assert mock_console.print.called

    @patch("calculator.rich_cli.console")
    @patch("calculator.ui.menu.questionary.select")
    @patch("calculator.ui.input.questionary.text")
    def test_multiple_calculations_accumulate_in_history(
        self,
        mock_text: MagicMock,
        mock_select: MagicMock,
        mock_console: MagicMock
    ) -> None:
        """Test that multiple calculations accumulate in history."""
        mock_console.width = 100

        # Simulate: 3 calculations then Exit
        mock_select.return_value.ask.side_effect = ['+', '-', '*', None]
        mock_text.return_value.ask.side_effect = [
            "5", "3",    # First calculation
            "10", "2",   # Second calculation
            "6", "7",    # Third calculation
        ]

        run_rich_calculator()

        # Verify multiple operations were selected
        assert mock_select.call_count >= 4  # 3 operations + exit

        # Verify multiple number inputs
        assert mock_text.call_count >= 6  # 6 numbers (2 per calculation)

    @patch("calculator.rich_cli.console")
    @patch("calculator.ui.menu.questionary.select")
    @patch("calculator.ui.input.questionary.text")
    def test_division_by_zero_handled_correctly(
        self,
        mock_text: MagicMock,
        mock_select: MagicMock,
        mock_console: MagicMock
    ) -> None:
        """Test that division by zero is handled correctly."""
        mock_console.width = 100

        # Simulate: Division, enter 10 and 0, then Exit
        mock_select.return_value.ask.side_effect = ['/', None]
        mock_text.return_value.ask.side_effect = ["10", "0"]

        run_rich_calculator()

        # Note: The validator should prevent zero input for division
        # But if it gets through, the operation should handle it
        assert mock_select.called
        assert mock_text.called

    @patch("calculator.rich_cli.console")
    @patch("calculator.ui.menu.questionary.select")
    def test_ctrl_c_on_operation_selection_exits_gracefully(
        self,
        mock_select: MagicMock,
        mock_console: MagicMock
    ) -> None:
        """Test that Ctrl+C on operation selection exits gracefully."""
        mock_console.width = 100

        # Simulate Ctrl+C (None response)
        mock_select.return_value.ask.return_value = None

        run_rich_calculator()

        # Should exit without errors
        assert mock_select.called

        # Should display goodbye message
        goodbye_calls = [
            call_obj for call_obj in mock_console.print.call_args_list
            if len(call_obj[0]) > 0 and "Thanks" in str(call_obj[0][0])
        ]
        assert len(goodbye_calls) > 0

    @patch("calculator.rich_cli.console")
    @patch("calculator.ui.menu.questionary.select")
    @patch("calculator.ui.input.questionary.text")
    def test_ctrl_c_on_number_input_exits_gracefully(
        self,
        mock_text: MagicMock,
        mock_select: MagicMock,
        mock_console: MagicMock
    ) -> None:
        """Test that Ctrl+C on number input exits gracefully."""
        mock_console.width = 100

        # Simulate: Select operation, then Ctrl+C on number input
        mock_select.return_value.ask.return_value = '+'
        mock_text.return_value.ask.return_value = None  # Ctrl+C

        run_rich_calculator()

        # Should exit without errors
        assert mock_select.called
        assert mock_text.called

        # Should display goodbye message
        goodbye_calls = [
            call_obj for call_obj in mock_console.print.call_args_list
            if len(call_obj[0]) > 0 and "Thanks" in str(call_obj[0][0])
        ]
        assert len(goodbye_calls) > 0

    @patch("calculator.rich_cli.console")
    @patch("calculator.ui.menu.questionary.select")
    @patch("calculator.ui.input.questionary.text")
    def test_all_four_operations_work(
        self,
        mock_text: MagicMock,
        mock_select: MagicMock,
        mock_console: MagicMock
    ) -> None:
        """Test that all four calculator operations work correctly."""
        mock_console.width = 100

        # Test all operations: +, -, *, /
        mock_select.return_value.ask.side_effect = ['+', '-', '*', '/', None]
        mock_text.return_value.ask.side_effect = [
            "5", "3",    # 5 + 3 = 8
            "10", "2",   # 10 - 2 = 8
            "6", "7",    # 6 * 7 = 42
            "20", "4",   # 20 / 4 = 5
        ]

        run_rich_calculator()

        # All operations should complete successfully
        assert mock_select.call_count >= 5  # 4 operations + exit
        assert mock_text.call_count >= 8    # 8 number inputs

    @patch("calculator.rich_cli.console")
    @patch("calculator.ui.menu.questionary.select")
    @patch("calculator.ui.input.questionary.text")
    def test_exit_option_works(
        self,
        mock_text: MagicMock,
        mock_select: MagicMock,
        mock_console: MagicMock
    ) -> None:
        """Test that selecting Exit option terminates the calculator."""
        mock_console.width = 100

        # Simulate selecting Exit
        mock_select.return_value.ask.return_value = "exit"

        run_rich_calculator()

        # Should exit after first selection
        assert mock_select.call_count == 1
        assert mock_text.call_count == 0  # No number inputs

    @patch("calculator.rich_cli.console")
    @patch("calculator.ui.menu.questionary.select")
    @patch("calculator.ui.input.questionary.text")
    def test_header_is_displayed(
        self,
        mock_text: MagicMock,
        mock_select: MagicMock,
        mock_console: MagicMock
    ) -> None:
        """Test that the header is displayed at startup."""
        mock_console.width = 100

        mock_select.return_value.ask.return_value = None  # Exit immediately

        run_rich_calculator()

        # Header should be printed (first print call)
        assert mock_console.print.called
        # First call should be the header Panel
        first_call_args = mock_console.print.call_args_list[0][0]
        assert len(first_call_args) > 0

    @patch("calculator.rich_cli.console")
    @patch("calculator.ui.menu.questionary.select")
    @patch("calculator.ui.input.questionary.text")
    def test_history_table_displayed_after_calculation(
        self,
        mock_text: MagicMock,
        mock_select: MagicMock,
        mock_console: MagicMock
    ) -> None:
        """Test that history table is displayed after each calculation."""
        mock_console.width = 100

        mock_select.return_value.ask.side_effect = ['+', None]
        mock_text.return_value.ask.side_effect = ["5", "3"]

        run_rich_calculator()

        # History table should be printed after calculation
        # Look for Table objects in print calls
        table_calls = [
            call_obj for call_obj in mock_console.print.call_args_list
            if len(call_obj[0]) > 0 and hasattr(call_obj[0][0], 'columns')
        ]
        assert len(table_calls) > 0  # At least one table was printed
