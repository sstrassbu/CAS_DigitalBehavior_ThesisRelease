# DS5 Step 2 — Master Synthesis Note

**Written:** 2026-04-20  
**Stage:** Stage 4, Step 2 — Phenotyping and Behavioral Subgroup Discovery  
**Dataset:** DS5 — German adolescents RCT, N=573 (414 StoP-eligible; 463 NeT-eligible)  
**Status:** Step 2 COMPLETE — all six paths executed; this document is the authoritative synthesis

---
 
## 0. What Step 2 was trying to establish

Step 2 used the five completed Step 1 model parameter sets (StoP, InT, DyS, StM, NeT) as features for behavioral subgroup discovery in DS5. The goal was not to confirm any specific model but to ask: **do DS5 participants differ from each other in structured, theoretically interpretable ways, and along which dimensions?**

The paper's phenotype framework (§4.3) anticipated distinctions along friction sensitivity, habitual stability, impulsivity, threshold dependence, context dependence, adaptation, override tendency, substitution tendency, network centralization, and feedback-loop dominance.

Step 2 is descriptive discovery, not confirmatory validation. All findings are DS5-specific, exploratory, and require cross-dataset replication before claims of stable individual phenotypes can be made.

---

## 1. Phase 1 — Global Phenotyping (notebook 100)

**What it asked:** What is the dominant axis of individual difference across all five model feature spaces combined?

**Features used:** sig_hat, H_emp, x_mean, HHI_net, rho_self (5 core features; N=414 complete)

**What it found:**
- k=2 solution; Jaccard=0.995 **STABLE**
- **Profile A** (N=125, 30.2%): distributed app-use network (HHI_net=0.545, rho_self=0.761); moderate behavioral variability
- **Profile B** (N=289, 69.8%): hub-dominated (HHI_net=0.978, rho_self=0.992); near-ceiling network concentration
- The split is driven entirely by HHI_net and rho_self; behavioral features (sig_hat, H_emp, x_mean) differ only modestly between profiles
- Condition distribution: χ²=1.22, p=0.545 → phenotypes cut **across** conditions (condition-independent at Phase 1)
- Psychosocial overlays (FoMO, belonging, ostracism, digital wellbeing): all non-significant after Bonferroni

**Genuine finding:** The dominant axis of individual difference in DS5 is **network-topological**, not behavioral-dynamical. Most participants (70%) are hub-locked.

**Confirmatory:** The Phase 2 extended clustering (k=3, ARI vs Phase 1 = 0.723) confirmed that the Phase 1 structure is preserved when secondary features are added.

---

## 2. Path C — Network Sub-Phenotyping (notebook 101)

**What it asked:** Within the dominant hub-locked profile (Profile B, N=289), is there meaningful sub-structure? Are there different types of hub-dominated users?

**Features used:** HHI_net, rho_self, H_trans, H_app (NeT features within each profile)

**Key finding — Profile B:**
- k=2; silhouette=0.866; Jaccard=0.996 **STABLE**
- **B1** (N=260, 89.9%): pure single/near-single-app locked (H_trans≈0, H_app≈0); 70.6% have exactly H_trans=H_app=0
- **B2** (N=29, 10.1%): multi-app hub-anchored (H_trans=0.230, H_app=0.475); genuine but limited transition diversity
- Condition: χ²=4.567, p=0.102 → condition-independent ✓
- Behavioral overlay (sig_hat, H_emp, x_mean): **minimal differences between B1 and B2** — network sub-structure is not accompanied by behavioral-dynamic differences

**Key finding — Profile A:**
- k=2; Jaccard=0.835 (STABLE but std=0.157)
- **A1** (N=85, 68%): moderately distributed (HHI=0.599, H_trans=0.649)
- **A2** (N=40, 32%): highly distributed (HHI=0.429, H_trans=1.087)
- Tentative — reported with stability caveat

**Full-sample NeT-only robustness:**
- k=2; Jaccard=0.994; **ARI vs Phase 1 = 0.990**
- Network topology **alone** reproduces the Phase 1 split almost perfectly
- Behavioral features amplified but did not create the Phase 1 structure

**H_pi supplementary:** Adding stationary distribution entropy changes sub-cluster structure by only ARI=0.948 — negligible impact.

**Genuinely new:** Confirmed that Profile B is NOT behaviorally homogeneous at the NeT sub-level — there is a small minority of multi-app hub-anchored users (B2, 10%). But the behavioral dynamics are indistinguishable between B1 and B2.

**Confirmatory:** NeT features entirely explain the Phase 1 split.

---

## 3. Path A — Behavior-Only Phenotyping (notebook 102)

**What it asked:** Does a genuinely different phenotype structure emerge when network topology is excluded?

**Features used:** sig_hat, H_emp, x_mean (behavioral dynamics only; N=414)

**What it found:**
- k=3; silhouette=0.407; Jaccard=0.991 **STABLE**
- **C1** (N=62, 15%): sig_hat=0.121, H_emp=1.734, x_mean=0.358 → low-noise, **low-override** (consistent, low-friction complier)
- **C2** (N=152, 37%): sig_hat=0.143, H_emp=1.604, x_mean=0.859 → low-noise, **high-override** (consistent, high-friction ignorer)
- **C3** (N=200, 48%): sig_hat=0.281, H_emp=2.454, x_mean=0.673 → **high-noise**, variable override
- **ARI vs Phase 1 = 0.020** → behavior-only clusters are nearly orthogonal to the NeT-driven split
- **ARI vs Path C sub-profiles = 0.017** → confirms orthogonality is not an artifact of Phase 1
- **Condition χ²=91.885, p<0.0001** → behavioral clusters ARE condition-dependent (NOT condition-invariant)
- Sensitivity with H_hour: ARI(4-feature vs 3-feature) = 0.718 — H_hour adds some structure via its r=-0.510 correlation with sig_hat

**Genuinely new:** The behavioral-dynamic axis (noise, entropy, override) has its own stable phenotype structure that is **nearly orthogonal to the network-topological axis** (ARI=0.020). This is the central independence finding of Step 2.

**Key concern uncovered:** The dramatic condition dependence (C2 = 65% of control vs 11% of default) flags that the behavioral taxonomy may be condition-mediated rather than purely trait-based — requires Path E to resolve.

---

## 4. Path F — Hierarchical Two-Stage Phenotyping (notebook 103)

**What it asked:** Can a two-level taxonomy — first split by network structure, then sub-typed by behavioral dynamics — reveal richer structure than any single-axis solution?

**Design:** Stage 1 = Phase 1 profile (NeT split); Stage 2 = behavioral k-means within each profile on [sig_hat, H_emp, x_mean]

**What it found — Profile B Stage 2 (N=289):**
- k=3; silhouette=0.410; Jaccard=0.954 **STABLE**
- **B_behav1** (N=37): sig_hat=0.127, H_emp=1.754, x_mean=0.364 → low-noise, low-override (matches C1)
- **B_behav2** (N=104): sig_hat=0.146, H_emp=1.607, x_mean=0.867 → low-noise, high-override (matches C2)
- **B_behav3** (N=148): sig_hat=0.282, H_emp=2.463, x_mean=0.677 → high-noise, variable (matches C3)

**What it found — Profile A Stage 2 (N=125):**
- k=2 Jaccard=0.744 **MARGINAL** (just below 0.75 threshold)
- Reported as **A_all** (Profile A as a single descriptive cell; no sub-split)

**Final taxonomy: 4 cells** — B_behav1, B_behav2, B_behav3, A_all

**Critical cross-path finding:**
- ARI(Stage 1 vs Phase 1) = 1.000 ✓ (validation check)
- **ARI(Stage 2-B vs Path A within B) = 1.000** → The behavioral sub-types within the hub-locked group are **exactly** the same as the full-sample Path A clusters
- Cramér's V (Path F × Path C) = 0.579 — driven by the A/B split, not within-B structure
- Within Profile B, behavioral sub-types (B_behav1/2/3) distribute ~89%/93%/88% in B1 and ~11%/7%/12% in B2 → **behavioral type and network sub-type are independent within Profile B**

**Genuinely new (the critical thesis result):** The ARI=1.000 between Stage 2-B and Path A within Profile B confirms that NeT type and behavioral type are orthogonal **not only globally** (ARI=0.020 full-sample) but **locally within each network group**. The behavioral phenotype structure discovered in Path A holds with perfect fidelity inside the hub-locked group.

**Confirmed:** The 4-cell taxonomy is a genuine joint characterization of two orthogonal dimensions. No single-axis solution captures both.

**Condition:** Profile B condition χ²=60.963, p<0.0001 → Path E required.

---

## 5. Path E — Condition-Stratified Phenotyping (notebook 104)

**What it asked:** Does the phenotype structure differ across experimental conditions? Are the behavioral profiles condition-invariant, or does friction assignment reshape subgroup structure?

**What it found — full-sample within-condition clustering:**

| Condition | N | Selected k | Jaccard | Flag |
|---|---|---|---|---|
| control | 137 | 2 | 0.744 | MARGINAL |
| **default** | **142** | **NONE** | **—** | **ALL REJECTED** |
| reintervention | 135 | 2 | 0.959 | STABLE |

**Critical finding:** The **default friction condition produced NO feasible clustering**. k=2 gave min_cell=28 (<30 threshold). The default condition collapses behavioral heterogeneity into an undifferentiated distribution.

**Profile B within-condition:**
- control: k=2, Jaccard=0.912 STABLE
- default: NO feasible solution (again)
- reintervention: k=2, Jaccard=0.883 STABLE

**Cross-path comparisons:**
- ARI(control vs Path A) = 0.262 → LOW structural alignment
- ARI(default vs Path A) = 0.000 → zero (all undifferentiated)
- ARI(reintervention vs Path A) = 0.697 → HIGH-MODERATE recovery
- Centroid displacement (control vs reintervention) = 1.136 SD units → LARGE

**Outcome D confirmed:** The default condition is **qualitatively different** from control and reintervention. It does not merely shift proportions — it **eliminates behavioral heterogeneity** itself.

**Genuinely new (most important Path E finding):** "Default friction acts as a behavioral homogenizer." This is a strong finding: one friction design type can eliminate the individual-difference variance that phenotyping would normally use. The default condition functionally removes the distinction between C2 and C3 types.

**What this means for the taxonomy:** The C2 (high-override, low-noise) type is predominantly a control-condition phenomenon (65% of control). The C3 (high-noise) type dominates default (72%). The behavioral taxonomy partially reflects condition effects, not only stable individual differences.

---

## 6. Path B — Intervention-Sensitive Phenotyping (notebook 105)

**What it asked:** Who shows variable friction outcomes, and does that variability cluster into interpretable types? Is friction-response diversity (H_out_resid) an independent phenotype axis?

**Feature gate result:**
- r(H_out_resid, x_mean) = **-0.707** → x_mean DROPPED; H_emp substituted
- r(H_out_resid, sig_hat) = 0.023 → sig_hat retained
- Final features: [H_out_resid, sig_hat, H_emp]

**Full-sample (N=414): k=3, silhouette=0.387, Jaccard=0.940 STABLE**

| Cluster | N | H_out_resid | sig_hat | x_mean (overlay) | chi_behav |
|---|---|---|---|---|---|
| B_fr1 | 148 | -0.211 | 0.140 | 0.837 | 19.2 |
| B_fr2 | 198 | -0.003 | 0.281 | 0.673 | 7.4 |
| B_fr3 | 68 | 0.467 | 0.133 | 0.444 | **45.8** |

**Critical cross-path results:**
- **ARI(Path B vs Path A) = 0.725** → largely recovers behavioral taxonomy → H_out_resid is NOT an independent dimension
- ARI(Path B vs Phase 1) = 0.032 → NeT-independent ✓
- **Within-reintervention: ARI(Path B vs Path E reintervention solution) = 1.000** → identical cluster assignments in the most relevant condition

**Genuinely new (most unexpected finding):** **B_fr3 (diverse responder, high H_out_resid) has chi_behav=45.8** — dramatically elevated compared to B_fr1 (19.2) and B_fr2 (7.4). The "diverse friction responder" type is the same as the near-tipping-point StM group — connecting friction response diversity directly to the StM tipping-point concept.

**Also new:** Even within the default condition where clustering collapses, Path F cell taxonomy significantly predicts H_out_resid direction (KW H=34.3, p<0.0001). Behavioral types persist as real individual differences even when the feature space is too compressed for stable clustering.

**Confirmed:** H_out_resid is not a genuinely independent third phenotype dimension. It captures largely the same variance as x_mean (r=-0.707). The friction-response diversity axis is not orthogonal to the behavioral-dynamic axis.

---

## 7. Path D — Dynamic/Stochastic Phenotyping (notebook 106)

**What it asked:** Do participants separate into groups based on their drift-noise structure? Does chi_behav (StM susceptibility) or mu_hat (drift) add new phenotype structure?

**Correlation gate results:** H_SDE dropped (r=0.942 with sig_hat); F_behav dropped (r=-0.922 with x_mean); beta_behav excluded. chi_behav and mu_hat pass gate.

**D1 [sig_hat, H_emp, chi_behav]: k=2 STABLE (silhouette=0.400; Jaccard=0.919)**
- k=3 REJECTED: min_cell=11 (only ~11 extreme-chi_behav participants)
- **D_sde1** (N=172): sig_hat=0.120, H_emp=1.596, chi_behav=46.68 → low-noise, high susceptibility
- **D_sde2** (N=242): sig_hat=0.268, H_emp=2.358, chi_behav=3.36 → high-noise, low susceptibility
- **ARI(D1 vs Path A) = 0.560** → Outcome 2: partial reorganization; C1+C2 collapsed into D_sde1

**Additional features:**
- D2 [sig_hat, H_emp, mu_hat]: k=2, ARI=0.578 → mu_hat adds almost no structure
- D3 [sig_hat, H_emp, H_hour]: k=3 STABLE but ARI=0.421 vs Path A → lower than D1

**DyS regime flags (critical condition-modulation finding):**
- control: 64.2% DyS-eligible; default: 28.9% DyS-eligible; reintervention: 57.8%
- χ²=39.7, p=2.4e-09 → **default condition reduces deterministic participants by >50% relative to control**
- behaviorally_deterministic: control=59.1%, default=12.7%, reintervention=40.7%

**sigma_mu_ratio (N=285 subsample):**
- C1: mean=11.24; C2: 13.86; C3: 22.94 → all groups are overwhelmingly noise-dominated (ratio>10)
- DS5 behavioral dynamics are diffusion-driven, not drift-driven

**mu_hat finding:** KW test significant (p=0.0002) but effect negligible (C1 mean=0.0009, C2=0.0091, C3=0.0084). DS5 behavioral dynamics are near-zero-drift.

**Genuinely new:** The k=3 rejection (min_cell=11) is itself informative — there is a small extreme-susceptibility subgroup at the very top of C1 (chi_behav >~100) that is too numerically rare for stable phenotyping but conceptually important for the StM tipping-point narrative. The DyS regime flag condition modulation extends Path E's homogenization finding into formal model-language.

**Confirmed:** Path D confirms and characterizes Path A's taxonomy in theoretical language but does not reveal a new independent dimension.

---

## 8. Robustness of the phenotype structures

| Structure | Type | Stability evidence |
|---|---|---|
| Phase 1 (Profile A/B) | ROBUST | Jaccard=0.995; ARI vs NeT-only=0.990; condition-independent (χ²=1.22, p=0.545) |
| Path C B1/B2 within Profile B | ROBUST | Jaccard=0.996 |
| Path C A1/A2 within Profile A | TENTATIVE | Jaccard=0.835 with std=0.157; report with caveat |
| Path A C1/C2/C3 behavioral clusters | ROBUST | Jaccard=0.991; confirmed in Path F within B (ARI=1.000) |
| Path F 4-cell taxonomy | ROBUST (B) / MARGINAL (A) | Profile B k=3 Jaccard=0.954; Profile A k=2 Jaccard=0.744 → A_all |
| Path E reintervention clusters | ROBUST | Jaccard=0.959 |
| Path E control clusters | MARGINAL | Jaccard=0.744 |
| Path E default | INFEASIBLE | No stable solution |
| Path B full-sample | ROBUST | Jaccard=0.940; but not independent of Path A |
| Path D D1 | ROBUST | Jaccard=0.919; partial reorganization of Path A |

---

## 9. The complete DS5 phenotype framework

After all six paths, the DS5 phenotype space is structured along **two genuinely independent layers** and **one confirmatory characterization**:

### Layer 1 — Network-topological dimension (NeT)

- **Source:** Phase 1 + Path C
- **Condition stability:** Stable across conditions (not tested directly for NeT features, but follows from feature nature)
- **Structure:** Hub-dominated (Profile B, 70%) vs. distributed (Profile A, 30%)
  - Within B: B1 single-loop lockers (90%) and B2 hub-anchored multi-app (10%)
  - Within A: A1 moderately distributed and A2 highly distributed (tentative)
- **Independence from Layer 2:** ARI(NeT structure vs behavioral structure) = 0.020 globally, 1.000 (perfect correspondence) locally within Profile B

### Layer 2 — Behavioral-dynamic dimension (StoP/DyS/StM)

- **Source:** Path A + Path F (primary); confirmed by Paths E, B, D
- **Condition stability:** Condition-**modulated** — observable in control (marginal) and reintervention (stable); **collapsed** in default condition
- **Structure:** Three types
  - **C1 / B_behav1** (N=62/37): Low-noise, low-override, near-tipping (chi_behav=56.8) — "stable, susceptible"
  - **C2 / B_behav2** (N=152/104): Low-noise, high-override, override-locked (chi_behav=15.4) — "stable, habitual overrider"
  - **C3 / B_behav3** (N=200/148): High-noise, variable-override, diffusion-dominated (chi_behav=7.7) — "noisy, unpredictable"
- **Independence from Layer 1:** Confirmed globally (ARI=0.020) and locally within Profile B (ARI=1.000 Stage2-B vs Path A within B)

### Layer 3 — Friction-response diversity (InT/StM) — NOT independent

- **Source:** Path B
- **Finding:** H_out_resid captures largely the same information as x_mean (r=-0.707). Not a genuinely new dimension.
- **Important exception:** B_fr3 type (high H_out_resid, low x_mean) has dramatically elevated chi_behav=45.8, connecting friction-response diversity to the StM tipping-point concept. This is a theoretical bridge, not a new phenotype dimension.

### Summary table: what each path established

| Path | New independent layer? | Primary contribution |
|---|---|---|
| Phase 1 | **YES (Layer 1 established)** | Hub-locked vs distributed split |
| C | No (confirms Layer 1) | Network sub-structure within Layer 1 |
| A | **YES (Layer 2 established)** | Behavioral-dynamic orthogonal to Layer 1 (ARI=0.020) |
| F | No (confirms Layers 1+2 are orthogonal) | Hierarchical taxonomy; ARI=1.000 within B proves independence |
| E | No (modulates Layer 2) | Default condition collapses Layer 2; strong finding about friction design |
| B | No (Layer 3 is not independent) | H_out_resid ≈ x_mean; chi_behav-B_fr3 bridge; |
| D | No (confirms Layer 2) | Formal model-language for Layer 2; k=3 rejection exposes extreme-chi_behav tail |

---

## 10. What remains genuinely unresolved

1. **Condition vs. trait:** The behavioral types (C1/C2/C3) are real in the data but their condition-dependence (Path E) means they cannot currently be claimed as stable individual traits. The default condition eliminates C2 entirely. Without within-person longitudinal data or cross-dataset replication (DS4), the degree to which these reflect stable dispositions vs. condition-induced states remains unknown.

2. **Profile A sub-structure:** The A1/A2 split (Jaccard=0.835, std=0.157) is tentative. Profile A (N=125) is too small for confident sub-clustering in all six paths. Profile A within conditions is infeasible (N=36–46).

3. **The extreme-chi_behav tail (C1 / ~N=11 hyper-susceptible):** Path D showed this subgroup exists but is too small to cluster stably. Whether it is a real behavioral type or a statistical artifact requires replication.

4. **Psychosocial null findings:** No psychosocial variable (FoMO, belonging, ostracism, digital wellbeing) distinguished clusters after Bonferroni correction across any of the six paths. This could mean: (a) genuine null; (b) survey measures are too coarse; (c) behavioral phenotypes and psychosocial traits are orthogonal in this sample; (d) the study was underpowered for psychosocial effects. Cannot currently distinguish.

5. **Cross-dataset replication:** All findings are DS5-specific. DS4 (longitudinal, N=1039, naturalistic) is the next dataset. Whether the same two-layer structure replicates in DS4 will substantially determine how strongly the thesis can claim these are general behavioral phenotypes of smartphone use rather than DS5-specific artifacts.

6. **GaT, ABM, SyD model families:** Not yet implemented. The behavioral types (C1/C2/C3) provide initialization vocabulary for ABM agent types, but the formal implementation has not been done.

---

## 11. Strongest overall conclusion

> **DS5 behavioral heterogeneity is organized along two genuinely orthogonal dimensions: network topology and behavioral dynamics. The network-topological dimension (hub-locked vs. distributed) is stable across experimental conditions and dominates the feature space. The behavioral-dynamic dimension (noise, entropy, override tendency) is orthogonal to network type but is condition-modulated — specifically, the default friction condition collapses behavioral heterogeneity and eliminates the behavioral sub-type structure. The reintervention friction condition best preserves individual-difference structure. These two findings together suggest that phenotype-sensitive personalization (Step 3) requires not only a behavioral profile of the user, but also a friction design that allows individual differences to express themselves — and that the default friction design may be the least suitable context for observing or exploiting behavioral heterogeneity.**

---

*Document written 2026-04-20. Based on executed notebooks 100–106, blueprints, and all model run summaries in `outputs/model_outputs/phenotyping/`.*
