"""Regenerate Fig 4.7 (DS6 stochastic-process parameters by period), thesis width, no title.

Restyle only: redraws from the already-fitted per-participant StoP parameter table; no re-fitting.
Source notebook: notebooks/73_ds6_stochastic_processes.ipynb (cell "Figure 1").
LaTeX placement: width=\\textwidth (03_stochastic_processes.tex). The old two-line panel titles
become short panel labels (Baseline / Intervention period); the state-variable note belongs in
the caption.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

DATA = ts.ROOT / "outputs" / "model_outputs" / "ds6" / "stochastic_processes" / "participant_stop_parameters.csv"
OUT_DIR = ts.ROOT / "outputs" / "model_outputs" / "ds6" / "stochastic_processes" / "figures"


def main() -> None:
    ts.apply()
    params = pd.read_csv(DATA)

    fig, ax = plt.subplots(1, 2, figsize=(ts.W_FULL, 2.9), sharex=False, sharey=False)
    for i, (period, label) in enumerate([("baseline", "Baseline period"),
                                          ("intervention", "Intervention period")]):
        sub = params.dropna(subset=[f"mu_hat_{period}", f"sig_hat_{period}"])
        ax[i].scatter(sub[f"mu_hat_{period}"], sub[f"sig_hat_{period}"], alpha=0.5, s=12)
        ax[i].axvline(0, color="gray", linewidth=1.0, linestyle="--")
        ax[i].set_xlabel(r"$\hat{\mu}$ (drift, attempts/day trend)")
        ax[i].set_ylabel(r"$\hat{\sigma}$ (diffusion)")
        ax[i].set_title(f"({'ab'[i]}) {label}", fontsize=ts.FS_PANEL)
        print(period, len(sub))
    fig.tight_layout(w_pad=1.5)

    for path in ts.save(fig, "DS6_onesec", "fig1_stop_mu_sigma_by_period.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
