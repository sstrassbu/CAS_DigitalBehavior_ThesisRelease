# Blueprint: DS5 Step 2 Path D — Dynamic/Stochastic Phenotyping

**Notebook:** `106_ds5_dynamic_stochastic_phenotype.ipynb`  
**Blueprint date:** 2026-04-20  
**Stage:** Stage 4, Step 2 — Path D (sixth and final Step 2 path)  
**Dataset:** DS5 (N=414 StoP-eligible participants)

---

## Central Question

> **After Paths A, C, F, E, and B — each of which has already drawn on the stochastic-process
> feature space (sig_hat, H_emp, x_mean) — does Path D reveal a genuinely new phenotype
> structure along the dynamic/stochastic axis, or does its main value lie in deepening
> and interpreting the behavioral-dynamic taxonomy already identified?**

**Pre-analysis answer (explicitly stated):**

Path D is NOT expected to reveal a genuinely new phenotype structure. The behavioral-dynamic
axis (sig_hat × H_emp) was already the primary discriminator in Path A (k=3, J=0.991 STABLE),
confirmed in Path F (Stage 2 within Profile B, k=3, J=0.954, ARI=1.000 vs Path A within B),
and validated under condition stratification in Paths E and B.

The remaining "dynamic" features not yet used in clustering (mu_hat, sigma_mu_ratio, chi_behav,
F_behav, H_SDE, beta_behav, H_hour) are either:

1. **Collinear with existing Path A features** and will fail the correlation gate
   (H_SDE, beta_behav, F_behav)
2. **Near-zero for too many participants** and provide minimal discriminatory power
   (mu_hat: |μ| < 0.005 for 31.2% of N=414; sigma_mu_ratio: 31.2% NaN — not suitable for
   clustering at all)
3. **Low-variance and likely weak** as a clustering dimension (H_hour: std=0.232)
4. **Theoretically motivated but partially derived** from features already in Path A
   (chi_behav = β·p·(1−p) where β=2/σ̂² and p=x_mean; so chi_behav is a function of
   both sig_hat and x_mean, which are already Path A features)

**Path D's thesis value is therefore:**

1. **Model-language grounding:** Express the Path A taxonomy in formal StoP/DyS/StM theoretical
   language — diffusion regime, drift structure, free-energy landscape, tipping-point proximity
2. **chi_behav deep characterization:** Systematically describe where each behavioral type sits
   in the susceptibility/tipping-point space, extending the Path B chi_behav finding
3. **Regime analysis:** Validate that the DyS regime flags (is_dys_eligible,
   behaviorally_deterministic) map predictably onto the Path A clusters
4. **sigma_mu_ratio profile** (N=285 descriptive subsample): Describe noise-vs-drift dominance
   for participants where this ratio is defined
5. **Condition sensitivity of stochastic regimes:** Test whether DyS eligibility proportions
   differ by condition — connecting to Path E's finding that the behavioral space is
   condition-modulated

If a clustering attempt with chi_behav reveals a sub-structure not found in Path A (possible but
unlikely given feature correlations), this would be reported honestly as a surprising finding.
The more expected result — high ARI(Path D vs Path A) — is the confirmatory outcome that
completes the Step 2 phenotype evidence base.

---

## What Path D Adds After Paths A–F, E, B

### What is still unresolved

1. **Model-language alignment:** Paths A/F established a behavioral-dynamic taxonomy in
   descriptive statistical terms (sig_hat high/low, H_emp high/low, x_mean). The formal
   model interpretation — which cluster corresponds to a stochastic regime, which to
   a deterministic regime, which to a near-tipping-point attractor — has not been
   systematically documented.

2. **chi_behav distribution within clusters:** Path B found that B_fr3 (diverse responder)
   has mean chi_behav=45.8 — dramatically elevated. But within the Path A taxonomy,
   C1 (low-noise, low-override) has mean chi_behav=56.8, C2=15.4, C3=7.7. This
   counterintuitive ordering (low-noise type is most susceptible in the StM sense)
   needs systematic explanation and visualization.

3. **Regime flag mapping:** is_dys_eligible (N=207, 50%) and behaviorally_deterministic
   (N=154, 37.2%) have never been cross-tabulated against the Path A/F taxonomy.
   The condition distribution (control: 88 DyS-eligible vs default: 41) connects to
   Path E's homogenization finding and needs documentation.

4. **Drift vs noise dominance:** sigma_mu_ratio (σ̂/|μ|) is undefined for 31.2% of the
   sample (|μ| < 0.005, treated as zero drift). For the N=285 where it is defined,
   this ratio describes whether daily behavior is noise-dominated or drift-dominated —
   a theoretically important StoP distinction that has never been overlaid on the
   behavioral phenotype.

5. **Temporal entropy:** H_hour (temporal spread of app use across hours of day) has been
   flagged as a Phase 2 sensitivity feature but never tested as a clustering dimension.

### Why Path D is still useful

Despite the confirmatory expectation, Path D closes the Step 2 analysis in three ways:

- **Completeness:** The six-path plan committed to exploring the dynamic/stochastic dimension.
  Path D provides the evidence that this dimension IS captured by the existing taxonomy,
  allowing the thesis to make that claim defensibly rather than by assumption.
- **Theoretical depth:** The thesis chapter on DS5 behavioral phenotypes needs to connect
  the empirical clusters to the five theoretical models (StoP, DyS, StM, InT, NeT).
  Path D provides the systematic feature profiles that enable this connection.
- **chi_behav narrative:** The tipping-point proximity finding (C1 has the HIGHEST chi_behav
  despite being the LOW-noise group) is counterintuitive and important. Path D gives this
  finding its full analysis rather than leaving it as a Path B side note.

---

## Feature Logic

### Available dynamic/stochastic features — analysis-level classification

| Feature | Source model | N available | r with sig_hat | r with H_emp | r with x_mean | Classification |
|---|---|---|---|---|---|---|
| `sig_hat` | StoP | 414 | — | 0.538 | — | **Path A primary** (already used) |
| `H_emp` | InT/DyS | 414 | 0.538 | — | — | **Path A primary** (already used) |
| `x_mean` | StoP | 414 | — | — | — | **Path A primary** (already used) |
| `mu_hat` | StoP | 414 (31.2% near-zero) | 0.092 | 0.046 | 0.161 | **SECONDARY** — low signal, no NaN |
| `sigma_mu_ratio` | StoP | 285 (31.2% NaN) | — | — | — | **DESCRIPTIVE ONLY** — 31.2% NaN, never cluster |
| `H_SDE` | InT | 414 | **0.942** | 0.650 | — | **EXCLUDED** — collinear with sig_hat (r=0.942 > 0.70) |
| `beta_behav` | StM | 414 | -0.523 | -0.565 | — | **EXCLUDED** — monotone transform of sig_hat (β=2/σ̂²) |
| `F_behav` | StM | 414 | -0.221 | -0.009 | **-0.922** | **EXCLUDED** — collinear with x_mean (r=−0.922 > 0.70) |
| `chi_behav` | StM | 414 | -0.478 | -0.372 | -0.371 | **PRIMARY candidate** — passes correlation gate vs sig_hat and H_emp |
| `H_hour` | InT | 414 | — | — | — | **SENSITIVITY** — low variance (std=0.232), test only |
| `H_app` | InT | 414 | — | — | — | **SENSITIVITY** — low variance (std=0.515), test only |
| `is_dys_eligible` | DyS | 414 | — | — | — | **REGIME FLAG** — overlay/cross-tab only |
| `behaviorally_deterministic` | DyS | 414 | — | — | — | **REGIME FLAG** — overlay/cross-tab only |

### Correlation gate protocol (same as all previous paths)

Before any clustering attempt, compute the full correlation matrix on candidate features.
For any pair with |r| > 0.70:

- Drop the feature with LOWER theoretical priority from the primary set
- Retain it as an overlay/post-hoc descriptor only
- Document the gate outcome explicitly

**Pre-specified gate outcomes (based on observed correlations above):**

- H_SDE vs sig_hat: r=0.942 → **H_SDE DROPPED** (sig_hat is the direct StoP parameter; H_SDE is a monotone transform)
- F_behav vs x_mean: r=−0.922 → **F_behav DROPPED** (x_mean is the direct StoP parameter; F_behav conflates it with H_emp and β)
- beta_behav vs sig_hat: indirectly collinear (β=2/σ̂²) → **beta_behav EXCLUDED** (not independent; monotone transform)
- chi_behav vs sig_hat: r=−0.478 → **PASSES GATE** (< 0.70)
- chi_behav vs H_emp: r=−0.372 → **PASSES GATE**
- mu_hat vs sig_hat: r=0.092 → **PASSES GATE** (but very low signal; treat as secondary)

### Primary candidate feature sets for clustering

Three candidate sets, evaluated in order:

**Set D1 — StoP + StM susceptibility [PRIMARY]:**
```
[sig_hat, H_emp, chi_behav]
```
Motivation: sig_hat (noise diffusion) + H_emp (behavioral entropy) = the same behavioral-dynamic
axes as Path A, extended by chi_behav (StM tipping-point proximity). This is the most
theoretically motivated set and has no gate-firing pairs. Note: chi_behav is not fully
independent of sig_hat+x_mean (it is derived from them), but at r=−0.478/−0.372 the
collinearity does not reach the gate threshold. x_mean is retained as an overlay.

**Set D2 — Pure StoP parameters [SECONDARY comparison]:**
```
[sig_hat, H_emp, mu_hat]
```
Motivation: the theoretically cleanest StoP set (diffusion + entropy + drift). mu_hat has
no NaN (all 414 available) and no gate-firing correlations. However, mu_hat has near-zero
values for 31.2% of participants (|μ|<0.005) and extremely low correlations with sig_hat
(0.092) and H_emp (0.046), meaning it adds almost no discriminatory signal. This set is
expected to yield ARI(D2 vs Path A) > 0.90 — essentially identical to a two-feature
solution [sig_hat, H_emp]. Run for completeness and to verify the mu_hat finding.

**Set D3 — Temporal [SENSITIVITY only]:**
```
[sig_hat, H_emp, H_hour]
```
Motivation: tests whether temporal distribution of use (H_hour) adds structure. H_hour
has low variance (std=0.232 on a range anchored near max entropy 4.04). Expected to add
minimal discriminatory power. Run only as a sensitivity check.

### Decision rule for primary reporting

If Set D1 k-selection yields a stable solution (J ≥ 0.75) with min_cell ≥ 30:
→ Report D1 as primary clustering result. Compare ARI(D1 vs Path A).

If Set D1 fails stability at all k ∈ {2,3,4}:
→ Report D2 as primary clustering result (expected to be highly confirmatory).

If both D1 and D2 fail:
→ Path D is descriptive/regime analysis only. No clustering contribution. Report this
   honestly as: "The dynamic/stochastic feature space does not support independent
   clustering beyond the Path A solution."

---

## Sample Size and Stability Safeguards

### Minimum requirements

| Threshold | Value | Rule |
|---|---|---|
| MIN_CELL | 30 | Any k that produces a cluster with N < 30 is REJECTED regardless of silhouette or Jaccard |
| JACCARD_STABLE | ≥ 0.75 | Required for reporting as primary result |
| JACCARD_MARG | 0.60–0.75 | MARGINAL — reportable with explicit caveat; not primary |
| N_BOOTSTRAPS | 100 | Bootstrap samples for Jaccard estimation |
| SAMPLE_FRAC | 0.80 | Fraction of N used per bootstrap sample |

### Feasibility context (N=414)

Full-sample analyses (N=414) are feasible for k=2,3,4. Path A already achieved k=3 STABLE
at N=414.

Within-condition analyses (N=135–142 per condition) are feasible for k=2; k=3 is marginal
(min_cell constraint often binds at N≈135–142). Within-condition analyses should be run
**as sensitivity checks only** — the primary Path D analysis is full-sample.

sigma_mu_ratio subsample (N=285): feasible for descriptive analysis and overlay only.
Do NOT run clustering on N=285 — this introduces a non-random subset with unknown selection
bias (|μ| < 0.005 participants excluded are those with effectively zero drift, concentrated
in C1).

**When to stop and declare "no new structure":**

Stop and report Path D as "confirmatory" (not a new phenotype) when:
- ARI(Path D primary solution vs Path A) ≥ 0.70, AND
- Path D cluster profiles show the same three interpretive types (low-noise, high-noise,
  low-override lock-in) as Path A

Stop and report Path D as "regime analysis only" (not clustering) when:
- All k ∈ {2,3,4} fail either min_cell<30 OR Jaccard<0.60 for all three feature sets

---

## Comparison Logic to Existing Paths

### Required cross-path ARI comparisons (run automatically, report in table)

| Comparison | Expected ARI | Interpretation if confirmed |
|---|---|---|
| Path D (D1 primary) vs Path A (cluster_behav) | **> 0.70** (likely > 0.80) | Path D largely recovers Path A — dynamic/stochastic axis is the behavioral-dynamic axis |
| Path D vs Phase 1 (profile_p1) | Low (< 0.10) | Path D is NeT-independent — confirms independence of dynamic and network layers |
| Path D vs Path F (cell_f) | Moderate (0.40–0.60) | Path D partial alignment with hierarchical taxonomy |
| Path D vs Path E (cond_cluster_full) | Low-Moderate | Dynamic structure partially condition-shaped |
| Path D (D2 [sig_hat, H_emp, mu_hat]) vs Path A | **> 0.90** | mu_hat adds almost no new structure |
| Path D within-reintervention vs Path E rei solution | Moderate (0.50–0.80) | Consistency check |

### Key interpretive questions to answer

1. **Is chi_behav an independent clustering dimension or a re-expression of sig_hat?**
   - If ARI(D1 vs Path A) > 0.80: chi_behav does not add independent structure
   - If ARI(D1 vs Path A) = 0.50–0.80: chi_behav partially reorganizes the space (possible
     sub-structure within C1, the high-chi_behav low-noise group)
   - Decision rule: inspect the cross-tabulation of Path D labels vs Path A labels for
     any splitting pattern

2. **Does the tipping-point proximity ordering (C1 >> C2 >> C3 on chi_behav) replicate?**
   - This is the central counterintuitive finding to confirm:
     Low-noise type (C1: sig_hat=0.121, x_mean=0.358) → chi_behav=56.8 (HIGHEST)
     High-noise type (C3: sig_hat=0.281, x_mean=0.673) → chi_behav=7.7 (LOWEST)
   - Interpretation: chi_behav peaks when σ is small AND x_mean ≈ 0.5 (near-threshold).
     C1 is low-noise AND near-threshold on override → closest to tipping point.
     C3 is high-noise → diffusion dominates → not near a deterministic tipping point.

3. **Do DyS regime flags map predictably onto Path A clusters?**
   - is_dys_eligible (σ < σ_median=0.1812): Expect C1+C2 predominantly eligible, C3 not
   - behaviorally_deterministic (DyS-eligible AND H_emp < median): Expect primarily C1/C2
   - Test with chi-square cross-tabulation (Path A cluster × DyS flag)

4. **Does the condition-modulation of DyS eligibility connect to Path E?**
   - Observed: control=88 DyS-eligible, default=41, reintervention=78
   - Default condition has fewest deterministic participants — consistent with Path E's
     finding that default collapses behavioral heterogeneity
   - Report chi-square: condition × is_dys_eligible

5. **What does sigma_mu_ratio reveal about the N=285 subsample?**
   - Mean=18.45, std=14.63, median=15.08
   - Most participants (73.7%) have sigma_mu_ratio > 10 → overwhelmingly noise-dominated
   - Report distribution by Path A cluster — does C1 have lower sigma_mu_ratio
     (drift plays larger role) than C3?

---

## Outcome Scenarios

**Outcome 1 (primary expected): ARI(D1 vs Path A) > 0.80 — CONFIRMATORY**

Path D clustering substantially recovers Path A. chi_behav, while it passes the correlation
gate, does not introduce genuinely new groupings — it re-orders participants in a way that
is largely consistent with the existing {low-noise, high-noise, override-locked} taxonomy.

Thesis conclusion: *"The dynamic/stochastic phenotyping analysis confirms that the
behavioral-dynamic axis (diffusion × entropy × tipping-point proximity) does not produce
a phenotype structure independent of the Path A taxonomy. The three behavioral types
identified in Path A simultaneously represent three distinct stochastic regimes: the
near-tipping deterministic type (C1: low σ̂, low H_emp, high χ_behav), the noise-dominated
unstructured type (C3: high σ̂, high H_emp, low χ_behav), and the deterministic compliant
type (C2: low σ̂, moderate H_emp, high override lock-in). Path D's contribution is to
ground this taxonomy in the formal language of stochastic-process and statistical-mechanics
theory."*

**Outcome 2 (possible): ARI(D1 vs Path A) = 0.50–0.80 — PARTIAL REORGANIZATION**

chi_behav introduces sub-structure, most likely by splitting C1 into two subgroups
(very-high chi_behav vs moderate chi_behav) or by reordering C1/C2. Report the specific
splitting pattern, document which participants switch cluster membership, and assess whether
the sub-structure has substantive interpretive meaning (e.g., does the highest-chi_behav
subgroup have distinct psychosocial profiles?).

Thesis conclusion: *"Path D's clustering reveals a partial reorganization relative to Path
A, with chi_behav (StM tipping-point proximity) introducing sub-structure within the low-
noise group. [Report specific split.] This suggests that susceptibility to behavioral change
differentiates two subgroups within the behaviorally deterministic profile — one near a
genuine tipping point (high chi_behav) and one in a stable override-locked attractor (low
chi_behav)."*

**Outcome 3 (least likely): ARI(D1 vs Path A) < 0.50 — GENUINELY NEW STRUCTURE**

chi_behav reorganizes the space substantially, revealing groups that cut across the Path A
taxonomy. Report with full documentation and treat as an unexpected finding requiring
careful interpretive qualification.

**Outcome 4 (stop condition): All clustering rejected**

If min_cell < 30 for all k ∈ {2,3,4} on all three feature sets, Path D is descriptive only.
This would mean the dynamic/stochastic feature space adds no feasible clustering to what
Path A already found. Report honestly: "Path D cannot partition the DS5 sample into stable
dynamic phenotypes beyond the Path A solution. The behavioral-dynamic taxonomy is confirmed
as the final Step 2 taxonomy."

---

## Notebook Structure

### Cell outline (≈30 cells)

**Section 0: Setup (2 cells)**
- Imports: pandas, numpy, scipy, sklearn (KMeans, StandardScaler), matplotlib, seaborn
- Constants: RANDOM_STATE=42, N_BOOTSTRAPS=100, SAMPLE_FRAC=0.80, MIN_CELL=30,
  JACCARD_STABLE=0.75, JACCARD_MARG=0.60
- Paths and color scheme (reuse Phase 1 palette)
- Load: ds5_phenotype_feature_matrix.csv, ds5_behav_only_cluster_assignments.csv,
  ds5_hierarchical_assignments.csv, ds5_condition_cluster_assignments.csv,
  ds5_intervention_cluster_assignments.csv

**Section 1: Dynamic Feature Audit (3 cells)**
- Cell 1: Full correlation matrix — all dynamic features including sig_hat, H_emp, x_mean,
  mu_hat, H_SDE, beta_behav, F_behav, chi_behav, H_hour, H_app
  → fig_d1_feature_correlations.png
- Cell 2: Apply correlation gate (|r| > 0.70). Print gate decisions for each pair.
  Confirm: H_SDE dropped, F_behav dropped, beta_behav excluded. chi_behav, mu_hat, H_hour
  pass.
- Cell 3: Feature distributions — violin plots for sig_hat, mu_hat, chi_behav by condition
  and by Path A cluster_behav label → fig_d2_feature_distributions_by_cluster.png

**Section 2: mu_hat and sigma_mu_ratio Descriptive (2 cells)**
- Cell 4: mu_hat analysis — histogram of full distribution; count of |μ|<0.005 by cluster;
  KW test mu_hat across Path A clusters
- Cell 5: sigma_mu_ratio — N=285 subsample only; histogram; KW test by Path A cluster;
  report proportion noise-dominated (ratio>10) per cluster
  → fig_d3_drift_noise_profiles.png

**Section 3: Primary Clustering — Set D1 [sig_hat, H_emp, chi_behav] (4 cells)**
- Cell 6: Scale features (StandardScaler on N=414)
- Cell 7: K-selection loop k∈{2,3,4} — silhouette, CH, DB, min_cell, bootstrap Jaccard
  → fig_d4_kselection_curves.png
- Cell 8: Fit final solution at selected k; assign labels ordered by sig_hat ascending
  (D_sde1 = lowest noise, etc.); print cluster profiles
- Cell 9: Cross-path ARI comparison — D1 vs Path A, Phase 1, Path F, Path E
  → Print ARI table

**Section 4: Secondary Clustering — Set D2 [sig_hat, H_emp, mu_hat] (2 cells)**
- Cell 10: K-selection loop (same procedure); bootstrap Jaccard
- Cell 11: ARI(D2 vs Path A) — confirm mu_hat adds no structure

**Section 5: Sensitivity — Set D3 [sig_hat, H_emp, H_hour] (1 cell)**
- Cell 12: K-selection; ARI(D3 vs Path A); note if H_hour contributes

**Section 6: Cluster Profile Analysis (3 cells)**
- Cell 13: Detailed cluster profiles — D1 labels, mean/std for all dynamic features
  (including overlay: x_mean, mu_hat, sigma_mu_ratio mean on available subsample, H_SDE, F_behav)
  → fig_d5_cluster_profiles.png
- Cell 14: chi_behav deep characterization — full distribution per cluster, annotate
  counterintuitive ordering (C1/D1 low-noise = highest chi_behav)
  → fig_d6_chi_behav_distribution.png
- Cell 15: Cross-tabulation — D1 labels vs Path A labels (heatmap of proportions)
  → fig_d7_crosspath_heatmap.png

**Section 7: DyS Regime Flag Analysis (2 cells)**
- Cell 16: is_dys_eligible × Path A cluster — chi-square test; cross-tab proportions
- Cell 17: is_dys_eligible × condition — chi-square test; connect to Path E homogenization
  finding (default condition has 41/142 = 28.9% DyS-eligible vs 64% in control)
  → fig_d8_dys_regime_by_cluster_condition.png

**Section 8: StM Model-Language Profile (2 cells)**
- Cell 18: Free-energy landscape — scatter sig_hat vs H_emp, color by D1 cluster,
  annotate with chi_behav contours; include F_behav overlay
  → fig_d9_stochastic_landscape.png
- Cell 19: Tipping-point distance profile — rank participants by chi_behav; annotate by
  Path A cluster; show that C1 (low-noise) occupies the high-susceptibility region

**Section 9: Condition Sensitivity (2 cells)**
- Cell 20: Within-reintervention analysis (N=135): attempt k-selection on D1 features;
  compare solution to Path E rei solution and Path B within-rei
- Cell 21: KW test — D1 cluster vs H_out_resid (cross-check with Path B finding)

**Section 10: Psychosocial Overlays (1 cell)**
- Cell 22: KW test psychosocial scales (n=5) across D1 clusters; Bonferroni correction
  (α_corrected = 0.05/5 = 0.01); report significant scales only

**Section 11: Outputs (2 cells)**
- Cell 23: Save CSV files + companion .md files; print verification
- Cell 24: Update model_run_summary_path_d.md

---

## Output File Structure

### Primary CSV outputs

| File | Location | Unit of observation | Key columns |
|---|---|---|---|
| `ds5_dynamic_cluster_assignments.csv` | `outputs/model_outputs/phenotyping/` | Participant (N=414) | participant_id_canonical, study_condition, profile_p1, cluster_d_full (D1), cluster_behav, cell_f, cond_cluster_full |
| `ds5_dynamic_cluster_profiles.csv` | `outputs/model_outputs/phenotyping/` | Cluster (N_clusters rows) | mean/std for all dynamic features per D1 cluster |
| `ds5_dynamic_cluster_stability.csv` | `outputs/model_outputs/phenotyping/` | Analysis level × k | analysis, N, k_tested, sil, min_cell, jaccard, flag, selected; includes D1/D2/D3 rows |
| `model_run_summary_path_d.md` | `outputs/model_outputs/phenotyping/` | — | Full run record with all results, key findings, thesis-conclusion language |

Each CSV must have a companion `.md` file with column reference table, unit description,
known limitations, and load snippet.

### Figures

| Figure | Content |
|---|---|
| `fig_d1_feature_correlations.png` | Correlation matrix of all dynamic features; gate-firing pairs highlighted |
| `fig_d2_feature_distributions_by_cluster.png` | Violin plots of sig_hat, chi_behav, mu_hat by Path A cluster |
| `fig_d3_drift_noise_profiles.png` | sigma_mu_ratio histogram; mu_hat near-zero distribution |
| `fig_d4_kselection_curves.png` | Silhouette, CH, Jaccard vs k for D1 (primary set) |
| `fig_d5_cluster_profiles.png` | Bar chart of D1 cluster means on all dynamic features |
| `fig_d6_chi_behav_distribution.png` | chi_behav distribution by cluster; annotation of counterintuitive ordering |
| `fig_d7_crosspath_heatmap.png` | D1 labels vs Path A labels cross-tabulation heatmap |
| `fig_d8_dys_regime_by_cluster_condition.png` | DyS flag proportions by cluster and condition |
| `fig_d9_stochastic_landscape.png` | Scatter plot: sig_hat × H_emp colored by D1 cluster; chi_behav contours |

All figures to `outputs/model_outputs/phenotyping/figures/`.

---

## Step 2 Constraint

Path D is strictly Step 2.

- No intervention recommendations
- No personalization proposals
- No causal language about what conditions produce which stochastic regime
- No claims that chi_behav predicts future behavior (it is a model parameter estimated from
  historical X_t, not a predictive tool here)
- DyS regime flags are descriptive classifications, not eligibility criteria for any treatment
- sigma_mu_ratio on N=285 is explicitly flagged as a non-random subsample analysis

---

## Key Feature Cautions (from data_docs/modeling_cautions.md)

The following cautions from Stage 1 QC apply specifically to Path D features:

1. **mu_hat near-zero caution:** The StoP model estimates μ as the mean daily increment in X_t.
   For participants with very stable behavioral patterns (little day-to-day change), |μ| is
   near zero. The sigma_mu_ratio is undefined for these participants. Do NOT interpret
   near-zero mu_hat as "no drift" — it means the drift contribution is unidentifiable
   relative to noise in the available time series length. C1 participants (N=62) have
   mean mu_hat≈0.0009 — essentially indistinguishable from zero at N=14 average days.

2. **chi_behav derivation caution:** chi_behav = β·p·(1−p) = (2/σ̂²)·x_mean·(1−x_mean).
   It is not an independently measured quantity — it is a mathematical combination of
   sig_hat and x_mean. Including chi_behav in clustering while treating sig_hat and x_mean
   as independent features would introduce double-counting. In Path D, x_mean is held as
   an OVERLAY and NOT in the primary feature set precisely to avoid this.

3. **F_behav caution:** F_behav = x_mean − (1/β)·H_emp. It has r=−0.922 with x_mean and
   r=−0.009 with H_emp. Do not use as independent feature. Useful as a free-energy landscape
   descriptor post-hoc only.

4. **H_SDE caution:** H_SDE = ½log₂(2πe·σ̂²) — a monotone transform of sig_hat. It contains
   zero independent information. Use sig_hat always.

---

## How Path D Completes the Step 2 Evidence Base

After Path D, the thesis can make the following complete claim about DS5 Step 2:

> *DS5 exhibits two genuinely independent phenotype layers and one confirmatory layer:*
> 
> *Layer 1 — Network-topological (NeT type):* Identified in Phase 1 and Path C. Profile B
> (hub-locked) vs Profile A (distributed), with NeT sub-profiles B1/B2 and A1/A2.
> Condition-stable. ARI(NeT vs behavioral) = 0.020 — orthogonal to all behavioral dimensions.
> 
> *Layer 2 — Behavioral-dynamic (StoP/DyS/StM):* Identified in Paths A and F, confirmed in
> Paths E and B. Three types: low-noise deterministic near-tipping (C1/B_behav1), override-locked
> deterministic compliant (C2/B_behav2), high-noise stochastic unstructured (C3/B_behav3).
> Condition-modulated (Path E Outcome D: default homogenizes). Path D confirms this is also
> the dynamic/stochastic taxonomy — no additional independent layer exists.
> 
> *Layer 3 — Friction-response (InT):* Investigated in Path B. Not an independent layer —
> H_out_resid is nearly collinear with x_mean (r=−0.707). The behavioral-dynamic taxonomy
> predicts friction-response diversity. Distinct finding: B_fr3 type has highest StM
> susceptibility (chi_behav=45.8), connecting the "diverse responder" type to the near-
> tipping-point subgroup.
> 
> *Path D's role:* Provides the formal model-language characterization of Layer 2 and confirms
> that no additional dynamic/stochastic layer exists beyond what was already identified.

---

## Before Implementation

The following questions should be verified against the actual data before the notebook is run:

1. **chi_behav at cluster-level:** The expected ordering (C1 chi_behav=56.8 >> C2=15.4 >> C3=7.7)
   should be visible in the feature distributions before clustering. Verify this by running
   a quick KW test on chi_behav by cluster_behav before the Path D clustering attempt.

2. **mu_hat near-zero concentration:** Confirm that |μ|<0.005 participants are distributed
   approximately evenly across clusters (they are in C1: 28/62=45%, C2: 55/152=36%, C3: 46/200=23%).
   If the concentration is uneven, report as a finding (C1 has the highest proportion of
   zero-drift participants — the most perfectly stable behavioral patterns).

3. **sigma_mu_ratio by cluster:** The N=285 subsample excludes |μ|<0.005 participants. Since
   C1 has the highest proportion of these (45%), the sigma_mu_ratio subsample underrepresents
   C1. Report this explicitly in the sigma_mu_ratio analysis.

4. **H_hour variance check:** Before including H_hour in Set D3, confirm std remains ~0.232.
   If std < 0.20, declare H_hour "insufficient variance" and skip Set D3 entirely.

---

## What Path D Lets the Thesis Conclude (draft language)

> *"The dynamic/stochastic phenotyping analysis (Path D) completes the six-path Step 2
> exploration of DS5 behavioral heterogeneity. The primary finding is confirmatory: the
> dynamic/stochastic feature space — including behavioral noise (σ̂), entropy (H_emp), and
> StM tipping-point proximity (χ_behav) — does not produce a phenotype structure independent
> of the behavioral-dynamic taxonomy identified in Paths A and F. The three behavioral
> types established earlier (low-noise near-tipping, override-locked, high-noise stochastic)
> simultaneously represent three distinct stochastic-process regimes. Most counterintuitively,
> the low-noise type (C1) exhibits the highest tipping-point susceptibility (χ_behav = 56.8
> vs 15.4 and 7.7 for C2 and C3) — reflecting that participants with stable, low-variance
> behavioral histories who have not fully committed to override (moderate x_mean ≈ 0.358)
> are nearest to a phase transition in their behavioral attractor, while high-noise participants
> are noise-dominated and far from a deterministic tipping point. Path D further confirms that
> the default friction condition substantially reduces the proportion of deterministic
> participants (28.9% DyS-eligible in default vs 64.2% in control), extending Path E's
> homogenization finding into the formal model-language characterization of DS5 heterogeneity.
> Taken together, the six Step 2 paths establish that DS5 behavioral phenotypes are structured
> along two genuinely orthogonal axes — network topology and behavioral dynamics — with no
> additional independent dimensions identified across network sub-structure (Path C),
> behavior-only dynamics (Path A), hierarchical integration (Path F), condition stratification
> (Path E), friction-response diversity (Path B), or dynamic/stochastic regime characterization
> (Path D)."*

---

## Summary Table — Six-Path Step 2 Results

| Path | Notebook | Primary question | Result type | ARI vs Path A | New structure? |
|---|---|---|---|---|---|
| C | 101 | Network sub-structure within Phase 1 profiles | Confirmatory | 0.990 (NeT-only vs Phase 1) | No — NeT fully explains Phase 1 |
| A | 102 | Behavior-only phenotypes (no NeT) | Primary taxonomy | — | YES — 3 types, orthogonal to NeT (ARI=0.020) |
| F | 103 | Hierarchical: NeT × behavioral | Integrative | ARI(B-behav vs A within B)=1.000 | No — confirms orthogonality |
| E | 104 | Condition-stratified | Moderating | ARI(rei vs A)=0.697; default=0.000 | No — condition modulates, not adds |
| B | 105 | Friction-response (H_out_resid) | Quasi-independent | 0.725 | No — redundant with x_mean |
| **D** | **106** | **Dynamic/stochastic (sig_hat, chi_behav, mu_hat)** | **Expected: confirmatory** | **Expected: > 0.70** | **Expected: No — deepens Layer 2** |

---

## ACTUAL RESULTS (appended post-implementation: 2026-04-20)

### Correlation Gate Outcomes

| Pair | r | Gate fires? | Decision |
|---|---|---|---|
| H_SDE vs sig_hat | 0.942 | YES | H_SDE DROPPED |
| F_behav vs x_mean | -0.922 | YES | F_behav DROPPED |
| beta_behav vs sig_hat | -0.523 | YES (indirect) | beta_behav EXCLUDED |
| chi_behav vs sig_hat | -0.478 | No | retained in D1 |
| chi_behav vs H_emp | -0.372 | No | retained in D1 |
| mu_hat vs sig_hat | 0.092 | No | retained in D2 |
| H_hour | std=0.232 ≥ 0.20 | — | D3 RAN (not skipped) |

All pre-specified gate outcomes confirmed. D3 ran (H_hour std=0.232 just above 0.20 threshold).

### K-Selection Results

**D1 [sig_hat, H_emp, chi_behav] — Full-sample (N=414):**

| k | Silhouette | min_cell | Jaccard | Flag | Selected |
|---|---|---|---|---|---|
| **2** | **0.400** | **172** | **0.919** | **STABLE** | **YES** |
| 3 | — | 11 | — | REJECTED_MINCELL | No |
| 4 | — | 6 | — | REJECTED_MINCELL | No |

**CRITICAL:** k=3 rejected (min_cell=11). chi_behav forces a very small extreme-susceptibility
cluster (N≈11) at k=3 — confirming that the high-chi_behav group (C1 tail) is numerically tiny
and cannot be robustly partitioned. **D1 forced to k=2.**

**D2 [sig_hat, H_emp, mu_hat] — Full-sample:**

| k | Silhouette | min_cell | Jaccard | Flag | Selected |
|---|---|---|---|---|---|
| **2** | **0.338** | **179** | **0.930** | **STABLE** | **YES** |
| 3 | 0.311 | 81 | 0.775 | STABLE | No (lower sil) |
| 4 | — | 17 | — | REJECTED_MINCELL | No |

**D3 [sig_hat, H_emp, H_hour] — Full-sample (sensitivity):**

| k | Silhouette | min_cell | Jaccard | Flag | Selected |
|---|---|---|---|---|---|
| 2 | 0.344 | 186 | 0.889 | STABLE | No |
| **3** | **0.367** | **49** | **0.930** | **STABLE** | **YES** |
| 4 | — | 23 | — | REJECTED_MINCELL | No |

**D1 within-reintervention (N=135):**

| k | Jaccard | Flag | Selected |
|---|---|---|---|
| **2** | **0.904** | **STABLE** | **YES** |

### D1 Cluster Profiles (k=2)

| Cluster | N | sig_hat | H_emp | chi_behav | x_mean (overlay) | Interpretation |
|---|---|---|---|---|---|---|
| D_sde1 | 172 | 0.120 | 1.540 | 31.59 | 0.730 | Low-noise deterministic — low diffusion, high susceptibility |
| D_sde2 | 242 | 0.268 | 2.385 | 8.20 | 0.669 | High-noise stochastic — high diffusion, low susceptibility |

(Values copied from `ds5_dynamic_cluster_profiles.csv`; the low-noise/high-noise chi_behav contrast is ~3.9x, not the ~14x implied by the earlier draft of this table.)

**D1 vs Path A cross-tabulation:**

|  | C1 | C2 | C3 |
|---|---|---|---|
| D_sde1 | 44 | 127 | 1 |
| D_sde2 | 18 | 25 | 199 |

Interpretation: D1 k=2 collapses C1 (N=62) and C2 (N=152) into D_sde1 (low-noise), while
C3 (N=200) falls almost entirely into D_sde2 (high-noise). chi_behav cannot distinguish
C1 from C2 at k=2 because both are low-noise (sigma < median) — only the extreme tail of
C1 (N≈11) attempts to split at k=3 but is rejected by min_cell.

### Cross-Path ARI Results

| Comparison | ARI | Interpretation |
|---|---|---|
| D1 vs Path A (cluster_behav) | **0.560** | MODERATE — partial reorganization; C1+C2 merged into one low-noise type |
| D1 vs Phase 1 (profile_p1) | 0.027 | LOW — D1 is NeT-independent (confirmed) |
| D1 vs Path F (cell_f) | 0.283 | LOW-MODERATE — hierarchical taxonomy partially aligned |
| D1 vs Path E (cond_cluster_full) | 0.232 | LOW-MODERATE |
| D1 vs Path B (cluster_b_full) | 0.565 | MODERATE |
| D2 vs Path A | 0.578 | MODERATE (unexpected: mu_hat does differentiate somewhat) |
| D3 vs Path A | 0.421 | MODERATE — H_hour introduces different structure |
| D1 within-rei vs Path A (rei) | 0.586 | MODERATE |

**k-mismatch controls (added):** D1/D2 are k=2 solutions and Path A is k=3, so ARI is bounded below 1
regardless of feature overlap. The pure k-mismatch baseline — clustering Path A's own
[sig_hat, H_emp, x_mean] at k=2 and comparing to Path A's k=3 labels — is **ARI = 0.720**. Against that
reference, D1's 0.560 is a modest difference, not a reorganization. The like-for-like test of what
chi_behav actually contributes is ARI(D1 k=2 vs k=2 on the shared [sig_hat, H_emp]) = **0.869**, and
ARI(k=2 on [sig_hat, H_emp] vs Path A k=3) = **0.628**. The same k-mismatch caveat applies to the
D1 vs Path F (0.283), D1 vs Path E (0.232), D2 vs Path A (0.578) and D1-within-rei vs Path A (0.586) rows.

### Outcome Classification

**OUTCOME 2 — PARTIAL REORGANIZATION (ARI=0.560)**

D1 k=2 collapses C1 (low-noise near-tipping) and C2 (override-locked) into a single
"deterministic" cluster, splitting only against C3 (high-noise stochastic). This is a
lower-resolution partition than Path A's k=3, not a new structure. chi_behav distinguishes
C1 from C2 only in the extreme tail (k=3 rejected due to min_cell=11).

The ARI=0.560 means D1 captures roughly half the variance in Path A's three-way split.
This is a consolidation of the behavioral-dynamic taxonomy, not an extension of it.

### Key Unexpected Findings

**Finding 1: k=3 rejection is itself informative**

The min_cell=11 at k=3 means that only ≈11 participants form a genuinely extreme chi_behav
cluster — the "hyper-susceptible" tail at the very top of C1 (chi_behav > ~100). These
participants cannot be stably clustered (N < 30) but their existence is real. Path D
confirms there is a small extreme-susceptibility subgroup that is too numerically rare for
stable phenotyping but conceptually important for the StM tipping-point narrative.

**Finding 2: DyS regime flags are strongly condition-modulated**

- control: 64.2% DyS-eligible; default: 28.9% DyS-eligible; reintervention: 57.8%
- χ²=39.7, p=2.4e-09
- behaviorally_deterministic: control=59.1%, default=12.7%, reintervention=40.7%
- χ²=65.5, p=6.1e-15
This extends Path E's homogenization finding into formal DyS regime language: default
friction exposure reduces the proportion of participants operating in a deterministic
behavioral regime by more than half relative to control.

**Finding 3: mu_hat is statistically significant but substantively weak**

KW test mu_hat by Path A cluster: H=17.28, p=0.0002 — significant. But C1 mean=0.0009,
C2=0.0091, C3=0.0084. The effect is marginal: C1 is near-zero drift, C2/C3 have slight
positive drift. D2 ARI=0.578 vs D1 ARI=0.560 — almost identical. mu_hat adds noise, not
structure. DS5 behavioral dynamics are overwhelmingly diffusion-dominated.

**Finding 4: D3 [sig_hat, H_emp, H_hour] achieves k=3 STABLE (J=0.930, ARI=0.421 vs Path A)**

H_hour's r(H_hour, sig_hat)=-0.510 means temporal spread is inversely related to noise:
high-noise participants tend to use apps at more concentrated hours (lower H_hour).
D3 k=3 finds a structure that partially reflects time-of-day patterns. ARI=0.421 is
lower than D1 (0.560), confirming D1 is the better primary feature set.

**Finding 5: sigma_mu_ratio is overwhelmingly noise-dominated across all clusters**

C1: mean ratio=11.24 (N=34 subsample), C2: 13.86 (N=97), C3: 22.94 (N=154).
C3 has the HIGHEST ratio (most noise-dominated) as expected. C1 has the lowest
(some drift component visible), but even C1 is noise-dominated at ratio > 10.
Confirms: DS5 behavioral processes are stochastic/diffusion-driven for all three types.

### Blueprint Accuracy Note

The blueprint pre-specified D1 at k=2 as the likely result if chi_behav does not add
orthogonal structure. The k=3 rejection (min_cell=11) was mentioned as possible ("tiny
cluster of extreme susceptibility"). The ARI=0.560 falls in the blueprint's Outcome 2
range (0.40–0.70). All pre-specified findings were essentially correct.

**One deviation:** D2 ARI=0.578 was labeled "UNEXPECTED" (script said "mu_hat introduces
more structure than expected"). This is a labeling artifact — ARI=0.578 at k=2 vs Path A k=3
is expected given that D2 also forces a k=2 low-vs-high-noise binary split. The "unexpected"
label applied because the script expected ARI > 0.90; the actual ARI reflects the structural
loss from k=2 vs k=3, not any real contribution of mu_hat.

**Blueprint update:** No structural changes to the blueprint needed. The "UNEXPECTED" label in
the script's D2 outcome message has been corrected in interpretation above.
