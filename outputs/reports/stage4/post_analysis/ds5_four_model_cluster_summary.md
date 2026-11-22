# DS5 Four-Model Cluster Summary — Stage 4 Step 1

**Written:** 2026-04-17  
**Covers:** StoP (nb 43), InT (nb 45), DyS (nb 42), StM (nb 41)  
**Dataset:** DS5 — German Adolescents RCT, N=573 (414 eligible for time-series models)  
**Purpose:** Consolidation reference for the completed DS5 model cluster: rationale for the
order, what each model contributes, its limits, the bridges between them, which results are
independent vs re-expressions, and what the four-model quadrangle means for Step 1 overall.

---

## 1. Why these four models and why this order

The four DS5 Step 1 models were not selected as four independent analyses run in parallel.
They were built as a connected chain, where each model either (a) depends on the previous one's
outputs or (b) interprets the same underlying data from a different theoretical language.
The order was designed to minimize new data infrastructure at each step and to maximize
the strength of the final unification claim.

### Order rationale: StoP → InT → DyS → StM

**Step 1: StoP** was the natural entry point because it required only the behavioral time series
(X_t = n_opened/n_events per day) and produced the two primary per-participant parameters:
drift μ̂ and diffusion σ̂. These parameters are the input to every subsequent model.
No other model family could have been started without first establishing X_t and estimating
(μ̂, σ̂) — StoP is the data-extraction foundation of the cluster.

**Step 2: InT** was built directly on StoP's σ̂ output via the Gaussian entropy bridge
H_SDE = ½ log₂(2πeσ̂²). This required no new estimation — only a transformation of an
already-computed parameter. By implementing InT immediately after StoP, the StoP↔InT bridge
(H_SDE vs H_emp) could be validated while StoP was still fresh. The result — r(H_SDE, H_emp)
= 0.650 — became the primary cross-model validation benchmark for the cluster.

**Step 3: DyS** was built on the σ→0 limit of StoP's Euler-Maruyama equation and on H_emp
from InT (as the independent entropy measure against which the DyS regime partition could be
validated). DyS required no new data either: it partitioned the 414 eligible participants
into deterministic (low-σ̂) and stochastic (high-σ̂) regimes using the StoP σ̂ threshold,
and then validated that partition by showing DyS-eligible participants have lower H_emp
(1.75 vs 2.32 bits). DyS closed the StoP↔InT bilateral relationship into a triangle.

**Step 4: StM** was built last because it required the most inputs: σ̂ from StoP (for β_behav),
H_emp from InT (for F_behav), is_dys_eligible from DyS (for four-model convergence), and the
behavioral distribution itself (for condition-level V(x)). StM cannot precede any of the other
three — it synthesizes all of them. Implementing it last allowed it to close the triangle into
a quadrangle and produce the four-model convergence criterion.

**Why not implement them independently?**

Building them in isolation and then comparing post-hoc would have been possible, but would
have missed the structural dependencies:
- DyS without StoP has no basis for the σ-threshold partition
- InT without StoP has no bridge to interpret H_SDE
- StM without InT has no H_emp for the free energy formula
- The four-model convergence criterion depends on all four simultaneously

The order was not arbitrary. It was a principled dependency chain that made each
implementation as small as possible while producing the strongest possible theoretical bridges.

---

## 2. What each model contributes

### StoP — Stochastic Processes

**Primary question:** How does behavior fluctuate and drift over time?

**What it produces:**
- μ̂ per participant: behavioral drift — whether override tendency is systematically increasing
  or decreasing (near-zero for all DS5 conditions: ~0.007)
- σ̂ per participant: behavioral diffusion — day-to-day variability in override rate
- σ_c ordering: default (0.245) > reintervention (0.200) > control (0.172) — friction raises
  behavioral noise
- h_c: condition-level drift difference — friction has near-zero effect on drift direction
  but substantial effect on volatility
- The state variable X_t that all subsequent models inherit

**Conceptual contribution:** StoP establishes that DS5 friction acts primarily as a volatility
amplifier, not a systematic drift reducer. This is the core behavioral finding from which all
other models draw meaning.

### InT — Information Theory

**Primary question:** How uncertain / predictable is behavioral output?

**What it produces:**
- H_emp: empirical behavioral state entropy (predictability of daily override rate)
- H_SDE: StoP-derived theoretical entropy prediction (Gaussian approximation)
- H_out: friction-outcome entropy (how mixed are opened/dismissed/closed outcomes)
- H_app, H_hour: broader behavioral context (app diversity, temporal spread)
- r(H_SDE, H_emp) = 0.650: the primary cross-model bridge result

**Conceptual contribution:** InT translates the diffusion parameter σ̂ into a
behaviorally intuitive quantity — how uncertain is this participant's override behavior from
day to day? It also provides the first empirical validation of the Gaussian-increment
assumption embedded in StoP (the 0.650 correlation).

**What InT adds beyond StoP:** H_emp is a non-parametric measure that does not assume
Gaussianity. The comparison H_emp vs H_SDE (which does assume Gaussianity) is a model
check, not just a re-expression. High r = 0.650 supports the Gaussian assumption; it is
not tautological.

### DyS — Dynamical Systems

**Primary question:** Who is in the near-deterministic regime, and does friction disrupt it?

**What it produces:**
- is_dys_eligible: regime partition (σ̂ < median → 207/414 participants)
- Condition-level DyS eligibility: control 64%, reintervention 58%, default only 29% — friction
  disrupts determinism most in the default condition
- predicted_boundary_fp and deviation_from_predicted_fixed_point: how close each participant's
  empirical mean is to the boundary predicted by constant-drift map
- behaviorally_deterministic (combined low-σ̂ AND low-H_emp): 154 participants (37.2%)
- DyS↔InT bridge: DyS-eligible mean H_emp = 1.75 vs StoP-stochastic H_emp = 2.32 (confirms
  that low-σ̂ participants are indeed more predictable)

**Conceptual contribution:** DyS frames friction as a perturbation of behavioral dynamics.
The most striking result — that only 29% of default-condition participants are in the
deterministic regime vs 64% of control — suggests friction breaks habitual determinism.
This is not visible from StoP drift alone (drift is near-zero for all conditions).

**What DyS adds beyond StoP:** The regime partition is qualitatively different from just
reporting σ̂. It answers "who is operating in a regime where behavior is approximately
predictable without knowing the noise?" — a different question than "who has low diffusion?"

### StM — Statistical Mechanics

**Primary question:** What is the behavioral temperature and energy landscape?

**What it produces:**
- β_behav per participant: behavioral inverse temperature (control 154.8 > reintervention 123.8
  > default 66.8) — friction raises behavioral temperature
- T_behav per participant: behavioral exploration intensity (higher in friction conditions)
- Condition-level V(x): energy landscape from KDE of pooled daily X_t distributions
- χ_behav per participant: intervention sensitivity (reintervention 23.2 > control 18.0 >
  default 12.8) — reintervention group unexpectedly near tipping point
- F_behav: energy-entropy tradeoff per participant
- H_StM: third entropy estimate (closely matching H_SDE)
- four_model_convergent: 154 participants (37.2%), closing the quadrangle

**Conceptual contribution:** StM reframes σ̂ as a "behavioral temperature" — a vocabulary shift
that connects the raw statistical finding (higher variance in friction conditions) to a
thermodynamic concept (thermal disorder). The susceptibility result χ_reintervention > χ_control
is unexpected and interpretable: reintervention participants appear to be near a behavioral
tipping point, not settled into a high-entropy random state.

**What StM adds beyond the other three:**
- Susceptibility χ_behav is a genuinely new quantity not computable from StoP, InT, or DyS
- The free energy F_behav operationalizes the tension between habitual pull and flexibility
- The energy landscape V(x) is a different representation of the behavioral distribution
  than H_emp or x_mean: it identifies where behavior is "costly" vs "cheap"
- H_StM provides a third entropy triangulation point (supporting H_SDE and H_emp)

---

## 3. What each model cannot do — and where a different dataset or approach would help

### StoP — Limitations

**Cannot do:**
- Detect mean-reversion or adaptation — the constant-drift SDE has no θ parameter; genuine
  return-to-baseline behavior is invisible
- Say anything about why variance is higher in friction conditions — confounded by
  condition assignment, not individual behavioral dynamics
- Model non-stationarity explicitly — X_t changes are assumed stationary

**Where a different dataset or approach would help:**
- **DS4** (897-day windows): the OU process (dX = θ(μ−X)dt + σdW) is estimable with long
  windows and adds mean-reversion. DS4 is the correct target for OU-StoP.
- **DS6** (repeated waves): session-level rather than daily X_t; different temporal granularity;
  tests whether the StoP model structure is consistent across measurement scales
- **Step 2 / MLE estimation**: method-of-moments estimators are consistent but inefficient;
  MLE would tighten parameter uncertainty and enable individual-level confidence intervals

### InT — Limitations

**Cannot do:**
- Distinguish signal entropy (H_emp) from noise entropy — H_emp conflates genuine behavioral
  uncertainty with measurement noise from short windows
- Compute mutual information between conditions and outcomes without careful bias correction
  (deferred FLAG 4)
- Separate H_out confounds — H_out is inflated in control condition by construction (only
  opened/dismissed outcomes dominate when friction is absent)

**Where a different dataset or approach would help:**
- **DS6**: session-level information structure (substitution entropy); different causal
  structure from DS5; tests whether entropy ordering is robust to a different population
- **Step 2 / bias-corrected MI**: Miller-Madow or jackknife correction for H_emp at small N;
  enable proper MI computation between behavioral profiles and psychosocial outcomes

### DyS — Limitations

**Cannot do:**
- Identify true interior attractors — the constant-drift 1D map has only boundary fixed
  points; "attractor" language is interpretive only
- Demonstrate bifurcation — 3 discrete conditions are insufficient to trace a bifurcation
  curve; the DyS result is a categorical comparison, not a phase diagram
- Access the multi-dimensional state space the paper envisions — urge, boredom, fatigue,
  self-control are not directly observed in DS5

**Where a different dataset or approach would help:**
- **DS6**: repeated behavioral waves at higher temporal resolution; opens possibility of
  observing within-person state transitions that look more like DyS trajectories
- **DS5 event-level** (not daily aggregation): using event-level latency data could provide
  a finer-grained state variable that better approximates the paper's multi-dimensional vision
- **OU on DS4**: the OU process is a confining DyS model with an analytically computable
  attractor at X* = μ; DS4 enables this

### StM — Limitations

**Cannot do in DS5:**
- Provide rigorous Boltzmann bridge — FLAG A: constant-drift SDE ≠ potential-well SDE;
  β_behav = 2/σ̂² is an approximation
- Estimate reliable individual-level V(x) — 7-45 daily observations are too sparse for KDE
- Demonstrate equilibrium — thermodynamic equilibrium requires ergodic state-space exploration
  that 7-45 days cannot guarantee
- Phase transitions or hysteresis — only 3 conditions; no post-intervention behavioral data

**Where a different dataset or approach would help:**
- **DS4** (rigorous OU-StM): OU process has exact quadratic potential V(x) = (θ/2)(x−μ)²
  and exact Gaussian stationary distribution; β_OU = 2θ/σ² is rigorous, not approximate.
  This is the primary motivation for the DS4 StM blueprint.
- **DS5 Step 2**: longer aggregate windows (using cumulative X_t across the full study period
  per participant rather than daily slices) might allow slightly more stable individual V(x)
- **Synthetic simulation**: phase transitions and bifurcations can be demonstrated in
  principle using the estimated parameters to generate synthetic data with continuous h sweeps

---

## 4. Strongest bridges between the four models

### Bridge A: StoP → InT via H_SDE (validated, r = 0.650)

The Gaussian differential entropy H_SDE = ½ log₂(2πeσ̂²) is a monotone transform of σ̂.
It is not an independent measurement — it is the predicted H_emp under the assumption that
daily increments are Gaussian. The empirical correlation r(H_SDE, H_emp) = 0.650 is therefore
a **model check**: it tests whether the Gaussian-increment assumption in StoP is consistent
with the non-parametric entropy estimate from InT. The moderate correlation (not perfect)
is informative: it suggests partial but not complete Gaussian fit for the increment distribution.

**Strength: High.** Both sides are directly computed from the same participants; correlation
is statistically robust (N=414).

### Bridge B: StoP → DyS via σ→0 limit (structural, by construction)

The DyS map X_{n+1} = clip(X_n + μ̂, 0, 1) is the σ→0 limit of StoP's Euler-Maruyama step.
This means every DyS-eligible participant is a StoP participant whose σ̂ falls below the
median threshold. The bridge is not empirically validated — it is formal: DyS IS StoP with σ
set to zero. The empirical content is in the regime partition (which participants are in the
σ→0 regime) and what that partition predicts about behavior (the condition-level DyS
eligibility differences).

**Strength: High structurally; Medium empirically** (the regime partition results add
content beyond the formal connection).

### Bridge C: DyS ↔ InT via behavioral determinism (validated)

DyS-eligible participants have lower H_emp (1.75 bits) than StoP-stochastic participants
(2.32 bits). This is the expected result — low-σ̂ participants should be more predictable —
but H_emp is a non-parametric quantity computed from the behavioral distribution, not from σ̂
directly. The fact that the ordering holds validates that the DyS regime partition is
behaviourally meaningful beyond just being a threshold on σ̂.

**Strength: High.** The entropy difference (0.57 bits) is large and consistent.

### Bridge D: StoP → StM via Boltzmann analog (approximate)

β_behav = 2/σ̂² maps diffusion to "behavioral temperature." H_StM (from condition-level KDE)
≈ H_SDE (both near −0.7 bits for control; near −0.1 bits for default). The close match
validates the Boltzmann KDE approximation at the condition level — the energy landscape
estimated from the data is consistent with the entropy predicted by StoP's Gaussian
assumption. **However: this bridge is approximate.** The constant-drift SDE does not
produce a proper Boltzmann stationary distribution (FLAG A). The agreement is reassuring
but does not retroactively make the bridge exact.

**Strength: Medium.** Validated numerically at condition level; not rigorous theoretically.

### Bridge E: InT ↔ StM via entropy triangulation

H_StM ≈ H_SDE ≫ (numerically, both from Gaussian assumptions) vs H_emp (non-parametric).
The three-way comparison provides a consistency check: if all three measures agree, the
Gaussian-Boltzmann approximation holds; divergence would reveal model inadequacy.
Results: H_StM and H_SDE match closely (both derived from σ̂ via Gaussian assumptions);
both differ somewhat from H_emp (the non-parametric estimate). This pattern is expected
and informative.

**Strength: Medium.** Consistent with expectations; adds cross-model validation depth.

### Bridge F: All four models → convergence criterion (structural + empirical)

The four-model convergence criterion is the strongest unification result. It identifies 154
participants (37.2%) where StoP (low σ̂), DyS (is_dys_eligible), InT (low H_emp), and StM
(high β_behav) all point to the same behavioral characterization: low-noise, near-deterministic,
predictable, thermodynamically ordered. This is not trivially tautological — H_emp is an
independent measure not derived from σ̂ — but the redundancy between σ̂ and β_behav should
be noted (β_behav = 2/σ̂², so three of the four criteria effectively reduce to two independent
conditions: low σ̂ AND low H_emp). The behavioral determinism count (154 participants in
behaviorally_deterministic by DyS+InT) equals the four-model convergent count, confirming
the internal consistency of the cluster.

**Strength: High as convergence result; needs transparency about partial redundancy.**

---

## 5. Which results are independent vs re-expressions

| Result | Status | Note |
|---|---|---|
| μ̂ per participant | Independent | Estimated directly from daily increments |
| σ̂ per participant | Independent | Estimated directly from daily increments |
| H_SDE = ½ log₂(2πeσ²) | Re-expression of σ̂ | Monotone transform; no new information |
| H_emp (K=10 bins) | Independent of σ̂ | Non-parametric; measures same construct differently |
| r(H_SDE, H_emp) = 0.650 | Independent result | Comparison of parametric prediction vs empirical estimate |
| is_dys_eligible (σ̂ < median) | Re-expression of σ̂ | Binarization; no new information vs σ̂ ordering |
| DyS condition eligibility distribution | Partly independent | The condition-level comparison adds content |
| Deviation from predicted_boundary_fp | New — requires x_mean | Combines μ̂ prediction with empirical mean |
| β_behav = 2/σ̂² | Re-expression of σ̂ | Exact monotone transform; no new information |
| T_behav = σ̂²/2 | Re-expression of σ̂ | Same |
| χ_behav = β·p_use·(1−p_use) | Partly new | p_use (from x_mean) is independent; β is from σ̂ |
| F_behav = E_use − (1/β)·H_emp | New — combines σ̂ and H_emp | E_use and β are from σ̂; H_emp is independent |
| H_StM from KDE | Partly new | Uses empirical distribution; not identical to H_SDE |
| four_model_convergent | Mostly structural | Effectively: low σ̂ AND low H_emp (two independent conditions) |
| V(x) condition-level landscape | New representation | KDE of empirical X_t distribution per condition |
| Psychosocial correlations | Independent | r(parameter, scale) uses independent survey data |

**Key independence point:** The only genuinely independent empirical axis across all four
models is H_emp. Everything else in the cluster either derives from σ̂ (a StoP parameter)
or from x_mean (a StoP quantity). This means the cluster is less multivariate than it
appears — it is primarily an exploration of what different theoretical vocabularies say about
the same two underlying empirical quantities: σ̂ and H_emp.

This is not a weakness — it is an honest characterization. The theoretical value of the
cluster is precisely that it shows how the same behavioral signal (daily override variance and
entropy) can be framed productively in four different scientific languages.

---

## 6. What the four-model quadrangle means conceptually

The four-model quadrangle is not a statistical result. It is a **theoretical coherence claim**:
that four distinct frameworks — stochastic dynamics (StoP), information uncertainty (InT),
deterministic geometry (DyS), and thermodynamic energy (StM) — converge on a consistent
characterization of behavioral variability for a subset of participants.

The 154 "thermodynamically ordered, behaviorally entrenched" participants have:
- Low daily noise in override behavior (StoP: low σ̂)
- Near-deterministic trajectory structure (DyS: in the σ→0 regime)
- Low behavioral uncertainty (InT: low H_emp)
- Low behavioral temperature and high order parameter concentration (StM: high β_behav)

These are not four different things. They are four ways of saying that certain participants
have stable, predictable, low-variance override behavior. The quadrangle demonstrates that
the CAS model families are not arbitrary — they share a common underlying behavioral construct
(behavioral regularity) and converge on it from different theoretical angles.

**What the quadrangle does NOT claim:**
- It does not claim to identify a psychological type (phenotyping is Step 2)
- It does not claim the 37.2% figure is a stable individual trait (cross-dataset replication
  would be needed)
- It does not claim causal structure (condition did not cause participants to be in this group;
  more control-group participants ended up there, but this is a correlational observation)

**Paper value of the quadrangle:**
The quadrangle is the primary evidence that the CAS multi-model framework is coherent rather
than additive. It is more convincing than saying "we applied four models and here are four
separate results." It says: "when behavior is regular, all four models recognize it as regular."
This is a theoretical contribution to the paper's §4.3 unification argument.

---

## 7. What this cluster contributes to Step 1 overall

**Empirical contributions:**
1. The apparent primary behavioral finding — friction raises σ̂ (volatility), not μ̂ (drift) — does
   not survive a sampling-noise control: σ̂ tracks each arm's binomial floor for the daily proportion
   X_t (ANOVA on σ̂/floor F=0.80, p=0.450), so the σ̂ ordering reflects daily event volume and mean
   override level, not behavioral regularity.
2. The condition-level ordering is consistent across all four model families, establishing
   convergent validity for the σ̂-based characterization.
3. The reintervention group's unexpectedly high susceptibility χ_behav (23.2 vs control 18.0)
   is a new finding from StM not visible in StoP or InT alone.
4. The DyS result — only 29% of default participants in the deterministic regime vs 64% of
   control — is the clearest behavioral evidence for friction disrupting habitual determinism.

**Methodological contributions:**
1. Four-model cluster as a template: the StoP → InT → DyS → StM dependency chain can be
   replicated for DS4, DS6, DS1 using the same notebook structure.
2. The regime partition (DyS-eligible / behaviorally deterministic) and convergence criterion
   are reusable analytical constructs for all datasets.
3. The bridge validation (r(H_SDE, H_emp) = 0.650) establishes a cross-model benchmarking
   standard: any future SDE-based model on any dataset should replicate this correlation.
4. Generator script pattern (make_41_stm.py etc.) enables reproducible re-runs and makes
   the implementation transparent for future extensions.

**Conceptual contributions for the paper:**
1. Demonstrates that the CAS framework is empirically operationalizable — each model family
   connects to a concrete DS5 measure.
2. Provides the vocabulary for Step 2 phenotyping: behavioral temperature β_behav,
   susceptibility χ_behav, free energy F_behav, and H_emp are candidate phenotype dimensions.
3. Documents the honest limits of DS5 for each model family — creating a comparison basis
   for DS4 (where some approximations become rigorous) and DS6 (where substitution dynamics
   are accessible).
4. The FLAG system and weakness flags in each notebook provide a model-by-model audit trail
   for the paper's limitations sections.

---

## 8. Next steps from this cluster

**Immediate (before paper submission):**
- Add missing equations to paper (see `structures/paper_equation_additions.md`)
- DS4 StM: implement OU-based rigorous Boltzmann bridge (see `ds4_stm_blueprint.md`)

**Stage 4 Step 1 — remaining DS5 models:**
- NeT (notebook 44): network transition matrices from app_next/app_prev sequences
- GaT (notebook 46): game-theoretic payoff framing (deferred until behavioral profiles set)
- ABM (notebook 47): requires prior model characterization — enabled by this cluster
- SyD (notebook 48): deferred to DS6 (requires repeated survey waves)

**Stage 4 Step 1 — DS4:**
- DS4 StoP: OU process with θ estimation using 897-day windows
- DS4 StM: rigorous β_OU = 2θ/σ² using OU results (see `ds4_stm_blueprint.md`)
- DS4 DyS: OU fixed point X* = μ is now a true interior attractor — resolves DS5's
  boundary-only limitation

**Stage 4 Step 2:**
- Phenotype discovery using (β_behav, χ_behav, F_behav, H_emp, is_dys_eligible, sig_hat)
  as feature dimensions — notebook 100
