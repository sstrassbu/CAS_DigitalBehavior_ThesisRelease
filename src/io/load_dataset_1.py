"""
Loaders for Dataset 1 — Compact friction intervention testing.

All three CSV files are semicolon-delimited.
Raw files are never modified; this module reads them as-is.

Usage
-----
from src.io.load_dataset_1 import load_behavioral, load_pre_survey, load_post_survey, DS1_RAW

beh  = load_behavioral()
pre  = load_pre_survey()
post = load_post_survey()
"""

from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[2]

DS1_RAW = _REPO_ROOT / "data_raw" / "1. data set, compact friction intervention testing"

_BEH_CSV  = DS1_RAW / "Behavior data set" / "behavioral_data_set_1.csv"
_PRE_CSV  = DS1_RAW / "Survey data sets" / "Pre-survey" / "pre_survey_data_set_1.csv"
_POST_CSV = DS1_RAW / "Survey data sets" / "Post-survey" / "post_survey_data_set_1.csv"

# ---------------------------------------------------------------------------
# Expected columns (for validation on load)
# ---------------------------------------------------------------------------

_BEH_COLS  = ["participantUuid", "app", "timestamp", "purpose", "resolution",
               "secondsSinceOneSecSetup"]

_PRE_COLS  = ["participantUuid", "duration", "consent_general", "problems",
               "other_problems", "goals", "other_goals", "hours",
               "problematic_cons", "happy", "problematic_cons_general",
               "problematic_cons_compared"]

_POST_COLS = ["participantUuid", "duration", "consent_general", "problems_solved",
               "goals_reached", "hours", "problematic_cons", "happy",
               "progress_satisfaction", "problematic_cons_general",
               "problematic_cons_compared"]

# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def load_behavioral(validate: bool = True) -> pd.DataFrame:
    """
    Load the raw DS1 behavioral event file.

    Returns
    -------
    pd.DataFrame
        407,060 rows × 6 columns (raw, unmodified).
        Delimiter: semicolon. Timestamp: int64 Unix epoch.
        Resolution values: openedApp / dismissedAppOpening / closedApp / NaN.

    Notes
    -----
    - secondsSinceOneSecSetup has 18.9% NaN (codebook erroneously lists it as
      secondsSinceStudySetup — the CSV column name is correct).
    - purpose has 71.3% NaN — optional free-text field.
    - 8,302 fully duplicate rows exist in the raw file.
    - 1 row has NaN participantUuid.
    - App name 'whastapp' is a typo for 'whatsapp'.
    - See outputs/reports/ds1_audit_report.md for full audit findings.
    """
    df = pd.read_csv(_BEH_CSV, sep=";")
    if validate:
        _check_columns(df, _BEH_COLS, "behavioral")
    return df


def load_pre_survey(validate: bool = True) -> pd.DataFrame:
    """
    Load the raw DS1 pre-intervention survey file.

    Returns
    -------
    pd.DataFrame
        1,135 rows × 12 columns (raw, unmodified).
        Delimiter: semicolon.

    Notes
    -----
    - 26 participants have duplicate rows — deduplicate before analysis.
    - 26 rows have consent_general == 'I do NOT consent' — exclude before analysis.
    - Likert columns store values as composite strings ('N - label').
      Extract numeric prefix with regex r'^(\\d+)' before quantitative use.
    - problems and goals are comma-concatenated multi-select strings.
    - ~37% missingness on all substantive survey columns (non-consenting / abandoned).
    """
    df = pd.read_csv(_PRE_CSV, sep=";")
    if validate:
        _check_columns(df, _PRE_COLS, "pre_survey")
    return df


def load_post_survey(validate: bool = True) -> pd.DataFrame:
    """
    Load the raw DS1 post-intervention survey file.

    Returns
    -------
    pd.DataFrame
        255 rows × 11 columns (raw, unmodified).
        Delimiter: semicolon.

    Notes
    -----
    - 30 participants have duplicate rows — deduplicate before analysis.
    - 1 row has consent_general == 'I do NOT consent' — exclude before analysis.
    - consent_general is present in the CSV but not documented in the codebook;
      treat as equivalent to the pre-survey consent field.
    - Likert columns store values as composite strings ('N - label').
    - progress_satisfaction codebook description ('Outcome of intervention') is
      a copy-paste error — the column is a satisfaction scale.
    """
    df = pd.read_csv(_POST_CSV, sep=";")
    if validate:
        _check_columns(df, _POST_COLS, "post_survey")
    return df


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _check_columns(df: pd.DataFrame, expected: list, name: str) -> None:
    """Warn if actual columns differ from expected columns."""
    actual = df.columns.tolist()
    missing = [c for c in expected if c not in actual]
    extra   = [c for c in actual   if c not in expected]
    if missing:
        print(f"[load_dataset_1] WARNING — {name}: expected columns not found: {missing}")
    if extra:
        print(f"[load_dataset_1] WARNING — {name}: unexpected extra columns: {extra}")
