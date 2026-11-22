"""
ds4_features.py
===============
Participant-level feature extraction for Dataset 4 — Large non-experimental data.

Design decisions and dataset-specific notes
--------------------------------------------
- Unit of observation: one intervention event per row (2,490,260 rows, 1,039 participants)
- Event class distinction (CRITICAL — do not mix these classes):
    * 'intervention_event'  (36.5%): has interventionType + interventionDuration;
      outcome can be opened or dismissed
    * 'app_close_event'     (47.1%): closedApp outcome only; no interventionType;
      structurally distinct — may reflect a different logging path
    * 'no_intervention'     (16.4%): opened or dismissed but no intervention fields.
      NOT purely behavioral: 257,785 of 408,383 such rows (63.1%) predate 2022-10-03,
      the date the interventionType/interventionDuration fields first appear in the log.
  EPOCH CAUTION (F005): no 'intervention_event' row exists before 2022-10-03 and no
  'app_close_event' row before 2021-05-09, in a file that starts 2020-09-30. Class
  shares therefore partly encode enrollment date, not behavior
  (corr(intervention_event_share, obs_window_days) = -0.57).
  Features that compute outcome rates do so separately by event class.
- Outcome-bearing rows:
    * For overall rates: all rows with event_outcome_simple in {opened, dismissed, closed}
    * For intervention-specific rates: intervention_event class only
  F139 CAUTION: the three `rate_*_all` features are NOT behavioural override rates.
  Their denominator pools all three event classes, and whether a participant has
  app_close_event rows at all is a logging-epoch property (305 of 1,039 have zero;
  close logging does not exist before 2021-05-09). Measured
  corr(close_event_share, rate_opened_all) = -0.701 vs +0.222 for
  rate_opened_intervention_events. Use rate_opened_intervention_events for any
  override construct. The `*_all` rates are kept deliberately (documented pooled
  descriptives), NOT re-based on friction decisions.
- Clock (F047): DS4 has NO local-time column. Every temporal feature is scored on
  UTC and temporal_features() is called with clock='utc_no_local_clock_available',
  which is stamped into the `temporal_clock` output column. peak_hour_of_day /
  evening_event_share / morning_event_share are therefore NOT comparable across
  participants (unknown, participant-specific UTC offsets).
- Longitudinal time axis: days_since_first_event (all rows; no NaN)
  Note: secondsSinceStudySetup / weeksSinceStudySetup are INVERTED — do not use.
- DS4-unique richness:
    * 6 intervention types: breathingExercise, minimalBreathingExercise,
      followTheDot, blackScreen, mirror, rotatePhone
    * Longest observation window (up to 897 days)
    * Largest event count per participant (up to 42,119 events)
    * Non-experimental design: no control condition
- Outputs split into two participant-level files:
  1. ds4_behavior_features.csv  — all 1,039 behavioral participants
  2. ds4_survey_features.csv    — 283 participants with survey record
     (survey contains ONLY qualitative open-text; no Likert scales)

Ambiguity note: 'dismissed_other' (812 rows) covers two undocumented dismissal
types mapped to dismissed_other during cleaning. These are excluded from
intervention-specific outcome rates and flagged separately.

Run via: notebooks/12_ds4_feature_extraction.ipynb
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from src.features.behavioral_features import (
    CLOCK_UTC_FALLBACK,
    EVENT_CLASS_DECISION,
    EVENT_CLASS_NONE,
    MIN_WINDOW_DAYS,
    classify_outcome_events,
    volume_features,
    app_structure_features,
    temporal_features,
    adaptation_tertile_features,
    override_streak_features,
    intervention_duration_features,
    hour_entropy,
    merge_feature_dicts,
)

# DS4 intervention types
DS4_INTERVENTION_TYPES = [
    "breathingExercise",
    "minimalBreathingExercise",
    "followTheDot",
    "blackScreen",
    "mirror",
    "rotatePhone",
]


# ---------------------------------------------------------------------------
# DS4-specific feature builders
# ---------------------------------------------------------------------------

def ds4_event_class_volume(df: pd.DataFrame) -> dict:
    """
    Volume features broken out by intervention_event_class.

    Type: DIRECT
    Confidence: High
    Minimum data: >= 1 row

    This is DS4-specific because the three-class event structure is unique
    to this dataset's logging architecture.
    """
    n_total = len(df)
    n_intervention = int((df["intervention_event_class"] == "intervention_event").sum())
    n_close = int((df["intervention_event_class"] == "app_close_event").sum())
    n_no_intervention = int((df["intervention_event_class"] == "no_intervention").sum())

    return {
        "n_intervention_events": n_intervention,
        "n_close_events": n_close,
        "n_no_intervention_events": n_no_intervention,
        "intervention_event_share": round(n_intervention / n_total, 4) if n_total > 0 else np.nan,
        "close_event_share": round(n_close / n_total, 4) if n_total > 0 else np.nan,
        "intervention_events_per_day": np.nan,  # filled after obs_window
    }


def ds4_outcome_by_class(df: pd.DataFrame) -> dict:
    """
    Outcome rates computed separately for each event class.

    Type: DIRECT
    Confidence: High (intervention_event class); Medium (no_intervention class)
    Minimum data: >= 5 rows per class

    Separating by class is essential: combining classes obscures the
    structural difference between active-friction events and close events.
    dismissed_other (812 rows) excluded from rates.

    F001/F213: the outcome vocabulary split is delegated to the shared
    classify_outcome_events() helper instead of two hand-rolled isin() lists, so
    DS4 cannot drift away from the friction-decision / session-termination
    definition every other dataset module now uses. Values are unchanged: the
    pooled `*_all` denominator is still decision + termination rows, and the
    intervention-class rates still use friction-decision rows only.

    F139: the `*_all` rates are deliberately left pooled across event classes.
    They are documented descriptives, not override rates — see module docstring.
    """
    feats = {}
    event_class = classify_outcome_events(df, "event_outcome_simple")

    # Overall (all classes; excludes 'missing'/NaN and the 'dismissed_other'
    # other-outcome label, which is neither a friction decision nor a close).
    valid_all = df[event_class != EVENT_CLASS_NONE]
    valid_all = valid_all[valid_all["event_outcome_simple"] != "dismissed_other"]
    n_all = len(valid_all)
    for outcome in ["opened", "dismissed", "closed"]:
        n_o = (valid_all["event_outcome_simple"] == outcome).sum()
        feats[f"rate_{outcome}_all"] = round(n_o / n_all, 4) if n_all > 0 else np.nan

    # Intervention-event class only, friction-decision rows only.
    is_ie = df["intervention_event_class"] == "intervention_event"
    ie_valid = df[is_ie & (event_class == EVENT_CLASS_DECISION)]
    n_ie = len(ie_valid)
    for outcome in ["opened", "dismissed"]:
        n_o = (ie_valid["event_outcome_simple"] == outcome).sum()
        feats[f"rate_{outcome}_intervention_events"] = round(n_o / n_ie, 4) if n_ie >= 5 else np.nan
    feats["n_intervention_event_outcomes"] = int(n_ie)

    return feats


def ds4_intervention_type_profile(df: pd.DataFrame) -> dict:
    """
    Per-type exposure rate features for DS4's 6 intervention types.

    Type: DIRECT
    Confidence: High (types are logged; coverage 36.5% of events)
    Minimum data: >= 1 intervention event with non-NaN interventionType

    These features are DS4-unique: no other dataset has this type diversity.
    """
    ie_df = df[
        (df["intervention_event_class"] == "intervention_event") &
        df["interventionType"].notna()
    ]
    n_ie = len(ie_df)

    if n_ie == 0:
        feats = {
            "n_intervention_types_seen": 0,
            "dominant_intervention_type": np.nan,
        }
        for t in DS4_INTERVENTION_TYPES:
            feats[f"{t}_rate"] = np.nan
        return feats

    type_counts = ie_df["interventionType"].value_counts()
    dominant = type_counts.index[0]
    n_types_seen = int(ie_df["interventionType"].nunique())

    feats = {
        "n_intervention_types_seen": n_types_seen,
        "dominant_intervention_type": dominant,
    }

    for t in DS4_INTERVENTION_TYPES:
        count = int(type_counts.get(t, 0))
        feats[f"{t}_rate"] = round(count / n_ie, 4)

    return feats


def ds4_longitudinal_activity(df: pd.DataFrame) -> dict:
    """
    Longitudinal activity structure features on the calendar-week grid.

    Type: DIRECT-DERIVED
    Confidence: High
    Minimum data: >= 1 row with a non-NaT timestamp_utc

    F006: both `active_weeks` and `activity_persistence` are now derived from the
    same (ISO year, ISO week) grid built off `timestamp_utc`. `days_since_first_event`
    is no longer used here — it was the fractional-day denominator that let
    `activity_persistence` exceed its own logical maximum of 1.0.
    """
    empty = {
        "active_weeks": np.nan,
        "activity_persistence": np.nan,
        "gaps_over_7d": np.nan,
    }
    if len(df) == 0 or "timestamp_utc" not in df.columns:
        return empty

    ts = pd.to_datetime(df["timestamp_utc"], utc=True).dropna()
    if len(ts) == 0:
        return empty

    # F006: active calendar weeks keyed on the (ISO year, ISO week) grid — a bare
    # .isocalendar().week.nunique() collides week numbers across years and
    # saturates at 53 (39/1,039 DS4 participants understated, up to 61 weeks).
    weeks = ts.dt.tz_localize(None).dt.to_period("W")
    active_weeks = int(weeks.nunique())

    # F006: persistence measured on the SAME calendar-week grid as its numerator,
    # so it is bounded in (0, 1]. The previous fractional-elapsed-day denominator
    # with a max(1, .) clamp pushed it above 1.0 for 837/1,039 participants.
    n_possible_weeks = int((weeks.max() - weeks.min()).n) + 1
    persistence = round(active_weeks / n_possible_weeks, 4)

    # Gaps > 7 days: count periods of inactivity
    dates = ts.dt.date.sort_values().unique()
    gaps_over_7 = 0
    if len(dates) > 1:
        for i in range(1, len(dates)):
            diff = (dates[i] - dates[i - 1]).days
            if diff > 7:
                gaps_over_7 += 1

    # Note: obs_window_days_ds4 was removed — use obs_window_days (from volume_features)
    # which is identical (r=1.0, zero difference across all 1039 participants).
    return {
        "active_weeks": active_weeks,
        "activity_persistence": persistence,
        "gaps_over_7d": gaps_over_7,
    }


def ds4_adaptation_calendar(df: pd.DataFrame) -> dict:
    """
    Longitudinal adaptation via calendar-time tertiles (days_since_first_event).
    Restricted to intervention_event class for a clean comparison.

    Type: PROXY
    Confidence: Medium (non-experimental; confounded by app updates, life events)
    Minimum data: >= 10 intervention events with varying days_since_first_event,
    AND >= MIN_ROWS_PER_THIRD rows in the third being scored

    F120/F129: the thirds are cut on the TIME axis, so they can hold wildly unequal
    event counts. The shared helper now returns NaN for a third holding fewer than
    MIN_ROWS_PER_THIRD rows (so the matching *_change is NaN too) and exports the
    two third sizes. Those sizes are passed through here — a wrapper that silently
    dropped them would defeat the point of exporting them.
    """
    ie_df = df[df["intervention_event_class"] == "intervention_event"].copy()
    result = adaptation_tertile_features(
        ie_df,
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
        # F120/F129: sample sizes behind the rates above, so a downstream user can
        # tell a real adaptation signal from a 5-row third.
        "n_rows_adaptation_eligible_calendar": result["n_rows_adaptation_eligible"],
        "n_early_third_calendar": result["n_early_third"],
        "n_late_third_calendar": result["n_late_third"],
    }
    return renamed


# ---------------------------------------------------------------------------
# Main participant-level builders
# ---------------------------------------------------------------------------

def build_ds4_behavior_features(beh: pd.DataFrame) -> pd.DataFrame:
    """
    Build the behavior-only participant-level feature table for DS4.

    Input: ds4_behavioral_clean.csv (2,490,260 rows)
    Output: one row per participant (1,039 rows)

    Feature groups:
      G1 Volume by event class     — DIRECT, High
      G2 Outcome rates by class    — DIRECT, High
      G3 Intervention type profile — DIRECT, High (DS4-unique)
      G4 Temporal structure        — DIRECT-DERIVED, High
      G5 Longitudinal activity     — DIRECT-DERIVED, High
      G6 Adaptation (calendar)     — PROXY, Medium
      G7 App structure             — DIRECT, High
      G8 Intervention duration     — DIRECT/PROXY, Medium
      G9 Override tendency         — PROXY, Medium
    """
    beh = beh.copy()
    beh["timestamp_utc"] = pd.to_datetime(beh["timestamp_utc"], utc=True)

    records = []
    for pid, grp in beh.groupby("participant_id_canonical"):
        grp = grp.sort_values("timestamp_utc")
        feats = {"participant_id_canonical": pid}

        # G1 volume
        vol = volume_features(grp)
        feats.update(vol)

        # G1 extension: by event class
        ev_class = ds4_event_class_volume(grp)
        # F005: the denominator is the participant's intervention-LOGGING-eligible
        # span, not the full observation window. No 'intervention_event' row can
        # exist before 2022-10-03 in a file that starts 2020-09-30, so dividing an
        # epoch-restricted numerator by a window of up to 897 d systematically
        # understated early-enrolled participants (corr with obs_window_days = -0.18).
        # F034: the same sub-day floor volume_features() applies, so a participant
        # whose intervention events span an hour does not get a x24 amplified rate.
        ie_days = grp.loc[
            grp["intervention_event_class"] == "intervention_event", "days_since_first_event"
        ]
        if len(ie_days) > 0:
            ie_span = float(ie_days.max() - ie_days.min())
            if ie_span >= MIN_WINDOW_DAYS:
                ev_class["intervention_events_per_day"] = round(
                    ev_class["n_intervention_events"] / ie_span, 4
                )
        feats.update(ev_class)

        # G2 outcome by class
        feats.update(ds4_outcome_by_class(grp))

        # G3 intervention type profile
        feats.update(ds4_intervention_type_profile(grp))

        # G4 temporal
        # F047/F029: DS4 is a multi-timezone cohort with NO timezone or local-time
        # column, so the honest declaration is the UTC fallback. peak_hour_of_day /
        # evening_event_share / morning_event_share are consequently not comparable
        # across participants; the choice is stamped into `temporal_clock`.
        feats.update(temporal_features(grp, "timestamp_utc", clock=CLOCK_UTC_FALLBACK))
        # hour_entropy is invariant to a whole-hour offset, so UTC is fine here.
        feats.update(hour_entropy(grp, "timestamp_utc"))

        # G5 longitudinal activity
        feats.update(ds4_longitudinal_activity(grp))

        # G6 adaptation (calendar time, intervention events only)
        feats.update(ds4_adaptation_calendar(grp))

        # G7 app structure
        feats.update(app_structure_features(grp, "app_name"))

        # G8 intervention duration (intervention_event class only)
        ie_df = grp[grp["intervention_event_class"] == "intervention_event"]
        dur_feats = intervention_duration_features(
            ie_df, "interventionDuration", "event_outcome_simple"
        )
        feats.update(dur_feats)

        # G9 override tendency (intervention_event class only for clean signal).
        # F003: the shared helper now drops non-decision rows before the run scan
        # instead of letting them terminate a run. DS4 already passed an
        # intervention_event frame, so the only rows this affects are that frame's
        # 'dismissed_other' / 'missing' rows.
        feats.update(override_streak_features(ie_df, "event_outcome_simple", "timestamp_utc"))

        records.append(feats)

    return pd.DataFrame(records)


def build_ds4_survey_features(
    beh: pd.DataFrame,
    survey: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the survey-linked feature table for DS4.

    Returns one row per participant with both behavioral and survey data (~283).

    IMPORTANT: DS4 survey contains ONLY qualitative open-text columns.
    No psychometric scales exist. Structured features here are limited to:
      - Demographics: age, gender_clean
      - Presence flags: has_survey, survey_qualitative_available

    The text columns (reason_use, benefits, negatives, usage_format) are flagged
    as available for future NLP-based extraction but are NOT featurized here.
    """
    behavioral_ids = set(beh["participant_id_canonical"].unique())
    survey_linked = survey[survey["participant_id_canonical"].isin(behavioral_ids)].copy()

    records = []
    for _, row in survey_linked.iterrows():
        pid = row["participant_id_canonical"]

        # Qualitative text availability flags
        text_cols = ["reason_use", "benefits", "negatives", "usage_format"]
        qualitative_available = int(any(not pd.isna(row.get(c)) for c in text_cols))

        feats = {
            "participant_id_canonical": pid,
            "has_survey": 1,
            "survey_age": row.get("age", np.nan),
            "gender_clean": row.get("gender_clean", np.nan),
            "survey_qualitative_available": qualitative_available,
            # Flags for which qualitative columns are present (for NLP pipeline planning)
            "has_reason_use": int(not pd.isna(row.get("reason_use", np.nan))),
            "has_benefits": int(not pd.isna(row.get("benefits", np.nan))),
            "has_negatives": int(not pd.isna(row.get("negatives", np.nan))),
            "has_usage_format": int(not pd.isna(row.get("usage_format", np.nan))),
        }
        records.append(feats)

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_ds4_files(cleaned_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all DS4 cleaned files. Returns (beh, survey, linkage)."""
    beh = pd.read_csv(cleaned_dir / "ds4_behavioral_clean.csv")
    survey = pd.read_csv(cleaned_dir / "ds4_survey_clean.csv")
    linkage = pd.read_csv(cleaned_dir / "ds4_participant_linkage.csv")
    return beh, survey, linkage
