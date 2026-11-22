"""Regenerate Fig 4.10 (DS5 entropy dimensions by condition) with thesis-width sizing (restyle only).

Also declutters the 5 identical per-panel condition x-tick labels into one shared
color legend at the bottom, since condition is already color-coded consistently
across all 5 panels (user request).

Redraws from the already-computed per-participant entropy table; no re-fitting.
Source notebook: notebooks/45_ds5_information_theory.ipynb (cell "Figure 1").
"""


import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

ROOT = ts.ROOT
DATA = ROOT / "outputs" / "model_outputs" / "information_theory" / "participant_entropy_metrics.csv"
OUT_DIR = ROOT / "outputs" / "model_outputs" / "information_theory" / "figures"
MIN_DAYS = 7

COND_ORDER, COND_LABELS, COND_COLORS = ts.COND_ORDER, ts.COND_LABELS, ts.COND_COLORS


def main() -> None:
    ts.apply()
    profile = pd.read_csv(DATA)

    # 2 x 3 grid (5 panels + legend cell) so each panel is wide enough at 5.9 in.
    fig, axes = plt.subplots(2, 3, figsize=(ts.W_FULL, 4.9))
    axes = axes.ravel()

    measure_info = [
        ("H_out", "$H_{out}$ (bits)", f"Outcome (max {np.log2(2):.0f} bit)"),
        ("H_app", "$H_{app}$ (bits)", "App (decision events)"),
        ("H_hour", "$H_{hour}$ (bits)", "Local hour (decision events)"),
        ("H_emp", "$H_{emp}$ (bits)", f"Daily state (days $\\geq$ {MIN_DAYS})"),
        ("H_SDE", "$H_{SDE}$ (bits)", "Gaussian bridge"),
    ]

    for ax, (measure, ylabel, note) in zip(axes, measure_info):
        parts = ax.violinplot(
            [profile[(profile["study_condition"] == c) & profile[measure].notna()][measure].values
             for c in COND_ORDER],
            positions=range(len(COND_ORDER)),
            showmedians=True,
            showmeans=False,
        )
        for pc, cond in zip(parts["bodies"], COND_ORDER):
            pc.set_facecolor(COND_COLORS[cond])
            pc.set_alpha(0.6)
        for key in ["cmedians", "cmins", "cmaxes", "cbars"]:
            parts[key].set_color("black")
            parts[key].set_linewidth(1.0)

        # Condition identity is carried by colour (shared legend in the 6th cell).
        ax.set_xticks(range(len(COND_ORDER)))
        ax.set_xticklabels([])
        ax.tick_params(axis="x", length=0)
        ax.set_ylabel(ylabel)
        ax.set_title(note, fontsize=ts.FS_ANNOT, color="#444444")

        for i, cond in enumerate(COND_ORDER):
            vals = profile[(profile["study_condition"] == cond) & profile[measure].notna()][measure]
            ax.scatter(i, vals.mean(), color="red", zorder=5, s=24, marker="D")

        if measure == "H_SDE":
            ax.axhline(0, color="gray", lw=0.8, ls="--", alpha=0.5)

        ax.grid(axis="y", alpha=0.3)

    # 6th cell: shared legend
    leg_ax = axes[5]
    leg_ax.axis("off")
    handles = [mpatches.Patch(facecolor=COND_COLORS[c], alpha=0.6, label=COND_LABELS[c]) for c in COND_ORDER]
    handles.append(Line2D([0], [0], marker="D", color="none", markerfacecolor="red",
                          markersize=6, label="Condition mean"))
    handles.append(Line2D([0], [0], color="black", lw=1.0, label="Median"))
    leg_ax.legend(handles=handles, loc="center", frameon=True, edgecolor="#CCCCCC",
                  fontsize=ts.FS_LEGEND + 0.5)

    fig.tight_layout(h_pad=1.2, w_pad=1.0)

    for path in ts.save(fig, "DS5_onesec", "fig1_int_entropy_by_condition.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
