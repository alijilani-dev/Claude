"""CLI Calculator package.

A simple command-line calculator supporting basic arithmetic operations.
"""

from typing import Literal

__version__ = "0.2.0"

# Type exports
Operator = Literal["+", "-", "*", "/"]

__all__ = ["Operator", "__version__"]
