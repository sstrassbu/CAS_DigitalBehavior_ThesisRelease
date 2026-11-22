"""
structured_features.py
=======================
Task-lifecycle and participant-level feature extraction for the Structured
Retrospective dataset (task-planning app; independent of DS1-DS6 OneSec series).

Design decisions and dataset-specific notes
--------------------------------------------
- Two units of observation are extracted here, not one:
    1. Task-lifecycle level (one row per task_id) — the natural unit for Network
       Theory / System Dynamics state-transition work.
    2. Participant level (one row per participant_id) — aggregates task-lifecycle
       features plus event-level temporal structure.
- CRITICAL finding (discovered during this extraction, not during inspection):
    60.7% of tasks (16,213 / 26,729) are LEFT-CENSORED — their first visible event
    is "Task Updated" or "Task Deleted", never "Task Created". These tasks already
    existed before the 2026-03-01 extraction window started (consistent with this
    being existing users' pre-existing task histories, not fresh signups). Full
    lifecycle reconstruction (created -> ... -> resolved) is only possible for the
    10,516 tasks with has_creation_event == True. Transition-level *counting*
    (state X -> state Y within the window) remains valid for ALL tasks, but the
    "entry point" / creation channel is NOT the only thing censoring removes
    (F030): terminal completion state is censoring-dependent too — see the
    completion note below and the caveat on pct_tasks_completed in
    build_structured_participant_features.
- Task completion is NOT a stored column. It is derived from update_type events:
    'task_completed' / 'task_uncompleted' tags, using LAST-TRANSITION-WINS logic
    (a task can be completed then un-completed later — 678/18,931 ever-completed
    tasks, 3.6%, show this "undo" pattern; a further 31 tasks carry only a
    'task_uncompleted' tag and no 'task_completed' tag, i.e. they were completed
    before the extraction window opened, F205). Naive "ever completed" would
    overcount.
- 'subtask_completed' / 'subtask_uncompleted' are a DIFFERENT signal (a subtask
  within the task, not the task itself) and must not be conflated with task-level
  completion (a naive substring match on the raw string does conflate them --
  verified and fixed here; use exact tag membership only).
- task_energy_level, task_alerts, and task category/topic are NOT available in
  this export despite being documented in the partial codebook or consent text --
  no feature here references them.
- Output tables:
    1. structured_task_lifecycle_features.csv — one row per task_id (~26,729)
    2. structured_participant_features.csv     — one row per participant (61, all
       with behavioral data)
    3. structured_survey_features.csv          — one row per participant with a
       survey response, restricted to behavioral-linked participants

Run via: notebooks/17_structured_feature_extraction.ipynb
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

from src.features.behavioral_features import (
    CLOCK_LOCAL,
    volume_features,
    temporal_features,
    hour_entropy,
)

COMPLETION_TAG = "task_completed"
UNCOMPLETION_TAG = "task_uncompleted"
RESCHEDULE_TAGS = {"date_changed", "start_time_changed"}


def _tags(list_str) -> list[str]:
    """Split a pipe-joined update_type_list_str into exact tags. Empty list for NaN/empty."""
    if pd.isna(list_str) or list_str == "":
        return []
    return list_str.split("|")


def _local_naive_timestamps(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp_utc",
    timezone_col: str = "event_timezone",
) -> pd.Series:
    """
    Convert UTC event timestamps to participant-LOCAL naive wall-clock time.

    F124: Structured logs a per-event IANA `event_timezone` (45 distinct values,
    present on 99.99% of rows; 24/61 participants span more than one zone), so the
    UTC offset is not even constant within a participant. Time-of-day and weekday
    constructs are only meaningful on this local clock — and because the offset
    varies, hour_entropy is NOT permutation-invariant here either and must also be
    computed on local time. Same tz_convert pattern already used in notebooks
    61/62/63/66/68; Stage 1 was the inconsistent layer.

    Parameters
    ----------
    df : DataFrame
        Event rows with a tz-aware UTC datetime column and an IANA timezone column.

    Returns
    -------
    Series of tz-naive local datetimes, aligned to df.index.
    """
    parts = []
    for tz_name, block in df.groupby(timezone_col, dropna=False):
        ts = block[timestamp_col]
        if isinstance(tz_name, str) and tz_name:
            parts.append(ts.dt.tz_convert(tz_name).dt.tz_localize(None))
        else:
            # ~0.01% of rows carry no event_timezone -- fall back to UTC wall clock.
            parts.append(ts.dt.tz_localize(None))
    return pd.concat(parts).reindex(df.index)


# ---------------------------------------------------------------------------
# 1. Task-lifecycle level features (one row per task_id)
# ---------------------------------------------------------------------------

def build_task_lifecycle_features(beh: pd.DataFrame) -> pd.DataFrame:
    """
    Build one row per task_id summarizing its observed lifecycle.

    Type: DIRECT (event counts, timestamps) / DIRECT-DERIVED (completion state,
    reschedule/edit counts via last-transition-wins and exact tag matching)
    Confidence: High for event counts; Medium for final_completed (depends on
    completion tags being logged reliably) and for tasks with has_creation_event
    == False (lifecycle is only partially observed for these).

    Parameters
    ----------
    beh : DataFrame
        structured_behavioral_clean.csv, with event_timestamp_utc parsed as datetime.

    Returns
    -------
    DataFrame, one row per task_id, columns:
        participant_id, n_events, n_created, n_updated, n_deleted,
        has_creation_event, first_event_type, first_event_ts, last_event_ts,
        lifecycle_span_days, task_type_first, task_type_last, type_changed_ever,
        ever_completed, ever_uncompleted, final_completed, is_deleted,
        lifecycle_status, n_reschedule_events, n_type_changes, n_recurrence_changes,
        n_notes_changes, n_subtasks_changes, n_duration_changes, n_title_changes,
        n_color_changes, n_icon_changes, n_energy_level_change_events,
        task_is_recurring_ever, subtasks_amount_last, task_has_notes_last,
        task_duration_min_last
    """
    beh = beh.sort_values(["task_id", "event_timestamp_utc"]).copy()

    records = []
    for task_id, grp in beh.groupby("task_id", sort=False):
        grp = grp.reset_index(drop=True)
        n = len(grp)
        first_row = grp.iloc[0]
        last_row = grp.iloc[-1]

        first_ts = grp["event_timestamp_utc"].min()
        last_ts = grp["event_timestamp_utc"].max()
        span_days = (last_ts - first_ts).total_seconds() / 86400.0

        n_created = int((grp["event_type"] == "Task Created").sum())
        n_updated = int((grp["event_type"] == "Task Updated").sum())
        n_deleted_events = int((grp["event_type"] == "Task Deleted").sum())
        has_creation_event = n_created > 0
        is_deleted = n_deleted_events > 0

        # Completion: last-transition-wins among task_completed/task_uncompleted tags,
        # in chronological order (grp is already sorted by event_timestamp_utc).
        completion_state = None  # None = never touched; True/False = last known state
        ever_completed = False
        ever_uncompleted = False
        n_reschedule = 0
        n_type_change = 0
        n_recurrence_change = 0
        n_notes_change = 0
        n_subtasks_change = 0
        n_duration_change = 0
        n_title_change = 0
        n_color_change = 0
        n_icon_change = 0
        n_energy_change_events = 0

        for list_str in grp["update_type_list_str"]:
            tags = _tags(list_str)
            if COMPLETION_TAG in tags:
                completion_state = True
                ever_completed = True
            if UNCOMPLETION_TAG in tags:
                completion_state = False
                ever_uncompleted = True
            if RESCHEDULE_TAGS & set(tags):
                n_reschedule += 1
            if "type_changed" in tags:
                n_type_change += 1
            if "recurrence_changed" in tags:
                n_recurrence_change += 1
            if "notes_changed" in tags:
                n_notes_change += 1
            if "subtasks_changed" in tags:
                n_subtasks_change += 1
            if "duration_changed" in tags:
                n_duration_change += 1
            if "title_changed" in tags:
                n_title_change += 1
            if "color_changed" in tags:
                n_color_change += 1
            if "icon_changed" in tags:
                n_icon_change += 1
            if "energy_level_changed" in tags:
                n_energy_change_events += 1

        final_completed = completion_state  # None / True / False

        # F030: 'unresolved' merges "never completed" with "completed before the
        # 2026-03-01 window opened" — final_completed is None for every task whose
        # completion transition happened out of window. Deliberately NOT relabelled
        # here (every downstream consumer keys on these three literals); restrict
        # completion analyses to has_creation_event == True instead.
        if is_deleted:
            lifecycle_status = "deleted"
        elif final_completed is True:
            lifecycle_status = "completed"
        else:
            lifecycle_status = "unresolved"

        records.append({
            "task_id": task_id,
            "participant_id": first_row["participant_id"],
            "n_events": n,
            "n_created": n_created,
            "n_updated": n_updated,
            "n_deleted": n_deleted_events,
            "has_creation_event": has_creation_event,
            "first_event_type": first_row["event_type"],
            "first_event_ts": first_ts,
            "last_event_ts": last_ts,
            "lifecycle_span_days": round(span_days, 3),
            "task_type_first": first_row["task_type"],
            "task_type_last": last_row["task_type"],
            "type_changed_ever": first_row["task_type"] != last_row["task_type"],
            "ever_completed": ever_completed,
            "ever_uncompleted": ever_uncompleted,
            "final_completed": final_completed,
            "is_deleted": is_deleted,
            "lifecycle_status": lifecycle_status,
            "n_reschedule_events": n_reschedule,
            "n_type_changes": n_type_change,
            "n_recurrence_changes": n_recurrence_change,
            "n_notes_changes": n_notes_change,
            "n_subtasks_changes": n_subtasks_change,
            "n_duration_changes": n_duration_change,
            "n_title_changes": n_title_change,
            "n_color_changes": n_color_change,
            "n_icon_changes": n_icon_change,
            "n_energy_level_change_events": n_energy_change_events,
            "task_is_recurring_ever": bool(grp["task_is_recurring"].any()),
            "subtasks_amount_last": last_row["subtasks_amount"],
            "task_has_notes_last": last_row["task_has_notes"],
            "task_duration_min_last": last_row["task_duration_min"],
        })

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# 2. Participant-level features (aggregated from task lifecycle + raw events)
# ---------------------------------------------------------------------------

def build_structured_participant_features(
    beh: pd.DataFrame,
    task_lifecycle: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build one row per participant, aggregating task-lifecycle outcomes and
    event-level temporal structure.

    Type: DIRECT / DIRECT-DERIVED (see task-lifecycle docstring for completion
    derivation caveats)
    Confidence: High for volume/type-share features; Medium for completion and
    reschedule rates (depend on has_creation_event coverage varying by participant)

    Feature groups:
      G1 Volume and activity        — DIRECT, High (via shared volume_features)
      G2 Task outcome composition   — DIRECT-DERIVED, Medium (completed/deleted/unresolved
         shares; F030: censoring-dependent — computed over ALL tasks including the 60.7%
         left-censored ones, whose pre-window completion state is unobservable.
         corr(pct_tasks_left_censored, pct_tasks_completed) = +0.357 across the 61
         participants; mean pct_tasks_completed is 0.489 over all tasks vs 0.391 restricted
         to has_creation_event == True)
      G3 Task type composition      — DIRECT, High (timed/all_day/inbox shares, task-level)
      G4 Editing / reschedule behavior — DIRECT-DERIVED, Medium-High
      G5 Structure use              — DIRECT, High (recurrence, notes, subtasks)
      G6 Temporal structure         — DIRECT-DERIVED, High (via shared temporal_features,
         hour_entropy, on the participant-LOCAL clock built from per-event event_timezone;
         F124 — the *_local column names mark the change from the earlier UTC version)
      G7 Subscription / censoring   — DIRECT, High
    """
    beh = beh.copy()
    beh["timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], utc=True)

    records = []
    for pid, grp in beh.groupby("participant_id"):
        grp = grp.sort_values("timestamp_utc")
        tasks = task_lifecycle[task_lifecycle["participant_id"] == pid]
        n_tasks = len(tasks)

        feats = {"participant_id": pid}

        # G1 volume (shared utility)
        feats.update(volume_features(grp))
        feats["n_unique_tasks"] = n_tasks
        feats["n_created_events"] = int((grp["event_type"] == "Task Created").sum())
        feats["n_updated_events"] = int((grp["event_type"] == "Task Updated").sum())
        feats["n_deleted_events"] = int((grp["event_type"] == "Task Deleted").sum())

        # G2 task outcome composition (task-level, not event-level)
        if n_tasks > 0:
            status_counts = tasks["lifecycle_status"].value_counts()
            feats["pct_tasks_completed"] = round(float(status_counts.get("completed", 0) / n_tasks), 4)
            feats["pct_tasks_deleted"] = round(float(status_counts.get("deleted", 0) / n_tasks), 4)
            feats["pct_tasks_unresolved"] = round(float(status_counts.get("unresolved", 0) / n_tasks), 4)
            feats["pct_tasks_ever_uncompleted"] = round(float(tasks["ever_uncompleted"].mean()), 4)
            feats["pct_tasks_left_censored"] = round(float((~tasks["has_creation_event"]).mean()), 4)
        else:
            feats["pct_tasks_completed"] = np.nan
            feats["pct_tasks_deleted"] = np.nan
            feats["pct_tasks_unresolved"] = np.nan
            feats["pct_tasks_ever_uncompleted"] = np.nan
            feats["pct_tasks_left_censored"] = np.nan

        # G3 task type composition (task-level, using last-known type)
        if n_tasks > 0:
            type_counts = tasks["task_type_last"].value_counts(normalize=True)
            feats["share_task_type_timed"] = round(float(type_counts.get("timed", 0.0)), 4)
            feats["share_task_type_all_day"] = round(float(type_counts.get("all_day", 0.0)), 4)
            feats["share_task_type_inbox"] = round(float(type_counts.get("inbox", 0.0)), 4)
        else:
            feats["share_task_type_timed"] = np.nan
            feats["share_task_type_all_day"] = np.nan
            feats["share_task_type_inbox"] = np.nan

        # G4 editing / reschedule behavior
        if n_tasks > 0:
            feats["mean_events_per_task"] = round(float(tasks["n_events"].mean()), 3)
            n_update_events = feats["n_updated_events"]
            feats["reschedule_rate"] = (
                round(float(tasks["n_reschedule_events"].sum() / n_update_events), 4)
                if n_update_events > 0 else np.nan
            )
            feats["mean_type_changes_per_task"] = round(float(tasks["n_type_changes"].mean()), 4)
        else:
            feats["mean_events_per_task"] = np.nan
            feats["reschedule_rate"] = np.nan
            feats["mean_type_changes_per_task"] = np.nan

        # G5 structure use
        if n_tasks > 0:
            feats["recurrence_use_rate"] = round(float(tasks["task_is_recurring_ever"].mean()), 4)
            feats["notes_use_rate"] = round(float(tasks["task_has_notes_last"].mean()), 4)
            feats["mean_subtasks_amount"] = round(float(tasks["subtasks_amount_last"].mean()), 3)
        else:
            feats["recurrence_use_rate"] = np.nan
            feats["notes_use_rate"] = np.nan
            feats["mean_subtasks_amount"] = np.nan

        # G6 temporal structure (shared utilities), on the participant's LOCAL clock.
        # F124: previously scored on timestamp_utc, which made peak_hour wrong for
        # 60/61 participants (mean |diff| 0.197 morning share, 0.162 evening,
        # 0.043 weekend) and shifted hour_entropy by >0.01 bits for 26/61.
        # Columns are renamed with a _local suffix so the semantic change is visible
        # rather than silently altering same-named values.
        grp = grp.copy()
        grp["timestamp_local_naive"] = _local_naive_timestamps(grp, "timestamp_utc")
        temporal = temporal_features(grp, "timestamp_local_naive", clock=CLOCK_LOCAL)
        feats.update({
            "peak_hour_local": temporal["peak_hour_of_day"],
            "weekend_event_share_local": temporal["weekend_event_share"],
            "evening_event_share_local": temporal["evening_event_share"],
            "morning_event_share_local": temporal["morning_event_share"],
            "temporal_clock": temporal["temporal_clock"],
        })
        feats["hour_entropy_local"] = hour_entropy(grp, "timestamp_local_naive")["hour_entropy"]

        # G7 subscription / censoring
        feats["subscription_type_last"] = grp["subscription_type_at_event"].iloc[-1]
        feats["subscription_changed"] = grp["subscription_type_at_event"].nunique() > 1
        feats["days_observed"] = round(float(grp["days_since_first_event"].max()), 3)

        records.append(feats)

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# 3. Survey features (behavior-linked participants only)
# ---------------------------------------------------------------------------

SURVEY_FEATURE_COLS = [
    "consent_given", "is_finished", "age", "gender", "structured_use_duration",
    "life_happiness_score", "productivity_happiness_score",
    "pct_tasks_planned_num", "pct_planned_tasks_completed_num",
    "productivity_importance_general_score", "productivity_importance_personal_score",
    "productivity_rating_vs_others_score",
    "autism_status", "adhd_status",
    "asrs_1_finish_details_score", "asrs_2_organization_score",
    "asrs_3_remembering_score", "asrs_4_avoid_delay_score",
    "asrs_5_fidget_score", "asrs_6_overactive_score",
]


def build_structured_survey_features(
    surv: pd.DataFrame,
    behavioral_ids: set,
) -> pd.DataFrame:
    """
    Restrict the cleaned survey to behavioral-linked participants and select
    the analysis-relevant columns.

    Type: DIRECT (demographics, single-item ratings) / self-report screener
    (ASRS items — not diagnostic; see structured_survey_clean.md)
    Confidence: Medium — rows are NOT pre-filtered on consent_given/is_finished;
    callers must filter explicitly (consistent with structured_survey_clean.csv
    convention of preserving all rows with flags rather than deleting)

    Returns
    -------
    DataFrame with participant_id + SURVEY_FEATURE_COLS, restricted to
    participants who also have behavioral data (61 rows expected).
    """
    linked = surv[surv["participant_id"].isin(behavioral_ids)].copy()
    cols = ["participant_id"] + SURVEY_FEATURE_COLS
    return linked[cols].reset_index(drop=True)


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_structured_files(cleaned_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all Structured cleaned files. Returns (beh, surv, linkage)."""
    beh = pd.read_csv(cleaned_dir / "structured_behavioral_clean.csv")
    beh["event_timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], format="mixed", utc=True)
    surv = pd.read_csv(cleaned_dir / "structured_survey_clean.csv")
    linkage = pd.read_csv(cleaned_dir / "structured_participant_linkage.csv")
    return beh, surv, linkage
