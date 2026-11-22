# Structured — Stochastic Processes (StoP) Blueprint

**Notebook:** `notebooks/63_structured_stochastic_processes.ipynb`
**Written:** 2026-08-03
**Position:** 63 in the Structured 60–68 decade. No dependency on NeT (64) or InT (65), but DyS (62) and
StM (61) will depend on this notebook's output, per the project's established dependency chain
(`cross_dataset_strategy.md`: "StoP-derived quantities feed StM's β approximation" — same logic that
applied to DS5 now applies to Structured).
**Depends on:** `outputs/cleaned/structured_behavioral_clean.csv`
**Output root:** `outputs/model_outputs/structured/stochastic_processes/`

---

## Part 0 — Design principle: why this cannot be a DS5 port

DS5's StoP notebook (`43_ds5_stochastic_processes.ipynb`) modeled `X_t` = a daily **override rate**
(fraction opened, bounded in [0,1]) — a proportion, because OneSec's friction events naturally produce a
bounded per-day outcome rate. Structured has no equivalent bounded daily outcome. The theory paper's own
StoP section names a genuinely different kind of daily variable:

> "Example A: Concrete Structured-planning illustration. A concrete Stochastic Processes example would
> model **the number of timed tasks created per user-day**. One user may show a positive drift, creating
> increasingly more timed tasks across the first month. Another user may show negative drift... A third
> user may show no clear drift but high diffusion, with irregular planning bursts."
>
> "Temporal Role: Useful for modeling planning activity, **completion marking**, inbox use, task
> complexity, and recurrence over repeated days."

The paper's own worked example is an unbounded **count** process, not a bounded rate. Forcing DS5's
proportion-based SDE machinery onto a count series would misrepresent the data. What *does* carry over
from DS5, because it is a general statistical technique rather than DS5-specific content, is the
**method-of-moments drift/diffusion estimation approach** (`mu_hat` = mean increment, `sig_hat` = std of
increment) — the same estimation *method*, applied to a different, paper-justified state variable.

---

## Part 1 — Two daily state variables (both named explicitly in the paper's Temporal Role sentence)

1. **`N_t^created`** — count of `timed`-task `Task Created` events per participant-local-day. Matches
   the paper's own worked example exactly ("the number of timed tasks created per user-day").
2. **`N_t^completed`** — count of `task_completed` marking events (from `update_type_list_str`) per
   participant-local-day. Operationalizes the paper's explicit "completion marking" temporal role.

Not implemented as separate StoP series here: inbox use, task complexity, recurrence. These are named by
the paper as *daily indicators* in a way that reads more naturally as **cross-sectional shares per
user-day** (DyS's own Table-1 row explicitly claims "task volume, timed-task share, inbox share,
completion rate, and task complexity" as its state-space variables) than as a repeated count process in
their own right. Leaving them for DyS (notebook 62) keeps StoP focused on the two variables the paper's
StoP paragraph itself names, rather than duplicating DyS's assigned scope.

---

## Part 2 — Local-calendar-day binning (a real, verified, Structured-specific decision)

**Decision: bin by the participant's LOCAL calendar day (via each event's own `event_timezone`), not
UTC calendar day.**

**Why this matters here specifically, verified before implementation, not assumed:** 24/61 participants
(39%) have more than one distinct `event_timezone` value across their events (device timezone changes /
travel), and the behavioral data spans 45 distinct timezones overall (per the inspection notebook). A
task created at 23:40 local time and one at 00:10 local time the same "planning evening" would land on
two different UTC calendar days for a participant in, say, `America/Los_Angeles` (UTC−7/−8) — naive
UTC-day binning would misclassify genuinely same-session planning activity as two separate days,
distorting both the daily count series and any drift/diffusion estimate built on it. Verified: local-date
conversion via `event_timezone` succeeds for all but 2/19,805 completion events (missing timezone,
dropped) and all 9,828 timed-creation events.

---

## Part 3 — Zero-filling and eligibility (verified against this dataset's real distribution)

For each participant and each of the two series, build a **regular daily grid** from their first to
last local-active-day for that series (inclusive), filling days with no matching event as `0` — a
day with zero task creations (or zero completion-markings) is a real, meaningful zero, not missing data.

**Eligibility threshold, checked directly against Structured's own local-day distributions (not copied
from DS5's `MIN_DAYS=7` span rule):**

```
MIN_SPAN_DAYS = 14      # need enough consecutive days for a meaningful drift/diffusion estimate
MIN_ACTIVE_DAYS = 5     # need enough non-zero observations to avoid a degenerate all-zero series
```

Verified eligible counts:
- `N_t^created`: 43/61 participants (70.5%) meet both thresholds
- `N_t^completed`: 38/61 participants (62.3%) meet both thresholds

(For reference, a stricter `MIN_ACTIVE_DAYS=7` — matching DS5's numeral, but note DS5's `MIN_DAYS=7`
meant *calendar span*, a different definition — gives 39/61 and 38/61 respectively; the chosen
`MIN_SPAN_DAYS=14` + `MIN_ACTIVE_DAYS=5` combination was picked because it separately controls for both
"enough calendar time to see a trend" and "enough non-zero days to estimate variability," which a single
combined threshold cannot.)

---

## Part 4 — Estimation (method of moments, general technique reused from DS5; input changed)

For each eligible participant and series, on the zero-filled daily grid `N_0, N_1, ..., N_T`:

```
ΔN_t = N_t - N_{t-1}                    for t = 1..T
mu_hat  = mean(ΔN_t)                    # drift: tasks/day trend
sig_hat = std(ΔN_t)                     # diffusion: day-to-day variability around the trend
sigma_mu_ratio = sig_hat / |mu_hat|     # diffusion-dominance ratio (same general SDE concept as DS5;
                                         # undefined / reported as NaN when mu_hat ~ 0)
```

**New quantity, not used in DS5 (count-process-specific, does not apply to DS5's bounded rate):**

```
Fano_factor = Var(N_t) / Mean(N_t)      # computed on the RAW (non-differenced) daily count series
```

The Fano factor is a standard point-process burstiness measure: `Fano ≈ 1` is consistent with a
Poisson-like (memoryless, evenly-random) process; `Fano > 1` indicates overdispersion — activity
clustered into bursts separated by quiet periods; `Fano < 1` indicates more regular/evenly-paced activity
than random chance would produce. This directly operationalizes the paper's "bursty" phenotype language
in a way `sig_hat` alone (which measures dispersion around a *linear trend*, not raw clustering) does not
capture as cleanly.

---

## Part 5 — Descriptive phenotype labeling (Step 1 scope: illustrative only, no clustering)

Matches the paper's own named categories ("Example B: drift-dominated... noise-dominated... bursty...
stable... decay-prone"). Consistent with this project's established Step 1 vs. Step 2 boundary (DS5:
Step 1 = model implementation only; Step 2 = clustering/phenotyping, not yet started even for DS5's own
richer feature set) — this is a **rule-based descriptive label for reporting purposes**, not a clustering
result, and must not be presented as one.

```
if   |mu_hat| is in the top tercile of |mu_hat| AND mu_hat > 0:  "growth-drift"
elif |mu_hat| is in the top tercile of |mu_hat| AND mu_hat < 0:  "decay-drift"
elif Fano_factor is in the top tercile:                          "bursty"
elif sigma_mu_ratio is in the bottom tercile (drift >> diffusion): "stable"
else:                                                             "noise-dominated"
```

Tercile cutpoints computed empirically from the eligible-participant distribution, reported in the
notebook — not hardcoded a priori.

---

## Part 6 — Observational subscription-group comparison (same caveat pattern as NeT FLAG W5)

Structured has no experimental condition. `subscription_type_last` (free/pro) is reported descriptively
by drift/diffusion/Fano — explicitly labeled non-causal, matching the precedent set in
`structured_net_blueprint.md` Part 4 FLAG W5.

---

## Part 7 — Output file structure

```
outputs/model_outputs/structured/stochastic_processes/
  participant_stop_parameters.csv     # one row per participant: mu_hat/sig_hat/sigma_mu_ratio/Fano_factor
                                       # for BOTH series (created, completed), n_active_days, span_days,
                                       # eligibility flags, descriptive phenotype label, subscription_type_last
  daily_series_long.csv               # long format: participant_id, series (created/completed),
                                       # local_date, day_index, N_t (for reproducibility / later reuse by DyS)
  figures/
    fig1_stop_mu_sigma_scatter.png
    fig2_stop_fano_distribution.png
    fig3_stop_subscription_comparison.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Theory paper §2.3 read in full and quoted directly above
- [x] Confirmed DS5's bounded-rate `X_t` does not transfer; count-based `N_t` is the paper's own example
- [x] Local-day-vs-UTC-day decision verified against real timezone-variability data (24/61 participants
      multi-timezone), not assumed
- [x] Eligibility thresholds verified against Structured's own local-day distributions (43/61 and 38/61),
      not copied from DS5's differently-defined `MIN_DAYS=7`
- [x] New Fano-factor burstiness metric justified as count-process-specific, not previously used in DS5
- [x] Phenotype labels are explicitly rule-based/descriptive, not a Step 2 clustering claim
- [x] Notebook 63 implemented and executed
