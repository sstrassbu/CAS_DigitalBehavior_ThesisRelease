"""
behavioral_features.py
======================
Shared utility functions for participant-level feature extraction.

Used by ds1_features.py, ds4_features.py, ds5_features.py, ds6_features.py.

All functions:
- accept a DataFrame of behavioral events filtered to one participant
- return a flat dict of scalar features
- are stateless and pure (no side effects)

Design rules:
- Feature functions are composable: each computes one conceptual group
- All functions document their confidence level and proxy status in docstrings
- NaN is returned for any feature that cannot be computed (insufficient data)
- No cross-dataset harmonization is performed here

Event classes (added 2026-08-08, findings F001 / F003 / F213)
------------------------------------------------------------
OneSec-style logs mix two structurally different record types in the same
outcome column:

* FRICTION DECISIONS  ('opened', 'dismissed') — the participant met the friction
  screen and chose. These are the only rows that carry override/compliance
  information.
* SESSION TERMINATIONS ('closed') — an app-CLOSE record emitted after an
  'opened' (median ~100 s later in DS1). A close is NOT evidence of "not
  opening"; it is evidence that an open happened and then ended. Close logging
  is a per-device/per-participant configuration (only 126 of 619 DS1
  participants log it at all), so pooling it into a rate denominator encodes
  logging configuration, not behavior.

Friction rates are therefore computed on friction-decision rows only, and
`closed` is reported separately as a count plus a logging-share rate.

Local-clock requirement (finding F029 / F208)
---------------------------------------------
`temporal_features()` produces LOCAL-clock constructs ("evening", "morning",
peak hour). It now requires the caller to state explicitly, via the keyword-only
`clock` argument, whether the timestamp column it is given is a participant-local
clock or a UTC fallback. There is no default: a caller with no local clock must
say so, rather than silently receiving a wrong-by-an-unknown-offset answer.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Optional


# ---------------------------------------------------------------------------
# Event-class vocabulary (F001 / F003 / F213)
# ---------------------------------------------------------------------------

#: Rows on which the participant actually made a friction-moment choice.
FRICTION_DECISION_OUTCOMES: frozenset = frozenset({"opened", "dismissed"})

#: Rows that terminate a session already started by an 'opened' event.
SESSION_TERMINATION_OUTCOMES: frozenset = frozenset({"closed"})

#: Labels that carry no outcome information at all.
NON_OUTCOME_LABELS: frozenset = frozenset({"missing"})

#: Event-class names returned by classify_outcome_events().
EVENT_CLASS_DECISION = "friction_decision"
EVENT_CLASS_TERMINATION = "session_termination"
EVENT_CLASS_OTHER = "other_outcome"
EVENT_CLASS_NONE = "no_outcome"

#: Accepted values for temporal_features(..., clock=...)  (F029)
CLOCK_LOCAL = "local"
CLOCK_UTC_FALLBACK = "utc_no_local_clock_available"
_VALID_CLOCKS = (CLOCK_LOCAL, CLOCK_UTC_FALLBACK)


def classify_outcome_events(
    df: pd.DataFrame,
    outcome_col: str = "event_outcome_simple",
    decision_outcomes: frozenset = FRICTION_DECISION_OUTCOMES,
    termination_outcomes: frozenset = SESSION_TERMINATION_OUTCOMES,
) -> pd.Series:
    """
    Label each event row with its structural event class.

    Type: DIRECT
    Confidence: High
    Minimum data: none (works on an empty frame)

    Why (F001/F003/F213): 'closed' is an app-close record, not a friction-moment
    decision. Every function that computes a friction rate or an override run
    must separate the two classes rather than pooling them on "not missing".

    Parameters
    ----------
    df : DataFrame
        Event-level rows for one participant.
    outcome_col : str
        Column holding the simplified outcome label.
    decision_outcomes, termination_outcomes : frozenset
        Overridable label vocabularies (e.g. a dataset that wants
        'dismissed_other' treated as a decision passes an extended set).

    Returns
    -------
    pd.Series of str, index-aligned with `df`, values in
    {'friction_decision', 'session_termination', 'other_outcome', 'no_outcome'}.
    """
    if len(df) == 0:
        return pd.Series([], dtype=object, index=df.index)

    outcome = df[outcome_col]
    cls = pd.Series(EVENT_CLASS_OTHER, index=df.index, dtype=object)
    cls[outcome.isna() | outcome.isin(NON_OUTCOME_LABELS)] = EVENT_CLASS_NONE
    cls[outcome.isin(decision_outcomes)] = EVENT_CLASS_DECISION
    cls[outcome.isin(termination_outcomes)] = EVENT_CLASS_TERMINATION
    return cls


# ---------------------------------------------------------------------------
# Volume and activity
# ---------------------------------------------------------------------------

#: Rates estimated from a sub-day span are 1/window amplification, not per-day
#: rates (F034 / F118 / F123): without this floor a 2-event, 2-second DS1 record
#: returned 86,400 events/day.
MIN_WINDOW_DAYS: float = 1.0


def volume_features(df: pd.DataFrame) -> dict:
    """
    Compute basic volume and observation-window features.

    Type: DIRECT
    Confidence: High
    Minimum data: >= 1 event row

    Parameters
    ----------
    df : DataFrame
        Event-level rows for one participant.
        Required columns: timestamp_utc (datetime, UTC)

    Returns
    -------
    dict with keys:
        total_events, n_days_observed, obs_window_days,
        obs_window_calendar_days, events_per_day, active_days_per_week

    Notes
    -----
    * `events_per_day` is NaN when the whole record spans less than
      MIN_WINDOW_DAYS (F034 / F118 / F123).
    * `active_days_per_week` uses an inclusive calendar-date denominator, on the
      same grid as its numerator, so it is bounded by 7 by construction
      (F035 / F048 / F117).
    """
    n = len(df)
    empty = {
        "total_events": n,
        "n_days_observed": np.nan,
        "obs_window_days": np.nan,
        "obs_window_calendar_days": np.nan,
        "events_per_day": np.nan,
        "active_days_per_week": np.nan,
    }
    if n == 0:
        empty["total_events"] = 0
        return empty

    ts = df["timestamp_utc"].dropna()
    if len(ts) == 0:
        return empty

    dates = ts.dt.date
    n_days_obs = dates.nunique()
    first = ts.min()
    last = ts.max()
    window = (last - first).total_seconds() / 86400.0  # days

    # Inclusive count of calendar dates spanned, first..last (F035/F048/F117).
    n_calendar_days = (last.date() - first.date()).days + 1

    # F034/F118/F123: no rate from a sub-day window.
    events_per_day = n / window if window >= MIN_WINDOW_DAYS else np.nan

    # F035/F048/F117: numerator is a distinct-calendar-date count, so the
    # denominator must be a calendar-date count too (a fractional elapsed-day
    # denominator let this exceed its own logical maximum of 7 for 1,279 of
    # 2,535 shipped participant rows). Eligibility is gated on the same grid.
    active_days_per_week = (
        7.0 * n_days_obs / n_calendar_days if n_calendar_days >= 7 else np.nan
    )

    return {
        "total_events": n,
        "n_days_observed": n_days_obs,
        "obs_window_days": round(window, 2),
        "obs_window_calendar_days": int(n_calendar_days),
        "events_per_day": round(events_per_day, 4) if not np.isnan(events_per_day) else np.nan,
        "active_days_per_week": round(active_days_per_week, 4) if not np.isnan(active_days_per_week) else np.nan,
    }


# ---------------------------------------------------------------------------
# Outcome distribution
# ---------------------------------------------------------------------------

def outcome_features(
    df: pd.DataFrame,
    outcome_col: str = "event_outcome_simple",
    decision_outcomes: frozenset = FRICTION_DECISION_OUTCOMES,
    include_rate_not_opened: bool = True,
) -> dict:
    """
    Compute intervention outcome distribution features.

    Type: DIRECT
    Confidence: High
    Minimum data: >= 1 outcome-bearing row (outcome_col not NaN / not 'missing')

    F001 / F213 (2026-08-08): the friction rates are computed on FRICTION-DECISION
    rows only. 'closed' is an app-close record emitted after an 'opened' (median
    ~100 s later in DS1) and is logged for only 126 of 619 DS1 participants; it
    was previously in the denominator of every rate AND in the numerator of
    `rate_not_opened`, i.e. a close was counted as evidence of NOT opening.
    `n_closed` is kept as a separate session-termination count, and `rate_closed`
    is redefined as a LOGGING-CONFIGURATION share (closes / all outcome-bearing
    rows), not a friction outcome.

    F200: labels outside the decision and termination vocabularies (DS4/DS5
    'dismissed_other') previously entered the denominator but no numerator, so the
    rates did not partition. They are now reported separately as
    `n_other_outcome` / `rate_other_outcome` and are excluded from the friction
    denominator. A dataset that wants such a label treated as a decision passes it
    in `decision_outcomes`.

    DS6 WARNING: DS6 has only 'opened' outcomes in this column.
    Do not treat DS6 outcome rates as equivalent to DS1/DS4/DS5 outcome rates.
    Use this function for DS6 only to document its single-outcome structure.

    Parameters
    ----------
    df : DataFrame
        Must contain `outcome_col`.
    decision_outcomes : frozenset
        Labels that count as a friction-moment decision. Denominator of
        rate_opened / rate_dismissed / rate_not_opened.
    include_rate_not_opened : bool
        Once closes are out of the numerator, `rate_not_opened` is by construction
        `1 - rate_opened` and, for the default two-label decision set, numerically
        identical to `rate_dismissed`. DS1 drops it per the user decision on
        record; DS5 keeps it because GaT's `commitment_score` is defined on it.

    Returns
    -------
    dict with keys:
        n_outcome_bearing, n_friction_decisions, n_opened, n_dismissed, n_closed,
        n_other_outcome, rate_opened, rate_dismissed, rate_closed,
        rate_other_outcome, modal_outcome
        (+ rate_not_opened unless include_rate_not_opened is False)
    """
    empty = {
        "n_outcome_bearing": 0,
        "n_friction_decisions": 0,
        "n_opened": np.nan,
        "n_dismissed": np.nan,
        "n_closed": np.nan,
        "n_other_outcome": np.nan,
        "rate_opened": np.nan,
        "rate_dismissed": np.nan,
        "rate_closed": np.nan,
        "rate_other_outcome": np.nan,
        "rate_not_opened": np.nan,
        "modal_outcome": np.nan,
    }
    if not include_rate_not_opened:
        empty.pop("rate_not_opened")

    event_class = classify_outcome_events(df, outcome_col, decision_outcomes=decision_outcomes)
    bearing = df[event_class != EVENT_CLASS_NONE]
    n_bearing = len(bearing)

    if n_bearing == 0:
        return empty

    decisions = df[event_class == EVENT_CLASS_DECISION]
    n_decisions = len(decisions)
    n_closed = int((event_class == EVENT_CLASS_TERMINATION).sum())
    n_other = int((event_class == EVENT_CLASS_OTHER).sum())

    counts = decisions[outcome_col].value_counts()
    n_opened = int(counts.get("opened", 0))
    n_dismissed = int(counts.get("dismissed", 0))

    # F200: the four classes must exhaust the outcome-bearing rows, otherwise a
    # rate silently stops partitioning again.
    assert n_decisions + n_closed + n_other == n_bearing, (
        "outcome event classes do not partition the outcome-bearing rows"
    )

    feats = {
        "n_outcome_bearing": n_bearing,
        "n_friction_decisions": n_decisions,
        "n_opened": n_opened,
        "n_dismissed": n_dismissed,
        "n_closed": n_closed,
        "n_other_outcome": n_other,
        # Friction rates: friction-decision denominator only (F001).
        "rate_opened": round(n_opened / n_decisions, 4) if n_decisions else np.nan,
        "rate_dismissed": round(n_dismissed / n_decisions, 4) if n_decisions else np.nan,
        # Logging-configuration shares: denominator is all outcome-bearing rows.
        "rate_closed": round(n_closed / n_bearing, 4),
        "rate_other_outcome": round(n_other / n_bearing, 4),
        "modal_outcome": bearing[outcome_col].mode().iloc[0],
    }
    if include_rate_not_opened:
        # = 1 - rate_opened over decision rows; closes are NOT "not opened" (F001).
        feats["rate_not_opened"] = (
            round((n_decisions - n_opened) / n_decisions, 4) if n_decisions else np.nan
        )
    return feats


# ---------------------------------------------------------------------------
# App structure
# ---------------------------------------------------------------------------

def app_structure_features(df: pd.DataFrame, app_col: str = "app_name") -> dict:
    """
    Compute app diversity and concentration features.

    Type: DIRECT
    Confidence: High
    Minimum data: >= 1 row with non-NaN app_col

    Returns
    -------
    dict with keys:
        n_unique_apps, top_app, top_app_share, top3_app_share,
        app_herfindahl, app_entropy
    """
    valid = df[df[app_col].notna()]
    n = len(valid)

    if n == 0:
        return {
            "n_unique_apps": 0,
            "top_app": np.nan,
            "top_app_share": np.nan,
            "top3_app_share": np.nan,
            "app_herfindahl": np.nan,
            "app_entropy": np.nan,
        }

    counts = valid[app_col].value_counts()
    shares = counts / n

    top_app = counts.index[0]
    top_app_share = float(shares.iloc[0])
    top3_share = float(shares.iloc[:3].sum())
    herfindahl = float((shares ** 2).sum())
    entropy = float(-(shares * np.log2(shares + 1e-12)).sum())

    return {
        "n_unique_apps": int(counts.shape[0]),
        "top_app": top_app,
        "top_app_share": round(top_app_share, 4),
        "top3_app_share": round(top3_share, 4),
        "app_herfindahl": round(herfindahl, 4),
        "app_entropy": round(entropy, 4),
    }


# ---------------------------------------------------------------------------
# Temporal / context structure
# ---------------------------------------------------------------------------

def temporal_features(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp_utc",
    *,
    clock: str,
) -> dict:
    """
    Compute temporal activity pattern features.

    Type: DIRECT-DERIVED (from timestamp_col)
    Confidence: High on a local clock; LOW for peak/evening/morning on UTC
    Minimum data: >= 2 rows with a non-NaT timestamp

    F029 / F208 / F047: `peak_hour_of_day`, `evening_event_share` (18-23) and
    `morning_event_share` (6-11) are LOCAL-clock constructs. Computing them on
    UTC shifts every participant's hour axis by an unknown offset (DS5's German
    and DS6's Danish cohorts were both being scored on UTC even though both ship
    a local clock; DS6's stored peak hour matched the local peak for only 2.07%
    of participants). `clock` is therefore keyword-only and REQUIRED: a caller
    with no local clock must say so explicitly instead of silently getting a
    wrong answer.

    Parameters
    ----------
    timestamp_col : str
        Datetime column to score. Must be the LOCAL clock when clock='local'.
    clock : {'local', 'utc_no_local_clock_available'}
        Declaration of what `timestamp_col` actually is.
        - 'local': a participant-local wall clock (DS5 `event_timestamp_local`,
          DS6 Europe/Copenhagen, Structured per-event `event_timezone`).
        - 'utc_no_local_clock_available': the dataset has no local clock at all
          (DS1, DS4). The three hour-axis features are then NOT comparable across
          participants and must be read with that caveat; `weekend_event_share`
          is only mildly affected and `hour_entropy` is shift-invariant.

    Returns
    -------
    dict with keys:
        peak_hour_of_day, weekend_event_share, evening_event_share,
        morning_event_share, temporal_clock
    """
    if clock not in _VALID_CLOCKS:
        raise ValueError(
            f"temporal_features(clock=...) must be one of {_VALID_CLOCKS}; got {clock!r}. "
            "State explicitly whether the timestamp column is a local clock (F029)."
        )

    # Provenance stamp so the saved feature table records which clock was used.
    clock_stamp = f"{clock}:{timestamp_col}"
    empty = {
        "peak_hour_of_day": np.nan,
        "weekend_event_share": np.nan,
        "evening_event_share": np.nan,
        "morning_event_share": np.nan,
        "temporal_clock": clock_stamp,
    }
    if len(df) < 2:
        return empty

    ts = df[timestamp_col].dropna()
    n = len(ts)
    if n < 2:
        return empty

    hour = ts.dt.hour
    dow = ts.dt.dayofweek  # Monday=0, Sunday=6

    # F204/F207: deterministic tie-break — lowest hour wins. pandas' value_counts
    # tie order is hash-dependent, so an identical no-op re-run could change this
    # column (17/502 DS5 participants, 1/61 Structured).
    peak_hour = int(hour.value_counts().sort_index().idxmax())
    weekend_share = round(float((dow >= 5).sum() / n), 4)
    evening_share = round(float(((hour >= 18) & (hour <= 23)).sum() / n), 4)
    morning_share = round(float(((hour >= 6) & (hour <= 11)).sum() / n), 4)

    return {
        "peak_hour_of_day": peak_hour,
        "weekend_event_share": weekend_share,
        "evening_event_share": evening_share,
        "morning_event_share": morning_share,
        "temporal_clock": clock_stamp,
    }


# ---------------------------------------------------------------------------
# Longitudinal adaptation (generic tertile split)
# ---------------------------------------------------------------------------

#: Minimum rows in EACH third before its outcome rate is reported (F120 / F129).
MIN_ROWS_PER_THIRD: int = 5


def adaptation_tertile_features(
    df: pd.DataFrame,
    time_col: str,
    outcome_col: str = "event_outcome_simple",
) -> dict:
    """
    Proxy for behavioral adaptation: compare outcome rates in early vs late
    thirds of the observation window (split by time_col values).

    Type: PROXY
    Confidence: Medium
    Proxy note: Change in outcome rates is consistent with adaptation but
    could also reflect attrition, changing app mix, or life context shifts.
    Minimum data: >= 10 outcome-bearing rows with non-NaN time_col

    Parameters
    ----------
    time_col : str
        Column with numeric forward-counting time (e.g. days_since_first_event,
        secondsSinceOneSecSetup). All-NaN or fewer than 10 rows returns NaN.

    Returns
    -------
    dict with keys:
        open_rate_early_third, open_rate_late_third, open_rate_change,
        dismiss_rate_early_third, dismiss_rate_late_third, dismiss_rate_change,
        n_rows_adaptation_eligible, n_early_third, n_late_third

    Notes
    -----
    F120 / F129: the thirds are cut on the TIME axis, not on row quantiles, so
    they can hold wildly unequal event counts. DS5's largest saved adaptation
    signal (open_rate_change = +0.9340) came from a participant with 706
    outcome-bearing events whose late third held 3. Each third now needs at least
    MIN_ROWS_PER_THIRD rows, and both third sizes are exported so downstream users
    can filter further.
    """
    sub = df[df[time_col].notna() & df[outcome_col].notna() & (df[outcome_col] != "missing")].copy()
    n = len(sub)

    empty = {
        "open_rate_early_third": np.nan,
        "open_rate_late_third": np.nan,
        "open_rate_change": np.nan,
        "dismiss_rate_early_third": np.nan,
        "dismiss_rate_late_third": np.nan,
        "dismiss_rate_change": np.nan,
        "n_rows_adaptation_eligible": n,
        # NaN, not 0: the thirds were never cut for these participants, so "0 rows
        # in the early third" would be a false statement about the data.
        "n_early_third": np.nan,
        "n_late_third": np.nan,
    }

    if n < 10:
        return empty

    t_min = sub[time_col].min()
    t_max = sub[time_col].max()
    span = t_max - t_min
    if span == 0:
        return empty

    third = span / 3.0
    early = sub[sub[time_col] <= t_min + third]
    late = sub[sub[time_col] >= t_max - third]

    def _rate(portion, outcome):
        # F120/F129: a rate over fewer than MIN_ROWS_PER_THIRD rows is 0 or 1 by
        # construction and entered open_rate_change with full weight.
        if len(portion) < MIN_ROWS_PER_THIRD:
            return np.nan
        return round(float((portion[outcome_col] == outcome).sum() / len(portion)), 4)

    open_early = _rate(early, "opened")
    open_late = _rate(late, "opened")
    dis_early = _rate(early, "dismissed")
    dis_late = _rate(late, "dismissed")

    return {
        "open_rate_early_third": open_early,
        "open_rate_late_third": open_late,
        "open_rate_change": round(open_late - open_early, 4) if not (np.isnan(open_early) or np.isnan(open_late)) else np.nan,
        "dismiss_rate_early_third": dis_early,
        "dismiss_rate_late_third": dis_late,
        "dismiss_rate_change": round(dis_late - dis_early, 4) if not (np.isnan(dis_early) or np.isnan(dis_late)) else np.nan,
        "n_rows_adaptation_eligible": n,
        "n_early_third": int(len(early)),
        "n_late_third": int(len(late)),
    }


# ---------------------------------------------------------------------------
# Override tendency (streak-based)
# ---------------------------------------------------------------------------

def override_streak_features(
    df: pd.DataFrame,
    outcome_col: str = "event_outcome_simple",
    timestamp_col: str = "timestamp_utc",
    decision_outcomes: frozenset = FRICTION_DECISION_OUTCOMES,
) -> dict:
    """
    Proxy for override tendency: length of consecutive 'opened' outcome runs.

    Type: PROXY — Behavioral
    Confidence: Medium
    Proxy note: A long streak of opens is consistent with habitual override,
    but individual opens may be intentional and non-problematic.
    Minimum data: >= 5 friction-decision rows

    F003 / F213: runs are computed on friction-decision rows only. Previously any
    non-'opened' label terminated a run, so DS1's interleaved `closedApp` records
    broke every open-run and the feature encoded a per-participant logging
    configuration rather than override tendency (median max_consecutive_opens 5.0
    for the 126 close-logging DS1 participants vs 18.0 for the other 493; 17.0
    once closes are excluded).

    Parameters
    ----------
    decision_outcomes : frozenset
        Labels treated as friction-moment decisions. Rows outside this set
        (closes, 'dismissed_other', 'missing') are dropped before the run scan
        rather than being allowed to terminate a run.

    Returns
    -------
    dict with keys:
        max_consecutive_opens, mean_open_run_length, p_open_after_dismiss
    """
    event_class = classify_outcome_events(df, outcome_col, decision_outcomes=decision_outcomes)
    sub = df[event_class == EVENT_CLASS_DECISION].copy()
    sub = sub.sort_values(timestamp_col)
    outcomes = sub[outcome_col].tolist()
    n = len(outcomes)

    if n < 5:
        return {
            "max_consecutive_opens": np.nan,
            "mean_open_run_length": np.nan,
            "p_open_after_dismiss": np.nan,
        }

    # Compute runs of 'opened'
    max_run = 0
    run_lengths = []
    current = 0
    for o in outcomes:
        if o == "opened":
            current += 1
        else:
            if current > 0:
                run_lengths.append(current)
                max_run = max(max_run, current)
            current = 0
    if current > 0:
        run_lengths.append(current)
        max_run = max(max_run, current)

    mean_run = float(np.mean(run_lengths)) if run_lengths else np.nan

    # P(open after dismiss)
    pairs = list(zip(outcomes[:-1], outcomes[1:]))
    dismiss_pairs = [(a, b) for a, b in pairs if a == "dismissed"]
    if dismiss_pairs:
        p_open_after_dismiss = round(
            sum(1 for _, b in dismiss_pairs if b == "opened") / len(dismiss_pairs), 4
        )
    else:
        p_open_after_dismiss = np.nan

    return {
        "max_consecutive_opens": int(max_run),
        "mean_open_run_length": round(mean_run, 3) if not np.isnan(mean_run) else np.nan,
        "p_open_after_dismiss": p_open_after_dismiss,
    }


# ---------------------------------------------------------------------------
# Intervention duration features
# ---------------------------------------------------------------------------

def intervention_duration_features(
    df: pd.DataFrame,
    duration_col: str,
    outcome_col: str = "event_outcome_simple",
) -> dict:
    """
    Compute intervention duration features split by outcome.

    Type: DIRECT (duration column) / PROXY (duration delta as friction sensitivity)
    Confidence: Medium (duration is only available for a subset of events)
    Minimum data: >= 5 rows with non-NaN duration_col

    Returns
    -------
    dict with keys:
        mean_intervention_duration, mean_duration_on_opened,
        mean_duration_on_dismissed, duration_open_vs_dismiss_delta,
        n_events_with_duration
    """
    with_dur = df[df[duration_col].notna() & (df[duration_col] > 0)].copy()
    n_dur = len(with_dur)

    if n_dur < 5:
        return {
            "mean_intervention_duration": np.nan,
            "mean_duration_on_opened": np.nan,
            "mean_duration_on_dismissed": np.nan,
            "duration_open_vs_dismiss_delta": np.nan,
            "n_events_with_duration": n_dur,
        }

    mean_all = round(float(with_dur[duration_col].mean()), 3)

    opened_dur = with_dur[with_dur[outcome_col] == "opened"][duration_col]
    dismissed_dur = with_dur[with_dur[outcome_col] == "dismissed"][duration_col]

    mean_open = round(float(opened_dur.mean()), 3) if len(opened_dur) >= 2 else np.nan
    mean_dismiss = round(float(dismissed_dur.mean()), 3) if len(dismissed_dur) >= 2 else np.nan

    if not (np.isnan(mean_open) or np.isnan(mean_dismiss)):
        delta = round(mean_open - mean_dismiss, 3)
    else:
        delta = np.nan

    return {
        "mean_intervention_duration": mean_all,
        "mean_duration_on_opened": mean_open,
        "mean_duration_on_dismissed": mean_dismiss,
        "duration_open_vs_dismiss_delta": delta,
        "n_events_with_duration": n_dur,
    }


# ---------------------------------------------------------------------------
# Reintervention features (DS5 and DS6)
# ---------------------------------------------------------------------------

def reintervention_features(
    df: pd.DataFrame,
    reintervention_flag_col: str,
    reintervention_delay_col: str,
    outcome_col: str = "event_outcome_simple",
) -> dict:
    """
    Compute reintervention exposure and response features.

    Type: DIRECT (counts and rates) / PROXY (reintervention_open_rate as
    friction resistance indicator)
    Confidence: Medium-High for DS5 reintervention group; Low for others
    (reintervention_delay_col is ~78% NaN in DS5 for non-reintervention participants)
    Minimum data: >= 1 reintervention event

    F112 / F119: `mean_reintervention_delay_sec` is averaged over the participant's
    REINTERVENTION rows only. It previously averaged every row carrying a non-NaN
    delay, and in DS6 the delay column is populated on 47,959 rows with the flag
    == 0 (95.8% of all non-NaN delay rows), which gave 8 participants a delay
    despite `has_reintervention == 0`.

    DS6 SEMANTIC WARNING: in DS6 every non-NaN value of `reintervention_delay_sec`
    is an exact multiple of 60 s (60-2700, 45 distinct levels) — it is the
    CONFIGURED re-intervention interval, not an observed latency. DS6 renames the
    output accordingly in ds6_features.build_ds6_behavior_features().

    Returns
    -------
    dict with keys:
        has_reintervention, n_reintervention_events,
        reintervention_event_rate, mean_reintervention_delay_sec,
        reintervention_open_rate
    """
    reintvn = df[df[reintervention_flag_col] == 1]
    n_reintvn = len(reintvn)
    n_total = len(df)

    has_reintvn = int(n_reintvn > 0)
    rate = round(n_reintvn / n_total, 4) if n_total > 0 else np.nan

    # F112/F119: average over the reintervention rows isolated above, not over
    # every row that happens to carry a configured delay value.
    delays = reintvn[reintvn[reintervention_delay_col].notna()][reintervention_delay_col]
    mean_delay = round(float(delays.mean()), 3) if len(delays) >= 1 else np.nan

    if n_reintvn >= 3 and outcome_col in reintvn.columns:
        valid_reintvn = reintvn[reintvn[outcome_col].notna() & (reintvn[outcome_col] != "missing")]
        reintvn_open_rate = (
            round(float((valid_reintvn[outcome_col] == "opened").mean()), 4)
            if len(valid_reintvn) >= 3
            else np.nan
        )
    else:
        reintvn_open_rate = np.nan

    return {
        "has_reintervention": has_reintvn,
        "n_reintervention_events": int(n_reintvn),
        "reintervention_event_rate": rate,
        "mean_reintervention_delay_sec": mean_delay,
        "reintervention_open_rate": reintvn_open_rate,
    }


# ---------------------------------------------------------------------------
# Hour distribution entropy (context diversity proxy)
# ---------------------------------------------------------------------------

def hour_entropy(df: pd.DataFrame, timestamp_col: str = "timestamp_utc") -> dict:
    """
    Compute Shannon entropy of hourly event distribution.

    Type: PROXY (context/temporal diversity)
    Confidence: Medium
    Minimum data: >= 10 events with a non-NaT timestamp

    Unlike temporal_features(), this quantity is invariant to a constant
    whole-hour timezone offset, so it is safe on a UTC clock (F029/F047) — the
    only residual sensitivity is to DST shifts and to sub-hour offsets. It
    therefore does not require a `clock` declaration.

    Returns
    -------
    dict with key: hour_entropy
    """
    ts = df[timestamp_col].dropna()
    if len(ts) < 10:
        return {"hour_entropy": np.nan}
    hours = ts.dt.hour.value_counts(normalize=True)
    ent = float(-(hours * np.log2(hours + 1e-12)).sum())
    return {"hour_entropy": round(ent, 4)}


# ---------------------------------------------------------------------------
# Helper: safe merge of feature dicts
# ---------------------------------------------------------------------------

def merge_feature_dicts(*dicts) -> dict:
    """Merge multiple feature dicts into one. Later dicts override earlier ones."""
    result = {}
    for d in dicts:
        result.update(d)
    return result
