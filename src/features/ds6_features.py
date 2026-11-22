"""
ds6_features.py
===============
Participant-level feature extraction for Dataset 6 — Danish adolescents.

Design decisions and dataset-specific notes
--------------------------------------------
CRITICAL STRUCTURAL NOTE: DS6 does NOT have dismiss or close outcomes.
All rows in ds6_behavioral_clean.csv have event_outcome_simple == 'opened'.
This means DS6 CANNOT be treated as equivalent to DS1/DS4/DS5 on outcome
dimensions (opened/dismissed/closed). Do not compare DS6 outcome rates
directly with other datasets in Stage 2 harmonization without explicit
acknowledgment of this structural difference.

- Unit of observation: one app-opening event per row (353,796 rows, 243 participants)
- Behavioral events ONLY = openedApp events; no dismiss or close events in resolution
- "Intervention exposure" is approximated by:
    * intervention_duration_sec > 0: friction was shown
    * is_reintervention == 1: a re-intervention event
    * study_period == 'intervention': participation during the intervention phase
- Outcome-bearing rows (conventional): NONE — all outcomes are 'opened'
  Outcome-like analysis instead uses: volume changes, inter-event timing,
  app-adjacency statistics, and app-use pattern changes across study_period.
  (NOT session rate changes -- see the group_id note below.)

- DS6-unique richness:
    * Pre-engineered sequence fields: app_prev (depth 2) -- GENUINE, ~42% same-app rate.
      app_next/app_next2/app_next3 and resolution_next* are NOT usable: DS6's underlying
      log alternates Open->Close->Open->Close and app_next mechanically echoes the current
      row's own app 99.3% of the time (verified on all 353,796 raw rows, 2026-08-06).
    * NOT session structure: group_id is unique per row, first_in_group == 1 for every row
      and last_close_in_group == 0 for every row, so these columns provide no session
      grouping at all (verified on all 353,796 raw rows, 2026-08-05). time_diff_secs IS
      genuine and is a real open->close dwell time for ~99% of rows.
    * Two-period design: baseline vs intervention (explicit study_period column)
    * Two-wave survey: addiction_index, self_control_index, fo_mo, trivsel, etc.
    * Demographic data: age (13–17), gender, region
    * Richest temporal structure: hour, week, day, participation_day columns
    * Youngest adolescent sample in the project

- Outputs split into three participant-level files:
  1. ds6_behavior_features.csv  — all 243 behavioral participants
  2. ds6_survey_features.csv    — participants with survey data (~209 with both waves)
  3. ds6_prepost_features.csv   — participants with both survey waves (~209)

Ambiguity note: 'intervention' study_condition events where intervention_duration_sec
is NaN represent app-open events during the intervention phase for which no friction
was logged. This may reflect: (a) apps not in the friction list, (b) logging gaps,
(c) baseline-like behavior during the intervention phase. These events are counted
but not used in friction-specific features.

Run via: notebooks/14_ds6_feature_extraction.ipynb
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from src.features.behavioral_features import (
    CLOCK_LOCAL,
    volume_features,
    app_structure_features,
    temporal_features,
    reintervention_features,
    hour_entropy,
    merge_feature_dicts,
)

# The five most frequent DS6 intervention types. NOTE (F113): the cleaned file
# contains 15 distinct types; the remaining 10 (blackScreen 1,427 · rotatePhone 986 ·
# lengo 728 · minimalBreathingExercise 683 · streakStudy 328 · loveYourSelf 282 ·
# photoIntervention 219 · webViewIntervention 207 · uSureAboutThat 175 · mirror 49;
# 5,084 events) are collapsed into `other_rate_ds6` so the exposure profile is closed
# and sums to 1.0.
DS6_INTERVENTION_TYPES = ["denmark", "breathingExercise", "math", "followTheDot", "randomText"]

#: Europe/Copenhagen is DS6's participant-local clock (F115): verified on all 353,796
#: rows that `hour_of_day` == event_timestamp_utc.tz_convert('Europe/Copenhagen').hour
#: for 100% of rows (offsets are exactly +2 CEST / +1 CET, no others).
DS6_LOCAL_TZ = "Europe/Copenhagen"


# ---------------------------------------------------------------------------
# DS6-specific feature builders
# ---------------------------------------------------------------------------

def ds6_period_volume(df: pd.DataFrame) -> dict:
    """
    Volume features split by study_period (baseline vs intervention).

    Type: DIRECT
    Confidence: High
    Minimum data: >= 1 row per period

    DS6-unique: the only dataset with an explicit baseline period for comparison.
    """
    baseline = df[df["study_period"] == "baseline"]
    intervention = df[df["study_period"] == "intervention"]

    n_base = len(baseline)
    n_intv = len(intervention)

    def _days(sub):
        if len(sub) == 0:
            return np.nan
        dates = sub["event_date"].nunique() if "event_date" in sub.columns else np.nan
        return dates

    n_base_days = _days(baseline)
    n_intv_days = _days(intervention)

    epd_base = round(n_base / n_base_days, 4) if (n_base_days and n_base_days > 0) else np.nan
    epd_intv = round(n_intv / n_intv_days, 4) if (n_intv_days and n_intv_days > 0) else np.nan

    rate_ratio = np.nan
    if not np.isnan(epd_base) and not np.isnan(epd_intv) and epd_base > 0:
        rate_ratio = round(epd_intv / epd_base, 4)

    return {
        "total_baseline_events": int(n_base),
        "total_intervention_period_events": int(n_intv),
        "n_baseline_days": int(n_base_days) if not np.isnan(n_base_days) else np.nan,
        "n_intervention_days": int(n_intv_days) if not np.isnan(n_intv_days) else np.nan,
        "events_per_day_baseline": epd_base,
        "events_per_day_intervention": epd_intv,
        "event_rate_ratio_intervention_vs_baseline": rate_ratio,
    }


def ds6_timing_features(df: pd.DataFrame) -> dict:
    """
    Inter-event timing feature using time_diff_secs (gap to next event).

    Type: DIRECT
    Confidence: High
    Minimum data: >= 5 non-NaN time_diff_secs values

    REMOVED (Stage 1 QC, 2026-08-05): this function used to be `ds6_session_features()`
    and returned 8 additional "session structure" columns (n_sessions_total,
    n_sessions_baseline, n_sessions_intervention_period, session_rate_baseline,
    session_rate_intervention, session_rate_ratio, share_events_first_in_group,
    share_sessions_with_matched_close), all derived from `group_id`/`first_in_group`/
    `last_close_in_group`. Verified against the raw source file
    (session_time_dataset_97_5_cutoff_data_forwarded.csv, all 353,796 rows): `group_id`
    is unique per row throughout (nunique == row count), `first_in_group` == 1 for
    every row, `last_close_in_group` == 0 for every row. These columns do not group
    multiple events into sessions at all -- every event is its own isolated "group".
    Consequently `n_sessions_total` was numerically identical to `total_events`,
    `session_rate_baseline` identical to `events_per_day_baseline`, and
    `session_rate_ratio` identical to `event_rate_ratio_intervention_vs_baseline`
    (checked: 0.0 max difference across all participants) -- not new information under
    a different name, just a duplicate.
    Separately, `close_ts` (and `last_closedapp_time`) look like real session-close
    timestamps but `close_ts - openedapp_open_time` equals `time_diff_secs` exactly
    (diff ~1e-12, float rounding) -- `close_ts` is the timestamp of the *next open
    event*, not a real app-close signal. Same pattern confirmed in
    `baseline_sessions_filt3.csv`. DS6 has no genuine session-boundary data in either
    raw behavioral file; the only usable timing signal is time-to-next-event, already
    captured below. Do not reintroduce group_id-based session counts.
    """
    mean_time_diff = np.nan
    if "time_diff_secs" in df.columns:
        valid_diffs = df["time_diff_secs"].dropna()
        if len(valid_diffs) >= 5:
            mean_time_diff = round(float(valid_diffs.mean()), 2)

    return {
        "mean_time_diff_secs": mean_time_diff,
    }


def ds6_sequence_features(df: pd.DataFrame) -> dict:
    """
    Sequence and substitution features from the pre-engineered app_prev field.

    Type: NEAR-DIRECT (fields are pre-computed in source data)
    Confidence: High for self-transition rate; Medium for substitution interpretation
    Minimum data: >= 10 rows with non-NaN app_prev

    DS6-unique: no other dataset has pre-engineered sequence depth-3 fields.
    The substitution interpretation requires domain judgment: not every adjacent app
    is a substitution response — some may reflect unrelated multitasking.

    CHANGED (Stage 1 QC, 2026-08-06): this function used to be built on `app_next`
    (self_transition_rate/cross_app_transition_rate/app_next_entropy/n_unique_next_apps/
    top_next_app/top_next_app_share, plus a `resolution_next_open_rate` field). Verified
    on the full raw file that `app_next` does NOT represent "the next app the user opened":
    DS6's true underlying event log alternates Open->Close->Open->Close (this exported file
    keeps only the Open rows), and `app_next` was computed against that full alternating
    sequence -- so for 99.3% of rows, the very next logged record is that SAME app's own
    close event, making `app_next == app_name` mechanically true, not a behavioral fact.
    (Confirmed via `resolution_next`: it equals 'closedApp' for 99.4% of rows; conditioned on
    that, `app_next == app_name` 99.3% of the time.) This explains the previously-documented
    "self_transition_rate near-ceiling" finding (2026-04-16) more precisely than the original
    "within-session same-app reopening" explanation -- it was never a session-grouping
    artifact (DS6 has no real sessions at all, see `ds6_timing_features()`), it was this
    look-ahead mechanics.
    `app_prev` does NOT have this problem: looking backward from an Open row, the
    immediately-prior logged record is typically the *previous, different* app's close event,
    not this app's own. Verified: `app_prev == app_name` only ~42% overall, stable across
    resolution_last categories (39-64%) -- a plausible, non-mechanical same-app-vs-switch
    split, unlike app_next's 99.3%. `app_next2`/`resolution_next2` also verified genuine
    (skips the intervening close), but `app_prev` is used here as it needs no conditioning on
    a resolution code and is directly available.
    `resolution_next_open_rate` (proportion where resolution_next == 'openedApp') was removed:
    verified near-constant-near-zero (0.5% overall) for the same look-ahead-mechanics reason --
    not useful, same treatment as the `reintervention_open_rate` removal (2026-04-16).
    Renamed on this pass for clarity, since the underlying field changed direction:
    app_next_entropy -> app_transition_entropy, n_unique_next_apps -> n_unique_transition_apps,
    top_next_app -> top_transition_app, top_next_app_share -> top_transition_app_share.
    self_transition_rate/cross_app_transition_rate keep their names (direction-symmetric
    construct); `max_consecutive_same_app` is unaffected by any of this -- it is built from
    the exported file's own row order (real consecutive Open events), not from app_next/prev.

    F114 WARNING (do not read three of these as transition statistics):
    `app_transition_entropy`, `n_unique_transition_apps` and `top_transition_app` are
    computed from the MARGINAL distribution of `app_prev` alone -- no joint or conditional
    distribution is ever formed. Within a participant `app_prev` is `app_name` lagged one
    event, so they are the app-usage marginal minus one boundary observation. Verified on
    ds6_behavior_features.csv (n=242): `n_unique_transition_apps` == `n_unique_apps` for
    242/242 (max abs diff 0.0), r(app_transition_entropy, app_entropy) = 0.983 (mean abs
    diff 0.039 bits), `top_transition_app` == `top_app` for 94.6%. Do not enter them
    alongside app_entropy/n_unique_apps/top_app, and do not label them "substitution
    diversity". `self_transition_rate`/`cross_app_transition_rate` ARE genuine adjacency
    statistics, though self_transition_rate correlates r=0.86 with `app_herfindahl`.
    A real substitution measure would be H(app_name | app_prev) or the entropy of the
    joint (app_prev, app_name) edge distribution -- neither is computed here.
    Kept as-is (not dropped) because the columns are already shipped and consumed; the
    fix is documentation, per the F114 patch.
    """
    prev_valid = df[df["app_prev"].notna() & df["app_name"].notna()].copy()
    n_prev = len(prev_valid)

    if n_prev < 10:
        return {
            "self_transition_rate": np.nan,
            "cross_app_transition_rate": np.nan,
            "app_transition_entropy": np.nan,
            "n_unique_transition_apps": np.nan,
            "top_transition_app": np.nan,
            "top_transition_app_share": np.nan,
            "max_consecutive_same_app": np.nan,
        }

    is_self = prev_valid["app_prev"] == prev_valid["app_name"]
    self_rate = round(float(is_self.mean()), 4)
    cross_rate = round(float((~is_self).mean()), 4)

    prev_counts = prev_valid["app_prev"].value_counts()
    prev_shares = prev_counts / n_prev
    app_transition_ent = float(-(prev_shares * np.log2(prev_shares + 1e-12)).sum())

    top_prev = prev_counts.index[0]
    top_prev_share = round(float(prev_shares.iloc[0]), 4)

    # Max consecutive same-app events (habit-chain proxy) -- unaffected, uses the
    # exported file's own real Open-event row order, not app_next/app_prev.
    app_seq = df.sort_values("event_timestamp_utc")["app_name"].tolist()
    max_run = 0
    curr = 0
    prev_app = None
    for app in app_seq:
        if app == prev_app:
            curr += 1
        else:
            curr = 1
        # Update on every iteration, not only inside the repeat branch: a participant
        # whose consecutive apps never repeat must score 1, not 0. Latent in DS6 (the
        # observed minimum across all 242 eligible participants is 5) but the previous
        # form was wrong for any sparser or per-period-split reuse of this function.
        max_run = max(max_run, curr)
        prev_app = app

    return {
        "self_transition_rate": self_rate,
        "cross_app_transition_rate": cross_rate,
        "app_transition_entropy": round(app_transition_ent, 4),
        "n_unique_transition_apps": int(prev_counts.shape[0]),
        "top_transition_app": top_prev,
        "top_transition_app_share": top_prev_share,
        "max_consecutive_same_app": int(max_run),
    }


def ds6_intervention_type_profile(df: pd.DataFrame) -> dict:
    """
    Per-type exposure rate features for DS6's intervention types.

    Type: DIRECT
    Confidence: High (types are logged for ~33% of events)
    Minimum data: >= 1 row with non-NaN intervention_type

    F113: `DS6_INTERVENTION_TYPES` covers only 5 of the 15 types present in the
    cleaned file, so the five `*_rate_ds6` shares did not sum to 1 for 64 of the 239
    participants with any typed friction event (7 summed below 0.50, and one —
    2osZDjrWckZtfW8, 728 `lengo` events — summed to exactly 0.000, indistinguishable
    from a participant with no friction exposure at all). `n_ds6_intervention_types_seen`
    and `dominant_intervention_type_ds6` were already computed on the full 15-type
    vocabulary, so they contradicted the rate block in their own row. `other_rate_ds6`
    closes the profile.
    """
    with_type = df[df["intervention_type"].notna()].copy()
    n_typed = len(with_type)

    if n_typed == 0:
        feats = {
            "n_ds6_intervention_types_seen": 0,
            "dominant_intervention_type_ds6": np.nan,
        }
        for t in DS6_INTERVENTION_TYPES:
            feats[f"{t}_rate_ds6"] = np.nan
        # F113: NaN (not 0.0) here, matching the listed types -- this participant has
        # no typed friction event at all, so no share is defined.
        feats["other_rate_ds6"] = np.nan
        return feats

    type_counts = with_type["intervention_type"].value_counts()
    dominant = type_counts.index[0]

    feats = {
        "n_ds6_intervention_types_seen": int(with_type["intervention_type"].nunique()),
        "dominant_intervention_type_ds6": dominant,
    }
    # F113: accumulate the listed types so the residual can close the profile to 1.0.
    listed_total = 0
    for t in DS6_INTERVENTION_TYPES:
        cnt = int(type_counts.get(t, 0))
        listed_total += cnt
        feats[f"{t}_rate_ds6"] = round(cnt / n_typed, 4)
    feats["other_rate_ds6"] = round((n_typed - listed_total) / n_typed, 4)

    # Intervention duration features
    dur_valid = df[df["intervention_duration_sec"].notna() & (df["intervention_duration_sec"] > 0)]
    feats["n_friction_events_ds6"] = int(len(dur_valid))
    feats["mean_intervention_duration_ds6"] = (
        round(float(dur_valid["intervention_duration_sec"].mean()), 3)
        if len(dur_valid) >= 5 else np.nan
    )

    return feats


def ds6_period_app_structure(df: pd.DataFrame) -> dict:
    """
    App structure features separately for baseline and intervention periods.

    Type: DIRECT
    Confidence: High
    Minimum data: >= 5 events per period
    """
    feats = {}
    for period in ["baseline", "intervention"]:
        sub = df[df["study_period"] == period]
        if len(sub) < 5:
            feats[f"n_unique_apps_{period}"] = np.nan
            feats[f"app_entropy_{period}"] = np.nan
            feats[f"top_app_{period}"] = np.nan
            feats[f"top_app_share_{period}"] = np.nan
            continue
        app_counts = sub["app_name"].value_counts()
        n_total = len(sub)
        shares = app_counts / n_total
        ent = float(-(shares * np.log2(shares + 1e-12)).sum())
        feats[f"n_unique_apps_{period}"] = int(app_counts.shape[0])
        feats[f"app_entropy_{period}"] = round(ent, 4)
        feats[f"top_app_{period}"] = app_counts.index[0]
        feats[f"top_app_share_{period}"] = round(float(shares.iloc[0]), 4)

    # Whether top app changed across periods
    base_top = feats.get("top_app_baseline", np.nan)
    intv_top = feats.get("top_app_intervention", np.nan)
    if not pd.isna(base_top) and not pd.isna(intv_top):
        feats["top_app_period_consistent"] = int(base_top == intv_top)
    else:
        feats["top_app_period_consistent"] = np.nan

    # Entropy change baseline -> intervention
    ent_base = feats.get("app_entropy_baseline", np.nan)
    ent_intv = feats.get("app_entropy_intervention", np.nan)
    if not np.isnan(ent_base) and not np.isnan(ent_intv):
        feats["app_entropy_change"] = round(ent_intv - ent_base, 4)
    else:
        feats["app_entropy_change"] = np.nan

    return feats


def ds6_period_temporal(df: pd.DataFrame) -> dict:
    """
    Temporal pattern comparison across study periods.

    Type: DIRECT-DERIVED
    Confidence: High
    Minimum data: >= 5 events per period
    """
    feats = {}
    for period in ["baseline", "intervention"]:
        sub = df[df["study_period"] == period]
        if len(sub) < 5 or "hour_of_day" not in sub.columns:
            feats[f"peak_hour_{period}"] = np.nan
            continue
        feats[f"peak_hour_{period}"] = int(sub["hour_of_day"].value_counts().idxmax())

    # Hour entropy (context diversity proxy)
    # Named 'hour_entropy' to match DS1/DS4/DS5 naming convention.
    # Computed from pre-engineered hour_of_day column rather than extracted from timestamps,
    # but the result is equivalent.
    if "hour_of_day" in df.columns and len(df) >= 10:
        hour_counts = df["hour_of_day"].value_counts(normalize=True)
        feats["hour_entropy"] = round(
            float(-(hour_counts * np.log2(hour_counts + 1e-12)).sum()), 4
        )
    else:
        feats["hour_entropy"] = np.nan

    # Participation span
    if "participation_day" in df.columns:
        feats["participation_day_max"] = int(df["participation_day"].max())
    else:
        feats["participation_day_max"] = np.nan

    if "study_week" in df.columns:
        feats["study_week_max"] = int(df["study_week"].max())
    else:
        feats["study_week_max"] = np.nan

    return feats


def ds6_longitudinal_adaptation(df: pd.DataFrame) -> dict:
    """
    Longitudinal adaptation features using participation_day as time axis.

    Type: PROXY
    Confidence: Medium (cohort effects; study design confounds individual trajectories)
    Minimum data: >= 14 participation days (for early/late comparison)

    Unlike DS1 (setup-time) and DS4 (calendar days), DS6 uses participation_day
    which is study-design-anchored and more directly comparable within the sample.

    REMOVED (Stage 1 QC, 2026-08-05): `session_rate_early`/`session_rate_late` used
    to be computed here via `group_id.nunique()`. Removed because `group_id` is
    unique per row in the raw data (verified on all 353,796 rows) and does not group
    multiple events into sessions -- these two columns were numerically identical to
    an event-count rate, not a distinct session-level signal. See
    `ds6_timing_features()` docstring for the full verification. Do not reintroduce.

    F116 WARNING: `event_rate_slope` is a single OLS line fitted across the participant's
    WHOLE record, pooling baseline and intervention. DS6's dominant behavioural fact is a
    level step between periods (~45 -> ~29 events/day), so the slope is largely a
    re-expression of that step: r = 0.936 (n=241) with
    `events_per_day_intervention - events_per_day_baseline`, which
    `event_rate_ratio_intervention_vs_baseline` already encodes. The 83.9% negative-slope
    rate is what a two-level step function mechanically produces -- it is NOT evidence of
    gradual within-period habituation. Corroborated independently by DS6 StoP (notebook
    73): the level moved, the within-period drift `h_period` did not (paired t p=0.659).
    Do not enter it in the same model as the period-ratio feature.
    """
    # F196(b): the gate must count participation DAYS, not event rows -- the docstring
    # above and ds6_features.md Group 8 both state ">= 14 participation days", but
    # `len(df) < 14` counted rows, so a participant with 14 events on 2 days passed.
    if "participation_day" not in df.columns or df["participation_day"].nunique() < 14:
        return {
            "event_rate_week1": np.nan,
            "event_rate_last_week": np.nan,
            "event_rate_slope": np.nan,
        }

    # Daily event counts.
    # F196(c) KNOWN LIMITATION (documented, not changed): `daily` holds only days with
    # >= 1 event, so the rates below are means over ACTIVE days, not calendar days.
    daily = df.groupby("participation_day").size().reset_index(name="n_events")
    max_day = int(daily["participation_day"].max())

    # F196(a): 7-day windows on BOTH ends. participation_day starts at 0 for 215/243
    # participants, so a literal `<= 7` gave week 1 an 8-day window while last_week
    # always got 7 -- the two were then compared with each other.
    min_day = int(daily["participation_day"].min())
    week1 = daily[daily["participation_day"] <= min_day + 6]
    last_week = daily[daily["participation_day"] >= max_day - 6]

    rate_w1 = round(float(week1["n_events"].mean()), 3) if len(week1) >= 3 else np.nan
    rate_last = round(float(last_week["n_events"].mean()), 3) if len(last_week) >= 3 else np.nan

    # Linear slope of daily event count (proxy for trajectory)
    slope = np.nan
    if len(daily) >= 7:
        x = daily["participation_day"].values
        y = daily["n_events"].values
        try:
            slope = round(float(np.polyfit(x, y, 1)[0]), 5)
        except Exception:
            slope = np.nan

    return {
        "event_rate_week1": rate_w1,
        "event_rate_last_week": rate_last,
        "event_rate_slope": slope,
    }


# ---------------------------------------------------------------------------
# Survey feature builders
# ---------------------------------------------------------------------------

def ds6_survey_features_wave(survey_row: pd.Series, wave: int) -> dict:
    """
    Extract psychometric index features for one survey wave.

    Type: DIRECT (pre-computed indices from validated scales)
    Confidence: High
    Available for: wave 1 = 269 participants, wave 2 = 209 participants
    """
    suffix = "pre" if wave == 1 else "post"

    def _val(col):
        v = survey_row.get(col, np.nan)
        return np.nan if pd.isna(v) else float(v)

    return {
        f"addiction_index_{suffix}": _val("addiction_index"),
        f"self_control_index_{suffix}": _val("self_control_index"),
        f"fo_mo_{suffix}": _val("fo_mo"),
        f"trivsel_{suffix}": _val("trivsel"),
        f"socialconnection_{suffix}": _val("socialconnection"),
        f"kontrolover_so_me_{suffix}": _val("kontrolover_so_me"),
        f"taenkerpa_so_me_{suffix}": _val("taenkerpa_so_me"),
        f"tilfredsmed_so_me_{suffix}": _val("tilfredsmed_so_me"),
    }


def ds6_prepost_change_features(pre_row: pd.Series, post_row: pd.Series) -> dict:
    """
    Compute signed pre-to-post change scores for DS6 survey indices.

    Type: DIRECT-DERIVED
    Confidence: Medium (attrition from wave 1 to wave 2; 60 participants dropped)
    Available for: ~209 participants with both survey waves
    """
    index_cols = [
        "addiction_index", "self_control_index", "fo_mo",
        "trivsel", "socialconnection", "kontrolover_so_me",
        "taenkerpa_so_me", "tilfredsmed_so_me",
    ]

    feats = {}
    for col in index_cols:
        pre = pre_row.get(col, np.nan)
        post = post_row.get(col, np.nan)
        if pd.isna(pre) or pd.isna(post):
            feats[f"{col}_change"] = np.nan
        else:
            feats[f"{col}_change"] = round(float(post) - float(pre), 3)

    return feats


# ---------------------------------------------------------------------------
# Main participant-level builders
# ---------------------------------------------------------------------------

def build_ds6_behavior_features(
    beh: pd.DataFrame,
    demo: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the behavior-only participant-level feature table for DS6.

    Merges demographics (age, gender, region) from demo file.

    Input: ds6_behavioral_clean.csv (353,796 rows) + ds6_demographics_clean.csv
    Output: one row per participant (243 rows)

    Feature groups:
      G1 Volume by period              — DIRECT, High
      G2 Inter-event timing            — DIRECT, High (mean_time_diff_secs only;
                                          session-structure columns removed, see
                                          ds6_timing_features() docstring)
      G3 Intervention exposure         — DIRECT, High
      G4 Sequence / substitution       — NEAR-DIRECT, High (DS6-unique)
      G5 App structure overall         — DIRECT, High
      G6 App structure by period       — DIRECT, High
      G7 Temporal structure            — DIRECT-DERIVED, High (Europe/Copenhagen
                                          LOCAL clock throughout, see F115 below)
      G8 Longitudinal adaptation       — PROXY, Medium
      study_condition / demographics   — DIRECT

    NOTE: No outcome rate features (opened/dismissed/closed) are computed
    because ALL events in DS6 have outcome = 'opened'. Volume and session
    rate changes across periods serve as the behavioral response proxy.
    Confirmed on the cleaned file (2026-08-08): event_outcome_simple == 'opened' for
    all 353,796 rows, so the shared module's friction-decision-denominator change
    (F001/F003/F213) is a structural no-op for DS6 -- this module does not import
    outcome_features() or override_streak_features() at all.

    Column changes on this pass:
      + obs_window_calendar_days   (new, from volume_features(); F035/F048/F117)
      + temporal_clock             (new, from temporal_features(); = 'local:timestamp_local')
      + other_rate_ds6             (new; F113 closes the intervention-type profile)
      ~ peak_hour_of_day / evening_event_share / morning_event_share /
        weekend_event_share        (now LOCAL, were UTC; F115)
      ~ events_per_day / active_days_per_week  (shared-module denominator fixes)
      ~ event_rate_week1 / event_rate_slope    (F196 symmetric window + day-based gate)
      → mean_reintervention_delay_sec renamed to
        mean_configured_reintervention_interval_sec (F112)
    """
    beh = beh.copy()
    beh["event_timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], utc=True)
    beh["timestamp_utc"] = beh["event_timestamp_utc"]
    # F115: DS6 mixed clocks inside a single feature row -- peak_hour_of_day /
    # evening_event_share / morning_event_share came from temporal_features() on the
    # UTC timestamp, while peak_hour_baseline / peak_hour_intervention / hour_entropy
    # came from the LOCAL `hour_of_day` column. Build the local clock explicitly and
    # score the hour-axis features on it, so the whole table is on one clock.
    # NOTE: `event_date` is deliberately left on UTC. Recomputing it locally would
    # move 2.36% of events to a different calendar day and change n_baseline_days /
    # n_intervention_days / events_per_day_* -- which every DS6 Stage 4 model notebook
    # already consumes. That is a separate, larger decision than this fix.
    beh["timestamp_local"] = beh["event_timestamp_utc"].dt.tz_convert(DS6_LOCAL_TZ)
    if "event_date" in beh.columns:
        beh["event_date"] = pd.to_datetime(beh["event_date"]).dt.date

    # Build demo lookup
    demo_idx = demo.set_index("participant_id_canonical")

    records = []
    for pid, grp in beh.groupby("participant_id_canonical"):
        grp = grp.sort_values("timestamp_utc")
        feats = {"participant_id_canonical": pid}

        # Study condition (directly in behavioral file)
        feats["study_condition"] = grp["study_condition"].mode().iloc[0] if len(grp) > 0 else np.nan

        # Demographics
        if pid in demo_idx.index:
            demo_row = demo_idx.loc[pid]
            feats["age"] = demo_row.get("age", np.nan)
            feats["gender"] = demo_row.get("gender", np.nan)
            feats["region"] = demo_row.get("region", np.nan)
        else:
            feats["age"] = np.nan
            feats["gender"] = np.nan
            feats["region"] = np.nan

        # G1 overall volume
        vol = volume_features(grp)
        feats.update(vol)

        # G1 period volume
        feats.update(ds6_period_volume(grp))

        # G2 inter-event timing
        feats.update(ds6_timing_features(grp))

        # G3 intervention exposure
        feats.update(ds6_intervention_type_profile(grp))
        ri_feats = reintervention_features(
            grp,
            reintervention_flag_col="is_reintervention",
            reintervention_delay_col="reintervention_delay_sec",
            outcome_col="event_outcome_simple",  # all 'opened' — rate will be 1.0
        )
        # Drop reintervention_open_rate: always 1.0 in DS6 because all outcomes are 'opened'.
        # Including it would mislead downstream users into treating it as a behavioral signal.
        ri_feats.pop("reintervention_open_rate", None)
        # F112 (DS6-local half): every non-NaN DS6 `reintervention_delay_sec` is an exact
        # multiple of 60 s (60-2700, 45 distinct levels) -- it is the CONFIGURED
        # re-intervention interval, not an observed latency. Renamed here rather than in
        # the shared module, where DS5's value really is a delay.
        ri_feats["mean_configured_reintervention_interval_sec"] = ri_feats.pop(
            "mean_reintervention_delay_sec"
        )
        feats.update(ri_feats)

        # G4 sequence / substitution
        feats.update(ds6_sequence_features(grp))

        # G5 app structure overall
        feats.update(app_structure_features(grp, "app_name"))

        # G6 app structure by period
        feats.update(ds6_period_app_structure(grp))

        # G7 temporal
        # F115/F029: local clock declared explicitly. `hour_of_day` (used by
        # ds6_period_temporal below) is Europe/Copenhagen, verified equal to
        # timestamp_local.dt.hour for 100% of 353,796 rows, so both halves of G7
        # now agree.
        feats.update(temporal_features(grp, "timestamp_local", clock=CLOCK_LOCAL))
        feats.update(ds6_period_temporal(grp))

        # G8 longitudinal adaptation
        feats.update(ds6_longitudinal_adaptation(grp))

        records.append(feats)

    return pd.DataFrame(records)


def build_ds6_survey_features(
    beh: pd.DataFrame,
    survey: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the survey feature table for DS6.

    Returns one row per participant who has behavioral data AND wave 1 survey.
    Includes wave 2 indices where available (NaN for participants missing wave 2).

    Feature groups:
      G10 Survey wave 1 (pre) indices   — DIRECT, High
      G11 Survey wave 2 (post) indices  — DIRECT, High (209 participants only)
    """
    behavioral_ids = set(beh["participant_id_canonical"].unique())
    survey_beh = survey[survey["participant_id_canonical"].isin(behavioral_ids)]

    # Build wave 1 and wave 2 lookup
    wave1 = survey_beh[survey_beh["survey_nr"] == 1].set_index("participant_id_canonical")
    wave2 = survey_beh[survey_beh["survey_nr"] == 2].set_index("participant_id_canonical")

    eligible = set(wave1.index)

    records = []
    for pid in sorted(eligible):
        feats = {"participant_id_canonical": pid}
        feats["study_condition"] = wave1.loc[pid].get("cond", np.nan)
        feats.update(ds6_survey_features_wave(wave1.loc[pid], wave=1))
        # Wave 2 where available
        if pid in wave2.index:
            feats.update(ds6_survey_features_wave(wave2.loc[pid], wave=2))
            feats["has_wave2_survey"] = 1
        else:
            for col in ["addiction_index", "self_control_index", "fo_mo",
                        "trivsel", "socialconnection", "kontrolover_so_me",
                        "taenkerpa_so_me", "tilfredsmed_so_me"]:
                feats[f"{col}_post"] = np.nan
            feats["has_wave2_survey"] = 0
        records.append(feats)

    return pd.DataFrame(records)


def build_ds6_prepost_features(
    beh: pd.DataFrame,
    survey: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the pre-post survey change feature table for DS6.

    Returns one row per participant with behavioral + both survey waves (~209).

    Feature groups:
      G12 Pre-post change scores   — DIRECT-DERIVED, Medium
    """
    behavioral_ids = set(beh["participant_id_canonical"].unique())
    survey_beh = survey[survey["participant_id_canonical"].isin(behavioral_ids)]

    wave1 = survey_beh[survey_beh["survey_nr"] == 1].set_index("participant_id_canonical")
    wave2 = survey_beh[survey_beh["survey_nr"] == 2].set_index("participant_id_canonical")

    eligible = set(wave1.index) & set(wave2.index) & behavioral_ids

    records = []
    for pid in sorted(eligible):
        pre_row = wave1.loc[pid]
        post_row = wave2.loc[pid]
        feats = {
            "participant_id_canonical": pid,
            "study_condition": pre_row.get("cond", np.nan),
        }
        feats.update(ds6_prepost_change_features(pre_row, post_row))
        records.append(feats)

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_ds6_files(cleaned_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all DS6 cleaned files. Returns (beh, survey, demo, linkage)."""
    beh = pd.read_csv(cleaned_dir / "ds6_behavioral_clean.csv")
    survey = pd.read_csv(cleaned_dir / "ds6_survey_clean.csv")
    demo = pd.read_csv(cleaned_dir / "ds6_demographics_clean.csv")
    linkage = pd.read_csv(cleaned_dir / "ds6_participant_linkage.csv")
    return beh, survey, demo, linkage
