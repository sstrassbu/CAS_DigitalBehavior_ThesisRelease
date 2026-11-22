"""Regenerate the DS5 Phase-1 phenotype radar (thesis Figure, ``..._enhanced_notitle``)
at thesis width, no title.

Extracted from notebooks/100_phenotype_exploration.ipynb cell 26 (restyle only).
Nothing is refit: cluster labels come from the frozen
``phenotyping/ds5_cluster_assignments.csv`` (N=209, column ``profile_p1``) and the 7 radar
features are merged from the saved per-participant model CSVs listed in notebook cell 4
(InT: H_emp, H_hour; StoP: sig_hat, x_mean; StM: chi_behav; NeT: HHI_net, rho_self).
Min-max normalisation is over the Phase-1 population exactly as in the notebook.

LaTeX placement: width=\\textwidth -> drawn at ts.W_FULL.
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

MODEL_ROOT = ts.ROOT / "outputs" / "model_outputs"
ASSIGNMENTS = MODEL_ROOT / "phenotyping" / "ds5_cluster_assignments.csv"
OUT_DIR = MODEL_ROOT / "phenotyping" / "figures"
FILENAME = "fig4_fontphenotype_profiles_enhanced_notitle.png"

FS = {"axis_labels": 7.5, "grid_ticks": 6.5, "legend": 7.5, "legend_title": 8}

RADAR_DIMS = OrderedDict([
    ("Behavioral\nentropy", "H_emp"),       # InT
    ("Impulsivity\n(noise)", "sig_hat"),    # StoP
    ("Override\ntendency", "x_mean"),       # StoP
    ("Susceptibility", "chi_behav"),        # StM
    ("Temporal\nspread", "H_hour"),         # InT
    ("Habitual\nrepetition", "rho_self"),   # NeT
    ("Network\nconcentration", "HHI_net"),  # NeT
])
AXIS_MODEL = {
    "Behavioral\nentropy": "InT", "Impulsivity\n(noise)": "StoP", "Override\ntendency": "StoP",
    "Susceptibility": "StM", "Temporal\nspread": "InT", "Habitual\nrepetition": "NeT",
    "Network\nconcentration": "NeT",
}
# Same colours as the figure currently in the thesis (notebook cell 26).
MODEL_COLORS = {"InT": "#2196F3", "StoP": "#FF9800", "StM": "#C5D307", "NeT": "#2AF431"}
PROFILE_COLORS = {"Profile A": "#A20A7C", "Profile B": "#7E57C2"}
SECTION_LAYERS = [
    {"name": "Behavioral dynamics", "dim_idx": [0, 1, 2], "color": "#C62828"},
    {"name": "Theoretical interpretation", "dim_idx": [3, 4], "color": "#0A4B96"},
    {"name": "Network structure", "dim_idx": [5, 6], "color": "#044B07"},
]
MODEL_DESC = {"InT": "Information Theory", "StoP": "Stochastic Processes",
              "StM": "Statistical Mechanics", "NeT": "Network Theory"}


def load_population() -> pd.DataFrame:
    """Merge saved cluster labels with the 7 radar features (no refit)."""
    a = pd.read_csv(ASSIGNMENTS)[["participant_id_canonical", "study_condition", "profile_p1"]]
    int_raw = pd.read_csv(MODEL_ROOT / "information_theory" / "participant_entropy_metrics.csv")
    stop_raw = pd.read_csv(MODEL_ROOT / "stochastic_processes" / "participant_parameters.csv")
    stm_raw = pd.read_csv(MODEL_ROOT / "statistical_mechanics" / "participant_stm_parameters.csv")
    net_raw = pd.read_csv(MODEL_ROOT / "network_models" / "participant_network_metrics.csv")
    key = "participant_id_canonical"
    df = a.merge(int_raw[[key, "H_emp", "H_hour"]], on=key, how="left")
    df = df.merge(stop_raw[[key, "sig_hat", "x_mean"]], on=key, how="left")
    df = df.merge(stm_raw[[key, "chi_behav"]], on=key, how="left")
    df = df.merge(net_raw[[key, "HHI_net", "rho_self"]], on=key, how="left")
    assert len(df) == len(a), "merge changed row count"
    return df


def normalize_features(df, feats):
    out = {}
    for f in feats:
        v = df[f].dropna()
        out[f] = (df[f] - v.min()) / (v.max() - v.min() + 1e-12)
    return out


def draw_model_arcs(ax, angles, labels, arc_r=1.04, arc_lw=2.2, alpha=0.45):
    half_gap = (2 * np.pi / len(angles)) * 0.40
    for label, angle in zip(labels, angles):
        color = MODEL_COLORS.get(AXIS_MODEL.get(label, ""), "#AAAAAA")
        theta = np.linspace(angle - half_gap, angle + half_gap, 40)
        ax.plot(theta, np.full_like(theta, arc_r), color=color, lw=arc_lw,
                solid_capstyle="round", alpha=alpha, clip_on=False, zorder=10)


def draw_section_layers(ax, angles, band_inner=1.09, band_outer=1.19):
    half = (angles[1] - angles[0]) / 2
    for sec in SECTION_LAYERS:
        idx, color = sec["dim_idx"], sec["color"]
        theta = np.linspace(angles[idx[0]] - half, angles[idx[-1]] + half, 300)
        ax.fill_between(theta, band_inner, band_outer, color=color, alpha=0.13, clip_on=False, zorder=5)
        for r in (band_inner, band_outer):
            ax.plot(theta, np.full_like(theta, r), color=color, lw=0.6, alpha=0.40, clip_on=False, zorder=6)


def draw_axis_label_boxes(ax, angles, labels, label_r=1.42):
    for label, angle in zip(labels, angles):
        ax.text(angle, label_r, label, ha="center", va="center", fontsize=FS["axis_labels"],
                color="#222222", clip_on=False, zorder=25, multialignment="center",
                bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="#BBBBBB", lw=0.6, alpha=0.97))


def plot_single_profile(ax, sub_df, norm_cols, angles, color, labels):
    for _, row in sub_df.iterrows():
        v = np.append(row[norm_cols].to_numpy(dtype=float), row[norm_cols].iloc[0])
        ax.plot(angles, v, color=color, alpha=0.18, lw=0.35, zorder=1)
    q25 = sub_df[norm_cols].quantile(0.25).to_numpy(dtype=float)
    q75 = sub_df[norm_cols].quantile(0.75).to_numpy(dtype=float)
    mean = sub_df[norm_cols].mean(skipna=True).to_numpy(dtype=float)
    close = lambda arr: np.append(arr, arr[0])  # noqa: E731
    q25, q75, mean = close(q25), close(q75), close(mean)
    ax.fill_between(angles, q25, q75, color=color, alpha=0.22, zorder=2)
    ax.plot(angles, q25, color=color, alpha=0.45, lw=0.7, ls="--", zorder=4)
    ax.plot(angles, q75, color=color, alpha=0.45, lw=0.7, ls="--", zorder=4)
    ax.plot(angles, mean, "o-", color=color, lw=1.7, ms=3.2, markerfacecolor="white",
            markeredgecolor=color, markeredgewidth=1.1, zorder=5)
    ax.fill(angles, mean, color=color, alpha=0.10, zorder=3)

    draw_model_arcs(ax, angles[:-1], labels)
    draw_section_layers(ax, angles[:-1])
    draw_axis_label_boxes(ax, angles[:-1], labels)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([""] * len(labels))
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.50, 0.75, 1.00])
    ax.set_yticklabels(["0.25", "0.50", "0.75", "1.00"], fontsize=FS["grid_ticks"],
                       alpha=0.5, color="#555555")
    ax.spines["polar"].set_color("#272727")
    ax.spines["polar"].set_linewidth(0.7)
    ax.grid(color="#121111", lw=0.4)


def main() -> None:
    ts.apply()
    pop = load_population()
    print(pop["profile_p1"].value_counts().to_string(), f"\nN = {len(pop)}")

    labels = list(RADAR_DIMS.keys())
    feats = list(RADAR_DIMS.values())
    norm = normalize_features(pop, feats)
    radar = pop.copy()
    for f in feats:
        radar[f"{f}_norm"] = norm[f]
    norm_cols = [f"{f}_norm" for f in feats]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    angles = np.append(angles, angles[0])

    fig = plt.figure(figsize=(ts.W_FULL, 4.55))
    gs = fig.add_gridspec(2, 2, height_ratios=[3.3, 1.0], hspace=0.02, wspace=0.40,
                          left=0.09, right=0.91, top=0.95, bottom=0.01)
    axes = [fig.add_subplot(gs[0, 0], projection="polar"),
            fig.add_subplot(gs[0, 1], projection="polar")]
    for pname, ax in zip(["Profile A", "Profile B"], axes):
        sub = radar[radar["profile_p1"] == pname]
        plot_single_profile(ax, sub, norm_cols, angles, PROFILE_COLORS[pname], labels)

    leg_kw = dict(fontsize=FS["legend"], title_fontsize=FS["legend_title"], framealpha=0.95,
                  edgecolor="#CCCCCC", borderpad=0.5, labelspacing=0.35, handlelength=1.4)
    profile_patches = [mpatches.Patch(facecolor=PROFILE_COLORS[p], label=f"{p} mean")
                       for p in PROFILE_COLORS]
    profile_patches.append(mpatches.Patch(facecolor="grey", alpha=0.35, label="IQR band (25th–75th pct.)"))
    arc_patches = [mpatches.Patch(color=c, label=f"{m} — {MODEL_DESC[m]}") for m, c in MODEL_COLORS.items()]
    sec_patches = [mpatches.Patch(color=s["color"], alpha=0.55, label=s["name"]) for s in SECTION_LAYERS]

    fig.legend(handles=arc_patches, loc="lower left", bbox_to_anchor=(0.0, 0.0),
               title="Model families (axis colour)", **leg_kw)
    fig.legend(handles=profile_patches, loc="lower center", bbox_to_anchor=(0.5, 0.0),
               title="Profiles (mean + IQR)", **leg_kw)
    fig.legend(handles=sec_patches, loc="lower right", bbox_to_anchor=(1.0, 0.0),
               title="Conceptual layers (band colour)", **leg_kw)

    for path in ts.save(fig, "DS5_onesec", FILENAME, OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
