# DS5 Step 2 Path F — Hierarchical Two-Stage Phenotype Blueprint

**Notebook:** `103_ds5_hierarchical_phenotype.ipynb`
**Written:** 2026-04-19
**Stage:** Stage 4, Step 2 — Path F (third of six paths)
**Depends on:**
- `outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv` — Phase 1 labels (Stage 1 split)
- `outputs/model_outputs/phenotyping/ds5_phenotype_feature_matrix.csv` — behavioral features for Stage 2
- `outputs/model_outputs/phenotyping/ds5_net_subcluster_assignments.csv` — Path C sub-labels (post-hoc comparison)
- `outputs/model_outputs/phenotyping/ds5_behav_only_cluster_assignments.csv` — Path A labels (post-hoc comparison)

---

## 0. Why this notebook comes third

Path C established that the Phase 1 k=2 network split is entirely NeT-driven (ARI vs.
full-sample NeT-only = 0.990). Within each profile, behavioral features (sig_hat, H_emp,
x_mean) were near-identical across sub-clusters. Network topology and behavioral dynamics
did not co-vary.

Path A established that behavioral dynamics (sig_hat, H_emp, x_mean) have their own
genuine phenotype structure (k=3, silhouette=0.407, Jaccard=0.991). This structure is
almost entirely orthogonal to the NeT-driven Phase 1 split (ARI = 0.020).

The near-zero ARI between Path A and Phase 1 is the critical result that makes Path F
theoretically essential, not optional. It means:

1. A participant's network structure tells you almost nothing about their behavioral
   dynamics (noise, entropy, compliance).
2. A participant's behavioral dynamics tell you almost nothing about their network type.
3. Both axes are independently real and independently contribute information.
4. No single flat clustering — whether NeT-only (Path C) or behavior-only (Path A) —
   captures the full heterogeneity space. Only a joint characterization does.

Path F constructs that joint characterization hierarchically: split first by the dominant
axis (network structure), then sub-type by the orthogonal axis (behavioral dynamics)
within each group.

---

## 1. Theoretical motivation

The two-level hierarchy maps directly onto the paper's theoretical distinction between:

- **Network-topological phenotype dimension** (NeT model family): How a participant
  structurally organizes their app use — hub-dominated (single/few apps) vs. distributed.
  This is a relatively stable structural property that shapes which apps compete for
  attention and how network centralization reinforces habit loops.

- **Behavioral-dynamic phenotype dimension** (StoP, InT, StM model families): How a
  participant *responds* within their structural setting — how noisy their process is
  (sig_hat), how diverse their responses to friction are (H_emp), and how persistently
  they override friction (x_mean). These are within-person dynamic properties that
  describe the attractor landscape, not the network topology.

A participant who is hub-locked AND high-noise AND high-override is categorically
different from a participant who is hub-locked AND low-noise AND low-override — even
though both share the same Phase 1 profile. Path F names and characterizes these
distinctions.

This hierarchy has direct theoretical interpretability:
- Stage 1 (NeT type) characterizes the *structural context* of intervention exposure.
- Stage 2 (behavioral type) characterizes the *dynamic response* within that context.

Together they define the richest single phenotype description available from DS5's
feature space.

---

## 2. Hierarchy design: the evaluated options

### Option 1 — Phase 1 profile as Stage 1 (RECOMMENDED)

Stage 1 split: Phase 1 `profile_p1` assignments (Profile A vs. Profile B)
Stage 2: Behavioral k-means within each profile on [sig_hat, H_emp, x_mean]

**Rationale for choosing this:**
- Phase 1 labels are fully validated (Jaccard=0.995; ARI vs. NeT-only full-sample=0.990).
  Using them requires no re-run and no new threshold decision.
- Profile A and Profile B are the established reference groups in all prior work; using
  them as Stage 1 nodes ensures that Path F's taxonomy builds directly on Phase 1 as
  the foundation, not as an alternative.
- ARI(Phase 1 vs. cluster_net_only) = 0.990, so using `profile_p1` vs. `cluster_net_only`
  as Stage 1 is essentially equivalent. Phase 1 is the established reference.

### Option 2 — Path C network sub-clusters as Stage 1 nodes (NOT RECOMMENDED)

Stage 1 split: Path C sub-cluster labels (B1, B2, A1, A2) as the four first-level nodes
Stage 2: Behavioral sub-clustering within each node

**Why this is rejected:**
- B2 (N=29) is below the minimum cluster size threshold (N≥30). A three-level Stage 2
  sub-clustering within B2 is not feasible and would require reporting N<30 cells.
- A2 (N=40) is borderline; Stage 2 within A2 risks producing cells of N<20.
- The tree becomes structurally imbalanced: B1 (N=260) can support Stage 2; B2 cannot;
  A1 (N=85) can support Stage 2 cautiously; A2 cannot.
- A balanced, interpretable taxonomy requires Stage 1 nodes large enough to support
  meaningful Stage 2 sub-clustering. Only the two Phase 1 groups satisfy this.
- **Path C's network sub-structure (B1/B2, A1/A2) is incorporated as a post-hoc
  overlay, not as a structural node.** See Section 7 (cross-path comparisons).

### Option 3 — Hybrid: apply Path C split to Profile B only (NOT RECOMMENDED)

Stage 1: Phase 1 profile (A/B)
Stage 1b (only for B): Path C B1/B2 split within Profile B
Stage 2: Behavioral clustering within B1 only (N=260); B2 descriptive only

**Why this is rejected:**
- Introduces an asymmetric three-level tree for one branch only (Profile B).
- Profile B Stage 2 is already asking: "within hub-locked participants, what behavioral
  types exist?" That question does not require B1/B2 as an intermediate node; it runs
  on all 289 Profile B participants. Adding the B1/B2 intermediate step reduces the
  Stage 2 analysis to N=260 and loses B2 entirely.
- Path C already answered the network sub-structure question within Profile B. Path F's
  contribution is behavioral sub-typing, which is cleanest when done on Profile B as a whole.

---

## 3. Proposed hierarchy

```
ALL N=414 (StoP-eligible, complete behavioral features)
│
├── STAGE 1: Phase 1 NeT-driven split (profile_p1)
│
├── Profile B — Hub-dominated (N=289, 69.8%)
│   HHI_net median≈1.0, rho_self median≈1.0
│   H_trans median≈0.01 (near-zero)
│   │
│   └── STAGE 2: Behavioral k-means on [sig_hat, H_emp, x_mean]
│       within-group StandardScaler; k=2 or k=3 (bootstrap-selected)
│       │
│       ├── B_behav1  (N=?)  — one behavioral sub-type within hub-locked context
│       ├── B_behav2  (N=?)  — second behavioral sub-type
│       └── B_behav3  (N=?)  — optional third sub-type if k=3 is stable
│
└── Profile A — Distributed-network (N=125, 30.2%)
    HHI_net median≈0.58, rho_self median≈0.88
    H_trans median≈0.65
    │
    └── STAGE 2: Behavioral k-means on [sig_hat, H_emp, x_mean]
        within-group StandardScaler; k=2 (k=3 likely infeasible at N=125)
        Bootstrap Jaccard required; if Jaccard < 0.75, report descriptive only
        │
        ├── A_behav1  (N=?)  — one behavioral sub-type within distributed-network context
        └── A_behav2  (N=?)  — second behavioral sub-type (if stable)
```

**Final combined labels:** B_behav1, B_behav2 [, B_behav3], A_behav1, A_behav2 [or A_all]
**Target final cell count:** 4 cells (2+2) as primary outcome; 5 cells (3+2) as secondary
outcome if k=3 within Profile B is stable.

---

## 4. Input files

| File | Used for |
|---|---|
| `outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv` | Phase 1 `profile_p1` — Stage 1 split |
| `outputs/model_outputs/phenotyping/ds5_phenotype_feature_matrix.csv` | sig_hat, H_emp, x_mean, H_hour, mu_hat, sigma_mu_ratio — Stage 2 clustering + overlay |
| `outputs/model_outputs/phenotyping/ds5_net_subcluster_assignments.csv` | Path C sub-labels (subprofile_B, subprofile_A, cluster_net_only) — post-hoc comparison |
| `outputs/model_outputs/phenotyping/ds5_behav_only_cluster_assignments.csv` | Path A cluster_behav labels — post-hoc comparison |
| `outputs/model_outputs/phenotyping/ds5_psychosocial_overlays.csv` | Psychosocial scales — post-hoc overlay |

---

## 5. Feature specification

### 5.1 Stage 1: network-structural split (no new clustering)

Stage 1 does NOT run a new clustering. It uses `profile_p1` from the Phase 1 output
directly as the first-level partition. This is the established, validated NeT-driven split.

No new NeT features are used as clustering inputs at Stage 1.

NeT features (HHI_net, rho_self, H_trans, H_app) appear as **Stage 1 descriptive
characterization** — they describe the profiles, not produce them.

### 5.2 Stage 2: behavioral clustering features (core set)

| Feature | Role | Notes |
|---|---|---|
| `sig_hat` | PRIMARY | OU noise; no NaN; N complete within each profile |
| `H_emp` | PRIMARY | Behavioral entropy; no NaN; N complete |
| `x_mean` | PRIMARY | Mean override rate; no NaN; N complete |

Same core 3-feature set as Path A. This is deliberate — it allows direct comparison
between within-profile Stage 2 clustering and the full-sample Path A result.

### 5.3 Secondary / sensitivity features (not in clustering)

| Feature | Role | Notes |
|---|---|---|
| `H_hour` | SENSITIVITY | r(H_hour, sig_hat)=-0.510; same reason as Path A — sensitivity run only |
| `mu_hat` | OVERLAY | Near-zero for 56.5% of DS5; not discriminative |
| `sigma_mu_ratio` | OVERLAY | 31.2% NaN; overlay on available subset |

### 5.4 Post-hoc overlay features (NOT in clustering)

After Stage 2 clustering:
- All NeT features (HHI_net, rho_self, H_trans, H_app) — do cells differ on network features?
- `study_condition` — χ² test within each profile (condition independence check)
- Psychosocial scales (5 scales, Kruskal-Wallis with Bonferroni)
- `H_hour` — temporal entropy overlay (if not used in sensitivity run)
- Path A `cluster_behav` labels — ARI comparison
- Path C `subprofile_B` / `subprofile_A` labels — ARI comparison

**Features to EXCLUDE from Stage 2 clustering entirely:**
- All NeT features (the entire point of Stage 2 is behavioral sub-typing independently
  of network structure, which was already captured at Stage 1)
- `H_out` raw (condition-confounded)
- Redundant transforms (H_SDE, beta_behav, chi_behav, F_behav, four_model_convergent)
- `sigma_mu_ratio` (31.2% NaN)
- `mu_hat` (56.5% near-zero)

### 5.5 Scaling design

**Critical decision: within-group scaler (recommended) vs. full-sample scaler**

Path F Stage 2 uses a **within-group StandardScaler** (fit separately on Profile B
participants, then separately on Profile A participants). This is the principled choice
because:
- Stage 2 is asking: "what structure exists within this NeT-type group?" — a within-group
  question that should use within-group standardization.
- Between-profile mean differences in behavioral features (even if small given ARI=0.020)
  would be amplified into the within-profile cluster structure if a full-sample scaler is used.
- Within-group scaling ensures the k-means distance metric reflects within-group variation,
  not cross-group contamination.

**Sensitivity check:** Also run Stage 2 with full-sample scaler (the same scaler from
Path A). Report ARI between within-group-scaled solution and full-sample-scaled solution
within each profile. If ARI is high, scaling choice doesn't matter; if low, document
why within-group scaling is preferred.

**For cross-profile profile comparison and figure overlays:** Report all feature values
in raw (unscaled) units. Within-group scaling is only for clustering; profiles are
described in raw units.

---

## 6. Analysis population and sample-size safeguards

### 6.1 Population

| Group | N | Eligible for Stage 2? |
|---|---|---|
| Profile B (full) | 289 | YES — k=2 or k=3 |
| Profile A (full) | 125 | YES — k=2 only; k=3 requires caution |
| B2 (sub-cluster from Path C) | 29 | NO — descriptive only; N < 30 |
| A2 (sub-cluster from Path C) | 40 | NO — Stage 2 sub-clustering not attempted |

Stage 2 is run on **Profile B (N=289) as a group** and **Profile A (N=125) as a group**.
Path C's sub-cluster labels (B1/B2, A1/A2) are used only for post-hoc cross-tabulation.

### 6.2 Minimum cell size enforcement

**Rule:** No Stage 2 cluster is reported as a phenotype cell if N < 30.

**Profile B (N=289):**
- k=2: cells expected N≈100–189 each — well above threshold for both k=2 splits.
- k=3: cells expected N≈50–140 range. If any cell falls below N=30, k=3 is rejected
  and k=2 is the reported solution.
- k=4: likely to produce at least one underpopulated cell in a N=289 group; run for
  diagnostics but do not report as a phenotype solution.

**Profile A (N=125):**
- k=2: cells expected N≈50–75 each — above threshold.
- k=3: at least one cell likely below N=30 given the Path A result (the "C1-like"
  low-override group was only N=62 out of 414, approximately 15% of the sample; within
  Profile A that would project to N≈19). Do NOT report k=3 within Profile A.
- **If Profile A k=2 Jaccard < 0.75:** Do not force clusters. Report Profile A as
  descriptively profiled only (no sub-type split). The Stage 2 cells would then be
  B_behav1, B_behav2, A_all — 3 cells total.

**Enforcement logic:**
```python
MIN_CLUSTER = 30
for k in K_RANGE:
    sizes = pd.Series(labels).value_counts()
    if sizes.min() < MIN_CLUSTER:
        # skip this k
```

### 6.3 Expected defensible final cell counts

| Scenario | Final cells | Condition |
|---|---|---|
| Primary (expected) | **4 cells** | Profile B k=2 (stable) + Profile A k=2 (stable) |
| Secondary (if B yields k=3) | **5 cells** | Profile B k=3 (stable, all N≥30) + Profile A k=2 (stable) |
| Conservative (if A is unstable) | **3 cells** | Profile B k=2 (stable) + Profile A descriptive only |
| Fallback | **2 cells** | Both Stage 2 splits are unstable; report Stage 1 only = Phase 1 replication |

The 4-cell primary outcome corresponds to a clean 2×2 taxonomy (NeT type × behavioral
sub-type) and is the most interpretable result for the thesis phenotype chapter.

---

## 7. Analysis plan

### Step 1 — Descriptive: within-profile behavioral feature inspection

Before clustering, for each of Profile B and Profile A separately:
- Histograms of sig_hat, H_emp, x_mean within the group (4-panel; overlay full-sample
  Path A distribution in light grey as reference)
- Pairwise scatter plots [sig_hat vs. H_emp, sig_hat vs. x_mean, H_emp vs. x_mean] with
  Path A cluster_behav overlay (color by C1/C2/C3) — do the Path A clusters land in
  distinct regions of the within-profile scatter?
- PCA within each profile: how many components explain ≥80% of variance? If PC1 > 85%,
  Stage 2 is effectively 1-dimensional; document this.
- Within-profile correlation matrix (sig_hat, H_emp, x_mean, H_hour)

**Decision gate:** If sig_hat, H_emp, x_mean are all approximately unimodal within a
profile and have low variance (std < 0.05 for all three), document "Stage 2 within
this profile has insufficient heterogeneity" and skip clustering for that branch.

### Step 2 — Feature scaling

- Fit StandardScaler on Profile B participants only → transform Profile B's [sig_hat, H_emp, x_mean]
- Fit a separate StandardScaler on Profile A participants only → transform Profile A's features
- Store both scalers
- Sensitivity: also transform using full-sample scaler from Path A (if preserved; otherwise
  re-fit on N=414)

### Step 3 — Stage 2 cluster selection within Profile B

For k in [2, 3, 4]:
- K-means (k-means++ init, n_init=10, random_state=42)
- Compute: silhouette, Calinski-Harabasz, Davies-Bouldin, min cell size
- Enforce N≥30 per cell; reject k if violated

For top candidate k (highest silhouette among valid k):
- Bootstrap Jaccard stability (100 bootstraps, 80% sample, random_state=42)
- Threshold: Jaccard ≥ 0.75 for STABLE; ≥ 0.60 for MARGINAL; < 0.60 for UNSTABLE

Report the selected k and stability classification.

### Step 4 — Stage 2 cluster selection within Profile A

Same procedure as Step 3, but K_RANGE = [2, 3] only (k=4 not attempted given N=125).
Apply additional rule: if k=3 produces any cell N<30, reject k=3 regardless of silhouette.

### Step 5 — Assign combined cell labels

After Stage 2 k-selection for each profile:
- Order within-B clusters by sig_hat ascending: B_behav1 (lowest), B_behav2, [B_behav3]
- Order within-A clusters by sig_hat ascending: A_behav1 (lowest), A_behav2
- Combine into a single `cell_f` column on all N=414 participants

Label assignment logic:
```python
df['cell_f'] = None
# For Profile B participants:
for bk, bname in zip(sorted_B_labels, ['B_behav1', 'B_behav2', ...]):
    mask = (df['profile_p1'] == 'Profile B') & (df['stage2_label'] == bk)
    df.loc[mask, 'cell_f'] = bname
# For Profile A participants:
for ak, aname in zip(sorted_A_labels, ['A_behav1', 'A_behav2']):
    mask = (df['profile_p1'] == 'Profile A') & (df['stage2_label'] == ak)
    df.loc[mask, 'cell_f'] = aname
```

### Step 6 — Cell profiles: what each cell looks like

For each cell:
- Mean and median of behavioral features (sig_hat, H_emp, x_mean, H_hour) — in raw units
- Mean and median of NeT overlay features (HHI_net, rho_self, H_trans, H_app)
- Condition distribution χ² within each profile group (not full-sample χ², because
  Stage 2 is within-profile; test: do cells within Profile B differ on condition?)
- Psychosocial Kruskal-Wallis within each profile (Bonferroni correction; 5 scales)
- mu_hat overlay where not NaN

**Important:** The condition χ² here is within-profile. Path A found a full-sample
condition χ²=91.885, p<0.0001, meaning that behavioral clusters are condition-dependent
when measured across the full sample. Within each profile, the condition distribution
may or may not be similarly confounded. Reporting this is required.

### Step 7 — Cross-path comparisons

This is the analytically most important section. Six comparisons:

**Comparison 1 — Stage 1 vs. Phase 1 (validation check):**
ARI(Path F Stage 1 label, Phase 1 profile_p1)
- Expected: 1.000 (Stage 1 IS Phase 1)
- If < 1.000 something went wrong in the join — investigate before proceeding

**Comparison 2 — Stage 2 within Profile B vs. Path A within Profile B:**
Restrict to Profile B (N=289). Compute:
ARI(Path F Stage 2 label within B, Path A cluster_behav label within B)
- High ARI (>0.7): the within-B behavioral clusters match Path A's full-sample clusters;
  the within-group scaling and reduced N don't change the structure
- Moderate ARI (0.4–0.7): partial correspondence; within-group structure is related but
  not identical to full-sample Path A; document which clusters re-align
- Low ARI (<0.4): within-group behavioral structure differs from full-sample; some
  within-group behavioral variation that was noise in the full-sample becomes signal here

**Comparison 3 — Stage 2 within Profile A vs. Path A within Profile A:**
Same as Comparison 2, restricted to Profile A (N=125).

**Comparison 4 — Full Path F taxonomy vs. Path A:**
Compute ARI(cell_f, cluster_behav) on full N=414.
- Expected: moderate ARI (~0.4–0.6), because cell_f includes the Stage 1 network split
  that is orthogonal to cluster_behav, but Stage 2 uses the same behavioral features

**Comparison 5 — Full Path F taxonomy vs. Path C:**
Compute ARI(cell_f, subprofile_C) on participants with valid Path C labels.
- Expected: moderate ARI, because Stage 1 of Path F (Profile A/B) partially recovers
  Path C's sub-profile structure (both use Phase 1 as base), but Stage 2 adds behavioral
  split not present in Path C

**Comparison 6 — Contingency cross-tabulation:**
Cross-tabulate cell_f (rows) × subprofile_C (columns: B1/B2/A1/A2).
- This shows how the behavioral sub-types distribute across the network sub-types.
- Key question: are B_behav1 participants concentrated in B1 (single-app locked) or
  distributed across B1/B2? If concentrated → behavioral type and network sub-type are
  NOT fully orthogonal even within Profile B.
- Report chi-square test of independence and Cramér's V.

### Step 8 — Sensitivity: what changes with H_hour in Stage 2?

Run Stage 2 on [sig_hat, H_emp, x_mean, H_hour] within each profile.
Report ARI(3-feature Stage 2 vs. 4-feature Stage 2) within Profile B and within Profile A.
Compare with Path A's finding: ARI(3-feature vs 4-feature) = 0.718 full-sample.

---

## 8. Expected findings and interpretation guidance

### Expected result — Profile B Stage 2 (N=289)

Profile B participants are hub-locked (network dimension saturated). Their behavioral
variation spans the same axes as the full sample. The k=2 split within Profile B is
expected to separate primarily on the noise dimension or the compliance dimension,
mirroring the full-sample Path A structure but within the hub-locked context:

- **B_behav1 (tentative: "Hub-locked, stable responder"):** Low sig_hat, low H_emp,
  relatively low x_mean. These participants have consistent, low-noise friction responses
  within a single-app-dominated phone structure. They are not noisy, and they don't
  override as much.
- **B_behav2 (tentative: "Hub-locked, high-compliance responder"):** Low sig_hat, low
  H_emp, high x_mean. Low noise, but overrides consistently. The compliance dimension
  (x_mean) is what separates them, not the noise level.

If k=3 is stable within Profile B, the expected structure mirrors Path A's C1/C2/C3:
- B_behav1: low-noise, low-override
- B_behav2: low-noise, high-override
- B_behav3: high-noise, variable override

The within-B distribution of behavioral types will test whether the near-zero full-sample
ARI(Path A vs Phase 1) holds within the hub-locked context: if the proportions of low-noise
vs. high-noise participants within Profile B match their full-sample proportions, the
independence claim is confirmed locally, not just globally.

### Expected result — Profile A Stage 2 (N=125)

Profile A is the smaller group. k=2 is the only feasible split. The Stage 2 split is
expected to separate on the noise axis:

- **A_behav1 (tentative: "Distributed-network, stable"):** Lower sig_hat, possibly lower
  H_emp. These participants have distributed app use AND relatively predictable friction
  responses.
- **A_behav2 (tentative: "Distributed-network, variable"):** Higher sig_hat, higher H_emp.
  Distributed network AND noisy behavioral dynamics — the most heterogeneous cell.

However, Profile A's Stage 2 may be weaker than Profile B's (smaller N, less power).
If Jaccard < 0.75 for k=2 within Profile A, report Profile A as a single descriptive
cell (A_all) and document this as a finding about Profile A's behavioral homogeneity.

### Scenario: Stage 2 structure mirrors Path A full-sample structure

If ARI(Stage 2 within B vs. Path A within B) and ARI(Stage 2 within A vs. Path A within A)
are both high (>0.70):
- **Interpretation:** The behavioral clustering is stable across full-sample and within-group
  contexts. The 4-cell taxonomy (2 NeT types × behavioral sub-types) is confirmed as a
  genuine cross product of two orthogonal dimensions. Stage 2 does not reveal new structure
  beyond Path A; it contextualizes Path A's structure within the NeT frame.
- **This is the expected and strongest outcome.** The claim is: "the behavioral sub-types
  identified in Path A hold within each NeT profile independently."

### Scenario: Stage 2 structure diverges from Path A

If ARI(Stage 2 within B vs. Path A within B) < 0.50:
- **Interpretation:** Within-group behavioral structure (controlling for NeT type) differs
  from the full-sample behavioral structure. The NeT type moderates which behavioral axis
  is primary.
- **Report this as a moderation finding.** It means that the behavioral phenotype space
  is not fully orthogonal at the within-profile level, even though it appears orthogonal
  at the full-sample level. Path E (condition-stratified) and Path B (intervention-sensitive)
  gain even more importance in this scenario.

---

## 9. Figures to produce

| Figure | Content |
|---|---|
| `fig_f1_hierarchy_structure.png` | Schematic diagram of the two-stage hierarchy: N counts at each node; Stage 1 = Phase 1 NeT split; Stage 2 = behavioral sub-clustering. Include Jaccard and silhouette at each Stage 2 node. |
| `fig_f2_profileB_behav_space.png` | 3-panel scatter plot within Profile B: sig_hat vs. H_emp, sig_hat vs. x_mean, H_emp vs. x_mean. Color by Path A cluster_behav (C1/C2/C3). Shows how Path A clusters land within Profile B's behavioral space. |
| `fig_f3_profileA_behav_space.png` | Same 3-panel scatter plot within Profile A. Color by Path A cluster_behav. |
| `fig_f4_profileB_k_selection.png` | Silhouette, CH, DB vs. k (k=2,3,4) for Profile B Stage 2 behavioral clustering. Mark selected k with vertical line. |
| `fig_f5_profileA_k_selection.png` | Silhouette, CH, DB vs. k (k=2,3) for Profile A Stage 2 behavioral clustering. Include stability annotation. |
| `fig_f6_cell_profiles.png` | Grouped bar chart: all final cells (4 or 5) showing mean of sig_hat, H_emp, x_mean, H_hour per cell. Include error bars (±1 SEM). Add NeT overlay (HHI_net) as secondary axis or annotation. This is the "fingerprint" of the full taxonomy. |
| `fig_f7_sankey_pathA_to_pathF.png` | Alluvial / Sankey diagram: Path A clusters (C1/C2/C3) flowing into Path F cells (B_behav1/B_behav2/A_behav1/A_behav2). Shows how the behavioral types from Path A distribute across the hierarchical cells. |
| `fig_f8_contingency_heatmaps.png` | Two side-by-side heatmaps: (a) Path F cell × Path C sub-cluster (B1/B2/A1/A2); (b) Path F cell × Path A cluster (C1/C2/C3). Counts and row percentages. |

---

## 10. Output files

| File | Content |
|---|---|
| `ds5_hierarchical_assignments.csv` | Per-participant: participant_id_canonical, study_condition, profile_p1, stage2_label_B (NaN for Profile A), stage2_label_A (NaN for Profile B), cell_f (combined cell label), cluster_behav (Path A, for ARI), subprofile_C (Path C, for ARI) |
| `ds5_hierarchical_profiles.csv` | Per cell: mean/median/std of sig_hat, H_emp, x_mean, H_hour, mu_hat (where available), HHI_net, rho_self, H_trans, H_app (NeT overlays), N per cell |
| `ds5_hierarchical_stability.csv` | Bootstrap Jaccard per Stage 2 node: (Profile B k=2), (Profile B k=3 if run), (Profile A k=2); plus k-selection diagnostics (silhouette/CH/DB per k per profile) |
| `ds5_hierarchical_assignments.md` | Companion: column reference, unit of observation, known limitations |
| `ds5_hierarchical_profiles.md` | Companion: column reference, how to interpret raw vs. scaled values |
| `model_run_summary_path_f.md` | Complete run record: N per node, selected k per node, Jaccard per node, all ARI comparisons, condition χ², psychosocial results |

All files → `outputs/model_outputs/phenotyping/`
Figures → `outputs/model_outputs/phenotyping/figures/`

---

## 11. What this taxonomy can and cannot claim

### Can claim

- The two-stage hierarchy produces a taxonomy with N≥30 per cell (given primary scenario).
- The Stage 2 behavioral sub-types within Profile B are stable (Jaccard ≥ 0.75 threshold).
- The full 4-cell taxonomy captures variation in both network topology AND behavioral
  dynamics simultaneously — no single-axis solution does this.
- Each cell has a distinct feature profile across both NeT and behavioral dimensions.
- The hierarchical taxonomy adds characterization depth beyond Phase 1 alone (which
  differentiated only on NeT type) and beyond Path A alone (which differentiated only
  on behavioral dynamics, without NeT context).
- Condition independence or condition-dependence within each profile (from within-profile
  χ² tests) — stated with the appropriate caveat from Path A (full-sample
  condition χ²=91.885, p<0.0001).

### Cannot claim

- **Cannot claim the hierarchy is causal.** Network type (hub-dominated vs. distributed)
  does not cause behavioral type (high-noise vs. low-noise). Stage 1 and Stage 2 axes
  are orthogonal but both could be downstream of unmeasured individual differences.
- **Cannot claim Stage 2 clusters within Profile A are as stable or reliable as within
  Profile B.** Profile A N=125 is borderline; bootstrap Jaccard is mandatory but may
  be weaker.
- **Cannot claim the 4-cell taxonomy is the uniquely correct partition.** k-selection
  diagnostics justify the choice, but other k values yield plausible alternatives.
  The taxonomy is one well-justified exploratory solution, not a ground truth.
- **Cannot claim the behavioral sub-types are condition-invariant.** Path A found
  condition χ²=91.885, p<0.0001 for the full-sample behavioral clusters. Path F inherits
  this limitation. Path E (condition-stratified) is required before making stability claims.
- **Cannot prescribe friction types or intervention sequences.** That is Step 3. Path F
  creates the initialization vocabulary; it does not define the prescription.
- **Cannot claim these cells replicate in DS4 or other datasets.** All findings are
  DS5-specific and exploratory. Cross-dataset validation is a separate stage.
- **Cannot treat cell labels as validated behavioral traits.** They are exploratory,
  data-driven cluster designations. Labels like "hub-locked, stable responder" are
  shorthand for feature profiles, not diagnostic categories.

---

## 12. What genuinely new information Path F adds

Compared to **Path C alone:**
- Path C characterizes the network sub-structure within each Phase 1 profile (B1/B2/A1/A2).
  It found that behavioral features (sig_hat, H_emp, x_mean) do not differentiate
  network sub-clusters. Path F does the reverse: it characterizes the behavioral
  sub-structure within each Phase 1 profile, without reference to network sub-features.
  The novel information is: "here is what the behavioral landscape looks like within
  each NeT type" — which Path C explicitly did not characterize.

Compared to **Path A alone:**
- Path A characterizes behavioral types (C1/C2/C3) across the full sample, mixing
  Profile A and Profile B participants. It cannot say whether the low-override cluster
  (C1, N=62) is predominantly hub-locked or distributed, or whether the high-noise cluster
  (C3, N=200) is concentrated in one network type.
- Path F answers these questions by conditioning the behavioral analysis on NeT type.
  If Profile B has a higher proportion of high-override participants (C2-like) than
  Profile A, that is a finding Path A cannot see because it pools both profiles.
  (Path A's ARI=0.020 suggests proportions are similar — but Path F tests this directly.)

**The unique contribution:**
Path F produces a **joint characterization table**: for each NeT profile, what is the
distribution of behavioral types? This cross-product description is the richest
single-table summary of DS5's phenotype heterogeneity, and it is the direct initialization
vocabulary for GaT/ABM agent types in Step 3.

---

## 13. Connections to later paths

| Path | How Path F feeds it |
|---|---|
| Path E (condition-stratified, notebook 104) | The 4-cell Path F taxonomy becomes the phenotype reference: does friction condition change the within-profile behavioral sub-type distribution? Path F cells are the units that Path E needs to test for condition × phenotype interactions. |
| Path B (intervention-sensitive, notebook 105) | H_out variability overlaid on Path F cells gives the first estimate of whether friction response unpredictability differs across cells — directly relevant to "who can be moved." |
| Path D (dynamic/stochastic, notebook 106) | The Stage 2 within-profile split on sig_hat/H_emp is related to the drift-noise regime in DyS; Path F cells can be cross-tabulated with DyS phenotype labels when that path is complete. |
| Step 3 (GaT / ABM, deferred) | Path F cells define the agent initialization types: NeT structure (network topology parameter set) × behavioral dynamics (noise level, compliance level, entropy). A 4-cell taxonomy means 4 agent types. |

---

## ACTUAL RESULTS (notebook 103 run 2026-04-19)

**Stage 1:** Phase 1 profile_p1 split used directly. Stage 1 validation ARI = 1.000.

**Profile B Stage 2 (N=289; k=3; silhouette=0.410; Jaccard=0.954 ± 0.071 STABLE):**
- B_behav1 (N=37): sig_hat=0.127, H_emp=1.754, x_mean=0.364 — low-noise, low-override
- B_behav2 (N=104): sig_hat=0.146, H_emp=1.607, x_mean=0.867 — low-noise, high-override
- B_behav3 (N=148): sig_hat=0.282, H_emp=2.463, x_mean=0.677 — high-noise, variable
- k=3 selected over k=2 (sil=0.364) because higher silhouette and all cells N≥30

**Profile A Stage 2 (N=125; k=2 attempted; Jaccard=0.744 MARGINAL):**
- k=2 Jaccard just below 0.75 threshold → reported as A_all (descriptive, no sub-split)
- k=3 rejected (min cell N=23 < 30)
- A_all: sig_hat=0.191, H_emp=1.964, x_mean=0.669 — distributed network, behaviorally undifferentiated

**Final taxonomy: 4 cells** — B_behav1, B_behav2, B_behav3, A_all

**Cross-path comparisons:**
- ARI(Stage 1 vs Phase 1) = 1.000 ✓
- ARI(Stage2-B vs Path A within B) = **1.000** → EXACT correspondence; B_behav1=C1, B_behav2=C2, B_behav3=C3
- ARI(Stage2-A vs Path A within A) = 0.000 (trivially zero; A_all is a single group)
- ARI(Path F combined vs Path A) = 0.520
- ARI(Path F combined vs Path C) = 0.343
- Cramér's V (Path F × Path C contingency) = 0.579 — driven structurally by A/B split, not within-B
- Within Profile B: B_behav1/2/3 distribute ~89%/93%/88% in B1 and ~11%/7%/12% in B2
  → behavioral sub-types within Profile B are INDEPENDENT of Path C's network sub-types

**Sensitivity (scaler):** ARI(within-group vs full-sample scaler within Profile B) = 1.000 — scaling choice irrelevant

**Sensitivity (feature set) — NOT PERFORMED:** The pre-registered Step 8 check (re-run Stage 2 on
[sig_hat, H_emp, x_mean, H_hour] within each profile and report ARI against the 3-feature solution,
benchmarked against Path A's full-sample 3-vs-4-feature ARI = 0.718) was never implemented in
notebook 103. H_hour is used there only as a descriptive/overlay column; CORE_FEATURES =
['sig_hat', 'H_emp', 'x_mean'] is the sole clustering input in every cell. Because H_hour
correlates with sig_hat at r = -0.517 (Profile B) / -0.515 (Profile A) — the notebook's own cell 7
output — and because adding it materially changed Path A's full-sample partition (ARI = 0.718),
the robustness of the 4-cell Path F taxonomy to this feature-set choice is UNVERIFIED.

**Condition independence:** Profile B chi2=60.963, df=4, p<0.0001 — NOT condition-independent;
same finding as Path A; Path E required.

**Key interpretation (scope corrected 2026-08-08):** Path A's k=3 behavioral partition is exactly
reproduced when re-fit inside Profile B (ARI=1.000; crosstab is a perfect permutation matrix,
C1→37, C2→104, C3→148), and the within-group vs. full-sample scaler check also gives ARI=1.000.
This confirms the behavioral split is not an artifact of pooling Profile A and Profile B and is
insensitive to the scaler choice. It is a consistency check on a subset of Path A's own solution,
using the same three features, the same k, the same algorithm and the same seed — not an
independent test of orthogonality. No equivalent test is possible within Profile A, which was not
sub-split (its only available number, ARI=0.000, is degenerate against the constant label 'A_all').
The local-orthogonality claim is therefore established for Profile B only; the 125 Profile A
participants (30.2% of the sample) contribute no evidence to it. The global orthogonality result
(ARI=0.020 full-sample, Path A vs. Phase 1) is unaffected and remains the primary evidence.

---

## 14. Key numbers from prior paths (for comparison reference)

### Phase 1

| Metric | Value |
|---|---|
| k | 2 (Profile A / Profile B) |
| N (Profile B) | 289 |
| N (Profile A) | 125 |
| Silhouette | not reported at full-sample level |
| Jaccard | 0.995 |
| Driving features | HHI_net, rho_self |

### Path C (notebook 101)

| Metric | Profile B sub-clustering | Profile A sub-clustering | Full-sample NeT-only |
|---|---|---|---|
| k | 2 (B1/B2) | 2 (A1/A2) | 2 |
| N per cell | B1=260, B2=29 | A1=85, A2=40 | — |
| Silhouette | 0.866 | — | — |
| Jaccard | 0.996 | 0.835 | 0.994 |
| ARI vs Phase 1 | — | — | 0.990 |
| Behavioral features differ? | No | No | — |

### Path A (notebook 102)

| Metric | Value |
|---|---|
| k | 3 (C1/C2/C3) |
| N per cell | C1=62, C2=152, C3=200 |
| Silhouette | 0.4071 |
| Jaccard | 0.991 ± 0.022 (STABLE) |
| ARI vs Phase 1 | **0.020** |
| ARI vs Path C sub-profiles | 0.017 |
| ARI vs NeT-only full-sample | 0.020 |
| Condition χ² | 91.885, p<0.0001 (NOT independent) |
| C1 profile | sig_hat=0.121, H_emp=1.734, x_mean=0.358 (low-noise, low-override) |
| C2 profile | sig_hat=0.143, H_emp=1.604, x_mean=0.859 (low-noise, high-override) |
| C3 profile | sig_hat=0.281, H_emp=2.454, x_mean=0.673 (high-noise, variable) |

**Path F Stage 2 target:** Recover a within-profile behavioral split that, when projected
back to the full sample, has high ARI with Path A's C1/C2/C3. The expected strongest
test: does Profile B's Stage 2 split correspond to a subset of Path A's three clusters?
If the within-B Stage 2 solution is ARI≈0.7–0.9 with Path A restricted to Profile B,
that confirms the behavioral sub-types are NeT-type-invariant — both the thesis's core
theoretical claim and the key cross-path finding.
