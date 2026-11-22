# Modeling Cautions — Stage 1 Feature QC Findings

**Written:** 2026-04-16  
**Purpose:** Persistent reference for modeling, harmonization, and Stage 2 work.  
Read this before starting any new modeling or cross-dataset harmonization work.

---

## 1. Features to exclude from modeling (non-informative or removed)

| Feature | Dataset | Reason | Status |
|---|---|---|---|
| `obs_window_days_ds4` | DS4 | Identical to `obs_window_days` (r=1.0) | Removed from output |
| `reintervention_open_rate` | DS6 | Always 1.0 — all DS6 outcomes are 'opened' | Removed from output |
| `app_next_entropy`, `n_unique_next_apps`, `top_next_app`, `top_next_app_share`, old `self_transition_rate`/`cross_app_transition_rate` (app_next-based) | DS6 | `app_next` does not represent "next app opened" — verified on the full raw file that DS6's log alternates Open→Close→Open→Close and `app_next` mechanically echoes the current app's own close record 99.3% of the time (not a behavioral fact). Superseded by `app_prev`-based versions 2026-08-06: `self_transition_rate`/`cross_app_transition_rate` recomputed on `app_prev` (now genuinely informative, mean=0.512/sd=0.217, not near-constant); `app_next_entropy`/`n_unique_next_apps`/`top_next_app`/`top_next_app_share` renamed to `app_transition_entropy`/`n_unique_transition_apps`/`top_transition_app`/`top_transition_app_share`. | Removed/renamed |
| `resolution_next_open_rate` | DS6 | Near-constant-near-zero (0.5%) — same look-ahead-mechanics cause as above | Removed from output |
| `n_sessions_total`, `n_sessions_baseline`, `n_sessions_intervention_period`, `session_rate_baseline`, `session_rate_intervention`, `session_rate_ratio`, `share_events_first_in_group`, `share_sessions_with_matched_close`, `session_rate_early`, `session_rate_late` | DS6 | `group_id` is unique per row across the entire raw file (verified on all 353,796 rows) — it does not group events into sessions. These columns were exact duplicates of event-count features under session-suggestive names (e.g. `session_rate_ratio` == `event_rate_ratio_intervention_vs_baseline`, 0.0 max difference). Found 2026-08-05. | Removed from output |

---

## 2. Features requiring filtering before use

### DS6: `event_rate_ratio_intervention_vs_baseline`

**Problem:** Extreme outliers from participants with minimal baseline periods.
- Participant with 1 baseline day: ratio = 77.1
- Participant with 5 baseline days: ratio = 12.6
- A rate based on 1 day is not a reliable baseline estimate.

**Required filter before model use:**
```python
# Filter to participants with at least 7 baseline days
ds6_filtered = ds6_beh[ds6_beh["n_baseline_days"] >= 7].copy()
```

After this filter, 2 extreme-outlier participants are excluded. The ratio distribution is reasonable for the remaining 239 participants.

### DS1 / DS5: `active_days_per_week`

**Problem:** 25–27% NaN due to short observation windows (< 7 days).

**Guidance:** Do not use as a primary feature in DS1 or DS5 models. Use `events_per_day` or `n_days_observed` instead, which have much lower NaN rates (17.4% and 12.4% respectively for `events_per_day`, mostly single-day window participants).

---

## 3. Features to treat cautiously (proxy limitations)

### Adaptation tertile features (`open_rate_change_*`, `dismiss_rate_change_*`)

Present in: DS1 (`_setup` suffix), DS4 (`_calendar` suffix), DS5 (`_calendar` suffix)

- For DS1 and DS5: shorter observation windows mean smaller tertile samples. Rate estimates in early/late thirds can be noisy for participants with < 30 total events.
- For DS4: very reliable given long windows (up to 897 days). The strongest adaptation signal in the project.
- Non-experimental datasets (DS1, DS4): trajectory changes may reflect attrition, app updates, or life context shifts rather than adaptation to friction. Interpret within experimental conditions (DS5) for cleaner signal.

### DS4: `active_weeks` — ISO week edge case

`active_weeks` is computed using ISO calendar week numbers. For participants observed across multiple years, the same ISO week number in two different years collapses to one value under `nunique()`. Effect: slight underestimation of active weeks for multi-year participants (roughly 25% of DS4 participants). `activity_persistence` inherits this small bias. For most analyses the effect is negligible.

### Override streak features (`max_consecutive_opens`, `mean_open_run_length`, `p_open_after_dismiss`)

Present in: DS1, DS4, DS5 (computed on all events / intervention-event class).

- These are behavioral regularity indicators, not direct self-control measures.
- A long streak of opens is consistent with habitual override but individual opens may be intentional.
- In DS4 and DS5, these are computed on the `intervention_event` class only, which gives the cleanest signal.
- In DS1, they are computed on all outcome-bearing events.

### DS6 `app_entropy_baseline` / `app_entropy_intervention` vs `app_entropy` (overall)

These three features are highly correlated:
- `app_entropy` vs `app_entropy_baseline`: r = 0.979
- `app_entropy` vs `app_entropy_intervention`: r = 0.967

Do not include all three simultaneously in regression or clustering. The minimal informative pair is:
- `app_entropy` (overall level) + `app_entropy_change` (intervention minus baseline shift)

### DS6: `self_transition_rate`/`cross_app_transition_rate` — corrected 2026-08-06 (see §6)

**Superseded finding:** this section previously reported these as near-constant
(mean=0.989, sd=0.018) due to "session-group" re-opening. Both the number and the cause
were wrong. The real cause: they were computed on `app_next`, which mechanically echoes
the current app's own close record 99.3% of the time (verified on the full raw file — see
§6 "DS6 — no genuine session-boundary data" is unrelated; this is a separate, distinct
issue in the `app_next` look-ahead field, not `group_id`). Recomputed on `app_prev`
2026-08-06: `self_transition_rate` mean=0.512, sd=0.217, range [0.18, 1.0] — now a genuine,
usable individual-difference feature. Old `app_next_entropy`/`n_unique_next_apps` (formerly
recommended as the substitution-analysis fallback) are renamed
`app_transition_entropy`/`n_unique_transition_apps` and are also now `app_prev`-based.
`resolution_next_open_rate` removed (near-constant-near-zero, same look-ahead cause).

**Use for DS6 substitution analysis:** `app_transition_entropy`, `n_unique_transition_apps`
(both `app_prev`-based) — or `self_transition_rate`/`cross_app_transition_rate` directly,
now that they carry real signal.

---

## 4. Strongest features per dataset for individual modeling

### DS1 (N=619, no experimental condition)

Behavioral:
- `rate_opened`, `rate_dismissed`, `rate_not_opened` — friction compliance rate; high coverage (0.2% NaN)
- `open_rate_change_setup`, `dismiss_rate_change_setup` — adaptation trajectory (setup-time axis)
- `max_consecutive_opens`, `p_open_after_dismiss` — habitual override tendency
- `app_entropy` — behavioral breadth

Survey (N=527 pre, N=168 with pre+post):
- `problematic_cons_pre`, `happy_pre` — validated 1–7 Likert; strongest self-report predictors in DS1
- `hours_self_reported_pre` — self-reported usage
- `problematic_cons_change`, `happy_change` — pre-post change scores (interpret cautiously: heavy attrition)

### DS4 (N=1039, largest dataset, no experimental condition)

- `rate_opened_intervention_events` — cleanest friction override metric; intervention events only
- `open_rate_change_calendar` — long-run adaptation proxy; best signal in the project for this construct given 897-day windows
- `duration_open_vs_dismiss_delta` — friction sensitivity proxy (positive = longer time when eventually opening)
- `activity_persistence`, `gaps_over_7d` — engagement stability and dropout patterns
- `app_entropy`, `n_intervention_types_seen`

### DS5 (N=573, RCT — three conditions; only experimental dataset)

- `rate_opened`, `open_rate_intervention_events` — with `study_condition` as moderator
- `open_rate_change_calendar` — within-condition adaptation
- `belong_mean_pre`, `ostracism_mean_pre`, `fomo_mean_pre` — validated psychometric scales; strongest psychosocial predictor set in the project
- `duration_open_vs_dismiss_delta` — friction sensitivity (meaningful for default and reintervention conditions; NaN for control ~99%)
- `belong_change`, `fomo_change` — pre-post psychosocial change scores

### DS6 (N=243, youngest sample: 13–17, Danish adolescents)

- `event_rate_ratio_intervention_vs_baseline` — primary behavioral response (after `n_baseline_days >= 7` filter)
- `app_transition_entropy` (renamed from `app_next_entropy` 2026-08-06, now app_prev-based) — preferred substitution diversity indicator
- `event_rate_slope` — longitudinal adaptation via participation_day regression
- `addiction_index_pre`, `self_control_index_pre` — strongest self-control indicators in the project
- `addiction_index_change`, `self_control_index_change` — primary pre-post outcome measures

---

## 5. Cross-dataset comparability: what is harmonizable and what is not

### Directly comparable (same name, same logic, post-QC)

These columns have identical names and equivalent computation across all four datasets:

```
events_per_day          obs_window_days         app_entropy
n_unique_apps           app_herfindahl          top_app_share
peak_hour_of_day        weekend_event_share     evening_event_share
morning_event_share     hour_entropy
```

### Comparable with documented caveats

| Feature | Available in | Caveat |
|---|---|---|
| Friction override rate | DS1: `rate_opened`; DS4: `rate_opened_intervention_events`; DS5: both | Different denominators (all events vs friction events only) — document explicitly; do NOT pool raw values |
| Adaptation trajectory | DS1: `open_rate_change_setup`; DS4/DS5: `open_rate_change_calendar` | Same logic (early vs late tertile); different time axes (setup-time vs calendar days) |
| Habit proxy | DS1/DS4/DS5: `max_consecutive_opens`; DS6: `max_consecutive_same_app` | Different behavioral mechanisms; `max_consecutive_same_app` (DS6) reflects consecutive same-app re-opening in the raw event sequence (not a real session boundary — see §6), not friction override streaks |
| FoMO | DS5: `fomo_mean_pre` (10-item validated scale); DS6: `fo_mo_pre` (different instrument) | Partially comparable; note instrument difference explicitly |

### Not harmonizable across datasets

| Feature type | Reason |
|---|---|
| DS6 outcome rates (`rate_opened`, etc.) | DS6 has ONLY 'opened' outcomes — no dismiss or close events |
| `event_rate_ratio_intervention_vs_baseline` | DS6-specific: only dataset with an explicit baseline period in behavioral data |
| Psychosocial scales | Each dataset uses different instruments; DS5 belonging/ostracism have no equivalent; DS6 addiction_index/trivsel have no equivalent |
| `secondsSinceOneSecSetup`-based features | DS1-specific time axis |
| Event class breakdown (`intervention_event`, `app_close_event`, `no_intervention`) | DS4-specific logging architecture |
| DS6 period-split features | DS6-specific: no other dataset has a baseline period |

---

## 6. DS-specific structural warnings (do not forget)

### DS6 — single-outcome structure

**ALL events in DS6 have `event_outcome_simple == 'opened'`.** This is not a data error. It reflects the fact that DS6 captures only app-opening events. There are no dismiss or close outcome events in the behavioral log.

Consequence: DS6 outcome rates are structurally incomparable with DS1/DS4/DS5. Use volume and event-rate changes across `study_period` as behavioral response proxies for DS6.

### DS6 — no genuine `group_id` session grouping (found 2026-08-05)

**`group_id`, `first_in_group`, `last_close_in_group` do NOT represent real sessions.** Verified on the full raw file (`session_time_dataset_97_5_cutoff_data_forwarded.csv`, all 353,796 rows): `group_id` is unique per row (nunique == row count), `first_in_group` == 1 for every row, `last_close_in_group` == 0 for every row. Same pattern in `baseline_sessions_filt3.csv`.

Consequence: DS6 has no session *count* via `group_id`. The 8 features that depended on this (`n_sessions_total`, `session_rate_baseline/intervention/ratio`, `share_events_first_in_group`, `share_sessions_with_matched_close`, `session_rate_early/late`) were removed from `ds6_behavior_features.csv` in Stage 1 QC — they were exact numerical duplicates of event-count features. Use `total_events`/`events_per_day*`/`event_rate_ratio_intervention_vs_baseline` directly instead.

**⚠ Correction to this entry (2026-08-06):** an earlier version of this note additionally
claimed `close_ts` "is the timestamp of the next open event, not an app-close signal." That
was wrong. DS6's true underlying log alternates Open→Close→Open→Close (this exported file
keeps only the Open rows); the very next logged event after an Open is that same app's own
**close** 99.4% of the time (`resolution_next == 'closedApp'`), not another open. So
`close_ts`/`time_diff_secs` (`close_ts − openedapp_open_time == time_diff_secs` exactly, as
originally found) IS genuine open→close dwell time for the large majority of rows — it was
the *interpretation*, not the arithmetic, that was wrong. `mean_time_diff_secs` should be
read as an average session-dwell-time proxy, not merely "time to next event with no
particular meaning." This does not change the `group_id`/`first_in_group`/
`last_close_in_group` finding above, which is independently verified and still correct.

### DS6 — `app_next` does not mean "next app opened" (found 2026-08-06)

**A second, separate look-ahead artifact — not the same bug as `group_id` above.**
`app_next` was assumed to record the next app the participant opened. It doesn't: because
the underlying log alternates Open→Close→Open→Close and `app_next` was computed against
that full sequence, for 99.3% of rows the very next logged record is the *current* app's
own close event — so `app_next` mechanically equals `app_name` almost always, not because
of real same-app re-opening behavior. `app_prev` does not have this problem (looking
backward hits the *previous, different* app's close event first — verified `app_prev ==
app_name` only ~42% overall, a plausible non-mechanical split). `app_next2`/`resolution_next2`
are also genuine (they skip the intervening close) but require conditioning on a resolution
code; `app_prev` doesn't and is used instead.

Consequence: `self_transition_rate`, `cross_app_transition_rate`, `app_next_entropy`,
`n_unique_next_apps`, `top_next_app`, `top_next_app_share`, and `resolution_next_open_rate`
were all built on `app_next`/`resolution_next` and were all unreliable. Recomputed on
`app_prev` 2026-08-06 (renamed `app_next_entropy`→`app_transition_entropy` etc. — see §1,
§4, §5 for corrected guidance); `resolution_next_open_rate` removed (near-constant-near-zero).
`max_consecutive_same_app` is unaffected — it never used `app_next`/`app_prev`, only the
exported file's own real Open-event row order.

### DS5 — condition not in behavioral file

`study_condition` must be joined from the pre-survey file (`cond` column). One participant (0.2%) has no pre-survey record and gets NaN condition. The `build_ds5_behavior_features()` function handles this, but if you reload `ds5_behavioral_clean.csv` directly you will not have condition.

### DS4 — event class distinction

DS4 has three structurally different event classes:
- `intervention_event` (36.5%): friction shown; has interventionType + duration
- `app_close_event` (47.1%): close events only; no intervention fields
- `no_intervention` (16.4%): open/dismiss but no friction logged

Do NOT mix event classes when computing outcome rates. Use `rate_opened_intervention_events` for friction-specific analysis.

### DS1 — `secondsSinceOneSecSetup` is 18.9% NaN

The adaptation and setup-time features are restricted to the 81.1% of events with non-NaN `secondsSinceOneSecSetup`. Participants with very few setup-time events (< 5) get NaN for `setup_window_days` and adaptation features (32.3% and 33.8% NaN respectively).

---

## 7. Proxy interpretation warnings

When using proxy features in models, maintain explicit awareness of the inferential step required:

| Feature | What it directly measures | What it is used to proxy | Limitation |
|---|---|---|---|
| `open_rate_change_*` | Change in opened-outcome rate over time | Behavioral adaptation / habituation to friction | Confounded by attrition, app-mix changes, life events (especially in non-experimental DS1, DS4) |
| `max_consecutive_opens` | Length of consecutive opened-outcome streaks | Habitual override tendency | Individual opens may be intentional and appropriate |
| `duration_open_vs_dismiss_delta` | Mean duration difference between outcomes | Friction sensitivity (more time = more engagement before opening) | Duration is NaN for closed events and some opened events |
| `app_entropy` | Shannon entropy of app distribution | Behavioral breadth / diversity | Does not distinguish between boredom-driven diversity and purposeful multi-app use |
| `hour_entropy` | Shannon entropy of hour-of-day distribution | Context diversity of phone use | Does not distinguish between variable schedules and genuinely context-diverse use |
| `event_rate_slope` (DS6) | Linear slope of daily event count over participation_day | Longitudinal adaptation / habituation | Cohort effects (same school groups); study design constrains window |
| `app_transition_entropy` (DS6, renamed from `app_next_entropy` 2026-08-06) | Entropy of the app_prev distribution (the app that preceded this one) | Substitution diversity | Not every adjacent app is a substitution response; some transitions reflect unrelated multitasking. Computed on `app_prev`, not `app_next` — `app_next` mechanically echoes the current app's own close event, see §1/§6. |
