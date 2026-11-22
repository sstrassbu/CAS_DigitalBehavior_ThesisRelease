# DS5 StoP ↔ InT — Comparison and Unification Note

**Written:** 2026-04-17  
**Covers:** Notebook 43 (StoP — Stochastic Processes) and Notebook 45 (InT — Information Theory)  
**Purpose:** Persistent record of what each model captures, where they overlap, what is genuinely new in InT, and what the bridge implies for later paper unification.

---

## 1. What each model captures

### StoP (Stochastic Processes — Notebook 43)

StoP models the daily behavioral override series X_t as a stochastic differential equation:

    dX_t = μ dt + σ dW_t

The two estimated parameters are:

| Parameter | Meaning | Scale |
|---|---|---|
| μ̂ (drift) | Mean daily directional change in X_t; direction of behavioral tendency | ~0.007; near-zero across all conditions |
| σ̂ (diffusion) | Day-to-day behavioral variability; noise magnitude around the drift | 0.172–0.245 depending on condition |
| σ/\|μ\| ratio | Impulsivity ratio; noise-to-signal ratio | Undefined for 31.2% of participants |

StoP is a **dynamic, trajectory-level description**: it characterizes how each participant's behavior moves over time and how noisy that movement is. The core claim is that X_t can be meaningfully approximated as a Wiener process with drift.

### InT (Information Theory — Notebook 45)

InT characterizes behavioral distributions — not trajectories — in terms of their uncertainty and diversity. Five entropy dimensions were estimated:

| Measure | Object described | Paper status |
|---|---|---|
| H_out | Uncertainty over friction outcomes (opened/dismissed/closed) | Eq. 25 — in paper |
| H_app | Diversity of apps that triggered friction events (Stage 1 feature re-framed) | Eq. 25 — in paper |
| H_hour | Diversity of hours when friction events occur | Eq. 25 — in paper |
| H_emp | Empirical entropy of the daily X_t distribution (K=10 bins) | Eq. 25 — in paper |
| H_SDE | Differential entropy of the stationary distribution implied by σ̂: H = ½ log₂(2πeσ̂²) | **NOT in paper — must add** |

InT is a **static, distributional description**: it characterizes how concentrated or dispersed each participant's behavioral patterns are, without modeling how those patterns evolve over time.

---

## 2. Overlap: what both models cover

The central overlap is through the **state variable X_t** and **σ̂**:

- Both StoP and InT (H_emp, H_SDE) operate on the same behavioral proxy: X_t = n_opened_day / n_events_day.
- H_SDE is a deterministic monotone transformation of σ̂ — it carries no additional empirical information. It is simply a re-expression of StoP's diffusion parameter in information-theoretic units (bits).
- H_emp is the empirical entropy of the discretized X_t distribution — it captures the same underlying behavioral variability as σ̂, but without assuming Gaussian increments.

The StoP → InT bridge is therefore:

    σ̂ (StoP, continuous) → H_SDE (InT bridge, bits)   [deterministic, not independent]
    σ̂ (StoP, increments) → H_emp (InT, binned X_t)     [related, empirically validated: r = 0.650]

Condition ordering is preserved in both:

| Condition | σ̂ (StoP) | H_SDE (bridge) | H_emp (empirical) |
|---|---|---|---|
| control | 0.172 | −0.691 bits | (lower) |
| reintervention | 0.200 | −0.496 bits | (middle) |
| default | 0.245 | −0.118 bits | (higher) |

This ordering is consistent across all three representations.

---

## 3. What the bridge means

### Mathematically

The differential entropy of a Gaussian distribution N(μ, σ²) is:

    H = ½ log₂(2πeσ²)    [Cover & Thomas 2006, Eq. 8.53]

This is a standard result. Applied here: if the daily increments ΔX_n are approximately Gaussian (which the StoP model assumes), then the stationary distribution of X_t has this entropy. H_SDE is therefore the information-theoretic interpretation of σ̂.

Because log₂(σ²) < 0 for σ < 1, H_SDE can be negative — this is expected for differential entropy of narrow distributions (σ̂ < 0.242 for all our conditions, hence all H_SDE values are negative). Negative differential entropy is mathematically valid and means the distribution is more concentrated than a uniform distribution over a unit interval.

### Conceptually

H_SDE answers: *"If this participant's behavioral increments were Gaussian, how much uncertainty (in bits) would be in their behavioral state tomorrow?"*

Lower H_SDE (more negative) = more predictable, more regular behavior.  
Higher H_SDE = less predictable, more variable behavioral day-to-day.

The friction effect visible in StoP σ̂ (friction conditions more variable than control) is therefore directly readable in H_SDE as a difference in behavioral unpredictability.

### What the bridge validates

The Pearson correlation r(H_SDE, H_emp) = 0.650 (n=414) is the key cross-method check:

- H_SDE assumes Gaussian increments (StoP model assumption).
- H_emp makes no parametric assumption — it bins the empirical X_t distribution.
- r = 0.650 indicates **moderate support for the Gaussian assumption** — the parametric and non-parametric entropy measures broadly agree, but there is meaningful variance in H_emp not captured by H_SDE.
- The gap (r < 1.0) suggests that some participants have non-Gaussian behavioral distributions (e.g., bimodal, highly skewed, or boundary-dominated patterns). These are the participants where the StoP Gaussian assumption is weakest.

---

## 4. What is genuinely new in InT (not re-expressions of StoP)

| Measure | Independence from StoP | What it adds |
|---|---|---|
| H_out | Fully independent | Uncertainty over friction outcomes — directly addresses intervention effectiveness; captures how "mixed" a participant's friction responses are; not computable from StoP parameters |
| H_app | Fully independent | App-level behavioral diversity — captures breadth of friction exposure across apps; not in StoP state variable at all |
| H_hour | Fully independent | Temporal diversity — captures whether friction events cluster at particular hours or spread across the day; not in StoP state variable |
| H_emp | Partially new | Shares state variable with StoP but makes no parametric assumption; tests the Gaussian assumption; captures non-Gaussian distributional features |
| H_SDE | Not independent | Deterministic function of σ̂; all empirical content is from StoP; only contribution is translating σ̂ into bits |

**Genuinely new InT signal (not obtainable from StoP):** H_out, H_app, H_hour, and the non-Gaussian component of H_emp.

**Genuine bridge / re-expression:** H_SDE (same information as σ̂ in different units).

---

## 5. Key empirical findings: StoP vs InT

### Condition-level patterns

| Finding | StoP | InT | Interpretation |
|---|---|---|---|
| Friction increases behavioral variability | σ̂: default (0.245) > reintervention (0.200) > control (0.172) | H_SDE mirrors exactly (monotone transform); H_emp broadly consistent | Consistent across both models |
| Drift near-zero across conditions | μ̂ ~0.007 across all conditions; h_c ~0.001 (negligible) | Not captured by entropy (entropy is about spread, not direction) | StoP-only finding |
| Friction increases outcome uncertainty | Not captured by StoP (no outcome distribution) | H_out: default (0.940) > reintervention (0.902) > control (0.691) bits | InT-only finding — ⚠ condition-confounded |
| App diversity differences | Not captured by StoP | H_app available but no strong condition-level pattern noted | InT-only; weak signal |

### Psychosocial correlates (exploratory, friction-exposed only)

| Finding | StoP | InT |
|---|---|---|
| FoMO ~ behavioral variability | σ̂: r=−0.13, p=0.036 | H_SDE: r=−0.13, p=0.038 (same participants, monotone transform — exact replication) |
| FoMO ~ drift | μ̂: r=−0.12, p=0.047 | — |
| Social media wellbeing ~ app diversity | — | H_app: r=+0.10, p=0.044 |
| Social media wellbeing ~ hourly diversity | — | H_hour: r=−0.13, p=0.024 |

**Key note:** The FoMO ~ H_SDE finding is a mathematical replication of FoMO ~ σ̂, not independent evidence. The H_app and H_hour wellbeing associations are genuinely new — not expressible in StoP parameters.

---

## 6. Limitations

### Shared limitations (both models)

1. **Proxy limitation:** Both operate on X_t = n_opened / n_events — behavioral tendency, not urge, self-control, or any latent state
2. **Daily aggregation:** Both collapse within-day sequential structure
3. **Short windows:** Participants with 7–14 days (eligible minimum) produce noisy estimates in both models
4. **Exploratory psychosocial analysis:** 25+ tests, no multiple-comparison correction

### StoP-specific limitations

- Constant-drift assumption misses mean-reversion and non-linear dynamics
- Drift-only friction effect (FLAG 3A) ignores σ response (which is in fact the more informative signal)
- Hard clip boundary [0,1] is not reflecting

### InT-specific limitations

- **H_out is condition-confounded:** control group has structurally fewer dismissed/closed events, inflating apparent H_out differences across conditions
- **H_SDE not in paper:** bridge equation must be added before submission (§4.1.5 or §5.1, Cover & Thomas 2006 citation)
- **K=10 bins for H_emp** is a defensible but arbitrary choice; H_emp is noisy for short windows
- **H_app and H_hour** span all events, not only friction-triggered events (different denominator than X_t)
- **No entropy bias correction** (Miller–Madow, Jackknife) — FLAG 1 and 2

---

## 7. Implications for paper unification

### What the StoP↔InT link contributes

The bridge H_SDE = ½ log₂(2πeσ̂²) is the first explicit cross-model unification in Stage 4. It demonstrates that:

1. The stochastic noise parameter σ̂ and the information-theoretic uncertainty H have a precise mathematical relationship under the Gaussian assumption.
2. The Gaussian assumption is empirically testable via r(H_SDE, H_emp) = 0.650 — and the moderate fit tells us the Gaussian SDE is a reasonable but imperfect first-pass model.
3. Different entropy dimensions (H_out, H_app, H_hour) capture behavioral variability that is orthogonal to the SDE state variable — they enrich the behavioral description without redundancy.

### Suggested paper framing

- In §4.1.3 (StoP): present σ̂ as the primary variability measure; note the InT bridge as a forward connection.
- In §4.1.5 (InT): introduce H_SDE explicitly with the differential entropy formula (currently missing); note it as a unification of §4.1.3 and §4.1.5; use r(H_SDE, H_emp) as an empirical validation of the Gaussian assumption.
- In §5 (integration/unification): the StoP↔InT bridge is the first concrete demonstration that the model families are mathematically connected, not just thematically related.
- In §4.2 (application to DS5): H_out, H_app, H_hour are genuinely independent observables and can be presented as separate behavioral dimensions alongside (μ̂, σ̂).

### Forward connection to DyS and StM

| Model | Connection to StoP↔InT |
|---|---|
| DyS (42) | When σ→0: H_SDE → −∞ (fully deterministic, zero uncertainty). Low-H_emp participants are DyS candidates. The DyS notebook can identify the σ→0 regime empirically. |
| StM (41) | Boltzmann: P_inf(x) ∝ exp(−2V(x)/σ²). Once V(x) is estimated from data, H_StM = −∫ P_inf log₂ P_inf dx gives a third entropy estimate to triangulate against H_SDE and H_emp. |
| Phenotyping (Step 2) | (μ̂, σ̂, H_out, H_app, H_hour, H_emp) form a 6-dimensional behavioral uncertainty profile — a natural input to Step 2 clustering |

---

## 8. Summary table

| Dimension | StoP | InT (direct) | InT (bridge) |
|---|---|---|---|
| Behavioral trajectory shape | μ̂, σ̂ | — | — |
| State variable distributional spread | — | H_emp | H_SDE (= f(σ̂)) |
| Friction outcome uncertainty | — | H_out | — |
| App diversity | — | H_app | — |
| Temporal diversity | — | H_hour | — |
| Cross-model link | σ̂ → H_SDE | H_emp validates H_SDE | r = 0.650 |
| FoMO association | r=−0.12/−0.13 | r=−0.13 (H_SDE only; same data) | — |
| Wellbeing association | — | H_app r=+0.10; H_hour r=−0.13 | — |
