"""Unit tests for input validation and parsing."""

import pytest

from calculator.validator import ParsedInput, parse_input, parse_number, validate_operator


class TestParseNumber:
    """Tests for the parse_number function."""

    def test_parse_number_valid_integer(self) -> None:
        """Test parsing valid integer strings."""
        assert parse_number("5") == 5.0
        assert parse_number("42") == 42.0
        assert parse_number("0") == 0.0

    def test_parse_number_valid_decimal(self) -> None:
        """Test parsing valid decimal strings."""
        assert parse_number("3.14") == 3.14
        assert parse_number("0.5") == 0.5
        assert parse_number("10.0") == 10.0

    def test_parse_number_valid_negative(self) -> None:
        """Test parsing valid negative numbers."""
        assert parse_number("-5") == -5.0
        assert parse_number("-3.14") == -3.14
        assert parse_number("-0.5") == -0.5

    def test_parse_number_invalid_text(self) -> None:
        """Test parsing invalid text returns error message."""
        result = parse_number("abc")
        assert isinstance(result, str)
        assert result == "Error: Invalid input - please enter valid numbers"

    def test_parse_number_empty_string(self) -> None:
        """Test parsing empty string returns error message."""
        result = parse_number("")
        assert isinstance(result, str)
        assert result == "Error: Invalid input - please enter valid numbers"

    def test_parse_number_invalid_mixed(self) -> None:
        """Test parsing mixed text and numbers returns error."""
        result = parse_number("5abc")
        assert isinstance(result, str)
        assert result == "Error: Invalid input - please enter valid numbers"


class TestValidateOperator:
    """Tests for the validate_operator function."""

    def test_validate_operator_valid_addition(self) -> None:
        """Test validating addition operator."""
        assert validate_operator("+") == "+"

    def test_validate_operator_valid_subtraction(self) -> None:
        """Test validating subtraction operator."""
        assert validate_operator("-") == "-"

    def test_validate_operator_valid_multiplication(self) -> None:
        """Test validating multiplication operator."""
        assert validate_operator("*") == "*"

    def test_validate_operator_valid_division(self) -> None:
        """Test validating division operator."""
        assert validate_operator("/") == "/"

    def test_validate_operator_invalid_symbol(self) -> None:
        """Test invalid operator symbol returns error."""
        result = validate_operator("$")
        assert isinstance(result, str)
        assert result == "Error: Invalid operator - use +, -, *, or /"

    def test_validate_operator_invalid_word(self) -> None:
        """Test invalid operator word returns error."""
        result = validate_operator("add")
        assert isinstance(result, str)
        assert result == "Error: Invalid operator - use +, -, *, or /"

    def test_validate_operator_invalid_empty(self) -> None:
        """Test empty operator returns error."""
        result = validate_operator("")
        assert isinstance(result, str)
        assert result == "Error: Invalid operator - use +, -, *, or /"


class TestParseInput:
    """Tests for the parse_input function."""

    def test_parse_input_valid_addition(self) -> None:
        """Test parsing valid addition input."""
        result = parse_input("5 + 3")
        assert isinstance(result, ParsedInput)
        assert result.operand1 == 5.0
        assert result.operator == "+"
        assert result.operand2 == 3.0

    def test_parse_input_valid_subtraction(self) -> None:
        """Test parsing valid subtraction input."""
        result = parse_input("10 - 4")
        assert isinstance(result, ParsedInput)
        assert result.operand1 == 10.0
        assert result.operator == "-"
        assert result.operand2 == 4.0

    def test_parse_input_valid_multiplication(self) -> None:
        """Test parsing valid multiplication input."""
        result = parse_input("6 * 7")
        assert isinstance(result, ParsedInput)
        assert result.operand1 == 6.0
        assert result.operator == "*"
        assert result.operand2 == 7.0

    def test_parse_input_valid_division(self) -> None:
        """Test parsing valid division input."""
        result = parse_input("20 / 4")
        assert isinstance(result, ParsedInput)
        assert result.operand1 == 20.0
        assert result.operator == "/"
        assert result.operand2 == 4.0

    def test_parse_input_valid_negative_numbers(self) -> None:
        """Test parsing negative numbers."""
        result = parse_input("-6 * -7")
        assert isinstance(result, ParsedInput)
        assert result.operand1 == -6.0
        assert result.operator == "*"
        assert result.operand2 == -7.0

    def test_parse_input_valid_decimals(self) -> None:
        """Test parsing decimal numbers."""
        result = parse_input("5.5 + 2.3")
        assert isinstance(result, ParsedInput)
        assert result.operand1 == 5.5
        assert result.operator == "+"
        assert result.operand2 == 2.3

    def test_parse_input_invalid_number(self) -> None:
        """Test parsing with invalid number returns error."""
        result = parse_input("abc + 5")
        assert isinstance(result, str)
        assert result == "Error: Invalid input - please enter valid numbers"

        result2 = parse_input("5 + xyz")
        assert isinstance(result2, str)
        assert result2 == "Error: Invalid input - please enter valid numbers"

    def test_parse_input_invalid_operator(self) -> None:
        """Test parsing with invalid operator returns error."""
        result = parse_input("5 $ 3")
        assert isinstance(result, str)
        assert result == "Error: Invalid operator - use +, -, *, or /"

    def test_parse_input_incomplete_input(self) -> None:
        """Test parsing incomplete input returns error."""
        result = parse_input("5 +")
        assert isinstance(result, str)
        assert result == "Error: Please provide two numbers and an operator"

        result2 = parse_input("5")
        assert isinstance(result2, str)
        assert result2 == "Error: Please provide two numbers and an operator"

        result3 = parse_input("")
        assert isinstance(result3, str)
        assert result3 == "Error: Please provide two numbers and an operator"

    def test_parse_input_too_many_tokens(self) -> None:
        """Test parsing input with too many tokens returns error."""
        result = parse_input("5 + 3 + 2")
        assert isinstance(result, str)
        assert result == "Error: Please provide two numbers and an operator"
