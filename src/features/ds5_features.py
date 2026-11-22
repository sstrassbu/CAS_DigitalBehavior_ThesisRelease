"""
ds5_features.py
===============
Participant-level feature extraction for Dataset 5 — German adolescents (RCT).

Design decisions and dataset-specific notes
--------------------------------------------
- Unit of observation: one friction-intervention event per row (288,688 rows, 573 participants)
- Intervention exposure definition:
    * is_intervention_event == 1: friction was shown (intervention_duration_sec > 0)
    * is_reintervention == 1: a re-intervention attempt (subset of above, reintervention group)
- Outcome event classes (F001 / F200 / F213, 2026-08-08):
    * FRICTION DECISIONS   — {opened (177,986), dismissed (62,107)}: the only rows
      that carry override/compliance information, and the ONLY denominator of
      rate_opened / rate_dismissed / rate_not_opened.
    * SESSION TERMINATIONS — {closed (45,019)}: app-close records emitted after an
      open. Kept as `n_closed`, and `rate_closed` is now a logging-configuration
      share (closes / all outcome-bearing rows), not a friction outcome.
    * OTHER                — {dismissed_other (119)}: reported as
      n_other_outcome / rate_other_outcome; excluded from the friction denominator.
    * NO OUTCOME           — {missing (3,457, 1.2%)}: excluded everywhere.
  Note: all 45,019 `closed` rows have is_intervention_event == 0 (verified), so the
  intervention-event-restricted G3 rate was never contaminated by them.
- Clock (F029): DS5 ships a participant-local wall clock (`event_timestamp_local`,
  predominantly Europe/Berlin but 39 distinct `event_timezone` values in total, and
  97 participants log more than one). All time-of-day features are computed on it,
  not on UTC; `temporal_clock` records this per row.
- Study condition (CRITICAL):
    * cond column is NOT in the behavioral file — must join from pre-survey
    * Values: control / default / reintervention
    * All participant-level feature tables carry study_condition as a column
- DS5-unique richness:
    * Three-group RCT — the only experimental dataset in this project
    * Reintervention timing: reintervention_delay_sec (~78% NaN; only reintervention group)
    * Pre-survey: belonging (8 items), ostracism (5 items), FoMO (10 items)
    * Post-survey mirrors pre-survey scales + solve_prob and address_goal
    * Pre-post change features available for ~284 fully-linked participants
- Outputs split into three participant-level files:
  1. ds5_behavior_features.csv  — all 573 behavioral participants (with condition joined)
  2. ds5_survey_features.csv    — participants with pre-survey (~572 linked)
  3. ds5_prepost_features.csv   — participants with behavioral + both surveys (~284)

Ambiguity note on reintervention_open_rate:
  This feature (opened rate among reintervention events) is most interpretable
  for the reintervention condition. For control/default participants where
  is_reintervention == 0 for all events, this will be NaN.

Run via: notebooks/13_ds5_feature_extraction.ipynb
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from src.features.behavioral_features import (
    CLOCK_LOCAL,
    FRICTION_DECISION_OUTCOMES,
    volume_features,
    outcome_features,
    app_structure_features,
    temporal_features,
    adaptation_tertile_features,
    override_streak_features,
    intervention_duration_features,
    reintervention_features,
    hour_entropy,
    merge_feature_dicts,
)


# ---------------------------------------------------------------------------
# DS5-specific feature builders
# ---------------------------------------------------------------------------

def ds5_intervention_event_outcome_rate(df: pd.DataFrame) -> dict:
    """
    Opened rate restricted to is_intervention_event == 1 rows.

    Type: DIRECT
    Confidence: High
    Minimum data: >= 5 friction-decision intervention events

    This is the cleanest override-tendency metric in DS5 because it isolates
    events where friction was demonstrably shown (duration > 0).

    F001 / F200: the denominator is the shared FRICTION_DECISION_OUTCOMES
    vocabulary instead of a hand-rolled {opened, dismissed, closed} list, so this
    rate uses the same denominator as `rate_opened` from outcome_features().
    For the current DS5 export this is an exact no-op — all 45,019 `closed` and
    all 119 `dismissed_other` rows carry is_intervention_event == 0 (verified on
    the full 288,688-row cleaned file) — but the old list would have silently
    pooled close records here if that ever changed.
    """
    ie_df = df[df["is_intervention_event"] == 1].copy()
    valid = ie_df[ie_df["event_outcome_simple"].isin(FRICTION_DECISION_OUTCOMES)]
    n = len(valid)

    if n < 5:
        return {
            "open_rate_intervention_events": np.nan,
            "n_intervention_event_outcomes": int(n),
        }

    rate = round(float((valid["event_outcome_simple"] == "opened").mean()), 4)
    return {
        "open_rate_intervention_events": rate,
        "n_intervention_event_outcomes": int(n),
    }


def ds5_adaptation_calendar(df: pd.DataFrame) -> dict:
    """
    Longitudinal adaptation via calendar-time quartiles (days_since_first_event).

    Type: PROXY
    Confidence: Medium (shorter windows than DS4; condition confounds trajectory)
    Minimum data: >= 10 outcome-bearing rows with days_since_first_event varying

    F120 / F129: the thirds are cut on the calendar-time axis, not on row
    quantiles, so they can hold very unequal event counts (DS5's largest saved
    signal, open_rate_change_calendar = +0.9340, came from a late third holding 3
    events out of 706). The shared function now returns NaN for a third holding
    fewer than MIN_ROWS_PER_THIRD rows, and the third sizes plus the eligible-row
    count are passed through here so downstream users can filter further instead
    of having them silently dropped by this rename dict.
    """
    result = adaptation_tertile_features(
        df,
        time_col="days_since_first_event",
        outcome_col="event_outcome_simple",
    )
    renamed = {
        "open_rate_early_third_calendar": result["open_rate_early_third"],
        "open_rate_late_third_calendar": result["open_rate_late_third"],
        "open_rate_change_calendar": result["open_rate_change"],
        "dismiss_rate_early_third_calendar": result["dismiss_rate_early_third"],
        "dismiss_rate_late_third_calendar": result["dismiss_rate_late_third"],
        "dismiss_rate_change_calendar": result["dismiss_rate_change"],
        # F120/F129: sample sizes behind the two rates above.
        "n_rows_adaptation_eligible_calendar": result["n_rows_adaptation_eligible"],
        "n_early_third_calendar": result["n_early_third"],
        "n_late_third_calendar": result["n_late_third"],
    }
    return renamed


# ---------------------------------------------------------------------------
# Survey feature builders
# ---------------------------------------------------------------------------

def ds5_pre_survey_features(pre_row: pd.Series) -> dict:
    """
    Extract participant-level pre-survey features from a single pre-survey row.

    Type: DIRECT (validated psychometric scales; self-report ratings)
    Confidence: High for scale means; Medium for single-item ratings
    Available for: ~572 behavioral-linked participants

    Scales:
      - belong_mean (8-item belonging scale)
      - ostracism_mean (5-item ostracism scale)
      - fomo_mean (10-item FoMO scale)
    These are DS5-specific: no equivalent scales in DS1, DS4, or DS6.
    """
    def _val(col):
        v = pre_row.get(col, np.nan)
        return np.nan if pd.isna(v) else v

    return {
        "study_condition": _val("cond"),
        "age": _val("age"),
        "belong_mean_pre": _val("belong_mean"),
        "ostracism_mean_pre": _val("ostracism_mean"),
        "fomo_mean_pre": _val("fomo_mean"),
        "digital_wellbeing_pre": _val("digital_wellbeing"),
        "prob_self_pre": _val("prob_self"),
        "prob_peers_pre": _val("prob_peers"),
        "time_peers_pre": _val("time_peers"),
        "social_media_wellbeing_pre": _val("social_media_wellbeing"),
        "hours_pre": _val("time"),
    }


def ds5_post_survey_features(post_row: pd.Series) -> dict:
    """
    Extract participant-level post-survey features from a single post-survey row.

    Type: DIRECT
    Confidence: High for scale means; Medium for outcome questions
    Available for: ~311 post-survey participants; behavioral-linked ~284

    solve_prob and address_goal are interpretable for intervention groups only.
    Control participants received no intervention and should not be compared
    directly on these outcome questions.
    """
    def _val(col):
        v = post_row.get(col, np.nan)
        return np.nan if pd.isna(v) else v

    return {
        "belong_mean_post": _val("belong_mean"),
        "ostracism_mean_post": _val("ostracism_mean"),
        "fomo_mean_post": _val("fomo_mean"),
        "digital_wellbeing_post": _val("digital_wellbeing"),
        "prob_self_post": _val("prob_self"),
        "social_media_wellbeing_post": _val("social_media_wellbeing"),
        "hours_post": _val("time"),
        "solve_prob_post": _val("solve_prob"),
        "address_goal_post": _val("address_goal"),
    }


def ds5_prepost_change_features(pre_row: pd.Series, post_row: pd.Series) -> dict:
    """
    Compute signed pre-to-post change scores.

    Type: DIRECT-DERIVED
    Confidence: Medium
    Available for: ~284 participants with behavioral + both surveys

    Sign convention: positive = increase post-intervention.
    For belonging/wellbeing: positive = improvement.
    For problematic use / prob_self: positive = worsening.
    Interpret within each condition separately.
    """
    def _diff(col):
        pre = pre_row.get(col, np.nan)
        post = post_row.get(col, np.nan)
        if pd.isna(pre) or pd.isna(post):
            return np.nan
        return round(float(post) - float(pre), 3)

    return {
        "belong_change": _diff("belong_mean"),
        "ostracism_change": _diff("ostracism_mean"),
        "fomo_change": _diff("fomo_mean"),
        "digital_wellbeing_change": _diff("digital_wellbeing"),
        "prob_self_change": _diff("prob_self"),
        "social_media_wellbeing_change": _diff("social_media_wellbeing"),
        "hours_change": _diff("time"),
    }


# ---------------------------------------------------------------------------
# Main participant-level builders
# ---------------------------------------------------------------------------

def build_ds5_behavior_features(
    beh: pd.DataFrame,
    pre: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the behavior-only participant-level feature table for DS5.

    Joins study_condition from pre-survey so every participant row carries
    their condition assignment.

    Input: ds5_behavioral_clean.csv (288,688 rows) + ds5_pre_survey_clean.csv
    Output: one row per participant (573 rows)

    Feature groups:
      G1 Volume and activity              — DIRECT, High
      G2 Outcome distribution             — DIRECT, High
      G3 Intervention event outcome rate  — DIRECT, High
      G4 Intervention duration            — DIRECT/PROXY, Medium
      G5 Reintervention                   — DIRECT, Medium-High
      G6 App structure                    — DIRECT, High
      G7 Temporal structure               — DIRECT-DERIVED, High
      G8 Longitudinal adaptation          — PROXY, Medium
      G9 Override tendency                — PROXY, Medium
      study_condition                     — DIRECT (joined from pre-survey)

    Columns added 2026-08-08 by the shared-module corrections (all must be
    documented in outputs/features/ds5/ds5_features.md):
      obs_window_calendar_days                  (G1, F035/F048/F117)
      n_friction_decisions, n_other_outcome,
      rate_other_outcome                        (G2, F001/F200)
      temporal_clock                            (G7, F029)
      n_rows_adaptation_eligible_calendar,
      n_early_third_calendar, n_late_third_calendar  (G8, F120/F129)

    Columns whose VALUES change (same names, new semantics):
      rate_opened / rate_dismissed / rate_not_opened — friction-decision
        denominator only; `closed` and `dismissed_other` are no longer in it.
        DS5 KEEPS rate_not_opened (GaT's commitment_score is defined on it), but
        it is now numerically identical to rate_dismissed for every participant,
        because the decision set has exactly two labels. Any DS5 model output
        computed from the pre-2026-08-08 values must be recomputed.
      rate_closed — now closes / all outcome-bearing rows, i.e. a
        LOGGING-CONFIGURATION share, not a friction outcome. Numerically
        unchanged for DS5, which makes it easy to mis-read as untouched.
      max_consecutive_opens / mean_open_run_length / p_open_after_dismiss —
        non-decision rows no longer terminate an open run (F003/F213); the
        min-data gate is now >= 5 friction-decision rows, not >= 5
        outcome-bearing rows.
      peak_hour_of_day / evening_event_share / morning_event_share /
        weekend_event_share — local clock (F029).
      hour_entropy — also changes, for 110 of 573 participants. This feature is
        invariant to a CONSTANT whole-hour offset, but DS5 is not constant-offset:
        112 participants span more than one UTC->local offset (Europe/Berlin DST
        plus travel across 39 distinct event_timezone values). The 110 changed
        participants are a strict subset of those 112; zero single-offset
        participants changed.
      events_per_day / active_days_per_week — F034/F118 window floor and
        F035/F048/F117 calendar-date denominator.
    """
    beh = beh.copy()
    beh["event_timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], utc=True)
    # Standardize timestamp column name for shared utilities (volume, ordering).
    beh["timestamp_utc"] = beh["event_timestamp_utc"]
    # F029: peak hour / evening / morning are LOCAL-clock constructs. DS5 ships a
    # participant-local wall clock (Europe/Berlin, tz-naive by construction); the
    # previous code aliased UTC into the temporal features and discarded it.
    beh["timestamp_local"] = pd.to_datetime(beh["event_timestamp_local"], errors="coerce")

    # Build condition map from pre-survey
    cond_map = pre.set_index("participant_id_canonical")["cond"].to_dict()

    records = []
    for pid, grp in beh.groupby("participant_id_canonical"):
        grp = grp.sort_values("timestamp_utc")
        feats = {"participant_id_canonical": pid}

        # Study condition (from pre-survey)
        feats["study_condition"] = cond_map.get(pid, np.nan)

        # G1 volume
        feats.update(volume_features(grp))
        n_ie = int((grp["is_intervention_event"] == 1).sum())
        n_ri = int((grp["is_reintervention"] == 1).sum())
        feats["n_intervention_events"] = n_ie
        feats["n_reintervention_events"] = n_ri

        # G2 outcomes
        feats.update(outcome_features(grp, "event_outcome_simple"))

        # G3 intervention-event-specific outcome rate
        feats.update(ds5_intervention_event_outcome_rate(grp))

        # G4 intervention duration
        feats.update(
            intervention_duration_features(grp, "intervention_duration_sec", "event_outcome_simple")
        )

        # G5 reintervention
        feats.update(
            reintervention_features(
                grp,
                reintervention_flag_col="is_reintervention",
                reintervention_delay_col="reintervention_delay_sec",
                outcome_col="event_outcome_simple",
            )
        )

        # G6 app structure
        feats.update(app_structure_features(grp, "app_name"))

        # G7 temporal — F029: local clock, declared explicitly. hour_entropy is
        # fed the same column so every time-of-day feature in this row sits on one
        # clock. It is invariant to a CONSTANT whole-hour offset but DS5 is not
        # constant-offset (DST + 39 event_timezone values), so its value does move
        # for the 110 multi-offset participants — that is the correction, not a bug.
        feats.update(temporal_features(grp, "timestamp_local", clock=CLOCK_LOCAL))
        feats.update(hour_entropy(grp, "timestamp_local"))

        # G8 longitudinal adaptation
        feats.update(ds5_adaptation_calendar(grp))

        # G9 override tendency
        feats.update(override_streak_features(grp, "event_outcome_simple", "timestamp_utc"))

        records.append(feats)

    return pd.DataFrame(records)


def build_ds5_survey_features(
    beh: pd.DataFrame,
    pre: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the pre-survey feature table, restricted to behavioral participants.

    Returns one row per participant with both behavioral data AND pre-survey
    response (~572 expected).

    Feature groups:
      G10 Pre-survey psychosocial  — DIRECT, High (belonging, ostracism, FoMO)
    """
    behavioral_ids = set(beh["participant_id_canonical"].unique())
    pre_linked = pre[pre["participant_id_canonical"].isin(behavioral_ids)].copy()

    records = []
    for _, row in pre_linked.iterrows():
        feats = {"participant_id_canonical": row["participant_id_canonical"]}
        feats.update(ds5_pre_survey_features(row))
        records.append(feats)

    return pd.DataFrame(records)


def build_ds5_prepost_features(
    beh: pd.DataFrame,
    pre: pd.DataFrame,
    post: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the pre-post change feature table for participants with behavioral +
    pre-survey + post-survey.

    Returns one row per participant in the three-way intersection (~284 expected).

    Feature groups:
      G11 Post-survey psychosocial     — DIRECT, High
      G12 Pre-post change scores       — DIRECT-DERIVED, Medium
    """
    behavioral_ids = set(beh["participant_id_canonical"].unique())
    pre_idx = pre.set_index("participant_id_canonical")
    post_idx = post.set_index("participant_id_canonical")

    eligible = set(pre_idx.index) & set(post_idx.index) & behavioral_ids

    records = []
    for pid in sorted(eligible):
        pre_row = pre_idx.loc[pid]
        post_row = post_idx.loc[pid]
        feats = {
            "participant_id_canonical": pid,
            "study_condition": pre_row.get("cond", np.nan),
        }
        feats.update(ds5_post_survey_features(post_row))
        feats.update(ds5_prepost_change_features(pre_row, post_row))
        records.append(feats)

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_ds5_files(cleaned_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all DS5 cleaned files. Returns (beh, pre, post, linkage)."""
    beh = pd.read_csv(cleaned_dir / "ds5_behavioral_clean.csv")
    pre = pd.read_csv(cleaned_dir / "ds5_pre_survey_clean.csv")
    post = pd.read_csv(cleaned_dir / "ds5_post_survey_clean.csv")
    linkage = pd.read_csv(cleaned_dir / "ds5_participant_linkage.csv")
    return beh, pre, post, linkage
