"""Run the two thesis-critical observation-model sensitivity analyses.

1. Structured: time-valid path dependence.  Prior completion status and the
   current task's structure are evaluated only with information available at
   the instant the current task was created.
2. DS6: matched observation windows.  Baseline and intervention daily-count
   processes are refit on equal-length, participant-specific local-day windows.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "model_outputs" / "supplemental_verification"
FIG = OUT / "figures"
THESIS_FIG = ROOT / "latex_master_thesis" / "figure" / "structured"
THESIS_FIG_DS6 = ROOT / "latex_master_thesis" / "figure" / "DS6_onesec"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)


def structured_time_valid_path_dependence() -> pd.DataFrame:
    beh = pd.read_csv(ROOT / "outputs" / "cleaned" / "structured_behavioral_clean.csv")
    beh["event_timestamp_utc"] = pd.to_datetime(
        beh["event_timestamp_utc"], format="mixed", utc=True
    )

    created = (
        beh.loc[beh["event_type"].eq("Task Created")]
        .sort_values(["participant_id", "event_timestamp_utc", "task_id"])
        .drop_duplicates("task_id", keep="first")
        .copy()
    )
    created["has_structure_at_creation"] = (
        created["task_is_recurring"].fillna(False).astype(bool)
        | created["task_has_notes"].fillna(False).astype(bool)
        | created["subtasks_amount"].fillna(0).gt(0)
    ).astype(int)

    # Exact task-completion tags only. If both tags occur on one row, the
    # uncompletion transition wins, matching the lifecycle feature builder.
    state_records = []
    for row in beh.sort_values("event_timestamp_utc").itertuples(index=False):
        tags = (
            set(str(row.update_type_list_str).split("|"))
            if pd.notna(row.update_type_list_str)
            else set()
        )
        state = None
        if "task_completed" in tags:
            state = True
        if "task_uncompleted" in tags or row.event_type == "Task Deleted":
            state = False
        if state is not None:
            state_records.append((row.task_id, row.event_timestamp_utc.value, state))

    state_events = pd.DataFrame(
        state_records, columns=["task_id", "timestamp_ns", "is_completed"]
    )
    state_by_task = {
        task_id: (
            grp["timestamp_ns"].to_numpy(),
            grp["is_completed"].to_numpy(dtype=bool),
        )
        for task_id, grp in state_events.groupby("task_id", sort=False)
    }

    def completed_as_of(task_id, cutoff):
        history = state_by_task.get(task_id)
        if history is None:
            return False
        timestamps, states = history
        idx = np.searchsorted(timestamps, cutoff.value, side="right") - 1
        return bool(states[idx]) if idx >= 0 else False

    records = []
    for participant_id, grp in created.groupby("participant_id", sort=False):
        streak = 0
        previous_task_id = None
        for row in grp.itertuples(index=False):
            if previous_task_id is not None:
                previous_completed = completed_as_of(
                    previous_task_id, row.event_timestamp_utc
                )
                streak = 0 if previous_completed else streak + 1
                records.append(
                    {
                        "participant_id": participant_id,
                        "task_id": row.task_id,
                        "creation_timestamp_utc": row.event_timestamp_utc,
                        "previous_task_completed_as_of_creation": previous_completed,
                        "prior_noncompletion_streak_as_of_creation": streak,
                        "has_structure_at_creation": row.has_structure_at_creation,
                    }
                )
            previous_task_id = row.task_id

    path = pd.DataFrame(records)
    x_col = "prior_noncompletion_streak_as_of_creation"
    y_col = "has_structure_at_creation"
    r_pooled, p_pooled = stats.pearsonr(path[x_col], path[y_col])
    path["streak_person_demeaned"] = path[x_col] - path.groupby("participant_id")[
        x_col
    ].transform("mean")
    path["structure_person_demeaned"] = path[y_col] - path.groupby("participant_id")[
        y_col
    ].transform("mean")
    r_within, p_within = stats.pearsonr(
        path["streak_person_demeaned"], path["structure_person_demeaned"]
    )

    # Shuffle the current-task outcome only within each participant. This
    # preserves each person's task count and structure prevalence.
    rng = np.random.default_rng(42)
    participant_indices = [
        grp.index.to_numpy() for _, grp in path.groupby("participant_id", sort=False)
    ]
    x_demeaned = path["streak_person_demeaned"].to_numpy()
    y_demeaned = path["structure_person_demeaned"].to_numpy()
    permuted_r = np.empty(2000)
    for iteration in range(len(permuted_r)):
        y_permuted = y_demeaned.copy()
        for indices in participant_indices:
            y_permuted[indices] = rng.permutation(y_permuted[indices])
        permuted_r[iteration] = np.corrcoef(x_demeaned, y_permuted)[0, 1]
    p_permutation = (
        1 + np.sum(np.abs(permuted_r) >= abs(r_within))
    ) / (len(permuted_r) + 1)

    result = pd.DataFrame(
        [
            {
                "analysis": "Structured time-valid path dependence",
                "predictor": x_col,
                "outcome": y_col,
                "pearson_r_pooled": r_pooled,
                "p_pooled": p_pooled,
                "pearson_r_within": r_within,
                "p_within_asymptotic": p_within,
                "p_within_participant_permutation": p_permutation,
                "n_task_transitions": len(path),
                "n_participants": path["participant_id"].nunique(),
                "n_permutations": len(permuted_r),
            }
        ]
    )
    path.to_csv(OUT / "structured_time_valid_path_observations.csv", index=False)
    result.to_csv(OUT / "structured_time_valid_path_test.csv", index=False)

    path["streak_bin"] = path[x_col].clip(upper=4)
    plotted = path.groupby("streak_bin")[y_col].agg(["mean", "count", "std"]).reset_index()
    plotted["se"] = plotted["std"] / np.sqrt(plotted["count"])
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    ax.errorbar(
        plotted["streak_bin"],
        plotted["mean"],
        yerr=1.96 * plotted["se"],
        fmt="o-",
        capsize=4,
        color="#3B6FB6",
    )
    ax.set_xticks(range(5), ["0", "1", "2", "3", "4+"])
    ax.tick_params(axis="both", labelsize=13)
    ax.set_xlabel("Prior not-completed streak known at task creation", fontsize=15)
    ax.set_ylabel("Share of newly created tasks with structure", fontsize=15)
    # Zoomed from the full [0,1] proportion scale: observed shares stay under 0.12,
    # so a [0,1] axis leaves ~85% of the panel blank. Still zero-anchored (not a
    # truncated/misleading non-zero baseline) so the "this share is small" reading
    # is preserved; only the wasted headroom above the data is removed.
    y_ceiling = (plotted["mean"] + 1.96 * plotted["se"]).max()
    ax.set_ylim(0, max(0.30, y_ceiling * 1.8))
    ax.set_title("Structured: time-valid path-dependence diagnostic", fontsize=17, pad=12)
    ax.text(
        0.02,
        0.95,
        f"Within-person r={r_within:.3f}; permutation p={p_permutation:.3f}",
        transform=ax.transAxes,
        fontsize=13,
        va="top",
    )
    fig.tight_layout()
    fig.savefig(FIG / "structured_time_valid_path_dependence.png", dpi=180)
    THESIS_FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(THESIS_FIG / "fig_time_valid_path_dependence.png", dpi=180)
    plt.close(fig)
    return result


def _zero_filled_daily_grid(frame):
    counts = frame.groupby("event_date_local").size()
    if counts.empty:
        return None
    date_range = pd.date_range(counts.index.min(), counts.index.max(), freq="D")
    return counts.reindex(date_range, fill_value=0).astype(float)


def _count_process_parameters(grid):
    values = np.asarray(grid, dtype=float)
    increments = np.diff(values)
    mu_endpoint = float(np.mean(increments))
    sig_hat = float(np.std(increments, ddof=1)) if len(increments) >= 2 else np.nan
    mu_se = sig_hat / np.sqrt(len(increments)) if len(increments) else np.nan
    time = np.arange(len(values), dtype=float)
    ols = stats.linregress(time, values)
    mean_n = float(np.mean(values))
    fano = float(np.var(values, ddof=1) / mean_n) if mean_n > 0 else np.nan
    return {
        "mu_endpoint": mu_endpoint,
        "mu_endpoint_se": mu_se,
        "mu_ols": float(ols.slope),
        "mu_ols_se": float(ols.stderr),
        "sig_hat": sig_hat,
        "fano": fano,
        "mean_N": mean_n,
        "span_days": len(values),
        "n_active_days": int(np.sum(values > 0)),
    }


def _classify_ds6_regime(mu, sigma, sigma_threshold, mu_threshold=0.5):
    if pd.isna(mu) or pd.isna(sigma):
        return np.nan
    if sigma >= sigma_threshold:
        return "stochastic"
    if mu < -mu_threshold:
        return "declining"
    if mu > mu_threshold:
        return "growing"
    return "resting"


def ds6_matched_observation_windows() -> pd.DataFrame:
    beh = pd.read_csv(ROOT / "outputs" / "cleaned" / "ds6_behavioral_clean.csv")
    # DS6 has one verified cohort clock (Europe/Copenhagen) but the cleaned
    # table stores only UTC timestamps. Reconstruct local calendar days here;
    # 2.36% of events otherwise fall on the adjacent date.
    local_timestamp = pd.to_datetime(
        beh["event_timestamp_utc"], format="mixed", utc=True, errors="coerce"
    ).dt.tz_convert("Europe/Copenhagen")
    beh["event_date_local"] = local_timestamp.dt.normalize()
    if beh["event_date_local"].isna().any():
        raise ValueError("DS6 local timestamps could not all be parsed")

    grids = {}
    condition_lookup = {}
    for participant_id, participant in beh.groupby("participant_id_canonical"):
        condition_lookup[participant_id] = participant["study_condition"].dropna().iloc[0]
        grids[participant_id] = {
            period: _zero_filled_daily_grid(
                participant.loc[participant["study_period"].eq(period)]
            )
            for period in ["baseline", "intervention"]
        }

    records = []
    for participant_id, period_grids in grids.items():
        baseline = period_grids["baseline"]
        intervention = period_grids["intervention"]
        if baseline is None or intervention is None:
            continue
        if (baseline > 0).sum() < 7 or (intervention > 0).sum() < 7:
            continue
        matched_days = min(len(baseline), len(intervention))
        if matched_days < 7:
            continue
        row = {
            "participant_id_canonical": participant_id,
            "study_condition": condition_lookup[participant_id],
            "matched_days": matched_days,
            "baseline_full_span_days": len(baseline),
            "intervention_full_span_days": len(intervention),
        }
        for period, grid in [
            ("baseline", baseline.iloc[:matched_days]),
            ("intervention", intervention.iloc[:matched_days]),
        ]:
            for key, value in _count_process_parameters(grid).items():
                row[f"{key}_{period}_matched"] = value
        records.append(row)

    matched = pd.DataFrame(records)
    sigma_thresholds = {
        period: matched[f"sig_hat_{period}_matched"].median()
        for period in ["baseline", "intervention"]
    }
    for period in ["baseline", "intervention"]:
        matched[f"regime_{period}_matched"] = [
            _classify_ds6_regime(mu, sigma, sigma_thresholds[period])
            for mu, sigma in zip(
                matched[f"mu_endpoint_{period}_matched"],
                matched[f"sig_hat_{period}_matched"],
            )
        ]
        matched[f"mu_signal_to_noise_{period}_matched"] = (
            matched[f"mu_endpoint_{period}_matched"].abs()
            / matched[f"mu_endpoint_se_{period}_matched"]
        )

    matched["regime_changed_matched"] = (
        matched["regime_baseline_matched"]
        != matched["regime_intervention_matched"]
    )
    matched["h_endpoint_matched"] = (
        matched["mu_endpoint_intervention_matched"]
        - matched["mu_endpoint_baseline_matched"]
    )
    matched["h_ols_matched"] = (
        matched["mu_ols_intervention_matched"] - matched["mu_ols_baseline_matched"]
    )

    raw_path = (
        ROOT
        / "outputs"
        / "model_outputs"
        / "ds6"
        / "dynamical_systems"
        / "participant_regime_classification.csv"
    )
    raw = pd.read_csv(raw_path)[
        ["participant_id_canonical", "regime_baseline", "regime_intervention"]
    ]
    matched = matched.merge(raw, on="participant_id_canonical", how="left")
    matched["regime_changed_raw"] = (
        matched["regime_baseline"] != matched["regime_intervention"]
    )

    order = ["declining", "resting", "growing", "stochastic"]
    raw_matrix = pd.crosstab(
        matched["regime_baseline"], matched["regime_intervention"]
    ).reindex(index=order, columns=order, fill_value=0)
    matched_matrix = pd.crosstab(
        matched["regime_baseline_matched"], matched["regime_intervention_matched"]
    ).reindex(index=order, columns=order, fill_value=0)

    paired_t_endpoint = stats.ttest_rel(
        matched["mu_endpoint_baseline_matched"],
        matched["mu_endpoint_intervention_matched"],
    )
    paired_t_ols = stats.ttest_rel(
        matched["mu_ols_baseline_matched"], matched["mu_ols_intervention_matched"]
    )
    summary = pd.DataFrame(
        [
            {
                "n_participants": len(matched),
                "median_matched_days": matched["matched_days"].median(),
                "mean_mu_endpoint_baseline_matched": matched[
                    "mu_endpoint_baseline_matched"
                ].mean(),
                "mean_mu_endpoint_intervention_matched": matched[
                    "mu_endpoint_intervention_matched"
                ].mean(),
                "paired_t_endpoint": paired_t_endpoint.statistic,
                "paired_p_endpoint": paired_t_endpoint.pvalue,
                "mean_mu_ols_baseline_matched": matched[
                    "mu_ols_baseline_matched"
                ].mean(),
                "mean_mu_ols_intervention_matched": matched[
                    "mu_ols_intervention_matched"
                ].mean(),
                "paired_t_ols": paired_t_ols.statistic,
                "paired_p_ols": paired_t_ols.pvalue,
                "share_abs_endpoint_mu_gt_2se_baseline": matched[
                    "mu_signal_to_noise_baseline_matched"
                ].gt(2).mean(),
                "share_abs_endpoint_mu_gt_2se_intervention": matched[
                    "mu_signal_to_noise_intervention_matched"
                ].gt(2).mean(),
                "share_regime_changed_raw": matched["regime_changed_raw"].mean(),
                "share_regime_changed_matched": matched[
                    "regime_changed_matched"
                ].mean(),
                "sigma_threshold_baseline_matched": sigma_thresholds["baseline"],
                "sigma_threshold_intervention_matched": sigma_thresholds[
                    "intervention"
                ],
            }
        ]
    )

    matched.to_csv(OUT / "ds6_matched_window_parameters.csv", index=False)
    summary.to_csv(OUT / "ds6_matched_window_summary.csv", index=False)
    matched_matrix.to_csv(OUT / "ds6_matched_regime_transition_matrix.csv")

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.2), constrained_layout=True)
    for ax, matrix, title in [
        (axes[0], raw_matrix, "Original unequal windows"),
        (axes[1], matched_matrix, "Equal-length local-day windows"),
    ]:
        image = ax.imshow(matrix.values, cmap="viridis")
        ax.set_xticks(range(4), order, rotation=35, ha="right", fontsize=13)
        ax.set_yticks(range(4), order, fontsize=13)
        ax.set_xlabel("Intervention regime", fontsize=15)
        ax.set_ylabel("Baseline regime", fontsize=15)
        ax.set_title(title, fontsize=16, fontweight="bold")
        for i in range(4):
            for j in range(4):
                color = "white" if matrix.values[i, j] > matrix.values.max() / 2 else "black"
                ax.text(j, i, int(matrix.values[i, j]), ha="center", va="center", color=color, fontsize=14)
        cbar = fig.colorbar(image, ax=ax, shrink=0.8, label="Participants")
        cbar.ax.tick_params(labelsize=12)
        cbar.set_label("Participants", fontsize=13)
    fig.suptitle("DS6 regime transitions: observation-window sensitivity", fontsize=17, fontweight="bold")
    fig.savefig(FIG / "ds6_matched_window_regime_comparison.png", dpi=180)
    THESIS_FIG_DS6.mkdir(parents=True, exist_ok=True)
    fig.savefig(THESIS_FIG_DS6 / "fig2_dys_regime_window_comparison.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    positions = [0, 1]
    endpoint_data = [
        matched["mu_endpoint_baseline_matched"],
        matched["mu_endpoint_intervention_matched"],
    ]
    parts = ax.violinplot(endpoint_data, positions=positions, showmedians=True)
    for body, color in zip(parts["bodies"], ["#4C72B0", "#DD8452"]):
        body.set_facecolor(color)
        body.set_alpha(0.65)
    ax.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_xticks(positions, ["Baseline", "Intervention"])
    ax.set_ylabel("Endpoint drift on matched windows (attempts/day)")
    ax.set_title("DS6 matched-window drift diagnostic")
    ax.text(
        0.02,
        0.03,
        f"paired p={paired_t_endpoint.pvalue:.3f}; |mu|>2 SE: "
        f"{summary.iloc[0]['share_abs_endpoint_mu_gt_2se_baseline']:.1%} / "
        f"{summary.iloc[0]['share_abs_endpoint_mu_gt_2se_intervention']:.1%}",
        transform=ax.transAxes,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(FIG / "ds6_matched_window_drift.png", dpi=180)
    plt.close(fig)
    return summary


def main():
    structured = structured_time_valid_path_dependence()
    ds6 = ds6_matched_observation_windows()
    print(structured.to_string(index=False))
    print(ds6.to_string(index=False))
    print(f"Outputs written to {OUT}")


if __name__ == "__main__":
    main()
