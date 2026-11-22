# Stage 1 Feature Extraction — QC Review Notes

**Review date:** 2026-04-16  
**Scope:** All four dataset-specific Stage 1 feature extractions (DS1, DS4, DS5, DS6)  
**Review type:** Post-implementation quality control — no new feature engineering

---

## What was reviewed

- All 11 output CSV files in `outputs/features/ds{1,4,5,6}/`
- All four `dsX_features.py` source modules in `src/features/`
- `src/features/behavioral_features.py` shared utilities
- All four `dsX_features.md` documentation files
- Notebooks 11–14

Checks performed:
- Row and column counts against proposed design
- Column names and cross-dataset naming consistency
- NaN rate distributions for key features
- Value distributions for sanity (outcome rates, ratios, entropy)
- Redundancy analysis (pairwise correlation of suspicious feature pairs)
- Condition-specific NaN patterns (DS5)
- Edge case logic (division by zero, minimum-data thresholds)

---

## Output file verification

| File | Rows | Cols (before QC) | Cols (after QC) | Notes |
|---|---|---|---|---|
| `ds1_behavior_features.csv` | 619 | 37 | 37 | No changes |
| `ds1_survey_features.csv` | 527 | 16 | 16 | No changes |
| `ds1_prepost_features.csv` | 168 | 14 | 14 | No changes |
| `ds4_behavior_features.csv` | 1039 | 55 | 54 | Dropped `obs_window_days_ds4` |
| `ds4_survey_features.csv` | 283 | 9 | 9 | No changes |
| `ds5_behavior_features.csv` | 573 | 49 | 49 | No changes |
| `ds5_survey_features.csv` | 572 | 12 | 12 | No changes |
| `ds5_prepost_features.csv` | 284 | 18 | 18 | No changes |
| `ds6_behavior_features.csv` | 243 | 78 | 77 | Dropped `reintervention_open_rate`; renamed `hour_entropy_ds6` → `hour_entropy` |
| `ds6_survey_features.csv` | 243 | 19 | 19 | No changes |
| `ds6_prepost_features.csv` | 188 | 10 | 10 | No changes |

---

## Redundancies and naming issues found

### 1. DS4: `obs_window_days_ds4` — perfect redundancy with `obs_window_days`

`obs_window_days` is computed from timestamp min/max in `volume_features()`.  
`obs_window_days_ds4` was computed from `days_since_first_event.max()` in `ds4_longitudinal_activity()`.

Correlation: r=1.0, mean difference: 0.0000 across all 1,039 participants.

**Action taken:** Dropped `obs_window_days_ds4` from `src/features/ds4_features.py` and regenerated `ds4_behavior_features.csv`. Use `obs_window_days` — this is the cross-dataset standard name.

### 2. DS6: `hour_entropy_ds6` — naming inconsistency with DS1/DS4/DS5

All other datasets use `hour_entropy`. DS6 used `hour_entropy_ds6`. The computation is slightly different (DS6 uses the pre-engineered `hour_of_day` column rather than extracting from UTC timestamps), but the result is conceptually and empirically equivalent.

**Action taken:** Renamed to `hour_entropy` in `src/features/ds6_features.py`, regenerated `ds6_behavior_features.csv`. No other files affected.

### 3. DS6: `reintervention_open_rate` — always 1.0 (non-informative)

DS6 has only 'opened' outcomes. The `reintervention_features()` function computes opened rate among reintervention events. In DS6 this is always 1.0 (60 non-NaN participants, all equal to 1.0). The column had no discriminative power and posed a risk of being mistaken for a behavioral signal.

**Action taken:** Added `ri_feats.pop("reintervention_open_rate", None)` in `build_ds6_behavior_features()` before `feats.update(ri_feats)`. The shared `reintervention_features()` utility is unchanged — the pop is DS6-local. Regenerated `ds6_behavior_features.csv`.

### 4. DS6: `app_entropy_baseline` / `app_entropy_intervention` highly correlated with `app_entropy`

```
app_entropy vs app_entropy_baseline:    r = 0.979
app_entropy vs app_entropy_intervention: r = 0.967
```

Not removed — they encode some period-specific signal and `app_entropy_change` (intervention − baseline) is the most informative derived feature. But using all three simultaneously in modeling risks collinearity. See `modeling_cautions.md` for guidance.

---

## Implementation edge cases

### DS4: `active_weeks` — ISO week number edge case

`active_weeks` uses `dt.isocalendar().week`. For participants observed across multiple calendar years, ISO week 52 of year 1 and ISO week 52 of year 2 collapse to the same value under `nunique()`, slightly underestimating unique active weeks. Effect is small (a handful of weeks per multi-year participant at most). Documented in `ds4_features.md` Group 5.

### DS5: `n_reintervention_events` double assignment (minor code messiness)

In `build_ds5_behavior_features()`, `feats["n_reintervention_events"]` is assigned manually at line 258 and then overwritten by `feats.update(reintervention_features(...))`. Both values are identical (same logic). Not a bug, but the first manual assignment is dead code. Low priority — no functional impact.

### DS1/DS5: `active_days_per_week` requires 7-day window

The `volume_features()` function returns NaN for `active_days_per_week` when `obs_window_days < 7`. This produces 25.5% NaN in DS1 and 26.7% NaN in DS5. Both documented correctly. Use `n_days_observed` or `events_per_day` as complementary features for short-window participants.

### DS6: `event_rate_ratio_intervention_vs_baseline` — extreme outlier from minimal baseline

Two participants produced extreme ratios (77x, 12x) due to 1-day and 5-day baseline periods respectively. The feature is computed correctly — these are genuine data points. But a 1-day baseline cannot establish a reliable rate estimate. Minimum filter: `n_baseline_days >= 7` before using this feature in any model. See `modeling_cautions.md`.

### DS6: `self_transition_rate` — near-constant (mean=0.989, sd=0.018)

Within-session same-app re-opening dominates DS6's `app_next` field, making `self_transition_rate` nearly non-discriminative across participants. See `modeling_cautions.md` and the updated `ds6_features.md` Group 4 note.

---

## Cross-dataset naming consistency (post-QC state)

After cleanup, these feature names are consistent across all four datasets:

| Feature | DS1 | DS4 | DS5 | DS6 |
|---|---|---|---|---|
| `events_per_day` | ✓ | ✓ | ✓ | ✓ |
| `obs_window_days` | ✓ | ✓ | ✓ | ✓ |
| `app_entropy` | ✓ | ✓ | ✓ | ✓ |
| `n_unique_apps` | ✓ | ✓ | ✓ | ✓ |
| `app_herfindahl` | ✓ | ✓ | ✓ | ✓ |
| `top_app_share` | ✓ | ✓ | ✓ | ✓ |
| `peak_hour_of_day` | ✓ | ✓ | ✓ | ✓ |
| `weekend_event_share` | ✓ | ✓ | ✓ | ✓ |
| `evening_event_share` | ✓ | ✓ | ✓ | ✓ |
| `morning_event_share` | ✓ | ✓ | ✓ | ✓ |
| `hour_entropy` | ✓ | ✓ | ✓ | ✓ (renamed) |

The remaining naming differences are intentional: they reflect genuine dataset-specific constructs (e.g., DS1's `_setup` suffix for setup-time axis, DS4's `_calendar` suffix for calendar-time axis, DS6's `_baseline`/`_intervention` period splits).

---

## Files changed in cleanup pass

**Source modules:**
- `src/features/ds4_features.py` — removed `obs_window_days_ds4` from `ds4_longitudinal_activity()`
- `src/features/ds6_features.py` — renamed `hour_entropy_ds6` → `hour_entropy` in `ds6_period_temporal()`; added `reintervention_open_rate` pop in `build_ds6_behavior_features()`

**Regenerated CSVs:**
- `outputs/features/ds4/ds4_behavior_features.csv` (1039 × 54)
- `outputs/features/ds6/ds6_behavior_features.csv` (243 × 77)
- `outputs/features/ds6/ds6_survey_features.csv` (regenerated — unchanged)
- `outputs/features/ds6/ds6_prepost_features.csv` (regenerated — unchanged)

**Documentation updated:**
- `outputs/features/ds4/ds4_features.md` — Group 5 updated; removed `obs_window_days_ds4` row; added ISO week edge case note
- `outputs/features/ds6/ds6_features.md` — column count updated; Group 3 removal note; Group 4 `self_transition_rate` caution; Group 7 `hour_entropy` rename

---

## Addendum — 2026-08-05: DS6 session-structure bug found during Stage 4 pre-modeling check

**Trigger:** Before implementing the first DS6 CAS model (Stochastic Processes), verified that
`group_id` — the basis for DS6's "Session Structure" Stage 1 feature group and the
"DS6-unique: session grouping not available in DS1/DS4/DS5" claim in `ds6_features.md` and
`ds6_audit_report.md` — actually groups multiple events into sessions, since that claim was
about to become the anchor for a model's state variable.

**Finding (verified on the full raw file, all 353,796 rows, not a sample):**
- `group_id` is unique per row (`nunique() == len(df)`).
- `first_in_group` == 1 for every row; `last_close_in_group` == 0 for every row.
- `unmatched_open` == False for every row.
- `close_ts − openedapp_open_time` equals `time_diff_secs` exactly (max diff ~1e-12, float
  rounding). [**Correction 2026-08-06:** this was originally interpreted as "close_ts is the
  timestamp of the next open event, not a real app-close event." That interpretation was
  wrong — see the 2026-08-06 addendum below. The arithmetic finding is unchanged and correct;
  `close_ts`/`time_diff_secs` turn out to be genuine open→close dwell time for ~99% of rows.]
- Same pattern confirmed in `baseline_sessions_filt3.csv` (no `group_id` column there, but its
  own `close_ts − timestamp` also tracks `time_diff_secs`).
- Direct consequence for `ds6_behavior_features.csv`: `n_sessions_total` was numerically
  identical to `total_events`, `session_rate_baseline` identical to
  `events_per_day_baseline`, `session_rate_ratio` identical to
  `event_rate_ratio_intervention_vs_baseline` (checked: 0.0 max difference, all 243
  participants). Not a near-duplicate like the `app_entropy_baseline` correlation noted above —
  an exact duplicate under a different name.

**Action taken:**
- `src/features/ds6_features.py`: removed `ds6_session_features()` (renamed to
  `ds6_timing_features()`, now returns only `mean_time_diff_secs`, which is genuine —
  computed from `time_diff_secs` directly, not from `group_id`); removed
  `session_rate_early`/`session_rate_late` from `ds6_longitudinal_adaptation()`.
- Re-ran `notebooks/14_ds6_feature_extraction.ipynb` (also patched its 2 cells that printed the
  now-removed columns) → regenerated `outputs/features/ds6/ds6_behavior_features.csv`
  (243 × 67, down from 243 × 77 — 10 columns removed).
- Updated `outputs/features/ds6/ds6_features.md`, `data_docs/modeling_cautions.md` (§1, §4, §5,
  §6), and this file.
- **Also corrected (same session, follow-up pass):** `outputs/reports/stage0/ds6_audit_report.md`
  (new §8a), `outputs/cleaned/ds6_behavioral_clean.md`, and 3 Stage 3 planning docs
  (`dataset_strengths_summary.md`, `dataset_strengths_table.csv`, `modeling_readiness_summary.md`)
  that had independently picked up the same false "session grouping" claim in April.

**Files changed:** `src/features/ds6_features.py`, `notebooks/14_ds6_feature_extraction.ipynb`,
`outputs/features/ds6/ds6_behavior_features.csv`, `outputs/features/ds6/ds6_features.md`,
`data_docs/modeling_cautions.md`, `data_docs/stage1_feature_qc_notes.md` (this file),
`outputs/reports/stage0/ds6_audit_report.md`, `outputs/cleaned/ds6_behavioral_clean.md`,
`outputs/reports/stage3/dataset_strengths_summary.md`,
`outputs/reports/stage3/dataset_strengths_table.csv`,
`outputs/reports/stage3/modeling_readiness_summary.md`.

---

## Addendum — 2026-08-06: DS6 `app_next` look-ahead bug — a second, separate finding

**Trigger:** While designing the DS6 Network Theory (NeT) model (which was about to use
`app_next` as its primary transition-edge data), stopped to verify `app_next` genuinely
represents "the next app the participant opened" before building on it — the same
mindfulness check that caught the `group_id` bug the day before.

**Finding (verified on the full raw file, not a sample):**
- DS6's true underlying event log alternates Open→Close→Open→Close — this exported file
  keeps only the Open rows, but the look-ahead columns (`app_next`/`resolution_next`, etc.)
  were computed against the FULL alternating sequence, not the filtered one.
- `resolution_next == 'closedApp'` for 351,446/353,796 rows (99.4%) — the very next logged
  event after an Open is almost always that same app's own close.
- Conditioned on `resolution_next == 'closedApp'`, `app_next == app_name` 99.3% of the
  time — `app_next` is mechanically echoing the current app's own close record, not
  recording a real subsequent choice.
- `app_next2`/`resolution_next2` skip this: `resolution_next2 == 'openedApp'` for 64.7% of
  rows (the true next Open), and conditioned on that, `app_next2 == app_name` only 38.8% of
  the time — a plausible, non-mechanical same-app-vs-switch split.
- `app_prev` (looking backward) does not have the forward problem either: `app_prev ==
  app_name` only ~42% overall, stable (39–64%) across `resolution_last` categories.
- **Correction to the 2026-08-05 addendum above:** `close_ts`/`time_diff_secs` were
  characterized there as "not a real app-close event." That was wrong — since the next
  logged event is usually a real close (per `resolution_next` above), `close_ts` is very
  likely a genuine open→close dwell time for ~99% of rows. The arithmetic
  (`close_ts − openedapp_open_time == time_diff_secs`) was correct; only the interpretation
  needed fixing.

**Direct consequence:** every DS6 Group 4 sequence feature except `max_consecutive_same_app`
was built on `app_next`/`resolution_next` and was unreliable:
- `self_transition_rate` (was mean=0.989, sd=0.018 — near-ceiling, previously attributed to
  "within-session re-opening") and `cross_app_transition_rate`: the near-ceiling reading was
  real but the cause was wrong — it was this look-ahead mechanics, not session behavior
  (DS6 has no real sessions at all per the 2026-08-05 finding).
- `app_next_entropy`, `n_unique_next_apps`, `top_next_app`, `top_next_app_share`: previously
  the **explicitly recommended** DS6 substitution features (`modeling_cautions.md` §3/§4) —
  all dominated by the same mechanical same-app-echo pattern, not reliable substitution
  measures.
- `resolution_next_open_rate`: verified near-constant-near-zero (0.5% overall) — same cause.

**Action taken:**
- `src/features/ds6_features.py::ds6_sequence_features()`: rebuilt on `app_prev` instead of
  `app_next`. `self_transition_rate`/`cross_app_transition_rate` keep their names (now
  mean=0.512, sd=0.217 — genuinely informative). Renamed `app_next_entropy` →
  `app_transition_entropy`, `n_unique_next_apps` → `n_unique_transition_apps`,
  `top_next_app` → `top_transition_app`, `top_next_app_share` → `top_transition_app_share`.
  Removed `resolution_next_open_rate`. `max_consecutive_same_app` untouched (never used
  `app_next`/`app_prev` — built from the exported file's own real Open-event row order).
- Re-ran `notebooks/14_ds6_feature_extraction.ipynb` (patched 1 cell referencing the renamed
  column) → regenerated `ds6_behavior_features.csv` (243 × 66, down from 67 — net −1 column,
  since Group 4 lost `resolution_next_open_rate` but otherwise kept the same field count).
- Updated `outputs/features/ds6/ds6_features.md` (Group 4), `data_docs/modeling_cautions.md`
  (§1, §4, §5, §6 — including the close_ts interpretation correction), and this file.

**Files changed:** `src/features/ds6_features.py`, `notebooks/14_ds6_feature_extraction.ipynb`,
`outputs/features/ds6/ds6_behavior_features.csv`, `outputs/features/ds6/ds6_features.md`,
`data_docs/modeling_cautions.md`, `data_docs/stage1_feature_qc_notes.md` (this file).
