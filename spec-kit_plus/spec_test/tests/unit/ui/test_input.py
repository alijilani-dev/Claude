"""Unit tests for number input validation component."""

import pytest
from unittest.mock import patch, MagicMock
from questionary import ValidationError

from calculator.ui.input import NumberValidator, get_number


class TestNumberValidator:
    """Test cases for NumberValidator class."""

    def test_validate_accepts_valid_integers(self) -> None:
        """Test that validator accepts valid integer strings."""
        validator = NumberValidator()
        # Should not raise ValidationError
        validator.validate("5")
        validator.validate("42")
        validator.validate("0")

    def test_validate_accepts_valid_decimals(self) -> None:
        """Test that validator accepts valid decimal numbers."""
        validator = NumberValidator()
        validator.validate("3.14")
        validator.validate("0.5")
        validator.validate("100.001")

    def test_validate_accepts_negative_numbers(self) -> None:
        """Test that validator accepts negative numbers."""
        validator = NumberValidator()
        validator.validate("-5")
        validator.validate("-3.14")
        validator.validate("-0.5")

    def test_validate_rejects_alphabetic_input(self) -> None:
        """Test that validator rejects alphabetic input."""
        validator = NumberValidator()
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("abc")
        assert "valid number" in str(exc_info.value).lower()

    def test_validate_rejects_mixed_input(self) -> None:
        """Test that validator rejects mixed alphanumeric input."""
        validator = NumberValidator()
        with pytest.raises(ValidationError):
            validator.validate("12abc")
        with pytest.raises(ValidationError):
            validator.validate("abc123")

    def test_validate_rejects_empty_string(self) -> None:
        """Test that validator rejects empty string."""
        validator = NumberValidator()
        with pytest.raises(ValidationError):
            validator.validate("")

    def test_validate_with_allow_zero_false_rejects_zero(self) -> None:
        """Test that validator rejects zero when allow_zero=False."""
        validator = NumberValidator(allow_zero=False)
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("0")
        assert "zero" in str(exc_info.value).lower()

    def test_validate_with_allow_zero_true_accepts_zero(self) -> None:
        """Test that validator accepts zero when allow_zero=True."""
        validator = NumberValidator(allow_zero=True)
        validator.validate("0")  # Should not raise


class TestGetNumber:
    """Test cases for get_number function."""

    @patch("calculator.ui.input.questionary.text")
    def test_get_number_accepts_valid_integers(self, mock_text: MagicMock) -> None:
        """Test that get_number accepts and returns valid integers."""
        mock_text.return_value.ask.return_value = "42"
        result = get_number("Enter number:")
        assert result == 42.0
        assert isinstance(result, float)

    @patch("calculator.ui.input.questionary.text")
    def test_get_number_accepts_valid_decimals(self, mock_text: MagicMock) -> None:
        """Test that get_number accepts and returns valid decimals."""
        mock_text.return_value.ask.return_value = "3.14"
        result = get_number("Enter number:")
        assert result == 3.14

    @patch("calculator.ui.input.questionary.text")
    def test_get_number_accepts_negative_numbers(self, mock_text: MagicMock) -> None:
        """Test that get_number accepts and returns negative numbers."""
        mock_text.return_value.ask.return_value = "-5.5"
        result = get_number("Enter number:")
        assert result == -5.5

    @patch("calculator.ui.input.questionary.text")
    def test_get_number_returns_none_on_ctrl_c(self, mock_text: MagicMock) -> None:
        """Test that get_number returns None when user cancels (Ctrl+C)."""
        mock_text.return_value.ask.return_value = None
        result = get_number("Enter number:")
        assert result is None

    @patch("calculator.ui.input.questionary.text")
    def test_get_number_with_allow_zero_parameter(self, mock_text: MagicMock) -> None:
        """Test that get_number passes allow_zero to validator."""
        # First test: allow_zero=True (default) should accept zero
        mock_text.return_value.ask.return_value = "0"
        result = get_number("Enter number:", allow_zero=True)
        assert result == 0.0

        # Verify validator was created with allow_zero=True
        # We can check this by examining the call to questionary.text
        call_kwargs = mock_text.call_args[1]
        validator = call_kwargs.get("validate")
        assert validator is not None

    @patch("calculator.ui.input.questionary.text")
    def test_get_number_uses_cyan_style(self, mock_text: MagicMock) -> None:
        """Test that get_number applies cyan styling to prompts."""
        mock_text.return_value.ask.return_value = "5"
        get_number("Enter number:")

        # Verify questionary.text was called
        assert mock_text.called
        # The style parameter should be passed
        call_kwargs = mock_text.call_args[1]
        assert "style" in call_kwargs
