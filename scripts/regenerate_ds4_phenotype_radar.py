"""Regenerate the DS4 phenotype radar (thesis Figure 4.13) at thesis width (5.9 in).

Restyle only. Previously drawn ~36 in wide and shrunk ~0.16x by LaTeX; now drawn at the
placed width (width=\\textwidth) as a 2x2 grid (3 cluster radars + legend cell) with
model-family / layer legends in a bottom row, so the fonts below print at true size.
No title; each radar carries a short panel label.

Loads the already-fitted DS4 cluster assignment (notebooks/59_ds4_phenotype_exploration.ipynb,
cell 19-20) from its frozen CSV output -- does not refit KMeans, so the cluster
solution reported in the thesis text cannot drift from this styling-only change.
"""

import sys
from collections import OrderedDict
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

ROOT = ts.ROOT
FEATURE_MATRIX = ROOT / "outputs" / "model_outputs" / "ds4_phenotyping" / "ds4_phenotype_feature_matrix.csv"
OUT_DIR = ROOT / "outputs" / "model_outputs" / "ds4_phenotyping" / "figures"

# Font sizes in pt at final printed size (figure is drawn at placed width).
FONT_SIZES = {
    "axis_labels": 7,
    "grid_ticks": 6,
    "legends": 7,
    "legend_titles": 7.5,
}

RADAR_DIMS = OrderedDict([
    ("Relaxation\ntime", "tau_hat"),                     # StoP
    ("Behavioral\nentropy", "H_emp"),                    # InT
    ("Model-fit\ndeviation", "fixed_point_deviation"),   # DyS
    ("Susceptibility", "chi_OU"),                        # StM
    ("Self-\ntransition", "rho_self"),                   # NeT
])
AXIS_MODEL = {
    "Relaxation\ntime": "StoP", "Behavioral\nentropy": "InT",
    "Model-fit\ndeviation": "DyS", "Susceptibility": "StM",
    "Self-\ntransition": "NeT",
}
MODEL_COLORS = {
    "InT": "#2196F3", "StoP": "#FF9800", "DyS": "#9C27B0",
    "NeT": "#4CAF50", "StM": "#C5D307",
}
SECTION_LAYERS = [
    {"name": "Behavioral dynamics", "dim_idx": [0, 1, 2], "color": "#C62828"},
    {"name": "Thermodynamic", "dim_idx": [3], "color": "#0A4B96"},
    {"name": "Network structure", "dim_idx": [4], "color": "#044B07"},
]
CLUSTER_COLORS = {0: "#A20A7C", 1: "#7E57C2", 2: "#00897B", 3: "#EF6C00", 4: "#3949AB"}


def normalize_features(df, dim_feats):
    norm = {}
    for feat in dim_feats:
        v = df[feat].dropna()
        norm[feat] = (df[feat] - v.min()) / (v.max() - v.min() + 1e-12)
    return norm


def draw_model_arcs(ax, angles, dim_labels, axis_model, model_colors,
                     arc_r=1.18, arc_lw=3, label_r=1.34, fontsize=6):
    half_gap = (2 * np.pi / len(angles)) * 0.38
    family_angles = {}
    for label, angle in zip(dim_labels, angles):
        model = axis_model.get(label, "")
        color = model_colors.get(model, "#AAAAAA")
        theta = np.linspace(angle - half_gap, angle + half_gap, 40)
        ax.plot(theta, np.full_like(theta, arc_r), color=color, lw=arc_lw,
                solid_capstyle="round", clip_on=False, zorder=10)
        family_angles.setdefault(model, []).append(angle)
    for model, ang_list in family_angles.items():
        mid = np.arctan2(np.mean(np.sin(ang_list)), np.mean(np.cos(ang_list)))
        color = model_colors.get(model, "#AAAAAA")
        ax.text(mid, label_r, model, ha="center", va="center", fontsize=fontsize,
                fontweight="bold", color=color, clip_on=False, zorder=11,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, lw=0.8, alpha=0.90))


def draw_section_layers(ax, angles, section_layers, band_inner=1.09, band_outer=1.20):
    step = angles[1] - angles[0]
    half = step / 2
    for sec in section_layers:
        idx = sec["dim_idx"]
        color = sec["color"]
        a0 = angles[idx[0]] - half
        a1 = angles[idx[-1]] + half
        theta = np.linspace(a0, a1, 300)
        ax.fill_between(theta, band_inner, band_outer, color=color, alpha=0.13,
                         clip_on=False, zorder=5)
        ax.plot(theta, np.full_like(theta, band_inner), color=color, lw=0.8,
                alpha=0.40, clip_on=False, zorder=6)
        ax.plot(theta, np.full_like(theta, band_outer), color=color, lw=0.8,
                alpha=0.40, clip_on=False, zorder=6)


def draw_axis_label_boxes(ax, angles, dim_labels, label_r=1.33):
    for label, angle in zip(dim_labels, angles):
        ax.text(angle, label_r, label, ha="center", va="center",
                fontsize=FONT_SIZES["axis_labels"], color="#222222",
                clip_on=False, zorder=25, multialignment="center",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#BBBBBB", lw=0.6, alpha=0.97))


def compute_iqr_band(sub_df, norm_cols):
    q25 = sub_df[norm_cols].quantile(0.25).to_numpy(dtype=float)
    q75 = sub_df[norm_cols].quantile(0.75).to_numpy(dtype=float)
    mean = sub_df[norm_cols].mean(skipna=True).to_numpy(dtype=float)
    close = lambda arr: np.append(arr, arr[0])
    return close(q25), close(q75), close(mean)


def plot_single_profile(ax, sub_df, norm_cols, angles, profile_name, color, dim_labels,
                         axis_model, model_colors, section_layers,
                         individual_alpha=0.15, individual_lw=0.3, mean_lw=1.5):
    for _, row in sub_df.iterrows():
        v = np.append(row[norm_cols].to_numpy(dtype=float), row[norm_cols].iloc[0])
        ax.plot(angles, v, color=color, alpha=individual_alpha, lw=individual_lw, zorder=1)
    q25, q75, mean_vals = compute_iqr_band(sub_df, norm_cols)
    ax.fill_between(angles, q25, q75, color=color, alpha=0.22, zorder=2)
    ax.plot(angles, q25, color=color, alpha=0.45, lw=0.6, ls="--", zorder=4)
    ax.plot(angles, q75, color=color, alpha=0.45, lw=0.6, ls="--", zorder=4)
    ax.plot(angles, mean_vals, "o-", color=color, lw=mean_lw, ms=3,
            markerfacecolor="white", markeredgecolor=color, markeredgewidth=0.9,
            label=f"{profile_name} mean (n={len(sub_df)})", zorder=5)
    ax.fill(angles, mean_vals, color=color, alpha=0.10, zorder=3)
    draw_model_arcs(ax, angles[:-1], dim_labels, axis_model, model_colors)
    draw_section_layers(ax, angles[:-1], section_layers)
    draw_axis_label_boxes(ax, angles[:-1], dim_labels)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([""] * len(dim_labels))
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.50, 0.75, 1.00])
    ax.set_yticklabels(["0.25", "0.50", "0.75", ""], fontsize=FONT_SIZES["grid_ticks"],
                        alpha=0.5, color="#555555")
    ax.spines["polar"].set_color("#272727")
    ax.spines["polar"].set_linewidth(0.6)
    ax.grid(color="#121111", lw=0.4)


def plot_phenotype_profiles_multi(df, cluster_col):
    available = OrderedDict((k, v) for k, v in RADAR_DIMS.items() if v in df.columns)
    dim_labels = list(available.keys())
    dim_feats = list(available.values())
    am = {k: AXIS_MODEL[k] for k in dim_labels}

    norm_map = normalize_features(df, dim_feats)
    radar_df = df.copy()
    for feat in dim_feats:
        radar_df[f"{feat}_norm"] = norm_map[feat]
    norm_cols = [f"{feat}_norm" for feat in dim_feats]

    angles = np.linspace(0, 2 * np.pi, len(dim_labels), endpoint=False)
    angles = np.append(angles, angles[0])

    clusters = sorted(df[cluster_col].unique())
    k = len(clusters)
    # 2 x 2 radar grid (3 clusters + legend cell) + one bottom row for the two other legends.
    fig = plt.figure(figsize=(ts.W_FULL, 7.0))
    gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.36], wspace=0.60, hspace=0.52,
                          left=0.09, right=0.93, top=0.97, bottom=0.01)
    axes = [fig.add_subplot(gs[i // 2, i % 2], projection="polar") for i in range(k)]
    leg_ax = fig.add_subplot(gs[1, 1]) if k == 3 else None
    if leg_ax is not None:
        leg_ax.axis("off")

    for letter, (c, ax) in zip("abcd", zip(clusters, axes)):
        sub = radar_df[radar_df[cluster_col] == c].copy()
        color = CLUSTER_COLORS.get(c, "#888888")
        if sub.empty:
            ax.set_title(f"cluster {c}\n(no data)")
            continue
        plot_single_profile(ax=ax, sub_df=sub, norm_cols=norm_cols, angles=angles,
                             profile_name=f"cluster {c}", color=color, dim_labels=dim_labels,
                             axis_model=am, model_colors=MODEL_COLORS,
                             section_layers=SECTION_LAYERS)
        ax.text(-0.17, 1.13, f"({letter}) cluster {c}", transform=ax.transAxes, ha="left", va="top",
                fontsize=ts.FS_PANEL - 1, fontweight="bold", color=color)

    profile_patches = [
        mpatches.Patch(facecolor=CLUSTER_COLORS.get(c, "#888888"),
                        label=f"cluster {c} mean (n={(df[cluster_col] == c).sum()})")
        for c in clusters
    ]
    profile_patches.append(mpatches.Patch(facecolor="grey", alpha=0.35,
                                           label="IQR band (25th-75th pct.)"))
    leg0 = leg_ax.legend(handles=profile_patches, loc="center", ncol=1,
                          fontsize=FONT_SIZES["legends"], framealpha=0.95, edgecolor="#CCCCCC",
                          title="Clusters (mean line + IQR)", title_fontsize=FONT_SIZES["legend_titles"])

    def _desc(m):
        return {"InT": "Information Theory", "StoP": "Stochastic Processes",
                "DyS": "Dynamical Systems", "NeT": "Network Theory",
                "StM": "Statistical Mechanics"}.get(m, m)

    arc_patches = [mpatches.Patch(color=col, label=f"{m} — {_desc(m)}")
                   for m, col in MODEL_COLORS.items()]
    sec_patches = [mpatches.Patch(color=s_["color"], alpha=0.55, label=s_["name"])
                   for s_ in SECTION_LAYERS]
    bl = fig.add_subplot(gs[2, 0]); bl.axis("off")
    br = fig.add_subplot(gs[2, 1]); br.axis("off")
    bl.legend(handles=arc_patches, loc="center", ncol=1, fontsize=FONT_SIZES["legends"],
              framealpha=0.95, edgecolor="#CCCCCC", title="Model families (axis color)",
              title_fontsize=FONT_SIZES["legend_titles"])
    br.legend(handles=sec_patches, loc="center", ncol=1, fontsize=FONT_SIZES["legends"],
              framealpha=0.95, edgecolor="#CCCCCC", title="Conceptual layers (band color)",
              title_fontsize=FONT_SIZES["legend_titles"])

    return fig


def main():
    ts.apply()
    complete = pd.read_csv(FEATURE_MATRIX)
    fig = plot_phenotype_profiles_multi(complete, cluster_col="cluster")
    for path in ts.save(fig, "DS4_onesec", "fig5_ds4_phenotype_radar.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
