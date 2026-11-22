"""Plot-only regeneration of the two supplemental thesis figures (restyle only, no title).

Reads the ALREADY-SAVED CSVs in outputs/model_outputs/supplemental_verification/ written by
scripts/run_supplemental_thesis_analyses.py (dated 2026-08-13, matching the thesis text).
Does NOT rerun any analysis, permutation test or model fit, and never writes those CSVs.

1. fig_time_valid_path_dependence.png  (Structured; width=0.75\\textwidth)
   inputs: structured_time_valid_path_observations.csv, structured_time_valid_path_test.csv
2. fig2_dys_regime_window_comparison.png  (DS6; width=0.9\\textwidth)
   inputs: ds6_matched_window_parameters.csv (raw + matched regime columns per participant).
   The raw-window transition matrix is a plain crosstab of the saved regime_baseline /
   regime_intervention columns; the matched matrix is cross-checked against the saved
   ds6_matched_regime_transition_matrix.csv.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

SUP = ts.ROOT / "outputs" / "model_outputs" / "supplemental_verification"
FIG_DIR = SUP / "figures"
ORDER = ["declining", "resting", "growing", "stochastic"]


def plot_path_dependence() -> None:
    path = pd.read_csv(SUP / "structured_time_valid_path_observations.csv")
    test = pd.read_csv(SUP / "structured_time_valid_path_test.csv").iloc[0]
    x_col, y_col = test["predictor"], test["outcome"]
    r_within = test["pearson_r_within"]
    p_perm = test["p_within_participant_permutation"]

    path["streak_bin"] = path[x_col].clip(upper=4)
    plotted = path.groupby("streak_bin")[y_col].agg(["mean", "count", "std"]).reset_index()
    plotted["se"] = plotted["std"] / np.sqrt(plotted["count"])

    fig, ax = plt.subplots(figsize=(ts.W_075, 3.4))
    ax.errorbar(plotted["streak_bin"], plotted["mean"], yerr=1.96 * plotted["se"],
                fmt="o-", capsize=3, ms=4, color="#3B6FB6")
    ax.set_xticks(range(5), ["0", "1", "2", "3", "4+"])
    ax.set_xlabel("Prior not-completed streak at task creation")
    ax.set_ylabel("Share of new tasks with structure")
    y_ceiling = (plotted["mean"] + 1.96 * plotted["se"]).max()
    ax.set_ylim(0, max(0.30, y_ceiling * 1.8))
    ax.text(0.03, 0.95, f"Within-person $r$ = {r_within:.3f}\npermutation $p$ = {p_perm:.3f}",
            transform=ax.transAxes, fontsize=ts.FS_ANNOT, va="top")
    fig.tight_layout()
    print(f"path-dependence: r_within={r_within:.3f}, p_perm={p_perm:.3f}, n={len(path)}")
    for p in ts.save(fig, "structured", "fig_time_valid_path_dependence.png", None):
        print(f"Saved: {p}")
    fig = None


def plot_regime_comparison() -> None:
    matched = pd.read_csv(SUP / "ds6_matched_window_parameters.csv")
    raw_matrix = pd.crosstab(matched["regime_baseline"], matched["regime_intervention"]).reindex(
        index=ORDER, columns=ORDER, fill_value=0)
    matched_matrix = pd.crosstab(matched["regime_baseline_matched"],
                                 matched["regime_intervention_matched"]).reindex(
        index=ORDER, columns=ORDER, fill_value=0)
    saved = pd.read_csv(SUP / "ds6_matched_regime_transition_matrix.csv", index_col=0)
    assert (saved.values == matched_matrix.values).all(), "matched matrix != saved matrix"
    print(f"regime matrices: N raw={raw_matrix.values.sum()}, N matched={matched_matrix.values.sum()}")

    fig, axes = plt.subplots(1, 2, figsize=(ts.W_090, 3.3), sharey=True, constrained_layout=True)
    vmax = max(raw_matrix.values.max(), matched_matrix.values.max())
    for ax, matrix, title in [(axes[0], raw_matrix, "Original unequal windows"),
                              (axes[1], matched_matrix, "Equal-length windows")]:
        # shared 0..max colour scale so both panels are directly comparable
        image = ax.imshow(matrix.values, cmap="viridis", vmin=0, vmax=vmax)
        ax.set_xticks(range(4), ORDER, rotation=40, ha="right")
        ax.set_yticks(range(4), ORDER)
        ax.set_xlabel("Intervention regime")
        ax.set_title(title)
        for i in range(4):
            for j in range(4):
                v = matrix.values[i, j]
                color = "white" if (v > vmax / 2 or v < 0.12 * vmax) else "black"
                ax.text(j, i, int(matrix.values[i, j]), ha="center", va="center",
                        color=color, fontsize=ts.FS_ANNOT)
    axes[0].set_ylabel("Baseline regime")
    cbar = fig.colorbar(image, ax=axes, shrink=0.85, pad=0.02, aspect=18)
    cbar.set_label("Participants")
    cbar.ax.tick_params(labelsize=ts.FS_TICK - 1)
    for p in ts.save(fig, "DS6_onesec", "fig2_dys_regime_window_comparison.png", None):
        print(f"Saved: {p}")


def main() -> None:
    ts.apply()
    plot_path_dependence()
    plot_regime_comparison()


if __name__ == "__main__":
    main()
