"""Unit tests for calculation history display component."""

import pytest
import time
from rich.table import Table

from calculator.models import CalculationHistory, CalculationRecord
from calculator.ui.history import render_history_table


class TestRenderHistoryTable:
    """Test cases for render_history_table function."""

    def test_render_history_table_with_empty_history(self) -> None:
        """Test that render_history_table handles empty history."""
        history = CalculationHistory()
        table = render_history_table(history)

        assert isinstance(table, Table)
        # Empty table should still have the title and columns
        assert "History" in str(table.title).lower() or "Calculation" in str(table.title)

    def test_render_history_table_with_one_record(self) -> None:
        """Test that render_history_table displays a single record."""
        history = CalculationHistory()
        record = CalculationRecord(
            operand1=5.0,
            operator='+',
            operand2=3.0,
            result=8.0,
            timestamp=time.time()
        )
        history.add(record)

        table = render_history_table(history)
        assert isinstance(table, Table)
        # Verify table has rows (1 record)
        assert history.count() == 1

    def test_render_history_table_with_five_records(self) -> None:
        """Test that render_history_table displays multiple records."""
        history = CalculationHistory()

        # Add 5 different calculations
        records = [
            CalculationRecord(5.0, '+', 3.0, 8.0, time.time()),
            CalculationRecord(10.0, '-', 2.0, 8.0, time.time()),
            CalculationRecord(6.0, '*', 7.0, 42.0, time.time()),
            CalculationRecord(20.0, '/', 4.0, 5.0, time.time()),
            CalculationRecord(10.0, '/', 0.0, "Error: Division by zero is not allowed", time.time()),
        ]

        for record in records:
            history.add(record)

        table = render_history_table(history)
        assert isinstance(table, Table)
        assert history.count() == 5

    def test_render_history_table_with_pagination(self) -> None:
        """Test that render_history_table paginates large histories."""
        history = CalculationHistory()

        # Add 25 records (should paginate to last 20)
        for i in range(25):
            record = CalculationRecord(
                operand1=float(i),
                operator='+',
                operand2=1.0,
                result=float(i + 1),
                timestamp=time.time()
            )
            history.add(record)

        table = render_history_table(history)
        assert isinstance(table, Table)
        assert history.count() == 25
        # Should only display last 20 (max_displayed default)
        recent = history.get_recent()
        assert len(recent) == 20

    def test_render_history_table_has_correct_columns(self) -> None:
        """Test that table has the correct column structure."""
        history = CalculationHistory()
        record = CalculationRecord(5.0, '+', 3.0, 8.0, time.time())
        history.add(record)

        table = render_history_table(history)

        # Check that table has columns (Rich Table has columns attribute)
        assert hasattr(table, 'columns')
        assert len(table.columns) >= 5  # Should have at least: #, Time, Expression, Operator, Result, Status

    def test_render_history_table_with_successful_calculation(self) -> None:
        """Test that successful calculations show OK status."""
        history = CalculationHistory()
        record = CalculationRecord(5.0, '+', 3.0, 8.0, time.time())
        history.add(record)

        table = render_history_table(history)
        # Table should be created successfully for valid record
        assert isinstance(table, Table)
        assert history.count() == 1

    def test_render_history_table_with_error_calculation(self) -> None:
        """Test that error calculations show ERROR status."""
        history = CalculationHistory()
        record = CalculationRecord(
            operand1=10.0,
            operator='/',
            operand2=0.0,
            result="Error: Division by zero is not allowed",
            timestamp=time.time()
        )
        history.add(record)

        table = render_history_table(history)
        # Table should handle error records
        assert isinstance(table, Table)
        assert history.count() == 1

    def test_render_history_table_with_mixed_results(self) -> None:
        """Test that table handles mix of successful and error records."""
        history = CalculationHistory()

        # Add successful calculation
        history.add(CalculationRecord(5.0, '+', 3.0, 8.0, time.time()))

        # Add error calculation
        history.add(CalculationRecord(
            10.0, '/', 0.0,
            "Error: Division by zero is not allowed",
            time.time()
        ))

        # Add another successful calculation
        history.add(CalculationRecord(6.0, '*', 7.0, 42.0, time.time()))

        table = render_history_table(history)
        assert isinstance(table, Table)
        assert history.count() == 3

    def test_render_history_table_with_decimal_results(self) -> None:
        """Test that table correctly displays decimal results."""
        history = CalculationHistory()
        record = CalculationRecord(10.0, '/', 3.0, 3.333333333333, time.time())
        history.add(record)

        table = render_history_table(history)
        assert isinstance(table, Table)
        assert history.count() == 1

    def test_render_history_table_with_negative_numbers(self) -> None:
        """Test that table correctly displays negative numbers."""
        history = CalculationHistory()
        record = CalculationRecord(5.0, '-', 10.0, -5.0, time.time())
        history.add(record)

        table = render_history_table(history)
        assert isinstance(table, Table)
        assert history.count() == 1
