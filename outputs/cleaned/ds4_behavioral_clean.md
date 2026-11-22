# ds4_behavioral_clean.csv

**Source dataset:** Dataset 4 — Large non-experimental data (historic, retrospective use)
**Source file:** `data_raw/4. data set, large non-experimental data/Behavior data set/behavior_data_set_4.csv`
**Produced by:** `notebooks/04_dataset_4_cleaning.ipynb`
**Rows:** 2,490,260
**Columns:** 17

---

## What this file contains

One row per logged OneSec app-interaction event, recorded from users of the OneSec friction app in naturalistic, non-experimental conditions. Only 36.5% of rows (909,948) are friction-intervention exposures; 47.1% (1,171,929) are app-close events and 16.4% (408,383) have no intervention fields at all — see the `intervention_event_class` distribution below, and do not compute override rates over all rows. The dataset spans 2020-09-30 to 2023-04-02 across 1,039 participants, with a median study duration of 66 days per participant and a maximum of ~897 days.

No rows were dropped during cleaning — this is a non-destructive transformation of the raw file.

---

## Column reference

### Original columns (preserved as-is)

| Column | Type | Description |
|---|---|---|
| `app` | string | Original app name triggering the intervention. Contains `whastapp` typo (39,045 rows). Use `app_name` for analysis. |
| `resolution` | string | Raw intervention outcome. 5 values: `closedApp`, `openedApp`, `dismissedAppOpening`, `dismissedByStructuredIntervention`, `dismissedWithHealthyAlternative`. Use `event_outcome_simple` for harmonized mapping. |
| `timestamp` | string | ISO 8601 UTC string (e.g. `2022-09-29T15:48:54Z`). Use `timestamp_utc` for analysis. |
| `interventionDuration` | float64 | Duration of the displayed intervention in seconds. 63.5% NaN — only available for `openedApp` and `dismissedAppOpening` events. All `closedApp` events are NaN. |
| `interventionType` | string | Type of friction intervention shown. 63.5% NaN — always co-missing with `interventionDuration`. 6 types: `breathingExercise`, `minimalBreathingExercise`, `followTheDot`, `blackScreen`, `mirror`, `rotatePhone`. |
| `purpose` | string | Open-text field for app-use reason. 83.1% NaN — not viable for systematic use. |
| `participantUuid` | string | Original participant UUID. No NaN. |
| `secondsSinceStudySetup` | float64 | **Do not use as forward-counting time.** All values are ≤ 0. Counts backward from a per-participant anchor ~8.8h after last event. See `days_since_first_event` instead. |
| `weeksSinceStudySetup` | float64 | Same issue as `secondsSinceStudySetup`. All values ≤ 0. |
| `userIndex` | int64 | Integer participant index (0–1038). 1:1 with `participantUuid`. |

### Derived columns (added during cleaning)

| Column | Type | Description |
|---|---|---|
| `timestamp_utc` | datetime64[ns, UTC] | Parsed UTC datetime from `timestamp`. Use for all time-based analysis. Zero parse failures. |
| `app_name` | string | Canonical app name with `whastapp` corrected to `whatsapp`. Use in place of `app` for analysis. |
| `event_outcome_raw` | string | Copy of raw `resolution` column. Preserved for traceability. |
| `event_outcome_simple` | string | Harmonized outcome: `opened`, `dismissed`, `closed`, `dismissed_other`. The two undocumented resolution values are mapped to `dismissed_other` — confirm their meaning before treating as equivalent to `dismissed`. |
| `intervention_event_class` | string | Structural event classification: `intervention_event` (non-NaN interventionType, 909,948 rows), `app_close_event` (closedApp with NaN interventionType, 1,171,929 rows), `no_intervention` (other rows missing intervention fields, 408,383 rows). |
| `days_since_first_event` | float64 | Forward-counting days elapsed since the participant's first observed event. Derived from `timestamp_utc`. Replaces unusable `secondsSinceStudySetup`. Range: 0–897 days. |
| `participant_id_canonical` | string | Canonical participant ID. Copy of `participantUuid`. Use for joining with survey or linkage table. |

---

## event_outcome_simple distribution

| Value | Count | Share | Notes |
|---|---|---|---|
| `closed` | 1,171,929 | 47.1% | User opened app then closed it |
| `opened` | 881,409 | 35.4% | User opened app despite intervention |
| `dismissed` | 436,110 | 17.5% | User dismissed the intervention |
| `dismissed_other` | 812 | 0.03% | Two undocumented dismissal types — confirm meaning |

## intervention_event_class distribution

| Value | Count | Share | Notes |
|---|---|---|---|
| `app_close_event` | 1,171,929 | 47.1% | All closedApp events; no interventionType recorded |
| `intervention_event` | 909,948 | 36.5% | Active friction intervention; interventionType available |
| `no_intervention` | 408,383 | 16.4% | opened/dismissed without intervention fields |

---

## Cleaning steps applied

1. Parsed `timestamp` to UTC datetime: `pd.to_datetime(df['timestamp'], utc=True)` → `timestamp_utc`
2. Created `app_name` correcting `whastapp` → `whatsapp` typo
3. Created `event_outcome_raw` (copy of `resolution`) and `event_outcome_simple` (mapped)
4. Created `intervention_event_class` based on NaN pattern in `interventionType` and `resolution` value
5. Derived `days_since_first_event` from `timestamp_utc` per participant
6. Added `participant_id_canonical` (copy of `participantUuid`)

No rows were dropped.

---

## Known limitations

- `interventionDuration` / `interventionType`: 63.5% NaN — only available for `intervention_event` class rows
- `purpose`: 83.1% NaN — context field not viable for systematic feature use
- `secondsSinceStudySetup` / `weeksSinceStudySetup` retained but should not be used as forward-counting time
- `dismissedByStructuredIntervention` and `dismissedWithHealthyAlternative` (812 rows) mapped to `dismissed_other` pending clarification
- Non-experimental design — no condition variable, no control group
- 756 participants have no survey data (no psychosocial variables available for them)
- `intervention_event_class = app_close_event` may represent a structurally different logging path; interpret separately from active intervention events

---

## How to load

```python
import pandas as pd

beh = pd.read_csv(
    "outputs/cleaned/ds4_behavioral_clean.csv",
    parse_dates=["timestamp_utc"]
)

# Filter to active intervention events only
interventions = beh[beh["intervention_event_class"] == "intervention_event"]

# Filter to participants with both behavioral and survey data
link = pd.read_csv("outputs/cleaned/ds4_participant_linkage.csv")
linked_ids = link[link["n_files"] == 2]["participant_id_canonical"].tolist()
beh_linked = beh[beh["participant_id_canonical"].isin(linked_ids)]
```
