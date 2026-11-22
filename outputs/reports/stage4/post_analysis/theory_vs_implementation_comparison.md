# Theory vs. Implementation Comparison — DS5 Model Families

**Written:** 2026-04-20  
**Purpose:** Compare the theoretical model-to-behavior translation intended in the paper against what was actually implemented in code; assess faithfulness, approximations, and places where implementation diverged

---

## Background

The conceptual paper frames DS5 through five CAS model families (StoP, InT, DyS, StM, NeT). Each family translates a formal mathematical model into behavioral terms using the proxy variable X_t = n_opened/n_events (daily override rate). This document compares what the theory demanded versus what the code did.

The state variable X_t is an important proxy caveat throughout: it is a count ratio from behavioral logs, not a directly observed psychological state. All model quantities inherit this limitation. This document notes where this matters most.

---

## StoP — Stochastic Processes

### Theory intended

The paper frames individual behavior as an Ornstein-Uhlenbeck (OU) process or simpler constant-drift SDE:

```
dX_t = μ dt + σ dW_t  (constant-drift version)
dX_t = θ(μ − X_t) dt + σ dW_t  (OU with mean-reversion)
```

Parameters: drift μ (systematic behavioral tendency), diffusion σ (noise/impulsivity), and for OU: mean-reversion θ (attractor strength). The paper anticipates that condition effects manifest as changes in μ (friction shifts the behavioral equilibrium).

### What was implemented

- **Used:** Constant-drift SDE (FLAG 1 — OU deferred)
- **Estimation:** Method of moments: μ̂ = mean(ΔX_t); σ̂ = std(ΔX_t) (FLAG 2 — MLE deferred)
- **Friction effect:** h_c = μ̂_control − μ̂_condition (single-parameter drift reduction)
- **Population:** N=414 (MIN_DAYS=7)

### Assessment

**Stayed close to theory:** The state variable, the SDE formulation, and the estimation logic are all theoretically coherent. The daily increment ΔX_t as the fundamental observable is a natural and defensible translation.

**Simplified:** The OU mean-reversion term was dropped. This is an important simplification because mean-reversion is the theoretically most meaningful part of the OU process (it captures the strength of the behavioral attractor). For DS5 with short 6-week windows, this simplification is defensible — θ cannot be reliably estimated from 7–45 daily observations. But it means the "attractor strength" concept central to the paper is not empirically captured in the current implementation.

**Proxy limitation matters most here:** X_t = n_opened/n_events is a ratio that can be driven by sparse events (few friction events in a day gives noisy X_t). Days with 1–2 events produce extreme X_t values (0 or 1) that inflate σ̂ estimates. The MIN_DAYS=7 threshold and event-minimum filtering help, but this remains a concern.

**Main approximation to defend in the paper:** Why μ̂ ≈ 0 for all participants: the study window is too short for drift to accumulate. This is an empirical finding (not a theoretical prediction), but it means the drift component of the SDE is unidentifiable at this timescale. The StoP model is essentially characterized by σ̂ alone in DS5 — which collapses the theoretically rich 2D (μ, σ) space to 1D.

---

## InT — Information Theory

### Theory intended

Behavioral uncertainty characterized via Shannon entropy across multiple dimensions — the "behavioral portfolio" interpretation. The paper anticipates H(X_t) as a measure of behavioral randomness, with H_out capturing friction-response diversity.

The paper specifically frames H_out as: "how unpredictably does this participant navigate friction outcomes?" — i.e., an individual-difference measure of friction response style.

### What was implemented

- **H_emp:** Empirical entropy of daily X_t distribution using K=10 bins → captures behavioral unpredictability; works as intended
- **H_out:** Shannon entropy over {opened, dismissed, closed} per participant → computed correctly but is condition-confounded (control participants cannot produce the same outcome mix as friction-exposed ones)
- **H_app, H_hour:** App and temporal entropy → straightforward; correctly computed
- **H_SDE:** Theoretical Gaussian entropy = ½ log₂(2πe σ̂²) → derived bridge from StoP; not directly observable

### Assessment

**Stayed close to theory:** H_emp correctly operationalizes behavioral entropy. H_app and H_hour are clean information-theoretic measures.

**Implementation challenge (H_out condition confound):** The theoretical frame treats H_out as an individual-difference measure, but the implementation correctly identified a structural problem: control participants cannot produce `dismissed` and `closed` outcomes in the same distribution as intervention-exposed participants. The solution (condition residualization, H_out_resid) is methodologically sound but adds a layer of assumption (OLS residualization assumes a linear additive condition effect). The paper's framing implies H_out is a trait; the data shows it is partly condition-induced. This should be stated explicitly in the paper.

**Bridge equation (H_SDE) is not in the paper:** The Gaussian differential entropy bridge connects the parametric SDE model to the non-parametric entropy measure. This is a non-trivial theoretical result (it requires the assumption that daily ΔX_t increments are Gaussian) and should be added to the paper's theoretical section.

**Analog is theory-faithful:** The mutual information bridge I_consec = H_app − H_trans (connecting InT and NeT) is theoretically interesting and empirically verified (r=0.945). This should also be explicitly stated in the paper.

---

## DyS — Dynamical Systems

### Theory intended

In the limit σ→0, the stochastic process reduces to a deterministic dynamical system. Fixed points (stable attractors) correspond to persistent behavioral equilibria. The paper anticipates identifying whether a participant is in a "high-override" or "low-override" attractor, and how far from the boundary they are.

Mathematically: the fixed-point equation X* = f(X*) gives the stable behavioral equilibria; the position of X* relative to a behavioral threshold (e.g., 0.5) determines the behavioral regime.

### What was implemented

- **DyS regime partition:** Is_dys_eligible = (σ̂ < σ_median) — binary threshold on StoP output
- **Fixed-point prediction:** predicted_boundary_fp = "upper" (μ̂>0) or "lower" (μ̂<0) based on StoP drift sign
- **Deviation:** |x_mean − predicted boundary| as a proxy for attractor distance

### Assessment

**Simplified substantially:** The implementation replaces the formal fixed-point analysis with a binary classification (low-σ vs. high-σ). The actual fixed-point equation (X* = lim_{t→∞} E[X_t]) would require estimating the OU process's stationary mean — which requires θ (not estimated). The "predicted boundary" from the sign of μ̂ is highly approximate: near-zero μ̂ makes the sign uninformative.

**Still theoretically meaningful:** Despite the simplification, the core concept (low-σ participants are more "deterministic" and thus more amenable to the DyS framework) is preserved. The regime partition is a legitimate implementation of the σ→0 limit.

**Cautious terminology enforced:** The code carefully avoids calling anything an "attractor" or "equilibrium." Instead: predicted_boundary_fp, deviation_from_predicted_fixed_point, empirical resting state. This is correct.

**Main approximation to defend:** The σ-median threshold for DyS-eligibility is arbitrary. Why median? Because it splits the sample evenly, which is conventional but not theoretically motivated. The true DyS regime requires σ to be genuinely near zero relative to the dynamical timescale — which is unknown in DS5.

**Should be revised or clarified:** The predicted_boundary_fp (upper vs. lower) based on μ̂ sign is problematic given that 56.5% of μ̂ values are |μ̂| < 0.01. These should arguably be classified as "boundary-ambiguous" rather than assigned to upper/lower.

---

## StM — Statistical Mechanics

### Theory intended

The Boltzmann-bridge between the SDE and thermodynamics: the stationary distribution of the OU process follows P_inf(X) ∝ exp(−2V(X)/σ²), where V(X) is the potential function. The behavioral inverse temperature β = 2/σ² controls the "sharpness" of the distribution around its minimum. The susceptibility χ_behav = β·p·(1−p) identifies participants near a phase transition.

### What was implemented

- **β_behav = 2/σ̂²** — approximation of the Boltzmann inverse temperature (FLAG A throughout)
- **V(x) via KDE** — empirical potential from kernel density estimation of condition-level X_t distributions
- **χ_behav = β·p·(1−p)** — behavioral susceptibility (where p ≈ x_mean)
- **F_behav = x_mean − (1/β)·H_emp** — free energy analog

### Assessment

**The critical approximation is documented (FLAG A):** β_behav = 2/σ̂² is correct for the constant-drift SDE (Fokker-Planck stationary distribution is exponential in X when V(X) = constant). BUT: the Boltzmann bridge in the paper assumes a potential-well SDE with a non-trivial V(X), not a constant-drift SDE. In the constant-drift case, the Fokker-Planck stationary distribution (reflecting boundaries) is not a Boltzmann distribution in the usual sense. FLAG A was documented explicitly throughout the code, and the implementation calls these "behavioral analogs" not "rigorous thermodynamics."

**V(x) from KDE is exploratory:** The potential-well reconstruction (V(x) = −log P(X=x)) from empirical KDE is shown at the condition level. It is informative (the default condition V(x) is flatter → higher behavioral temperature), but the reconstruction is noisy and requires large N for reliable estimation. It is presented as illustrative, not quantitative.

**chi_behav is theory-faithful:** The susceptibility formula χ = β·p·(1−p) is exactly the mean-field susceptibility for a two-state system near its critical point. It is correctly derived and correctly computed. The counterintuitive result (C1 has highest chi_behav despite being low-noise) emerges correctly from the formula: low σ → high β; x_mean ≈ 0.35 → p(1−p) near maximum → high χ. This is a genuine theoretical prediction confirmed by data, not an artifact.

**Main issue to defend:** The entire StM framework (β, F, χ) rests on the approximation β = 2/σ̂². This is exact for the constant-drift GBM/OU case in an unbounded domain but approximate for X_t ∈ [0,1] with reflecting boundaries. The paper must acknowledge this explicitly.

---

## NeT — Network Theory

### Theory intended

Each participant's app-switching behavior defines a directed weighted network over apps. The paper anticipates characterizing the network's concentration (how hub-dominated), self-loop rate (habitual repetition), and transition entropy (diversity of app switching).

### What was implemented

- **Temporal succession networks:** App sequences derived from consecutive events within the observation period. W_ij = count(app_i followed by app_j); T_ij = W_ij / sum_j(W_ij)
- **HHI_net** = Herfindahl index of outdegree weights = Σ_i (s_i^out / S_total)²
- **rho_self** = diagonal weight fraction (self-loops)
- **H_trans** = source-weighted conditional entropy of T_ij
- **π** = stationary distribution (ergodic Markov chain; requires M≥50 transitions)

### Assessment

**Stayed close to theory:** The network construction is theoretically coherent. The HHI_net, rho_self, and H_trans are well-defined network statistics.

**Implementation approximations to note:**
1. No time-gap filter (FLAG G1): consecutive events that are hours apart are treated as genuine app transitions. This may inflate self-loop rates for overnight sequences. However, because DS5 events are friction events (app openings), temporal gaps may be less problematic than for general phone-use logs.
2. First-order Markov assumption (FLAG M1): The transition matrix T_ij assumes the next app depends only on the current app, not on prior history. This is a standard simplification that may not hold for habitual sequences.
3. No session boundaries: DS5 does not have session markers. The temporal succession network spans the entire observation period without any within-session segmentation.
4. Self-loops included (FLAG S1): Consecutive openings of the same app are included as self-loop transitions (rho_self). This inflates rho_self substantially for users who open and reopen the same app repeatedly.

**Main concern:** The near-ceiling HHI_net (0.84–0.86) and rho_self (0.922–0.924) values suggest that the DS5 network features may have limited discriminatory power due to ceiling effects. Most participants primarily use one app (likely Instagram, TikTok, etc.) with OneSec installed. The NeT features may be capturing "which app has OneSec installed on it" rather than true network topology.

**Most defensible finding:** I_consec = H_app − H_trans (verified at r=0.945). This mathematical identity between app entropy, transition entropy, and mutual information is theoretically clean and empirically confirmed.

---

## Phenotyping — Clustering Methods

### Theory intended

The paper anticipates discovering behavioral subgroups along theoretically meaningful dimensions (§4.3): friction sensitivity, habitual stability, impulsivity, threshold dependence, context dependence, etc.

### What was implemented

- k-means with k-means++ initialization; silhouette + CH + DB for k selection; bootstrap Jaccard ≥ 0.75 for stability
- Feature selection based on independence analysis (not all 20+ features used; only genuinely independent axes)
- Six systematic paths covering NeT-only, behavioral-only, hierarchical, condition-stratified, intervention-sensitive, and dynamic/stochastic dimensions

### Assessment

**Theory-faithful in intent:** The six-path design explicitly tests whether the paper's anticipated dimensions (network, behavioral dynamics, friction response) are independently discoverable.

**Methodologically sound:** The independence analysis (identifying redundant features before clustering) prevented the "apparent richness" fallacy — reporting 20 features as if they represent 20 independent phenotype dimensions when they reduce to ~3.

**Where implementation became approximate:**
- Profile A (N=125) Stage 2 was reported as A_all because Jaccard=0.744 (just below 0.75). This is a sensible decision, but the 0.75 threshold is conventional, not theoretically derived. A different threshold would yield a different answer.
- The k-selection criteria (silhouette, CH, DB combined) are informative but not definitive — they guide judgment, not determine a unique answer.

**Where results stayed surprising and honest:**
- The orthogonality of NeT and behavioral dimensions (ARI=0.020) was not anticipated to be this strong.
- The default condition's collapse of behavioral heterogeneity was not anticipated.
- The chi_behav ordering (C1 highest) was counterintuitive but correctly derived from the StM formula.

---

## Overall assessment: which models were theory-faithful vs heuristic

| Model | Theory faithfulness | Primary approximation | Should be defended in paper? |
|---|---|---|---|
| StoP (constant-drift) | **MODERATE** | OU mean-reversion dropped; MoM not MLE | Yes — explain why OU deferred and why MoM is sufficient at DS5 window lengths |
| InT | **HIGH** | H_out condition confound handled via residualization | Yes — note the confound and justify H_out_resid |
| DyS | **LOW-MODERATE** | Binary partition based on σ median; predicted_fp from near-zero μ̂ sign | Yes — acknowledge regime threshold is conventional, not theoretically derived |
| StM | **MODERATE** | β = 2/σ̂² approximation (FLAG A); constant-drift ≠ potential-well SDE | **Requires explicit paper section** — the FLAG A caveat must be prominently stated |
| NeT | **HIGH** | No session boundary filter; first-order Markov; self-loops included | Yes — note as known structural limitations (W1–W6 documented in notebook) |
| Phenotyping | **HIGH** | Conventional k-selection thresholds; Profile A Jaccard threshold | Yes — standard methods; justify choices briefly |

---

## What should be explicitly added to the paper before submission

Based on this comparison, the following theoretical elements are referenced in the code but NOT yet in the conceptual paper:

1. **H_SDE = ½ log₂(2πe σ²)** — the Gaussian differential entropy bridge (InT ↔ StoP)
2. **FLAG A caveat** — the constant-drift β = 2/σ̂² approximation and its limits
3. **σ→0 limit equation** — the formal DyS reduction from SDE to ODE
4. **Boundary fixed-point equation** — marginal stability (λ=1) note for DyS
5. **I_consec = H_app − H_trans** — the InT-NeT mutual information bridge
6. **NeT formulas:** W_ij, s_i^out, T_ij, H_trans, π, HHI_net (the formal network definitions)

These are gaps between what was implemented and what is currently documented in the theory.

---

*Written 2026-04-20 as part of the DS5 Step 2 synthesis waypoint.*
