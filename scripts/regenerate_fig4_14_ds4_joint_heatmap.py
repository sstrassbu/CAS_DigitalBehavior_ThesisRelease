"""Regenerate Fig 4.14 (DS4 behavioral x network partition cross-tabulation), thesis width, no title.

Restyle only: redraws from the already-computed Path A' / Path C' cluster assignments; no re-fitting.
Source notebook: notebooks/133_ds4_hierarchical_phenotype.ipynb.
LaTeX placement: width=0.75\\textwidth (09_lenses_framework.tex). The chi-square p-value that was
in the title now sits in the plot as an annotation (caption can still cite it).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import chi2_contingency

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

DATA_DIR = ts.ROOT / "outputs" / "model_outputs" / "ds4_phenotyping"
OUT_DIR = DATA_DIR / "figures"


def main() -> None:
    ts.apply()
    path_a = pd.read_csv(DATA_DIR / "path_a_feature_matrix.csv")[
        ["participant_id_canonical", "path_a_cluster"]]
    path_c = pd.read_csv(DATA_DIR / "path_c_feature_matrix.csv")[
        ["participant_id_canonical", "path_c_cluster"]]
    joint = path_a.merge(path_c, on="participant_id_canonical", how="inner")

    ct = pd.crosstab(joint["path_a_cluster"], joint["path_c_cluster"])
    _, p_value, _, _ = chi2_contingency(ct)
    print(f"chi2 p = {p_value:.4f}, table:\n{ct}")

    fig, ax = plt.subplots(figsize=(ts.W_075, 3.6))
    im = ax.imshow(ct.values, cmap="Purples")
    ax.set_xticks(range(ct.shape[1]))
    ax.set_xticklabels([f"net {c}" for c in ct.columns])
    ax.set_yticks(range(ct.shape[0]))
    ax.set_yticklabels([f"behav {r}" for r in ct.index])
    for i in range(ct.shape[0]):
        for j in range(ct.shape[1]):
            ax.text(j, i, ct.values[i, j], ha="center", va="center", fontsize=ts.FS_LABEL + 1,
                    color="white" if ct.values[i, j] > ct.values.max() / 2 else "black")
    ax.set_xlabel("Path C' network cluster")
    ax.set_ylabel("Path A' behavior cluster")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Participants (n)", fontsize=ts.FS_LABEL)
    cbar.ax.tick_params(labelsize=ts.FS_TICK)
    p_txt = "$p < 0.001$" if p_value < 0.001 else f"$p = {p_value:.3f}$"
    ax.text(0.5, -0.20, f"$\\chi^2$ test: {p_txt}", transform=ax.transAxes,
            ha="center", va="top", fontsize=ts.FS_ANNOT)
    fig.tight_layout()

    for path in ts.save(fig, "DS4_onesec", "path_f_fig1_joint_heatmap.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
