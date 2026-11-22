"""Shared thesis figure style (restyle only -- no analysis is ever recomputed here).

Why this exists
---------------
The thesis is A4 / 12 pt / 3 cm margins -> text width = 15 cm = 5.9 in. Earlier figures
were drawn 7-26 in wide and then shrunk by LaTeX (e.g. a 22 in panel at 0.27 scale turned
14 pt labels into ~3.8 pt). The fix is to draw each figure at (about) the width it is
placed at, so the font sizes set here are the sizes that actually print.

Usage
-----
    from thesis_style import apply, W_FULL, W_075, COND_COLORS, save
    apply()
    fig, ax = plt.subplots(figsize=(W_075, 3.4))
    ...
    save(fig, "DS5_onesec", "fig4_dys_stop_int.png", outputs_dir=OUT_DIR)

No in-figure titles: the LaTeX caption carries the description. Short per-panel labels
are fine where they identify panels.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
THESIS_FIG = ROOT / "latex_master_thesis" / "figure"

# Figure widths in inches, matching \includegraphics widths (text width = 5.9 in).
W_FULL = 5.9            # width=\textwidth
W_090 = 5.3             # width=0.9\textwidth
W_080 = 4.7             # width=0.8\textwidth
W_075 = 4.4             # width=0.75\textwidth
W_050 = 2.95            # width=0.5\textwidth

# Font sizes in pt at final printed size.
FS_BASE = 9
FS_LABEL = 10
FS_TICK = 9
FS_LEGEND = 8.5
FS_PANEL = 10           # short per-panel titles / letters
FS_ANNOT = 8.5

DPI = 300

# Condition colours: DS5 randomized arms (single source of truth).
COND_ORDER = ["control", "default", "reintervention"]
COND_LABELS = {"control": "Control", "default": "Default", "reintervention": "Reintervention"}
COND_COLORS = {"control": "#218D0E", "default": "#1976D2", "reintervention": "#F57C00"}


def apply() -> None:
    """Install thesis rcParams (call once at the top of a script)."""
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],  # has sigma-hat, subscripts, etc.
            "font.size": FS_BASE,
            "axes.labelsize": FS_LABEL,
            "axes.titlesize": FS_PANEL,
            "axes.titleweight": "normal",
            "xtick.labelsize": FS_TICK,
            "ytick.labelsize": FS_TICK,
            "legend.fontsize": FS_LEGEND,
            "legend.title_fontsize": FS_LEGEND,
            "figure.titlesize": FS_PANEL,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "lines.linewidth": 1.4,
            "figure.dpi": 100,
            "savefig.dpi": DPI,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.04,
        }
    )


def save(fig, thesis_subdir: str, filename: str, outputs_dir: Path | None = None) -> list[Path]:
    """Write fig to latex_master_thesis/figure/<subdir>/ and optionally outputs_dir/.

    Returns the written paths. Existing files are overwritten (a backup of the pre-pass
    thesis figures lives in outputs/backups/pre_style_pass_2026-11-19/).
    """
    targets = [THESIS_FIG / thesis_subdir / filename]
    if outputs_dir is not None:
        targets.insert(0, Path(outputs_dir) / filename)
    for path in targets:
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=DPI, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    return targets
