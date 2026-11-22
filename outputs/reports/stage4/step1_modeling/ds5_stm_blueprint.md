# DS5 StM Model — Stage 4 Step 1 Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**
**Written:** 2026-04-17
**Notebook:** `notebooks/41_ds5_statistical_mechanics.ipynb`
**Producing dataset:** DS5 (German Adolescents RCT, N=573)
**Model family:** Statistical Mechanics (StM)
**Prerequisites:** Notebooks 43 (StoP — complete), 45 (InT — complete), 42 (DyS — complete)

---

## 1. Is DS5 the right dataset for the first StM implementation?

**Yes — but it is the hardest of the four Step 1 notebooks so far, and it requires a more layered
strategy than StoP, InT, or DyS.**

DS5 is the correct first StM target for the following reasons:

1. **StoP, DyS, and InT are all complete on DS5.** StM is formally downstream of all three. The
   Boltzmann bridge P_inf(x) ∝ exp(−2V(x)/σ²) requires σ̂ from StoP, the potential V(x) from
   the stationary distribution of the SDE (which connects to DyS fixed points), and produces an
   entropy H_StM that should triangulate against H_emp and H_SDE from InT. None of these inputs
   require a new data pipeline — they are already in the model output files.

2. **The RCT condition structure is unique to DS5.** The paper frames friction as an "external
   field h" that shifts the probability of entering a "use" vs "non-use" state (§4.2.1). This
   framing is most meaningful when a true reference condition exists. DS5 control gives this
   reference. The effective susceptibility χ = ∂⟨X⟩/∂h is measurable at the condition level.

3. **The paper explicitly selects StM as a Step 1 model.** §4.4 notes that "Statistical Mechanics
   may also be relatively feasible if behavior is discretized into use/non-use states." This is
   exactly the two-state Boltzmann framing planned here (FLAG 1).

4. **The Boltzmann bridge was deferred from StoP (FLAG 4) specifically to be developed in this
   notebook.** That deferral was a design choice, not a dead end. The intent was always that StM
   would be the place where V(x) and β_behav are introduced, completing the StoP ↔ StM connection.

**Why this notebook is harder than DyS:**

DyS used only σ̂ and μ̂ from StoP and reinterpreted them in geometric language. StM requires an
additional derivation step: estimating P_inf(x) from the empirical X_t distribution, and inverting
it to get V(x). For individual participants with 7-45 daily observations, this step is noisy. The
Step 1 strategy therefore has two levels:

- **Level 1 (most defensible):** Effective temperature β_behav = 2/σ̂², derived directly from
  StoP's σ̂. No V(x) estimation needed. This is the cleanest StM bridge.

- **Level 2 (condition-level only):** Pooled P̂_inf(x) per condition (3,000+ data points per
  condition), V(x) estimated via KDE inversion. More stable than individual V(x).

- **Level 3 (individual V(x), flagged as exploratory):** Individual-level V(x) for participants
  with the longest windows. Explicitly flagged as noisy and illustrative only.

**Critical DS5 limitation for StM (must be stated clearly):**

The constant-drift SDE from StoP (dX_t = μ dt + σ dW_t) does NOT have a potential-well structure.
The Boltzmann stationary distribution P_inf(x) ∝ exp(−2V(x)/σ²) formally applies to the
potential-well SDE dX_t = −(dV/dx) dt + σ dW_t. In the constant-drift model, V(x) = −μx (a
linear slope), which does not produce a normalizable stationary distribution on R. On the clipped
[0,1] domain, the stationary distribution concentrates at the boundary rather than forming a
smooth Boltzmann density. This means the β = 2/σ̂² mapping is an approximation — valid as an
analog but not as a strict thermodynamic derivation. This must be flagged everywhere.

---

## 2. FLAG decisions for DS5 StM Step 1

| Flag | Decision | Alternative (deferred) | Why deferred |
|---|---|---|---|
| FLAG 1 | Two-state behavioral Boltzmann model: X_t discretized into "high-use" (X_t > 0.5) and "low-use" (X_t ≤ 0.5) states; single-particle model (no coupling) | Continuous V(x) via KDE inversion for individual participants | Individual-level V(x) requires dense P_inf; 7-45 observations is too noisy for reliable potential estimation |
| FLAG 2 | Effective temperature: β_behav = 2/σ̂² from StoP (constant-drift approximation) | OU-process β = 2θ/σ² (mean-reversion rate θ explicit) | OU requires a third parameter θ; DS4's longer windows are the correct target for OU-based β estimation |
| FLAG 3 | No Ising coupling between participants: independent single-spin model per participant | Population-level Ising where participants interact | DS5 participants are independent individuals; no interaction term is available or theoretically justified |
| FLAG 4 | Phase transition analysis deferred: no critical temperature T_c estimated | T_c from continuous β sweep or condition-parameterized phase diagram | Only 3 discrete conditions; cannot trace a phase boundary; defer to synthetic simulation or DS4 |

---

## 3. Equations to use — with paper status and role

### Core equations — ALREADY IN PAPER

| Eq. | Formula | Paper location | Role | Core/optional |
|---|---|---|---|---|
| Eq. 1 | H(q,p) = T(p) + V(q) | §4.1.1, p. 7 | Hamiltonian — defines energy landscape concept | Conceptual framing; V(q) is the part relevant to Step 1 |
| Eq. 2 | P(s) = e^{−βH(s)} / Z | §4.1.1, p. 7 | Boltzmann distribution — the central equation | Core: all StM quantities derive from this |
| Eq. 3 | Z(H) = Σ_i e^{−E_i/k_BT} | §4.1.1, p. 7 | Partition function — normalizer of Boltzmann distribution | Core: needed for F and Z computation |
| Eq. 4 | F = −k_BT ln Z | §4.1.1, p. 7 | Helmholtz free energy — balances energy vs entropy | Core for behavioral free energy analog |
| Eq. 5 | S = k_B ln Ω | §4.1.1, p. 7 | Thermodynamic entropy — number of accessible microstates | Bridge to InT (S ↔ H_emp) |
| Eq. 7 | C_v = (β²/N)(⟨E²⟩ − ⟨E⟩²) | §4.1.1, p. 7 | Specific heat — variance of energy = fluctuation measure | Optional: computable as β² · Var(X_t); connects to σ̂² |
| Eq. 8 | χ = (∂M/∂H)_T | §4.1.1, p. 7 | Susceptibility — sensitivity to external field | Core: behavioral susceptibility χ_behav = ∂⟨X⟩/∂h_friction |
| Eq. 10 | H = −J Σ_{⟨i,j⟩} s_i s_j | §4.1.1, p. 8 | Ising Hamiltonian — collective coupling model | Conceptual reference only; J = 0 in DS5 (FLAG 3) |
| Eq. 11 | H = −J Σ s_i s_j − h Σ s_i | §4.1.1, p. 8 | Ising with external field — friction as external field h | Core analogy: h ↔ friction condition |
| Eq. 12 | Z = Σ e^{−βH_i} | §4.1.1, p. 8 | Discrete partition function | Core for two-state model |
| Eq. 13 | F = −k_BT ln Z | §4.1.1, p. 8 | Free energy from partition function | Core |

### Required for implementation — NOT in paper

| Equation | Formula | Status | Action required |
|---|---|---|---|
| Boltzmann bridge (StoP → StM) | P_inf(x) ∝ exp(−2V(x)/σ²) for potential-well SDE dX = −(dV/dx)dt + σ dW | Mathematically standard; NOT in paper | **Must add to paper** §4.1.1 or §4.1.3 as StoP↔StM bridge; note the constant-drift caveat |
| Effective behavioral temperature | β_behav = 2/σ̂² (approximation from SDE; exact only for OU/potential-well) | NOT in paper | **Must add to paper** §4.1.1 or §4.2.1; flag it as an approximation under constant-drift |
| Potential inversion | V(x) = −(σ̂²/2) log P̂_inf(x) | NOT in paper | **Must add to paper** §4.2.1 as behavioral potential estimation method; flag condition-level vs individual-level |
| Two-state partition function | Z_2 = e^{−β·E_use} + e^{−β·E_non-use}; E_use = −ln(p̂_use) | Standard; NOT in paper for behavioral context | **Must add** §4.2.1 — the single-particle two-state model is the simplest defensible DS5 StM implementation |
| Behavioral susceptibility | χ_behav = β · p̂_use · (1 − p̂_use) (two-state model) | Standard; NOT in paper | **Must add** §4.2.1 as the intervention sensitivity measure |
| StM entropy (continuous) | H_StM = −∫ P_inf(x) log₂ P_inf(x) dx | NOT in paper | **Must add** §4.2.1 for InT bridge; allows triangulation H_StM vs H_emp vs H_SDE |
| Behavioral free energy (analog) | F_behav = E_behav − (1/β) · S_behav | NOT in paper | **Add as conceptual equation** §4.2.1; not rigorously derived but motivates the E-S tradeoff framing |

### Optional equations — deferred to later stages

| Equation | Formula | Why deferred |
|---|---|---|
| Ising with coupling | H = −J Σ s_i s_j − h Σ s_i | No coupling between participants in DS5; J = 0 is the only defensible choice |
| Ornstein-Uhlenbeck β | β_OU = 2θ/σ² | Requires mean-reversion rate θ; DS4 long windows needed |
| Phase boundary | T_c from ∂²F/∂h² = 0 | Requires continuous h variation; only 3 discrete conditions |
| Hysteresis loop | x(h) ≠ x(−h): path-dependent magnetization | Requires behavioral data before, during, and after friction removal; not available in DS5 |

**Summary of paper gaps to address before submission:**

1. Boltzmann bridge equation P_inf(x) ∝ exp(−2V(x)/σ²) — connects StoP to StM; NOT in paper
2. β_behav = 2/σ̂² mapping with explicit caveat about constant-drift approximation — NOT in paper
3. Potential inversion V(x) = −(σ̂²/2) log P̂_inf(x) — NOT in paper
4. Two-state partition function and behavioral susceptibility formula — NOT in paper
5. H_StM = −∫ P_inf log P_inf dx as the StM entropy bridge to InT — NOT in paper
6. Explicit statement that DS5 constant-drift SDE only approximates the potential-well SDE needed for exact Boltzmann framing — NOT in paper

---

## 4. Full theory-to-data translation table

| Theoretical quantity | Original scientific meaning | DS5 variable / derived quantity | Mapping type | Confidence | Justification and limitations |
|---|---|---|---|---|---|
| System microstate s | State of one particle/spin at a moment | X_t = n_opened_day / n_events_day (daily) — or s ∈ {+1, −1} for two-state model | Proxy | Medium | Behavioral tendency proxy from StoP; not latent urge, boredom, or self-control |
| State space | Set of all possible microstates | [0, 1] continuous (or {high-use, low-use} for two-state FLAG 1) | Direct (continuous) / Derived (two-state) | Medium | Daily X_t ∈ [0,1] is well-defined; two-state simplification loses intra-participant variability structure |
| Hamiltonian H(s) | Total energy function over microstates | E_use = −ln(p̂_use); E_non-use = −ln(p̂_non-use); or V(x) via inversion | Derived (FLAG 1) | Low-Medium | Energy defined as negative log-probability (information-theoretic energy); not a physical energy |
| Potential V(x) | Continuous energy landscape; minima = stable states | V̂(x) = −(σ̄²/2) log P̂_inf(x) from pooled KDE per condition | Derived (FLAG 1, condition-level only) | Low | ⚠ Individual-level V(x) requires 7-45 daily observations — too noisy; condition-level pools 3,000+ points |
| Temperature T (inverse β) | System's exploration intensity; T controls P(s) | T_behav = σ̂²/2; β_behav = 2/σ̂² per participant | Derived from StoP (FLAG 2) | Medium | ⚠ Exact only for potential-well SDE; approximation for constant-drift SDE; higher σ̂ = more behavioral exploration |
| Partition function Z | Sum of Boltzmann weights over all states | Z_2 = e^{−β · E_use} + e^{−β · E_non-use} (two-state) | Derived (FLAG 1) | Low-Medium | Two-state simplification; continuous Z would require integrating over [0,1] |
| Boltzmann distribution P(s) | Probability of state s at equilibrium | P̂(X_t) = empirical daily distribution; compare with Boltzmann fit | Empirical (observed) vs theoretical | Low-Medium | ⚠ Thermodynamic equilibrium requires full state-space exploration; 7-45 day windows weakly support this |
| Free energy F | F = E − TS; balance of energy cost vs entropic exploration | F_behav = E_behav − (1/β) · H_emp (in bits) | Derived (conceptual) | Low | Numerically computable but interpretation is analogical; "energy" and "entropy" here are behavioral analogs |
| Thermodynamic entropy S | S = k_B ln Ω; number of accessible microstates | S_StM ≈ H_emp from InT (empirical entropy); H_StM from Boltzmann P_inf | Bridge to InT | Medium | H_emp already computed; H_StM is the theoretical StM prediction; r(H_StM, H_emp) is the cross-model validation |
| Specific heat C_v | Variance of energy; fluctuation measure | C_behav = β² · Var(X_t) = β² · σ̂² ≈ 4 (simplifies for β = 2/σ²) | Derived from StoP | Low-Medium | C_behav = β² · σ̂² reduces to 4 under β = 2/σ̂²; near-constant across participants at this level; condition-level variance may differ |
| Susceptibility χ | ∂⟨M⟩/∂h: how strongly mean state responds to external field | χ_behav = β · p̂_use · (1 − p̂_use) per participant; or χ_cond = Δ⟨X_t⟩ / Δh_friction condition-level | Derived (participant-level + condition-level) | Low-Medium | Condition-level susceptibility is the most defensible (direct comparison across 3 conditions); individual χ is noisy |
| External field h | Biases system toward one state; breaks symmetry | Friction condition: control (h ≈ 0), default (h > 0), reintervention (h > 0, different strength) | Proxy | Low-Medium | ⚠ The friction "strength" is ordinal not cardinal; cannot assign precise h values; condition-level comparison only |
| Energy minimum (stable state) | Minimum of V(x) = attractor of the SDE | Peak of P̂_inf(x); compare with x_mean from StoP | Derived (condition-level KDE) | Low | ⚠ For individuals, peak of P̂_inf with 7-45 points is unreliable; condition-level only |
| Hysteresis | Path-dependence: system retains memory of past perturbations | NOT AVAILABLE: DS5 has no post-friction baseline period | Not available | None | ⚠ Would require behavioral data after intervention removal; DS5 study design does not include this |
| Phase transition | Qualitative change in macroscopic order at T_c | NOT AVAILABLE: only 3 discrete conditions; cannot trace T_c | Not available | None | ⚠ See weakness FLAG E |
| Ising spin coupling J | Strength of spin-spin interaction | NOT AVAILABLE: DS5 participants are independent (J = 0) | Not applicable (FLAG 3) | None | ⚠ No coupling between participants; single-particle model only |
| Magnetization ⟨M⟩ | Mean order parameter of the system | ⟨X_t⟩ = x_mean per participant (from StoP) | Direct reuse from StoP | Medium | x_mean is the behavioral magnetization analog — mean override tendency |

---

## 5. DS5 weakness flags — where strong StM claims are NOT supportable

These must be flagged explicitly in every relevant notebook cell.

### ⚠ FLAG A: Constant-drift SDE ≠ potential-well SDE

The Boltzmann bridge P_inf(x) ∝ exp(−2V(x)/σ²) is formally correct for the **potential-well SDE**:
dX_t = −(dV/dx) dt + σ dW_t. The StoP notebook used the **constant-drift SDE**: dX_t = μ dt + σ dW_t,
which is V(x) = −μx (linear, non-confining). A linear potential does not produce a normalizable
stationary distribution on R, and on [0,1] it produces a boundary-concentrated distribution, not a
smooth Boltzmann density.

**Consequence:** The mapping β_behav = 2/σ̂² and the potential inversion V(x) = −(σ̂²/2) log P̂_inf(x)
are approximations that would be exact only if the SDE had a confining potential. They are useful
behavioral analogs but should not be presented as rigorous thermodynamic quantities.

**What is still valid:** The qualitative ordering (higher σ̂ → higher T_behav → more exploration) is
robust. The quantitative values of β_behav are approximate.

### ⚠ FLAG B: Individual V(x) estimation is underpowered

7-45 daily X_t observations per participant cannot reliably support a continuous potential landscape.
KDE on 7-45 points produces artifacts (spurious peaks, excessive smoothing) that should not be
interpreted as real potential wells.

**What is valid:** Condition-level V(x) from pooled data (3,000+ points per condition) is more
defensible but still approximate. Use it for visualization and conceptual illustration, not for
strong inferential claims about individual participants.

### ⚠ FLAG C: Thermodynamic equilibrium is not established

Statistical mechanics assumes the system has sampled its state space ergodically — that is, given
enough time, the empirical distribution P̂_inf(x) converges to the true stationary distribution.
With 7-45 days, there is no guarantee that each participant's behavior has converged to any
equilibrium. Some participants may be in transient adaptation states, not a stationary regime.

**Consequence:** P̂_inf(x) per participant should be labeled as an "empirical state distribution,"
not a "stationary distribution" or "thermodynamic equilibrium distribution."

### ⚠ FLAG D: No Ising coupling (J = 0 is the only defensible assumption)

The Ising model requires spin-spin interactions (coupling constant J). DS5 participants are
independent individuals with no measured social interaction terms. Applying the Ising Hamiltonian
with J > 0 would require either (a) defining what "neighboring spins" means for participants, or
(b) treating each participant's own sequential decisions as spins — which is a within-person
formulation requiring event-level temporal structure not available in daily-aggregated X_t.

**What is valid:** A single-particle model (J = 0) with external field h (friction condition) is
the correct DS5 implementation. The Ising framing is cited as conceptual context, not as an
implemented coupling model.

### ⚠ FLAG E: Phase transitions require continuous parameter tuning — not available

A phase transition at critical temperature T_c requires tracing how macroscopic order changes as a
control parameter (temperature or field strength) is varied continuously. DS5 has three discrete
friction levels (control, default, reintervention). Three points cannot define a phase boundary.

**What is valid:** A categorical comparison — condition-level β_behav values, condition-level
p_use, condition-level susceptibility χ — can suggest whether friction moves the population toward
or away from an order-disorder transition, but this is an analogy, not a bifurcation analysis.

### ⚠ FLAG F: Hysteresis cannot be demonstrated in DS5

Hysteresis (path-dependence: x(h) ≠ x after h is removed) requires observing behavior before,
during, AND after the friction intervention is removed. DS5 has pre- and post-surveys, but the
behavioral log covers only the active study period (during intervention). There is no post-intervention
behavioral baseline to detect whether behavior returned to pre-study levels.

**What is valid:** The paper's discussion of hysteresis (§4.2.1) is motivational context for why
StM is conceptually relevant. It cannot be empirically tested in DS5.

### ⚠ FLAG G: "Energy" in behavioral StM is information-theoretic, not physical

The behavioral energy E_use = −ln(p̂_use) is the negative log-probability (surprisal), not a
physical energy in joules. Calling this "energy" imports a thermodynamic vocabulary that is
useful but requires explicit qualification. The equation P(s) = e^{−βH(s)} / Z is used as an
analogy: states with lower "energy" (higher probability) are more frequently occupied.

This is a valid analogy in physics-inspired behavioral modeling. But readers should understand that
β_behav is not a temperature in the physical sense — it is a dimensionless quantity that encodes
how concentrated the behavioral distribution is.

---

## 6. StoP ↔ DyS ↔ InT ↔ StM connection logic

### The formal chain of bridges

```
StoP (43)
  σ̂ (diffusion per participant)
  └── σ→0 limit ──────────────── DyS (42)
  │                               fixed points, is_dys_eligible, x_mean
  └── H_SDE = ½ log₂(2πeσ̂²) ── InT (45)
  │                               H_emp, H_SDE, H_out, H_app, H_hour
  └── β_behav = 2/σ̂²  ─────── StM (41)   ← NEW
       V(x) = −(σ̂²/2) log P̂_inf(x)
       P_inf(x) ∝ exp(−2V(x)/σ²)
```

**What each model adds:**

| Model | Primary question | Key output | Behavioral framing |
|---|---|---|---|
| StoP | How does behavior move? | μ̂, σ̂: trajectory dynamics | Direction and noise of daily override tendency |
| DyS | Where does behavior tend to rest? | x_mean, is_dys_eligible: geometric resting state | Fixed-point structure; deterministic vs stochastic regime |
| InT | How uncertain is behavior? | H_emp, H_SDE, H_out: distributional uncertainty | Behavioral predictability; entropy of outcome and state distributions |
| StM | What is the energy landscape? | β_behav, V(x), χ_behav: exploration structure | Behavioral "temperature"; cost-probability mapping; intervention sensitivity |

### What StM adds that StoP, DyS, InT cannot:

1. **The energy cost framing.** StoP knows that high-σ̂ participants are more variable. DyS knows
   they are unlikely to be in the deterministic regime. InT knows they have higher H_emp. But only
   StM makes explicit what the "cost" of override vs non-override is, framed as a probability
   landscape. The Boltzmann distribution says: the most probable state is the lowest-energy state,
   and β controls how steeply the energy difference matters.

2. **Susceptibility as intervention sensitivity.** χ_behav = β · p̂_use · (1 − p̂_use) captures
   something none of the other three models compute directly: how sensitively mean behavior
   responds to a small change in the external friction field. Participants near p_use ≈ 0.5 and
   with high β (low σ̂) have highest χ — they are poised to tip in either direction from a
   small intervention push.

3. **The free energy tradeoff.** F_behav = E_behav − (1/β) · S_behav makes explicit the tension
   between habituation (low energy states) and behavioral flexibility (high entropy). Participants
   with low F_behav have found a state that is both low-energy (habitual override) and low-entropy
   (predictable) — the "locked-in" phenotype. Participants with high F_behav are in higher-energy
   but higher-entropy states — the "exploratory" phenotype.

4. **A third entropy estimate for cross-model triangulation.** H_StM = −∫ P_inf log₂ P_inf dx is
   the entropy of the fitted Boltzmann distribution. Adding r(H_StM, H_emp) to the r(H_SDE, H_emp)
   = 0.650 already computed in InT gives a three-way entropy comparison: parametric SDE (H_SDE),
   Boltzmann fit (H_StM), and non-parametric empirical (H_emp). Agreement across all three
   would be strong convergent evidence for the Gaussian-Boltzmann approximation.
   (⚠ ordering only — H_SDE and H_StM are differential entropies, H_emp is a discrete K=10-bin
   entropy; their levels differ by ~log₂10 = 3.32 bits by construction and cannot agree in
   magnitude.)

### Cross-model validation structure

| Comparison | Left | Right | Expected relationship | Confidence |
|---|---|---|---|---|
| StoP → StM | σ̂ | β_behav = 2/σ̂² | Perfect monotone negative (by definition) | High — deterministic transform |
| InT ↔ StM | H_SDE | H_StM | r close to 1.0 (both Gaussian-derived) | High — expect r ≈ 1 if Boltzmann fit is consistent |
| InT ↔ StM | H_emp | H_StM | r similar to r(H_emp, H_SDE) = 0.650 | Medium — H_StM is Boltzmann fit; H_emp is non-parametric |
| DyS ↔ StM | is_dys_eligible | β_behav | DyS-eligible have higher β (lower T_behav) | High — low σ̂ → high β; both derived from σ̂ |
| DyS ↔ StM | x_mean | V_min location | x_mean should be near V(x) minimum location | Low — noisy for individuals; better at condition level |
| StM-new | χ_behav | Δ⟨X_t⟩ by condition | Higher χ → larger observed condition difference | Medium — tests susceptibility as intervention sensitivity |

### Four-model convergence criterion

The strongest result available in Stage 4 Step 1 will be the identification of a subset of
participants where all four models converge on the same behavioral characterization:

    Low σ̂ (StoP)              → low behavioral noise; near deterministic
    is_dys_eligible = True (DyS) → in the σ→0 regime; near boundary resting state
    Low H_emp (InT)             → behaviorally predictable; concentrated distribution
    High β_behav (StM)          → low behavioral "temperature"; narrow energy well

    ⚠ NOT four independent axes. β_behav ≡ 2/σ̂² and is_dys_eligible ≡ (σ̂ < median σ̂ = 0.181220),
    so the σ̂, DyS and β clauses are the SAME clause. The criterion reduces to
    (low σ̂ AND low H_emp), which is exactly DyS notebook 42's existing
    `behaviorally_deterministic` flag. Verified: the two columns select identical
    participant sets (crosstab [[260,0],[0,154]]). StM contributes no participants to
    this flag; it is a two-axis result reported across four notebooks.

    ⚠ A fifth clause 'Low χ_behav (StM)' was originally listed here and was deliberately NOT
      implemented in notebook 41 — it is incompatible with the other clauses. Because
      χ_behav = β·p·(1−p) and Spearman(χ_behav, β_behav) = 0.915, 'high β AND low χ' is close
      to an empty set. Empirically the convergent group has 4.0× HIGHER mean χ_behav than the
      non-convergent group (33.98 vs 8.41).

These participants are the "thermodynamically ordered, behaviorally entrenched" phenotype: low
noise, low entropy, high β. ⚠ They are NOT 'hard to move' in the χ sense — they are the
highest-χ group in the sample (mean 33.98 vs 8.41), because χ = β·p·(1−p) rewards high β
whenever p_use is not extreme. 'Ordered' and 'insensitive to friction' are therefore NOT the
same thing under this χ definition, and the two must not be conflated in thesis prose.

---

## 7. Notebook structure — `41_ds5_statistical_mechanics.ipynb`

| Cell | Type | Content |
|---|---|---|
| 1 | Markdown | **Scope statement**: Goal / Not goal / Output; Step 1 framing; acknowledgment that full thermodynamic StM requires equilibrium and coupling that DS5 cannot support; explicit statement that this notebook implements the Boltzmann bridge and effective temperature analog |
| 2 | Markdown | **FLAG decisions table** (FLAG 1–4) with rationale |
| 3 | Markdown | **Proxy warning** — X_t = n_opened/n_events; same warning as StoP/DyS/InT; StM-specific caveat about constant-drift vs potential-well SDE approximation |
| 4 | Markdown + LaTeX | **Theory section 1: StM core** — Eq. 1 (Hamiltonian), Eq. 2 (Boltzmann), Eq. 3–4 (Z, F), Eq. 5 (entropy), Eq. 7 (specific heat), Eq. 8 (susceptibility); brief conceptual paragraph on each |
| 5 | Markdown + LaTeX | **Theory section 2: Ising model and external field** — Eq. 10–11 (Ising); note J=0 (FLAG 3); h as friction field analog |
| 6 | Markdown + LaTeX | **Theory section 3: Boltzmann bridge from StoP** — potential-well SDE; P_inf(x) ∝ exp(−2V(x)/σ²); β_behav = 2/σ̂²; FLAG A caveat (constant-drift approximation) |
| 7 | Markdown + LaTeX | **Theory section 4: Two-state behavioral model** — Z_2 = e^{−βE_use} + e^{−βE_non-use}; χ_behav = β·p_use·(1−p_use); FLAG 1 applied |
| 8 | Markdown | **Theory-to-data mapping table** (Section 4 of this blueprint) |
| 9 | Markdown | **Equation gaps table** — what is in paper vs what needs to be added |
| 10 | Code | **Setup**: imports, paths, constants (BETA_THRESHOLD, KDE_BANDWIDTH, THRESHOLD_USE = 0.5) |
| 11 | Code | **Data loading**: load `participant_parameters.csv` (StoP), `participant_entropy_metrics.csv` (InT), `participant_dynamics_parameters.csv` (DyS) — no new data pipeline |
| 12 | Code | **Level 1 — effective temperature**: compute β_behav = 2/σ̂² per participant; T_behav = σ̂²/2; describe β distribution by condition |
| 13 | Code | **Level 1 — two-state model**: compute p_use = mean(X_t > 0.5) per participant using x_mean proxy; E_use = −ln(p_use); Z_2; χ_behav = β·p_use·(1−p_use); F_behav; describe by condition |
| 14 | Code | **Level 2 — condition-level V(x)**: pool X_t from behavioral clean file per condition; KDE estimation of P̂_inf(x) per condition; V̂(x) = −(σ̄²/2) log KDE(x); plot condition-level landscapes |
| 15 | Code | **Level 2 — V(x) minima**: find peak of P̂_inf(x) per condition; compare with condition-level x_mean; document shift across conditions |
| 16 | Code | **StM entropy H_StM**: compute H_StM = −∫ KDE(x) log₂ KDE(x) dx (numerical integration) per condition; compare with condition-level H_emp and H_SDE from InT |
| 17 | Code | **Susceptibility analysis**: condition-level χ_cond = (x̄_c − x̄_ctrl) / Δh_friction (condition comparison); individual χ_behav distribution by condition; identify high-χ participants |
| 18 | Code | **Free energy by condition**: F_behav per participant using E_use, H_emp, β_behav; describe F distribution by condition; identify "locked-in" vs "exploratory" regime |
| 19 | Code | **Four-model convergence**: join StoP + DyS + InT + StM parameters; define convergence criterion: low σ̂ AND is_dys_eligible AND low H_emp AND high β_behav; count and describe convergent participants |
| 20 | Code | **Psychosocial correlates** (exploratory): FoMO, belonging, digital_wellbeing vs β_behav, χ_behav, F_behav (friction-exposed only); flag for multiple comparisons |
| 21 | Code | **Export outputs**: all CSV files, model_run_summary.md |
| 22 | Code | **Figure 1**: β_behav distribution by condition — violin/box (mirrors StoP fig1 structure) |
| 23 | Code | **Figure 2**: Two-state model — p_use and χ_behav by condition |
| 24 | Code | **Figure 3**: Condition-level V(x) energy landscape — three overlaid curves; peaks labeled |
| 25 | Code | **Figure 4**: Four-model comparison — β_behav vs H_emp scatter; colored by is_dys_eligible; size-coded by χ_behav |
| 26 | Markdown | **Interpretation and limits**: 8+ bullet points; must include all DS5 weakness flags (A–G) |
| 27 | Markdown | **Forward connections** — to DS4 (OU-based β estimation), to Step 2 phenotyping (β, χ, F dimensions), to paper gaps |
| 28 | Markdown | **Unification notes** — the four-model behavioral profile; StM completes the StoP↔DyS↔InT triangle into a quadrangle |

---

## 8. Proposed saved outputs

**Output root:** `outputs/model_outputs/statistical_mechanics/`

| File | Description | Rows | Key columns |
|---|---|---|---|
| `participant_stm_parameters.csv` | Per-participant StM-level quantities | 414 (StoP-eligible) | participant_id_canonical, study_condition, mu_hat, sig_hat, beta_behav, T_behav, p_use_approx, E_use, E_nonuse, Z_2state, chi_behav, F_behav, H_StM_participant (approx, noisy), n_days |
| `condition_stm_summary.csv` | Condition-level StM statistics | 3 rows | study_condition, n, mean_beta, mean_T_behav, mean_p_use, mean_chi, mean_F_behav, H_StM_condition (from KDE), V_min_location, V_min_depth |
| `condition_potential.csv` | Condition-level V(x) landscape data | 3 × N_grid rows | study_condition, x_grid, kde_density, V_x, is_minimum |
| `stm_stop_int_dys_comparison.csv` | Four-model cross-model table | 414 | participant_id_canonical, mu_hat, sig_hat, H_emp, H_SDE, H_StM_participant, is_dys_eligible, beta_behav, chi_behav, F_behav, four_model_convergent |
| `psychosocial_stm_correlations.csv` | Pearson r of StM params vs psychosocial scales | — | feature, r_beta, r_chi, r_F_behav, p_value, n |
| `model_run_summary.md` | Run record with FLAG decisions, key results, cross-model summary | — | — |
| `figures/fig1_stm_beta_by_condition.png` | β_behav distribution by condition | — | — |
| `figures/fig2_stm_puse_chi_by_condition.png` | Two-state model: p_use and χ by condition | — | — |
| `figures/fig3_stm_potential_landscape.png` | Condition-level V(x) curves (3 overlaid) | — | — |
| `figures/fig4_stm_four_model_comparison.png` | β_behav vs H_emp scatter; DyS-eligible color; χ size | — | — |

### Column reference: participant_stm_parameters.csv

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Participant identifier (from StoP) |
| `study_condition` | str | RCT condition (control / default / reintervention) |
| `n_days` | int | Days in StoP estimation window (≥7) |
| `mu_hat` | float | Drift estimate — reused from StoP |
| `sig_hat` | float | Diffusion estimate — reused from StoP |
| `beta_behav` | float | Effective behavioral inverse temperature: 2/σ̂² |
| `T_behav` | float | Effective behavioral temperature: σ̂²/2 |
| `p_use_approx` | float | Fraction of days in "high-use" state (X_t > 0.5 proxy); approximated via x_mean |
| `E_use` | float | Behavioral energy of use state: −ln(p_use_approx) |
| `E_nonuse` | float | Behavioral energy of non-use state: −ln(1 − p_use_approx) |
| `Z_2state` | float | Two-state partition function |
| `chi_behav` | float | Behavioral susceptibility: β · p_use · (1 − p_use) |
| `F_behav` | float | Behavioral free energy analog: E_use − (1/β) · H_emp |
| `H_StM_participant` | float | Participant-level H_StM approximation (very noisy — use cautiously) |
| `H_emp` | float | Empirical entropy from InT — joined for reference |
| `is_dys_eligible` | bool | DyS regime flag — joined from DyS |

---

## 9. Data pipeline

### Sources (no new data pipeline beyond behavioral file for Level 2)

| File | Role | Notes |
|---|---|---|
| `outputs/model_outputs/stochastic_processes/participant_parameters.csv` | Primary input — μ̂, σ̂, x_mean; 414 rows | All StM parameters derived from σ̂ |
| `outputs/model_outputs/information_theory/participant_entropy_metrics.csv` | H_emp, H_SDE per participant | Join for cross-model comparison and free energy computation |
| `outputs/model_outputs/dynamical_systems/participant_dynamics_parameters.csv` | is_dys_eligible, x_mean, attractor_boundary | Join for four-model convergence flag |
| `outputs/cleaned/ds5_behavioral_clean.csv` + condition join | Raw daily X_t series for Level 2 (condition-level KDE) | Need to re-derive daily X_t aggregation per condition for KDE; join study_condition from ds5_survey_features.csv |
| `outputs/features/ds5/ds5_survey_features.csv` | Psychosocial correlates (FoMO, belonging, digital_wellbeing) | Join for exploratory psychosocial analysis |

### Pipeline steps

**Level 1 (participant-level, from stored outputs only):**
1. Load `participant_parameters.csv` — 414 rows
2. Load `participant_entropy_metrics.csv` — inner join → 414 rows
3. Load `participant_dynamics_parameters.csv` — inner join → 414 rows
4. Compute `beta_behav = 2 / sig_hat**2`
5. Compute `T_behav = sig_hat**2 / 2`
6. Approximate `p_use_approx = x_mean` (x_mean ≈ p_use for uniform discretization; exact when threshold = mean)
7. Compute `E_use = -np.log(np.clip(p_use_approx, 1e-6, 1-1e-6))`
8. Compute `E_nonuse = -np.log(np.clip(1 - p_use_approx, 1e-6, 1-1e-6))`
9. Compute `Z_2state = np.exp(-beta_behav * E_use) + np.exp(-beta_behav * E_nonuse)`
10. Compute `chi_behav = beta_behav * p_use_approx * (1 - p_use_approx)`
11. Compute `F_behav = E_use - (1/beta_behav) * H_emp` (in bits: divide H_emp by ln(2) for nats if needed)
12. Assign `four_model_convergent`: sig_hat < SIGMA_THRESHOLD AND is_dys_eligible AND H_emp < H_EMP_MEDIAN AND beta_behav > BETA_THRESHOLD

**Level 2 (condition-level V(x), requires behavioral file):**
1. Load `ds5_behavioral_clean.csv`; join study_condition from `ds5_survey_features.csv`
2. Filter: event_outcome_simple in {opened, dismissed, closed}; MIN_DAYS=7 (already applied in StoP)
3. Re-derive daily X_t per participant (same logic as StoP)
4. Pool all X_t values by condition → 3 arrays of ~3,000-4,000 values each
5. KDE per condition (scipy.stats.gaussian_kde, Silverman bandwidth)
6. Evaluate KDE on grid x_grid = np.linspace(0, 1, 200)
7. Compute V̂(x) = -(sigma_bar_c**2 / 2) * np.log(kde_density + EPS) using condition-level mean σ̄_c
8. Find V(x) minimum (= P̂_inf peak): x_min = x_grid[np.argmax(kde_density)]
9. Compute H_StM_condition = -np.sum(kde_density * np.log2(kde_density + EPS)) * dx (numerical integration)

### Sanity checks

- `beta_behav` ordering by condition: control (highest β, lowest T) > reintervention > default
  (σ̂ ordering from StoP: default (0.245) > reintervention (0.200) > control (0.172), so β = 2/σ̂² inverts
  this: control (2/0.172² ≈ 67.7) > reintervention (2/0.200² = 50.0) > default (2/0.245² ≈ 33.3))
  → Higher β (lower temperature) for control — control is more "ordered" in StM language
  → This is consistent: friction (default/reintervention) raises behavioral temperature → more exploration
- `chi_behav` was expected to be highest near p_use ≈ 0.5 — **this check FAILS**: spearmanr(chi_behav, |p_use − 0.5|) = −0.051 while spearmanr(chi_behav, beta_behav) = 0.915. The β factor dominates, so chi_behav is a monotone restatement of 1/σ̂².
- `H_StM_condition` (from KDE) should order consistently with H_SDE and H_emp from InT
- `V_min_location` per condition should approximately match condition-level x_mean from StoP
- `four_model_convergent` flag should overlap substantially with `is_dys_eligible` (both derived from σ̂)

---

## 10. Forward connections from StM

| Connection | Mechanism | Target |
|---|---|---|
| StM → DS4 | OU process has confining potential V(x) = (θ/2)(x−μ)²; then P_inf = N(μ, σ²/2θ) is exact Gaussian; β = 2θ/σ² is rigorous; DS4's 897-day windows make θ estimable | DS4 StM notebook (future) |
| StM → Phenotyping (Step 2) | β_behav (behavioral temperature), χ_behav (susceptibility), F_behav (free energy) are three continuous phenotype dimensions | Notebook 100 |
| StM → Paper §4.1.1 | Add: Boltzmann bridge equation; β_behav mapping; two-state partition function; χ_behav formula; H_StM entropy bridge | Must add before submission |
| StM → Unification (§4.3) | StM completes the four-model framework; the four-model convergence criterion is the first empirical test of multi-model consistency for individual participants | §4.3 integration section |
| StM → DyS (DS4) | For OU process: V_min = μ (OU mean); β = 2θ/σ²; DyS fixed points and StM energy minima coincide exactly | Formal bridge becomes rigorous in DS4 |
| StM → SyD | The "energy landscape" framing in StM parallels the "feedback loops" framing in SyD: high-V states are maintained by strong reinforcing loops; low-V states are stable equilibria | Conceptual bridge to notebook 48 |

---

## 11. Equation gaps to resolve before or during implementation

| Gap | Status | Action |
|---|---|---|
| Boltzmann bridge: P_inf(x) ∝ exp(−2V(x)/σ²) | NOT in paper | **Must add** §4.1.1 or §4.1.3 — the StoP↔StM connection; include caveat about constant-drift approximation |
| Effective behavioral temperature: β_behav = 2/σ̂² | NOT in paper | **Must add** §4.2.1 — explicitly flag as an approximation for constant-drift SDE |
| Potential inversion: V(x) = −(σ̂²/2) log P̂_inf(x) | NOT in paper | **Must add** §4.2.1 — include note about condition-level vs individual-level stability |
| Two-state partition function for behavioral states | NOT in paper | **Must add** §4.2.1 — Z_2 = e^{−βE_use} + e^{−βE_non-use} |
| Behavioral susceptibility: χ = β · p_use · (1 − p_use) | NOT in paper | **Must add** §4.2.1 — most operationally interpretable StM quantity for intervention design |
| H_StM = −∫ P_inf log₂ P_inf dx (StM entropy bridge to InT) | NOT in paper | **Must add** §4.2.1 or §5 — needed for three-way entropy triangulation (H_SDE, H_emp, H_StM) |
| Behavioral free energy: F_behav = E_behav − (1/β) · S_behav | NOT in paper | **Add as conceptual equation** §4.2.1 — motivates E-S tradeoff interpretation |
| Explicit caveat: constant-drift SDE ≠ potential-well SDE | NOT in paper | **Must add** §4.2.1 limitations — critical for scientific accuracy |

---

## 12. StM complexity layers — what is core vs what is optional in Step 1

| Layer | What it computes | Defensibility | Recommended? |
|---|---|---|---|
| β_behav = 2/σ̂² from StoP σ̂ | Effective temperature per participant | High — follows directly from σ̂ | Yes — Level 1 core |
| T_behav = σ̂²/2 | Inverse temperature (behavioral exploration) | High | Yes — Level 1 core |
| Two-state p_use, Z_2, χ_behav | Boltzmann probability of "use" state; susceptibility | Medium — two-state approximation; FLAG 1 caveat | Yes — Level 1 core |
| F_behav = E_use − (1/β) H_emp | Behavioral free energy analog | Medium — H_emp from InT; valid as analog | Yes — Level 1 core |
| Condition-level V(x) via KDE | Energy landscape from pooled data | Medium — stable only at condition level; FLAG B applies | Yes — Level 2 visualization |
| Individual-level V(x) via KDE | Individual energy landscapes | Low — 7-45 points too sparse | Optional — flag as exploratory |
| H_StM from condition KDE | Third entropy estimate | Medium — validates Boltzmann approximation | Yes — cross-model validation |
| Four-model convergence | All four models agreeing on same participants | High — uses already-computed flags | Yes — key unification result |
| Phase transition T_c | Critical temperature estimation | Very low — only 3 conditions | No — defer |
| Ising coupling J | Spin-spin interaction | None available in DS5 | No — conceptual reference only |
| Hysteresis | Path-dependent behavior | None — not in DS5 study design | No — note absence explicitly |

---

## 13. Summary: what this notebook adds to Stage 4 Step 1

| Output | Source | StM contribution |
|---|---|---|
| β_behav, T_behav | New (from StoP σ̂) | First behavioral "temperature" estimate; connects exploration intensity to thermodynamic framing |
| χ_behav (susceptibility) | Not independent | Intended as an intervention-sensitivity analog, but empirically Spearman 0.915 with β_behav (= 2/σ̂²) and 0.051 with p(1−p) — it does not identify participants closest to the tipping point. Do NOT use alongside sig_hat / beta / H_SDE in a clustering feature set without residualising. |
| F_behav (free energy) | New | E-S tradeoff framing — balance between habitual pull and behavioral flexibility |
| Condition-level V(x) | New (KDE from behavioral data) | First energy landscape visualization; shows how friction shifts the behavioral potential |
| H_StM (Boltzmann entropy, condition-level KDE) | New | Third entropy estimate at the CONDITION level; validates Gaussian-Boltzmann approximation alongside H_SDE and H_emp. ⚠ ordering only — H_SDE and H_StM are differential entropies, H_emp is a discrete K=10-bin entropy; their levels differ by ~log₂10 = 3.32 bits by construction and cannot agree in magnitude. ⚠ The participant-level H_StM_participant is H_SDE − 0.5 exactly and is not independent evidence |
| four_model_convergent | New | Closes the StoP↔DyS↔InT triangle into a four-model quadrangle; most rigorous unification claim in Step 1 |

---

## 14. Key StM weakness claims summary (mandatory disclosures in notebook)

The following statements must appear explicitly in the notebook interpretation cell:

1. β_behav = 2/σ̂² is an approximation. It would be exact only for an OU/potential-well SDE. The
   constant-drift SDE used in StoP produces a degenerate potential (linear slope), and the mapping
   to β_behav is an analog, not a rigorous thermodynamic derivation.

2. Individual V(x) estimation from 7-45 daily observations is unreliable. All individual-level
   V(x) visualizations should be labeled "illustrative only." The condition-level V(x) from pooled
   data is more stable but still approximate.

3. Thermodynamic equilibrium is not established. DS5 windows of 7-45 days may not be long enough
   for behavioral state distributions to converge to a stationary distribution.

4. No Ising coupling between participants. DS5 participants are independent. The J=0 limit of
   the Ising model is a single-particle model with external field only.

5. Phase transitions, critical temperature T_c, and hysteresis cannot be demonstrated in DS5.
   These are motivational concepts from the paper that guide interpretation but are not empirically
   testable with the available data structure.

6. Behavioral "energy" is information-theoretic (surprisal = −ln p), not physical energy. The
   Boltzmann analogy is useful for framing but should not be interpreted as making physical claims
   about the cognitive or metabolic costs of smartphone behavior.

---

*This blueprint is the design document for `notebooks/41_ds5_statistical_mechanics.ipynb`.
Do not implement the notebook until the user confirms this blueprint.*
