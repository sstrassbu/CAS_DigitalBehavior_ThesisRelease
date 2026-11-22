"""
Loaders for Dataset 6 -- Danish adolescents, experimental longitudinal study.

Delimiter note: ALL CSV files are COMMA-delimited.

Timestamp note: behavioral timestamps are ISO 8601 UTC strings ('2024-10-04T20:56:16Z').
  Parse directly with pd.to_datetime(df['timestamp'], utc=True). No localization needed.

ID note: behavioral 'ID' directly matches survey 'response_id' and demographic 'ID'.
  No prefix stripping or transformation is needed.

File selection note: use session_time_dataset_97_5_cutoff_data_forwarded.csv as the
  primary behavioral file -- it covers both baseline AND intervention periods.
  baseline_sessions_filt3.csv is a filtered baseline-only subset with additional
  sequence engineering; use it for baseline-specific analysis.

Usage
-----
from src.io.load_dataset_6 import (
    load_behavioral, load_demographics, load_survey_clean,
    load_behavioral_clean, load_survey_clean_out, load_participant_linkage
)

# Raw files
beh  = load_behavioral()        # session file (both periods)
demo = load_demographics()
surv = load_survey_clean()      # cleaned survey (2 waves, pre-computed indices)

# Cleaned outputs
beh_clean = load_behavioral_clean()
linkage   = load_participant_linkage()
"""

from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[2]

DS6_RAW  = _REPO_ROOT / "data_raw" / "6. data set, Danish adolescents" / "Data"
DS6_BEH  = DS6_RAW / "behavioral data"

_SESSION_CSV    = DS6_BEH / "session_time_dataset_97_5_cutoff_data_forwarded.csv"
_BASELINE_CSV   = DS6_BEH / "baseline_sessions_filt3.csv"
_DEMO_CSV       = DS6_BEH / "demographic_data.csv"
_SURVEY_C_CSV   = DS6_BEH / "survey_data_clean.csv"
_SURVEY_F_CSV   = DS6_BEH / "survey_data_full.csv"

DS6_CLEANED = _REPO_ROOT / "outputs" / "cleaned"

_BEH_CLEAN      = DS6_CLEANED / "ds6_behavioral_clean.csv"
_SURV_CLEAN     = DS6_CLEANED / "ds6_survey_clean.csv"
_DEMO_CLEAN     = DS6_CLEANED / "ds6_demographics_clean.csv"
_LINKAGE_CLEAN  = DS6_CLEANED / "ds6_participant_linkage.csv"

# ---------------------------------------------------------------------------
# Expected columns (for validation on load)
# ---------------------------------------------------------------------------

_SESSION_KEY_COLS = [
    "ID", "study_id", "app", "timestamp", "time",
    "resolution", "cond", "condition", "period",
    "interventionDuration", "interventionType", "isReIntervention",
    "timeIntervalUntilReIntervention", "participation_day",
    "group_id", "app_next", "app_prev", "resolution_next",
    "time_diff_secs", "row_id",
]

_DEMO_COLS = ["ID", "age", "gender", "region"]

_SURVEY_CLEAN_COLS = [
    "response_id", "cond", "start_date", "end_date", "survey_nr",
    "addiction_index", "retention_index", "self_control_index",
    "trivsel", "socialconnection", "fo_mo",
    "kontrolover_so_me", "taenkerpa_so_me", "tilfredsmed_so_me",
    "cond_exp2", "survey_nr_fact",
]

# ---------------------------------------------------------------------------
# Raw loaders
# ---------------------------------------------------------------------------


def load_behavioral(validate: bool = True) -> pd.DataFrame:
    """
    Load the primary DS6 behavioral event file (both baseline and intervention periods).

    Returns
    -------
    pd.DataFrame
        353,796 rows x 70 columns (raw, unmodified).
        Delimiter: COMMA.
        Timestamp: ISO 8601 UTC string -- parse with pd.to_datetime(df['timestamp'], utc=True).

    Notes
    -----
    - ALL rows have resolution = 'openedApp'. No close or dismiss outcomes are stored.
      Session close timing is encoded via group_id, close_ts, and time_diff_secs columns.
    - Period: 'baseline' (158,889 rows) and 'intervention' (194,907 rows).
    - condition (text): 'control', 'default', 'intervention'.
      cond (numeric): 1-6 (cohort groups). Use 'condition' for most analysis.
    - 243 unique participants.
    - isReIntervention: 2,120 events across the file.
    - interventionType: NaN for ~67% (control / baseline events);
      values: denmark, breathingExercise, math, followTheDot, randomText.
    - Pre-engineered sequence columns present: app_next*, app_prev*, resolution_next*,
      time_diff_secs, time_diff_minutes, group_id.
    - purpose: 89% NaN -- not usable for routine analysis.
    - ID column directly matches response_id in survey and ID in demographics.
    - See outputs/reports/ds6_audit_report.md for full audit findings.
    """
    df = pd.read_csv(_SESSION_CSV, low_memory=False)
    if validate:
        _check_columns(df, _SESSION_KEY_COLS, "behavioral (session)")
    return df


def load_behavioral_baseline(validate: bool = True) -> pd.DataFrame:
    """
    Load the baseline-only behavioral file (openedApp events, baseline period only).

    Returns
    -------
    pd.DataFrame
        195,515 rows x 63 columns (raw, unmodified).

    Notes
    -----
    - Baseline period only; ALL rows: period='baseline', resolution='openedApp'.
    - Contains date2 (date-only field) and close_ts for session close matching.
    - 244 unique participants.
    - Use this file for baseline-specific sequence and substitution analysis.
    - Use load_behavioral() for cross-period analysis.
    """
    return pd.read_csv(_BASELINE_CSV, low_memory=False)


def load_demographics(validate: bool = True) -> pd.DataFrame:
    """
    Load the DS6 demographic file.

    Returns
    -------
    pd.DataFrame
        399 rows x 4 columns (raw, unmodified).
        Delimiter: COMMA.

    Notes
    -----
    - gender: Danish text -- 'kvinde' (female), 'mand' (male); 1 NaN.
    - age: 13-17 (true adolescent range).
    - region: 5 Danish regions.
    - 399 participants; only 243 have behavioral data.
    - ID matches behavioral 'ID' and survey 'response_id' directly.
    """
    df = pd.read_csv(_DEMO_CSV, low_memory=False)
    if validate:
        _check_columns(df, _DEMO_COLS, "demographics")
    return df


def load_survey_clean(validate: bool = True) -> pd.DataFrame:
    """
    Load the cleaned DS6 survey file (pre-computed indices, 2 waves).

    Returns
    -------
    pd.DataFrame
        478 rows x 17 columns (raw, unmodified).
        Delimiter: COMMA.

    Notes
    -----
    - survey_nr: 1 = pre-intervention wave, 2 = post-intervention wave.
    - 269 unique response_id; 209 have both waves (478 total rows).
    - Columns: pre-computed psychometric indices -- addiction_index,
      self_control_index, retention_index, trivsel, socialconnection, fo_mo.
    - response_id matches behavioral 'ID' directly.
    - Raw items available in survey_data_full.csv (3 waves, 440 participants).
    """
    df = pd.read_csv(_SURVEY_C_CSV, low_memory=False)
    if validate:
        _check_columns(df, _SURVEY_CLEAN_COLS, "survey_clean")
    return df


def load_survey_full() -> pd.DataFrame:
    """
    Load the full DS6 survey file (raw items, 3 waves, 440 participants).

    Returns
    -------
    pd.DataFrame
        929 rows x 32 columns (raw, unmodified).

    Notes
    -----
    - Includes raw items: afhaengighed_1-6 (addiction), selvkontrol_1-5 (self-control).
    - survey_nr: 1, 2, 3 (three waves).
    - 440 unique response_id.
    - Use this for item-level analysis or recomputing indices.
    """
    return pd.read_csv(_SURVEY_F_CSV, low_memory=False)


# ---------------------------------------------------------------------------
# Cleaned loaders
# ---------------------------------------------------------------------------


def load_behavioral_clean(parse_timestamps: bool = True) -> pd.DataFrame:
    """
    Load the cleaned DS6 behavioral file (outputs/cleaned/ds6_behavioral_clean.csv).

    Returns
    -------
    pd.DataFrame
        353,796 rows x 34 columns.
        event_timestamp_utc is UTC-aware if parse_timestamps=True.
        Includes participant_id_canonical, event_outcome_simple, study_period,
        study_condition, intervention fields, sequence columns, days_since_first_event.

    Example
    -------
    beh = load_behavioral_clean()
    demo = load_demographics_clean()
    merged = beh.merge(demo[["participant_id_canonical","age","gender"]],
                       on="participant_id_canonical", how="left")
    """
    df = pd.read_csv(_BEH_CLEAN, low_memory=False)
    if parse_timestamps:
        df["event_timestamp_utc"] = pd.to_datetime(df["event_timestamp_utc"], utc=True)
    return df


def load_survey_clean_out() -> pd.DataFrame:
    """Load cleaned DS6 survey (outputs/cleaned/ds6_survey_clean.csv, 478 rows x 20 cols)."""
    return pd.read_csv(_SURV_CLEAN, low_memory=False)


def load_demographics_clean() -> pd.DataFrame:
    """Load cleaned DS6 demographics (399 rows x 6 cols, gender in English)."""
    return pd.read_csv(_DEMO_CLEAN, low_memory=False)


def load_participant_linkage() -> pd.DataFrame:
    """Load DS6 participant linkage table (399 participants, flags, event summaries, demographics)."""
    return pd.read_csv(_LINKAGE_CLEAN, low_memory=False)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _check_columns(df: pd.DataFrame, expected: list, name: str) -> None:
    """Warn if actual columns differ from expected columns."""
    actual  = df.columns.tolist()
    missing = [c for c in expected if c not in actual]
    extra   = [c for c in actual   if c not in expected]
    if missing:
        print(f"[load_dataset_6] WARNING -- {name}: expected columns not found: {missing}")
    if extra:
        print(f"[load_dataset_6] WARNING -- {name}: unexpected extra columns: {extra}")
