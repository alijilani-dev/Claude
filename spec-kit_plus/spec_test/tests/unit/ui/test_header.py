"""Unit tests for header rendering component."""

import pytest
from rich.panel import Panel
from rich.box import DOUBLE

from calculator.ui.header import render_header


def test_render_header_returns_panel() -> None:
    """Test that render_header() returns a Rich Panel object."""
    result = render_header()
    assert isinstance(result, Panel)


def test_render_header_contains_correct_title() -> None:
    """Test that panel contains 'Panaversity Calculator v2.0' text."""
    panel = render_header()
    # Panel.renderable contains the content
    content = str(panel.renderable)
    assert "Panaversity Calculator v2.0" in content


def test_render_header_has_cyan_border() -> None:
    """Test that panel has cyan border style."""
    panel = render_header()
    assert panel.border_style == "cyan"


def test_render_header_has_double_box_style() -> None:
    """Test that panel uses DOUBLE box style."""
    panel = render_header()
    assert panel.box == DOUBLE


def test_render_header_has_padding() -> None:
    """Test that panel has proper padding."""
    panel = render_header()
    # Panel padding is a tuple (top, right, bottom, left)
    # We expect (0, 2) which expands to (0, 2, 0, 2)
    assert panel.padding == (0, 2)
