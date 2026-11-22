"""Regenerate DS4 fixed-point validation scatter at thesis width, no title.

Extracted from notebooks/55_ds4_dynamical_systems.ipynb cell 14 (restyle only; no refit).
Reads the saved per-participant table that the notebook wrote; valid_fp == rows with
fit_valid True (N=641), exactly as in the notebook.
LaTeX placement: width=0.75\\textwidth (Empirical_Results_Appendix.tex).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

DATA = ts.ROOT / "outputs" / "model_outputs" / "ds4_dynamical_systems" / "participant_dynamics_parameters.csv"
OUT_DIR = ts.ROOT / "outputs" / "model_outputs" / "ds4_dynamical_systems" / "figures"


def main() -> None:
    ts.apply()
    dys = pd.read_csv(DATA)
    valid_fp = dys[dys["fit_valid"]]
    r_val = valid_fp["x_mean_raw"].corr(valid_fp["mu_hat_OU"])
    print(f"N valid = {len(valid_fp)}, r = {r_val:.4f}")

    fig, ax = plt.subplots(figsize=(ts.W_075, 3.5))
    ax.scatter(valid_fp["mu_hat_OU"], valid_fp["x_mean_raw"], s=9, alpha=0.6, color="#55A868")
    ax.plot([0, 1], [0, 1], color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Fitted long-run mean ($\\hat{\\mu}_{OU}$)")
    ax.set_ylabel("Empirical participant mean")
    ax.text(0.04, 0.95, f"$r = {r_val:.4f}$,  $N = {len(valid_fp)}$", transform=ax.transAxes,
            ha="left", va="top", fontsize=ts.FS_ANNOT)
    fig.tight_layout()

    for path in ts.save(fig, "DS4_onesec", "fig3_ds4_fixedpoint_validation.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
