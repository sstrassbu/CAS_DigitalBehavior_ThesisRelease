# DS6 Audit Report — Danish Adolescents

**Date:** 2026-04-15  
**Dataset:** Dataset 6 — Danish adolescents  
**Raw folder:** `data_raw/6. data set, Danish adolescents/`  
**Study design:** Experimental longitudinal study — baseline phase + intervention phase + open-restriction phase  
**Population:** Danish adolescents (ages 13–17)

---

## 1. File Inventory

| File | Location | Size | Rows | Cols | Role |
|---|---|---|---|---|---|
| `session_time_dataset_97_5_cutoff_data_forwarded.csv` | Data/behavioral data/ | 243 MB | 353,796 | 70 | **Primary behavioral file** — baseline + intervention periods |
| `baseline_sessions_filt3.csv` | Data/behavioral data/ | 126 MB | 195,515 | 63 | Baseline-only openedApp events with sequence features |
| `survey_data_clean.csv` | Data/behavioral data/ | 60 KB | 478 | 17 | Repeated survey (2 waves, psychometric indices) |
| `survey_data_full.csv` | Data/behavioral data/ | 137 KB | 929 | 32 | Extended survey with raw items (3 waves) |
| `demographic_data.csv` | Data/behavioral data/ | 14 KB | 399 | 4 | Participant demographics |
| `Danish adolescents & one sec, main study, pre-survey.csv` | Data/ | 1.0 MB | 467 | 68+ | Pre-study Qualtrics survey (large, complex) |
| `Pre-Survey overview.pdf` | Data/ | 1.2 MB | — | — | Survey documentation |
| `Project description…docx` | root | 6.7 KB | — | — | Study design |
| `README.md` | root | 8.7 KB | — | — | Dataset overview |

---

## 2. Delimiter and Encoding

All CSV files use **comma (`,`)** as delimiter.  
Encoding: UTF-8.

---

## 3. Primary Behavioral File: session_time_dataset_97_5_cutoff_data_forwarded.csv

### 3.1 Structure

- **Unit of observation:** one app-opening event (openedApp) per row
- **All rows have resolution = `openedApp`** — this file exports only the Open half of an alternating Open→Close→Open→Close log; `group_id`/`first_in_group`/`last_close_in_group` do NOT provide session grouping (verified false 2026-08-05, see §8a), but `close_ts`/`time_diff_secs` do carry genuine open→close dwell time for ~99% of rows via the look-ahead columns (see §8b)
- **Primary key:** `ID` (participant ID), no composite key but `row_id` is unique
- **Timestamp:** ISO 8601 UTC strings (`2024-10-04T20:56:16Z`)
- **Periods covered:** both `baseline` (158,889 rows) and `intervention` (194,907 rows)

### 3.2 Confirmed Column Set (key columns)

| Column | Type | Notes |
|---|---|---|
| `ID` | string | Participant identifier (15-char alphanumeric) |
| `study_id` | int | Numeric study ID; 1:1 with ID |
| `timestamp` | string | ISO 8601 UTC event timestamp |
| `time` | string | Duplicate of timestamp column |
| `app` | string | App name |
| `resolution` | string | Always `openedApp` in this file |
| `cond` | int | Numeric condition code (1–6; study school/cohort group) |
| `condition` | string | Text condition: `control`, `default`, `intervention` |
| `period` | string | `baseline` or `intervention` |
| `participation_day` | int | Day number in study (1-indexed) |
| `week` | int | Study week number |
| `week_day` | int | Numeric day of week |
| `hour` | int | Hour of day (0–23) |
| `interventionType` | string | Type of friction shown; NaN for ~67% (control/baseline events) |
| `interventionDuration` | float | Duration of intervention in seconds; NaN for ~67% |
| `isReIntervention` | int | 1 if this was a re-intervention attempt |
| `timeIntervalUntilReIntervention` | float | Seconds until re-intervention; NaN for ~86% |
| `group_id` | int | **Does NOT group open+close sessions** — verified 2026-08-05 to be unique per row across all 353,796 rows. See §8a. |
| `app_next`, `app_next2`, `app_next3` | string | Next 1–3 apps in the RAW look-ahead sequence — **not** "next apps opened" (see §8b): `app_next` mechanically echoes the current app's own close record 99.3% of the time; `app_next2` is the genuine next distinct app opened |
| `app_prev`, `app_prev2` | string | Previous 1–2 apps |
| `resolution_next`, `resolution_next2`, `resolution_next3` | string | Next event outcomes |
| `time_diff_secs` | float | Seconds until next event |
| `time_diff_minutes` | float | Minutes until next event |
| `first_in_group` | int/bool | **Constant** — always 1 for every row (verified 2026-08-05). Not informative. |
| `last_close_in_group` | int/bool | **Constant** — always 0 for every row (verified 2026-08-05). Not informative. |
| `purpose` | string | Stated purpose; 88.9% NaN |
| `row_id` | int | Unique row identifier |

### 3.3 Condition Distribution

| condition | Count | period=baseline | period=intervention |
|---|---|---|---|
| control | 153,236 | — | — |
| default | 100,888 | — | — |
| intervention | 99,672 | — | — |

Note: `condition` label refers to intervention arm; `control` participants also have data in both periods.

### 3.4 Participant IDs

- **243 unique IDs** in session file
- Format: 15-character alphanumeric string (e.g. `20Pg2e8tYCFG5N8`)
- No transformation needed — already canonical format
- `ID` and `response_id` in survey file are **identical** — direct join possible

### 3.5 Timestamp Format

- ISO 8601 UTC (`2024-10-04T20:56:16Z`) — parse directly with `pd.to_datetime(utc=True)`
- No timezone conversion needed

### 3.6 Missingness (top columns)

| Column | NaN count | NaN % |
|---|---|---|
| `purpose` | 314,184 | 88.8% |
| `timeIntervalUntilReIntervention` | 303,717 | 85.8% |
| `interventionType` | 236,270 | 66.8% |
| `interventionDuration` | 236,270 | 66.8% |
| `app_prev2`, `resolution_last2` | ~174 | 0.05% |
| `app_next3`, `resolution_next3` | ~164 | 0.05% |

### 3.7 Duplicate Rows

**Zero duplicate rows** in session file or baseline file.

---

## 4. Baseline File: baseline_sessions_filt3.csv

- **195,515 rows**, 63 columns
- **All rows: period = `baseline`, resolution = `openedApp`**
- Contains same core columns as session file plus additional sequence columns
- `studyActivated = 0` for all rows (baseline: intervention not yet active)
- Intervention fields nearly entirely NaN (only 18 `interventionType` values, all during baseline pre-activation)
- Key distinction: `date2` column provides date-only field; `close_ts` provides a genuine matched close timestamp for ~99% of rows (see §8b — not session-grouped via `group_id`, but real dwell-time data via the row's own look-ahead)
- **Relationship to session file:** baseline_sessions_filt3.csv is a filtered subset of baseline period rows from the larger dataset, with additional sequence engineering. The session file is primary for cross-period analysis.

---

## 5. Survey Files

### survey_data_clean.csv

- 478 rows, 17 columns
- **269 unique response_id** (= participant IDs) — 2 waves each for 209 participants, 1 wave for 60
- survey_nr: 1 = pre-intervention wave, 2 = post-intervention wave
- Columns: pre-computed psychometric indices (addiction_index, self_control_index, retention_index, trivsel, socialconnection, fo_mo) — already aggregated
- `cond`: text (default/intervention/control); `cond_exp2`: simplified binary (OneSec Default / Control)

### survey_data_full.csv

- 929 rows, 32 columns
- **440 unique response_id** — 3 waves (survey_nr 1/2/3)
- Includes raw items: `afhaengighed_1`–`afhaengighed_6` (addiction), `selvkontrol_1`–`selvkontrol_5` (self-control)
- Also includes: `svaertatlukke`, `meretidendonsket`, `fotrudttid`, `forstyrretaf_so_me` (additional digital use items)
- All 269 participants in survey_clean are a subset of the 440 in survey_full

### Danish pre-survey

- 467 rows, 68+ columns — Qualtrics export format
- Contains ResponseId, condition, and extensive pre-study items (Danish language)
- Complex structure — not cleaned in this pipeline; flagged for separate treatment

---

## 6. Demographics

- 399 rows × 4 columns: `ID`, `age`, `gender`, `region`
- Gender: `kvinde` (female, 269), `mand` (male, 129), 1 NaN
- Age: 13–17 (true adolescent range, unlike DS5)
- Regions: Midtjylland (120), Hovedstaden (116), Syddanmark (74), Sjælland (62), Nordjylland (27)
- 399 demographic records, but only 243 have behavioral data → 156 enrolled but no behavioral events

---

## 7. ID Reconciliation

| Set | Count |
|---|---|
| Behavioral IDs (session file) | 243 |
| Demographic IDs | 399 |
| Survey clean IDs | 269 |
| Behavioral ∩ Demographic | 243 (100%) |
| Behavioral ∩ Survey clean | 244 (≈100%, 1 extra) |
| Demographic ∩ Survey clean | 269 |
| In all three | 243 |

All 243 behavioral participants have demographic records. All 243 also appear in survey_clean. 156 demographic-only participants (enrolled, not active).

---

## 8. Codebook Discrepancies and Ambiguities

| Item | Status |
|---|---|
| All rows in both behavioral files = `openedApp` | Confirmed — no close/dismiss events in these files |
| `cond` is numeric (1–6), `condition` is text | Confirmed — use `condition` for analysis |
| `baseline_sessions_filt3.csv` vs session file relationship | Confirmed — baseline file is filtered baseline-only subset |
| `survey_data_clean` vs `survey_data_full` | Confirmed — clean is subset of full; clean = 2 waves, full = 3 waves |
| Pre-survey Qualtrics file structure | Complex Qualtrics export — not yet cleaned |
| `gender` column in Danish | Confirmed — `kvinde`=female, `mand`=male |
| `interventionType` values | `denmark`, `breathingExercise`, `math`, `followTheDot`, `randomText` |

---

## 8a. Session-structure bug (found 2026-08-05, during Stage 4 pre-modeling check)

This section corrects §3.2 and §9 (original text below has been struck through inline
above/below where affected). Before implementing the first DS6 CAS model, the claim that
`group_id` enables session-level (open→close) analysis was checked directly against the raw
file rather than taken on faith.

**Verified on the full raw file (`session_time_dataset_97_5_cutoff_data_forwarded.csv`, all
353,796 rows):**
- `group_id` is unique per row (`nunique() == len(df)`) — it does not group multiple events
  into a session.
- `first_in_group == 1` for every row; `last_close_in_group == 0` for every row;
  `unmatched_open == False` for every row.
- `close_ts − openedapp_open_time` equals `time_diff_secs` exactly (max abs difference
  ~1e-12, i.e. float rounding).
- Same pattern in `baseline_sessions_filt3.csv` (no `group_id` column there; its own
  `close_ts − timestamp` also tracks `time_diff_secs`).

**Conclusion:** `group_id`/`first_in_group`/`last_close_in_group` provide **no genuine
session-count grouping** — every "group" is a single row. This is in addition to (not the
same as) the already-documented finding that the `resolution` column has no dismiss/close
outcomes — that finding is about outcomes; this one is about the separate `group_id` column
that was believed to provide session grouping independent of outcome. The 8 Stage 1 features
built on `group_id` (`n_sessions_total`, `session_rate_baseline/intervention/ratio`,
`share_events_first_in_group`, `share_sessions_with_matched_close`,
`session_rate_early/late`) were exact numerical duplicates of event-count features and have
been removed — see `data_docs/stage1_feature_qc_notes.md` addendum.

**⚠ Correction (2026-08-06):** the paragraph above originally also claimed `close_ts` "is the
timestamp of the next open event, not a real app-close timestamp." That claim was wrong and
is retracted — see §8b below. `close_ts`/`time_diff_secs` are genuine open→close dwell-time
data for the large majority of rows; only `group_id`-based *session grouping* is fake, not
`close_ts` itself.

## 8b. `app_next` look-ahead bug — a second, separate finding (2026-08-06)

Found while designing the DS6 Network Theory model, which was about to use `app_next` as
its primary transition-edge data.

DS6's true underlying event log alternates Open→Close→Open→Close — this exported file keeps
only the Open rows, but look-ahead columns (`app_next`, `resolution_next`, etc.) were
computed against the FULL alternating sequence:

- `resolution_next == 'closedApp'` for 351,446/353,796 rows (99.4%) — the very next logged
  event after an Open is almost always that same app's own close. This is *why*
  `close_ts`/`time_diff_secs` are genuine dwell time (§8a correction above): the next logged
  event really is usually a real close.
- Conditioned on `resolution_next == 'closedApp'`, `app_next == app_name` 99.3% of the time
  — `app_next` mechanically echoes the current app's own close record, not a real
  subsequent app choice. `app_next` therefore does **not** mean "next app opened."
- `app_next2`/`resolution_next2` skip this correctly: `resolution_next2 == 'openedApp'` for
  64.7% of rows (the true next Open), and conditioned on that, `app_next2 == app_name` only
  38.8% of the time — a believable same-app-vs-switch split.
- `app_prev` (looking backward) does not have the forward problem: `app_prev == app_name`
  only ~42% overall, stable (39–64%) across `resolution_last` categories.

**Consequence:** every DS6 sequence feature except `max_consecutive_same_app` was built on
`app_next`/`resolution_next` and was unreliable — including `app_next_entropy` and
`n_unique_next_apps`, which §4/Group 4 of `ds6_features.md` had **explicitly recommended**
as the preferred substitution features. Rebuilt on `app_prev` 2026-08-06 — see
`data_docs/stage1_feature_qc_notes.md` addendum and `ds6_features.md` Group 4 for the
corrected feature set and real numbers (`self_transition_rate` mean=0.512, sd=0.217 — was
mean=0.989, sd=0.018).

---

## 9. Data Quality Summary

| Dimension | Assessment |
|---|---|
| Completeness | Good for core event and condition columns; high NaN for purpose and reintervention timing |
| Timestamp quality | ISO 8601 UTC — excellent, parse directly |
| ID quality | Clean 15-char IDs, no transformation needed |
| Duplicate rows | None in any file |
| Condition assignment | Clean in both numeric and text forms |
| Session structure | **No genuine session structure** — `group_id` does not group events; see §8a (corrects earlier "enables open/close matching" claim) |
| Survey waves | Consistent across clean file; full file extends to 3 waves |

---

## 10. Cleaning Steps Applied

1. Loaded session file with comma delimiter
2. Used `ID` directly as `participant_id_canonical` (no transformation)
3. Parsed `timestamp` as UTC → `event_timestamp_utc`
4. Set `event_outcome_raw` = `resolution` (= openedApp), `event_outcome_simple` = `'opened'`
5. Cast `interventionDuration`, `timeIntervalUntilReIntervention` to float
6. Used `isReIntervention` as `is_reintervention` (0/1)
7. Computed `days_since_first_event` per participant from UTC timestamps
8. Retained pre-engineered sequence columns (app_next*, app_prev*, resolution_next*, group_id, time_diff_*)
9. Renamed `app` → `app_name`
10. Cleaned demographics: added `gender_raw`, mapped gender to English (`female`/`male`)
11. Built participant linkage from union of all participant IDs

---

## 11. Remaining Limitations

- No dismiss or close events in behavioral files — cannot compute dismiss rates from the resolution column
- **No session *count* is recoverable** — `group_id` does not encode real session boundaries (see §8a). Open→close *dwell time* IS recoverable via `time_diff_secs`/`close_ts` for ~99% of rows (see §8b), but not multi-event session grouping.
- **`app_next` does not mean "next app opened"** (see §8b) — use `app_prev` (or `app_next2`) for real transition/substitution analysis
- 156 participants in demographics have no behavioral data
- Pre-survey Qualtrics file (467 rows, 68+ cols) not yet cleaned
- `survey_data_full.csv` wave 3 (survey_nr=3) not represented in survey_clean
- `purpose` is 89% NaN — not usable for most analysis
- `condition` = 'control' includes both baseline and intervention periods; may require period-stratified analysis

---

## 12. Outputs

| File | Location |
|---|---|
| `ds6_behavioral_clean.csv` | `outputs/cleaned/` |
| `ds6_survey_clean.csv` | `outputs/cleaned/` |
| `ds6_demographics_clean.csv` | `outputs/cleaned/` |
| `ds6_participant_linkage.csv` | `outputs/cleaned/` |
| `ds6_audit_report.md` | `outputs/reports/` |
