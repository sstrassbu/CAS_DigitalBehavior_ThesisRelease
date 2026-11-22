"""Regenerate the Structured phenotype radar (thesis Figure 4.16) at thesis width.

Restyle only: no title, drawn at ts.W_FULL (width=\\textwidth in 09_lenses_framework.tex) so
fonts print at true size. Loads the already-fitted Structured cluster assignment
(notebooks/120_structured_phenotype_exploration.ipynb, cell 19) from its frozen CSV --
does not refit anything.

Data: PRE-RERUN (61-participant era, N=36 complete cases: Profile A n=22, B n=14) via
structured_old_data.read_old_csv, because the thesis text still reports that solution.
Note: this radar is intrinsically dense (7 axes x 2 panels + 3 legends); label/legend
fonts are 7-7.5 pt, slightly below the 8.5-10 pt used for ordinary plots.
"""

import sys
from collections import OrderedDict
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402
from structured_old_data import read_old_csv  # noqa: E402

OUT_DIR = ts.ROOT / "outputs" / "model_outputs" / "structured" / "phenotyping" / "figures"

PROFILE_NAMES = ["Profile A", "Profile B"]

FONT_SIZES = {
    "axis_labels": 7.5,
    "grid_ticks": 6.5,
    "bottom_legends": 6.8,
    "legend_titles": 7.0,
}
FIG_H = 3.95         # inches
POLAR_D = 1.55       # polar axes diameter, inches
LABEL_R = 1.24       # axis-label radius in data units (ylim = 0..1)
PANEL_CY = 2.60      # polar centre height above figure bottom, inches

RADAR_DIMS = OrderedDict([
    ("Structure\nsusceptibility", "susceptibility"),             # StM
    ("Burstiness", "created_Fano_factor"),                       # StoP
    ("Trajectory\ninstability", "state_space_volatility"),       # DyS
    ("Backlog\ntrend", "backlog_trend_slope"),                   # SyD
    ("Network\nconcentration", "HHI_net"),                       # NeT
    ("Completion\npredictability", "H_completion"),              # InT
    ("Mean\ncommitment", "mean_commitment_score"),               # GaT
])
AXIS_MODEL = {
    "Structure\nsusceptibility": "StM", "Burstiness": "StoP",
    "Trajectory\ninstability": "DyS", "Backlog\ntrend": "SyD",
    "Network\nconcentration": "NeT", "Completion\npredictability": "InT",
    "Mean\ncommitment": "GaT",
}
MODEL_COLORS = {
    "NeT": "#4CAF50", "InT": "#2196F3", "StoP": "#FF9800",
    "DyS": "#3F51B5", "SyD": "#00BCD4", "StM": "#9C27B0", "GaT": "#F44336",
}
PROFILE_COLOR_CYCLE = ["#A20A7C", "#7E57C2", "#00897B", "#EF6C00"]
PROFILE_COLORS = {name: PROFILE_COLOR_CYCLE[i] for i, name in enumerate(PROFILE_NAMES)}
SECTION_LAYERS = [
    {"name": "State & Process", "dim_idx": [0, 1], "color": "#C62828"},
    {"name": "Feedback & Flow", "dim_idx": [2, 3], "color": "#0A4B96"},
    {"name": "Structural & Strategic", "dim_idx": [4, 5, 6], "color": "#2E7D32"},
]


def normalize_features(df, dim_feats):
    norm = {}
    for feat in dim_feats:
        v = df[feat].dropna()
        norm[feat] = (df[feat] - v.min()) / (v.max() - v.min() + 1e-12)
    return norm


def draw_model_arcs(ax, angles, dim_labels, axis_model, model_colors, arc_r=1.04, arc_lw=2.0, alpha=0.45):
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


def draw_axis_label_boxes(ax, angles, dim_labels, label_r=LABEL_R):
    """Axis-name boxes anchored by their NEAR edge (left/right/top/bottom by angle) so the
    box starts outside the conceptual-layer band instead of straddling it."""
    for label, angle in zip(dim_labels, angles):
        c, sn = np.cos(angle), np.sin(angle)
        ha = "left" if c > 0.3 else ("right" if c < -0.3 else "center")
        va = "bottom" if sn > 0.8 else ("top" if sn < -0.8 else "center")
        ax.text(angle, label_r, label, ha=ha, va=va,
                fontsize=FONT_SIZES["axis_labels"], color="#222222",
                clip_on=False, zorder=25, multialignment="center",
                bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#BBBBBB", lw=0.6, alpha=0.97))


def compute_iqr_band(sub_df, norm_cols, angles):
    q25 = sub_df[norm_cols].quantile(0.25).to_numpy(dtype=float)
    q75 = sub_df[norm_cols].quantile(0.75).to_numpy(dtype=float)
    mean = sub_df[norm_cols].mean(skipna=True).to_numpy(dtype=float)
    def close(arr): return np.append(arr, arr[0])
    return close(q25), close(q75), close(mean)


def plot_single_profile(ax, sub_df, norm_cols, angles, profile_name, color, dim_labels,
                         axis_model, model_colors, section_layers,
                         individual_alpha=0.25, individual_lw=0.4, mean_lw=1.6):
    for _, row in sub_df.iterrows():
        v = np.append(row[norm_cols].to_numpy(dtype=float), row[norm_cols].iloc[0])
        ax.plot(angles, v, color=color, alpha=individual_alpha, lw=individual_lw, zorder=1)

    q25, q75, mean_vals = compute_iqr_band(sub_df, norm_cols, angles)
    ax.fill_between(angles, q25, q75, color=color, alpha=0.22, zorder=2)
    ax.plot(angles, q25, color=color, alpha=0.45, lw=0.6, ls="--", zorder=4)
    ax.plot(angles, q75, color=color, alpha=0.45, lw=0.6, ls="--", zorder=4)

    ax.plot(angles, mean_vals, "o-", color=color, lw=mean_lw, ms=3,
            markerfacecolor="white", markeredgecolor=color, markeredgewidth=1.0,
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
    ax.set_yticklabels(["0.25", "0.50", "0.75", "1.00"], fontsize=FONT_SIZES["grid_ticks"],
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
    fig = plt.figure(figsize=(ts.W_FULL, FIG_H))
    axes = []
    centers_x = [ts.W_FULL * 0.25, ts.W_FULL * 0.75]
    for cx in centers_x[:n_profiles]:
        rect = [(cx - POLAR_D / 2) / ts.W_FULL, (PANEL_CY - POLAR_D / 2) / FIG_H,
                POLAR_D / ts.W_FULL, POLAR_D / FIG_H]
        axes.append(fig.add_axes(rect, projection="polar"))

    for pname, ax in zip(profile_names, axes):
        color = profile_colors[pname]
        sub = radar_df[radar_df[profile_col] == pname].copy()
        if sub.empty:
            ax.text(0.5, 0.5, "(no data)", transform=ax.transAxes, ha="center")
            continue
        plot_single_profile(ax=ax, sub_df=sub, norm_cols=norm_cols, angles=angles,
                             profile_name=pname, color=color, dim_labels=dim_labels,
                             axis_model=am, model_colors=MODEL_COLORS, section_layers=SECTION_LAYERS)

    def _desc(m):
        return {"InT": "Information Theory", "StoP": "Stochastic Processes", "StM": "Statistical Mechanics",
                "NeT": "Network Theory", "DyS": "Dynamical Systems", "SyD": "System Dynamics",
                "GaT": "Game Theory"}.get(m, m)

    graph_patches = [mpatches.Patch(facecolor=profile_colors[p], label=f"{p} mean") for p in profile_names]
    graph_patches.append(mpatches.Patch(facecolor="grey", alpha=0.35, label="IQR band (25th-75th pct.)"))

    arc_patches = [mpatches.Patch(color=c, label=f"{m} \u2014 {_desc(m)}") for m, c in MODEL_COLORS.items()]
    sec_patches = [mpatches.Patch(color=s["color"], alpha=0.55, label=s["name"]) for s in SECTION_LAYERS]

    kw = dict(fontsize=FONT_SIZES["bottom_legends"], framealpha=0.95, edgecolor="#CCCCCC",
              title_fontsize=FONT_SIZES["legend_titles"], handlelength=1.3, handleheight=0.9,
              labelspacing=0.3, borderpad=0.4, ncol=1)
    # All three legends in one bottom row (left / centre / right).
    leg1 = fig.legend(handles=arc_patches, loc="lower left", bbox_to_anchor=(0.0, 0.0),
                      title="Model families (axis colour)", **kw)
    fig.add_artist(leg1)
    leg0 = fig.legend(handles=graph_patches, loc="lower center", bbox_to_anchor=(0.505, 0.0),
                      title="Profiles (mean + IQR)", **kw)
    fig.add_artist(leg0)
    fig.legend(handles=sec_patches, loc="lower right", bbox_to_anchor=(1.0, 0.0),
               title="Conceptual layers (band colour)", **kw)

    for p in ts.save(fig, "structured", "fig4_phenotype_profiles_enhanced_notitle.png", OUT_DIR):
        print(f"Saved: {p}")


def main():
    ts.apply()
    complete_case = read_old_csv("phenotyping/cluster_assignments.csv")
    print(complete_case["cluster_label"].value_counts().to_dict(), f"N={len(complete_case)}")
    plot_phenotype_profiles_enhanced(
        pop_df=complete_case,
        profile_col="cluster_label",
        participant_col="participant_id",
        profile_names=PROFILE_NAMES,
        profile_colors=PROFILE_COLORS,
    )


if __name__ == "__main__":
    main()
