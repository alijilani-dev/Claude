"""UI components for the calculator."""

from rich.console import Console

from calculator.ui.colors import CALCULATOR_THEME

# Shared console instance with themed styling
console = Console(theme=CALCULATOR_THEME)

__all__ = ["console"]
