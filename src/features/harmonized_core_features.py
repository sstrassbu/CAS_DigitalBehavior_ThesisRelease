"""
Stage 2 — Light cross-dataset harmonized core feature builder.

Produces a single participant-level table with one row per participant per dataset,
containing only features that are reasonably comparable across DS1, DS4, DS5, and DS6.

Design principles
-----------------
- DS6 outcome rates are NOT harmonizable with DS1/DS4/DS5. All DS6 events are 'opened'.
  Use event_rate_ratio_intervention_vs_baseline as the behavioral response proxy for DS6,
  filtered to n_baseline_days >= 7 (see data_docs/modeling_cautions.md Section 2).
- Friction override rate is assembled from different source columns per dataset.
  The source is documented via the friction_override_source column. Do not pool
  raw values across datasets without reading that column.
- Adaptation trajectory uses different time axes per dataset. Documented via
  open_rate_change_axis. Sign/direction interpretable; magnitude not directly comparable.
- Time-of-day features are NOT cross-dataset comparable — see the clock note below.
  Documented via the temporal_clock column.
- App-structure features are comparable WITHIN a dataset only — see the app-vocabulary
  note below.
- Psychosocial scales are NOT harmonized. Instruments differ strongly across datasets.
  Only availability flags (has_survey, has_prepost_survey) are included.
- Dataset-specific features (DS4 event classes, DS6 session/sequence features,
  override streaks, all scale scores) remain in Stage 1 files only.

Friction denominator (F001 / F213, 2026-08-08)
----------------------------------------------
The Stage 1 friction rates this module reads are now computed on FRICTION-DECISION
rows only ('opened' / 'dismissed'). 'closed' is an app-close record, not a friction
decision, and used to sit in the denominator of DS1's rate_opened for the 126 DS1
participants whose logs contain closes. friction_override_rate therefore CHANGED for
126 DS1 rows (their mean 0.3552 -> 0.6978; DS1 cohort mean 0.5427 -> 0.6125) and for
87 DS5 rows (their mean 0.3875 -> 0.7230), where closes and 'dismissed_other' (F200)
both left the denominator. The friction_override_source strings were relabelled from
'rate_opened__all_events__ds{1,5}' to 'rate_opened__friction_decisions_only__ds{1,5}',
because the old labels are now factually wrong. DS4 is unaffected: its source column
(rate_opened_intervention_events) always used an opened/dismissed denominator.

Clock heterogeneity in the time-of-day block (F029 / F047 / F208)
-----------------------------------------------------------------
peak_hour_of_day, evening_event_share and morning_event_share are LOCAL-clock
constructs, and the four datasets do not share a clock:

    DS5  local wall clock (event_timestamp_local)
    DS6  local wall clock (Europe/Copenhagen)
    DS1  UTC — no local clock exists in the source data
    DS4  UTC — multi-timezone cohort with no timezone column

These three columns are therefore NOT comparable across datasets and must not be
pooled: a DS1 "evening" share is an evening share in UTC, a DS5 one is an evening
share in Berlin. Each row carries the declaration in temporal_clock; filter on it
before any cross-dataset time-of-day statement. Within a dataset they remain valid.
weekend_event_share is mildly clock-dependent (only events near local midnight on a
Friday/Sunday boundary can move) and carries the same caveat in weaker form.
hour_entropy is very nearly clock-invariant — a CONSTANT whole-hour offset is a
permutation of the hour histogram — but it is not exactly so: it is now scored on
each dataset's declared clock, and 110 of 573 DS5 participants changed value because
DS5 spans DST shifts and 39 distinct event timezones. Treat it as comparable across
datasets with that small caveat, not as exempt.

App-vocabulary heterogeneity (F202)
-----------------------------------
n_unique_apps, top_app_share, app_herfindahl and app_entropy are bounded by the set
of apps each study could observe, which is partly a study-configuration decision and
not participant behavior (global unique app counts: DS6 10, DS1 48, DS5 71, DS4 399).
As shipped, the 10-app dataset has the HIGHEST mean app_entropy. Cross-dataset
differences in these four columns are confounded and uninterpretable as shipped;
normalize (e.g. app_entropy / log2(n_unique_apps)) before comparing across datasets.

Usage
-----
From the project root:

    python -m src.features.harmonized_core_features

Or in a notebook/script:

    from src.features.harmonized_core_features import build_harmonized_core
    df = build_harmonized_core()

Output saved to: outputs/harmonized/stage2/harmonized_core_features.csv

See also
--------
- outputs/harmonized/stage2/harmonized_core_schema.md — full feature documentation
- outputs/harmonized/stage2/feature_mapping_table.csv — per-feature source mapping
- outputs/harmonized/stage2/cross_dataset_comparability_notes.md — caveats for users
- data_docs/modeling_cautions.md — QC-derived filtering requirements
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_FEAT = Path("outputs/features")
_OUT = Path("outputs/harmonized/stage2")

# ---------------------------------------------------------------------------
# Column order for the final table
# ---------------------------------------------------------------------------

HARMONIZED_COLUMNS = [
    # --- Identifiers and design metadata ---
    "dataset_id",
    "participant_id_canonical",
    "study_design_type",
    "study_condition",
    # --- Volume (Group A) ---
    "total_events",
    "n_days_observed",
    "obs_window_days",
    "events_per_day",
    # --- App structure (Group A — comparable WITHIN a dataset only, F202) ---
    # Bounded by each study's configured app vocabulary (DS6 10 apps vs DS4 399).
    "n_unique_apps",
    "top_app_share",
    "app_herfindahl",
    "app_entropy",
    # --- Temporal structure (Group A) ---
    # F029/F047/F208: peak_hour_of_day / evening_event_share / morning_event_share are
    # clock-dependent and NOT cross-dataset comparable (DS5/DS6 local, DS1/DS4 UTC).
    # Read temporal_clock before pooling. weekend_event_share is mildly clock-dependent;
    # hour_entropy is near-invariant but not exactly (DS5 DST/multi-timezone).
    "peak_hour_of_day",
    "weekend_event_share",
    "evening_event_share",
    "morning_event_share",
    "hour_entropy",
    "temporal_clock",
    # --- Friction response (Group B) ---
    "friction_override_rate",
    "friction_override_source",
    # --- DS6 behavioral response proxy (Group B, DS6 only) ---
    "behavioral_response_ratio",
    "behavioral_response_proxy_type",
    # --- Adaptation trajectory (Group B) ---
    "open_rate_change",
    "open_rate_change_axis",
    # --- Availability flags ---
    "has_survey",
    "has_prepost_survey",
    "has_study_condition",
    "has_friction_outcome",
    "has_behavioral_response_ratio",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _temporal_clock(beh: pd.DataFrame, dataset_id: str) -> pd.Series:
    """
    Return the Stage 1 `temporal_clock` provenance column for one dataset.

    F029/F047/F208: temporal_features() stamps every Stage 1 behavior table with the
    clock its hour-axis features were scored on. That stamp is carried into the
    harmonized table so a user can filter before pooling time-of-day columns. It is a
    hard requirement rather than a silent default: an unlabelled hour axis is exactly
    the failure this column exists to prevent.
    """
    if "temporal_clock" not in beh.columns:
        raise KeyError(
            f"{dataset_id} behavior features are missing the 'temporal_clock' column. "
            "Regenerate the Stage 1 feature table first (it is added by "
            "src/features/behavioral_features.py::temporal_features)."
        )
    return beh["temporal_clock"]


# ---------------------------------------------------------------------------
# Dataset loaders
# ---------------------------------------------------------------------------


def _load_ds1() -> pd.DataFrame:
    """
    Load DS1 and return one harmonized row per participant.

    Friction override source: rate_opened over FRICTION-DECISION rows only
    ('opened' / 'dismissed'). F001/F213: 'closed' is an app-close record emitted after
    an open (median ~100 s later) and is logged for only 126 of 619 participants; it
    used to inflate the denominator, which depressed friction_override_rate for exactly
    those 126 participants and nobody else. Values changed with that fix.

    Clock: UTC (F047) — DS1 has no local clock, so peak_hour_of_day /
    evening_event_share / morning_event_share are UTC-scored and not comparable to
    DS5/DS6 (which are local). Recorded in temporal_clock.

    Adaptation axis: setup-time (secondsSinceOneSecSetup tertiles).
    Time axis differs from DS4/DS5 calendar days — comparable in sign, not magnitude.
    """
    beh = pd.read_csv(_FEAT / "ds1/ds1_behavior_features.csv")
    survey_ids = set(
        pd.read_csv(_FEAT / "ds1/ds1_survey_features.csv")["participant_id_canonical"]
    )
    prepost_ids = set(
        pd.read_csv(_FEAT / "ds1/ds1_prepost_features.csv")["participant_id_canonical"]
    )
    pid = beh["participant_id_canonical"]

    df = pd.DataFrame(
        {
            # Identifiers
            "dataset_id": "DS1",
            "participant_id_canonical": pid,
            "study_design_type": "non_experimental",
            "study_condition": np.nan,
            # Volume (Group A)
            "total_events": beh["total_events"],
            "n_days_observed": beh["n_days_observed"],
            "obs_window_days": beh["obs_window_days"],
            "events_per_day": beh["events_per_day"],
            # App structure (Group A)
            "n_unique_apps": beh["n_unique_apps"],
            "top_app_share": beh["top_app_share"],
            "app_herfindahl": beh["app_herfindahl"],
            "app_entropy": beh["app_entropy"],
            # Temporal (Group A)
            "peak_hour_of_day": beh["peak_hour_of_day"],
            "weekend_event_share": beh["weekend_event_share"],
            "evening_event_share": beh["evening_event_share"],
            "morning_event_share": beh["morning_event_share"],
            "hour_entropy": beh["hour_entropy"],
            "temporal_clock": _temporal_clock(beh, "DS1"),
            # Friction override (Group B)
            # F001/F213: source is rate_opened over friction-decision rows only
            # (opened + dismissed). The old label said 'all_events', which is no longer
            # true — closes are excluded from the denominator.
            "friction_override_rate": beh["rate_opened"],
            "friction_override_source": "rate_opened__friction_decisions_only__ds1",
            # DS6 behavioral response (Group B) — not applicable for DS1
            "behavioral_response_ratio": np.nan,
            "behavioral_response_proxy_type": np.nan,
            # Adaptation (Group B)
            # Axis: secondsSinceOneSecSetup tertiles. NaN when the participant has < 10
            # events with a setup time, and (F120/F129) also when either third holds
            # fewer than 5 rows — the latter gate is new, so NaN coverage increased.
            # Different axis from DS4/DS5 calendar days — do not compare magnitudes.
            "open_rate_change": beh["open_rate_change_setup"],
            "open_rate_change_axis": "setup_time_ds1",
            # Availability flags
            "has_survey": pid.isin(survey_ids),
            "has_prepost_survey": pid.isin(prepost_ids),
            "has_study_condition": False,
            "has_friction_outcome": beh["rate_opened"].notna(),
            "has_behavioral_response_ratio": False,
        }
    )
    return df[HARMONIZED_COLUMNS]


def _load_ds4() -> pd.DataFrame:
    """
    Load DS4 and return one harmonized row per participant.

    Friction override source: rate_opened_intervention_events.
    DS4 has three event classes. Only intervention_event class (36.5%) has friction shown.
    This is the cleanest per-event friction signal. Unaffected by the F001/F213
    friction-denominator fix: ds4_outcome_by_class() already used an opened/dismissed
    denominator within the intervention_event class. The denominator is still not the
    same object as DS1's/DS5's (event-class restricted), so do not pool raw values.

    Clock: UTC (F047) — DS4 is a multi-timezone cohort with no timezone column, so the
    hour-axis features are UTC-scored and not comparable to DS5/DS6 (local), nor
    strictly comparable across DS4 participants. Recorded in temporal_clock.

    Adaptation axis: calendar days (days_since_first_event tertiles). Same axis as DS5.
    DS4 has the longest windows (up to 897 days) — most reliable adaptation signal.
    """
    beh = pd.read_csv(_FEAT / "ds4/ds4_behavior_features.csv")
    survey_ids = set(
        pd.read_csv(_FEAT / "ds4/ds4_survey_features.csv")["participant_id_canonical"]
    )
    # DS4 has no pre-post survey
    pid = beh["participant_id_canonical"]

    df = pd.DataFrame(
        {
            # Identifiers
            "dataset_id": "DS4",
            "participant_id_canonical": pid,
            "study_design_type": "non_experimental",
            "study_condition": np.nan,
            # Volume (Group A)
            "total_events": beh["total_events"],
            "n_days_observed": beh["n_days_observed"],
            "obs_window_days": beh["obs_window_days"],
            "events_per_day": beh["events_per_day"],
            # App structure (Group A)
            "n_unique_apps": beh["n_unique_apps"],
            "top_app_share": beh["top_app_share"],
            "app_herfindahl": beh["app_herfindahl"],
            "app_entropy": beh["app_entropy"],
            # Temporal (Group A)
            "peak_hour_of_day": beh["peak_hour_of_day"],
            "weekend_event_share": beh["weekend_event_share"],
            "evening_event_share": beh["evening_event_share"],
            "morning_event_share": beh["morning_event_share"],
            "hour_entropy": beh["hour_entropy"],
            "temporal_clock": _temporal_clock(beh, "DS4"),
            # Friction override (Group B)
            # Source: intervention_event class only (opened / dismissed denominator).
            # 3.0% NaN (participants with < 5 intervention events).
            # Denominator DIFFERS from DS1/DS5 — document carefully.
            "friction_override_rate": beh["rate_opened_intervention_events"],
            "friction_override_source": "rate_opened__intervention_events_only__ds4",
            # DS6 behavioral response (Group B) — not applicable for DS4
            "behavioral_response_ratio": np.nan,
            "behavioral_response_proxy_type": np.nan,
            # Adaptation (Group B)
            # Axis: calendar days tertiles. Same axis as DS5. NaN when < 10 eligible
            # rows and (F120/F129) when either third holds < 5 rows — NaN coverage
            # increased relative to the previously documented 4.7%.
            "open_rate_change": beh["open_rate_change_calendar"],
            "open_rate_change_axis": "calendar_days",
            # Availability flags
            "has_survey": pid.isin(survey_ids),
            "has_prepost_survey": False,
            "has_study_condition": False,
            "has_friction_outcome": beh["rate_opened_intervention_events"].notna(),
            "has_behavioral_response_ratio": False,
        }
    )
    return df[HARMONIZED_COLUMNS]


def _load_ds5() -> pd.DataFrame:
    """
    Load DS5 and return one harmonized row per participant.

    Friction override source: rate_opened over FRICTION-DECISION rows only
    ('opened' / 'dismissed'). F001/F213/F200: closes and 'dismissed_other' left the
    denominator, so values changed for 87 of 573 participants (their mean 0.3875 ->
    0.7230; DS5 cohort mean 0.6311 -> 0.6824).

    Note: DS5 control condition has no friction exposure — their rate_opened reflects
    friction-free app opens. Compare friction_override_rate across DS5 conditions
    rather than pooling with DS1/DS4 directly. F121: has_friction_outcome is False for
    control for that reason, so the documented `core[core["has_friction_outcome"]]`
    recipe now actually returns friction-exposed participants only.

    Clock: LOCAL (F029) — DS5's Stage 1 hour-axis features are scored on
    event_timestamp_local (German cohort), so they are NOT comparable to DS1/DS4,
    which are UTC. Recorded in temporal_clock.

    Adaptation axis: calendar days (days_since_first_event tertiles). Same as DS4.
    Shorter windows than DS4 — adaptation signal less reliable, especially for control.
    """
    beh = pd.read_csv(_FEAT / "ds5/ds5_behavior_features.csv")
    survey_ids = set(
        pd.read_csv(_FEAT / "ds5/ds5_survey_features.csv")["participant_id_canonical"]
    )
    prepost_ids = set(
        pd.read_csv(_FEAT / "ds5/ds5_prepost_features.csv")["participant_id_canonical"]
    )
    pid = beh["participant_id_canonical"]
    cond = beh["study_condition"]

    df = pd.DataFrame(
        {
            # Identifiers
            "dataset_id": "DS5",
            "participant_id_canonical": pid,
            "study_design_type": "experimental_rct",
            "study_condition": cond,
            # Volume (Group A)
            "total_events": beh["total_events"],
            "n_days_observed": beh["n_days_observed"],
            "obs_window_days": beh["obs_window_days"],
            "events_per_day": beh["events_per_day"],
            # App structure (Group A)
            "n_unique_apps": beh["n_unique_apps"],
            "top_app_share": beh["top_app_share"],
            "app_herfindahl": beh["app_herfindahl"],
            "app_entropy": beh["app_entropy"],
            # Temporal (Group A)
            "peak_hour_of_day": beh["peak_hour_of_day"],
            "weekend_event_share": beh["weekend_event_share"],
            "evening_event_share": beh["evening_event_share"],
            "morning_event_share": beh["morning_event_share"],
            "hour_entropy": beh["hour_entropy"],
            "temporal_clock": _temporal_clock(beh, "DS5"),
            # Friction override (Group B)
            # F001/F213: source is rate_opened over friction-decision rows only
            # (same denominator logic as DS1, and the same relabelling reason).
            # CAVEAT: DS5 control condition has no friction — their rate_opened is
            # friction-free opens. Only default/reintervention conditions are
            # comparable to DS1/DS4 friction_override_rate.
            "friction_override_rate": beh["rate_opened"],
            "friction_override_source": "rate_opened__friction_decisions_only__ds5",
            # DS6 behavioral response (Group B) — not applicable for DS5
            "behavioral_response_ratio": np.nan,
            "behavioral_response_proxy_type": np.nan,
            # Adaptation (Group B)
            # Axis: calendar days tertiles. Same axis as DS4. NaN when < 10 eligible
            # rows and (F120/F129) when either third holds < 5 rows — NaN coverage
            # increased relative to the previously documented 16.6%.
            "open_rate_change": beh["open_rate_change_calendar"],
            "open_rate_change_axis": "calendar_days",
            # Availability flags
            "has_survey": pid.isin(survey_ids),
            "has_prepost_survey": pid.isin(prepost_ids),
            "has_study_condition": cond.notna(),
            # F121: DS5 control has NO friction exposure (is_intervention_event mean =
            # 0.000), so its rate_opened is a friction-free app-open rate, not an
            # override rate. A pure not-null test flagged all 184 controls as
            # friction-exposed, contradicting the documented load recipe; the flag now
            # selects 385 DS5 rows instead of 569.
            "has_friction_outcome": beh["rate_opened"].notna() & (cond != "control"),
            "has_behavioral_response_ratio": False,
        }
    )
    return df[HARMONIZED_COLUMNS]


def _load_ds6() -> pd.DataFrame:
    """
    Load DS6 and return one harmonized row per participant.

    CRITICAL: DS6 has ONLY 'opened' outcomes in the behavioral log.
    friction_override_rate is NaN for ALL DS6 rows — this is structural, not missing data.
    Do not impute. (Unaffected by the F001/F213 friction-denominator fix: with a single
    outcome label there is no denominator question to get wrong.)

    Clock: LOCAL (F029) — DS6's Stage 1 hour-axis features are scored on
    Europe/Copenhagen local time, so they are NOT comparable to DS1/DS4, which are UTC.
    Recorded in temporal_clock.

    Behavioral response proxy:
    event_rate_ratio_intervention_vs_baseline captures behavioral response for DS6.
    Filter applied: n_baseline_days >= 7 (participants with shorter baselines produce
    ratios up to 77x — see modeling_cautions.md Section 2). 7 participants fall below
    the threshold (baseline days 1, 1, 2, 2, 3, 5, 5); 6 of them had a computable
    ratio, leaving 235 usable DS6 rows. Note 4 of the 7 have unremarkable ratios
    (0.5626, 0.6473, 1.3366, 1.8750) and are dropped purely on baseline length.

    Adaptation trajectory: DS6 has no equivalent of the tertile-based open_rate_change
    used in DS1/DS4/DS5 (different study structure; only 'opened' outcomes).
    open_rate_change is NaN for all DS6 rows.
    """
    beh = pd.read_csv(_FEAT / "ds6/ds6_behavior_features.csv")
    survey_ids = set(
        pd.read_csv(_FEAT / "ds6/ds6_survey_features.csv")["participant_id_canonical"]
    )
    prepost_ids = set(
        pd.read_csv(_FEAT / "ds6/ds6_prepost_features.csv")["participant_id_canonical"]
    )
    pid = beh["participant_id_canonical"]

    # Apply n_baseline_days >= 7 filter.
    # Participants with < 7 baseline days yield unreliable event rate baselines.
    # Their ratio values are set to NaN and has_behavioral_response_ratio = False.
    valid_baseline_mask = beh["n_baseline_days"] >= 7
    behavioral_response_ratio = beh["event_rate_ratio_intervention_vs_baseline"].where(
        valid_baseline_mask
    )
    has_behavioral_response = behavioral_response_ratio.notna()
    proxy_type = has_behavioral_response.map(
        {True: "event_rate_ratio_intervention_vs_baseline", False: None}
    )

    df = pd.DataFrame(
        {
            # Identifiers
            "dataset_id": "DS6",
            "participant_id_canonical": pid,
            "study_design_type": "experimental_quasi",
            "study_condition": beh["study_condition"],
            # Volume (Group A)
            "total_events": beh["total_events"],
            "n_days_observed": beh["n_days_observed"],
            "obs_window_days": beh["obs_window_days"],
            "events_per_day": beh["events_per_day"],
            # App structure (Group A)
            "n_unique_apps": beh["n_unique_apps"],
            "top_app_share": beh["top_app_share"],
            "app_herfindahl": beh["app_herfindahl"],
            "app_entropy": beh["app_entropy"],
            # Temporal (Group A)
            "peak_hour_of_day": beh["peak_hour_of_day"],
            "weekend_event_share": beh["weekend_event_share"],
            "evening_event_share": beh["evening_event_share"],
            "morning_event_share": beh["morning_event_share"],
            "hour_entropy": beh["hour_entropy"],
            "temporal_clock": _temporal_clock(beh, "DS6"),
            # Friction override (Group B)
            # NaN for all DS6 rows — structural incompatibility, not missing data.
            # DS6 has no dismiss or close outcomes; opened rate = 1.0 for all participants.
            "friction_override_rate": np.nan,
            "friction_override_source": "not_applicable__ds6_all_outcomes_opened",
            # DS6 behavioral response (Group B) — primary behavioral outcome for DS6
            "behavioral_response_ratio": behavioral_response_ratio,
            "behavioral_response_proxy_type": proxy_type,
            # Adaptation (Group B) — no equivalent for DS6
            "open_rate_change": np.nan,
            "open_rate_change_axis": "not_available_ds6",
            # Availability flags
            "has_survey": pid.isin(survey_ids),
            "has_prepost_survey": pid.isin(prepost_ids),
            "has_study_condition": beh["study_condition"].notna(),
            "has_friction_outcome": False,
            "has_behavioral_response_ratio": has_behavioral_response,
        }
    )
    return df[HARMONIZED_COLUMNS]


# ---------------------------------------------------------------------------
# Main builder
# ---------------------------------------------------------------------------


def build_harmonized_core() -> pd.DataFrame:
    """
    Build the Stage 2 harmonized core participant-level feature table.

    Returns
    -------
    pd.DataFrame
        One row per participant per dataset. 2,474 rows total (619 + 1039 + 573 + 243).
        29 columns as defined in HARMONIZED_COLUMNS.

    Notes
    -----
    - Group A features (14 columns incl. the temporal_clock provenance stamp):
      directly comparable across all four datasets EXCEPT (a) the three clock-dependent
      time-of-day columns, which are UTC for DS1/DS4 and local for DS5/DS6 (F029/F047),
      and (b) the four app-structure columns, which are bounded by each study's app
      vocabulary (F202). Both exceptions are described in the module docstring.
    - Group B features (6 columns, 4 logical features): comparable with documented caveats.
    - friction_override_rate now uses a friction-decision denominator for DS1/DS5
      (F001/F213); DS4's source column was already on that basis.
    - DS6 friction_override_rate is structurally NaN — do not impute.
    - DS6 behavioral_response_ratio requires n_baseline_days >= 7 (already applied here).
    - All dataset-specific features remain in outputs/features/ds{1,4,5,6}/ — those
      are the primary layer for individual dataset modeling.
    """
    ds1 = _load_ds1()
    ds4 = _load_ds4()
    ds5 = _load_ds5()
    ds6 = _load_ds6()

    core = pd.concat([ds1, ds4, ds5, ds6], ignore_index=True)

    # Confirm column order
    assert list(core.columns) == HARMONIZED_COLUMNS, "Column order mismatch"

    return core


# ---------------------------------------------------------------------------
# Entry point — generates all outputs when run as a script
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    _OUT.mkdir(parents=True, exist_ok=True)

    core = build_harmonized_core()

    out_path = _OUT / "harmonized_core_features.csv"
    core.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")
    print(f"Shape: {core.shape}")

    print("\nRows per dataset:")
    print(core["dataset_id"].value_counts().sort_index().to_string())

    print("\nColumn non-NaN coverage (%):")
    cov = (core.notna().mean() * 100).round(1)
    for col, pct in cov.items():
        print(f"  {col:<40} {pct:.1f}%")

    print("\nfriction_override_source distribution:")
    print(core["friction_override_source"].value_counts().to_string())

    # F029/F047: make the clock split visible at build time — the three time-of-day
    # columns cannot be pooled across the groups printed here.
    print("\ntemporal_clock distribution (do NOT pool time-of-day across these):")
    print(
        core.groupby("dataset_id")["temporal_clock"]
        .agg(lambda s: s.dropna().unique().tolist())
        .to_string()
    )

    print("\nhas_friction_outcome by dataset (DS5 control excluded by design, F121):")
    print(core.groupby("dataset_id")["has_friction_outcome"].sum().to_string())

    print("\nbehavioral_response_ratio available (DS6):")
    ds6_rows = core[core["dataset_id"] == "DS6"]
    print(f"  has_behavioral_response_ratio=True:  {ds6_rows['has_behavioral_response_ratio'].sum()}")
    print(f"  has_behavioral_response_ratio=False: {(~ds6_rows['has_behavioral_response_ratio']).sum()}")
