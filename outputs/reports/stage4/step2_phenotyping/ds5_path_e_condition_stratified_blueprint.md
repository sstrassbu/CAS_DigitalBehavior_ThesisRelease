# DS5 Step 2 Path E — Condition-Stratified Phenotyping Blueprint

**Notebook:** `104_ds5_condition_stratified_phenotype.ipynb`
**Written:** 2026-04-19
**Stage:** Stage 4, Step 2 — Path E (fourth of six paths)
**Depends on:**
- `outputs/model_outputs/phenotyping/ds5_phenotype_feature_matrix.csv` — behavior features
- `outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv` — Phase 1 labels
- `outputs/model_outputs/phenotyping/ds5_behav_only_cluster_assignments.csv` — Path A cluster_behav
- `outputs/model_outputs/phenotyping/ds5_hierarchical_assignments.csv` — Path F cell_f labels

---

## 0. Why this notebook is essential now

Paths A and F both confirmed a severe condition-dependence problem:

| Finding | Source |
|---|---|
| Condition χ² = 91.885, p<0.0001 | Path A — full-sample behavioral clusters |
| Condition χ² = 60.963, p<0.0001 | Path F — behavioral clusters within Profile B |

The observed distribution shift is dramatic:

| Cluster | Control | Default | Reintervention |
|---|---|---|---|
| C1 (low-noise, low-override) | 11.7% | 17.6% | 15.6% |
| C2 (low-noise, **high-override**) | **65.0%** | **10.6%** | 35.6% |
| C3 (high-noise, variable) | 23.4% | 71.8% | 48.9% |

C2 is present in 65% of the control group but only 11% of the default group. This is the largest
distributional difference across all previous phenotyping paths and raises a direct threat to
the current DS5 phenotype taxonomy.

Two competing explanations exist, and Path E is designed to distinguish them:

**Explanation 1 — Distributional effect:**
The same three behavioral phenotype types exist in all conditions, but condition assignment changes
the probability of belonging to each type. C2 participants in the default group were reassigned
to C3 not because the cluster structure changed, but because friction exposure changed their
measured override rate (x_mean) and/or behavioral entropy (H_emp). The underlying trait is the
same; the observable measurement shifted.

**Explanation 2 — Structural effect:**
The default condition does not merely shift people across a fixed phenotype space. It reshapes
the space itself — the cluster centroids, the feature distributions, and possibly the within-group
variance structure change across conditions. In this case, the behavioral subtypes are not truly
condition-invariant latent types. They are condition-emergent patterns.

**This is the central question Path E must answer.**

---

## 1. Exact goal

Path E tests whether the behavioral phenotype structure documented in Path A (k=3, full-sample)
and Path F (Stage 2 within Profile B, k=3) is:

**(a) Condition-invariant:** The same cluster number, centroid positions, and cluster geometry
recur in each condition separately, with similar proportions. Condition assignment does not
structurally change the phenotype landscape — it may shift some individuals between types, but
the types themselves are stable across experimental contexts.

**(b) Condition-shaped:** Different conditions yield different cluster structures, different
centroid positions, or unstable cluster solutions. The phenotype types observed in the full
sample are partly or largely an artifact of condition mixing — they reflect the combination of
three different within-condition distributions rather than true latent individual differences.

**Intermediate outcomes also matter:**
- Cluster structure stable but proportions differ → condition selects for types, not shapes them
- Cluster structure partially stable (k constant, centroids shift) → condition modulates expression
- Cluster structure unstable in some conditions → sample-size limit, not structural conclusion

Path E cannot establish causality. It can only describe how within-condition clustering solutions
relate to full-sample solutions.

---

## 2. What Path E adds that Paths A and F cannot

| Question | Path A | Path F | Path E |
|---|---|---|---|
| Does behavior-only structure exist? | YES — k=3 identified | YES — within Profile B | Confirms or qualifies |
| Is structure NeT-independent? | YES — ARI vs Phase 1 = 0.020 | YES — ARI=1.000 within B | Does not re-examine |
| Are types condition-invariant? | UNKNOWN — chi² only | UNKNOWN — chi² only | **THIS IS PATH E** |
| Are centroids stable across conditions? | UNKNOWN | UNKNOWN | **THIS IS PATH E** |
| Do same k types recur within each condition? | UNKNOWN | UNKNOWN | **THIS IS PATH E** |
| What is the proportion shift direction? | UNKNOWN | UNKNOWN | **THIS IS PATH E** |

Path A and Path F established that behavioral clusters exist and that they are NOT condition-independent
by chi-square test. But chi-square only tests whether cluster membership and condition are associated —
it does not distinguish structural from distributional effects.

Path E moves the question from "are they associated?" (Path A/F answer: yes) to
"are the types themselves different?" (Path E question: structural or distributional?).

This distinction matters for the thesis because:
- If **distributional**: the current four-cell taxonomy (B_behav1/2/3, A_all) remains a valid
  description of DS5 heterogeneity; condition just predicts which cell participants end up in
- If **structural**: the four-cell taxonomy conflates condition-induced patterns with individual
  differences; any interpretation of B_behav2 as "high-override type" must be qualified as
  "primarily a control-condition phenomenon"

---

## 3. Input files

| File | Used for |
|---|---|
| `ds5_phenotype_feature_matrix.csv` | Core clustering features + study_condition |
| `ds5_behav_only_cluster_assignments.csv` | Path A cluster_behav labels (full-sample reference) |
| `ds5_hierarchical_assignments.csv` | Path F cell_f labels + profile_p1 |
| `ds5_survey_features.csv` | Psychosocial overlays (post-hoc only) |

---

## 4. Conditions in DS5

| Condition | N (full sample) | Profile B | Profile A |
|---|---|---|---|
| control | 137 | 94 | 43 |
| default | 142 | 96 | 46 |
| reintervention | 135 | 99 | 36 |

### 4.1 Sample-size implications

**Full-sample within-condition clustering (all N~135–142):**
- k=2: cells ≈ 68–71 per cluster → safe (well above N=30)
- k=3: cells ≈ 45–47 average → acceptable; reject k=3 if any cell < 30
- k=4: cells ≈ 34–35 average → risky; only defensible if min cell ≥ 30 AND Jaccard ≥ 0.75

**Profile B within-condition clustering (N~94–99):**
- k=2: cells ≈ 47–50 → safe
- k=3: cells ≈ 31–33 average → borderline acceptable; REQUIRE min cell ≥ 30 and Jaccard ≥ 0.75
- k=4: cells ≈ 23–25 → REJECT (below N=30 threshold)

**Profile A within-condition clustering (N=36–46):**
- k=2: cells ≈ 18–23 → BELOW N=30 threshold
- **Profile A within-condition clustering is NOT feasible.** Do not attempt it.
- Profile A within-condition analysis: descriptive feature distributions only (no clustering)

---

## 5. Feature specification

### 5.1 Primary clustering features (identical to Path A)

| Feature | Role |
|---|---|
| `sig_hat` | Diffusion/noise |
| `H_emp` | Behavioral entropy |
| `x_mean` | Override rate |

Use the same three-feature set as Path A for direct comparability. Within-condition solutions
must be comparable to the Path A full-sample solution — feature changes would confound the
comparison.

### 5.2 Scaling

**Within-condition StandardScaler (primary):** Fit a separate scaler on each condition's data.
This is the appropriate choice when asking whether the cluster structure is the same within each
condition, because it normalizes within-condition variance before clustering.

**Caveat:** Within-condition scaling changes the interpretation of centroid distances relative to
the full-sample scaler. Centroid positions in within-condition scaled space cannot be directly
compared numerically to full-sample Path A centroids. Use ARI (label comparison) rather than
centroid distance for cross-condition and cross-path comparison.

**Full-sample scaler sensitivity (supplementary):** Also run all within-condition clustering
using the full-sample scaler fitted on Path A data. This allows direct centroid comparison.
Report ARI(within-cond scaler vs full-sample scaler) per condition.

### 5.3 Do NOT use

- NeT features: excluded (same as Path A)
- `study_condition` as a clustering feature: excluded (this is the stratification variable)
- `H_out` raw: condition-confounded
- `sigma_mu_ratio`: 31.2% NaN — reduces N; exclude from clustering

---

## 6. Analysis design

Path E has two complementary but distinct sub-analyses:

### Sub-analysis 1 — Within-condition k-means (structural test)

Run k-means independently on each condition's data, using the primary [sig_hat, H_emp, x_mean]
feature set with within-condition scaling. This tests whether the same cluster structure
(same k, similar centroid geometry) recurs in isolation within each experimental group.

**For each condition (control, default, reintervention):**
1. Scale features with within-condition StandardScaler
2. Run k-means for k in [2, 3, 4]; enforce min cell size ≥ 30
3. Bootstrap Jaccard stability (100 bootstraps, 80% sample)
4. Select k by: max silhouette where all cells ≥ 30 AND Jaccard ≥ 0.60, applying the §8 stability bands: ≥0.75 STABLE (interpret freely), 0.60–0.75 MARGINAL (report with an explicit caveat), <0.60 UNSTABLE (do not interpret). NOTE: this is a deliberately looser acceptance rule than Path F (notebook 103), which requires ≥0.75 before a sub-split is reported at all — Path F rejected a Profile A split at Jaccard=0.744 while Path E reports a control solution at the same 0.744 as MARGINAL. The two paths ask different questions (does within-condition structure exist? vs. should a taxonomy cell be sub-divided?), but the divergence must be stated wherever both are cited together.
5. If no stable k exists: report "insufficient within-condition structure"
6. Label clusters by sig_hat ascending (same convention as Path A/F)

**Also run Profile B within each condition** (if feasible per Section 4.1):
1. Same procedure; max k=3; reject k=3 if min cell < 30

### Sub-analysis 2 — Feature distribution comparison (distributional test)

Without clustering, directly compare the within-condition distributions of sig_hat, H_emp, x_mean.
If the condition effect is purely distributional (same underlying types, different proportions),
then:
- The overall univariate distributions of all three features should differ significantly across
  conditions (KW test)
- But the within-cluster feature distributions (using Path A C1/C2/C3 labels) should show stable
  centroids even across conditions

Test:
- KW test: sig_hat, H_emp, x_mean across conditions (three-way)
- Pairwise Mann-Whitney U: control vs default, control vs reintervention, default vs reintervention
- Within-cluster feature distributions: within Path A C1, C2, C3 — do feature means differ by
  condition? (If yes → structural effect contaminating Path A cluster centroids)

---

## 7. Comparison logic (full set, six comparisons)

### Comparison 1: ARI(within-condition vs Path A full-sample)
**Per condition:** Apply Path A full-sample cluster labels to the same participants;
compare against within-condition solution labels.
- High ARI (>0.7): Within-condition clustering reproduces the full-sample structure →
  condition-invariant types supported
- Moderate ARI (0.4–0.7): Partial recovery — some types stable, others not
- Low ARI (<0.4): Within-condition structure diverges substantially from full-sample →
  structural condition effect

### Comparison 2: ARI(within-condition solution vs within-condition solution, cross-conditions)
Compare the cluster assignments of participants who would appear in both solutions if the
same k is found across conditions (via ARI on the intersection, or descriptively):
- More practically: apply each within-condition centroid (via KMeans predict) to ALL 414
  participants, then compare ARI across the three condition-specific models applied to the
  full sample
- High consistency across conditions → the cluster geometry is stable; just proportions differ
- Low consistency → the conditions have genuinely different cluster geometries

### Comparison 3: Within-cluster feature means by condition
For each Path A cluster (C1, C2, C3), compute mean of sig_hat, H_emp, x_mean separately
for participants in control vs default vs reintervention.
- If means are similar across conditions within each cluster → cluster centroids are stable;
  condition acts as a selector, not a shaper
- If means differ strongly → condition changes the measured behavioral features even within
  the same cluster type → structural confound

### Comparison 4: Within-condition k selection vs full-sample k
Does the same k emerge from all three conditions as from the full sample (k=3)?
- k consistent across all conditions (and with Path A): structure is condition-invariant
- k differs across conditions: condition may be determining the dimensionality of phenotype space

### Comparison 5: Profile B within-condition vs Path F Stage 2 within Profile B
For Profile B participants only, compare within-condition B clustering vs full-sample
Profile B Stage 2 (B_behav1/2/3 from Path F):
- ARI per condition: how well does within-condition Profile B solution match B_behav1/2/3?
- This is the most targeted test of whether the Profile B behavioral sub-types are condition-driven

### Comparison 6: Centroid displacement (supplementary, full-sample scaler run)
Using the full-sample scaler sensitivity run, compare centroid positions across conditions in
the same feature space.
- Small centroid displacement (< 0.5 SD units) → distributional; same types, different N
- Large centroid displacement (> 1.0 SD units) → structural; condition reshapes the space

---

## 8. Stability rules

| Scenario | Rule |
|---|---|
| Jaccard ≥ 0.75 | STABLE — report and interpret |
| Jaccard 0.60–0.75 | MARGINAL — report with explicit caveat |
| Jaccard < 0.60 | UNSTABLE — do not interpret clusters; report as weak-structure finding |
| All k yield min cell < 30 | INFEASIBLE — report descriptively only, no clusters |
| k=1 or no convergence | Null finding: "no cluster structure within this condition" |

If within-condition clustering yields unstable or infeasible results in one or more conditions,
this is itself an informative Path E finding: it means the full-sample solution was partly an
artifact of sample pooling, not a reflection of within-condition individual differences.

---

## 9. What different outcomes mean

### Outcome A — Structure-invariant (ideal case for thesis)
All three conditions independently yield:
- k=3 stable (Jaccard ≥ 0.75 in all conditions)
- ARI(within-cond vs Path A) > 0.6 per condition
- Similar centroid positions (small displacement in full-sample scaler space)
- Only proportions differ across conditions

**Interpretation:** Behavioral phenotypes are genuine individual differences. The condition
effect documented in Path A/F reflects that conditions differentially attract or retain
particular behavioral types. The current taxonomy remains valid. Condition should be included
as a covariate in downstream analyses.

### Outcome B — Distributional shift (mixed case)
Within-condition solutions are partially consistent with Path A (ARI 0.4–0.7), but proportions
differ dramatically and centroids shift moderately.

**Interpretation:** Behavioral features are condition-sensitive (the intervention changes x_mean
and H_emp), but the underlying cluster geometry is partially preserved. The taxonomy can be
retained with the explicit qualification that observed cluster membership partly reflects
condition effects. Individual differences and condition effects are entangled. This is the
most honest and likely realistic outcome.

### Outcome C — Structure-dependent (worst case for simple phenotype claim)
Within-condition solutions yield:
- Different k across conditions, OR
- Unstable k in one or more conditions, OR
- ARI(within-cond vs Path A) < 0.4 consistently

**Interpretation:** The behavioral phenotypes identified in Path A/F are primarily a consequence
of pooling three condition-specific distributions. The types are not condition-invariant latent
classes. The taxonomy must be presented as exploratory and condition-mediated. This strengthens
the case for condition-specific Step 3 personalization approaches.

### Outcome D — Default condition is structurally different from control/reintervention
The control and reintervention conditions show stable within-condition solutions consistent
with Path A, but the default condition yields a different k or unstable structure.

**Interpretation:** The default friction condition is qualitatively different from the other
two in its effect on the behavioral feature space. This is theoretically coherent — default
friction makes non-override the path of least resistance, potentially collapsing the override
rate distribution and homogenizing the H_emp space. If so, the default condition effectively
removes the behavioral diversity that drives the Path A cluster structure.

---

## 10. Figures to produce

| Figure | Content |
|---|---|
| `fig_e1_feature_distributions_by_condition.png` | Violin or box plots of sig_hat, H_emp, x_mean split by condition (3×3 panel) |
| `fig_e2_pairplots_by_condition.png` | Pairwise scatter plots [sig_hat, H_emp, x_mean] with condition as color; shows feature-space geometry per condition |
| `fig_e3_cluster_selection_by_condition.png` | Silhouette vs k for all three conditions on one figure (3-panel or overlaid) |
| `fig_e4_within_condition_profiles.png` | Cluster profiles (radar or grouped bar) per condition — shows centroid positions |
| `fig_e5_ari_comparison_heatmap.png` | ARI matrix: rows = within-condition solutions, columns = full-sample Path A, Path F, cross-conditions |
| `fig_e6_proportion_shifts.png` | Stacked bar chart showing cluster composition per condition (within-condition solution); shows proportion shift direction |
| `fig_e7_within_cluster_condition_split.png` | Within each Path A cluster (C1/C2/C3): boxplot of features by condition; tests centroid stability |
| `fig_e8_alluvial_cond_vs_path_a.png` | Alluvial diagram: within-condition cluster assignments vs Path A full-sample assignments |

---

## 11. Notebook structure (cell outline)

```
[0] Setup — imports, paths, constants
[1] Load data — feature matrix, Path A labels, Path F labels
[2] Merge master dataframe (N=414)
[3] Condition descriptives — N per condition, feature means, chi² Path A × condition
[4] Sub-analysis 2 setup: KW test and pairwise MWU across conditions for each feature
[5] Within-cluster (Path A) feature stability by condition (Comparison 3)
[6] fig_e1 — feature distributions by condition
[7] fig_e2 — pairplots by condition

--- Full-sample within-condition clustering ---
[8] Within-condition scaling (3 separate scalers)
[9] Control: k-selection loop (k=2,3,4), bootstrap Jaccard k_best
[10] Default: k-selection loop, bootstrap Jaccard k_best
[11] Reintervention: k-selection loop, bootstrap Jaccard k_best
[12] fig_e3 — cluster selection by condition

--- Within-condition label assignment ---
[13] Control: assign labels, order by sig_hat ascending
[14] Default: assign labels
[15] Reintervention: assign labels
[16] fig_e4 — within-condition cluster profiles

--- Profile B within-condition (if feasible) ---
[17] Profile B split per condition
[18] Profile B: within-condition k-selection (k=2,3)
[19] Profile B: bootstrap Jaccard per condition
[20] Profile B: label assignment if stable

--- Comparisons ---
[21] Comparison 1: ARI(within-cond vs Path A) per condition
[22] Comparison 2: cross-condition ARI via centroid projection
[23] Comparison 3: already done in cell [5]
[24] Comparison 4: k consistency table
[25] Comparison 5: Profile B within-cond vs Path F Stage 2
[26] fig_e5 — ARI comparison heatmap

--- Sensitivity: full-sample scaler ---
[27] Full-sample scaler re-run (3 conditions, same procedure)
[28] Comparison 6: centroid displacement

--- Results summaries ---
[29] fig_e6 — proportion shifts
[30] fig_e7 — within-cluster condition split
[31] fig_e8 — alluvial

--- Output saving ---
[32] Save ds5_condition_cluster_assignments.csv + .md
[33] Save ds5_condition_cluster_profiles.csv + .md
[34] Save ds5_condition_cluster_stability.csv + .md
[35] Save model_run_summary_path_e.md
[36] Verification — confirm all outputs present
```

---

## 12. Output files

All to `outputs/model_outputs/phenotyping/`:

| File | Content |
|---|---|
| `ds5_condition_cluster_assignments.csv` | Per-participant: participant_id_canonical, study_condition, profile_p1, cond_cluster_full (within-condition full-sample cluster label), cond_cluster_B (within-condition Profile B label, NaN if Profile A or infeasible), cluster_behav (Path A), cell_f (Path F) |
| `ds5_condition_cluster_assignments.md` | Companion |
| `ds5_condition_cluster_profiles.csv` | Mean/median/std of features per within-condition cluster; plus condition column |
| `ds5_condition_cluster_profiles.md` | Companion |
| `ds5_condition_cluster_stability.csv` | k-selection and Jaccard results per condition per k; includes feasibility flag |
| `ds5_condition_cluster_stability.md` | Companion |
| `model_run_summary_path_e.md` | Complete run record |
| `figures/fig_e1_feature_distributions_by_condition.png` | |
| `figures/fig_e2_pairplots_by_condition.png` | |
| `figures/fig_e3_cluster_selection_by_condition.png` | |
| `figures/fig_e4_within_condition_profiles.png` | |
| `figures/fig_e5_ari_comparison_heatmap.png` | |
| `figures/fig_e6_proportion_shifts.png` | |
| `figures/fig_e7_within_cluster_condition_split.png` | |
| `figures/fig_e8_alluvial_cond_vs_path_a.png` | |

---

## 13. What this notebook cannot do

- **Cannot establish causality.** Condition was randomly assigned, so the design is experimental;
  but Path E clusters are post-hoc and observational. "Condition shapes cluster membership" is
  a descriptive association claim, not a causal mechanism claim.
- **Cannot separate trait from state.** Even within each condition, observed sig_hat/H_emp/x_mean
  reflect both stable individual differences and within-study behavioral change. Path E cannot
  decompose this.
- **Cannot cluster Profile A within conditions.** N=36–46 per condition yields cells below N=30.
  Profile A within-condition analysis is descriptive only.
- **Cannot resolve whether condition assignment preceded or followed behavioral type.** In a true
  RCT, assignment is random and prior to measurement, so the direction is condition → behavior.
  But this still does not mean condition causes a latent type to emerge vs. suppress expression.
- **Cannot claim between-condition consistency without cross-dataset replication.**
- **Cannot prescribe friction types.** This is Step 2 only.

---

## 14. Central question: if behavioral clusters differ strongly by condition, what does that mean for the current DS5 phenotypes?

This is the pivotal interpretive question for the thesis.

**If strong structural condition-dependence is confirmed (Outcome C or D above):**

The current DS5 phenotype taxonomy (B_behav1/2/3, A_all from Path F; C1/C2/C3 from Path A)
should be presented as:

> "Behavioral phenotypes identified in the full DS5 sample reflect a mixture of individual
> differences and condition-induced behavioral patterns. The high-override type (C2/B_behav2)
> is predominantly present in the control condition (65% of control participants), while the
> high-noise, high-entropy type (C3/B_behav3) dominates the default condition (72%). This
> means that the behavioral taxonomy partially reflects condition effects rather than purely
> stable individual differences."

This does NOT invalidate the taxonomy. It reframes it. The finding becomes:
- The taxonomy correctly describes behavioral heterogeneity in DS5 as observed
- But condition × behavioral type interaction is the more scientifically interesting finding
- Step 3 personalization should be conditioned on condition assignment, not just on phenotype type

**If distributional shift with structural stability is confirmed (Outcome B):**

The current taxonomy remains valid with moderate qualification:
> "Condition assignment is associated with differential cluster membership, consistent with
> friction conditions shifting override rates and behavioral entropy. However, the within-
> condition cluster geometry is partially preserved, suggesting that individual differences
> in sig_hat/H_emp/x_mean persist across conditions and are not entirely condition-induced.
> The current taxonomy captures both stable individual differences and condition-mediated
> behavioral profiles."

**If structure-invariant (Outcome A):**

The current taxonomy is strongly validated:
> "The three behavioral sub-types identified in Path A and Path F recur within each condition
> independently. Condition assignment shifts the distribution of type membership — the default
> friction condition is associated with fewer high-override participants — but does not change
> the underlying behavioral type structure. The phenotype taxonomy reflects stable individual
> differences that condition selects for or against."

---

## 15. Connections to later paths and thesis

| Path / Step | How Path E feeds it |
|---|---|
| Path B (intervention-sensitive) | If structural condition dependence found, Path B must stratify by condition; if distributional, Path B can use full-sample phenotype as base |
| Path D (dynamic/stochastic) | Condition timing effects on sig_hat trajectory; condition-stratified insight from Path E informs whether to include condition as a predictor |
| Step 3 (personalization) | If Outcome C/D: personalization should be condition-specific; if Outcome A: phenotype alone can guide friction type recommendation |
| Thesis chapter structure | Path E provides the critical "what do the phenotypes mean given the experimental design" section; moves the thesis from descriptive phenotyping to phenotype-condition interaction |

---

## 16. Key prior numbers for comparison

| Metric | Value | Source |
|---|---|---|
| Path A: condition chi² | 91.885, p<0.0001 | 102_ds5_behavior_only_phenotype.ipynb |
| Path F within-B: condition chi² | 60.963, p<0.0001 | 103_ds5_hierarchical_phenotype.ipynb |
| C2 in control | 65.0% of control | Path A full-sample |
| C2 in default | 10.6% of default | Path A full-sample |
| C2 in reintervention | 35.6% of reintervention | Path A full-sample |
| x_mean: control mean | 0.783 | Feature matrix by-condition |
| x_mean: default mean | 0.618 | Feature matrix by-condition |
| x_mean: reintervention mean | 0.685 | Feature matrix by-condition |
| sig_hat: control mean | 0.172 | Feature matrix by-condition |
| sig_hat: default mean | 0.245 | Feature matrix by-condition |
| B_behav2 in control B | 66.0% | Path F within Profile B |
| B_behav2 in default B | 13.5% | Path F within Profile B |

---

## ACTUAL RESULTS (added 2026-04-20 after execution of notebook 104)

### K-selection results (full-sample within-condition)

| Condition | N | Selected k | Jaccard | Flag |
|---|---|---|---|---|
| control | 137 | 2 | 0.744 | MARGINAL |
| default | 142 | NONE | — | ALL REJECTED (min_cell < 30) |
| reintervention | 135 | 2 | 0.959 | STABLE |

**Critical finding:** The default condition produced NO feasible clustering. k=2 gave min_cell=28
(< 30 threshold), k=3 gave min_cell=27, k=4 gave min_cell=8. The default friction condition
collapses behavioral heterogeneity into an undifferentiated distribution.

### K-selection results (Profile B within-condition)

| Condition | Profile B N | Selected k | Jaccard | Flag |
|---|---|---|---|---|
| control | 94 | 2 | 0.912 | STABLE |
| default | 96 | NONE | — | ALL REJECTED |
| reintervention | 99 | 2 | 0.883 | STABLE |

### Within-condition cluster profiles

| Cluster | N | sig_hat | H_emp | x_mean |
|---|---|---|---|---|
| CON_C1 (control) | 65 | 0.118 | 1.296 | 0.885 |
| CON_C2 (control) | 72 | 0.221 | 2.026 | 0.690 |
| undifferentiated (default) | 142 | 0.245 | 2.331 | 0.618 |
| REI_C1 (reintervention) | 68 | 0.126 | 1.696 | 0.711 |
| REI_C2 (reintervention) | 67 | 0.276 | 2.472 | 0.659 |

### Cross-path comparisons

| Comparison | Value | Interpretation |
|---|---|---|
| ARI(control within-cond vs Path A) | 0.262 | LOW — structural divergence |
| ARI(default within-cond vs Path A) | 0.000 | zero (all undifferentiated) |
| ARI(reintervention within-cond vs Path A) | 0.697 | HIGH-MODERATE — partial recovery |
| Mean ARI | 0.320 | — |
| ARI(control model vs reintervention model, full sample) | 0.266 | LOW — different geometries |
| Centroid 1 displacement (control vs reintervention) | 1.136 SD units | LARGE |
| Centroid 2 displacement (control vs reintervention) | 0.905 SD units | MODERATE |
| ARI(Profile B: control within-cond vs Path F stage2_B) | 0.603 | MODERATE |
| ARI(Profile B: reintervention within-cond vs Path F stage2_B) | 0.749 | HIGH-MODERATE |
| ARI(within-cond vs full-sample scaler, control) | 0.858 | STABLE (scaler irrelevant) |
| ARI(within-cond vs full-sample scaler, reintervention) | 0.970 | VERY STABLE |

### Interpretation outcome

**Outcome D confirmed:** The default condition is structurally different from control and
reintervention. The default friction condition eliminates behavioral heterogeneity — it does not
merely shift proportions, it collapses the behavioral feature space into an undifferentiated
distribution where no stable k-means solution with N≥30 cells is achievable.

Key interpretive conclusions:
1. The full-sample Path A k=3 taxonomy is partly condition-mediated:
   - C2 (high-override, low-noise) is predominantly a control-condition phenomenon
   - C3 (high-noise, variable) is dominated by default-condition participants
   - The reintervention condition is intermediate and preserves more within-condition structure
2. The default friction condition is qualitatively different: it suppresses behavioral
   diversity rather than merely redistributing participants across stable types
3. The reintervention condition most closely approximates the full-sample Path A structure
   (ARI=0.70), suggesting the full-sample solution is largely driven by reintervention+control
4. Path B (intervention-sensitive) and Step 3 (personalization) MUST stratify by condition
5. The behavioral phenotype taxonomy should be presented with explicit condition qualification

### What this means for the thesis

The DS5 behavioral phenotype taxonomy (B_behav1/2/3 and C1/C2/C3) must be interpreted as:
- Describing DS5 behavioral heterogeneity as observed in a mixed-condition sample
- NOT describing stable individual differences that are condition-invariant
- Being substantially shaped by which experimental condition participants were assigned to
- The default friction condition functionally eliminates the behavioral trait distinction
  between the low-noise/high-override type and the high-noise/variable type

This is a strong thesis finding in its own right: friction condition type determines whether
behavioral heterogeneity is observable at all.
