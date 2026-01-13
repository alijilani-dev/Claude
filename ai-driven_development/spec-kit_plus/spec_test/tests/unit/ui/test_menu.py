"""Unit tests for menu selection component."""

import pytest
from unittest.mock import patch, MagicMock
from typing import Literal

from calculator import Operator
from calculator.ui.menu import select_operation, MENU_OPTIONS


class TestMenuOptions:
    """Test cases for MENU_OPTIONS constant."""

    def test_menu_options_contains_all_operations(self) -> None:
        """Test that MENU_OPTIONS includes all 4 calculator operations."""
        # Extract operator values from menu options
        operators = [opt.value for opt in MENU_OPTIONS if hasattr(opt, 'value')]

        # Should contain all 4 operations
        assert '+' in operators or any('Addition' in str(opt) for opt in MENU_OPTIONS)
        assert '-' in operators or any('Subtraction' in str(opt) for opt in MENU_OPTIONS)
        assert '*' in operators or any('Multiplication' in str(opt) for opt in MENU_OPTIONS)
        assert '/' in operators or any('Division' in str(opt) for opt in MENU_OPTIONS)

    def test_menu_options_contains_exit(self) -> None:
        """Test that MENU_OPTIONS includes an Exit option."""
        # Check for exit/quit option
        exit_found = any(
            'Exit' in getattr(opt, 'title', '') or 'Quit' in getattr(opt, 'title', '')
            for opt in MENU_OPTIONS
        )
        assert exit_found


class TestSelectOperation:
    """Test cases for select_operation function."""

    @patch("calculator.ui.menu.questionary.select")
    def test_select_operation_returns_valid_operator(self, mock_select: MagicMock) -> None:
        """Test that select_operation returns a valid Operator."""
        mock_select.return_value.ask.return_value = '+'
        result = select_operation()
        assert result == '+'
        assert result in ['+', '-', '*', '/']

    @patch("calculator.ui.menu.questionary.select")
    def test_select_operation_addition(self, mock_select: MagicMock) -> None:
        """Test selecting addition operation."""
        mock_select.return_value.ask.return_value = '+'
        result = select_operation()
        assert result == '+'

    @patch("calculator.ui.menu.questionary.select")
    def test_select_operation_subtraction(self, mock_select: MagicMock) -> None:
        """Test selecting subtraction operation."""
        mock_select.return_value.ask.return_value = '-'
        result = select_operation()
        assert result == '-'

    @patch("calculator.ui.menu.questionary.select")
    def test_select_operation_multiplication(self, mock_select: MagicMock) -> None:
        """Test selecting multiplication operation."""
        mock_select.return_value.ask.return_value = '*'
        result = select_operation()
        assert result == '*'

    @patch("calculator.ui.menu.questionary.select")
    def test_select_operation_division(self, mock_select: MagicMock) -> None:
        """Test selecting division operation."""
        mock_select.return_value.ask.return_value = '/'
        result = select_operation()
        assert result == '/'

    @patch("calculator.ui.menu.questionary.select")
    def test_select_operation_ctrl_c_returns_none(self, mock_select: MagicMock) -> None:
        """Test that Ctrl+C (None response) returns None."""
        mock_select.return_value.ask.return_value = None
        result = select_operation()
        assert result is None

    @patch("calculator.ui.menu.questionary.select")
    def test_select_operation_exit_returns_none(self, mock_select: MagicMock) -> None:
        """Test that selecting Exit option returns None."""
        mock_select.return_value.ask.return_value = "exit"
        result = select_operation()
        assert result is None

    @patch("calculator.ui.menu.questionary.select")
    def test_select_operation_uses_questionary_select(self, mock_select: MagicMock) -> None:
        """Test that function calls questionary.select."""
        mock_select.return_value.ask.return_value = '+'
        select_operation()
        assert mock_select.called

    @patch("calculator.ui.menu.questionary.select")
    def test_select_operation_passes_message(self, mock_select: MagicMock) -> None:
        """Test that a message/prompt is passed to questionary."""
        mock_select.return_value.ask.return_value = '+'
        select_operation()

        # First argument should be the message/prompt
        call_args = mock_select.call_args
        assert call_args is not None
        assert len(call_args[0]) > 0  # At least one positional arg (the message)

    @patch("calculator.ui.menu.questionary.select")
    def test_select_operation_applies_styling(self, mock_select: MagicMock) -> None:
        """Test that styling is applied to the menu."""
        mock_select.return_value.ask.return_value = '+'
        select_operation()

        # Check if style parameter was passed
        call_kwargs = mock_select.call_args[1] if mock_select.call_args else {}
        assert 'style' in call_kwargs
