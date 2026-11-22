# Core Comparability Summary — Stage 3

**Written:** 2026-04-16  
**Purpose:** Decision-support reference for paper writing and cross-dataset analysis. Specifies exactly which features from the harmonized core are safe for descriptive comparison, which require explicit caveats, and which should not be compared across datasets. Supplements `outputs/harmonized/stage2/cross_dataset_comparability_notes.md` with paper-facing framing.

---

## Three-tier comparability structure

Features across the four datasets fall into three tiers based on whether cross-dataset comparison is methodologically defensible:

| Tier | Label | Meaning |
|---|---|---|
| A | Directly comparable | Same computation, same logic, consistent naming post-QC; safe for cross-dataset descriptive statistics and pooled modeling subject to population difference awareness |
| B | Comparable with explicit caveats | Same conceptual construct but different source columns, denominators, or time axes; usable cross-dataset if caveats are prominently documented |
| C | Not cross-dataset comparable | Dataset-specific constructs; cross-dataset use would be misleading or structurally impossible |

---

## Tier A — Directly comparable features (13 features)

These features are computed identically across all four datasets. They are safe for cross-dataset descriptive comparison, distribution plots, and pooled modeling — subject to the **population difference caveat** (see below).

| Feature | What it captures | NaN coverage | Caveats |
|---|---|---|---|
| `total_events` | Total behavioral event count | 0% | None |
| `n_days_observed` | Distinct calendar days with ≥1 event | 0% | None |
| `obs_window_days` | Days from first to last event | 0% | None |
| `events_per_day` | Rate of events per day | 7.5% | NaN for single-day participants; DS1: 17.4%; DS5: 12.4% |
| `n_unique_apps` | Count of distinct target apps | 0% | DS1 has only 48 apps (narrow); DS4 has 399 (broad) |
| `top_app_share` | Share of events from dominant app | 0.2% | Reflects app concentration in the specific target app space per dataset |
| `app_herfindahl` | App concentration index | 0.2% | Sum of squared app-share values; higher = more concentrated |
| `app_entropy` | Shannon entropy of app distribution | 0.2% | Higher = more diverse app use; directly comparable |
| `peak_hour_of_day` | Hour (0–23) with most events | 7.5% | DS1 timestamps assumed UTC (no timezone column); DS5 timezone-corrected; DS4/DS6 confirmed UTC |
| `weekend_event_share` | Proportion of events on Sat/Sun | 7.5% | NaN for single-day participants |
| `evening_event_share` | Proportion of events 18:00–23:00 | 7.5% | NaN for single-day participants |
| `morning_event_share` | Proportion of events 06:00–11:00 | 7.5% | NaN for single-day participants |
| `hour_entropy` | Shannon entropy of hourly distribution | 10.4% | DS6 uses pre-engineered `hour_of_day` column vs UTC extraction — confirmed empirically equivalent; DS6 renamed from `hour_entropy_ds6` in Stage 1 QC |

**Population difference caveat (applies to all Tier A features):**
Even these directly comparable features should not be interpreted as if the four datasets are samples from the same population. DS1/DS4 are self-selected adult OneSec users (international). DS5 is German adolescents (13–25) in a study. DS6 is Danish adolescents (13–17) in school cohorts. Behavioral volume, temporal structure, and app diversity statistics are directly comparable in value — but participants are not matched samples. Pooling Tier A features for cross-dataset modeling requires explicit population adjustment or stratified analysis.

**DS1 temporal caveat:**
DS1 timestamps are assumed UTC. Participants are international users; their local peak hour, morning/evening shares, and weekend shares may be shifted relative to their actual local time. DS5 applies proper timezone localization. DS4 and DS6 are confirmed UTC. DS1 temporal features should be treated with slightly lower precision than the other three for any analysis sensitive to local-time behavioral patterns.

---

## Tier B — Comparable with explicit caveats (4 constructs, 6 columns)

These features share a conceptual construct but differ in source column, denominator, time axis, or structural availability across datasets. They are usable for cross-dataset analysis only with prominent documentation of the specific caveat.

### B1. Friction override rate

**Harmonized column:** `friction_override_rate`  
**Source column key:** `friction_override_source` — always read this before using `friction_override_rate`

| Dataset | Source | Denominator |
|---|---|---|
| DS1 | `rate_opened` | All outcome-bearing events (all DS1 events are friction-triggered) |
| DS4 | `rate_opened_intervention_events` | Intervention-event class only (36.5% of all DS4 events) |
| DS5 | `rate_opened` | All outcome-bearing events (but control group has no friction — their rate reflects friction-free opens) |
| DS6 | NaN (structural) | Not applicable — all DS6 outcomes are 'opened'; no override vs compliance distinction exists |

**Rules for use:**
1. Never use DS6 `friction_override_rate` — it is structurally NaN; do not impute
2. For cross-dataset comparison of DS1/DS4/DS5: document the denominator difference prominently; do not treat raw values as equivalent
3. For DS5: restrict to default and reintervention conditions before any friction-specific cross-dataset comparison; the control condition's `rate_opened` is NOT a friction override rate
4. DS4's values are computed on a narrower but cleaner fraction of events than DS1/DS5; direction and relative ranking within DS4 are meaningful; pooling DS4 raw values with DS1/DS5 raw values requires explicit acknowledgment

**Paper guidance:** When reporting friction override rate cross-dataset, either (a) report separately per dataset with explicit denominator annotation, or (b) present as a broad behavioral tendency index and note the denominator differences explicitly.

---

### B2. Behavioral response ratio (DS6 only)

**Harmonized column:** `behavioral_response_ratio`  
**Source:** `event_rate_ratio_intervention_vs_baseline` (DS6 only; always NaN for DS1/DS4/DS5)

This is the DS6-specific behavioral response proxy: intervention events/day ÷ baseline events/day. A ratio > 1 means more app-opening events during the intervention period than during baseline. A ratio < 1 means fewer events — consistent with a behavioral suppression response to the intervention.

**Required filter:** `n_baseline_days >= 7`. Applied in the harmonized core builder. 7 DS6 participants excluded (including extreme-outlier cases with 77x and 12x ratios from 1-day and 5-day baselines).

**Rules for use:**
1. Never compare `behavioral_response_ratio` to `friction_override_rate` — they measure different constructs (volume change vs event-level outcome classification)
2. Check `has_behavioral_response_ratio` before any DS6 analysis; 8 participants have NaN
3. Ratio > 1 is NOT necessarily "more friction override" — it means more app-opening events, which may reflect baseline suppression effects, cohort dynamics, or study-design artifacts

**Paper guidance:** Report this separately from override rate analyses. Describe it as a volume-change behavioral response proxy — not a compliance rate.

---

### B3. Adaptation trajectory

**Harmonized column:** `open_rate_change`  
**Source column key:** `open_rate_change_axis` — always read this before using `open_rate_change`

| Dataset | Source column | Time axis | Signal reliability |
|---|---|---|---|
| DS1 | `open_rate_change_setup` | Setup-time axis (secondsSinceOneSecSetup tertiles) | Weaker — 33.8% NaN; short windows |
| DS4 | `open_rate_change_calendar` | Calendar days (days_since_first_event tertiles) | Strongest — 897-day windows |
| DS5 | `open_rate_change_calendar` | Calendar days (days_since_first_event tertiles) | Moderate — shorter windows |
| DS6 | NaN (structural) | Not available — different study structure; period-based rather than tertile-based | N/A |

Interpretation: negative value = habituation (decreasing override over time); positive value = escalation (increasing override over time).

**Rules for use:**
1. Never use `open_rate_change` for DS6 — structural NaN; use `event_rate_slope` from Stage 1 DS6 features instead
2. For DS1: sign and direction are cautiously comparable to DS4/DS5; magnitude is NOT directly comparable (different time axes and window lengths)
3. For cross-dataset adaptation analysis: use `open_rate_change_axis` to stratify; do not pool DS1 setup-time values with DS4/DS5 calendar-day values in regression without encoding the axis difference
4. Non-experimental datasets (DS1, DS4): trajectory changes may reflect attrition, app updates, or life context shifts rather than behavioral adaptation to friction; interpret adaptation claims from DS5 (experimental) for cleaner signal

**Paper guidance:** Report adaptation trajectories separately by dataset and time axis. The cross-dataset finding is directional (who habituates vs escalates), not magnitude-comparable.

---

### B4. Study condition and experimental design flags

**Harmonized column:** `study_condition`  
**Availability flags:** `has_study_condition`, `has_friction_outcome`, `has_behavioral_response_ratio`

| Dataset | Values | Meaning |
|---|---|---|
| DS1 | NaN | Non-experimental; no condition structure |
| DS4 | NaN | Non-experimental; no condition structure |
| DS5 | control / default / reintervention | RCT — three individual-randomized arms |
| DS6 | control / default / intervention | Quasi-experimental — school cohort assignment |

`study_condition` is only meaningful for DS5 and DS6. For DS1 and DS4, `has_study_condition` is always False.

**Rules for use:**
1. DS5 and DS6 conditions share some labels (control/default) but are not equivalent — different intervention protocols, different populations, different assignment mechanisms
2. DS6 "intervention" ≠ DS5 "reintervention" — different designs
3. When reporting condition effects cross-dataset, always distinguish DS5 (individual RCT) from DS6 (cohort quasi-experimental) explicitly

---

## Tier C — Not cross-dataset comparable (excluded from harmonized core)

These feature types are present in individual dataset Stage 1 files but must NOT be used for cross-dataset comparison. They remain available in the dataset-specific `outputs/features/dsX/` files for within-dataset modeling.

| Feature type | Available in | Why not harmonizable |
|---|---|---|
| `rate_dismissed`, `rate_closed`, `rate_not_opened` | DS1, DS4, DS5 | DS6 has no dismiss/close outcomes — comparison would be structurally misleading |
| `event_rate_ratio_intervention_vs_baseline` | DS6 only | No equivalent baseline period in DS1/DS4/DS5 |
| Session structure features (`n_sessions_*`, `session_rate_*`) | DS6 only (historical) | Removed from DS6 itself in Stage 1 QC 2026-08-05 — `group_id` verified non-functional (unique per row, not real sessions); these columns no longer exist in any dataset, not merely a cross-dataset gap |
| Sequence features (`app_transition_entropy`, `self_transition_rate` — renamed/recomputed on app_prev 2026-08-06, was app_next-based) | DS6 only | Pre-engineered app_prev fields not present in other datasets (app_next verified non-functional, see `data_docs/modeling_cautions.md` §6) |
| DS4 event class features (`intervention_event_share`, etc.) | DS4 only | Three-class logging architecture is unique to DS4 |
| DS4 longitudinal activity (`active_weeks`, `activity_persistence`, `gaps_over_7d`) | DS4 only | Long-window design makes these features dataset-specifically meaningful |
| Override streak features (`max_consecutive_opens`, etc.) | DS1, DS4, DS5 | DS6 equivalent (`max_consecutive_same_app`) reflects a different mechanism |
| All psychosocial scale scores | Dataset-specific | Instruments differ strongly — pooling raw values would misrepresent measurement differences |
| `problematic_cons_pre`, `happy_pre` | DS1 only | No equivalent in DS4, DS5, DS6 |
| `belong_mean_pre`, `ostracism_mean_pre`, `fomo_mean_pre` | DS5 only | No equivalent in DS1, DS4, DS6 |
| `addiction_index_pre`, `self_control_index_pre` | DS6 only | No equivalent in DS1, DS4, DS5 |
| DS6 period-split features (`*_baseline`, `*_intervention`) | DS6 only | No equivalent period structure in DS1/DS4/DS5 |
| DS5 `duration_open_vs_dismiss_delta` | DS1, DS4, DS5 | DS6 has no dismiss events — cannot compute |
| `active_days_per_week` | DS1, DS5 (unreliable) | 25–27% NaN in DS1/DS5 due to short windows; excluded from harmonized core |

**FoMO partial note:** DS5 uses a 10-item validated FoMO scale (`fomo_mean_pre`). DS6 uses a different FoMO instrument (`fo_mo`). These are partially comparable in construct (both measure fear of missing out) but NOT in scale or instrument. Do not pool raw values. If cross-dataset FoMO comparison is needed: z-score within each dataset and document the instrument difference explicitly.

---

## Pre-analysis checklist for cross-dataset use

Before any cross-dataset descriptive comparison or modeling:

- [ ] Confirm which features are Tier A (directly comparable) vs Tier B (caveats required) vs Tier C (excluded)
- [ ] For `friction_override_rate`: check `friction_override_source` distribution; decide whether to restrict DS5 to non-control conditions
- [ ] For `open_rate_change`: check `open_rate_change_axis`; do not pool DS1 setup-time values with DS4/DS5 calendar-day values without encoding the axis difference
- [ ] For any DS6 analysis: do not use `friction_override_rate`; use `behavioral_response_ratio` with `n_baseline_days >= 7` filter applied; `self_transition_rate`/`cross_app_transition_rate` are usable within DS6 (recomputed on `app_prev` 2026-08-06 — mean=0.512, sd=0.217, no longer near-constant) but have no cross-dataset equivalent
- [ ] For psychosocial constructs: use dataset-specific Stage 1 survey feature files; do not compare raw scale scores across datasets
- [ ] Document population differences in any cross-dataset claim: DS1/DS4 are adult non-experimental; DS5 is German adolescent RCT; DS6 is Danish adolescent quasi-experimental cohort
- [ ] Check `has_survey`, `has_prepost_survey`, `has_study_condition`, `has_friction_outcome`, `has_behavioral_response_ratio` before any analysis requiring those features

---

## Paper-facing framing guidance

When writing cross-dataset results sections:

1. **Describe the comparability tier first.** Before reporting any cross-dataset number, state whether it comes from a Tier A (directly comparable), Tier B (with documented caveat), or dataset-specific source.

2. **Never report a single pooled statistic without population disclosure.** Even Tier A features should be accompanied by a note that datasets differ in population, country, and study design.

3. **Treat DS6 separately for friction response.** DS6 cannot contribute to override/compliance analysis. Its behavioral response (volume change) is a distinct construct that deserves its own reporting section.

4. **Report adaptation trajectories directionally, not in magnitude.** The sign (habituation vs escalation) is cautiously cross-dataset comparable. The magnitude is not.

5. **FoMO and self-control cannot be pooled.** If you want to discuss psychosocial moderators cross-dataset, do so with z-scores and explicit instrument disclosure, or treat them as conceptual replications rather than pooled estimates.
