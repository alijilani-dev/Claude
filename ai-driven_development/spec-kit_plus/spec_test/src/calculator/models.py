"""Data models for the professional calculator interface."""

from dataclasses import dataclass, field

from calculator import Operator


@dataclass(frozen=True)
class CalculationRecord:
    """Immutable record of a single calculation.

    Attributes:
        operand1: First number in the calculation
        operator: Arithmetic operator (+, -, *, /)
        operand2: Second number in the calculation
        result: Calculated result (float) or error message (str)
        timestamp: Unix timestamp when calculation was performed
    """

    operand1: float
    operator: Operator
    operand2: float
    result: float | str
    timestamp: float


@dataclass(frozen=True)
class ColorScheme:
    """UI color scheme constants.

    Attributes:
        prompt_color: Color for user input prompts (cyan)
        success_color: Color for successful results (green)
        error_color: Color for error messages (red)
        operator_color: Color for operator symbols (yellow)
        border_color: Color for panel borders (cyan)
        header_color: Color for header text (cyan)
        dim_color: Color for secondary/dim text (dim white)
    """

    prompt_color: str = "cyan"
    success_color: str = "green bold"
    error_color: str = "red bold"
    operator_color: str = "yellow"
    border_color: str = "cyan"
    header_color: str = "bold cyan"
    dim_color: str = "dim"


# Singleton instance
DEFAULT_COLOR_SCHEME = ColorScheme()


@dataclass(frozen=True)
class MenuOption:
    """Menu option for operation selection.

    Attributes:
        display_name: Human-readable name shown in menu
        operator: Corresponding operator symbol
        description: Optional description of the operation
    """

    display_name: str
    operator: Operator
    description: str = ""


@dataclass
class CalculationHistory:
    """Mutable collection of calculation records.

    Attributes:
        records: List of calculation records (chronological order)
        max_displayed: Maximum records to display in table (for performance)
    """

    records: list[CalculationRecord] = field(default_factory=list)
    max_displayed: int = 20

    def add(self, record: CalculationRecord) -> None:
        """Add a calculation record to history."""
        self.records.append(record)

    def clear(self) -> None:
        """Clear all history records."""
        self.records.clear()

    def get_recent(self, count: int | None = None) -> list[CalculationRecord]:
        """Get most recent records.

        Args:
            count: Number of records to retrieve (defaults to max_displayed)

        Returns:
            List of most recent records (newest last)
        """
        n = count if count is not None else self.max_displayed
        return self.records[-n:] if len(self.records) > n else self.records

    def count(self) -> int:
        """Get total number of records."""
        return len(self.records)

    def is_empty(self) -> bool:
        """Check if history is empty."""
        return len(self.records) == 0
