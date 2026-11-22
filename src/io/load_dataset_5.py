"""
Loaders for Dataset 5 — German adolescents, three-group RCT.

Delimiter note: ALL three CSV files are SEMICOLON-delimited.

Timestamp note: behavioral timestamps are LOCAL time strings (no UTC offset).
  They MUST be localized using the per-row 'timezone' column (IANA format) before
  converting to UTC. The cleaned output (ds5_behavioral_clean.csv) already has
  event_timestamp_utc — use that for analysis.

ID note: behavioral 'userid' has a study prefix that must be stripped to match
  survey 'uuid'. The canonical format is 'one-sec-next-gen-bzkj-2024-XXXXXXXX-...'.
  Stripping rule: remove 'study-one-sec-next-gen-bzkj-2024-' from userid.

Usage
-----
from src.io.load_dataset_5 import load_behavioral, load_pre_survey, load_post_survey

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

DS5_RAW = _REPO_ROOT / "data_raw" / "5. data set, German adolescents"

_BEH_CSV  = DS5_RAW / "Behavior data set" / "behavior_data_set_5.csv"
_PRE_CSV  = DS5_RAW / "Survey data sets" / "Pre-survey"  / "pre_survey_data_set_5.csv"
_POST_CSV = DS5_RAW / "Survey data sets" / "Post-survey" / "post_survey_data_set_5.csv"

DS5_CLEANED = _REPO_ROOT / "outputs" / "cleaned"

_BEH_CLEAN     = DS5_CLEANED / "ds5_behavioral_clean.csv"
_PRE_CLEAN     = DS5_CLEANED / "ds5_pre_survey_clean.csv"
_POST_CLEAN    = DS5_CLEANED / "ds5_post_survey_clean.csv"
_LINKAGE_CLEAN = DS5_CLEANED / "ds5_participant_linkage.csv"

# ---------------------------------------------------------------------------
# Expected columns (for validation on load)
# ---------------------------------------------------------------------------

_BEH_COLS = [
    "timestamp", "timezone", "interventionDuration",
    "timeIntervalUntilReIntervention", "app", "resolution", "userid",
    "reason", "suggestionBannerShown", "suggestionDetailViewAppear",
    "suggestionDetailViewDisappear", "terminationReason",
    "suggestionLearnMoreLinkTapped",
]

_PRE_COLS = [
    "uuid", "cond", "age", "digital_wellbeing", "time",
    "prob_peers", "time_peers", "prob_self", "social_media_wellbeing",
    "prob", "prob_other", "goal", "goal_other", "social_media_updated",
    "belong_1", "belong_2", "belong_3", "belong_4",
    "belong_5", "belong_6", "belong_7", "belong_8",
    "ostracism_1", "ostracism_2", "ostracism_3", "ostracism_4", "ostracism_5",
    "fomo_1", "fomo_2", "fomo_3", "fomo_4", "fomo_5",
    "fomo_6", "fomo_7", "fomo_8", "fomo_9", "fomo_10",
]

_POST_COLS = [
    "uuid", "digital_wellbeing", "time", "prob_peers", "time_peers",
    "prob_self", "social_media_wellbeing", "solve_prob", "address_goal",
    "social_media_updated",
    "belong_1", "belong_2", "belong_3", "belong_4",
    "belong_5", "belong_6", "belong_7", "belong_8",
    "ostracism_1", "ostracism_2", "ostracism_3", "ostracism_4", "ostracism_5",
    "fomo_1", "fomo_2", "fomo_3", "fomo_4", "fomo_5",
    "fomo_6", "fomo_7", "fomo_8", "fomo_9", "fomo_10",
]

# ---------------------------------------------------------------------------
# Raw loaders
# ---------------------------------------------------------------------------


def load_behavioral(validate: bool = True) -> pd.DataFrame:
    """
    Load the raw DS5 behavioral event file.

    Returns
    -------
    pd.DataFrame
        288,688 rows x 13 columns (raw, unmodified).
        Delimiter: SEMICOLON.
        Timestamp: local datetime string (no UTC offset).
          Localize using per-row 'timezone' column (IANA tz string).
          Fallback timezone: Europe/Berlin for NaN timezone rows.

    Notes
    -----
    - Resolution: openedApp (61.6%), dismissedAppOpening (21.5%),
      closedApp (15.6%), NaN (1.2%), dismissedByStructuredIntervention (0.04%).
    - userid prefix: 'study-one-sec-next-gen-bzkj-2024-' must be stripped
      to match survey uuid format. Result = participant_id_canonical.
    - interventionDuration = 0.0 for ALL openedApp events. Non-zero only
      when friction was shown (dismissed or structured intervention).
    - timeIntervalUntilReIntervention: 77.9% NaN -- only populated for
      the reintervention condition.
    - reason: 42.3% NaN -- German free-text; not yet categorized.
    - suggestion columns (suggestionBannerShown etc.): 99%+ NaN -- only
      populated for the small suggestion-exposure sub-group.
    - cond NOT in behavioral file -- must join from pre-survey via canonical ID.
    - 573 unique participants in behavioral file.
    - 3,457 rows have NaN timezone, app, and resolution (co-missing).
    - See outputs/reports/ds5_audit_report.md for full audit findings.
    """
    df = pd.read_csv(_BEH_CSV, sep=";", low_memory=False)
    if validate:
        _check_columns(df, _BEH_COLS, "behavioral")
    return df


def load_pre_survey(validate: bool = True) -> pd.DataFrame:
    """
    Load the raw DS5 pre-intervention survey.

    Returns
    -------
    pd.DataFrame
        792 rows x 37 columns (raw, unmodified).
        Delimiter: SEMICOLON.

    Notes
    -----
    - Contains condition assignment (cond): control=265, default=264,
      reintervention=263.
    - uuid matches behavioral participant_id_canonical after prefix strip.
    - Scale items are stored as numeric Likert values (may need coerce on load).
    - Scale structure:
        belong_1 to belong_8    (8 items, sense of belonging)
        ostracism_1 to ostracism_5  (5 items, ostracism)
        fomo_1 to fomo_10       (10 items, fear of missing out)
    - prob_other and goal_other: 94-98% NaN -- open text, not usable.
    - Age range: 13-25 (modal 18-20; includes young adults despite label).
    - 0 duplicate UUIDs.
    - See outputs/reports/ds5_audit_report.md for full audit findings.
    """
    df = pd.read_csv(_PRE_CSV, sep=";", low_memory=False)
    if validate:
        _check_columns(df, _PRE_COLS, "pre_survey")
    return df


def load_post_survey(validate: bool = True) -> pd.DataFrame:
    """
    Load the raw DS5 post-intervention survey.

    Returns
    -------
    pd.DataFrame
        314 rows x 33 columns (raw, including 3 duplicate UUIDs).
        Delimiter: SEMICOLON.

    Notes
    -----
    - 311 unique UUIDs; 3 participants appear twice. For analysis, use
      the cleaned version (ds5_post_survey_clean.csv, first occurrence kept).
    - No condition column -- join from pre-survey via uuid.
    - Additional outcome columns: solve_prob, address_goal.
    - Same scale structure as pre-survey (belong, ostracism, fomo).
    - See outputs/reports/ds5_audit_report.md for full audit findings.
    """
    df = pd.read_csv(_POST_CSV, sep=";", low_memory=False)
    if validate:
        _check_columns(df, _POST_COLS, "post_survey")
    return df


# ---------------------------------------------------------------------------
# Cleaned loaders
# ---------------------------------------------------------------------------


def load_behavioral_clean(parse_timestamps: bool = True) -> pd.DataFrame:
    """
    Load the cleaned DS5 behavioral file (outputs/cleaned/ds5_behavioral_clean.csv).

    Returns
    -------
    pd.DataFrame
        288,688 rows x 19 columns.
        event_timestamp_utc is UTC-aware if parse_timestamps=True.
        Includes participant_id_canonical, event_outcome_simple,
        intervention fields, days_since_first_event, and reason.
        Does NOT include study_condition -- join from pre-survey.

    Example
    -------
    beh = load_behavioral_clean()
    pre = load_pre_survey_clean()
    cond_map = pre.set_index("participant_id_canonical")["cond"]
    beh["study_condition"] = beh["participant_id_canonical"].map(cond_map)
    """
    df = pd.read_csv(_BEH_CLEAN, low_memory=False)
    if parse_timestamps:
        df["event_timestamp_utc"] = pd.to_datetime(df["event_timestamp_utc"], utc=True)
    return df


def load_pre_survey_clean() -> pd.DataFrame:
    """Load cleaned DS5 pre-survey (792 rows x 42 cols, includes scale means)."""
    return pd.read_csv(_PRE_CLEAN, low_memory=False)


def load_post_survey_clean() -> pd.DataFrame:
    """Load cleaned DS5 post-survey (311 rows x 38 cols, duplicates removed, includes scale means)."""
    return pd.read_csv(_POST_CLEAN, low_memory=False)


def load_participant_linkage() -> pd.DataFrame:
    """Load DS5 participant linkage table (793 participants, with flags and event summaries)."""
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
        print(f"[load_dataset_5] WARNING -- {name}: expected columns not found: {missing}")
    if extra:
        print(f"[load_dataset_5] WARNING -- {name}: unexpected extra columns: {extra}")
