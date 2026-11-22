# Theory vs. Implementation Comparison — DS6 Model Families

**Written:** 2026-08-08
**Overlap check:** Read in full — `outputs/reports/stage4/post_analysis/theory_vs_implementation_comparison.md`
(DS5 template, mirrored here), `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md`
§2 (cross-dataset per-family findings — cited, not re-derived), `outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md`.
**Scope of this file:** DS6-only theory-to-implementation fidelity, at a level of numerical
and mechanistic detail the cross-dataset synthesis does not attempt (that document compares
DS6 to three other datasets at the headline-finding level; this document traces each DS6
family's own blueprint decisions against the paper's text).

---

## Background

DS6 shares the same generic OneSec theory-paper sections as DS5 (§1.3, §2.1–2.8 are written
generically across all OneSec-family datasets, unlike Structured, which needed its own
paper). But DS6 cannot use the paper's outcome-dependent operationalizations at all — DS6's
behavioral log contains **only `openedApp`** events, confirmed structural on the full raw
file (`data_docs/modeling_cautions.md` §6). Every DS6 family blueprint therefore opens with
an explicit "why this cannot be a DS5 port" section, quoting the paper's own alternative
operationalization directly rather than inventing one. This document's central theme is
**how faithfully each DS6 family followed its own quoted alternative**, not how closely it
resembles DS5's implementation — resemblance to DS5 is often the wrong standard here.

---

## StoP — Stochastic Processes

### Theory intended

Paper §1.3, quoted directly in the blueprint: *"Stochastic Processes are also feasible
because event logs can be aggregated into user-day or user-week time series, such as **daily
attempt count**, daily dismissal rate, daily opening rate, or daily friction-success rate."*
DS6 uses the first of these four named fallbacks — the only one not requiring the missing
outcome variable.

### What was implemented

- State variable: `N_t` = daily app-opening attempt count, zero-filled, fit **separately per
  `study_period`** (baseline/intervention) rather than per RCT condition
- Constant-drift method-of-moments estimation (`mu_hat`, `sig_hat`) — same estimator family as DS5/Structured
- `h_period = mu_hat_intervention − mu_hat_baseline` — a within-participant drift-shift quantity with no DS5 equivalent (DS5's `h_c` is between-condition)
- `MU_THRESHOLD` rescaled from DS5's `0.005` to `0.5` (attempts/day), with an explicit stated proportional-equivalence rationale (~1.4% of DS6's mean daily count vs. DS5's 0.005 being ~1–1.7% of a typical override rate)

### Assessment

**Theory-faithful in the strongest sense available for DS6:** the state variable is the
paper's own named fallback, quoted directly, not an ad hoc substitute. **Not a DS5 port**:
count vs. rate is a different mathematical object (unbounded below-only vs. bounded [0,1]),
and the comparison axis is within-participant period rather than between-subject condition.
This is closer in spirit to Structured's own count-based StoP than to DS5's rate-based one,
but is explicitly not a Structured port either — DS6 additionally has the baseline/
intervention period structure Structured's naturalistic (no-condition) design lacks.

**Genuine finding, independently confirmed:** mean daily attempt volume drops from 45.1 to
29.1 events/day (level effect), cross-validating the pre-existing Stage 1
`event_rate_ratio_intervention_vs_baseline` feature via an entirely different estimation
method (a zero-filled daily grid + method of moments, vs. a simple ratio of period means).
`h_period` (the trend/drift shift) is **not** significant (paired t p=0.659) — level moved,
trend did not.

**Main caveat to defend:** the baseline window (~15 days) is roughly half the intervention
window (~28 days), so `sig_hat`/`Fano_factor` are estimated from about half as many daily
increments in baseline — the observed baseline > intervention Fano gap (median 6.58 vs 3.34)
could partly reflect this precision asymmetry, not a purely behavioral difference. Flagged
explicitly in the model_run_summary and carried forward as an open caveat into DyS.

---

## NeT — Network Theory

### Theory intended

Paper §2.4, quoted directly: nodes may be "target apps, app categories, outcome states, or
combined app-outcome states"; edges are "consecutive observed One Sec events," to be
"interpreted as temporal adjacencies, not causal effects." DS6 cannot use outcome-based node
types (no outcome variance) — uses the paper's other named option, target apps, matching the
paper's own Example A illustration exactly.

### What was implemented

- Nodes = target apps: a small, closed, **10-app global vocabulary** (mean 3.65 apps/participant) — verified via `app_name.nunique()` on the full file, not assumed
- Edges: self-derived via `shift(-1)` on time-sorted rows within participant × period — the notebook went further than its own blueprint's stated plan (which specified building edges from `app_prev[t] → app_name[t]`) and instead trusted neither `app_prev` nor `app_next`, matching DS5's own NeT technique exactly
- `HHI_net`, `rho_self`, `H_trans`, stationary distribution `π` — same formal definitions as DS5's NeT
- `MIN_TRANSITIONS = 20` per period — reused directly from DS5's own NeT threshold, not re-derived, since DS6's median transition count (521–629/period) vastly exceeds it

### Assessment

**Theory-faithful, and with an extra layer of caution beyond the blueprint's own plan:**
before any node/edge design work, the notebook verified that `app_next` — which would have
been the obvious pre-engineered field to use — mechanically echoes the current row's own
`app_name` 99.3% of the time and does **not** represent a real subsequent app choice (full
detail in `ds6_bug_discoveries_and_fixes_chronicle.md`, item b). Having found that, the
implementation chose not to fully trust `app_prev` either (despite `app_prev` being
separately verified genuine), and self-derived transitions from raw row order instead — a
more conservative choice than strictly required by the verification result, and the same
choice DS5's own NeT notebook made independently.

**Structural, not implementation-driven, divergence from DS1/DS4/DS5:** DS6's 10-app
vocabulary is far smaller than DS1 (48 apps) or DS4 (399 apps) — closer to Structured's own
small (7-state) vocabulary. The blueprint explicitly pre-registered the expectation that this
would push `HHI_net` toward ceiling "independent of any behavioral effect." **Only partly
confirmed:** observed `HHI_net` is moderate (~0.50 both periods), not pushed to ceiling —
reported honestly rather than reframed to match the pre-registered expectation.

**Genuine cross-model finding:** `corr(HHI_net change, daily-volume change) = −0.213,
p=0.0012` — participants who cut usage back more under the intervention show a larger
increase in network concentration over the same period. This required both StoP's (73) and
NeT's (74) outputs to exist; neither notebook alone could have found it.

---

## InT — Information Theory

### Theory intended

Paper §2.5, quoted directly: "Entropy can be computed for target app, resolution code, time
of day, condition-specific outcomes, app category, or user-day response states." DS6 cannot
use "resolution code," "condition-specific outcomes," or MI toward "opening versus
dismissal" — uses "target app," "time of day," and "user-day response states" (StoP's `N_t`).

### What was implemented

- `H_app`, `H_hour`, `H_emp`, `H_SDE` — all computed, all **split by `study_period`** (a
  DS6-specific consistency requirement StoP and NeT already established; DS5 has no period
  axis to split by)
- `H_out` — **excluded entirely**, not computed-and-discarded: a single-category outcome
  distribution has entropy ≡ 0 by construction, not a measurement worth reporting
- `H_emp` binning: **K=10 quantile bins per participant** (FLAG InT-1), not DS5's fixed
  [0,1]-range bins, because `N_t` is an unbounded 1–333/day count with no natural global range
- New: pooled `MI(study_period; app_name) = 0.0003` bits — a measure DS5 declined entirely
  (FLAG 4, "MI/KL deferred"). Justified by a direct link to NeT's already-completed
  concentration finding, not scope creep for its own sake.

### Assessment

**High theory faithfulness, with two structurally forced divergences from DS5 (not
approximations, exclusions):** `H_out`'s absence is not a simplification — it is the correct
response to a distribution that literally carries zero information in this dataset. The
quantile-binning change for `H_emp` is a direct, necessary consequence of the state variable
being unbounded; DS6's `H_emp` values are consequently **not directly comparable in absolute
terms** to DS5's `H_emp` (different variable, different binning scheme) — stated explicitly
in the model_run_summary's Known Limitations, not left implicit.

**H_SDE bridge is theory-faithful but still not in the conceptual paper** — same gap DS5's
InT notebook already flagged (`H_SDE = ½log₂(2πe·σ̂²)` is a real derived bridge, unformalized
in the paper text). Confirmed empirically here too: r(H_SDE, H_emp) = 0.583 (baseline,
p=6.9e-23) / 0.719 (intervention, p=6.7e-39) — support for the Gaussian-increment assumption
behind StoP's method-of-moments estimator, on independent (DS6) data.

**Bridge implementation required two failed attempts before it was trustworthy** (see
`ds6_bug_discoveries_and_fixes_chronicle.md`, item c) — the mandatory `I_consec >= 0` gate did
its job exactly as intended, catching both a Stage-1-feature boundary mismatch and a
wrong-marginal error before either result was published.

**New MI test is a genuine, honestly-reported null**: pooled `MI(study_period; app_name) =
0.0003` bits does not contradict NeT's per-participant `HHI_net`-volume finding — different
participants narrow toward different favorite apps, so no population-level shift in the app
distribution needs to occur for every individual to still be narrowing toward their own.

---

## DyS — Dynamical Systems

### Theory intended

Paper §2.2, quoted directly: state-space variables may include "attempt volume, opening
rate, dismissal rate, target-app concentration, time since prior attempt, repeated-override
rate, and condition exposure." DS6 cannot use "dismissal rate" or "repeated-override rate" —
uses the paper's first-named variable, attempt volume, directly (= StoP's `N_t`).

### What was implemented

- σ→0 limit taken on `N_t` (bounded below at 0, **no ceiling**) instead of DS5's [0,1]-bounded
  `X_t` — this produces a **structurally new, asymmetric 3-way regime space**
  (`declining`/`growing`/`resting`) that DS5's double-bounded case cannot produce at all, not
  a simplification of DS5's boundary-fixed-point framing
- Per-period σ threshold (median split computed separately for baseline and intervention),
  a deliberate departure from DS5's single pooled threshold, justified directly by StoP's own
  documented window-length asymmetry
- `MU_THRESHOLD = 0.5` reused unchanged from StoP (73), not re-derived a second time
- `regime_transition_matrix.csv` — a 4×4 within-participant contingency table with no DS5
  equivalent (DS5 only compares regimes between RCT arms)

### Assessment

**This is DS6's single largest genuinely new piece of theoretical territory relative to DS5
— not a simplification, an extension.** DS5's careful "predicted_boundary_fp" terminology
exists specifically because a bounded-both-sides state variable only ever settles at one of
two boundaries under the deterministic limit. DS6's floor-only bound produces a third,
qualitatively different possibility (unbounded upward drift, "growing") that has literally no
DS5 analog to be compared against or ported from.

**Independently confirms StoP's own headline finding via a different method:** baseline
"declining" (30 participants) nearly vanishes in intervention (2), but intervention is
dominated by "resting" (95, up from baseline's 51) — consistent with StoP's "level moved,
trend didn't" finding, from a completely different (categorical regime, not continuous
drift) analytical angle.

**Main caveat, explicitly flagged, not resolved:** `MU_THRESHOLD` is an absolute cutoff, and
`std(mu_hat_baseline)=3.036` vs. `std(mu_hat_intervention)=0.964` — window-length differences
in estimation precision likely inflate the "resting" surge in intervention alongside any real
behavioral narrowing. Stated as an open confound, inherited from StoP's own already-flagged
window-length caveat, not silently absorbed into the regime-shift interpretation.

**Confirmed pre-registered bridge prediction:** deterministic-regime participants show
significantly lower `H_emp` than stochastic-regime participants, both periods (p=2.5e-06
baseline, p=1.5e-04 intervention) — an independent validation using InT's entropy measure.

---

## StM — Statistical Mechanics

### Theory intended

Paper §2.1, quoted directly: configuration properties include "condition, target app, time,
prior attempts, and resolution code"; the paper explicitly cautions that "physical quantities
such as energy or temperature are not directly observed... [and] should be treated as
behavioral analogies... not literal measurements." DS6 cannot use "resolution code" or "prior
attempts/outcome" — uses "target app" and "time" directly.

### What was implemented

- Microstate = joint (`app_name`, `hour_bucket`) — the paper's other two named configuration
  properties, matching the exact bucket boundaries already established in Stage 1
- **No β/T/Z/F apparatus at all** — the single largest deliberate divergence from DS5 in
  the entire DS6 program. DS6 follows Structured's own precedent of declining this apparatus,
  but for an even more direct reason: DS5's `β_behav = 2/σ̂²` bridge presumes a state variable
  that plausibly approximates a two-state [0,1] occupation probability; DS6's StoP state
  variable is not bounded on the upper side at all, so the analogy does not hold even loosely
- Does **not depend on StoP's output** at all — a genuine data-usage divergence from DS5's
  StM, which is built entirely on top of StoP's `sig_hat`
- `H_joint` (joint entropy), `config_persistent` (dominant-config match across periods),
  `susceptibility` (Jensen–Shannon divergence between baseline/intervention (app, hour)
  distributions) — all period-boundary-based, all DS6-specific (no DS5 equivalent measure
  uses this apparatus)

### Assessment

**Theory-faithful by way of deliberate omission, not approximation** — the paper's own
explicit caution against literal thermodynamic quantities is honored more completely here
than in DS5, where `β_behav = 2/σ̂²` was built with an explicit "FLAG A" caveat rather than
declined outright. DS6's approach (2-for-2 with Structured now) suggests the paper's
Boltzmann-bridge apparatus should be explicitly scoped to bounded rate variables in future
revisions, not applied by default to every OneSec-family dataset.

**Two bugs found and fixed before results were trusted** (granularity mismatch in the
sanity gate, then a `NaN >= threshold` pandas assertion bug found immediately after fixing
the first — full detail in the bug chronicle, item d). Both were caught before the headline
finding was computed, not after.

**Headline finding is DS6's first condition-differentiated (not merely period-differentiated)
result across all of Step 1:** control shows significantly lower susceptibility than either
friction condition (control=0.028 vs default=0.070, p=0.0011; vs intervention=0.052,
p=0.0075; default vs intervention not significantly different, p=0.22). This directly
matches the paper's own StM framing ("a friction-sensitive user may show a large shift...
after a relatively small intervention") and is part of a 2-dataset convergent finding with
DS5's own StoP result (friction conditions show higher σ̂ than control) — see
`cross_dataset_cas_model_synthesis.md` §2 (StM) for the cross-dataset framing; not re-derived
here.

---

## SyD — System Dynamics

### Theory intended

Paper §2.8, quoted directly: stocks "may include habit strength, accumulated successful
dismissals, accumulated overrides, app-use pressure, intervention exposure, and
disengagement"; "successful dismissals decrease the stock or increase a competing stock of
self-regulation." DS6 cannot use the dismissal/override-based stocks — uses the paper's other
two named stocks, "app-use pressure" and "self-regulation," operationalized directly via
`addiction_index` and `self_control_index`.

### What was implemented

- Two stocks, both paper-named, not invented: `addiction_index` (pressure), `self_control_index` (self-regulation)
- Two feedback-loop hypotheses (pressure reinforcement; self-regulation correction), both stated before running
- Regression-to-the-mean control (raw + partial correlation, controlling for baseline level) — a DS6-specific adaptation of Structured's own person-demeaning lesson, appropriate here because DS6 has only 2 survey waves (a 2-point series demeaned is just the change score already used as the outcome, so demeaning in Structured's literal sense does not apply)

### Assessment

**This is the model family DS6 exists for in the project's own sequencing** —
`stage4_implementation_plan.md` deferred SyD from DS5 to DS6 explicitly because SyD needs
repeated survey waves. DS6's implementation closes that structural gap directly, using
paper-named stocks rather than inventing new ones.

**Non-redundancy checked first, matching Structured's own SyD precedent:** confirmed no
other DS6 Step 1 notebook had treated a psychosocial score as a formal stock, or tested
behavioral flow against psychosocial **change** (only static wave-1 levels had been
correlated before).

**Both feedback loops are genuine null results, before and after the regression-to-the-mean
control:** Loop 1 partial r=0.057 (p=0.45, `mean_N_baseline`) / r=−0.111 (p=0.14,
`mu_hat_baseline`); Loop 2 partial r=0.093 (p=0.22). Condition-level ANOVA on
`addiction_index_change` also non-significant (F=1.225, p=0.296). Reported honestly, matching
the mostly-null psychosocial pattern already present across every other DS6 Step 1 family.

---

## Overall assessment: which DS6 families were theory-faithful, and how

| Family | Theory faithfulness | Primary divergence from DS5 (structural, not a simplification unless noted) | Should be defended in paper? |
|---|---|---|---|
| StoP | **HIGH** | Count-based state variable, not bounded rate; within-participant period axis, not between-condition | Yes — cite paper §1.3's own named fallback directly |
| NeT | **HIGH** | Structurally smaller (10-app) vocabulary; self-derived edges after finding `app_next` unreliable | Yes — note small state space as a partly-confirmed, partly-disconfirmed pre-registered expectation |
| InT | **HIGH** | `H_out` structurally absent (not approximated); quantile not fixed-range binning for `H_emp`; one new MI test beyond DS5's scope | Yes — flag `H_emp` cross-dataset incomparability explicitly |
| DyS | **MODERATE–HIGH** | Genuinely new 3-way asymmetric regime space (not in DS5's theoretical vocabulary at all); per-period not pooled σ threshold | Yes — this is new theoretical content, not just a caveat |
| StM | **HIGH (by omission)** | No β/T/Z/F apparatus at all; independent of StoP; susceptibility via JS divergence, not the mean-field χ formula | Yes — the paper's Boltzmann-bridge section needs explicit scoping to bounded variables |
| SyD | **HIGH** | New family relative to DS5 (never built there); partial-correlation, not person-demeaning, RTM control | Yes — genuine null, explicitly not causal |
| GaT | N/A — deferred | DS6 has no outcome-variance proxy candidate at all (harder than DS5's situation) | See `ds6_deferred_models_rationale.md` |
| ABM | N/A — deferred | No structural blocker identified; scheduling gap only | See `ds6_deferred_models_rationale.md` |

---

## What should be explicitly added to the paper, based on DS6's build history

1. **The count-based daily-attempt fallback (paper §1.3) needs equal billing with the
   rate-based state variable**, not a footnote status — two of this project's four
   empirically-modeled OneSec-family datasets (DS6, and Structured for its own unrelated
   reasons) needed it, not just an edge case.
2. **DyS's asymmetric 3-way regime space (declining/growing/resting) is new theoretical
   content**, derivable directly from a floor-only-bounded state variable, and is not
   currently described anywhere in the paper's DyS section, which is written entirely in
   DS5's double-bounded-boundary-fixed-point language.
3. **The paper's Boltzmann-bridge apparatus (β, T, Z, F) should be explicitly scoped** to
   state variables that plausibly approximate a bounded two-state occupation probability.
   DS6 and Structured have now both independently declined to build it for structurally
   similar reasons — this is a pattern, not two isolated implementation choices.
4. **A general methodological note on look-ahead artifacts in alternating open/close event
   logs** is worth adding for future datasets of this kind: DS6's `app_next` field looked
   plausible on its face and was explicitly recommended as a substitution-tendency feature in
   an earlier version of this project's own documentation before being found unreliable (see
   `ds6_bug_discoveries_and_fixes_chronicle.md`, item b) — a generic caution, not DS6-specific.

---

*Written 2026-08-08 as part of the DS6 post-analysis reporting set.*
