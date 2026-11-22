# structured_participant_features.csv

**Source dataset:** Structured — Retrospective
**Source files:** `outputs/cleaned/structured_behavioral_clean.csv`, `outputs/features/structured/structured_task_lifecycle_features.csv`
**Producing notebook:** `notebooks/17_structured_feature_extraction.ipynb`
**Producing module:** `src/features/structured_features.py::build_structured_participant_features`
**Rows:** 61 (all behavioral participants)
**Columns:** 32
**Unit of observation:** One participant

---

## What this file contains

One row per participant with behavioral data, aggregating task-lifecycle outcomes (from
`structured_task_lifecycle_features.csv`) with event-level volume and temporal-pattern features
(reusing the same shared utilities — `volume_features`, `temporal_features`, `hour_entropy` — used by
the DS1/DS4/DS5/DS6 feature extraction modules in this project).

---

## Column Reference

| Column | Type | Description |
|---|---|---|
| `participant_id` | string (UUID) | Participant identifier |
| `total_events` | int | Total behavioral events (from shared `volume_features`) |
| `n_days_observed` | int | Distinct calendar days with ≥1 event |
| `obs_window_days` | float | Days between first and last event |
| `events_per_day` | float | Mean events per day of observation = `total_events / obs_window_days`; **unbounded for very short windows** — see Known Limitations |
| `active_days_per_week` | float | Mean active days per 7-day window |
| `n_unique_tasks` | int | Distinct tasks this participant touched |
| `n_created_events` / `n_updated_events` / `n_deleted_events` | int | Event-type counts |
| `pct_tasks_completed` | float | Share of this participant's tasks with `lifecycle_status == "completed"` |
| `pct_tasks_deleted` | float | Share with `lifecycle_status == "deleted"` |
| `pct_tasks_unresolved` | float | Share with `lifecycle_status == "unresolved"` (the three shares sum to 1.0, verified) |
| `pct_tasks_ever_uncompleted` | float | Share of tasks ever marked completed then un-completed |
| `pct_tasks_left_censored` | float | Share of this participant's tasks with no visible `Task Created` event — **varies enormously by participant** (0% to 100%, median 42.9%) |
| `share_task_type_timed` / `_all_day` / `_inbox` | float | Task-type composition, computed at the task level using each task's last-known type |
| `mean_events_per_task` | float | Average lifecycle depth (edits) per task |
| `reschedule_rate` | float | Reschedule-tagged update events ÷ total update events |
| `mean_type_changes_per_task` | float | Average number of task-type changes per task |
| `recurrence_use_rate` | float | Share of tasks ever marked recurring |
| `notes_use_rate` | float | Share of tasks with notes at last observation |
| `mean_subtasks_amount` | float | Average subtask count per task |
| `peak_hour_of_day` | int | Modal hour of activity (shared utility) |
| `weekend_event_share` / `evening_event_share` / `morning_event_share` | float | Temporal distribution (shared utility) |
| `hour_entropy` | float | Shannon entropy of hourly activity distribution (shared utility) |
| `subscription_type_last` | string | Subscription tier at most recent event |
| `subscription_changed` | bool | True if subscription tier changed during the observed period |
| `days_observed` | float | Days from first to last event (duplicate of `obs_window_days`, kept for naming consistency with `structured_behavioral_clean.csv`) |

---

## Key Distributions

### Task outcome composition (mean across 61 participants — differs from the task-level pooled figures in `structured_task_lifecycle_features.md` because task counts are highly skewed across participants)
| Metric | Mean |
|---|---|
| pct_tasks_completed | 0.489 |
| pct_tasks_deleted | 0.116 |
| pct_tasks_unresolved | 0.395 |

### Task type composition (mean)
| Metric | Mean |
|---|---|
| share_task_type_timed | 0.941 |
| share_task_type_all_day | 0.027 |
| share_task_type_inbox | 0.032 |

### Left-censoring (`pct_tasks_left_censored`)
min 0%, median 42.9%, mean 48.8%, max 100% — left-censoring is not uniform; some participants'
task histories are almost entirely pre-existing, others are almost entirely observed from creation.
Any model using `has_creation_event`-dependent features should check this per participant.

---

## Cleaning / Derivation Steps Applied

1. Loaded `structured_task_lifecycle_features.csv` and grouped by `participant_id`
2. Reused shared `volume_features`, `temporal_features`, `hour_entropy` from `src/features/behavioral_features.py` (same utilities used by DS1/DS4/DS5/DS6) — no Structured-specific reimplementation needed for these
3. Task outcome/type-composition features computed at the task level (one vote per task), not the event level, to avoid biasing toward heavily-edited tasks
4. Validated: `pct_tasks_completed + pct_tasks_deleted + pct_tasks_unresolved == 1.0` for all 61 participants (max deviation 0.0001, floating-point rounding only)

---

## Known Limitations

- All ratio features have a variable, sometimes small denominator (`n_unique_tasks` ranges widely across participants) — no minimum-task-count threshold has been applied yet; consider one before using these features in a clustering/phenotyping stage (mirrors the `MIN_DAYS` threshold applied for DS5).
- `events_per_day` is `total_events / obs_window_days` with only a `window > 0` guard (unlike its sibling `active_days_per_week`, which is gated at `window >= 7`), so participants whose entire observation span is minutes get meaningless rates: `<participant-id>` (4 events, 0.00 days) = 5830.55, `<participant-id>` (16 events, 0.01 days) = 2824.67, `<participant-id>` (69 events, 0.03 days) = 2055.38, against a cohort median of 3.65 (mean 186.85, std 857.33). **Never use `events_per_day` unstandardised or as a distance-based clustering feature without first filtering on `obs_window_days >= 1`** (Structured Path D, `notebooks/124_structured_dynamic_stochastic_phenotype.ipynb`, already returned "no feasible k" because of a single extreme outlier). Apply this filter alongside the `n_unique_tasks >= 10` filter suggested above.
- `pct_tasks_left_censored` is a genuine confound for any feature relying on creation-event visibility (e.g. creation-channel analysis) — high-censoring participants should be flagged or excluded from those specific analyses, not from all analyses.
- `pct_tasks_completed` / `pct_tasks_unresolved` are **censoring-dependent**: they are computed over all tasks, including the 60.7% that are left-censored, whose pre-window completion state is unobservable. Across the 61 participants corr(`pct_tasks_left_censored`, `pct_tasks_completed`) = +0.357 and corr(`pct_tasks_left_censored`, `pct_tasks_unresolved`) = −0.513. Mean `pct_tasks_completed` is 0.489 over all tasks but 0.391 when restricted to `has_creation_event == True`; for `<participant-id>` (98.1% censored) the two values are 0.869 vs 0.158. This column therefore partly measures how much pre-existing task history a participant had. It feeds the tercile split that assigns GaT phenotype labels in `notebooks/66_structured_game_theory.ipynb` (cell 15) — re-check those labels against a `has_creation_event == True` variant before treating them as behavioral.
- `reschedule_rate` denominator is `n_updated_events`, not `n_unique_tasks` — it measures "how often an update is a reschedule," not "how often a task gets rescheduled."
- No survey/psychosocial data joined here — see `structured_survey_features.csv` for that, joined separately (deliberately not merged into this file to preserve the behavior-only unit of analysis).
- `peak_hour_of_day` is `hour.value_counts().idxmax()` with **no deterministic tie-break**, and pandas' tie ordering is hash-dependent. One participant here, `<participant-id>`, has an exact 13-vs-13 tie between hours 19 and 17: the committed CSV stores 17, while a re-run of `notebooks/17_structured_feature_extraction.ipynb` on pandas 2.3.3 returns 19. Every other column reproduces exactly. Do not read a change in this single cell after a re-run as a real code change.

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/features/structured")

pf = pd.read_csv(OUT / "structured_participant_features.csv")

# Join survey features
sf = pd.read_csv(OUT / "structured_survey_features.csv")
merged = pf.merge(sf, on="participant_id", how="left")

# Restrict to participants with reasonably-sized task histories
pf_min10 = pf[pf["n_unique_tasks"] >= 10]
```
