# DS5 DyS Model — Stage 4 Step 1 Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**  
**Written:** 2026-04-17  
**Notebook:** `notebooks/42_ds5_dynamical_systems.ipynb`  
**Producing dataset:** DS5 (German Adolescents RCT, N=573)  
**Model family:** Dynamical Systems (DyS)  
**Prerequisites:** Notebooks 43 (StoP — complete) and 45 (InT — complete)

---

## 1. Is DS5 the right dataset for the first DyS implementation?

**Yes — with explicit constraints.**

DS5 is the correct first target for DyS Step 1 for the following reasons:

1. **StoP is already complete on DS5.** DyS is connected to StoP via the σ→0 limit. The state variable X_t, all participant-level parameter estimates (μ̂, σ̂, x_mean), and the condition structure are already in place. DyS does not require a new data pipeline — it inherits directly from StoP outputs.

2. **InT is already complete on DS5.** The information-theoretic uncertainty profile (H_emp in particular) is the third leg of the StoP↔DyS↔InT triangle. The DyS-eligible regime (low σ̂) corresponds exactly to the low-H_emp participants in InT. Implementing DyS on DS5 closes this triangle with actual empirical data.

3. **The RCT condition structure is unique to DS5.** DyS describes how friction acts as a perturbation of behavioral dynamics. The three-condition RCT (control / default / reintervention) makes DS5 the only dataset where friction's perturbation effect can be compared against a true reference trajectory. This is the most theoretically meaningful setting for a DyS first pass.

4. **The σ→0 regime partition is most interpretable in DS5.** Because DS5 has an experimental condition, identifying which participants fall in the "near-deterministic" (DyS) vs "noise-dominated" (StoP) regime carries behavioral meaning: are friction conditions more or less likely to produce deterministic-looking trajectories?

**Critical honesty about DS5 limits for DyS:**

The paper itself (§4.4) explicitly notes: *"More operationally demanding may be Dynamical Systems and System Dynamics, because they often rely on internal state variables such as boredom, urge, fatigue, or self-control that are not always directly measured at the relevant temporal scale."*

DS5 gives us exactly one behavioral state variable: X_t = n_opened/n_events (daily). The paper's vision of DyS involves a multi-dimensional state space (urge, boredom, fatigue, self-control) — but none of these latent variables are directly observed at event-level temporal resolution in DS5. This is the central limitation, and it must be flagged everywhere in the notebook.

The DyS Step 1 notebook for DS5 is therefore honest about its scope: **it implements DyS in the σ→0 limit on a 1D behavioral proxy.** It does not demonstrate full attractor geometry, does not estimate bifurcation points, and does not simulate multi-dimensional state space trajectories. These remain deferred to Step 2 or to DS6 (which has richer temporal structure).

---

## 2. FLAG decisions for DS5 DyS Step 1

| Flag | Decision | Alternative (deferred) | Why deferred |
|---|---|---|---|
| FLAG 1 | 1D constant-drift discrete map: X_{n+1} = clip(X_n + μ, 0, 1) — the σ→0 limit of StoP | Nonlinear ODE with potential V(x): dX/dt = −dV/dX | Nonlinear potential requires empirical estimation of P(X) and SDE-to-V inversion; also requires StM connection (FLAG 4 in StoP) |
| FLAG 2 | σ→0 regime defined as σ̂ < median(σ̂) across eligible participants | Formal OU-process convergence rate estimation (θ parameter) | OU adds a third parameter; meaningful convergence rate requires longer windows; DS4 better suited |
| FLAG 3 | Empirical resting state x_mean used as attractor proxy (time-average of X_t) | True fixed-point of analytically-derived nonlinear ODE | True fixed points require V(x); only derivable after StM/potential estimation (FLAG 4 in StoP) |
| FLAG 4 | Bifurcation analysis and multi-dimensional state space deferred | Bifurcation diagram sweeping friction magnitude continuously | DS5 has only 3 discrete conditions — insufficient to trace a bifurcation curve; defer to DS6 or synthetic simulation |

---

## 3. Equations to use — with paper status and role

### Core equations — IN PAPER

| Eq. | Formula | Paper location | Role | Core/optional |
|---|---|---|---|---|
| Eq. 14 | dx/dt = f(x(t), μ) | §4.1.2, p. 8 | Continuous-time ODE — general DyS formulation | Core: defines the theoretical framework |
| Eq. 15 | f: X → X, x_{n+1} = f(x_n) | §4.1.2, p. 8 | Discrete-time map — the implementation form | Core: used directly in DS5 as daily map |
| Eq. 16 | H(x,v) = E_kin(v) + V(x) | §4.1.2, p. 8 | Conservative-system energy; V(x) potential well | Optional: cited for conceptual framing; V(x) itself deferred (FLAG 1) |
| Eq. 19 | X_{n+1} = X_n + μΔt + Δt σ(X_n) Z_n | §4.1.3, p. 9 | E-M step from StoP — parent equation | Core for DyS: σ→0 limit of this equation is the DyS map |

### Required for implementation — NOT explicitly in paper

| Equation | Formula | Status | Action required |
|---|---|---|---|
| DyS map (σ→0 limit of Eq. 19) | X_{n+1} = clip(X_n + μ, 0, 1) | Standard result; NOT explicitly stated in paper | **Add to paper:** §4.1.2 or §4.1.3 — state the σ→0 limit explicitly as the connection between StoP and DyS |
| Fixed-point condition (1D) | f(X*) = X* ↔ X* + μ = X* ↔ μ = 0 | Standard result; NOT in paper for this behavioral context | **Add to paper:** brief note in §4.1.2 application or §4.2.2 |
| Boundary fixed points (clipped map) | X* = 0 if μ < 0; X* = 1 if μ > 0; X* ∈ [0,1] if μ = 0 | NOT in paper | **Verify and add** to paper if DyS section is to support empirical grounding |
| Jacobian / stability for 1D linear map | J = df/dX = 1 (at all X); eigenvalue λ = 1 (marginally stable) | Standard linear stability result; NOT in paper | **Note in paper** — or note in notebook that the constant-drift map gives marginal stability (not asymptotic) |
| σ→0 regime criterion | is_dys_eligible: σ̂ < median(σ̂) | Implementation choice (FLAG 2) | Not a paper equation — document as implementation decision |
| StoP→DyS reduction | lim_{σ→0} [X_n + μ + σZ_n] = X_n + μ | Standard SDE limit; NOT in paper | **Add to paper** as the formal StoP↔DyS cross-model connection |

### Optional equations — deferred

| Equation | Formula | Why deferred |
|---|---|---|
| Nonlinear gradient ODE | dX/dt = −dV/dX | Requires V(x) from empirical P(X); see StM FLAG 4 |
| Ornstein–Uhlenbeck ODE | dX/dt = θ(μ − X) | Three-parameter system; FLAG 2 deferred; best for DS4 long windows |
| Bifurcation condition | ∂f/∂μ = 0 at (X*, μ*) | Requires continuous μ sweep; DS5 has only 3 conditions |

**Summary of paper gaps to address:**

1. The σ→0 limit equation is missing — the StoP→DyS bridge is not explicitly stated in §4.1.2 or §4.1.3
2. The behavioral fixed-point interpretation (boundaries of [0,1] for constant-drift map) is not stated
3. Marginal stability (λ=1) of the linear map is not discussed — this is an important limitation to acknowledge honestly

---

## 4. Full theory-to-data translation table

| Theoretical quantity | Original scientific meaning | DS5 variable / derived quantity | Mapping type | Confidence | Justification and limitations |
|---|---|---|---|---|---|
| State variable X(t) | System's position in abstract state space at time t | X_t = n_opened_day / n_events_day (daily) | Proxy | Medium | Behavioral tendency proxy from StoP; not latent urge, boredom, or self-control; same proxy as StoP |
| Update rule f(x) | Function governing state change each step | f(X_n) = clip(X_n + μ̂, 0, 1) — σ→0 limit of E-M step | Derived (FLAG 1) | Medium | Reuses μ̂ from StoP; constant-drift simplification; nonlinear ODE deferred |
| Drift parameter μ | Rate and direction of deterministic state change | μ̂ = mean(ΔX_n) from StoP participant_parameters.csv | Direct reuse from StoP | Medium | Already estimated; method of moments; inherits StoP proxy limitation |
| Diffusion σ | Stochastic component of state change | σ̂ from StoP participant_parameters.csv | Direct reuse from StoP | Medium | Used only to define σ→0 partition (is_dys_eligible) |
| Fixed point X* | State where system stops changing: f(X*) = X* | Boundary points {0, 1} for μ≠0; any X for μ=0 | Derived (trivial for linear map) | Low | Constant-drift 1D map has trivial fixed points — boundaries, not interior attractors; see DS5 weakness flag |
| Empirical resting state | Where trajectory actually spends most time | x_mean = time-average of X_t per participant (from StoP) | Proxy (FLAG 3) | Low-Medium | Empirical proxy for fixed-point concept; valid as summary but not identical to DyS fixed point |
| Attractor | Stable fixed point / limit cycle to which trajectories converge | x_mean as weak empirical proxy | Very weak proxy | Low | ⚠ CANNOT demonstrate true mathematical attractor with 1D linear map; terminology must be used carefully; see §10 |
| Stability (eigenvalue) | Rate at which perturbations decay toward fixed point | Not computable for constant-drift linear map (λ=1 everywhere) | Not computable at Step 1 | Very low | Marginal stability of linear map is theoretically trivial; requires nonlinear ODE for informative stability |
| σ→0 regime | Regime where deterministic dynamics dominate | is_dys_eligible: σ̂ below median (FLAG 2) | Derived threshold | Medium | Operationally defined partition; threshold is a design choice, not a principled DyS derivation |
| Friction perturbation | External force displacing trajectory from attractor | h_c = μ̂_ctrl − μ̂_c by condition (from StoP) | Reused from StoP | Low-Medium | Condition-level effect; same as StoP h_c; reinterpretation in DyS language as perturbation |
| Bifurcation | Qualitative change in attractor structure at critical parameter | Not estimable: only 3 discrete conditions (FLAG 4) | Categorical approximation | Very low | ⚠ Cannot trace bifurcation curve with 3 conditions; see §10 |
| Multi-dim state space | State space with dimensions = urge, boredom, fatigue, self-control | Not available: DS5 has only X_t at daily resolution | Not available | None | ⚠ Central DS5 limitation; paper's DyS vision requires multi-dim state; see §10 |
| Phase portrait | Vector field f(x) visualized across state space | 1D: μ̂ distribution across participants, colored by condition | Conceptual analogy | Medium | Technically feasible and interpretable for 1D; honest about being a simplified phase portrait |
| Experimental condition | Control parameter that shifts system dynamics | study_condition (control / default / reintervention) from StoP join | Direct | High | Well-defined RCT condition; best available control-parameter analog in DS5 |

---

## 5. DS5 weakness flags — where strong DyS claims are NOT supportable

These are the locations where DS5 cannot support strong DyS claims. Every one of these must be flagged explicitly in the notebook.

### ⚠ FLAG A: No multi-dimensional state space

The paper's DyS vision (§4.2.2) describes a state space defined by "urge, boredom, fatigue, and self-control." DS5 has exactly one behavioral state variable: X_t. A 1D state space cannot show:
- Limit cycles (requires ≥ 2D)
- Spiral attractors (requires ≥ 2D)  
- Strange attractors / chaos (requires ≥ 3D)
- Manifold structure

**What is possible:** A 1D phase portrait (the vector field at each X value), which for a constant-drift map is trivially a constant arrow pointing left (μ<0) or right (μ>0).

### ⚠ FLAG B: Trivial fixed points for the linear map

For f(X_n) = X_n + μ (constant drift), the only fixed points satisfying f(X*) = X* are:
- μ = 0 → every point is a fixed point (neutral / indifferent behavior)
- μ ≠ 0 → no interior fixed point; boundaries {0, 1} absorb the trajectory

This means the linear constant-drift map does **not** have an interesting interior attractor. The use of "attractor" in the behavioral framing must be qualified as an analogy pointing toward future nonlinear implementation (StM potential V(x) bridge).

### ⚠ FLAG C: Marginal stability (eigenvalue λ = 1)

The Jacobian of the constant-drift map is J = df/dX = 1 everywhere. The eigenvalue λ = 1 means the system is **marginally stable** (neither asymptotically stable nor unstable). Perturbations neither decay nor grow. This is the mathematical reason why the constant-drift model cannot make attractor stability claims.

**What this implies:** To get informative stability, we need either (a) a nonlinear ODE (V(x) potential) or (b) an OU process (mean-reversion parameter θ). Both are deferred. DS4, with longer windows, is the natural next target for OU estimation.

### ⚠ FLAG D: No continuous bifurcation parameter

A bifurcation requires tracing how the qualitative structure of attractors changes as a control parameter varies continuously. DS5 has only 3 discrete conditions. Three points cannot trace a bifurcation curve.

**What is possible:** A categorical comparison of behavioral regime proportions across conditions (e.g., fraction DyS-eligible, fraction μ>0 vs μ<0 by condition). This is informative as a discrete-parameter comparison, but should not be called a bifurcation analysis.

### ⚠ FLAG E: Short observation windows limit inference

Median eligible observation window in DS5 is approximately 25–35 days. For DyS with meaningful convergence rates, longer windows are strongly preferred. Participants with 7–14 day windows have noisy μ̂ and σ̂ estimates, making DyS-eligibility classification uncertain at the individual level.

### ⚠ FLAG F: "Attractor" terminology must be used carefully

The paper uses "attractor" to describe stable usage regimes. In Step 1, the notebook should use the phrase **"empirical resting state"** (x_mean) as the data-grounded term, and reserve "attractor" for the conceptual/theoretical framing only. Do not use "attractor" as if it has been empirically demonstrated.

---

## 6. StoP ↔ DyS ↔ InT connection logic

### The σ→0 limit — formal connection between StoP and DyS

The StoP Euler–Maruyama step (Eq. 19) is:

    X_{n+1} = clip(X_n + μ·Δt + Δt·σ(X_n)·Z_n, 0, 1)

As σ→0, the stochastic term vanishes:

    lim_{σ→0}  X_{n+1} = clip(X_n + μ, 0, 1)

This is exactly the DyS discrete-time map (Eq. 15 in the paper). The σ→0 limit is therefore the formal reduction of StoP to DyS. This connection is not currently in the paper and should be added (§4.1.2 or §4.1.3).

**Empirical implementation:** Participants with σ̂ below median are "DyS-eligible" — their observed behavior is better approximated by the deterministic limit. Participants with σ̂ above median are "StoP-regime" — the stochastic term is non-negligible and StoP remains the appropriate model.

### What DyS captures that StoP does not

| Concept | DyS | StoP |
|---|---|---|
| Fixed points | Explicit: X* where f(X*)=X* | Not primary (stationary distribution is implicit) |
| Attractor framing | Central: trajectories converge to attractors | Periphery: stationary distribution is the analog but not framed as an attractor |
| Geometric intuition | Phase portrait, vector fields, state-space geometry | Probability distribution, variance, correlation |
| Perturbation framing | Friction = perturbation from attractor basin | Friction = drift reduction or diffusion change |
| Stability language | Stable/unstable/marginal fixed points | Noise amplitude (σ̂) as variability measure |

### What StoP captures that DyS does not

| Concept | StoP | DyS |
|---|---|---|
| Noise explicitly modeled | σ̂ measured per participant | Noise suppressed in σ→0 limit |
| Empirical uncertainty | Method-of-moments estimates with appropriate variability | σ̂ is discarded, losing information |
| Short-window accuracy | Tolerates noisy trajectories | Assumes deterministic trajectory; noise is a problem, not a feature |
| Behavioral variability | σ̂ is a first-class result (friction disrupts regularity) | Behavioral variability is not a model output |

### What InT contributes as the third point

InT provides the information-theoretic criterion that can be used for model selection between DyS and StoP:

- **Low H_emp** (concentrated X_t distribution) → participant is closer to DyS regime (near a fixed point, low variability)
- **High H_emp** (spread X_t distribution) → participant is deeper in StoP regime (noisy, no clear resting state)
- **H_SDE** is the differential-entropy analog of σ̂: it connects the Gaussian model assumption (StoP) to the information content of the behavioral distribution
- **DyS threshold criterion** (is_dys_eligible) can also be expressed in InT language: H_SDE < threshold (equivalently, σ̂ < threshold)

The three-way map for the paper:

    StoP: trajectory dynamics (μ̂, σ̂) — how behavior changes day to day
    DyS:  geometric structure (fixed points, attractor analogy) — where behavior tends to rest
    InT:  distributional uncertainty (H_emp, H_SDE) — how predictable behavior is

For a participant with low H_emp, low σ̂, and x_mean near a boundary: all three models agree they have nearly deterministic, low-uncertainty behavior clustered at one extreme. This convergence across three lenses is the most compelling unification result.

### Implications for later unification in the paper

The StoP↔DyS↔InT triangle enables a three-model phenotype dimension: **"behavioral determinism"**.

    High behavioral determinism: low σ̂ (StoP), DyS-eligible, low H_emp (InT)
    Low behavioral determinism: high σ̂ (StoP), StoP-regime, high H_emp (InT)

This dimension maps directly to the paper's phenotype dimension "habitual stability / attractor strength" (§4.3, p. 27). In Step 2, it becomes a candidate for phenotyping via clustering.

---

## 7. Proposed notebook structure — `42_ds5_dynamical_systems.ipynb`

### Cell sequence

| Cell | Type | Content |
|---|---|---|
| 1 | Markdown | **Scope statement**: Goal / Not goal / Output; Step 1 framing; explicit acknowledgment that multi-dim state space is unavailable |
| 2 | Markdown | **FLAG decisions table** (FLAG 1–4) with rationale |
| 3 | Markdown | **Proxy warning** — X_t = n_opened/n_events; same warning as StoP; DyS limitation note: state space is 1D behavioral proxy, not multi-dim latent state |
| 4 | Markdown + LaTeX | **Theory section 1: DyS core** — Eq. 14 (ODE), Eq. 15 (map), Eq. 16 (Hamiltonian/V(x)); paragraph on fixed points and stability |
| 5 | Markdown + LaTeX | **Theory section 2: σ→0 limit** — derivation of DyS map from StoP E-M step; connection to Eq. 19; FLAG 1 applied |
| 6 | Markdown | **Theory-to-data mapping table** (Section 4 of this blueprint) |
| 7 | Markdown | **Equation gaps table** — what is in paper vs what needs to be added |
| 8 | Code | **Setup**: imports, paths, constants (SIGMA_MEDIAN_THRESHOLD, MIN_DAYS=7) |
| 9 | Code | **Data loading**: load `participant_parameters.csv` (StoP), `participant_entropy_metrics.csv` (InT) — no new data pipeline |
| 10 | Code | **σ→0 regime partition**: compute is_dys_eligible flag; add to participants dataframe; describe regime distribution by condition |
| 11 | Code | **Fixed-point analysis**: compute theoretical fixed points by sign of μ̂ (boundary attractor classification); compare with x_mean |
| 12 | Code | **Empirical resting-state analysis**: x_mean distribution by condition (DyS-eligible vs not); is x_mean near predicted boundary attractor? |
| 13 | Code | **Phase portrait / vector field**: 1D vector field — histogram of μ̂ values with sign-coded coloring; binned mean μ̂ as function of x_mean |
| 14 | Code | **DyS ↔ StoP ↔ InT comparison**: joint analysis of (σ̂, H_emp, is_dys_eligible); cross-model regime labeling |
| 15 | Code | **Condition-level dynamics summary**: fraction DyS-eligible by condition; mean x_mean by condition; table export |
| 16 | Code | **Psychosocial correlates** (exploratory): FoMO, belonging vs is_dys_eligible and x_mean (friction-exposed only) |
| 17 | Code | **Export outputs**: all CSV files, model_run_summary.md |
| 18 | Code | **Figure 1**: 1D phase portrait — μ̂ distribution across participants, colored by condition (vector field analog) |
| 19 | Code | **Figure 2**: x_mean (empirical resting state) by condition — violin/box; DyS-eligible vs all |
| 20 | Code | **Figure 3**: σ→0 regime partition — scatter (μ̂, σ̂) with DyS-eligible highlighted; condition colors |
| 21 | Code | **Figure 4**: Three-model comparison — (σ̂, H_emp) scatter colored by DyS-eligible regime |
| 22 | Markdown | **Interpretation and limits**: 6+ bullet points; must include all DS5 weakness flags (A–F) |
| 23 | Markdown | **Forward connections** — to StM (V(x) potential), to DS4 (OU convergence rate), to Step 2 phenotyping |

---

## 8. Proposed saved outputs

**Output root:** `outputs/model_outputs/dynamical_systems/`

| File | Description | Rows | Key columns |
|---|---|---|---|
| `participant_dynamics_parameters.csv` | Per-participant DyS classification and parameters | 414 (StoP-eligible) | participant_id_canonical, study_condition, n_days, mu_hat, sig_hat, x_mean, sigma_mu_ratio, is_dys_eligible, regime_label, predicted_boundary_fp, predicted_fp_value, deviation_from_predicted_fixed_point, behaviorally_deterministic, H_emp, H_SDE |
| ~~`fixed_point_summary.csv`~~ | **Plan-vs-implementation note (added 2026-08-07):** this file was never produced as a separate CSV. The fixed-point columns it planned (`fp_type`→shipped as `predicted_boundary_fp`, `deviation_from_fp`→shipped as `deviation_from_predicted_fixed_point`; the 2026-08-07 version of this note said `attractor_boundary`, which is not the name that shipped — corrected on audit) were merged directly into `participant_dynamics_parameters.csv` above instead. No other doc references this filename, so this row is inert — kept here only as a record of the plan-vs-implementation drift, not an outstanding gap. | — | — |
| `condition_dynamics_summary.csv` | Condition-level DyS statistics | 3 rows | study_condition, n_eligible, n_dys_eligible, frac_dys_eligible, mean_x_mean, median_x_mean, mean_mu_hat, frac_upper_boundary_fp, frac_lower_boundary_fp, frac_neutral_fp, mean_deviation_from_predicted_fp |
| `dys_stop_int_comparison.csv` | Per-participant cross-model table | 414 | participant_id_canonical, mu_hat, sig_hat, H_emp, H_SDE, is_dys_eligible, predicted_boundary_fp, deviation_from_predicted_fixed_point, behaviorally_deterministic, regime_label |
| `psychosocial_dys_correlations.csv` | Pearson r of DyS targets (x_mean, deviation_from_predicted_fixed_point, is_dys_eligible) vs 5 pre-survey psychosocial scales, friction-exposed only | 15 | target, scale, r, p, n, nominally_sig |
| `model_run_summary.md` | Run record with parameters, FLAG decisions, key results | — | — |
| `figures/fig1_dys_vector_field.png` | 1D vector field: μ̂ distribution by condition (phase portrait analog) | — | — |
| `figures/fig2_dys_resting_state.png` | x_mean (empirical resting state) distribution by condition | — | — |
| `figures/fig3_dys_regime_partition.png` | Scatter (μ̂, σ̂): DyS-eligible vs StoP-regime; condition colors | — | — |
| `figures/fig4_dys_stop_int.png` | Three-model comparison: (σ̂, H_emp) scatter, DyS-eligible highlighted | — | — |

### Column reference: participant_dynamics_parameters.csv

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Participant identifier (from StoP) |
| `study_condition` | str | RCT condition (control/default/reintervention) |
| `n_days` | int | Days in StoP estimation window (≥7) |
| `mu_hat` | float | Drift estimate (from StoP — reused) |
| `sig_hat` | float | Diffusion estimate (from StoP — reused) |
| `x_mean` | float | Time-average daily X_t — empirical resting state proxy |
| `is_dys_eligible` | bool | True if σ̂ < median(σ̂) — σ→0 partition (FLAG 2) |
| `predicted_boundary_fp` | str | "lower" (μ̂<−0.005), "upper" (μ̂>+0.005), "neutral" (\|μ̂\|≤0.005) |
| `predicted_fp_value` | float | 0.0 if "lower", 1.0 if "upper", x_mean if "neutral" (FLAG 3 proxy) |
| `deviation_from_predicted_fixed_point` | float | \|x_mean − predicted_fp_value\|; identically 0 for "neutral" participants by construction |
| `behaviorally_deterministic` | bool | is_dys_eligible AND H_emp < median(H_emp) — joint DyS+InT convergence flag |
| `sigma_mu_ratio` | float | From StoP — retained for continuity |
| `H_emp` | float | Empirical entropy from InT — joined |
| `H_SDE` | float | StoP bridge entropy from InT — joined |
| `regime_label` | str | "DyS-deterministic" or "StoP-stochastic" |

---

## 9. Data pipeline — how the notebook loads and processes data

### Sources (no new data pipeline needed)

| File | Role |
|---|---|
| `outputs/model_outputs/stochastic_processes/participant_parameters.csv` | Primary input — μ̂, σ̂, x_mean per participant; 414 rows |
| `outputs/model_outputs/information_theory/participant_entropy_metrics.csv` | Join for H_emp, H_SDE — 572 rows (inner join on participant_id_canonical gives 414 with both StoP and InT) |
| `outputs/features/ds5/ds5_survey_features.csv` | For psychosocial correlates (FoMO, belonging, ostracism) — join on participant_id_canonical |

**The DyS notebook does NOT reload ds5_behavioral_clean.csv.** All necessary quantities are already computed in StoP and InT outputs. This makes the DyS notebook the lightest in Stage 4 Step 1 so far.

### Pipeline steps

1. Load `participant_parameters.csv` — 414 rows
2. Load `participant_entropy_metrics.csv` — inner join on `participant_id_canonical` → 414 rows with both StoP + InT fields
3. Compute `SIGMA_THRESHOLD = median(sig_hat)` across all 414 eligible participants
4. Assign `is_dys_eligible = sig_hat < SIGMA_THRESHOLD`
5. Assign `predicted_boundary_fp`: "lower" if μ̂ < −MU_THRESHOLD, "upper" if μ̂ > MU_THRESHOLD, "neutral" otherwise (reuse MU_THRESHOLD=0.005 from StoP)
6. Compute `predicted_fp`: 0 if "lower", 1 if "upper", x_mean if "neutral"
7. Compute `deviation_from_predicted_fixed_point = abs(x_mean − predicted_fp)`
8. Assign `regime_label`: "DyS-deterministic" if is_dys_eligible else "StoP-stochastic"
9. Join survey features for psychosocial correlates
10. Export all outputs

### Sanity checks

- `n(is_dys_eligible=True)` ≈ 50% of 414 by construction (median threshold)
- `mean(x_mean)` should match StoP reported x_mean distribution (~0.6–0.8 range for all conditions)
- `deviation_from_predicted_fixed_point` should be smaller for DyS-eligible participants than StoP-regime participants (key empirical test)

---

## 10. Forward connections from DyS

| Connection | Mechanism | Target |
|---|---|---|
| DyS → StM | DyS fixed points are minima of potential V(x); P_inf(x) ∝ exp(−2V(x)/σ²) → V(x) from empirical P(X_t) | Notebook 41 (StM) |
| DyS → OU (DS4) | Ornstein–Uhlenbeck process has convergence rate θ; DS4's 897-day windows make θ estimable | DS4 DyS notebook (future) |
| DyS → Phenotyping (Step 2) | is_dys_eligible + predicted_boundary_fp + x_mean → "behavioral determinism" phenotype dimension | Notebook 100 |
| DyS → StoP unification | σ→0 limit is the formal reduction; DyS notebook documents the partition empirically | Already in StoP + comparison doc |
| DyS → InT unification | Low H_emp ↔ DyS-eligible: InT criterion for model selection | Already in InT + comparison doc |
| DyS → Paper §4.1.2 | Add: σ→0 limit equation; boundary fixed points; marginal stability note; behavioral interpretation | Must add before submission |

---

## 11. Equation gaps to resolve before or during implementation

| Gap | Status | Action |
|---|---|---|
| σ→0 limit of Eq. 19 → DyS map | NOT in paper | **Must add to paper** §4.1.2 or §4.1.3 — this is the StoP↔DyS bridge |
| Fixed-point condition for 1D clipped map | NOT in paper | **Add to paper** — brief statement that boundary fixed points {0,1} are the consequence of constant drift |
| Marginal stability (λ=1) of linear map | NOT in paper | **Add as limitation note** in §4.1.2 or §4.2.2 |
| Behavioral interpretation of attractor → x_mean proxy | NOT in paper | **Add caveat** in §4.2.2 — distinguish mathematical attractor from empirical resting state |
| Formal definition of "DyS-eligible regime" | NOT in paper | **Document as implementation decision** in notebook FLAG table; not a paper equation |
| Bifurcation absence with only 3 conditions | NOT in paper | **Acknowledge in §4.2.2 limitations** — this is an honest statement of DS5's limits for DyS |

---

## 12. Summary: what this notebook adds to Stage 4 Step 1

| Output | Source model | DyS contribution |
|---|---|---|
| μ̂, σ̂, x_mean | StoP (reused) | Reinterpreted in geometric / attractor language |
| is_dys_eligible | New (FLAG 2 partition) | First empirical test of σ→0 regime |
| predicted_boundary_fp | New (from sign of μ̂) | Theoretical fixed-point framing of behavioral tendency |
| deviation_from_predicted_fixed_point | New | First test of whether behavior actually clusters near predicted attractor |
| regime_label | New | Cross-model identifier: DyS-deterministic vs StoP-stochastic |
| Three-model comparison | New | Closes StoP↔InT↔DyS triangle with empirical data |
| Phase portrait (1D) | New | First visualization of DS5 behavioral vector field |

---

*This blueprint is the design document for `notebooks/42_ds5_dynamical_systems.ipynb`. Do not implement the notebook until the user confirms this blueprint.*
