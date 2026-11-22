"""Regenerate the Structured Fano-factor distribution figure at thesis width, no title.

Extracted from notebooks/63_structured_stochastic_processes.ipynb cell 19 (restyle only;
no refit). Data: PRE-RERUN (61-participant) participant_stop_parameters.csv via
structured_old_data.read_old_csv (caption reports N=43 created / N=38 completed).
LaTeX placement: width=\\textwidth (Empirical_Results_Appendix.tex).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402
from structured_old_data import read_old_csv  # noqa: E402

OUT_DIR = ts.ROOT / "outputs" / "model_outputs" / "structured" / "stochastic_processes" / "figures"


def main() -> None:
    ts.apply()
    stop_df = read_old_csv("stochastic_processes/participant_stop_parameters.csv")
    elig_c = stop_df[stop_df["created_is_eligible"]]
    elig_p = stop_df[stop_df["completed_is_eligible"]]
    print(f"N created = {len(elig_c)}, N completed = {len(elig_p)}")

    fig, axes = plt.subplots(1, 2, figsize=(ts.W_FULL, 2.6))
    axes[0].hist(elig_c["created_Fano_factor"].dropna(), bins=15, color="#4C72B0", edgecolor="white")
    axes[1].hist(elig_p["completed_Fano_factor"].dropna(), bins=15, color="#DD8452", edgecolor="white")
    panel_labels = ["Timed-task creations", "Completion markings"]
    for ax, label in zip(axes, panel_labels):
        ax.axvline(1, color="red", ls="--", lw=1.2, label="Poisson ($F=1$)")
        ax.set_title(label)
        ax.set_xlabel("Fano factor")
        ax.legend(loc="upper right", frameon=False)
    for ax in axes:
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    axes[0].set_ylabel("Participants")
    fig.tight_layout(w_pad=1.5)

    for path in ts.save(fig, "structured", "fig2_stop_fano_distribution.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
