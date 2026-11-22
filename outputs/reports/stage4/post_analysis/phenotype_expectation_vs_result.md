# Phenotype Expectation vs. Phenotype Result

**Written:** 2026-04-20  
**Purpose:** Compare the phenotype distinctions anticipated by the paper and conceptual framework against what the implemented models and Step 2 analyses actually found in DS5

---

## Part 1 — Phenotypes theoretically expected

### What the paper (§4.3) anticipated

The paper's conceptual framework anticipated the following phenotype distinctions as theoretically central:

| Anticipated dimension | Expected operationalization | Model family |
|---|---|---|
| **Friction sensitivity** | Override rate, friction outcome diversity | StoP (x_mean), InT (H_out) |
| **Habitual stability / attractor strength** | Low noise, near-attractor position | DyS (is_dys_eligible), StoP (low σ̂) |
| **Impulsivity / noise dominance** | High σ̂, high σ/|μ| ratio | StoP (sig_hat, sigma_mu_ratio) |
| **Threshold dependence** | Near tipping point, high susceptibility | StM (chi_behav) |
| **Context dependence** | Temporal variability in behavior | InT (H_hour) |
| **Adaptation over repeated exposure** | Directional behavioral drift | StoP (mu_hat) |
| **Override tendency** | Mean override rate, self-loop rate | StoP (x_mean), NeT (rho_self) |
| **Substitution tendency** | App switching after friction | InT (H_app), NeT (H_trans, I_consec) |
| **Network centralization / hub dependence** | Concentration of app use | NeT (HHI_net, rho_self) |
| **Feedback-loop dominance** | Attractor-driven vs noise-driven regime | DyS/StM (is_dys_eligible, F_behav) |

**Implicit expectation:** The paper seems to anticipate that multiple distinct phenotype types would emerge, each characterized by a unique combination of several of these dimensions. The framework implies at minimum 3–5 meaningfully distinct groups (e.g., "friction-sensitive habitual user," "noise-dominated impulsive user," "threshold-near susceptible user").

**Implicit assumption about independence:** The paper treats these dimensions as largely conceptually distinct — as if the empirical feature space would reflect 8–10 real degrees of freedom. The construct mapping table (§4.3) presents them as parallel, non-redundant axes.

---

## Part 2 — Phenotypes actually recovered

### What Step 2 found

After all six phenotyping paths:

**Layer 1 — Network-topological dimension (NeT)**
- Two types: hub-dominated (Profile B, 70%) and distributed (Profile A, 30%)
- Sub-structure: B1 (pure single-app, 63%); B2 (multi-hub anchored, 7%); A1 (moderate, 20%); A2 (highly distributed, 10%)
- Driving features: HHI_net and rho_self only
- Behavior-unrelated (ARI with Layer 2 = 0.020)

**Layer 2 — Behavioral-dynamic dimension (StoP/InT/StM)**
- Three types: C1 (stable, susceptible), C2 (stable, override-locked), C3 (noisy, variable)
- Driving features: sig_hat, H_emp, x_mean only
- Orthogonal to Layer 1
- Condition-dependent (collapsed by default friction condition)

**No independent Layer 3 found:**
- Friction-response diversity (Path B): collinear with x_mean (r=-0.707)
- Dynamic/stochastic (Path D): collapses C1+C2; no new structure beyond Path A

---

## Part 3 — Where expectations and results matched

### Match 1: Network centralization as a real phenotype dimension
- **Expected:** Hub dependence as a meaningful individual-difference dimension
- **Found:** YES — dominates the feature space; Phase 1 k=2 is entirely NeT-driven (ARI=0.990)
- **Match quality:** Strong — the expectation was correct, but the dominance of NeT over other dimensions was not anticipated to be this absolute

### Match 2: Impulsivity / noise dominance as a phenotype axis
- **Expected:** High σ̂ users as a distinct type
- **Found:** YES — C3 (N=200) is the high-noise type; it is the largest cluster in the behavior-only taxonomy
- **Match quality:** Strong — sig_hat is one of the two main behavioral-dynamic axes

### Match 3: Habitual stability
- **Expected:** Low-noise, near-attractor users as a distinct type
- **Found:** YES — C1 and C2 both have low sig_hat; DyS-eligible participants concentrate there
- **Match quality:** Moderate — the paper expected "habitual stability" as a single type; the data found two low-noise types (C1 and C2) that differ on override compliance

### Match 4: Threshold dependence / susceptibility
- **Expected:** Near-tipping-point users as identifiable
- **Found:** YES — chi_behav=56.8 for C1 identifies the near-tipping group, confirmed in Path D and Path B
- **Match quality:** Strong — but counterintuitively, the near-tipping group is the LOW-noise type, not a separate distinct cluster

### Match 5: Substitution tendency
- **Expected:** App-switching diversity as an individual-difference dimension
- **Found:** Partially — H_trans and H_app do contribute to the NeT sub-structure (B1 vs B2; A1 vs A2) but are zero for 70.6% of Profile B participants (zero inter-app transitions)
- **Match quality:** Weak — the substitution tendency is dominated by the network floor effect (most DS5 users stay in one app; there is nothing to substitute into)

---

## Part 4 — Where expectations and results differed

### Difference 1: The number of genuinely independent dimensions

**Expected:** 8–10 independent phenotype axes (one per paper concept)

**Found:** Only ~3 genuinely independent empirical axes:
- NeT concentration (HHI_net ≈ rho_self)
- Behavioral noise (sig_hat ≈ H_emp; r=0.538)
- Override compliance (x_mean ≈ H_out_resid; r=-0.707)

All other features are either monotone transforms (H_SDE, β_behav), near-duplicates (p_use, F_behav, is_dys_eligible), or have near-zero variance in DS5 (mu_hat, H_hour).

**Implication:** The paper's 10-dimension conceptual framework collapses to ~3 empirically independent dimensions in DS5. The apparent richness of the CAS framework is not matched by phenotypic diversity in this dataset. This does not invalidate the framework — it may reflect DS5's design limitations (short windows, highly filtered behavior) rather than a fundamental theoretical issue.

### Difference 2: The dominance of network topology over behavioral dynamics

**Expected:** Both network topology and behavioral dynamics would be important, roughly co-equal phenotype dimensions.

**Found:** Network topology explains 99% of the variance in the Phase 1 (full-feature) clustering. Behavioral features (sig_hat, H_emp, x_mean) contribute virtually nothing to the Phase 1 split. The NeT dimension **dominates** the joint feature space.

**Why this matters:** The paper's phenotype framework treats network centralization as one among many dimensions. In DS5, it is effectively the only dimension in the joint space. Behavioral dynamics are a secondary orthogonal layer that requires active feature exclusion (Path A) to observe.

**Implication for the paper:** The narrative should reflect this empirical finding. The paper may need to reframe: "In DS5, the dominant phenotype axis is structural (network topology), while the behavioral-dynamic dimension is orthogonal but secondary in effect size terms."

### Difference 3: Adaptation over repeated exposure — effectively zero

**Expected:** Directional behavioral drift (μ̂) as a phenotype dimension capturing adaptation to friction.

**Found:** μ̂ ≈ 0 for virtually all participants (mean ~0.007; C1 mean=0.0009). DS5's 6-week window is too short for drift to accumulate. The adaptation dimension anticipated in the paper is unidentifiable in DS5.

**Implication:** The paper's claim about "adaptation over repeated exposure" as a phenotype dimension must be qualified. DS4 (897-day windows) is the correct dataset for testing this. DS5 cannot contribute to this dimension.

### Difference 4: Context dependence (H_hour) — low discriminatory power

**Expected:** Temporal variability as a meaningful phenotype axis (when does the user engage with friction — morning, evening, uniformly?).

**Found:** H_hour has r=-0.510 with sig_hat — partially correlated with the noise axis rather than independent. Its variance is low (std=0.232). Including it in clustering (Path A sensitivity, Path D set D3) changes cluster assignments (ARI=0.718 vs 3-feature) but does not reveal genuinely new phenotype types.

**Implication:** H_hour is a secondary enrichment feature, not a primary phenotype dimension in DS5. It may be more informative in DS4 or DS6 where longer windows capture true circadian patterns.

### Difference 5: Friction sensitivity as a unified phenotype concept

**Expected:** "Friction sensitivity" as a coherent individual-difference dimension identifying "who is most moveable by friction."

**Found:** "Friction sensitivity" maps onto multiple non-equivalent features:
- x_mean (override tendency) — primary signal for Path A/F
- H_out_resid (friction response diversity) — nearly collinear with x_mean (r=-0.707)
- chi_behav (StM susceptibility) — near-tipping participants, paradoxically the low-noise type
- C2 type (override-locked, low-noise) is dominant in the control group — the "high-friction-ignorer" type

There is no single "friction sensitivity" type. Different operationalizations yield different groupings. The paper should not present friction sensitivity as a single recoverable phenotype dimension.

### Difference 6: Phenotype stability — condition-mediated, not trait-like

**Expected:** The paper's phenotype framework implies stable individual traits that persist across contexts.

**Found:** The behavioral types (C1/C2/C3) are condition-mediated. The default friction condition collapses behavioral heterogeneity entirely. The types are observable in control and reintervention but not in default.

**Implication:** The "stable individual phenotype" claim requires qualification. At minimum: "phenotypes as described are observed in this dataset under these conditions; their stability as traits requires longitudinal or multi-context replication (DS4)."

---

## Part 5 — Whether the implemented model pipeline changed the phenotype picture

**Did the pipeline change what phenotypes are visible?**

Yes, substantially:

1. The choice to include NeT features in Phase 1 clustering made network topology the dominant axis. Had only behavioral features been used (Path A), the picture would have been: 3 behavioral types with moderate structure. The Phase 1 global clustering conflates the network layer (which dominates) with the behavioral layer (which is nearly invisible at this scale).

2. The six-path approach was necessary to disentangle what Phase 1 had conflated. Without the separate paths, one would conclude: "DS5 has two phenotypes, driven by whether someone uses one app or many." The paths revealed this is a 2-layer structure where the second layer (behavioral dynamics) is nearly independent of the first.

3. The discovery that the default condition collapses behavioral heterogeneity (Path E) fundamentally changes the interpretation of what Phase 1 found. Phase 1 found condition-independent phenotypes — but that is because Phase 1 used NeT features, which are less condition-sensitive. Behavioral features are highly condition-sensitive.

---

## Part 6 — Are the "phenotypes we assumed" and the "phenotypes we found" meaningfully different?

**Short answer: Yes, in two important ways.**

**Way 1 — Dimensionality reduction:** The paper assumed 8–10 independent phenotype dimensions. The data revealed ~3 empirically independent axes. The phenotype space is much lower-dimensional than the framework implied. This is an important honest conclusion: the richness of the theoretical framework exceeds the discriminating power of the available data.

**Way 2 — The role of conditions:** The paper's framework does not adequately distinguish between phenotypes as stable individual traits (condition-invariant) and phenotypes as condition-mediated behavioral profiles (condition-shaped). The implemented analysis revealed that this distinction is empirically consequential: behavioral types are condition-mediated in DS5. This is a finding the paper needs to engage with.

**Ways they are similar:**
- The two-layer structure (structural × dynamical) corresponds to the paper's distinction between network-topological phenotypes and behavioral-dynamical phenotypes
- The three behavioral types (C1/C2/C3) correspond roughly to the paper's anticipated "habitual/stable," "compliant/locked," and "noisy/variable" types
- The chi_behav finding (C1 = most susceptible despite being most stable) is a theoretically predicted result of the StM model, correctly reproduced

**What this means for the thesis:**

The thesis should not claim to have confirmed all phenotype dimensions anticipated in the paper. It should claim:
- Two independent phenotype layers were identified (network topology and behavioral dynamics)
- These layers correspond to two clusters of paper concepts (NeT ↔ hub dependence/substitution; StoP/StM ↔ impulsivity/stability/susceptibility)
- The anticipated dimensions map onto these layers, but not all are independently observable as separate axes
- The condition-mediation finding is the most practically important result — it qualifies all behavioral phenotype claims

---

*Written 2026-04-20 as part of the DS5 Step 2 synthesis waypoint.*
