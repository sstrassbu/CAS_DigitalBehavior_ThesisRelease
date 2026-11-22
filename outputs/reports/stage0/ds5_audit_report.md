# DS5 Audit Report — German Adolescents

**Date:** 2026-04-15  
**Dataset:** Dataset 5 — German adolescents  
**Raw folder:** `data_raw/5. data set, German adolescents/`  
**Study design:** Experimental, three-group RCT (control / default friction / reintervention)  
**Population:** German adolescents (ages 13–25, median ~18–19)

---

## 1. File Inventory

| File | Location | Size | Rows | Cols | Role |
|---|---|---|---|---|---|
| `behavior_data_set_5.csv` | Behavior data set/ | 51 MB | 288,688 | 13 | Primary behavioral events |
| `behavior_data_set_5.xlsx` | Behavior data set/ | 12 MB | same | same | Duplicate XLSX export — not used |
| `codebook_behavior_data_set_5.pdf` | Behavior data set/ | 62 KB | — | — | Behavioral codebook |
| `pre_survey_data_set_5.csv` | Survey data sets/Pre-survey/ | 307 KB | 792 | 37 | Pre-intervention survey |
| `codebook_pre_survey_data_set_5.pdf` | Survey data sets/Pre-survey/ | 71 KB | — | — | Pre-survey codebook |
| `post_survey_data_set_5.csv` | Survey data sets/Post-survey/ | 39 KB | 314 | 33 | Post-intervention survey |
| `codebook_post_survey_data_set_5.pdf` | Survey data sets/Post-survey/ | 70 KB | — | — | Post-survey codebook |
| `Project description…docx` | root | 6.6 KB | — | — | Study design description |
| `README.md` | root | 6.1 KB | — | — | Dataset overview |

---

## 2. Delimiter and Encoding

All three CSV files use **semicolon (`;`)** as delimiter.  
Encoding: UTF-8. No encoding errors observed.

---

## 3. Behavioral File Audit

### 3.1 Structure

- **Unit of observation:** one app-opening or friction-intervention event per row
- **Primary key:** `userid` (participant identifier, always populated)
- **Timestamp column:** `timestamp` — local datetime string (ISO-like, no timezone suffix)
- **Timezone column:** `timezone` — IANA timezone string (e.g. `Europe/Berlin`)
- **Delimiter:** semicolon

### 3.2 Confirmed Column Set

| Column | Type | Notes |
|---|---|---|
| `timestamp` | string | Local datetime, requires timezone localization |
| `timezone` | string | IANA tz; 3,457 NaN (same rows as missing resolution) |
| `interventionDuration` | float | Seconds; 0.0 for opened, 6.0 for dismissed |
| `timeIntervalUntilReIntervention` | float | Seconds until re-intervention (reintervention group only) |
| `app` | string | App name (lowercase) |
| `resolution` | string | Event outcome |
| `userid` | string | Participant ID with study prefix |
| `reason` | string | German-language stated reason for app use |
| `suggestionBannerShown` | string | German suggestion text; 99%+ NaN |
| `suggestionDetailViewAppear` | float | Timestamp-like; 99.9%+ NaN |
| `suggestionDetailViewDisappear` | float | 99.9%+ NaN |
| `terminationReason` | string | `terminatedByUser` for 12 rows only |
| `suggestionLearnMoreLinkTapped` | float | 99.9%+ NaN |

### 3.3 Resolution (Event Outcome)

| Value | Count | % | Mapping |
|---|---|---|---|
| `openedApp` | 177,986 | 61.6% | `opened` |
| `dismissedAppOpening` | 62,107 | 21.5% | `dismissed` |
| `closedApp` | 45,019 | 15.6% | `closed` |
| NaN | 3,457 | 1.2% | `missing` |
| `dismissedByStructuredIntervention` | 119 | 0.04% | `dismissed_other` |

### 3.4 Participant IDs

- **573 unique userids** in behavioral
- userid format: `study-one-sec-next-gen-bzkj-2024-one-sec-next-gen-bzkj-2024-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX`
- The prefix `study-one-sec-next-gen-bzkj-2024-` must be stripped to align with survey `uuid` format
- After stripping: canonical format = `one-sec-next-gen-bzkj-2024-XXXXXXXX-...`

### 3.5 Timestamp Format

- Format: `2024-12-04 19:03:44.66361` (local time, no tz offset)
- Timezone column provides IANA zone per row
- Cleaning action: parse as naive → localize via timezone col → convert to UTC
- 3,457 rows have NaN timezone (same rows missing resolution and app) — fallback Europe/Berlin applied

### 3.6 Missingness

| Column | NaN count | NaN % |
|---|---|---|
| `reason` | 122,190 | 42.3% |
| `interventionDuration` | 48,742 | 16.9% |
| `timeIntervalUntilReIntervention` | 224,868 | 77.9% |
| `suggestionBannerShown` | 285,924 | 99.0% |
| `suggestionDetailViewAppear` | 288,358 | 99.9% |
| `suggestionDetailViewDisappear` | 288,358 | 99.9% |
| `terminationReason` | 288,676 | 99.996% |
| `suggestionLearnMoreLinkTapped` | 288,667 | 99.993% |
| `timezone`, `app`, `resolution` | 3,457 each | 1.2% |
| `timestamp`, `userid` | 0 | 0% |

**Note:** `interventionDuration` = 0 for all `openedApp` events (no friction shown). `timeIntervalUntilReIntervention` is present only for the reintervention condition. Suggestion columns are nearly all missing because only a small experiment sub-group was shown suggestions.

### 3.7 Duplicate Rows

**Zero duplicate rows** in behavioral file.

### 3.8 Timezone Distribution

39 unique timezone values. Dominant timezone: `Europe/Berlin`. Other European, Asian, and American timezones present in small numbers (study travel / non-German participants).

---

## 4. Pre-Survey Audit

- **Shape:** 792 rows × 37 columns
- **Unit:** one survey response per participant
- **Zero duplicate UUIDs**
- **Condition distribution:** control=265, default=264, reintervention=263 (well-balanced)
- **Age range:** 13–25 (modal 18–20; labelled as adolescent but includes young adults)
- **Psychometric scales:** belong (8 items), ostracism (5 items), fomo (10 items)
- **Scale items:** Numeric Likert, moderate missingness (~7% for scale items, ~5–7% for individual ratings)
- **Notable:** `prob_other` is 94% NaN (free text field), `goal_other` is 98% NaN — both open-ended optional fields

### 4.1 Scale Missingness

| Scale | N items | NaN per item |
|---|---|---|
| belong | 8 | 53 rows (~6.7%) |
| ostracism | 5 | 47 rows (~5.9%) |
| fomo | 10 | 54 rows (~6.8%) |
| digital_wellbeing | 1 | 18 rows |
| social_media_wellbeing | 1 | 17 rows |

---

## 5. Post-Survey Audit

- **Shape:** 314 rows × 33 columns
- **311 unique UUIDs** — 3 participants have two responses (kept first occurrence)
- **No condition column** in post-survey (must be joined from pre-survey)
- **Additional columns vs pre:** `solve_prob`, `address_goal` (intervention outcome questions)
- **Scale structure identical to pre-survey**

---

## 6. ID Reconciliation

| Set | Count |
|---|---|
| Behavioral participants (after strip) | 573 |
| Pre-survey participants | 792 |
| Post-survey participants | 311 |
| In behavioral AND pre-survey | 572 |
| In behavioral AND post-survey | 284 |
| In pre-survey AND post-survey | 311 |
| In all three | 284 |

- 1 behavioral participant not found in pre-survey (no condition assignable)
- 220 pre-survey participants have no behavioral data (enrolled but app not used or data not captured)
- Post-survey is fully a subset of pre-survey (all 311 post respondents are in pre-survey)

---

## 7. Codebook Discrepancies and Ambiguities

| Item | Status |
|---|---|
| `cond` not in behavioral | Confirmed — condition only in pre-survey; must be joined |
| `reason` column: German text, not coded | Confirmed — free text, not yet categorized |
| `interventionDuration` = 0 for openedApp | Expected — opened events bypass friction |
| `suggestionBannerShown` nearly all NaN | Confirmed — only populated for small suggestion-exposure sub-group |
| `terminationReason` near-entirely NaN | Confirmed — only 12 events have this (terminatedByUser) |
| Age range extends to 25 | Confirmed — dataset labelled adolescent but includes young adults |
| Timestamp has no UTC suffix | Confirmed — local time; use timezone column for UTC conversion |

---

## 8. Data Quality Summary

| Dimension | Assessment |
|---|---|
| Completeness | Good for core columns; sparse for suggestion and termination columns |
| Timestamp quality | Parseable; requires timezone-aware localization |
| ID quality | Clean; prefix stripping aligns formats |
| Duplicate rows | None |
| Duplicate IDs | None in behavioral or pre; 3 in post (resolved by first-occurrence rule) |
| Condition balance | Excellent (265/264/263) |
| Core outcome variable | Clean and consistent across resolution values |

---

## 9. Cleaning Steps Applied

1. Load behavioral with semicolon delimiter
2. Strip `study-one-sec-next-gen-bzkj-2024-` prefix from `userid` → `participant_id_canonical`
3. Parse `timestamp` as naive datetime, localize per `timezone` column using `zoneinfo`, convert to UTC → `event_timestamp_utc`
4. Map `resolution` → `event_outcome_raw` (original) and `event_outcome_simple` (simplified 5-class)
5. Cast `interventionDuration` and `timeIntervalUntilReIntervention` to float → `intervention_duration_sec`, `reintervention_delay_sec`
6. Derive `is_intervention_event` (1 if duration > 0), `is_reintervention` (1 if delay not NaN)
7. Compute `days_since_first_event` per participant (from UTC timestamps)
8. Load pre/post surveys with semicolon; compute mean scores for belong, ostracism, fomo scales
9. Drop 3 duplicate UUIDs from post-survey (keep first)
10. Build participant linkage table

---

## 10. Remaining Limitations

- `reason` column is German free text — not yet categorized or coded
- `cond` not in behavioral — must join via participant linkage
- 220 pre-survey participants have no behavioral data (unknown whether they dropped out or never activated app)
- Suggestion columns are nearly entirely NaN — cannot use for most participants
- Timestamps are localized using a single timezone per row; participants who traveled and changed timezone mid-study may have localization errors
- `dismissedByStructuredIntervention` (119 rows) is an undocumented resolution type — treated as `dismissed_other`

---

## 11. Outputs

| File | Location |
|---|---|
| `ds5_behavioral_clean.csv` | `outputs/cleaned/` |
| `ds5_pre_survey_clean.csv` | `outputs/cleaned/` |
| `ds5_post_survey_clean.csv` | `outputs/cleaned/` |
| `ds5_participant_linkage.csv` | `outputs/cleaned/` |
| `ds5_audit_report.md` | `outputs/reports/` |
