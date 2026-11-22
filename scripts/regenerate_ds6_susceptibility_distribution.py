"""Regenerate DS6 susceptibility histogram at thesis width, no title.

Extracted from notebooks/71_ds6_statistical_mechanics.ipynb cell 16 (restyle only; no refit).
Reads the saved participant_macrostate_metrics.csv (same `susceptibility` column the notebook
plotted from macro_df). LaTeX placement: width=0.75\\textwidth (Empirical_Results_Appendix.tex).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

SM_DIR = ts.ROOT / "outputs" / "model_outputs" / "ds6" / "statistical_mechanics"
OUT_DIR = SM_DIR / "figures"


def main() -> None:
    ts.apply()
    macro_df = pd.read_csv(SM_DIR / "participant_macrostate_metrics.csv")
    vals = macro_df["susceptibility"].dropna()
    print(f"N = {len(vals)}, mean = {vals.mean():.4f}")

    fig, ax = plt.subplots(figsize=(ts.W_075, 3.3))
    ax.hist(vals, bins=40, color="#C44E52", alpha=0.8)
    ax.axvline(vals.mean(), color="black", linestyle="--", linewidth=1.2,
               label=f"Mean = {vals.mean():.3f}")
    ax.set_xlabel("Susceptibility (JS divergence, bits)")
    ax.set_ylabel("Participants")
    ax.legend(frameon=False)
    fig.tight_layout()

    for path in ts.save(fig, "DS6_onesec", "fig3_stm_susceptibility_distribution.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
