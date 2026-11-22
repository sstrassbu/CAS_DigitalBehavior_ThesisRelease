# DS5 Step 2 — Phenotyping Blueprint

**Notebook:** `100_phenotype_exploration.ipynb`  
**Written:** 2026-04-18  
**Stage:** Stage 4, Step 2 — Phenotyping and Behavioral Subgroup Discovery  
**Dataset:** DS5 — German adolescents RCT, N=573 (414 StoP-eligible; 463 NeT-eligible)  
**Purpose:** Master planning document for the DS5 phenotyping notebook. Read this before writing
any code. Do not implement the notebook until this blueprint is confirmed.

---

## 0. The boundary between Step 2 and Step 3

**Step 2 (this notebook):** Use the completed Step 1 model parameters as features for
behavioral subgroup discovery. Describe who differs from whom and along which dimensions.
No intervention fitting. No prescriptive recommendations. No "this group should receive X
friction type." Cautious labels only.

**Step 3 (not this notebook):** Use Step 2 phenotype profiles to ask: which phenotype
responds best to which friction type? DS5 is the correct first Step 3 dataset because
condition assignment was experimental. Step 3 is not started here.

**Transition signal:** A Step 2 notebook becomes Step 3 the moment it predicts an optimal
friction strategy per user or prescribes an intervention. Avoid this.

---

## 1. Why phenotyping now — and what the paper asks for

The paper's roadmap (§6.1) defines three consecutive levels:

1. Theoretical and Conceptual Modeling — **complete** (DS5 Step 1)
2. Phenotyping and understanding behavioral heterogeneity — **this step**
3. Applied personalization and intervention fitting — Step 3 (later)

The paper's §4.3 explicitly identifies the following phenotype dimensions as central to the
CAS multi-model framework:

| Paper phenotype dimension | What it maps to in Step 1 output |
|---|---|
| Friction sensitivity | x_mean (override level), H_out (outcome uncertainty) |
| Habitual stability / attractor strength | is_dys_eligible, behaviorally_deterministic, rho_self |
| Impulsivity / noise dominance | sig_hat, sigma_mu_ratio |
| Threshold dependence | chi_behav (susceptibility near tipping point) |
| Context dependence | H_hour (temporal spread) |
| Adaptation over repeated exposure | mu_hat (drift), open_rate_change (Stage 1 feature) |
| Override tendency | x_mean, rho_self |
| Substitution tendency | H_trans, I_consec |
| Network centralization / hub dependence | HHI_net, top1_share_net |
| Feedback-loop dominance | F_behav (free energy analog, partially) |

Step 2's task is to operationalize these dimensions using the completed Step 1 outputs,
discover whether meaningful behavioral subgroups exist in DS5, and describe them carefully
without overclaiming.

---

## 2. Full feature inventory from all five DS5 Step 1 model outputs

### 2.1 StoP — `outputs/model_outputs/stochastic_processes/participant_parameters.csv`

| Column | Type | Description |
|---|---|---|
| `mu_hat` | float | Behavioral drift (mean daily increment in X_t) |
| `sig_hat` | float | Behavioral diffusion (day-to-day variability in X_t) |
| `sigma_mu_ratio` | float | Impulsivity ratio σ/\|μ\|; 31.2% NaN (undefined for \|μ\| < 0.005) |
| `x_mean` | float | Mean daily override rate (time-average of X_t) |
| `n_days` | int | Number of eligible days for this participant |
| `study_condition` | str | Experimental condition (control/default/reintervention) |

### 2.2 InT — `outputs/model_outputs/information_theory/participant_entropy_metrics.csv`

| Column | Type | Description |
|---|---|---|
| `H_out` | float | Entropy of friction outcome distribution (opened/dismissed/closed) |
| `H_app` | float | Entropy of app distribution (app diversity across friction events) |
| `H_hour` | float | Entropy of hour-of-day distribution (temporal spread) |
| `H_emp` | float | Empirical entropy of daily X_t distribution (K=10 bins) |
| `H_SDE` | float | Gaussian differential entropy prediction = ½ log₂(2πeσ̂²); monotone transform of sig_hat |
| `sig_hat` | float | Carries over from StoP; same value |

### 2.3 DyS — `outputs/model_outputs/dynamical_systems/participant_dynamics_parameters.csv`

| Column | Type | Description |
|---|---|---|
| `is_dys_eligible` | bool | σ̂ < σ_median (0.1812); binarization of sig_hat |
| `regime_label` | str | "DyS-deterministic" / "StoP-stochastic" |
| `predicted_boundary_fp` | str | "upper" (μ̂>0) or "lower" (μ̂<0) |
| `deviation_from_predicted_fixed_point` | float | \|x_mean − predicted boundary\| |
| `behaviorally_deterministic` | bool | is_dys_eligible AND H_emp < H_emp_median |
| `H_emp` | float | Same as InT |
| `H_SDE` | float | Same as InT |

### 2.4 StM — `outputs/model_outputs/statistical_mechanics/participant_stm_parameters.csv`

| Column | Type | Description |
|---|---|---|
| `beta_behav` | float | Behavioral inverse temperature = 2/σ̂²; monotone transform of sig_hat |
| `T_behav` | float | Behavioral temperature = σ̂²/2; monotone transform of sig_hat |
| `p_use_approx` | float | ≈ x_mean (proportion of days X_t > 0.5); near-duplicate |
| `chi_behav` | float | Behavioral susceptibility = β·p·(1−p); partially new via p_use |
| `F_behav` | float | Free energy analog = E_use − (1/β)·H_emp; combines sig_hat + H_emp |
| `H_StM_participant` | float | Entropy from KDE of empirical X_t; correlates with H_SDE |
| `four_model_convergent` | bool | Low σ̂ AND low H_emp (effectively = behaviorally_deterministic) |
| `behavioral_regime` | str | "ordered" / "exploratory" / etc. |
| `high_chi` | bool | χ_behav above median; intervention sensitivity flag |

### 2.5 NeT — `outputs/model_outputs/network_models/participant_network_metrics.csv`

| Column | Type | Description |
|---|---|---|
| `HHI_net` | float | Network Herfindahl index; flow concentration across apps |
| `top1_share_net` | float | Share of dominant app in total transitions |
| `top3_share_net` | float | Share of top-3 apps in total transitions |
| `rho_self` | float | Self-loop rate; same-app repetition in consecutive events |
| `H_trans` | float | Transition entropy (source-weighted conditional entropy of T_ij) |
| `H_pi` | float | Stationary distribution entropy (only 378 eligible, 66.4%) |
| `I_consec` | float | Mutual information I(app_t; app_t+1) = H_app − H_trans |
| `H_app` | float | App entropy (same as InT — both drawn from same source) |
| `is_net_eligible` | bool | M ≥ 20 transitions |
| `is_stationary_eligible` | bool | M ≥ 50 AND ergodic transition matrix |

---

## 3. Feature classification — redundancy, independence, and clustering role

### 3.1 The core independence finding

Before assigning features to clustering, the key fact from `ds5_four_model_cluster_summary.md`
must be applied:

> **Within the StoP↔InT↔DyS↔StM cluster, the only genuinely independent empirical axes are
> σ̂ (sig_hat) and H_emp. Everything else either derives from σ̂ or from x_mean.**

This means:
- β_behav = 2/σ̂² → SAME as sig_hat, opposite direction
- T_behav = σ̂²/2 → SAME as sig_hat
- H_SDE = ½ log₂(2πeσ̂²) → SAME as sig_hat
- is_dys_eligible = (sig_hat < median) → BINARIZATION of sig_hat
- four_model_convergent = (low sig_hat AND low H_emp) → COMPOSITE of the two independent axes

**NeT adds genuinely new axes** not derivable from sig_hat or H_emp:
- HHI_net: flow concentration in the app-transition network
- rho_self: same-app self-transition dominance
- H_trans: conditional transition entropy

**InT adds partially new axes** beyond H_emp:
- H_out: friction outcome uncertainty (independent but condition-confounded ⚠)
- H_app: app diversity (independent; reframing of a Stage 1 feature)
- H_hour: temporal diversity (independent)

**I_consec is NOT independent** of H_app and H_trans — it is their difference
(I_consec = H_app − H_trans). Using all three simultaneously is redundant.

---

### 3.2 Feature classification table

| Feature | Classification | Rationale |
|---|---|---|
| `sig_hat` | **CORE CLUSTERING** | StoP backbone; independent; represents impulsivity/noise dimension |
| `H_emp` | **CORE CLUSTERING** | InT backbone; partially independent of sig_hat (r=0.650); represents behavioral predictability |
| `x_mean` | **CORE CLUSTERING** | Mean override level; independent; represents friction compliance level |
| `HHI_net` | **CORE CLUSTERING** | NeT backbone; genuinely new; represents network hub-concentration |
| `rho_self` | **CORE CLUSTERING** | NeT; genuinely new; represents habitual same-app repetition |
| `H_out` | **CORE (CAUTION)** | InT; independent; represents friction response diversity — ⚠ condition-confounded; use within-condition analysis or as secondary |
| `mu_hat` | **SECONDARY** | StoP; independent; near-zero for all DS5 (weak discriminator); include in sensitivity analysis |
| `H_hour` | **SECONDARY** | InT; independent; temporal diversity; may add context-dependence signal |
| `H_app` | **SECONDARY** | InT; independent; app breadth; correlated with H_trans via I_consec |
| `H_trans` | **SECONDARY** | NeT; partially new; correlated with H_app; use in extended model |
| `chi_behav` | **SECONDARY** | StM; partly independent (via p_use ≈ x_mean); adds modest susceptibility signal |
| `deviation_from_predicted_fixed_point` | **SECONDARY** | DyS; combines mu_hat + x_mean; interpretation aid |
| `beta_behav` | **INTERPRETATION ONLY** | = 2/sig_hat² — monotone transform; no new information for clustering |
| `T_behav` | **INTERPRETATION ONLY** | = sig_hat²/2 — same |
| `H_SDE` | **INTERPRETATION ONLY** | = f(sig_hat) — monotone transform |
| `F_behav` | **INTERPRETATION ONLY** | = f(sig_hat, H_emp) — combines two features already in clustering |
| `is_dys_eligible` | **INTERPRETATION ONLY** | Binarization of sig_hat; use to describe clusters, not to form them |
| `behaviorally_deterministic` | **INTERPRETATION ONLY** | = (low sig_hat AND low H_emp); composite label |
| `four_model_convergent` | **INTERPRETATION ONLY** | Same as behaviorally_deterministic effectively |
| `regime_label` / `behavioral_regime` | **INTERPRETATION ONLY** | Categorical labels from DyS/StM |
| `high_chi` | **INTERPRETATION ONLY** | Binarization of chi_behav |
| `I_consec` | **EXCLUDE** | = H_app − H_trans; derived; do NOT use with H_app and H_trans simultaneously |
| `top1_share_net`, `top3_share_net` | **EXCLUDE** | Correlated with HHI_net; partial redundancy |
| `H_pi` | **EXCLUDE (Phase 1)** | Lower coverage (378/569); bring in only if Phase 1 clustering is stable |
| `H_StM_participant` | **EXCLUDE** | ≈ H_SDE for most participants; adds negligible independent signal |
| `sigma_mu_ratio` | **EXCLUDE** | 31.2% NaN; interpretation aid only; too noisy for clustering |
| `p_use_approx` | **EXCLUDE** | ≈ x_mean (r ≈ 0.95+); redundant |
| `E_use`, `E_nonuse`, `Z_2state`, `C_behav` | **EXCLUDE** | Internal StM intermediates; not phenotype dimensions |
| `n_days`, `n_nodes`, `n_edges`, `M_transitions` | **EXCLUDE** | Data quality covariates; not behavioral dimensions |
| `is_net_eligible`, `is_stationary_eligible` | **EXCLUDE** | Eligibility flags; not behavioral dimensions |
| `study_condition` | **OVERLAY ONLY** | Experimental condition; MUST NOT be used as clustering feature; use post-hoc |

---

### 3.3 Why certain features must not be used together

| Pair | Problem |
|---|---|
| `sig_hat` + `beta_behav` | Exact monotone transform; perfectly collinear |
| `sig_hat` + `H_SDE` | Monotone transform; perfectly collinear |
| `H_app` + `I_consec` + `H_trans` | I_consec = H_app − H_trans; three features encode two dimensions |
| `is_dys_eligible` + `sig_hat` | Binary threshold on continuous variable; redundant |
| `four_model_convergent` + `sig_hat` + `H_emp` | Composite; already encoded by its components |
| `x_mean` + `p_use_approx` | Near-identical (both ≈ mean daily override rate) |
| `HHI_net` + `top1_share_net` | Both measure hub-concentration; correlated |

---

## 4. Analysis population and missing data

| Feature group | N complete | % of 573 | Bottleneck |
|---|---|---|---|
| StoP features (sig_hat, mu_hat, x_mean) | ~414 | ~72% | MIN_DAYS = 7 threshold |
| InT features (H_emp, H_app, H_out, H_hour) | ~572 | ~100% | Essentially all |
| DyS flags (is_dys_eligible) | ~414 | ~72% | Same as StoP |
| StM features (chi_behav, F_behav) | ~414 | ~72% | Same as StoP |
| NeT features (HHI_net, rho_self, H_trans) | ~463 | ~81% | MIN_TRANSITIONS = 20 |

**Primary analysis population:** Participants with complete data on all 5 core clustering
features (sig_hat, H_emp, x_mean, HHI_net, rho_self) — approximately 400–410 participants
depending on overlap. Compute exact N after merging files.

**Participants with H_emp but not StoP features:** ~158 additional participants have InT data
but not StoP data. These are participants with too few days for SDE estimation but enough
events for entropy estimation. Report this group's descriptives separately.

**Do not impute.** Participants missing core features get NaN cluster assignments and are
described as "insufficient data" rather than assigned to a cluster.

---

## 5. Feature-space diagnostics plan

Before clustering, run these diagnostics in sequence:

### 5.1 Univariate distributions
- Histogram + KDE for each core and secondary feature
- Flag severe skew (|skew| > 2): may need log transform (e.g., HHI_net, rho_self are bounded near 1)
- Note: sig_hat, H_emp, x_mean — check for bimodality (could anticipate cluster structure)
- Apply standard scaling before clustering (zero-mean, unit variance)

### 5.2 Pairwise correlation matrix
- Pearson r for all candidate features on the analysis population
- Confirm expected redundancies (e.g., sig_hat vs beta_behav r ≈ 1.0; sig_hat vs H_SDE r ≈ 1.0)
- Identify unexpected correlations between supposedly independent features
- Flag: if r(sig_hat, HHI_net) > 0.5, report — this would suggest StoP and NeT are measuring overlapping behavioral regularity

### 5.3 PCA / dimensionality reduction
- Run PCA on all candidate features (after scaling)
- How many components explain 80% of variance?
- If 2–3 components dominate, the effective feature space is lower than the number of inputs
- Visualize biplot: which features load on which components?
- Note: this is a diagnostic step, NOT the basis for cluster assignment

### 5.4 Missing data pattern
- Compute N complete for each combination of core features
- Visualize missingness matrix (which participants miss which features)
- Report whether missingness is random or structured (e.g., does condition predict missingness?)

---

## 6. Clustering strategy

### 6.1 Phase 1 — Behavior-only clustering on 5 core features

**Features used:**
- `sig_hat` (standardized) — behavioral noise/impulsivity
- `H_emp` (standardized) — behavioral predictability/entropy
- `x_mean` (standardized) — mean override tendency
- `HHI_net` (standardized) — network hub-concentration
- `rho_self` (standardized) — same-app habitual repetition

**Why psychosocial variables are excluded from Phase 1:**
Psychosocial scales (FoMO, belonging, ostracism, digital_wellbeing) measure subjective experience,
not behavioral structure. Including them in clustering would conflate behavioral profiles with
psychological states, making it impossible to ask "does this behavioral phenotype predict
psychosocial outcomes?" afterward. Use psychosocial variables only as post-hoc interpretation
overlays (Phase 3 of this notebook).

**Why condition is excluded from Phase 1:**
Study condition is an experimental assignment, not a behavioral trait. Clustering on condition
would produce condition groups, not behavioral phenotypes. The interesting question is whether
phenotypes cut across conditions or align with them — this can only be answered if condition
was not used to form the clusters.

**Algorithm:**
1. **K-means** with k = 2, 3, 4, 5, 6
   - Initialize with k-means++ (10 random seeds)
   - Assess via silhouette score, Calinski-Harabasz (CH) index, Davies-Bouldin (DB) index
2. **Agglomerative hierarchical clustering** with Ward linkage, Euclidean distance
   - Plot dendrogram to assess natural cut points
   - Compare with k-means solution at selected k
3. **Gaussian Mixture Model (GMM)** with k = 2, 3, 4, 5
   - Assess via BIC/AIC
   - Allows soft cluster assignment (probabilistic phenotype membership)

**Selection criterion for k:** Prefer the solution where:
- Silhouette score > 0.2 (minimum interpretable separation)
- Dendrogram cut aligns with the k-means solution
- Clusters have at least N=40 members each (avoid singletons)
- Clusters are interpretable in terms of paper phenotype dimensions

**Robustness check:**
- Bootstrap stability: for selected k, resample 80% of data 100 times and recompute clusters;
  report proportion of pairs clustered together across resamples (Jaccard stability)
- Sensitivity to feature set: re-run clustering with and without H_emp (given its r=0.650
  correlation with sig_hat); confirm cluster structure is not driven by this partial redundancy

### 6.2 Phase 2 — Extended model with secondary features

After Phase 1 is stable:
- Add `H_out` (condition-aware: residualize on condition first, or analyze within conditions)
- Add `H_hour` and `H_app` to test whether temporal and app-breadth dimensions split clusters further
- Add `chi_behav` to test whether intervention susceptibility is captured by Phase 1 clusters
- Re-run k-means and compare with Phase 1 solution (adjusted Rand index)
- Report: which secondary features add independent cluster-splitting information?

### 6.3 What NOT to do in clustering

- Do not use the cluster solution to "confirm" individual model results — clusters are
  discovery, not validation of Step 1 findings
- Do not perform statistical tests within clusters on the same features used to form them
  (circular analysis)
- Do not report cluster differences on condition as if clusters explain condition effects;
  condition was not used to form clusters and clusters are not expected to align perfectly

---

## 7. Phenotype interpretation strategy

### 7.1 Labeling philosophy

Step 2 cluster labels are **descriptive behavioral profiles**, not diagnostic types.

Preferred language:
- "Profile A is characterized by low behavioral diffusion and high network concentration..."
- "Participants in Profile B show higher day-to-day override variability and lower habitual repetition..."

Avoid:
- "Type A users are impulsive overriders" (psychological attribution without individual-level validation)
- "These clusters represent distinct phenotypes" (overclaims fixed categorization)
- "Profile A needs friction intervention X" (Step 3 territory — not here)

### 7.2 Connecting profiles to paper dimensions

After cluster assignment, describe each cluster along the ten paper dimensions from §4.3,
using both the clustering features AND the interpretation-only features:

| Paper dimension | Cluster description source |
|---|---|
| Friction sensitivity | x_mean rank within cluster; H_out within cluster |
| Habitual stability | rho_self, is_dys_eligible, behaviorally_deterministic |
| Impulsivity / noise | sig_hat, sigma_mu_ratio (where non-NaN) |
| Threshold dependence | chi_behav, high_chi flag |
| Context dependence | H_hour |
| Adaptation | mu_hat direction (trend, not level) |
| Override tendency | x_mean; rho_self |
| Substitution tendency | H_trans, I_consec |
| Network centralization | HHI_net, top1_share_net |
| Feedback-loop dominance | F_behav (qualitative framing only) |

### 7.3 Psychosocial overlays (Phase 3 of notebook)

After clusters are formed and labeled:
- Compare cluster means on: fomo_mean_pre, belong_mean_pre, ostracism_mean_pre,
  digital_wellbeing, social_media_wellbeing
- Report one-way ANOVA (or Kruskal-Wallis if non-normal) for each psychosocial scale
- Apply Bonferroni correction across scales within this section
- Effect size: eta-squared or epsilon-squared; report alongside p-values
- **Interpretation constraint:** Psychosocial differences between clusters are descriptive
  associations, not explanations. The clusters were not formed to predict psychosocial outcomes.

### 7.4 Condition overlay

After clusters are formed:
- Report condition distribution within each cluster (χ² test)
- Key question: do clusters cut across conditions (phenotype > condition) or align with them
  (phenotype ≈ condition)?
- If clusters strongly align with condition, note this explicitly: "the cluster solution
  partially recovers condition assignment, suggesting the experimental manipulation is the
  primary source of variance in these behavioral features"
- This is an important honest characterization, not a failure

### 7.5 Uncertainty and caveats to document

At minimum, the notebook must state:
1. **Short window caveat:** DS5 observation windows are 7–45 days; cluster assignments may
   not reflect stable individual traits — they reflect behavioral profiles during the study period
2. **Proxy limitation:** All features are derived from X_t = n_opened/n_events, a behavioral
   proxy, not direct measurement of urge, self-control, or psychological state
3. **N limitation for NeT features:** HHI_net and rho_self are available for 81% of participants;
   clustering on a subsample introduces potential selection bias
4. **Condition confound in H_out:** Friction outcome entropy is partly driven by experimental
   condition rather than individual behavioral style
5. **Cluster labels are not types:** The profiles describe patterns in this dataset during this
   study. Cross-dataset replication (DS4, DS6) would be required to support the claim of stable
   individual phenotypes

---

## 8. What each model family contributes to the phenotype space

### StoP — Stochastic Processes

StoP contributes the **backbone** of the phenotype space:
- `sig_hat`: the primary behavioral variability axis. High sig_hat = noise-dominated, impulsive;
  low sig_hat = habit-stable, predictable. This is the most discriminating single feature
  in DS5. It maps directly to the paper's "impulsivity / noise dominance" dimension.
- `mu_hat`: behavioral drift. Near-zero for all DS5 conditions, but directional sign (positive
  = drift toward opens) may differentiate profiles within the low-sig_hat group.
- `x_mean`: mean override tendency. Independent of variability; captures whether a participant
  is, on average, a high or low complier regardless of consistency.

StoP's key conceptual contribution: it separates **level** (x_mean) from **variability** (sig_hat).
Two participants with the same mean override rate can have very different behavioral structures
if one is consistent and one is variable.

### InT — Information Theory

InT contributes the **entropy portrait** of each participant:
- `H_emp`: non-parametric behavioral predictability. Partially independent of sig_hat (r=0.650).
  Captures non-Gaussian patterns (bimodality, heavy tails) that sig_hat misses.
- `H_out`: friction outcome diversity. Adds information about how "mixed" a participant's
  friction responses are — a high H_out person doesn't settle into one response mode.
- `H_app`, `H_hour`: behavioral breadth and temporal regularity. These add dimensions not
  captured by X_t at all — they characterize the broader behavioral context within which
  friction events occur.

InT's key contribution: it shows that two participants with similar sig_hat can differ in
*what kind* of uncertainty structures their behavior — Gaussian noise vs. structured
multi-modal patterns.

### DyS — Dynamical Systems

DyS contributes **regime labels** for interpretation overlays:
- `is_dys_eligible` / `behaviorally_deterministic`: these binarizations are interpretation tools,
  not independent features. But they provide theoretically meaningful language for describing
  cluster differences: "Profile A participants are predominantly DyS-deterministic (64% in the
  low-σ̂ regime) while Profile C participants are almost entirely StoP-stochastic (12% DyS-eligible)."
- `deviation_from_predicted_fixed_point`: adds information about how close a participant's
  empirical mean is to the boundary prediction — may differentiate "settled" from "drifting"
  participants within the low-mu_hat group.

DyS does NOT add an independent clustering feature in Step 2. Its value is in the interpretation
vocabulary it provides.

### StM — Statistical Mechanics

StM contributes the **thermodynamic framing** and one genuinely useful new quantity:
- `chi_behav`: behavioral susceptibility. While correlated with sig_hat (via β = 2/σ̂²),
  the p_use component (≈ x_mean) adds modest independent signal. High-χ participants are those
  nearest a behavioral tipping point — near x_mean ≈ 0.5 AND high-variability. This is a
  natural combination that may identify "threshold-dependent" phenotypes (paper §4.3).
- `F_behav`: free energy analog, useful for describing clusters in thermodynamic language
  (low-F = habitual pull dominates; high-F = behavioral flexibility). Not an independent
  clustering feature, but a useful summary label.
- `behavioral_regime` / `four_model_convergent`: narrative labels useful for describing how
  clusters relate to the four-model quadrangle result from Step 1.

StM's key contribution: it provides the vocabulary for describing whether clusters represent
behaviorally "ordered" or "exploratory" states, and which clusters are near behavioral
tipping points (intervention-sensitive).

### NeT — Network Theory

NeT contributes the **relational structure** of each participant's behavioral repertoire:
- `HHI_net`: how concentrated app-use flow is in a single hub app. High HHI = hub-dependent
  (paper: "network centralization"); Low HHI = distributed transitions.
- `rho_self`: how much same-app repetition dominates. Very high across DS5 (0.92–0.92), but
  individual variation still exists and may co-vary with other features.
- `H_trans`: conditional transition entropy — how diverse are transitions given which app
  was just used? Lower than H_app by definition (chain rule); differences encode substitution
  structure.

NeT's key contribution: it adds the **relational / network** phenotype dimension that is
entirely absent from the StoP↔InT↔DyS↔StM cluster. Two participants with identical sig_hat,
H_emp, and x_mean can differ entirely in how their app-switching behavior is organized.
This is the strongest justification for including NeT features in phenotyping.

---

## 9. Proposed notebook structure for `100_phenotype_exploration.ipynb`

**Suggested cell blocks:**

| Block | Cells | Purpose |
|---|---|---|
| **A: Scope and framing** | A01–A02 | Step 2 definition; what this is and is not; proxy warnings; FLAG system |
| **B: Inputs and data assembly** | B01–B05 | Load all 5 model CSVs; merge on participant_id_canonical; load survey features |
| **C: Feature-space diagnostics** | C01–C06 | Univariate distributions; pairwise correlation matrix; PCA; missingness; eligibility counts |
| **D: Feature selection** | D01–D03 | Apply classification from blueprint; assemble core feature matrix; standardize |
| **E: Phase 1 clustering** | E01–E08 | k-means k=2–6; hierarchical; GMM; evaluation metrics; dendrogram; select k |
| **F: Robustness checks** | F01–F03 | Bootstrap stability; sensitivity to feature set; compare solutions |
| **G: Cluster profiles** | G01–G05 | Per-cluster means on all features; interpretation-only overlay; paper dimension mapping |
| **H: Condition overlay** | H01–H02 | Condition distribution per cluster; χ² test |
| **I: Psychosocial overlays** | I01–I04 | FoMO/belonging/ostracism/digital_wellbeing by cluster; ANOVA/KW; effect sizes |
| **J: Phase 2 extended clustering** | J01–J04 | Add secondary features; compare with Phase 1 (Adjusted Rand Index) |
| **K: Phenotype descriptions** | K01–K03 | Cautious label prose for each identified profile |
| **L: Limitations** | L01 | Short window; proxy; NeT coverage; condition confound; non-replication |
| **M: Forward connections** | M01–M02 | Step 3 setup; what phenotype profiles imply for GaT/ABM (not prescriptive) |
| **N: Save outputs** | N01–N06 | Save all output files; write model_run_summary.md |

---

## 10. Output file structure

```
outputs/model_outputs/phenotyping/
├── ds5_phenotype_feature_matrix.csv        # All features merged; analysis population only
├── ds5_feature_redundancy_report.csv       # Pairwise correlations + classification
├── ds5_cluster_assignments.csv            # participant_id + cluster_label (Phase 1 + Phase 2)
├── ds5_cluster_profiles.csv               # Per-cluster means, medians, SD on all features
├── ds5_psychosocial_overlays.csv          # Cluster × psychosocial scale summary
├── figures/
│   ├── fig1_feature_correlation_matrix.png  # Pairwise correlation heatmap
│   ├── fig2_pca_biplot.png                 # PCA components + feature loadings
│   ├── fig3_cluster_selection_metrics.png  # Silhouette / CH / DB by k
│   ├── fig4_cluster_profiles_radar.png     # Per-cluster profile across phenotype dimensions
│   ├── fig5_condition_by_cluster.png       # Condition distribution across clusters
│   ├── fig6_psychosocial_by_cluster.png    # Psychosocial scale means by cluster
│   └── fig7_dendrogram.png                # Hierarchical clustering dendrogram
└── model_run_summary.md                   # Key results; cluster descriptions; limitations
```

**Companion .md files required** (per CLAUDE.md output documentation rule):
- `ds5_phenotype_feature_matrix.md`
- `ds5_cluster_assignments.md`
- `ds5_cluster_profiles.md`

---

## 11. FLAG system for Step 2

Document these decisions before writing any code:

| Flag | Default (simplest defensible) | Alternative (deferred) |
|---|---|---|
| FLAG P1 | Core clustering: 5 features (sig_hat, H_emp, x_mean, HHI_net, rho_self) | Include H_out in Phase 1 (condition-adjusted) |
| FLAG P2 | K-means for primary clustering algorithm | GMM for soft membership (preferred if Phase 1 shows ambiguous cluster structure) |
| FLAG P3 | k selected by silhouette + dendrogram alignment | Penalty-based methods (BIC/AIC from GMM) |
| FLAG P4 | Psychosocial scales as post-hoc overlay only | Supervised clustering with psychosocial supervision (cross-validated) — Step 3 territory |
| FLAG P5 | No imputation; participants with missing core features excluded from Phase 1 | Multiple imputation for borderline cases (NeT-ineligible) |
| FLAG P6 | H_out excluded from Phase 1 (condition confound) | Residualize H_out on condition then include |

---

## 12. Pre-implementation checklist

Before writing any code in `100_phenotype_exploration.ipynb`:

- [ ] Read `outputs/reports/stage4/stage4_implementation_plan.md` (master plan)
- [ ] Read this blueprint fully
- [ ] Read `data_docs/modeling_cautions.md` for DS5 structural warnings
- [ ] Verify all 5 model output CSV files exist and are non-empty
- [ ] Verify `outputs/features/ds5/ds5_survey_features.csv` exists (for study_condition and psychosocial scales)
- [ ] Verify `outputs/features/ds5/ds5_prepost_features.csv` exists (for pre-survey psychosocial scales)
- [ ] Document all FLAG decisions in notebook header before coding
- [ ] Write proxy warning cell before any clustering code
- [ ] Confirm that study_condition is loaded from survey file, NOT assumed to be in behavioral outputs

---

## 13. Critical limitations to carry forward into Step 3

These limitations discovered in Step 2 must be documented and resolved in Step 3, not suppressed:

1. **Phenotypes ≠ stable traits.** DS5 observation windows (7–45 days) are short. Profiles
   may reflect transient states or study-period behavioral patterns, not lifelong dispositions.
   Cross-dataset replication (DS4 naturalistic data, DS6 repeated waves) is required.

2. **The four-model quadrangle has partial redundancy.** The 154 four-model-convergent
   participants effectively satisfy only two independent conditions (low σ̂ AND low H_emp).
   The phenotype space from StoP↔InT↔DyS↔StM reduces to ~2 genuinely independent behavioral
   dimensions, plus NeT adds 1–2 more. The apparent richness of the feature space should not
   be mistaken for high-dimensional phenotypic diversity.

3. **NeT metrics are extremely high across DS5** (HHI_net ≈ 0.84–0.86; rho_self ≈ 0.92).
   Individual variation exists but both variables are compressed near their upper bounds.
   NeT phenotype differences in DS5 are subtle and should be interpreted cautiously.

4. **H_out is condition-confounded.** Control participants structurally cannot produce the same
   mix of dismiss/close outcomes that friction-exposed participants can. H_out differences
   between clusters may partly reflect condition assignment rather than behavioral style.

5. **Step 2 is discovery, not confirmation.** Cluster structures discovered in DS5 are
   hypotheses, not findings. They will require replication in DS4 and DS6 before they can
   be reported as robust phenotypes in the paper.

---

*Blueprint written 2026-04-18. Implementation pending user confirmation.*
