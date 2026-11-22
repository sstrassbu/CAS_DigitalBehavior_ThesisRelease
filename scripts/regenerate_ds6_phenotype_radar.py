"""Regenerate the DS6 phenotype radar (thesis Figure 4.15) at thesis width (5.9 in).

Restyle only. Previously drawn ~18 in wide and shrunk ~0.33x by LaTeX; now drawn at the
placed width (width=\\textwidth) so the fonts below print at true size. No title; each
radar carries a short panel label. Legends stay in one bottom row.

Loads the already-fitted DS6 cluster assignment (notebooks/140_ds6_phenotype_exploration.ipynb,
cell 19) from its frozen CSV output -- does not refit anything, so the cluster
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
ASSIGNMENTS = ROOT / "outputs" / "model_outputs" / "ds6" / "phenotyping" / "cluster_assignments.csv"
OUT_DIR = ROOT / "outputs" / "model_outputs" / "ds6" / "phenotyping" / "figures"

PROFILE_NAMES = ["Profile A", "Profile B"]

# Font sizes in pt at final printed size (figure is drawn at placed width).
FONT_SIZES = {
    "axis_labels": 7,
    "section_layers": 7,
    "grid_ticks": 6,
    "bottom_legends": 7,
    "legend_titles": 7.5,
}

RADAR_DIMS = OrderedDict([
    ("Trend\nshift", "h_period"),                       # StoP
    ("Predictability\n(baseline)", "H_emp_baseline"),   # InT
    ("Network\nconcentration shift", "hhi_change"),     # NeT
    ("Configuration\nsusceptibility", "susceptibility"),  # StM
    ("Regime\nchanged", "regime_changed"),               # DyS
])
AXIS_MODEL = {
    "Trend\nshift": "StoP", "Predictability\n(baseline)": "InT",
    "Network\nconcentration shift": "NeT", "Configuration\nsusceptibility": "StM",
    "Regime\nchanged": "DyS",
}
MODEL_COLORS = {
    "NeT": "#4CAF50", "InT": "#2196F3", "StoP": "#FF9800",
    "DyS": "#3F51B5", "StM": "#9C27B0",
}
PROFILE_COLOR_CYCLE = ["#A20A7C", "#7E57C2", "#00897B", "#EF6C00"]
PROFILE_COLORS = {name: PROFILE_COLOR_CYCLE[i] for i, name in enumerate(PROFILE_NAMES)}
SECTION_LAYERS = [
    {"name": "Volume & Predictability", "dim_idx": [0, 1], "color": "#C62828"},
    {"name": "Structure Change", "dim_idx": [2, 3], "color": "#0A4B96"},
    {"name": "Regime", "dim_idx": [4], "color": "#2E7D32"},
]


def normalize_features(df, dim_feats):
    norm = {}
    for feat in dim_feats:
        v = df[feat].dropna()
        norm[feat] = (df[feat] - v.min()) / (v.max() - v.min() + 1e-12)
    return norm


def draw_model_arcs(ax, angles, dim_labels, axis_model, model_colors, arc_r=1.04, arc_lw=2.5, alpha=0.45):
    n = len(angles)
    half_gap = (2 * np.pi / n) * 0.40
    for label, angle in zip(dim_labels, angles):
        model = axis_model.get(label, "")
        color = model_colors.get(model, "#AAAAAA")
        theta = np.linspace(angle - half_gap, angle + half_gap, 40)
        ax.plot(theta, np.full_like(theta, arc_r), color=color, lw=arc_lw,
                solid_capstyle="round", alpha=alpha, clip_on=False, zorder=10)


def draw_section_layers(ax, angles, section_layers, band_inner=1.09, band_outer=1.18):
    step = angles[1] - angles[0]
    half = step / 2
    for sec in section_layers:
        idx = sec["dim_idx"]
        color = sec["color"]
        a0 = angles[idx[0]] - half
        a1 = angles[idx[-1]] + half
        theta = np.linspace(a0, a1, 300)
        ax.fill_between(theta, band_inner, band_outer, color=color, alpha=0.13, clip_on=False, zorder=5)
        ax.plot(theta, np.full_like(theta, band_inner), color=color, lw=0.5, alpha=0.40, clip_on=False, zorder=6)
        ax.plot(theta, np.full_like(theta, band_outer), color=color, lw=0.5, alpha=0.40, clip_on=False, zorder=6)


def draw_axis_label_boxes(ax, angles, dim_labels, label_r=1.30):
    for label, angle in zip(dim_labels, angles):
        ax.text(angle, label_r, label, ha="center", va="center",
                fontsize=FONT_SIZES["axis_labels"], color="#222222",
                clip_on=False, zorder=25, multialignment="center",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#BBBBBB", lw=0.6, alpha=0.97))


def compute_iqr_band(sub_df, norm_cols, angles):
    q25 = sub_df[norm_cols].quantile(0.25).to_numpy(dtype=float)
    q75 = sub_df[norm_cols].quantile(0.75).to_numpy(dtype=float)
    mean = sub_df[norm_cols].mean(skipna=True).to_numpy(dtype=float)
    def close(arr): return np.append(arr, arr[0])
    return close(q25), close(q75), close(mean)


def plot_single_profile(ax, sub_df, norm_cols, angles, profile_name, color, dim_labels,
                         axis_model, model_colors, section_layers,
                         individual_alpha=0.25, individual_lw=0.35, mean_lw=1.5):
    for _, row in sub_df.iterrows():
        v = np.append(row[norm_cols].to_numpy(dtype=float), row[norm_cols].iloc[0])
        ax.plot(angles, v, color=color, alpha=individual_alpha, lw=individual_lw, zorder=1)

    q25, q75, mean_vals = compute_iqr_band(sub_df, norm_cols, angles)
    ax.fill_between(angles, q25, q75, color=color, alpha=0.22, zorder=2)
    ax.plot(angles, q25, color=color, alpha=0.45, lw=0.6, ls="--", zorder=4)
    ax.plot(angles, q75, color=color, alpha=0.45, lw=0.6, ls="--", zorder=4)

    ax.plot(angles, mean_vals, "o-", color=color, lw=mean_lw, ms=3,
            markerfacecolor="white", markeredgecolor=color, markeredgewidth=0.9,
            label=f"{profile_name} mean  (n={len(sub_df)})", zorder=5)
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


def plot_phenotype_profiles_enhanced(pop_df, profile_col, participant_col, profile_names,
                                      profile_colors):
    available = OrderedDict((k, v) for k, v in RADAR_DIMS.items() if v in pop_df.columns)
    dim_labels = list(available.keys())
    dim_feats = list(available.values())
    am = {k: AXIS_MODEL[k] for k in dim_labels}

    norm_map = normalize_features(pop_df, dim_feats)
    radar_df = pop_df.copy()
    for feat in dim_feats:
        radar_df[f"{feat}_norm"] = norm_map[feat]
    norm_cols = [f"{feat}_norm" for feat in dim_feats]

    angles = np.linspace(0, 2 * np.pi, len(dim_labels), endpoint=False)
    angles = np.append(angles, angles[0])

    n_profiles = len(profile_names)
    fig = plt.figure(figsize=(ts.W_FULL, 4.2))
    outer = fig.add_gridspec(2, 1, height_ratios=[1, 0.40], hspace=0.02,
                             left=0.08, right=0.92, top=0.97, bottom=0.01)
    top = outer[0].subgridspec(1, n_profiles, wspace=0.70)
    axes = [fig.add_subplot(top[0, i], projection="polar") for i in range(n_profiles)]
    bottom = outer[1].subgridspec(1, 3, wspace=0.10)
    bax = [fig.add_subplot(bottom[0, i]) for i in range(3)]
    for b_ in bax:
        b_.axis("off")

    for letter, (pname, ax) in zip("abcd", zip(profile_names, axes)):
        color = profile_colors[pname]
        sub = radar_df[radar_df[profile_col] == pname].copy()
        if sub.empty:
            ax.set_title(f"{pname}\n(no data)")
            continue
        plot_single_profile(ax=ax, sub_df=sub, norm_cols=norm_cols, angles=angles,
                             profile_name=pname, color=color, dim_labels=dim_labels,
                             axis_model=am, model_colors=MODEL_COLORS, section_layers=SECTION_LAYERS)
        ax.text(-0.17, 1.13, f"({letter}) {pname}", transform=ax.transAxes,
                ha="left", va="top", fontsize=ts.FS_PANEL - 1, fontweight="bold", color=color)

    def _desc(m):
        return {"InT": "Information Theory", "StoP": "Stochastic Processes", "StM": "Statistical Mechanics",
                "NeT": "Network Theory", "DyS": "Dynamical Systems"}.get(m, m)

    graph_patches = [mpatches.Patch(facecolor=profile_colors[p], label=f"{p} mean (n={(pop_df[profile_col] == p).sum()})") for p in profile_names]
    graph_patches.append(mpatches.Patch(facecolor="grey", alpha=0.35, label="IQR band (25th-75th pct.)"))

    arc_patches = [mpatches.Patch(color=c, label=f"{m} — {_desc(m)}") for m, c in MODEL_COLORS.items()]
    sec_patches = [mpatches.Patch(color=s["color"], alpha=0.55, label=s["name"]) for s in SECTION_LAYERS]

    kw = dict(loc="center", ncol=1, fontsize=FONT_SIZES["bottom_legends"], framealpha=0.95,
              edgecolor="#CCCCCC", title_fontsize=FONT_SIZES["legend_titles"])
    bax[0].legend(handles=arc_patches, title="Model families (axis color)", **kw)
    bax[1].legend(handles=graph_patches, title="Profiles (mean line + IQR)", **kw)
    bax[2].legend(handles=sec_patches, title="Conceptual layers (band color)", **kw)
    return fig


def main():
    ts.apply()
    complete_case = pd.read_csv(ASSIGNMENTS)
    fig = plot_phenotype_profiles_enhanced(
        pop_df=complete_case,
        profile_col="cluster_label",
        participant_col="participant_id_canonical",
        profile_names=PROFILE_NAMES,
        profile_colors=PROFILE_COLORS,
    )
    for path in ts.save(fig, "DS6_onesec", "fig4_phenotype_profiles_enhanced.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
