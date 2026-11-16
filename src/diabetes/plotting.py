"""Shared figure styling so every chart in the project looks consistent.

Colors come from a validated categorical palette (colorblind-safe pair):
class 0 is always blue and class 1 is always orange, in every figure.
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from diabetes.config import FIGURES_DIR

CLASS_COLORS = {0: "#2a78d6", 1: "#eb6834"}
CLASS_LABELS = {0: "0 - No diabetes", 1: "1 - Diabetes"}
NEUTRAL = "#898781"

# Diverging map for correlations: blue (negative) <-> gray (zero) <-> red (positive).
DIVERGING_CMAP = LinearSegmentedColormap.from_list(
    "blue_gray_red", ["#184f95", "#2a78d6", "#f0efec", "#e34948", "#a32a2a"]
)

_INK = "#0b0b0b"
_INK_SECONDARY = "#52514e"
_GRID = "#e1e0d9"
_AXIS = "#c3c2b7"


def apply_style() -> None:
    """Set recessive grid/axes and readable text for all subsequent plots."""
    plt.rcParams.update({
        "figure.facecolor": "#fcfcfb",
        "axes.facecolor": "#fcfcfb",
        "axes.edgecolor": _AXIS,
        "axes.labelcolor": _INK_SECONDARY,
        "axes.titlecolor": _INK,
        "axes.titlesize": 11,
        "axes.titleweight": "semibold",
        "axes.labelsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": _GRID,
        "grid.linewidth": 0.6,
        "xtick.color": _INK_SECONDARY,
        "ytick.color": _INK_SECONDARY,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "legend.frameon": False,
        "figure.dpi": 110,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
    })


def save_fig(fig, name: str) -> None:
    """Save a figure as PNG under results/figures/ (used by the report)."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES_DIR / f"{name}.png")
