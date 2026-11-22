"""
ds1_features.py
===============
Participant-level feature extraction for Dataset 1 — Compact friction intervention testing.

Design decisions and dataset-specific notes
--------------------------------------------
- Unit of observation: one intervention event per row (398,757 rows, 619 participants)
- Intervention exposure definition: all rows; every row in DS1 represents a triggered
  OneSec friction event (there is no separate structural event class distinction).
- Outcome-bearing rows: rows where event_outcome_simple is not NaN / not 'missing'
  (missing = 467 rows, 0.1%). These split into two STRUCTURALLY DIFFERENT classes
  (F001 / F003, 2026-08-08):
    * friction decisions   — 'opened' / 'dismissed'; the participant met the friction
      screen and chose. Only these carry override/compliance information.
    * session terminations — 'closed'; an app-CLOSE record emitted after an 'opened'
      (median ~100 s later). Close logging is a per-device configuration: only 126 of
      619 DS1 participants log it at all, and they hold 183,257 of 398,757 rows.
  All DS1 friction rates and open-run streaks are therefore computed on friction-decision
  rows only. `rate_not_opened` is DROPPED for DS1 (user decision on record): once closes
  leave the numerator it is an exact duplicate of `rate_dismissed`.
- Longitudinal time axis: secondsSinceOneSecSetup (available for 81.1% of events).
  Rows with NaN secondsSinceOneSecSetup are excluded from adaptation features. F036: that
  missingness is participant-level and all-or-nothing (529 participants have the field on
  100% of rows, 90 on 0%, none in between) and tracks enrollment wave, so G5/G6 describe a
  ~June-2021-onward sub-cohort rather than a random 81% of events. Within an included
  participant the early/late tertile split is unbiased.
- No local clock: DS1's `timestamp` is a raw UTC epoch and the dataset ships no timezone
  column, so time-of-day features are declared UTC-only (F029 / F047 / F208) — see
  build_ds1_behavior_features().
- DS1-specific richness:
  * secondsSinceOneSecSetup gives a precise setup-time axis not available in other datasets
  * Pre/post surveys include problematic_cons (1-7), happy (1-7), goals, problem domains
  * Pre-post change features available for 168 participants linked to both surveys
- Outputs are split into three participant-level files:
  1. ds1_behavior_features.csv  — all 619 behavioral participants
  2. ds1_survey_features.csv    — participants with pre-survey (up to 1,086; behavioral-linked only)
  3. ds1_prepost_features.csv   — participants with both surveys + behavioral (168)

Run via: notebooks/11_ds1_feature_extraction.ipynb
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from src.features.behavioral_features import (
    CLOCK_UTC_FALLBACK,
    volume_features,
    outcome_features,
    app_structure_features,
    temporal_features,
    adaptation_tertile_features,
    override_streak_features,
    hour_entropy,
    merge_feature_dicts,
)

# ---------------------------------------------------------------------------
# DS1-specific feature builders
# ---------------------------------------------------------------------------

def ds1_setup_time_features(df: pd.DataFrame) -> dict:
    """
    Features derived from secondsSinceOneSecSetup — DS1's unique time axis.

    Type: DIRECT (column directly observed) / PROXY (adaptation interpretation)
    Confidence: Medium (18.9% NaN; also no experimental control)
    Minimum data: >= 5 rows with non-NaN secondsSinceOneSecSetup

    The setup_window_days reflects the participant's active span as measured
    from their first app setup event, not calendar time.

    F036: the 18.9% event-level NaN is strictly participant-level — 529 participants
    have the field on every row, 90 on none, none mixed — and the 90 are almost
    entirely the April–May 2021 enrollment wave. `n_events_with_setup_time == 0`
    therefore flags cohort membership, not sparse logging.
    """
    col = "secondsSinceOneSecSetup"
    valid = df[df[col].notna()].copy()
    n_valid = len(valid)

    base = {
        "n_events_with_setup_time": n_valid,
        "setup_window_days": np.nan,
    }

    if n_valid < 5:
        return base

    max_sec = valid[col].max()
    base["setup_window_days"] = round(max_sec / 86400.0, 2)
    return base


def ds1_adaptation_via_setup_time(df: pd.DataFrame) -> dict:
    """
    Adaptation features using secondsSinceOneSecSetup as the longitudinal axis.

    Wraps the generic adaptation_tertile_features with DS1-specific column name.
    Adds suffix '_setup' to distinguish from calendar-time-based variants.

    Type: PROXY
    Confidence: Medium

    F120 / F129: the thirds are cut on the TIME axis, not on row quantiles, so they can
    hold very unequal event counts. The shared helper now returns NaN for a third holding
    fewer than MIN_ROWS_PER_THIRD (=5) rows, which makes the corresponding *_change NaN
    too. The two third sizes are passed through here so downstream users can filter
    further; without the explicit pass-through this wrapper's renamed dict would silently
    drop them. They are NaN (not 0) when the thirds were never cut at all.
    """
    col = "secondsSinceOneSecSetup"
    result = adaptation_tertile_features(df, time_col=col, outcome_col="event_outcome_simple")
    # Rename keys to make the time axis explicit
    renamed = {
        "open_rate_early_third_setup": result["open_rate_early_third"],
        "open_rate_late_third_setup": result["open_rate_late_third"],
        "open_rate_change_setup": result["open_rate_change"],
        "dismiss_rate_early_third_setup": result["dismiss_rate_early_third"],
        "dismiss_rate_late_third_setup": result["dismiss_rate_late_third"],
        "dismiss_rate_change_setup": result["dismiss_rate_change"],
        # F120/F129: export the per-third row counts so a *_change built on a
        # near-empty third is visible in the saved table, not just inside the helper.
        "n_early_third_setup": result["n_early_third"],
        "n_late_third_setup": result["n_late_third"],
    }
    return renamed


# ---------------------------------------------------------------------------
# Survey feature builders
# ---------------------------------------------------------------------------

def ds1_pre_survey_features(pre_row: pd.Series) -> dict:
    """
    Extract participant-level pre-survey features from a single pre-survey row.

    Type: DIRECT
    Confidence: High for numeric Likert scales; Medium for multi-select counts
    Available for: participants in ds1_pre_survey_clean.csv (~1,086 total;
    behavioral-linked subset ~619 attempted, 168 with behavioral + both surveys)
    """
    def _val(col):
        v = pre_row.get(col, np.nan)
        return np.nan if pd.isna(v) else v

    # Count selected problems and goals from binary indicator columns
    problem_cols = [
        "problem_another_problem",
        "problem_automatic_consumption",
        "problem_excessive_consumption",
        "problem_feeling_of_no_control",
    ]
    goal_cols = [
        "goal_another_goal",
        "goal_consuming_selectively",
        "goal_less_consumption",
        "goal_more_awareness_of_consumption",
    ]

    # F130: `_val` maps NaN to np.nan, which never equals 1, so an all-NaN group used to
    # collapse to 0 — conflating "answered and selected nothing" with "question never
    # answered" (5 fabricated zeros for problems, 6 for goals in ds1_survey_features.csv).
    n_problems = (np.nan if all(pd.isna(_val(c)) for c in problem_cols)
                  else sum(1 for c in problem_cols if _val(c) == 1))
    n_goals = (np.nan if all(pd.isna(_val(c)) for c in goal_cols)
               else sum(1 for c in goal_cols if _val(c) == 1))

    feats = {
        "problematic_cons_pre": _val("problematic_cons_num"),
        "happy_pre": _val("happy_num"),
        "problematic_cons_general_pre": _val("problematic_cons_general_num"),
        "problematic_cons_compared_pre": _val("problematic_cons_compared_num"),
        "hours_self_reported_pre": _val("hours_num"),
        "n_problems_selected": n_problems,
        "n_goals_selected": n_goals,
    }

    # Include individual problem/goal binary flags
    for c in problem_cols:
        feats[c] = int(_val(c)) if not pd.isna(_val(c)) else np.nan
    for c in goal_cols:
        feats[c] = int(_val(c)) if not pd.isna(_val(c)) else np.nan

    return feats


def ds1_post_survey_features(post_row: pd.Series) -> dict:
    """
    Extract participant-level post-survey features from a single post-survey row.

    Type: DIRECT
    Confidence: High for numeric Likert scales
    Available for: 224 post-survey participants; behavioral-linked subset 168
    """
    def _val(col):
        v = post_row.get(col, np.nan)
        return np.nan if pd.isna(v) else v

    return {
        "problematic_cons_post": _val("problematic_cons_num"),
        "happy_post": _val("happy_num"),
        "problematic_cons_general_post": _val("problematic_cons_general_num"),
        "problematic_cons_compared_post": _val("problematic_cons_compared_num"),
        "problems_solved_post": _val("problems_solved_num"),
        "goals_reached_post": _val("goals_reached_num"),
        "progress_satisfaction_post": _val("progress_satisfaction_num"),
        "hours_self_reported_post": _val("hours_num"),
    }


def ds1_prepost_change_features(pre_row: pd.Series, post_row: pd.Series) -> dict:
    """
    Compute signed pre-to-post change scores.

    Type: DIRECT-DERIVED
    Confidence: Medium (between-survey attrition is heavy; completers may differ)
    Available for: 168 participants with behavioral + both surveys
    Sign convention: positive = increase (e.g. more problematic consumption post),
    negative = improvement on problematic_cons / worsening on happy.
    """
    def _diff(pre_col, post_col):
        pre = pre_row.get(pre_col, np.nan)
        post = post_row.get(post_col, np.nan)
        if pd.isna(pre) or pd.isna(post):
            return np.nan
        return round(float(post) - float(pre), 3)

    return {
        "problematic_cons_change": _diff("problematic_cons_num", "problematic_cons_num"),
        "happy_change": _diff("happy_num", "happy_num"),
        "problematic_cons_general_change": _diff("problematic_cons_general_num", "problematic_cons_general_num"),
        "problematic_cons_compared_change": _diff("problematic_cons_compared_num", "problematic_cons_compared_num"),
        "hours_change": _diff("hours_num", "hours_num"),
    }


# ---------------------------------------------------------------------------
# Main participant-level builders
# ---------------------------------------------------------------------------

def build_ds1_behavior_features(beh: pd.DataFrame) -> pd.DataFrame:
    """
    Build the behavior-only participant-level feature table for DS1.

    Input: ds1_behavioral_clean.csv (398,757 rows)
    Output: one row per participant (619 rows)

    Feature groups included (all from behavioral data only):
      G1 Volume and activity           — DIRECT, High
      G2 Outcome distribution          — DIRECT, High
      G3 App structure                 — DIRECT, High
      G4 Temporal structure            — DIRECT-DERIVED, High
      G5 Setup-time window             — DIRECT, High (count) / Medium (window)
      G6 Longitudinal adaptation       — PROXY, Medium (setup-time axis)
      G7 Override tendency streaks     — PROXY, Medium

    Notes on row eligibility per group:
      G1: `events_per_day` is NaN when the whole record spans < 1 day (F034/F118);
          `active_days_per_week` needs a >= 7-calendar-day window (F035/F048/F117) and
          the new `obs_window_calendar_days` is its denominator.
      G2: excludes event_outcome_simple == 'missing' (467 rows, 0.1%); the friction
          rates then use the friction-decision denominator only (F001), and DS1 drops
          `rate_not_opened` because it would duplicate `rate_dismissed` exactly.
      G4: UTC-only clock — see the `clock=` declaration below (F029/F047/F208).
      G5/G6: excludes rows with NaN secondsSinceOneSecSetup (18.9% of events, but a
          participant-level cohort split — F036); each third needs >= 5 rows (F120/F129).
      G7: requires >=5 FRICTION-DECISION rows per participant (F003), not >=5
          outcome-bearing rows.
    """
    beh = beh.copy()
    beh["timestamp_utc"] = pd.to_datetime(beh["timestamp_utc"], utc=True)

    records = []
    for pid, grp in beh.groupby("participant_id_canonical"):
        feats = {"participant_id_canonical": pid}
        feats.update(volume_features(grp))
        # F001: friction rates on friction-decision rows only. `rate_not_opened` is
        # dropped for DS1 (user decision on record) — with `closed` out of the numerator
        # it is identical to `rate_dismissed` for the two-label decision vocabulary.
        feats.update(outcome_features(grp, "event_outcome_simple", include_rate_not_opened=False))
        feats.update(app_structure_features(grp, "app_name"))
        # F029/F047/F208: DS1's `timestamp` is a raw UTC epoch and the dataset ships no
        # timezone column, so peak_hour_of_day / evening_event_share / morning_event_share
        # genuinely cannot be put on a participant-local clock. Declare that explicitly
        # rather than silently reporting UTC hours as if they were local.
        feats.update(temporal_features(grp, "timestamp_utc", clock=CLOCK_UTC_FALLBACK))
        # hour_entropy is invariant to a whole-hour offset, so UTC is safe here.
        feats.update(hour_entropy(grp, "timestamp_utc"))
        feats.update(ds1_setup_time_features(grp))
        feats.update(ds1_adaptation_via_setup_time(grp))
        # F003: closes no longer terminate an open-run (the shared helper drops
        # non-decision rows before the scan); no argument change needed here.
        feats.update(override_streak_features(grp, "event_outcome_simple", "timestamp_utc"))
        records.append(feats)

    return pd.DataFrame(records)


def build_ds1_survey_features(
    beh: pd.DataFrame,
    pre: pd.DataFrame,
    linkage: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the pre-survey feature table, restricted to behavioral participants.

    Returns one row per participant who has both behavioral data AND a pre-survey
    response. (527 matches — verified against the saved ds1_survey_features.csv.)

    Feature groups:
      G7 Pre-survey baseline     — DIRECT, High (Likert scales, problem/goal flags)
    """
    behavioral_ids = set(beh["participant_id_canonical"].unique())
    pre_linked = pre[pre["participant_id_canonical"].isin(behavioral_ids)].copy()

    records = []
    for _, row in pre_linked.iterrows():
        feats = {"participant_id_canonical": row["participant_id_canonical"]}
        feats.update(ds1_pre_survey_features(row))
        records.append(feats)

    return pd.DataFrame(records)


def build_ds1_prepost_features(
    beh: pd.DataFrame,
    pre: pd.DataFrame,
    post: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the pre-post change feature table for participants with behavioral +
    pre-survey + post-survey.

    Returns one row per participant in the three-way intersection (168 — verified
    against the saved ds1_prepost_features.csv).

    Feature groups:
      G8 Post-survey           — DIRECT, High
      G9 Pre-post change       — DIRECT-DERIVED, Medium
    """
    behavioral_ids = set(beh["participant_id_canonical"].unique())
    pre_idx = pre.set_index("participant_id_canonical")
    post_idx = post.set_index("participant_id_canonical")

    eligible = (
        set(pre_idx.index) & set(post_idx.index) & behavioral_ids
    )

    records = []
    for pid in sorted(eligible):
        pre_row = pre_idx.loc[pid]
        post_row = post_idx.loc[pid]
        feats = {"participant_id_canonical": pid}
        feats.update(ds1_post_survey_features(post_row))
        feats.update(ds1_prepost_change_features(pre_row, post_row))
        records.append(feats)

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_ds1_files(cleaned_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all DS1 cleaned files. Returns (beh, pre, post, linkage)."""
    beh = pd.read_csv(cleaned_dir / "ds1_behavioral_clean.csv")
    pre = pd.read_csv(cleaned_dir / "ds1_pre_survey_clean.csv")
    post = pd.read_csv(cleaned_dir / "ds1_post_survey_clean.csv")
    linkage = pd.read_csv(cleaned_dir / "ds1_participant_linkage.csv")
    return beh, pre, post, linkage
