# Cross-Dataset Comparability Notes — Stage 2 Harmonized Core

**Written:** 2026-04-16  
**Purpose:** Persistent reference for anyone using `harmonized_core_features.csv`.  
Read before any cross-dataset analysis, modeling, or descriptive comparison.

---

## 1. The three-layer comparability structure

Features in the harmonized core fall into three comparability levels:

### Group A — directly comparable (13 features)

These features are computed identically across all four datasets, have consistent names post-QC, and can be used for direct descriptive comparison. They are safe for cross-dataset modeling subject to normal within-dataset NaN handling.

```
total_events          n_days_observed       obs_window_days       events_per_day
n_unique_apps         top_app_share         app_herfindahl        app_entropy
peak_hour_of_day      weekend_event_share   evening_event_share
morning_event_share   hour_entropy
```

**Even Group A features require design awareness:** DS4 has the longest windows (up to 897 days), DS1 is the shortest, DS6 has an explicit baseline/intervention period structure. Behavioral volumes and app diversity statistics are directly comparable in value, but participants across datasets are not matched samples — they come from different populations, study designs, and countries.

### Group B — comparable with documented caveats (4 logical features, 6 columns)

These features require reading the caveat columns (`friction_override_source`, `open_rate_change_axis`, `behavioral_response_proxy_type`) before any use.

| Feature | Core caveat |
|---|---|
| `friction_override_rate` | Different denominators across datasets; DS6 always NaN (structural) |
| `open_rate_change` | Different time axes (setup-time vs calendar days); DS6 NaN |
| `behavioral_response_ratio` | DS6-specific; no equivalent elsewhere; different construct from friction_override_rate |
| `study_condition` | Only meaningful for DS5 and DS6; DS1/DS4 non-experimental |

### Group C — excluded (dataset-specific only)

These features were excluded from the harmonized core because cross-dataset comparison would be misleading. They remain in the Stage 1 dataset-specific feature files.

See `harmonized_core_schema.md` Section "What is NOT in this file" for the full list and exclusion reasons.

---

## 2. DS6 structural incompatibility — the most important caveat

**DS6 has ONLY 'opened' outcomes.** This is not a data error. The DS6 behavioral log captures only app-opening events — there are no dismiss or close events.

Consequences:
- `friction_override_rate` is NaN for all 243 DS6 rows. This is structural — do NOT impute.
- `open_rate_change` is NaN for all DS6 rows. No equivalent feature exists.
- DS6 behavioral response to friction is measured via volume changes (events/day ratio across baseline vs intervention periods), not via outcome rates.
- The `behavioral_response_ratio` column captures this DS6-specific behavioral response.

**Never compare `friction_override_rate` values from DS1/DS4/DS5 to DS6 rows. The NaN in DS6 does not mean "missing data" — it means "the concept does not apply to this dataset's outcome structure."**

---

## 3. Friction override rate — denominator differences

The `friction_override_rate` column is sourced from three different source features:

| Dataset | Source column | Denominator |
|---|---|---|
| DS1 | `rate_opened` | All outcome-bearing events (all DS1 events are friction-triggered) |
| DS4 | `rate_opened_intervention_events` | Intervention-event class only (36.5% of all DS4 events) |
| DS5 | `rate_opened` | All outcome-bearing events (includes friction-free control opens) |
| DS6 | NaN | Not applicable |

**Implications:**
- DS4's friction_override_rate is computed on a cleaner but narrower subset than DS1/DS5.
- DS5 control participants' friction_override_rate reflects friction-free app opens — it is NOT a measure of friction override. For cross-dataset friction comparison, restrict DS5 to default and reintervention conditions.
- Despite denominator differences, the direction and relative ordering of participants within each dataset is meaningful. Pooling raw values requires explicit acknowledgment of this limitation.

**Rule:** When comparing friction_override_rate across datasets, either (a) restrict DS5 to non-control conditions and annotate the denominator difference prominently, or (b) treat it as a broad behavioral tendency index rather than a precise rate.

---

## 4. Adaptation trajectory — time axis differences

The `open_rate_change` column is sourced from:

| Dataset | Source column | Time axis |
|---|---|---|
| DS1 | `open_rate_change_setup` | Tertiles of `secondsSinceOneSecSetup` (individual setup-time axis) |
| DS4 | `open_rate_change_calendar` | Tertiles of `days_since_first_event` (calendar days) |
| DS5 | `open_rate_change_calendar` | Tertiles of `days_since_first_event` (calendar days) |
| DS6 | NaN | Not available (different study structure; only 'opened' outcomes) |

**Implications:**
- DS1's setup-time axis anchors each participant to their own app installation moment. Calendar day 1 for two DS1 participants may be months apart in absolute time.
- DS4 and DS5 use calendar days from first event — comparable to each other.
- DS1 is comparable to DS4/DS5 in sign (negative = habituation, positive = increasing override) but not in magnitude (different window lengths and time anchoring).
- DS4 windows are much longer (up to 897 days) — the strongest adaptation signal in the project.
- Non-experimental datasets (DS1, DS4) cannot rule out attrition, app update effects, or life context changes as drivers of the trajectory.

**Rule:** Use `open_rate_change_axis` to stratify before any analysis. Do not pool DS1 setup-time values with DS4/DS5 calendar-day values in a regression without encoding the axis difference.

---

## 5. DS6 behavioral response ratio — filter and interpretation

The `behavioral_response_ratio` for DS6 requires:
1. `n_baseline_days >= 7` — already applied in the harmonized core builder. Participants with shorter baselines get NaN.
2. Interpretation: ratio > 1 means more app-opening events per day during the intervention period than during baseline. This does NOT necessarily mean more friction override — it may reflect baseline suppression effects, cohort dynamics, or study-design artifacts.
3. This feature has no equivalent in DS1/DS4/DS5 (those datasets have no explicit baseline period in the behavioral data).

7 DS6 participants were excluded by the filter (out of 243). The 2 most extreme cases had 1-day and 5-day baselines producing ratios of 77x and 12x respectively.

---

## 6. Population and design differences

The four datasets are NOT from the same population:

| Dataset | Population | Design | N |
|---|---|---|---|
| DS1 | General adult users of OneSec | No control group; self-selected | 619 |
| DS4 | Large self-selected OneSec user base | Non-experimental retrospective | 1,039 |
| DS5 | German adolescents (13–25) | RCT — 3 conditions | 573 |
| DS6 | Danish adolescents (13–17) | Quasi-experimental (school cohorts) | 243 |

**Implications for cross-dataset modeling:**
- Pooling DS1/DS4 (adult, non-experimental) with DS5/DS6 (adolescent, experimental) requires explicit population adjustment or separate analysis layers.
- Age ranges differ substantially. DS6 is the youngest cohort (13–17). DS5 is adolescent to young adult (13–25). DS1/DS4 are general adult.
- Cultural and country contexts differ (DS5: Germany, DS6: Denmark, DS1/DS4: international mix).

---

## 7. Survey coverage by dataset

| Dataset | Survey coverage | Pre-post coverage | Psychosocial scales |
|---|---|---|---|
| DS1 | 527/619 (85.1%) | 168/619 (27.1%) | `problematic_cons_pre`, `happy_pre` (1–7 Likert) |
| DS4 | 283/1039 (27.2%) | None | Qualitative text only — no Likert scales |
| DS5 | 572/573 (99.8%) | 284/573 (49.6%) | `belong_mean_pre`, `ostracism_mean_pre`, `fomo_mean_pre` (validated psychometric scales) |
| DS6 | 243/243 (100%) | 188/243 (77.4%) | `addiction_index_pre`, `self_control_index_pre`, `fo_mo_pre`, `trivsel_pre` |

Psychosocial scale scores are NOT in the harmonized core because instruments differ across datasets. The availability flags (`has_survey`, `has_prepost_survey`) indicate which participants have any survey data.

**FoMO note:** DS5 uses a 10-item validated FoMO scale (`fomo_mean_pre`). DS6 uses a different FoMO instrument (`fo_mo_pre`). These are partially comparable in construct but not in scale. Do not pool raw values — if cross-dataset FoMO comparison is needed, z-score within each dataset and annotate the instrument difference explicitly.

---

## 8. What to check before using the harmonized core for modeling

Before using `harmonized_core_features.csv` in any analysis:

- [ ] Read `data_docs/modeling_cautions.md` in full
- [ ] Read `data_docs/stage1_feature_qc_notes.md`
- [ ] Read this file
- [ ] Check `friction_override_source` distribution — do not pool DS4 with DS1/DS5 raw values without documenting the denominator difference
- [ ] For any analysis involving DS5, decide whether to include or exclude the control condition from friction_override_rate comparisons
- [ ] For any analysis involving DS6, do not use friction_override_rate — use behavioral_response_ratio and check has_behavioral_response_ratio
- [ ] Check `open_rate_change_axis` if using adaptation trajectory features
- [ ] For psychosocial moderators, go back to the dataset-specific Stage 1 feature files — they are not in the harmonized core
- [ ] Remember that Group A features are comparable in value but the datasets are not matched samples — populations, countries, and study designs differ
