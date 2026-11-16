"""Estilo compartilhado das figuras, para que todos os gráficos do projeto sejam consistentes.

As cores vêm de uma paleta categórica validada (par seguro para daltonismo):
a classe 0 é sempre azul e a classe 1 é sempre laranja, em todas as figuras.
"""

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from diabetes.config import FIGURES_DIR

CLASS_COLORS = {0: "#2a78d6", 1: "#eb6834"}
CLASS_LABELS = {0: "0 - Sem diabetes", 1: "1 - Com diabetes"}
NEUTRAL = "#898781"

# Mapa divergente para correlações: azul (negativa) <-> cinza (zero) <-> vermelho (positiva).
DIVERGING_CMAP = LinearSegmentedColormap.from_list(
    "blue_gray_red", ["#184f95", "#2a78d6", "#f0efec", "#e34948", "#a32a2a"]
)

_INK = "#0b0b0b"
_INK_SECONDARY = "#52514e"
_GRID = "#e1e0d9"
_AXIS = "#c3c2b7"


def apply_style() -> None:
    """Define grade e eixos discretos e texto legível para todos os gráficos seguintes."""
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
    """Salva a figura como PNG em results/figures/ (usada no relatório)."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES_DIR / f"{name}.png")
