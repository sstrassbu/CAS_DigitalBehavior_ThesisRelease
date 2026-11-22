# DS4 StoP Model — Stage 4 Step 1 Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**
**Written:** 2026-08-06
**Status: IMPLEMENTED — approved and completed 2026-08-06.** See
`outputs/model_outputs/ds4_stochastic_processes/model_run_summary.md` for actual
executed results. Blueprint preserved below as the pre-registration record; unmodified
except for this status line.
**Notebook (to be created):** `notebooks/53_ds4_stochastic_processes.ipynb`
**Generator script (to be created):** `notebooks/make_53_ds4_stop.py`
**Producing dataset:** DS4 — Large Naturalistic OneSec Users (N=1,039)
**Model family:** Stochastic Processes (StoP)
**Prerequisites:** None — this is the first DS4 model. InT(52), DyS(55), and StM(51) all
depend on this notebook's output; NeT(54) does not.

---

## 1. Why DS4 needs its own StoP model, not DS5's

DS5's StoP notebook (`43_ds5_stochastic_processes.ipynb`) used a **constant-drift SDE**:

```
dX_t = μ dt + σ dW_t
```

This was a deliberate simplification (FLAG 1 in that notebook), forced by DS5's short
observation windows (7–45 days). A mean-reversion parameter θ cannot be reliably
estimated from windows that short — there simply aren't enough independent return-to-
baseline cycles to observe.

DS4's windows extend up to 897 days (median 66, mean 97) across all event classes; on the
`intervention_event` rows that actually form X_t the span is max 165 days (median 65, mean
62), giving a median of 57 observed daily X_t values per participant. This makes an
**Ornstein–Uhlenbeck (OU) process** — a genuinely different, richer model, not a
DS5 port — potentially identifiable for the first time in this project:

```
dX_t = θ(μ − X_t) dt + σ dW_t
```

θ (mean-reversion rate), μ (long-run mean / interior fixed point), and σ (diffusion) are
all estimated per participant. This is DS4's central methodological upgrade over DS5 and
the reason DS4 StoP must be implemented before InT/DyS/StM: all three of those consume
θ̂/σ̂/μ̂ directly (H_SDE bridge, regime partition, rigorous β_OU respectively — see
`ds4_stm_blueprint.md` §1, written 2026-04-17 anticipating this dependency).

---

## 2. DS4 structural notes — required reading, restated here for this notebook

These are DS4's own confirmed facts (from `data_docs/modeling_cautions.md` §6,
`outputs/cleaned/ds4_behavioral_clean.md`, and `outputs/reports/stage0/ds4_audit_report.md`)
— not assumptions carried from DS5.

### 2.1 Event class — use `intervention_event` only

DS4 logs three structurally different event classes:
- `intervention_event` (36.5%, 909,948 rows): active friction shown; has interventionType
  + interventionDuration
- `app_close_event` (47.1%): closedApp outcome only; no intervention fields; may reflect a
  different logging path entirely
- `no_intervention` (16.4%): opened/dismissed without friction logged

**The state variable must use `intervention_event_class == 'intervention_event'` rows
only, with outcome in `{opened, dismissed}`.** Do not use `rate_opened_all` — it mixes
friction and non-friction events and would conflate three different behavioral contexts
into one series.

### 2.2 Time axis

Use `timestamp_utc` (already parsed, zero failures) to build calendar-day bins. Do
**not** use `secondsSinceStudySetup` / `weeksSinceStudySetup` — the Stage 0 audit
confirmed these are entirely non-positive and encode a per-participant backward-counting
anchor, not forward time (see `ds4_audit_report.md` §6).

### 2.3 No experimental condition

DS4 has no RCT — participants self-selected into using OneSec. There is no control
group and no condition variable. All StoP results describe within-participant dynamics
and cross-participant heterogeneity, never a "condition effect." This is a structural
fact of the dataset, not a limitation of this notebook specifically — it propagates to
every downstream DS4 model too.

---

## 3. FLAG decisions

| Flag | Decision | Justification |
|---|---|---|
| **FLAG 1 — process type** | OU: `dX_t = θ(μ−X_t)dt + σdW_t` | DS4's long windows make θ potentially identifiable, unlike DS5. This is the dataset's whole reason for a dedicated StoP model rather than reusing DS5's. |
| **FLAG 2 — estimation method** | Closed-form conditional MLE via ordinary least squares (OLS) regression of `X_{t+1}` on `X_t`, restricted to consecutive-day pairs (gap = 1 day) | The exact discrete-time OU transition at fixed Δt is `X_{t+1}\|X_t ~ N(μ+(X_t−μ)e^{-θΔt}, σ²(1−e^{-2θΔt})/(2θ))` — an AR(1) process. For Δt=1 (consecutive days), OLS on `X_{t+1} = c + φX_t + ε` **is** the conditional MLE in closed form (Gaussian innovations, linear-Gaussian model) — no numerical optimizer needed, and no approximation is introduced by using it. Verified 96.16% of all day-to-day pairs in DS4 are consecutive (gap=1), so restricting to them costs little data. Non-consecutive pairs are dropped rather than assumed to follow the same fixed-Δt transition, which would be wrong for irregular gaps. |
| **FLAG 3 — MIN_DAYS threshold** | 30 distinct daily X_t observations per participant, and ≥10 usable consecutive-day pairs after the gap filter | Verified against real data (not estimated): 1,036/1,039 participants have ≥1 intervention-outcome day at all; 786/1,039 (75.6%) meet the 30-day threshold; of those, 785 retain ≥10 consecutive-day pairs (1 participant drops for insufficient consecutive pairs despite meeting the day-count threshold). |
| **FLAG 4 — invalid-fit handling** | Participants whose OLS slope φ̂ falls outside (0,1) — a unit root (φ̂≥1, non-reverting/random-walk-like) or an oscillating fit (φ̂≤0) — get NaN for θ̂_OU/σ̂_OU/τ̂. Excluded from downstream models, not imputed. | Verified: of 785 fit attempts, 641 (81.7%) produce a valid 0<φ̂<1 fit. The 18.3% invalid-fit rate is reported explicitly, not smoothed over — matches this project's established "do not impute below-threshold participants" convention (see `ds5_structural_discoveries.md` MIN_DAYS precedent). |
| **FLAG 5 — daily event-count floor** | No additional per-day minimum-event filter; use all days with ≥1 outcome-bearing intervention event | Checked as an explicit robustness test rather than assumed: re-fitting with a floor of ≥1/≥3/≥5 events-per-day before including that day gives median θ̂ = 1.587 / 1.464 / 1.378 respectively (see §4). The result is not a low-count noise artifact of days with only 1–2 events, so no floor is applied by default. |

---

## 4. Headline empirical finding — read before assuming anything about τ

**DS4's daily override-rate mean-reverts very fast: median τ̂ = 1/θ̂ ≈ 0.63 days.**

This is a real, computed result (see verification table below), not an assumption
carried over from planning documents written before any DS4 OU fit existed. In
particular, `ds4_stm_blueprint.md` §4 (written 2026-04-17, before this notebook existed)
used "if τ̂ = 14 days..." as an *illustrative* example of what an OU relaxation time
might mean behaviorally — that was a hypothetical, not a prediction, and the real number
is nearly 2 orders of magnitude faster.

| Quantity | Value |
|---|---|
| Total DS4 participants | 1,039 |
| Participants with ≥1 intervention-outcome day | 1,036 |
| Eligible at MIN_DAYS=30 | 786 (75.6%) |
| Of those, retain ≥10 consecutive-day pairs | 785 |
| Valid mean-reverting fit (0<φ̂<1) | 641/785 (81.7%) |
| Median θ̂_OU (mean-reversion rate, /day) | 1.587 |
| Median τ̂ = 1/θ̂_OU (days) | **0.63** |
| Median σ̂_OU | 0.290 |
| Median θ̂ with ≥3-event/day floor | 1.464 (τ≈0.68d) |
| Median θ̂ with ≥5-event/day floor | 1.378 (τ≈0.73d) |

**Two honest readings, both stated in the notebook, neither silently preferred:**

1. **Genuine fast habitual reversion.** Naturalistic override behavior may snap back to
   a personal baseline within about a day — consistent with habit-driven, largely
   automatic app-checking rather than a slowly-drifting psychological state.
2. **Daily aggregation is a noisy ratio even at moderate counts.** `X_t` is
   `n_opened/n_events` on a typical day of ~11 intervention events (median). Even though
   the event-count-floor sensitivity check (§3, FLAG 5) rules out *very* low counts as
   the driver, day-to-day sampling noise in a ratio-of-small-counts variable will always
   look more "mean-reverting" than a smoothly drifting latent state would.

The notebook includes a **weekly-aggregation sensitivity check** (cell 14) specifically
to help distinguish these two readings — if weekly θ̂ is dramatically slower than daily
θ̂, reading 2 is favored; if it stays fast, reading 1 gains support. This is not resolved
in this blueprint; it is resolved with the notebook's own output, and reported either
way.

---

## 5. State variable and estimator — technical specification

```python
# State variable construction
df = beh[beh["intervention_event_class"] == "intervention_event"].copy()
df = df[df["event_outcome_simple"].isin(["opened", "dismissed"])].copy()
df["opened_flag"] = (df["event_outcome_simple"] == "opened").astype(int)
df["event_date"] = df["timestamp_utc"].dt.date

daily = df.groupby(["participant_id_canonical", "event_date"]).agg(
    n_opened=("opened_flag", "sum"),
    n_events=("opened_flag", "count"),
).reset_index()
daily["X_t"] = daily["n_opened"] / daily["n_events"]
daily["event_date"] = pd.to_datetime(daily["event_date"])
daily = daily.sort_values(["participant_id_canonical", "event_date"])
```

```python
# Per-participant OU fit via AR(1) OLS on consecutive-day pairs
def fit_ou_participant(g: pd.DataFrame) -> dict:
    """g: one participant's daily X_t rows, sorted by event_date."""
    n_days = len(g)
    gap = g["event_date"].diff().dt.days
    x_t = g["X_t"].values[:-1]
    x_t1 = g["X_t"].values[1:]
    consec = (gap.values[1:] == 1)
    x_t, x_t1 = x_t[consec], x_t1[consec]
    n_pairs = len(x_t)

    out = dict(n_days_obs=n_days, n_consec_pairs=n_pairs,
               mu_hat_OU=np.nan, theta_hat_OU=np.nan, sigma_hat_OU=np.nan,
               tau_hat=np.nan, phi_hat=np.nan, fit_valid=False)
    if n_days < 30 or n_pairs < 10:
        return out

    X = np.column_stack([np.ones_like(x_t), x_t])
    coef, *_ = np.linalg.lstsq(X, x_t1, rcond=None)
    c, phi = coef
    out["phi_hat"] = phi
    if not (0 < phi < 1):
        return out  # unit-root or oscillating fit — not mean-reverting

    resid = x_t1 - X @ coef
    v = resid.var(ddof=2)
    theta = -np.log(phi)
    mu = c / (1 - phi)
    sigma2 = 2 * theta * v / (1 - phi ** 2)

    out.update(mu_hat_OU=mu, theta_hat_OU=theta, sigma_hat_OU=float(np.sqrt(max(sigma2, 0))),
                tau_hat=1 / theta, fit_valid=True)
    return out
```

---

## 6. Theory-to-data mapping

| Theoretical quantity | DS4 variable / derived quantity | Mapping type | Confidence |
|---|---|---|---|
| State variable X_t | `n_opened / n_events` per day, `intervention_event` class only | Proxy — behavioral rate, not a latent psychological state | Medium (same proxy caveat as every OneSec dataset in this project) |
| OU drift μ | `mu_hat_OU` — unconditional mean of X_t implied by the AR(1) fit | Direct reuse | High for valid fits (786-eligible sample) |
| Mean-reversion rate θ | `theta_hat_OU` from AR(1) OLS | New parameter — estimated, not assumed | Medium — real, verified estimate; interpretation (habit vs. noise) is open, see §4 |
| Diffusion σ | `sigma_hat_OU` from AR(1) residual variance | Estimated | Medium-High |
| Relaxation time τ | `tau_hat = 1/theta_hat_OU` (days) | Direct transform | High as a number; behavioral interpretation flagged open in §4 |

---

## 7. Notebook structure — `notebooks/53_ds4_stochastic_processes.ipynb`

| Cell | Type | Content |
|---|---|---|
| 1 | Markdown | Scope statement: OU model, why DS4 not DS5, what InT/DyS/StM need from this notebook |
| 2 | Markdown | FLAG decisions table (§3) |
| 3 | Markdown | DS4 structural cautions (event class, time axis, no condition — §2) |
| 4 | Markdown + LaTeX | OU SDE theory: `dX_t=θ(μ−X_t)dt+σdW_t`, stationary distribution `N(μ,σ²/2θ)`, discrete AR(1) equivalence at fixed Δt |
| 5 | Markdown | Theory-to-data mapping table (§6) |
| 6 | Code | Setup: imports, paths, constants (`MIN_DAYS=30`, `MIN_PAIRS=10`) |
| 7 | Code | Load `ds4_behavioral_clean.csv`; build daily X_t (§5 state-variable snippet) |
| 8 | Code | Per-participant OU fit loop (§5 estimator snippet); build `participant_parameters` for all 1,039 participants (NaN rows where `fit_valid=False`) |
| 9 | Code | Eligibility funnel report: total → ≥1 outcome day → MIN_DAYS met → ≥10 consec pairs → valid mean-reverting fit |
| 10 | Code | Distribution summaries: μ̂_OU, θ̂_OU, σ̂_OU, τ̂ — mean/median/percentiles |
| 11 | Code | Weakness-flag reporting: % excluded at each funnel stage; % invalid fits, with a φ̂ histogram showing the unit-root vs. oscillating split |
| 12 | Code | Sensitivity check: re-fit with daily event-count floors (1/3/5); reproduce the §4 robustness table from real output |
| 13 | Code | Export `participant_parameters.csv`, `ds4_stop_summary.csv`, `model_run_summary.md` |
| 14 | Code | Sensitivity check: re-run the fit on **weekly**-aggregated X_t (ISO week, sum opened / sum events); export `participant_parameters_weekly_sensitivity.csv` |
| 15 | Code | Figure 1: θ̂_OU distribution (histogram) |
| 16 | Code | Figure 2: τ̂ distribution (histogram, log-x given the sub-day median) |
| 17 | Code | Figure 3: μ̂_OU vs σ̂_OU scatter, colored by τ̂ |
| 18 | Code | Figure 4: daily-θ̂ vs weekly-θ̂ scatter per participant — direct visual of the §4 sensitivity question |
| 19 | Markdown | Interpretation and limits — state the fast-reversion finding plainly with both readings from §4; recommend the weekly view as the more conservative headline number if daily/weekly θ̂ diverge sharply |
| 20 | Markdown | Forward connections — what InT(52)/DyS(55)/StM(51) each consume from this output |

---

## 8. Proposed outputs

**Output root:** `outputs/model_outputs/ds4_stochastic_processes/`

| File | Description | Rows |
|---|---|---|
| `participant_parameters.csv` | All 1,039 participants: `n_days_obs`, `n_consec_pairs`, `phi_hat`, `mu_hat_OU`, `theta_hat_OU`, `sigma_hat_OU`, `tau_hat`, `fit_valid` | 1,039 |
| `participant_parameters_weekly_sensitivity.csv` | Same schema, weekly-aggregated X_t | ~1,039 (fewer valid) |
| `ds4_stop_summary.csv` | Eligibility funnel counts + distribution percentiles | 1 |
| `model_run_summary.md` | Full run record with actual executed numbers | — |
| `figures/fig1_ds4_theta_distribution.png` | θ̂_OU histogram | — |
| `figures/fig2_ds4_tau_distribution.png` | τ̂ histogram (log-x) | — |
| `figures/fig3_ds4_mu_sigma_scatter.png` | μ̂_OU vs σ̂_OU, colored by τ̂ | — |
| `figures/fig4_daily_vs_weekly_theta.png` | Daily vs weekly θ̂ sensitivity scatter | — |

---

## 9. DS4 weakness flags

### ⚠ FLAG I: No experimental condition

DS4 is observational. All StoP results are within-participant or cross-participant
heterogeneity descriptions, never a friction/condition effect.

### ⚠ FLAG II: Self-selected users — attrition confound

Long-window participants (eligible at MIN_DAYS=30) are those who kept using OneSec.
This is not a random subsample of all 1,039 participants — it may be systematically
different from the 253 participants excluded by the threshold.

### ⚠ FLAG III: Fast θ̂ interpretation is open, not resolved

The median sub-day relaxation time may reflect genuine fast habitual reversion, or may
reflect that a daily ratio-of-counts is inherently noisy even after ruling out very-low-
count days (§3 FLAG 5). The weekly-aggregation check (cell 14/18) is reported as
evidence either way, not as a resolution baked into this blueprint.

### ⚠ FLAG IV: 18.3% invalid-fit rate

Nearly one in five eligible participants (144/785) produce no valid mean-reverting fit
(φ̂ outside (0,1)). This is reported explicitly in the funnel (cell 9/11), not absorbed
silently into the "eligible" count. Downstream models (InT/DyS/StM) inherit this same
loss.

### ⚠ FLAG V: Behavioral proxy limitation persists

`X_t` is a behavioral override rate, not a latent psychological state. The OU model's
mathematical elegance does not change this — same caveat as every StoP/StM model in this
project (see `ds4_stm_blueprint.md` §8 FLAG V for the DS5-parallel statement).

---

## 10. Forward connections

| Connection | Mechanism | Target |
|---|---|---|
| DS4 StoP → DS4 InT | σ̂_OU feeds the H_SDE Gaussian-entropy bridge, same construction as DS5's H_SDE from σ̂ | `52_ds4_information_theory.ipynb` |
| DS4 StoP → DS4 DyS | θ̂_OU/σ̂_OU partition participants into regimes; OU gives a true interior fixed point X*=μ̂_OU (not the boundary-only fixed point DS5 DyS was limited to) | `55_ds4_dynamical_systems.ipynb` |
| DS4 StoP → DS4 StM | μ̂_OU, θ̂_OU, σ̂_OU feed the rigorous β_OU=2θ̂/σ̂² Boltzmann bridge | `51_ds4_statistical_mechanics.ipynb` (blueprint already written, `ds4_stm_blueprint.md`) |
| DS4 StoP → Paper | OU SDE, discrete AR(1) equivalence, θ/τ interpretation are not yet in the conceptual paper — must be added alongside the DS4 StM additions already flagged in `ds4_stm_blueprint.md` §4 |

---

## ⚠ IMPLEMENTATION HOLD (historical — resolved 2026-08-06)

This hold applied during blueprint review and has since been cleared; the notebook was
approved and implemented. Kept below for the historical record.

When the user approves:
1. Create `notebooks/make_53_ds4_stop.py` (generator script, same pattern as `make_41_stm.py`)
2. Run generator to create `notebooks/53_ds4_stochastic_processes.ipynb`
3. Execute notebook; verify all outputs against §4's pre-registered numbers
4. Write companion `.md` docs for every output file (CLAUDE.md output-documentation rule)
5. Update `memory/project_stage.md` and `memory/cross_dataset_strategy.md` with DS4 StoP status
6. Move to DS4 InT (52) blueprint — informed by this notebook's real executed output, not
   written in advance
