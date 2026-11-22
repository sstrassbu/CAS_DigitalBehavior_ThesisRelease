# ds1_behavioral_clean.csv

**Source dataset:** Dataset 1 — Compact friction intervention testing  
**Source file:** `data_raw/1. data set, compact friction intervention testing/Behavior data set/behavioral_data_set_1.csv`  
**Produced by:** `notebooks/02_dataset_1_cleaning.ipynb`  
**Rows:** 398,757  
**Columns:** 10  

---

## What this file contains

One row per smartphone intervention event. Each row records a single moment when the OneSec app intercepted a user attempting to open a social media app, and what the user did in response (opened the app anyway, dismissed the intervention, or closed the app).

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participantUuid` | string | Original participant identifier — raw UUID from source file. Preserved for traceability. |
| `app` | string | Original app name from source file. May contain typos (e.g. `whastapp`). |
| `timestamp` | int64 | Original Unix epoch timestamp in seconds. Preserved as-is. |
| `purpose` | string | Optional free-text comment entered by the user at the time of the event. 71.3% NaN — not reliable as a systematic variable. |
| `resolution` | string | Original intervention outcome. Values: `openedApp`, `dismissedAppOpening`, `closedApp`, NaN. |
| `secondsSinceOneSecSetup` | float64 | Seconds elapsed since the participant first set up the OneSec app. 18.9% NaN. Range: ~76 sec to ~64.7 days. Useful as a longitudinal adaptation proxy for participants where available. |
| `timestamp_utc` | string | Human-readable UTC datetime derived from `timestamp`. Format: `YYYY-MM-DD HH:MM:SS+00:00`. Converted with `pd.to_datetime(unit='s', utc=True)`. |
| `app_name` | string | Cleaned canonical app name. Same as `app` except `whastapp` corrected to `whatsapp`. Use this column for all app-level analysis. |
| `event_outcome_simple` | string | Simplified intervention outcome. Values: `opened`, `dismissed`, `closed`, `missing`. Maps from `resolution`. Use for cross-dataset harmonization and outcome modeling. |
| `participant_id_canonical` | string | Canonical participant identifier for harmonized analysis. Copy of `participantUuid`. Use this column when joining with other datasets or the linkage table. |

---

## Cleaning steps applied

1. Reread source CSV with `sep=';'` (semicolon delimiter)
2. Dropped 1 row with NaN `participantUuid`
3. Dropped 8,302 fully duplicate rows (`keep='first'`)
4. Converted `timestamp` to UTC datetime → `timestamp_utc`
5. Corrected `whastapp` typo → `whatsapp` in `app_name`
6. Mapped `resolution` to simplified values in `event_outcome_simple`
7. Added `participant_id_canonical` as canonical ID column

---

## Key distributions

| event_outcome_simple | Count | Share |
|---|---|---|
| opened | 203,293 | 51.0% |
| dismissed | 98,278 | 24.6% |
| closed | 96,719 | 24.2% |
| missing | 467 | 0.1% |

Note: `dismissed` share shifted relative to the raw file because duplicates were disproportionately `dismissedAppOpening` events.

---

## Known limitations

- `purpose`: 71.3% NaN — use only as qualitative supplement, not as a systematic feature
- `secondsSinceOneSecSetup`: 18.9% NaN at event level, but the missingness is participant-level and all-or-nothing — 529 participants have it on every row, 90 on none, none mixed. The field was effectively not logged before ~June 2021 (monthly coverage: 0.7% in 2021-04, 3.2% in 2021-05, 56.4% in 2021-06, 97.6% in 2021-07), so the 90 zero-coverage participants are an enrollment cohort (68 first seen 2021-04, 14 in 2021-05), not a random subset. Treat exclusion from longitudinal/adaptation analysis as cohort selection and check it as a covariate.
- No timezone column — all timestamps treated as UTC (assumption, not confirmed in codebook)
- 619 unique participants in behavioral data; only 168 are linked to both surveys (see linkage table)

---

## How to load

```python
import pandas as pd
beh = pd.read_csv("outputs/cleaned/ds1_behavioral_clean.csv",
                  parse_dates=["timestamp_utc"])
```
