"""
Loaders for Dataset 4 — Large non-experimental data (historic, retrospective).

Delimiter note: behavioral CSV is COMMA-delimited; survey CSV is SEMICOLON-delimited.
This differs from DS1 (all semicolons) and is confirmed in the audit.

Usage
-----
from src.io.load_dataset_4 import load_behavioral, load_survey, DS4_RAW

beh    = load_behavioral()
survey = load_survey()
"""

from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_REPO_ROOT = Path(__file__).resolve().parents[2]

DS4_RAW = _REPO_ROOT / "data_raw" / "4. data set, large non-experimental data"

_BEH_CSV    = DS4_RAW / "Behavior data set" / "behavior_data_set_4.csv"
_SURVEY_CSV = DS4_RAW / "Survey data set"   / "post_survey_data_set_4.csv"
_SURVEY_XLS = DS4_RAW / "Survey data set"   / "post_survey_data_set_4.xlsx"

# ---------------------------------------------------------------------------
# Expected columns (for validation on load)
# ---------------------------------------------------------------------------

_BEH_COLS = [
    "app", "resolution", "timestamp", "interventionDuration",
    "interventionType", "purpose", "participantUuid",
    "secondsSinceStudySetup", "weeksSinceStudySetup", "userIndex",
]

_SURVEY_COLS = [
    "uuid", "age", "gender", "gender_additional",
    "reason_use", "benefits", "negatives",
    "usage_format", "add_features", "comments",
]

# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------


def load_behavioral(validate: bool = True) -> pd.DataFrame:
    """
    Load the raw DS4 behavioral event file.

    Returns
    -------
    pd.DataFrame
        2,490,260 rows × 10 columns (raw, unmodified).
        Delimiter: COMMA — different from DS1 (semicolon).
        Timestamp: ISO 8601 UTC string, e.g. '2022-09-29T15:48:54Z'.
        Parse timestamps with pd.to_datetime(df['timestamp'], utc=True).

    Notes
    -----
    - Resolution: 5 values confirmed — closedApp (47.1%), openedApp (35.4%),
      dismissedAppOpening (17.5%), plus 2 undocumented types (812 rows total).
      Do NOT apply outcome_map from DS1 without confirming the 2 undocumented values.
    - interventionDuration and interventionType: 63.5% NaN — ALWAYS co-missing.
      All 1,171,929 closedApp events have NaN intervention fields.
      These rows may represent a structurally different event type, not failed logging.
    - secondsSinceStudySetup / weeksSinceStudySetup: ALL values are ≤ 0.
      Codebook description ("time since setup, positive") is incorrect.
      These count backward from a per-participant anchor ~8.8h after last event.
      Use timestamp directly to derive forward-counting time variables.
    - purpose: 83.1% NaN — open-text field; not viable for systematic use.
    - whastapp typo: 39,045 events for 'whastapp' (should be 'whatsapp').
    - No NaN in: app, resolution, timestamp, participantUuid, userIndex.
    - No fully duplicate rows.
    - See outputs/reports/ds4_audit_report.md for full audit findings.
    """
    df = pd.read_csv(_BEH_CSV, sep=",", low_memory=False)
    if validate:
        _check_columns(df, _BEH_COLS, "behavioral")
    return df


def load_survey(validate: bool = True, source: str = "csv") -> pd.DataFrame:
    """
    Load the raw DS4 post-use retrospective survey file.

    Parameters
    ----------
    source : {'csv', 'xlsx'}
        'csv'  — use the CSV file (semicolon-delimited; has trailing whitespace).
        'xlsx' — use the XLSX file (pre-trimmed; functionally equivalent after strip).

    Returns
    -------
    pd.DataFrame
        304 rows × 10 columns (raw, unmodified; 299 unique uuid after dedup).
        Delimiter: SEMICOLON (CSV) — different from the behavioral file.

    Notes
    -----
    - Survey uuid has prefix 'donatus-master-thesis-one-sec-early-2023-'.
      Strip prefix before matching to behavioral participantUuid.
      After prefix strip + uppercase: 283 of 299 survey participants match behavioral.
    - 5 duplicate uuid rows exist — keep first occurrence during cleaning.
    - gender is stored as text strings ('Male', 'Female', etc.),
      NOT numeric codes as the codebook claims.
    - All substantive columns are open-text / qualitative — no psychometric scales.
    - age: 20.4% NaN; range 13–54; mean 26.4.
    - See outputs/reports/ds4_audit_report.md for full audit findings.
    """
    if source == "xlsx":
        df = pd.read_excel(_SURVEY_XLS)
    else:
        df = pd.read_csv(_SURVEY_CSV, sep=";")
    if validate:
        _check_columns(df, _SURVEY_COLS, "survey")
    return df


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _check_columns(df: pd.DataFrame, expected: list, name: str) -> None:
    """Warn if actual columns differ from expected columns."""
    actual  = df.columns.tolist()
    missing = [c for c in expected if c not in actual]
    extra   = [c for c in actual   if c not in expected]
    if missing:
        print(f"[load_dataset_4] WARNING — {name}: expected columns not found: {missing}")
    if extra:
        print(f"[load_dataset_4] WARNING — {name}: unexpected extra columns: {extra}")
