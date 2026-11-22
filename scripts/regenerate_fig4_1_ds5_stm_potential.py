"""Regenerate Fig 4.1 (DS5 condition-level behavioral landscape) at thesis width, no title.

Restyle only: redraws from the already-computed condition-level KDE grid; no re-fitting.
Source notebook: notebooks/41_ds5_statistical_mechanics.ipynb (cell "Figure 3").
LaTeX placement: width=\\textwidth -> drawn at ts.W_FULL.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

DATA = ts.ROOT / "outputs" / "model_outputs" / "statistical_mechanics" / "condition_potential.csv"
OUT_DIR = ts.ROOT / "outputs" / "model_outputs" / "statistical_mechanics" / "figures"

CONDITIONS, COND_COLORS = ts.COND_ORDER, ts.COND_COLORS


def main() -> None:
    ts.apply()
    df_pot = pd.read_csv(DATA)

    fig, axes = plt.subplots(1, 2, figsize=(ts.W_FULL, 2.9))

    ax = axes[0]
    for cond in CONDITIONS:
        sub = df_pot[df_pot["study_condition"] == cond]
        ax.plot(sub["x_grid"].values, sub["kde_density"].values, color=COND_COLORS[cond],
                linewidth=1.8, label=ts.COND_LABELS[cond])
    ax.set_xlabel("$X_t$ (daily override proportion)")
    ax.set_ylabel(r"$\hat{P}_\infty(x)$ (density)")
    ax.set_title("(a) Stationary density", fontsize=ts.FS_PANEL)
    ax.legend(loc="upper left", frameon=False)

    ax = axes[1]
    for cond in CONDITIONS:
        sub = df_pot[df_pot["study_condition"] == cond]
        ax.plot(sub["x_grid"].values, sub["V_x"].values, color=COND_COLORS[cond],
                linewidth=1.8, label=ts.COND_LABELS[cond])
        v_min_loc = float(sub.loc[sub["V_x"].idxmin(), "x_grid"])
        v_min_val = float(sub["V_x"].min())
        ax.scatter([v_min_loc], [v_min_val], color=COND_COLORS[cond], s=32, zorder=5)
    ax.set_xlabel("$X_t$ (daily override proportion)")
    ax.set_ylabel(r"$\hat{V}(x)$ (min = 0)")
    ax.set_title("(b) Potential (dots = minima)", fontsize=ts.FS_PANEL)

    fig.tight_layout(w_pad=1.5)

    for path in ts.save(fig, "DS5_onesec", "fig3_stm_potential_landscape.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
