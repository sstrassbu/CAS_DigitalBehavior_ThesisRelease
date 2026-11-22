"""DS6 configuration change (JS divergence) across condition cohorts, thesis width, no title.

Restyle only: reads saved participant_macrostate_metrics.csv; no re-fitting.
LaTeX placement: width=0.75\\textwidth (01_statistical_mechanics.tex).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

INPUT = ts.ROOT / "outputs" / "model_outputs" / "ds6" / "statistical_mechanics" / "participant_macrostate_metrics.csv"


def main() -> None:
    ts.apply()
    data = pd.read_csv(INPUT, usecols=["study_condition", "susceptibility"])
    order = ["control", "default", "intervention"]
    labels = ["Control", "Default friction", "Intervention"]
    colors = ["#7A4AA8", "#A62BC0", "#B53BB7"]

    grouped = data.groupby("study_condition")["susceptibility"]
    means = [grouped.get_group(c).mean() for c in order]
    sems = [grouped.get_group(c).sem() for c in order]
    counts = [grouped.get_group(c).notna().sum() for c in order]

    fig, ax = plt.subplots(figsize=(ts.W_075, 3.6))
    x = range(len(order))
    for position, mean, sem, color in zip(x, means, sems, colors):
        ax.errorbar(position, mean, yerr=sem, fmt="o", markersize=6, color=color, ecolor=color,
                    elinewidth=1.6, capsize=4, zorder=3)
        ax.annotate(f"{mean:.3f}", (position, mean + sem), xytext=(0, 6), textcoords="offset points",
                    ha="center", va="bottom", fontsize=ts.FS_ANNOT, fontweight="bold", color="#2A3763")

    ax.axhline(0.014, color="#888888", linewidth=1.0, linestyle="--",
               label="Mean finite-sampling reference ≈ 0.014 bits")
    ax.set_xticks(list(x), [f"{l}\n($n={n}$)" for l, n in zip(labels, counts)])
    ax.set_ylabel("Configuration change (JS, bits)")
    ax.set_xlim(-0.55, 2.55)
    ax.set_ylim(0, max(m + s for m, s in zip(means, sems)) + 0.03)
    ax.grid(axis="y", color="#E2E2E2", linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper left", fontsize=ts.FS_LEGEND - 0.5)
    fig.tight_layout()

    for path in ts.save(fig, "DS6_onesec", "fig3_stm_susceptibility_by_condition.png"):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
