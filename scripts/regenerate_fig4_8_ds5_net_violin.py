"""Regenerate Fig 4.8 (DS5 multi-app network metrics by condition) at thesis width, no title.

Restyle only: redraws from the already-computed per-participant network metrics table.
Source notebook: notebooks/44_ds5_network_models.ipynb (cell "Figure 1").
LaTeX placement: width=0.9\\textwidth -> drawn at ts.W_090.
"""

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

DATA = ts.ROOT / "outputs" / "model_outputs" / "network_models" / "participant_network_metrics.csv"
OUT_DIR = ts.ROOT / "outputs" / "model_outputs" / "network_models" / "figures"

COND_ORDER, COND_COLORS = ts.COND_ORDER, ts.COND_COLORS


def main() -> None:
    ts.apply()
    net_params = pd.read_csv(DATA)
    net_elig = net_params[net_params["is_net_eligible"] & net_params["study_condition"].notna()].copy()

    fig, axes = plt.subplots(1, 2, figsize=(ts.W_090, 3.4))

    panels = [
        ("HHI_net", "$HHI_{net}$", "(a) Flow concentration"),
        ("H_trans", "$H_{trans}$ (bits)", "(b) Transition entropy"),
    ]
    for ax, (metric, ylabel, title) in zip(axes, panels):
        data = [net_elig[net_elig["study_condition"] == c][metric].dropna().values
                for c in COND_ORDER]
        parts = ax.violinplot(data, positions=range(len(COND_ORDER)), showmedians=True)
        for body, cond in zip(parts["bodies"], COND_ORDER):
            body.set_facecolor(COND_COLORS[cond])
            body.set_alpha(0.70)
        for key in ["cmedians", "cmins", "cmaxes", "cbars"]:
            parts[key].set_color("black")
            parts[key].set_linewidth(1.0)
        # Condition identity is carried by colour (shared legend below).
        ax.set_xticks(range(len(COND_ORDER)))
        ax.set_xticklabels([])
        ax.tick_params(axis="x", length=0)
        ax.set_ylabel(ylabel)
        ax.set_title(title, fontsize=ts.FS_PANEL)
        ax.grid(axis="y", alpha=0.3)

    n_by_cond = {c: int(net_elig[net_elig["study_condition"] == c]["HHI_net"].notna().sum())
                 for c in COND_ORDER}
    handles = [mpatches.Patch(facecolor=COND_COLORS[c], alpha=0.7,
                              label=f"{ts.COND_LABELS[c]} (n={n_by_cond[c]})") for c in COND_ORDER]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, -0.02), fontsize=ts.FS_LEGEND, columnspacing=1.2)
    fig.tight_layout(w_pad=1.5, rect=(0, 0.07, 1, 1))

    for path in ts.save(fig, "DS5_onesec", "fig1_net_hhi_h_trans_by_condition.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
