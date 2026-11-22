# DS6 — Dynamical Systems (DyS) Blueprint

**Notebook:** `notebooks/72_ds6_dynamical_systems.ipynb`
**Written:** 2026-08-06
**Position:** 72 in the DS6 70s decade. Depends on StoP (73, for mu_hat/sig_hat — the σ→0
reduction target) and InT (75, for H_emp — the bridge validation), both complete.
**Depends on:** `outputs/model_outputs/ds6/stochastic_processes/participant_stop_parameters.csv`,
`outputs/model_outputs/ds6/information_theory/participant_entropy_metrics.csv`
**Output root:** `outputs/model_outputs/ds6/dynamical_systems/`

---

## Part 0 — Why this is not a DS5 port

DS5's DyS notebook took the σ→0 limit of its own StoP SDE (`dX_t = μ dt + σ dW_t`, X
bounded in [0,1]) to get a deterministic ODE `dX/dt = μ`. Because X is bounded on BOTH
sides, a nonzero μ drives the trajectory to a **boundary** fixed point (0 or 1) — hence DS5's
careful terminology "predicted_boundary_fp," not "attractor."

DS6's StoP state variable is different in a way that matters here specifically: `N_t` is a
**daily attempt count, bounded below at 0 but with no upper bound.** Taking the same σ→0
limit (`dN/dt = mu_hat`, constant drift) on this state space gives a **structurally
asymmetric** picture that DS5's framing does not cover:

- `mu_hat` significantly negative → deterministic trajectory drifts toward the **floor at
  N=0** (a real boundary — can't have negative attempts). This is DS6's analog of DS5's
  boundary fixed point, but only on one side.
- `mu_hat` significantly positive → deterministic trajectory drifts **upward with no
  ceiling**. There is no boundary to get "stuck" at — unbounded growth in the deterministic
  limit. DS5 has no equivalent regime (both its boundaries are reachable).
- `mu_hat` ≈ 0 → trajectory hovers near an **interior resting level** (`mean_N`), a genuine
  classical fixed point (`dN/dt=0`), not a boundary approximation.

This three-way asymmetric structure — floor-bound, unbounded-growth, and interior-resting
— is DS6-specific and is the core design decision of this blueprint, not present in DS5's
symmetric [0,1] case.

---

## Part 1 — Theory grounding (paper §2.2, quoted directly)

> "State-space variables: Possible variables include attempt volume, opening rate, dismissal
> rate, target-app concentration, time since prior attempt, repeated-override rate, and
> condition exposure."
>
> "System stability: The model asks whether users fall into stable response attractors,
> oscillate between regimes, rebound, or drift toward disengagement."

DS6 cannot use "dismissal rate" or "repeated-override rate" (no outcome variance). Uses the
paper's first-named variable directly: **attempt volume** — exactly StoP's `N_t`.

---

## Part 2 — Regime classification (per participant × period)

**Step 1 — deterministic vs. stochastic (σ threshold), computed separately per period:**

```
sigma_threshold_baseline     = median(sig_hat_baseline)   across DyS-eligible participants
sigma_threshold_intervention = median(sig_hat_intervention)
is_dys_eligible_<period>     = sig_hat_<period> < sigma_threshold_<period>
```

**Per-period threshold, not one pooled threshold — a deliberate departure from DS5's single
pooled median.** StoP (73) already found baseline sig_hat is systematically higher than
intervention sig_hat, partly a real effect and partly a window-length precision artifact
(baseline ~15 days vs intervention ~28 days — StoP's own "Estimation-precision caution").
A single pooled threshold would conflate that artifact with genuine regime classification
(baseline participants would be mechanically over-represented in the "stochastic" bucket).
Per-period thresholds control for this.

**Step 2 — within the deterministic-eligible group, sub-classify by drift sign/magnitude**
(reuses StoP's `MU_THRESHOLD=0.5` attempts/day, not a new threshold):

```
if not is_dys_eligible:                      regime = "stochastic"
elif mu_hat < -MU_THRESHOLD:                  regime = "declining"    (drifts to floor)
elif mu_hat > +MU_THRESHOLD:                  regime = "growing"      (unbounded drift)
else:                                         regime = "resting"      (interior fixed point)
```

---

## Part 3 — Regime transitions across the baseline→intervention boundary

**DS6-specific — no DS5 equivalent** (DS5 only compares regimes between-subject across
RCT conditions; DS6 additionally has a real within-participant before/after design, matching
the pattern established by StoP's `h_period` and NeT's `hhi_change`). Build a 4×4 contingency
table of `regime_baseline × regime_intervention` for the ~230 participants eligible in both
periods (per StoP's own eligibility count). Open question, not assumed: do participants
mostly stay in the same regime, or does the intervention period shift them (e.g.,
"growing"→"declining", consistent with StoP's own already-found mean volume drop)?

---

## Part 4 — Bridge to InT: regime vs H_emp

Same bridge logic as DS5's DyS notebook (`stage4_implementation_plan.md`: "DyS-det mean
H_emp=1.75 vs StoP-stoch H_emp=2.32"). Prediction, stated before running: deterministic-regime
participants (`is_dys_eligible=True`) should show LOWER `H_emp` (from InT, notebook 75) than
stochastic-regime participants, since low diffusion should correspond to a more predictable
(lower-entropy) daily count series. Tested per period, not assumed.

---

## Part 5 — Output file structure

```
outputs/model_outputs/ds6/dynamical_systems/
  participant_regime_classification.csv   # one row per participant: regime_<period>,
                                           # is_dys_eligible_<period>, sigma_threshold_<period>,
                                           # mu_hat/sig_hat (reused from StoP), study_condition
  regime_transition_matrix.csv            # 4x4 baseline-x-intervention regime contingency table
  regime_int_bridge.csv                   # regime vs H_emp comparison, per period
  condition_regime_summary.csv            # study_condition x study_period x regime counts
  figures/
    fig1_dys_regime_distribution.png
    fig2_dys_regime_transition_heatmap.png
    fig3_dys_regime_hemp_bridge.png
    fig4_dys_mu_sigma_regime_scatter.png
  model_run_summary.md
```

Each CSV gets its own companion `.md` file, per the documentation convention established
2026-08-06 (see StoP/NeT/InT companion docs and the memory note recording this as the
standard going forward, not just for InT).

---

## Implementation readiness checklist

- [x] Confirmed DS6's N_t is floor-bound/ceiling-free, unlike DS5's double-bounded [0,1] X_t
      — the asymmetric regime structure (declining/growing/resting) is derived from this,
      not copied from DS5's boundary-fp framing
- [x] Paper §2.2 quoted directly; "attempt volume" is the paper's own first-listed state variable
- [x] Per-period σ threshold justified by StoP's own already-documented window-length caveat,
      not an arbitrary design choice
- [x] Regime-transition analysis identified as DS6-specific (within-participant), not a
      DS5-equivalent feature
- [x] InT bridge (regime vs H_emp) stated as a testable prediction before running
- [x] Notebook 72 implemented and executed. Headline: regime shift independently confirms
      StoP's "level moved, trend didn't" finding — baseline "declining" (30) nearly vanishes
      in intervention (2), but intervention is dominated by "resting" (95, up from 51), not
      decline, consistent with a between-period level shift rather than a within-period
      declining trend. DyS-InT bridge prediction confirmed both periods (p=2.5e-06,
      p=1.5e-04). Flagged an interpretive caution: MU_THRESHOLD is absolute, so window-length
      differences in mu_hat estimation precision likely contribute to the "resting" surge.
      See `outputs/model_outputs/ds6/dynamical_systems/model_run_summary.md`.
