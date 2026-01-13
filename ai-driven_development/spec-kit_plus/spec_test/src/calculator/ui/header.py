"""Header component for calculator UI."""

from rich.align import Align
from rich.box import DOUBLE
from rich.panel import Panel


def render_header() -> Panel:
    """
    Render the professional branded header for the calculator.

    Returns:
        Panel: A Rich Panel containing "Panaversity Calculator v2.0" with
               cyan border and DOUBLE box style.
    """
    title_text = "Panaversity Calculator v2.0"
    centered_text = Align.center(title_text)

    return Panel(
        centered_text,
        border_style="cyan",
        box=DOUBLE,
        padding=(0, 2)
    )
