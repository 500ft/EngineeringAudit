"""Shared figure rules for study plots: type sizes, ticks, legends, colours and export.

Plots call ``apply()`` before drawing and ``save()`` to write every format.
Only presentation lives here; no plotted value is computed in this module.
"""
from pathlib import Path

import matplotlib.pyplot as plt

# One colour and marker per artifact variant. Every figure uses the same pair,
# so a variant keeps its colour wherever it appears. Blue/red follows the
# enclosure reference figures and stays distinct under deuteranopia; the
# marker shape repeats the distinction without colour.
VARIANTS = {
    "correct_control": {"label": "Control", "color": "#2980b9", "marker": "o"},
    "modulus_fault": {"label": "Half modulus", "color": "#c0392b", "marker": "s"},
}
REFERENCE_COLOR = "#6b7280"
GRID_COLOR = "#e5e7eb"

# Three type sizes, chosen by role: titles and axis labels, then legend and
# annotation text, then tick labels. Panel letters are the only exception.
TITLE_SIZE, NOTE_SIZE, TICK_SIZE = 9, 8, 7
LETTER_SIZE = 11
DPI = 300


def apply() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": TITLE_SIZE,
        "axes.titlesize": TITLE_SIZE,
        "axes.labelsize": TITLE_SIZE,
        "legend.fontsize": NOTE_SIZE,
        "xtick.labelsize": TICK_SIZE,
        "ytick.labelsize": TICK_SIZE,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.dpi": DPI,
        # Editable SVG text and stable element ids, so reruns give the same bytes.
        "svg.fonttype": "none",
        "svg.hashsalt": "engineering-audit",
    })


def save(fig, stem: Path, formats=("png", "svg")) -> None:
    """Write ``stem.<ext>`` for each format with no timestamps."""
    for ext in formats:
        path = stem.with_suffix(f".{ext}")
        fig.savefig(path, dpi=DPI, metadata={"Date": None} if ext in ("svg", "pdf") else {})
        if ext == "svg":
            # Matplotlib path lines carry trailing spaces; normalize the text export.
            path.write_text("\n".join(line.rstrip() for line in path.read_text().splitlines()) + "\n")
