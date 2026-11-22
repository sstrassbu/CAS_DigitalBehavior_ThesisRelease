"""Regenerate the two DS5 figures requested for the final thesis (thesis-width, no titles).

Restyle only -- data handling (daily table, eligibility, ANOVA) is unchanged.

The trajectory figure uses the final decision-event state definition

    X_t = opened / (opened + dismissed)

LaTeX placement: ds5_indivTrajectory_groupMean_final -> width=\\textwidth (ts.W_FULL);
fig1_stop_params_four_panel -> width=0.8\\textwidth (ts.W_080).
The script writes copies to the analysis-output tree and to the LaTeX figure tree.
"""

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402

ROOT = ts.ROOT
CLEANED = ROOT / "outputs" / "cleaned"
FEATURES = ROOT / "outputs" / "features" / "ds5"
STOP = ROOT / "outputs" / "model_outputs" / "stochastic_processes"
PLAYGROUND = ROOT / "outputs" / "playground_outputs"

COLORS = ts.COND_COLORS
LABELS = {
    "control": "Control",
    "default": "Default friction",
    "reintervention": "Reintervention",
}
ORDER = ts.COND_ORDER


def regenerate_trajectory_figure():
    events = pd.read_csv(CLEANED / "ds5_behavioral_clean.csv", low_memory=False)
    features = pd.read_csv(
        FEATURES / "ds5_behavior_features.csv",
        usecols=["participant_id_canonical", "study_condition"],
    )
    condition_map = features.drop_duplicates("participant_id_canonical").set_index(
        "participant_id_canonical"
    )["study_condition"]
    events["study_condition"] = events["participant_id_canonical"].map(condition_map)

    # Final DS5 state definition: only events that resolve the opening decision.
    decisions = events[
        events["event_outcome_simple"].isin(["opened", "dismissed"])
        & events["study_condition"].isin(ORDER)
    ].copy()
    decisions["event_date"] = pd.to_datetime(
        decisions["event_timestamp_utc"], utc=True, errors="coerce"
    ).dt.normalize()
    decisions = decisions.dropna(subset=["event_date"])

    daily = (
        decisions.groupby(
            ["participant_id_canonical", "study_condition", "event_date"],
            as_index=False,
        )
        .agg(
            n_decisions=("event_outcome_simple", "size"),
            n_opened=("event_outcome_simple", lambda x: (x == "opened").sum()),
        )
        .sort_values(["participant_id_canonical", "event_date"])
    )
    daily["X_t"] = daily["n_opened"] / daily["n_decisions"]
    first_date = daily.groupby("participant_id_canonical")["event_date"].transform("min")
    daily["relative_day"] = (daily["event_date"] - first_date).dt.days

    active_days = daily.groupby("participant_id_canonical")["event_date"].nunique()
    eligible = active_days[active_days >= 14].index
    daily = daily[daily["participant_id_canonical"].isin(eligible)].copy()

    pid_condition = daily.drop_duplicates("participant_id_canonical").set_index(
        "participant_id_canonical"
    )["study_condition"]
    pivot = daily.pivot_table(
        index="participant_id_canonical", columns="relative_day", values="X_t"
    )
    # Restrict the display to the common trial-scale horizon used by the original figure.
    pivot = pivot.loc[:, [c for c in pivot.columns if 0 <= c <= 42]]
    smooth = pivot.T.rolling(window=7, min_periods=1).mean().T

    ts.apply()
    fig, axes = plt.subplots(1, 2, figsize=(ts.W_FULL, 3.0), sharex=True, sharey=True)
    days = smooth.columns.to_numpy(dtype=float)

    for panel, ax in enumerate(axes):
        if panel == 1:
            for pid in smooth.index:
                condition = pid_condition.get(pid)
                if condition in ORDER:
                    ax.plot(
                        days,
                        smooth.loc[pid].to_numpy(dtype=float),
                        color=COLORS[condition],
                        alpha=0.22,
                        linewidth=0.4,
                        zorder=1,
                    )

        for condition in ORDER:
            pids = [pid for pid in smooth.index if pid_condition.get(pid) == condition]
            group_mean = smooth.loc[pids].mean(axis=0, skipna=True).to_numpy(dtype=float)
            ax.plot(
                days,
                group_mean,
                color=COLORS[condition],
                linewidth=2.0,
                label=LABELS[condition],
                zorder=5,
            )

        ax.set_xlim(0, 42)
        ax.set_ylim(-0.02, 1.02)
        ax.set_xlabel("Days since first decision event")
        ax.grid(alpha=0.22, linestyle="--")

    axes[0].set_ylabel("$X_t$ (7-day rolling mean)")
    axes[0].legend(loc="lower right", frameon=True, framealpha=0.9)
    axes[0].set_title("A. Condition means", fontsize=ts.FS_PANEL)
    axes[1].set_title("B. Individual trajectories", fontsize=ts.FS_PANEL)
    fig.tight_layout(w_pad=1.2)

    output_path = PLAYGROUND / "ds5_indivTrajectory_groupMean_final.png"
    thesis_path = ts.THESIS_FIG / "general" / "ds5_indivTrajectory_groupMean_final.png"
    for path in ts.save(fig, "general", "ds5_indivTrajectory_groupMean_final.png", PLAYGROUND):
        pass

    condition_counts = (
        daily.drop_duplicates("participant_id_canonical")["study_condition"]
        .value_counts()
        .reindex(ORDER)
    )
    summary = pd.DataFrame(
        {
            "metric": [
                "eligible_participants",
                "participant_days",
                "decision_events",
                "control_participants",
                "default_participants",
                "reintervention_participants",
            ],
            "value": [
                daily["participant_id_canonical"].nunique(),
                len(daily),
                int(daily["n_decisions"].sum()),
                int(condition_counts["control"]),
                int(condition_counts["default"]),
                int(condition_counts["reintervention"]),
            ],
        }
    )
    summary.to_csv(PLAYGROUND / "ds5_indivTrajectory_groupMean_final_summary.csv", index=False)
    print(summary.to_string(index=False))
    print(f"Saved trajectory figure: {output_path}")
    print(f"Copied trajectory figure: {thesis_path}")


def violin_panel(ax, frame, column, title, equation, ylabel, reference):
    groups = [frame.loc[frame["study_condition"] == c, column].dropna().to_numpy() for c in ORDER]
    parts = ax.violinplot(
        groups,
        positions=np.arange(len(ORDER)),
        showmedians=True,
        showextrema=False,
        widths=0.86,
    )
    for body, condition in zip(parts["bodies"], ORDER):
        body.set_facecolor(COLORS[condition])
        body.set_edgecolor(COLORS[condition])
        body.set_alpha(0.58)
    parts["cmedians"].set_color("black")
    parts["cmedians"].set_linewidth(1.2)
    ax.axhline(reference, color="#777777", linestyle="--", linewidth=0.8, alpha=0.8)
    for index, values in enumerate(groups):
        if len(values):
            ax.scatter(index, np.mean(values), color="red", zorder=5, s=18, marker="D")
    # Condition identity is carried by colour (shared legend below the figure).
    ax.set_xticks(np.arange(len(ORDER)))
    ax.set_xticklabels([])
    ax.tick_params(axis="x", length=0)
    ax.set_title(f"{title}\n{equation}", fontsize=ts.FS_PANEL - 1)
    ax.set_ylabel(ylabel)
    f_stat, p_value = stats.f_oneway(*groups)
    p_label = f"p = {p_value:.3f}" if p_value >= 0.001 else "p < 0.001"
    ax.set_xlabel(f"ANOVA: F = {f_stat:.2f}, {p_label}", fontsize=ts.FS_ANNOT - 0.5, color="#444444")
    ax.grid(axis="y", alpha=0.16)
    return [len(g) for g in groups]


def regenerate_stochastic_figure():
    params = pd.read_csv(STOP / "participant_parameters.csv")
    params = params[params["study_condition"].isin(ORDER)].copy()

    ts.apply()
    fig, axes = plt.subplots(2, 2, figsize=(ts.W_080, 4.9))
    ns = violin_panel(
        axes[0, 0], params, "mu_hat",
        "(a) Endpoint drift", r"$\hat\mu_{\rm end}=(X_T-X_1)/(T-1)$",
        "Change per step", 0.0,
    )
    violin_panel(
        axes[0, 1], params, "mu_ols",
        "(b) All-days drift", r"$\hat\mu_{\rm OLS}=\operatorname{slope}(X_t,t)$",
        "OLS change per day", 0.0,
    )
    violin_panel(
        axes[1, 0], params, "sig_hat",
        "(c) Raw variability", r"$\hat\sigma_{\rm raw}=\operatorname{SD}(X_{t+1}-X_t)$",
        "SD of increments", 0.0,
    )
    violin_panel(
        axes[1, 1], params, "sig_floor_ratio",
        "(d) Adjusted variability", r"$R_\sigma=\hat\sigma_{\rm raw}/\hat\sigma_{\rm binomial}$",
        "Observed SD / binomial floor", 1.0,
    )

    handles = [mpatches.Patch(facecolor=COLORS[c], alpha=0.6, label=ts.COND_LABELS[c]) for c in ORDER]
    handles.append(Line2D([0], [0], marker="D", color="none", markerfacecolor="red",
                          markersize=5, label="Mean"))
    handles.append(Line2D([0], [0], color="black", lw=1.2, label="Median"))
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False,
               bbox_to_anchor=(0.5, -0.02), fontsize=ts.FS_LEGEND - 0.5, columnspacing=1.0,
               handletextpad=0.4)
    fig.tight_layout(h_pad=1.0, w_pad=1.0, rect=(0, 0.05, 1, 1))

    for path in ts.save(fig, "DS5_onesec", "fig1_stop_params_four_panel.png", STOP / "figures"):
        print(f"Saved four-panel stochastic figure: {path}")


if __name__ == "__main__":
    regenerate_trajectory_figure()
    regenerate_stochastic_figure()
