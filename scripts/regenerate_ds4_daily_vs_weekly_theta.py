"""Regenerate DS4 daily-vs-weekly relaxation-rate scatter at thesis width, no title.

Extracted from notebooks/53_ds4_stochastic_processes.ipynb cell 17 (restyle only; no refit).
Merges the two saved per-participant tables exactly as the notebook did; both_valid == rows
with fit_valid and fit_valid_weekly (N=291, matches the thesis caption).
LaTeX placement: width=0.75\\textwidth (Empirical_Results_Appendix.tex).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

SP_DIR = ts.ROOT / "outputs" / "model_outputs" / "ds4_stochastic_processes"
OUT_DIR = SP_DIR / "figures"


def main() -> None:
    ts.apply()
    daily = pd.read_csv(SP_DIR / "participant_parameters.csv")
    weekly = pd.read_csv(SP_DIR / "participant_parameters_weekly_sensitivity.csv")
    merged = daily[["participant_id_canonical", "theta_hat_OU", "fit_valid"]].merge(
        weekly[["participant_id_canonical", "theta_hat_OU_weekly", "fit_valid_weekly"]],
        on="participant_id_canonical", how="inner",
    )
    both_valid = merged[merged["fit_valid"] & merged["fit_valid_weekly"]]
    r = both_valid["theta_hat_OU"].corr(both_valid["theta_hat_OU_weekly"])
    print(f"N both valid = {len(both_valid)}, r = {r:.3f}")

    fig, ax = plt.subplots(figsize=(ts.W_075, 3.5))
    ax.scatter(both_valid["theta_hat_OU"], both_valid["theta_hat_OU_weekly"],
               s=10, alpha=0.7, color="#8172B2")
    ax.set_xlabel(r"Daily $\hat{\theta}_{OU}$ (per day)")
    ax.set_ylabel(r"Weekly $\hat{\theta}_{OU}$ (per week)")
    ax.text(0.04, 0.95, f"$N = {len(both_valid)}$,  $r = {r:.3f}$", transform=ax.transAxes,
            ha="left", va="top", fontsize=ts.FS_ANNOT)
    fig.tight_layout()

    for path in ts.save(fig, "DS4_onesec", "fig4_daily_vs_weekly_theta.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
