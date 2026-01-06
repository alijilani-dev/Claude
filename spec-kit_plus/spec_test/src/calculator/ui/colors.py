"""Color scheme and theme definitions for the calculator UI."""

from rich.theme import Theme

from calculator.models import DEFAULT_COLOR_SCHEME

# Rich Theme for consistent color styling
CALCULATOR_THEME = Theme(
    {
        "prompt": DEFAULT_COLOR_SCHEME.prompt_color,
        "success": DEFAULT_COLOR_SCHEME.success_color,
        "error": DEFAULT_COLOR_SCHEME.error_color,
        "operator": DEFAULT_COLOR_SCHEME.operator_color,
        "border": DEFAULT_COLOR_SCHEME.border_color,
        "header": DEFAULT_COLOR_SCHEME.header_color,
        "dim": DEFAULT_COLOR_SCHEME.dim_color,
    }
)

# Individual color constants for direct use
CYAN = DEFAULT_COLOR_SCHEME.prompt_color
GREEN = DEFAULT_COLOR_SCHEME.success_color
RED = DEFAULT_COLOR_SCHEME.error_color
YELLOW = DEFAULT_COLOR_SCHEME.operator_color
