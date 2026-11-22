# DS6 — Stochastic Processes (StoP) Blueprint

**Notebook:** `notebooks/73_ds6_stochastic_processes.ipynb`
**Written:** 2026-08-06
**Position:** 73 in the DS6 70s decade (see `outputs/reports/stage4/ds6_step1_plan.md`). First
DS6 model family implemented. InT (75) and DyS (72) will depend on this notebook's drift/
diffusion output, matching the DS5/Structured dependency pattern.
**Depends on:** `outputs/cleaned/ds6_behavioral_clean.csv`, `outputs/features/ds6/ds6_behavior_features.csv`
(post session-structure-fix version, 243 × 67 — see §0 of the Step 1 plan)
**Output root:** `outputs/model_outputs/ds6/stochastic_processes/`

---

## Part 0 — Why this cannot be a DS5 port

DS5's StoP notebook modeled `X_t = n_opened_day / n_events_day`, a **bounded [0,1] override
rate** — meaningful because DS5 logs opened/dismissed/closed outcomes. DS6 logs **only
`openedApp`** (confirmed structural, not missing data — `data_docs/modeling_cautions.md` §6).
Applying DS5's formula to DS6 gives `X_t ≡ 1` for every participant every day: a constant,
zero-information series. DS5's state variable is unusable here, full stop.

The theory paper's own §1.3 text names the fallback explicitly: *"Stochastic Processes are
also feasible because event logs can be aggregated into user-day or user-week time series,
such as **daily attempt count**, daily dismissal rate, daily opening rate, or daily
friction-success rate."* DS6 uses the first of these — the only one of the four that doesn't
require an outcome variable DS6 doesn't have.

This also means DS6 is closer in spirit to Structured's StoP (unbounded daily **count**, not
a bounded rate) than to DS5's. But it is not a Structured port either: Structured's count
was task-creation events with no experimental structure; DS6's count is app-opening attempts
with an explicit **within-participant baseline-vs-intervention period** the paper's own shared
episode framing doesn't have an equivalent for in any other dataset in this project. That
period structure, not the count-vs-rate distinction, is what actually drives this blueprint's
design (Part 1).

---

## Part 1 — State variable: daily attempt count, split by study period

```
N_t^(i,period) = count of app-opening events for participant i on calendar day t,
                 restricted to period in {baseline, intervention}
```

**Two series per participant, not one.** DS6's `study_period` column is directly in every
behavioral row (unlike DS5, where `study_condition` must be joined from the survey file).
Fitting one SDE per period, per participant, is the natural DS6-specific design: it turns
the already-existing but purely descriptive `event_rate_ratio_intervention_vs_baseline`
feature (a single ratio of means) into two full drift/diffusion characterizations that can
be compared — does the participant's daily-count *trend* change from baseline to
intervention, not just its *level*?

Verified before committing to this design (not assumed):
- `study_period` has exactly 2 values in the behavioral file: `baseline` (158,889 rows),
  `intervention` (194,907 rows). No third value — confirms the raw project description's
  mention of a later "50% returned to baseline / 50% opened restrictions" phase is **not**
  captured as a distinct `study_period` value in this export (it may be folded into
  `intervention` or simply not covered by this file's window). Flagged, not resolved — a
  genuine unknown, not silently assumed away.
- Daily attempt volume is high: mean ≈ 36 events per active participant-day (min 1, max 333).
  This is a much higher-count process than Structured's (~6/day) — worth noting because it
  means DS6's Fano factor (Part 4) is being estimated from richer per-day counts, likely more
  stable than Structured's estimates were.

---

## Part 2 — Period window structure (verified against DS6's real distribution, not assumed)

```
n_baseline_days:      count=243, mean=14.3, median=15, min=1, max=15   (active days per participant)
n_intervention_days:  count=241, mean=27.1, median=29, min=2, max=30
```

The baseline period is a study-design-fixed ~15-day window; intervention is a ~29–30-day
window (matches the audit report's period-length description). Most participants are dense
within their window — median `active_days / span_days` ratio is **1.0** for both periods
(no internal gaps) — but a real minority are sparse (min ratio 0.38 baseline, 0.07
intervention), and a handful have pathologically short baseline windows (2 participants with
exactly 1 baseline day, 2 with 2 days, 1 with 3 days) — the same participants already flagged
in `modeling_cautions.md` §2 for producing extreme `event_rate_ratio` outliers (77x, 12.6x).

**Zero-filling:** build a regular daily grid from each participant's first to last active day
*within each period* (inclusive), filling non-observed days with `N_t = 0`. A day with zero
attempts is a real, meaningful zero (participant did not open a target app that day), not
missing data — same reasoning as Structured Part 3.

**Eligibility threshold — reused from the already-established, already-verified
`modeling_cautions.md` §2 finding, not re-derived from scratch:**

```
MIN_ACTIVE_DAYS = 7   # per period, independently
```

Checked directly against this notebook's own eligibility split:

```
Baseline eligible (>=7 active days):      236/243 (97.1%)
Intervention eligible (>=7 active days):  236/243 (97.1%)
Both periods eligible:                    230/243 (94.7%)
```

Participants eligible in only one period get NaN parameters for the other (not imputed,
not dropped from the output table).

---

## Part 3 — Estimation (method of moments, same general technique as DS5/Structured; input changed)

For each eligible participant × period, on the zero-filled daily grid `N_0, ..., N_T`:

```
ΔN_t = N_t - N_{t-1}                     for t = 1..T
mu_hat^(period)  = mean(ΔN_t)            # drift: attempts/day trend within that period
sig_hat^(period) = std(ΔN_t, ddof=1)     # diffusion: day-to-day variability around the trend
sigma_mu_ratio   = sig_hat / |mu_hat|    # NaN if |mu_hat| < MU_THRESHOLD (0.5, see Part 6 —
                                          # DS6's counts are ~36/day scale, so DS5's
                                          # MU_THRESHOLD=0.005 (tuned for a [0,1] rate) would
                                          # almost never trigger here; rescaled accordingly)
```

**Between-period effect (re-derivation of the paper's friction-as-drift-reduction logic,
Part 1's original DS5 form was `h_c = mu_bar_control - mu_bar_c` across conditions; DS6's
natural analog is within-participant, across periods):**

```
h_period^(i) = mu_hat^(i,intervention) - mu_hat^(i,baseline)
```

Positive `h_period` = accelerating daily-attempt trend once the intervention period starts;
negative = decelerating. This is a genuinely new quantity — not recoverable from the existing
`event_rate_ratio_intervention_vs_baseline` feature, which compares period *means*, not
period *trends*.

---

## Part 4 — Fano factor (count-process-specific, same justification as Structured)

```
Fano_factor^(period) = Var(N_t) / Mean(N_t)     # computed on the RAW (non-differenced) grid
```

`Fano ≈ 1`: Poisson-like, evenly random attempt timing. `Fano > 1`: overdispersed / bursty
clustering. `Fano < 1`: more regular than chance. Not applicable to DS5's bounded [0,1] rate
(variance of a bounded proportion isn't comparable to its mean in the same way) — a
count-process-specific diagnostic, same role it played for Structured.

---

## Part 5 — Condition × period breakdown

DS6 has both `study_condition` (control/default/intervention — the RCT-like arm) **and**
`study_period` (baseline/intervention — before/after within participant) directly in the
behavioral file. Report `mu_hat`/`sig_hat`/`Fano_factor` aggregated by `study_condition ×
study_period` (a 3×2 summary table), not just by period alone — this is the one place a
DS5-style condition comparison genuinely applies to DS6, since `study_condition` doesn't
need to be joined here (unlike DS5, where it's absent from the behavioral file — DS6's
`ds6_behavioral_clean.md` confirms `study_condition` is a native column).

**Caution carried over from `modeling_cautions.md` §6:** DS6's `study_condition = 'control'`
includes rows from both periods — the condition label does not itself change what
`study_period` means. Both factors are reported, not collapsed into one.

---

## Part 6 — Parameter choices (FLAG decisions, recorded before implementation)

| Flag | Decision | Rationale |
|---|---|---|
| FLAG 1 | Constant-drift process on zero-filled daily counts (not OU, not a point-process intensity model) | Matches DS5 FLAG 1's simplicity precedent; DS6's ~15/~29-day windows are too short for a 3-parameter OU fit, same reasoning DS5 used for its own short windows |
| FLAG 2 | Method-of-moments estimators (mean/std of Δ) | Same technique as DS5/Structured; consistent estimation methodology across the project |
| FLAG 3 | Period effect as drift difference: `h_period = mu_hat_intervention - mu_hat_baseline` (within-participant) | DS6-specific re-derivation of DS5's between-condition `h_c`; period is the more natural comparison axis here (§1) |
| FLAG 4 | `MU_THRESHOLD = 0.5` (attempts/day) for the `sigma_mu_ratio` denominator guard, not DS5's `0.005` | DS6's raw scale is ~36 events/day vs DS5's [0,1] rate — reusing DS5's threshold unchanged would either never trigger (if left at 0.005) or be arbitrary; 0.5 is ~1.4% of the mean daily count, the same relative proportion DS5's 0.005 represents of a typical ~0.3–0.5 override rate |
| FLAG 5 | StM/InT Boltzmann-type bridges: noted as forward connections, not implemented here | Same deferral pattern as DS5 FLAG 4 |

---

## Part 7 — Theory-to-data mapping

| Theoretical quantity | Data column / computation | Source file | Proxy limitation |
|---|---|---|---|
| State variable N_t | Daily count of behavioral rows | ds6_behavioral_clean.csv | Attempt volume, not urge, self-control, or habit strength |
| Time index t | event_date within study_period | ds6_behavioral_clean.csv | Calendar days; ignores intra-day structure |
| Period split | study_period ∈ {baseline, intervention} | ds6_behavioral_clean.csv (native column) | Two fixed-length study-design windows, not participant-chosen |
| Drift mu_hat | mean(ΔN_t) per period | Computed from zero-filled daily grid | Trend in raw attempt count, not motivation |
| Diffusion sigma_hat | std(ΔN_t, ddof=1) per period | Computed from zero-filled daily grid | Includes context noise + measurement error |
| Burstiness | Fano_factor per period | Computed from zero-filled daily grid | Standard point-process diagnostic, not a claim about psychological state |
| Period effect | h_period = mu_hat_intervention - mu_hat_baseline | Computed from participant-level params | Population/individual drift shift; not a causal claim without further design controls |
| Experimental condition | study_condition | ds6_behavioral_clean.csv (native column) | Quasi-experimental cohort assignment, not individual randomization (per stage3 dataset_strengths_table.csv) |
| Psychosocial moderators | addiction_index_pre, self_control_index_pre | ds6_survey_features.csv | Pre-intervention wave 1 only |

---

## Part 8 — Output file structure

```
outputs/model_outputs/ds6/stochastic_processes/
  participant_stop_parameters.csv   # one row per participant: mu_hat/sig_hat/sigma_mu_ratio/
                                     # Fano_factor for BOTH periods, h_period, n_active_days,
                                     # span_days per period, eligibility flags, study_condition
  daily_series_long.csv             # long format: participant_id, study_period, event_date,
                                     # day_index, N_t (zero-filled) — for reproducibility /
                                     # reuse by DyS (72) and InT (75)
  condition_period_summary.csv      # study_condition x study_period aggregate table
  psychosocial_correlations.csv     # mu_hat/sig_hat/h_period vs addiction_index_pre,
                                     # self_control_index_pre
  figures/
    fig1_stop_mu_sigma_by_period.png
    fig2_stop_h_period_distribution.png
    fig3_stop_fano_by_period.png
    fig4_stop_condition_period_comparison.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Confirmed DS5's bounded-rate X_t does not transfer (X_t ≡ 1 always in DS6) — verified,
      not assumed
- [x] Paper §1.3 quoted directly; daily attempt count is the paper's own named fallback
- [x] Period-window distributions verified against real data (15/29-day windows, gap ratios,
      the 5 already-known short-baseline outliers)
- [x] Eligibility threshold reused from the already-verified `modeling_cautions.md` finding,
      re-checked against this notebook's own split (236/236/230 out of 243)
- [x] MU_THRESHOLD rescaled with an explicit, stated rationale (not DS5's value copied
      unchanged, not picked arbitrarily)
- [x] Condition x period breakdown scoped to avoid the known `study_condition='control'`
      spans-both-periods pitfall
- [x] Notebook 73 implemented and executed — 230/243 (94.7%) both-period eligible; headline:
      mean daily attempt volume drops 45.1 -> 29.1 events/day baseline to intervention
      (level effect, cross-validates Stage 1's `event_rate_ratio` feature independently),
      but h_period (trend/drift shift) is not significant (paired t p=0.659) — level moved,
      trend didn't. Window-length asymmetry (15 vs 28 days) flagged as an open caveat on the
      sig_hat/Fano period contrast, not resolved. See `model_run_summary.md`.
