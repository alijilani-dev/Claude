"""Input handling components for calculator UI."""

from typing import Any

import questionary
from questionary import Style, ValidationError, Validator


class NumberValidator(Validator):
    """Validator for numeric input in calculator."""

    def __init__(self, allow_zero: bool = True) -> None:
        """
        Initialize the number validator.

        Args:
            allow_zero: Whether to allow zero as a valid input. Default is True.
        """
        self.allow_zero = allow_zero

    def validate(self, document: Any) -> None:
        """
        Validate that the input is a valid number.

        Args:
            document: The Document object from questionary containing the input text.

        Raises:
            ValidationError: If the input is not a valid number or is zero when
                           allow_zero is False.
        """
        # Handle both str and Document types from questionary
        text = document.text if hasattr(document, "text") else str(document)

        if not text or not text.strip():
            raise ValidationError(
                message="Please enter a valid number"
            )

        try:
            value = float(text)
            if not self.allow_zero and value == 0:
                raise ValidationError(
                    message="Zero is not allowed for this input"
                )
        except ValueError:
            raise ValidationError(
                message="Please enter a valid number (integers, decimals, or negatives)"
            )


def get_number(prompt: str, allow_zero: bool = True) -> float | None:
    """
    Prompt user for a numeric input with validation.

    Args:
        prompt: The prompt message to display to the user.
        allow_zero: Whether to allow zero as a valid input. Default is True.

    Returns:
        The validated number as a float, or None if user cancels (Ctrl+C).
    """
    # Define custom style with cyan prompts
    custom_style = Style([
        ("qmark", "fg:cyan bold"),
        ("question", "fg:cyan bold"),
        ("answer", "fg:cyan"),
        ("pointer", "fg:cyan bold"),
        ("highlighted", "fg:cyan bold"),
        ("selected", "fg:cyan"),
    ])

    validator = NumberValidator(allow_zero=allow_zero)

    result = questionary.text(
        prompt,
        validate=validator,
        style=custom_style
    ).ask()

    # If user cancels (Ctrl+C), questionary returns None
    if result is None:
        return None

    return float(result)
