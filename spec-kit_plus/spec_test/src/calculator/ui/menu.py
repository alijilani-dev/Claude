"""Menu selection component for calculator UI."""


import questionary
from questionary import Choice, Style

from calculator import Operator

# Menu options for operation selection
MENU_OPTIONS = [
    Choice(title="➕ Addition", value="+"),
    Choice(title="➖ Subtraction", value="-"),
    Choice(title="✖️  Multiplication", value="*"),
    Choice(title="➗ Division", value="/"),
    Choice(title="───────────────", value="", disabled="true"),  # Separator
    Choice(title="🚪 Exit", value="exit"),
]


def select_operation() -> Operator | None:
    """
    Display interactive menu for operation selection.

    Returns:
        Selected operator ('+', '-', '*', '/') or None if user cancels (Ctrl+C)
        or selects Exit.
    """
    # Define custom style with cyan theme
    custom_style = Style([
        ("qmark", "fg:cyan bold"),
        ("question", "fg:cyan bold"),
        ("answer", "fg:cyan"),
        ("pointer", "fg:cyan bold"),
        ("highlighted", "fg:cyan bold"),
        ("selected", "fg:cyan"),
    ])

    result = questionary.select(
        "Select an operation:",
        choices=MENU_OPTIONS,
        style=custom_style
    ).ask()

    # If user cancels (Ctrl+C) or selects Exit, return None
    if result is None or result == "exit" or result == "":
        return None

    # Return the operator (we know it's a valid operator at this point)
    # questionary returns Any, but we know it's a valid Operator
    return result  # type: ignore[no-any-return]
