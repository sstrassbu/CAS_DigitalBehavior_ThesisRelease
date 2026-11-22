# structured_task_lifecycle_features.csv

**Source dataset:** Structured — Retrospective
**Source file:** `outputs/cleaned/structured_behavioral_clean.csv`
**Producing notebook:** `notebooks/17_structured_feature_extraction.ipynb`
**Producing module:** `src/features/structured_features.py::build_task_lifecycle_features`
**Rows:** 26,729
**Columns:** 33
**Unit of observation:** One task (all of its events grouped by `task_id`)

---

## What this file contains

One row per task, summarizing everything observable about that task's lifecycle within the export
window: how it was first seen, whether it was ever completed/uncompleted/deleted, how many times each
kind of field was edited, and its final known state. This is the primary input for Network Theory
(state-transition structure) and System Dynamics (stock/flow) model families, and a required input for
the completion-rate features in `structured_participant_features.csv`.

**Critical structural finding surfaced by this table (not visible during inspection/cleaning):**
60.7% of tasks (16,213/26,729) have `has_creation_event = False` — their first visible event is
`Task Updated` or `Task Deleted`, never `Task Created`. These tasks already existed before the
2026-03-01 extraction window started (consistent with these being existing users with pre-existing
task histories, matching the "retrospective" study framing). Full lifecycle reconstruction
(created → ... → resolved) is only possible for the 10,516 tasks with `has_creation_event = True`.
State-to-state transition *counting* (e.g. timed → moved → completed) remains valid for **all** tasks
regardless of censoring, but the entry point is **not** the only thing censoring removes: terminal
completion state is censoring-dependent too. `final_completed = None` (→ `lifecycle_status =
'unresolved'`) cannot distinguish "never completed" from "completed before 2026-03-01", and a censored
task only enters this export at all if it had an in-window event, which selects for activity. Direct
evidence: 31 tasks carry a `task_uncompleted` tag with no `task_completed` tag ever observed (11 of
them left-censored) — they were demonstrably completed before the window opened. Censored tasks show a
*higher* completed share than creation-visible tasks (71.2% vs 68.7%). Restrict completion-based
analyses to `has_creation_event == True`, or report both versions side by side.

---

## Column Reference

| Column | Type | Description |
|---|---|---|
| `task_id` | string (UUID) | Task identifier, matches `structured_behavioral_clean.csv` |
| `participant_id` | string (UUID) | Owning participant |
| `n_events` | int | Total events observed for this task |
| `n_created` / `n_updated` / `n_deleted` | int | Count of each event type for this task |
| `has_creation_event` | bool | False = left-censored (task pre-existed the window) |
| `first_event_type` | string | Event type of the first observed row for this task |
| `first_event_ts` / `last_event_ts` | datetime[UTC] | First/last observed event timestamps |
| `lifecycle_span_days` | float | Days between first and last observed event |
| `task_type_first` / `task_type_last` | string | Task type at first/last observed event |
| `type_changed_ever` | bool | Whether task_type differs between first and last observation |
| `ever_completed` | bool | Whether a `task_completed` update tag was ever seen |
| `ever_uncompleted` | bool | Whether a `task_uncompleted` update tag was ever seen (an "undo") |
| `final_completed` | bool / None | Last-transition-wins completion state; `None` if completion was never touched |
| `is_deleted` | bool | Whether a `Task Deleted` event was observed |
| `lifecycle_status` | string | `completed` / `deleted` / `unresolved` (see derivation logic below) |
| `n_reschedule_events` | int | Count of update events tagged `date_changed` and/or `start_time_changed` |
| `n_type_changes` | int | Count of update events tagged `type_changed` |
| `n_recurrence_changes` | int | Count of update events tagged `recurrence_changed` |
| `n_notes_changes` | int | Count of update events tagged `notes_changed` |
| `n_subtasks_changes` | int | Count of update events tagged `subtasks_changed` |
| `n_duration_changes` | int | Count of update events tagged `duration_changed` |
| `n_title_changes` | int | Count of update events tagged `title_changed` (title content itself is not exported — see `structured_behavioral_clean.md`) |
| `n_color_changes` / `n_icon_changes` | int | Count of cosmetic update events |
| `n_energy_level_change_events` | int | Count of update events tagged `energy_level_changed` — note: the *event* is logged but the *energy value itself* is never exported (not a column anywhere in this dataset) |
| `task_is_recurring_ever` | bool | True if `task_is_recurring` was True at any observed event |
| `subtasks_amount_last` | float | Subtask count at last observed event |
| `task_has_notes_last` | bool | Whether the task had notes at last observed event |
| `task_duration_min_last` | float | Duration in minutes at last observed event |

---

## Derivation Logic

**Completion (`final_completed`, `lifecycle_status`):** Uses last-transition-wins logic over
chronologically ordered `task_completed` / `task_uncompleted` tags — a task marked completed and
later uncompleted correctly resolves to its last known state, not "ever completed." Verified: 678/18,931
ever-completed tasks (3.6%) were later un-completed.

**`lifecycle_status` priority:** `deleted` takes priority over `completed` if a task was both completed
and later deleted (deletion is the terminal, unambiguous event); otherwise `completed` if
`final_completed is True`; otherwise `unresolved` (covers: never touched, or last known state is
not-completed).

**Tag matching:** Uses exact membership in the pipe-split `update_type_list_str`, not substring
matching — a naive substring check on the raw string would incorrectly match `subtask_completed`
(a different signal, about a subtask, not the task itself) as if it were `task_completed`. This bug
was caught and fixed during this extraction.

---

## Key Distributions

### `lifecycle_status` (task-level, pooled across all participants)
| Status | Count | % |
|---|---|---|
| completed | 18,773 | 70.2% |
| unresolved | 5,530 | 20.7% |
| deleted | 2,426 | 9.1% |

Note: this pooled distribution is dominated by high-volume participants; see
`structured_participant_features.md` for the per-participant mean (which differs — 48.9% / 39.5% /
11.6% — because task counts are highly skewed across participants).

---

## Known Limitations

- For left-censored tasks (60.7%), `task_type_first` reflects the type at first *observation*, not
  first *creation* — do not interpret it as the task's originally-assigned type.
- `n_energy_level_change_events` counts an event that fired, but there is no way to know what the
  energy level changed *to* or *from* — this column cannot support any energy-level-based model
  (Statistical Mechanics' proposed energy-level microstate dimension remains unavailable).
- `lifecycle_span_days = 0` for single-event tasks (most left-censored tasks touched only once).
- Completion derivation assumes `update_type` logging is complete and reliable; any missed/duplicate
  PostHog event would bias `final_completed`.

---

## How to Load

```python
import pandas as pd
from pathlib import Path

OUT = Path("outputs/features/structured")

tasks = pd.read_csv(OUT / "structured_task_lifecycle_features.csv",
                     parse_dates=["first_event_ts", "last_event_ts"])

# Fully-observed lifecycles only (creation event visible)
full_lifecycle = tasks[tasks["has_creation_event"]]

# Tasks that were completed and later un-completed
undone = tasks[tasks["ever_completed"] & tasks["ever_uncompleted"]]
```
