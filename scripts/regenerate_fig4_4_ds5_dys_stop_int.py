"""Regenerate Fig 4.4 (DS5 low-noise and low-entropy overlap) at thesis width, no title.

Restyle only: redraws from the already-computed cross-model comparison table; no re-fitting.
Source notebook: notebooks/42_ds5_dynamical_systems.ipynb (cell "Figure 4").
LaTeX placement: width=0.75\\textwidth -> drawn at ts.W_075 so fonts print at true size.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

DATA = ts.ROOT / "outputs" / "model_outputs" / "dynamical_systems" / "dys_stop_int_comparison.csv"
OUT_DIR = ts.ROOT / "outputs" / "model_outputs" / "dynamical_systems" / "figures"

COND_ORDER, COND_COLORS = ts.COND_ORDER, ts.COND_COLORS


def main() -> None:
    ts.apply()
    merged = pd.read_csv(DATA)

    fig, ax = plt.subplots(figsize=(ts.W_075, 3.7))

    for cond in COND_ORDER:
        dys_sub = merged[(merged["study_condition"] == cond) & merged["is_dys_eligible"]]
        stop_sub = merged[(merged["study_condition"] == cond) & ~merged["is_dys_eligible"]]
        ax.scatter(dys_sub["sig_hat"], dys_sub["H_emp"],
                   color=COND_COLORS[cond], alpha=0.65, s=16, marker="o",
                   label=f"{ts.COND_LABELS[cond]}, DyS-eligible")
        ax.scatter(stop_sub["sig_hat"], stop_sub["H_emp"],
                   color=COND_COLORS[cond], alpha=0.20, s=9, marker="s")

    sigma_threshold = merged["sig_hat"].median()
    hemp_thresh = merged["H_emp"].median()
    ax.axvline(sigma_threshold, color="black", lw=1.1, ls="--", alpha=0.6,
               label=f"σ̂ median = {sigma_threshold:.3f}")
    ax.axhline(hemp_thresh, color="darkred", lw=1.0, ls="--", alpha=0.6,
               label=f"$H_{{emp}}$ median = {hemp_thresh:.2f}")

    xmin = merged["sig_hat"].min() * 0.95
    ax.fill_betweenx([merged["H_emp"].min() * 0.95, hemp_thresh],
                     xmin, sigma_threshold,
                     alpha=0.08, color="green", label="Low-σ̂, low-$H_{emp}$ region")

    ax.set_xlabel("σ̂ (increment variability)")
    ax.set_ylabel("$H_{emp}$ (bits)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False,
              columnspacing=1.2, handletextpad=0.4, labelspacing=0.3)
    fig.tight_layout()

    for path in ts.save(fig, "DS5_onesec", "fig4_dys_stop_int.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
