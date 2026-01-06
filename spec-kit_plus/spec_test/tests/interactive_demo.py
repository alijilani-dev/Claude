"""Interactive demo of Rich Calculator UI.

This script runs the calculator with simulated input to show actual output.
"""

import sys
from unittest.mock import patch

sys.path.insert(0, 'src')

from calculator.rich_cli import run_rich_calculator


def demo_calculator():
    """Run calculator with simulated user input."""
    print("=" * 70)
    print("INTERACTIVE DEMO - Rich Calculator UI")
    print("Simulating: Addition (5+3), Multiplication (6*7), Division (20/4)")
    print("=" * 70)
    print()

    with patch('calculator.ui.menu.questionary.select') as mock_select, \
         patch('calculator.ui.input.questionary.text') as mock_text:

        # Simulate user selections: +, *, /, then exit
        mock_select.return_value.ask.side_effect = ['+', '*', '/', None]

        # Simulate number inputs
        mock_text.return_value.ask.side_effect = [
            '5', '3',      # 5 + 3 = 8
            '6', '7',      # 6 * 7 = 42
            '20', '4',     # 20 / 4 = 5
        ]

        # Run calculator (will show actual Rich output)
        run_rich_calculator()


if __name__ == '__main__':
    demo_calculator()
