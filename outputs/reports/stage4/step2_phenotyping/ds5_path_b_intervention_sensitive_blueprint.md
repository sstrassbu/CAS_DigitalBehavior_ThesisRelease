# DS5 Step 2 Path B — Intervention-Sensitive Phenotyping Blueprint

**Notebook:** `105_ds5_intervention_sensitive_phenotype.ipynb`
**Written:** 2026-04-20
**Stage:** Stage 4, Step 2 — Path B (fifth of six paths)
**Depends on:**
- `outputs/model_outputs/phenotyping/ds5_phenotype_feature_matrix.csv` — all behavioral and intervention features including `H_out_resid`
- `outputs/model_outputs/phenotyping/ds5_behav_only_cluster_assignments.csv` — Path A `cluster_behav` labels
- `outputs/model_outputs/phenotyping/ds5_hierarchical_assignments.csv` — Path F `cell_f` labels
- `outputs/model_outputs/phenotyping/ds5_condition_cluster_assignments.csv` — Path E `cond_cluster_full`, `cond_cluster_B` labels

---

## 0. Why this notebook is fifth and why Path E findings are essential input

Paths A and F identified a stable three-type behavioral phenotype structure (k=3; C1/C2/C3;
B_behav1/2/3) using [sig_hat, H_emp, x_mean]. Path E then confirmed that this structure is
**condition-mediated**, not condition-invariant (Outcome D):

| Condition | Within-condition clustering result |
|---|---|
| control (N=137) | k=2, Jaccard=0.744 (marginal) |
| default (N=142) | NO feasible solution — all k rejected (min_cell < 30) |
| reintervention (N=135) | k=2, Jaccard=0.959 (stable) |

The default friction condition collapses behavioral heterogeneity entirely. The reintervention
condition preserves the richest within-condition individual-difference structure.

**This transforms the requirements for Path B.** Path B cannot treat H_out_resid as a simple
additional feature to be clustered in the full sample without condition awareness. The condition
is not merely a covariate — it determines whether and where individual differences in friction
response are observable. Path B must be designed around this finding.

Path B also carries a different theoretical identity from all prior paths. Paths A, F, E all
used the same three behavioral dynamics features (sig_hat, H_emp, x_mean). Path B introduces
a genuinely new phenotype axis: **the diversity of friction-specific response behavior**,
captured by `H_out_resid`. This is the most directly intervention-relevant feature in DS5.

---

## 1. Exact goal of Path B

Path B asks whether there exist **individual-difference phenotypes in how participants respond
to friction itself** — distinct from how variable their behavior is in general (sig_hat),
how diverse their overall friction outcomes are (H_emp), or how often they override (x_mean).

Specifically, Path B characterizes:

1. **Friction-response diversity as a phenotype axis:** `H_out_resid` measures how diversely
   a participant distributes their friction outcomes (cancel / continue / redirect) after
   removing the condition-level mean. A high-resid participant uses a richer and less predictable
   mixture of responses; a low-resid participant is condition-locked into one dominant response.
   Are there stable phenotype types along this axis?

2. **Whether intervention-sensitive phenotypes cut across or align with existing taxonomy:**
   Does H_out_resid-based clustering produce types that match the existing B_behav1/2/3 + A_all
   cells, or does it reveal a genuinely orthogonal dimension?

3. **Whether the reintervention condition is the "phenotyping window" for friction response:**
   Path E showed that reintervention preserves behavioral heterogeneity (ARI=0.70 vs Path A).
   Path B tests whether the same is true for friction-response heterogeneity specifically.

4. **What happens to H_out_resid heterogeneity across conditions:** Even though the condition
   mean is removed, within-condition variance in H_out_resid differs (control std=0.289,
   default std=0.206, reintervention std=0.300). Does this variance difference lead to different
   clustering feasibility, mirroring the Path E behavioral-feature result?

---

## 2. Why Path B is not redundant with Paths A, E, or F

| Question | What prior paths established | What Path B adds |
|---|---|---|
| Are there behavioral phenotypes? | Path A: yes (k=3) | Path B: are there friction-specific ones? |
| Are they condition-independent? | Path E: no (Outcome D) | — |
| Do NeT and behavioral types interact? | Path F: they are orthogonal (ARI=1.000 within B) | Path B: does H_out_resid cut across or align with this? |
| Is default different? | Path E: yes, collapses | Path B: does it collapse H_out_resid variance too? |
| What drives friction response? | Unknown | Path B: friction-response diversity clusters |

**The key non-redundancy:** `H_out_resid` is not the same as `H_emp`. Both are entropy measures
but they differ in scope and in how they relate to the intervention:
- `H_emp`: entropy over all behavioral outcomes — a global measure of behavioral diversity
- `H_out_resid`: entropy over friction-specific outcomes, **after removing the condition-level
  mean** — a measure of individual-level friction-response diversity that is condition-controlled

H_emp captures how behaviorally varied a participant is in general. H_out_resid captures how
idiosyncratically they respond to friction specifically, with the shared condition context
factored out. A participant who is always variable (high H_emp, high sig_hat) might have low
H_out_resid if their friction responses happen to be condition-consistent. A participant who is
generally stable (low H_emp) might have high H_out_resid if they respond to friction in unusual
ways. These are theoretically distinct.

**Feature correlation verification required** (Cell 3 in notebook): compute pairwise Pearson
correlations between H_out_resid and [sig_hat, H_emp, x_mean] to confirm that H_out_resid
carries non-redundant information. If |r| > 0.70 with any prior feature, this must be flagged
and the corresponding feature excluded from the primary clustering set.

**Path B contributes to the thesis by:**
- Completing the intervention-sensitive dimension of the phenotype space
- Directly characterizing individual differences in friction response behavior
- Providing empirical grounding for the claim that "not all participants respond to friction
  in the same way" — moving beyond the override rate alone (x_mean) to the full response
  diversity structure
- Establishing whether the intervention-sensitive dimension is orthogonal to, or aligned with,
  the established behavioral taxonomy

---

## 3. Condition-aware design

### 3.1 Role of each condition in Path B

| Condition | N | Role | Analysis type |
|---|---|---|---|
| reintervention | 135 | **PRIMARY** — where friction response individual differences are most observable | Full clustering analysis |
| control | 137 | **COUNTERFACTUAL BASELINE** — friction present but no delay intervention | Clustering attempt + baseline comparison |
| default | 142 | **DESCRIPTIVE REFERENCE** — where behavioral heterogeneity collapses | Descriptive statistics ONLY — no clustering |

### 3.2 Reintervention as primary condition (rationale)

Reintervention is the condition where:
- Participants received a wait-period friction intervention (the OneSec-like delay before
  app access is granted)
- Individual differences in response to this intervention are most meaningfully expressed
- Within-condition behavioral cluster structure survived Path E (Jaccard=0.959)
- H_out_resid variance is highest (std=0.300 vs 0.289 control, 0.206 default)

Reintervention is therefore the **phenotyping window** for intervention-sensitive individual
differences. The primary clustering analysis, the primary comparison against Path F cells,
and the primary interpretation of Path B results all focus on this condition.

### 3.3 Control as counterfactual baseline

Control participants experienced friction events (the app did attempt to intervene) but did
not receive the intentional delay. Their H_out_resid captures individual variation in how they
distributed friction responses even without the experimental reintervention. This serves as a
counterfactual:

- If H_out_resid clustering yields similar phenotypes in control as in reintervention, then
  H_out_resid phenotypes reflect pre-existing individual differences in friction-response
  diversity, not the reintervention treatment specifically
- If H_out_resid clustering yields different structure in control vs. reintervention, it
  suggests that the reintervention treatment itself activates or amplifies friction-response
  heterogeneity

Path E found that control and reintervention have different within-condition behavioral cluster
structures (ARI cross-condition = 0.266; centroid displacement = 1.136 SD units). Path B should
test whether this extends to the H_out_resid axis.

**Clustering attempt for control:** Run the same k-selection procedure as for reintervention.
Report findings honestly — if no stable solution exists, report this (it would be a finding,
extending the Path E result to the H_out_resid dimension).

### 3.4 Default as descriptive reference

Path E confirmed that the default friction condition collapses behavioral heterogeneity
(no feasible clustering in [sig_hat, H_emp, x_mean]). H_out_resid variance is also lowest in
default (std=0.206 — 31% lower than reintervention). These two facts together predict that
clustering within default on H_out_resid will also be infeasible or marginal.

**Decision rule for default:** Do NOT attempt k-means clustering in the default condition.
Instead, report:
- H_out_resid descriptive statistics for the full default group
- H_out_resid overlay by Path F cell (B_behav1/2/3, A_all) within default — are there any
  within-condition cell differences in H_out_resid?
- Comparison of default H_out_resid distribution vs. reintervention H_out_resid distribution

**Justification for this decision:** The Path E finding (no feasible clustering in default on
behavioral features) was not a sample-size failure — N=142 is sufficient for k=2 if cells
are balanced. It was a genuine structural finding: the feature space collapses in default.
Attempting clustering anyway would risk extracting a spurious solution. The appropriate
response is to report the default condition as the "collapsed" reference case — a finding in
its own right.

---

## 4. Feature specification

### 4.1 Primary clustering features

| Feature | Role | Completeness | Notes |
|---|---|---|---|
| `H_out_resid` | PRIMARY — intervention-sensitive axis | N=414, 0 NaN | Condition mean removed; std varies by condition |
| `x_mean` | SECONDARY — override tendency | N=414, 0 NaN | Direct friction compliance measure |
| `sig_hat` | SECONDARY — behavioral noise | N=414, 0 NaN | Within-person response variability |

**Rationale for this feature set:**
- `H_out_resid` is the defining feature of Path B — the axis that makes it intervention-sensitive
  and distinct from all prior paths
- `x_mean` captures whether participants override frequently or rarely — a direct compliance
  measure that, unlike H_out_resid, does not require condition-residualization because it is
  a rate measure that is less condition-mean-confounded than the raw entropy
- `sig_hat` captures the noise/impulsivity of the friction response process — a participant
  who is high-sig_hat responds erratically to friction; combined with H_out_resid, this
  distinguishes "diverse-but-patterned" from "diverse-and-erratic" friction responses

**Why H_emp is excluded from primary clustering:**
`H_emp` is the full behavioral outcome entropy and is correlated with `sig_hat` (r=0.538 from
Path A). It also partially conceptually overlaps with `H_out_resid`. Including both H_emp and
H_out_resid in the same clustering would risk double-counting the entropy dimension. H_emp
will be used as a post-hoc overlay only.

**Why chi_behav is excluded from primary clustering:**
`chi_behav` is a friction susceptibility measure. It is included as a post-hoc overlay to
characterize whether Path B clusters differ in susceptibility, not as a clustering input.
Including it in clustering would conflate phenotype definition with an outcome measure.

### 4.2 Feature correlation verification (required before clustering)

Before running any clustering, compute and report the pairwise Pearson correlation matrix:
[H_out_resid, x_mean, sig_hat, H_emp, H_out]

Decision rule:
- |r(H_out_resid, x_mean)| > 0.70: drop x_mean from primary set, use as overlay
- |r(H_out_resid, sig_hat)| > 0.70: drop sig_hat from primary set, use as overlay
- If both drop: run Path B on H_out_resid alone with full-sample stratification; this
  would mean friction response diversity is not capturing new information beyond the
  existing axes — a finding in itself

### 4.3 Scaling

**Full-sample analysis (primary):** StandardScaler fitted on full N=414 on [H_out_resid,
x_mean, sig_hat]. Because H_out_resid is already condition-mean-centered (residualized),
pooling across conditions is theoretically valid for the full-sample run.

**Within-condition analyses (reintervention, control):** StandardScaler fitted separately
on each condition's data. Same rationale as Path E: within-condition scaling normalizes
within-condition variance before clustering.

**Sensitivity run:** Apply full-sample scaler to within-condition data (same procedure as
Path E Comparison 6). Report ARI(within-cond scaler vs full-sample scaler) per condition.

### 4.4 Features NOT to use

| Feature | Reason |
|---|---|
| `H_out` (raw) | Condition-confounded; H_out_resid is the correct version |
| `H_emp` | Clustering input: conceptual overlap with H_out_resid; use as overlay |
| All NeT features | Excluded across all behavioral paths |
| `study_condition` | Stratification variable, not clustering input |
| `sigma_mu_ratio` | 31.2% NaN — reduces N; use as overlay on available subset |
| `mu_hat` | 56.5% near-zero; use as overlay only |
| `H_SDE`, `beta_behav`, etc. | Redundant transforms; excluded per prior QC |

---

## 5. Analysis design

### 5.1 Full-sample primary analysis (N=414)

**Purpose:** Establish whether there exist stable phenotype types in the intervention-sensitive
feature space when pooling across conditions (justified by H_out_resid being pre-residualized).

**Procedure:**
1. Scale [H_out_resid, x_mean, sig_hat] with full-sample StandardScaler
2. Run k-means for k in [2, 3, 4]
   - k-means++, n_init=10, random_state=42
   - Compute: silhouette, Calinski-Harabasz, Davies-Bouldin, min cell size
3. Bootstrap Jaccard stability (100 bootstraps, 80% sample) for top candidate k
4. Select k: max silhouette where all cells ≥ 30 AND Jaccard ≥ 0.75
5. If no stable k: report "weak intervention-sensitive structure in full sample"
6. Label clusters by H_out_resid ascending (low-resid = low friction-response diversity;
   high-resid = high friction-response diversity) — analogous to sig_hat ascending in Path A

**This full-sample run is the anchor for all subsequent condition-specific analyses.**
Because H_out_resid is already condition-controlled, the full-sample solution represents
the best-powered test of whether intervention-sensitive phenotype types exist at all.

### 5.2 Within-reintervention analysis (N=135, PRIMARY within-condition)

**Purpose:** Validate the full-sample solution in the condition where individual differences
are most observable; test whether a stable friction-response phenotype exists within the
experimental reintervention context specifically.

**Procedure:**
1. Subset: reintervention condition only (N=135)
2. Scale [H_out_resid, x_mean, sig_hat] with within-reintervention StandardScaler
3. Run k-selection: k in [2, 3, 4], same stability protocol as full-sample
4. Select k per feasibility rules (Section 6)
5. If stable: label clusters by H_out_resid ascending
6. Comparison: ARI(within-reintervention Path B vs. full-sample Path B)
7. Comparison: ARI(within-reintervention Path B vs. Path A cluster_behav)
8. Comparison: ARI(within-reintervention Path B vs. Path E cond_cluster_full for reintervention)

**Profile B sub-analysis within reintervention (if feasible):**
- Profile B reintervention N≈99 (from Path E: profile_p1=B in reintervention group)
- k=2: cells ≈50 → safe; k=3: cells ≈33 → borderline (min_cell ≥ 30 required); k=4: reject
- If stable: compare against B_behav1/2/3 from Path F (ARI)
- This tests whether Path F cells differ systematically in H_out_resid within reintervention

**Profile A reintervention (N≈36): DESCRIPTIVE ONLY — no clustering**

### 5.3 Within-control analysis (N=137, COUNTERFACTUAL)

**Purpose:** Establish what H_out_resid structure looks like in the absence of the reintervention
treatment; distinguishes pre-existing trait-level friction-response diversity from
treatment-activated diversity.

**Procedure:**
1. Subset: control condition only (N=137)
2. Scale [H_out_resid, x_mean, sig_hat] with within-control StandardScaler
3. Run k-selection: k in [2, 3, 4], same stability protocol
4. Report finding honestly — if infeasible, state "no stable intervention-sensitive structure
   in control (counterfactual baseline)"
5. If stable: ARI(control Path B vs. reintervention Path B) — tests whether phenotypes are
   condition-specific or trait-level

### 5.4 Default condition (N=142, DESCRIPTIVE ONLY — no clustering attempt)

**Decision gate:** Do NOT run k-means in the default condition.

**Descriptive analysis:**
- H_out_resid distribution statistics (mean, std, quartiles)
- H_out_resid by Path F cell (B_behav1/2/3, A_all) — KW test within default
- H_out_resid by Path A cluster (C1/C2/C3) — are Path A clusters distinguishable on H_out_resid
  even in default where behavioral clustering is infeasible?
- Report the std=0.206 finding prominently: this is a 31% reduction in H_out_resid variance
  compared to reintervention (0.300), consistent with the behavioral heterogeneity collapse
  documented in Path E

---

## 6. Sample-size and stability safeguards

### 6.1 Full-sample (N=414)
| k | Expected cells | Feasibility |
|---|---|---|
| 2 | ~207 | Safe |
| 3 | ~138 | Safe |
| 4 | ~104 | Safe, but prefer k≤3 unless clearly justified |

### 6.2 Reintervention (N=135)
| k | Expected cells | Feasibility |
|---|---|---|
| 2 | ~68 | Safe |
| 3 | ~45 | Acceptable; reject if any cell < 30 |
| 4 | ~34 | Risky; only accept if min_cell ≥ 30 AND Jaccard ≥ 0.75 |

### 6.3 Control (N=137)
Same thresholds as reintervention. Same constraints as Path E control analysis.

### 6.4 Profile B within reintervention (N≈99)
| k | Expected cells | Feasibility |
|---|---|---|
| 2 | ~50 | Safe |
| 3 | ~33 | Borderline; REQUIRE min_cell ≥ 30 |
| 4 | ~25 | REJECT always |

### 6.5 Stability decision rules

| Jaccard | Decision |
|---|---|
| ≥ 0.75 | STABLE — report and interpret |
| 0.60–0.75 | MARGINAL — report with explicit caveat; do not treat as definitive |
| < 0.60 | UNSTABLE — do not interpret; report as weak-structure finding |
| All k yield min_cell < 30 | INFEASIBLE — descriptive only |

### 6.6 Stopping rule

If no stable k is found in the full-sample analysis, Path B reports:
> "No stable friction-response phenotype types were identified in DS5. H_out_resid does not
> form discrete clusters when combined with x_mean and sig_hat, suggesting that
> intervention-sensitive behavioral variation in DS5 is distributed continuously rather
> than in discrete types."

This is a valid and informative finding. Do not force a cluster solution.

---

## 7. Comparison logic

### Comparison 1: ARI(full-sample Path B vs. Path A cluster_behav)

The primary test of whether friction-response phenotypes are orthogonal to behavioral phenotypes.

- High ARI (> 0.5): H_out_resid clustering mostly recovers the Path A structure; the
  intervention-sensitive axis is not independent — it reflects the same underlying
  behavioral variation (noise, entropy, override) that Path A already captured
- Low ARI (< 0.2): Path B clusters are genuinely orthogonal to Path A; a participant's
  friction-response diversity type is independent of their behavioral dynamics type
- Intermediate: partial alignment; report both what overlaps and what diverges

### Comparison 2: ARI(full-sample Path B vs. Path E cond_cluster_full)

Tests whether Path B recovers the condition-stratified structure from Path E. The Path E
solution assigned CON_C1, CON_C2, REI_C1, REI_C2 labels (plus undifferentiated for default).
If Path B recovers a similar structure, it suggests that the main friction-response axis tracks
the within-condition behavioral variation identified by Path E.

### Comparison 3: ARI(full-sample Path B vs. Phase 1 profile_p1)

Tests whether intervention-sensitive phenotypes are NeT-driven. Low ARI expected (consistent
with Path A's ARI=0.020 vs Phase 1). If high: H_out_resid is correlated with network topology,
which would be theoretically surprising and would require investigation.

### Comparison 4: ARI(within-reintervention Path B vs. full-sample Path B, within reintervention)

Tests how much the within-condition scaling and subsetting changes cluster assignments in
reintervention. High ARI: reintervention drives the full-sample solution. Low ARI: full-sample
solution is influenced by other conditions in ways that change how reintervention participants
are grouped.

### Comparison 5: ARI(within-reintervention Path B vs. within-control Path B, on shared participants)

Not directly feasible (different people in different conditions), but can be approximated by:
applying the reintervention-fitted centroid model to control participants and vice versa, then
comparing cluster geometries. This tests whether friction-response phenotype geometry is
condition-specific or generalizable across conditions.

### Comparison 6: H_out_resid distribution by Path F cell within each condition

For each condition (particularly reintervention), run KW test: does H_out_resid differ across
B_behav1, B_behav2, B_behav3, A_all? This tests whether the existing hierarchical taxonomy
(derived from sig_hat, H_emp, x_mean) predicts who shows high vs. low friction-response
diversity in reintervention.

- If KW significant with large effect: Path F cells are predictive of intervention-sensitive
  response → Path B aligns with Path F
- If KW not significant: Path F cell membership does not predict H_out_resid → they are
  orthogonal dimensions, and Path B adds a genuinely new phenotyping axis

---

## 8. Post-hoc overlays (not used in clustering)

After clustering is complete, overlay the following for interpretive characterization:

| Feature | Overlay analysis |
|---|---|
| `H_emp` | KW test across Path B clusters; do friction-response phenotypes differ in overall behavioral entropy? |
| `mu_hat` | Mean by cluster (where not NaN); directional drift |
| `sigma_mu_ratio` | Mean by cluster on available subset (N≈285); impulsivity index |
| `chi_behav` | KW test across Path B clusters; friction susceptibility |
| `study_condition` | χ² test: are Path B clusters condition-independent? (Expected: partially yes, since H_out_resid is residualized) |
| `profile_p1` | χ² test: are Path B clusters NeT-type-independent? |
| `cell_f` | χ² test: Path B vs. Path F cells — alignment or orthogonality? |
| `cluster_behav` | χ² test + ARI: Path B vs. Path A |
| Psychosocial scales | KW test with Bonferroni correction on available overlays in `ds5_psychosocial_overlays.csv` |

---

## 9. What different outcomes mean

### Outcome 1 — Independent friction-response phenotypes (ideal)

Full-sample Path B yields stable k ≥ 2 with:
- ARI(Path B vs. Path A) < 0.2 (orthogonal to behavioral dynamics)
- ARI(Path B vs. Phase 1) < 0.2 (orthogonal to network topology)
- Stable within-reintervention solution
- H_out_resid KW within Path F cells: not significant

**Interpretation:** Friction-response diversity is a genuinely new phenotype axis,
independent of both the network-topological and behavioral-dynamic dimensions. The DS5
phenotype space is at minimum three-dimensional: (NeT type) × (behavioral type) × (friction-
response type). Path B completes the Step 2 phenotype description.

### Outcome 2 — Partially aligned friction-response phenotypes

Full-sample Path B yields stable k with:
- ARI(Path B vs. Path A) = 0.3–0.5 (partial overlap with behavioral dynamics)
- Within-reintervention solution stable but partially recovers Path A
- H_out_resid KW within Path F cells: significant (some cells differ)

**Interpretation:** The friction-response axis partially aligns with behavioral dynamics —
participants who are already high-noise and high-entropy also tend to show more diverse
friction responses. The new information from Path B is partial. Report the overlap explicitly
and characterize what the residual (non-overlapping) variance in H_out_resid captures.

### Outcome 3 — Friction-response structure mirrors behavioral structure

Full-sample Path B yields stable k with:
- ARI(Path B vs. Path A) > 0.5 (substantial overlap with behavioral dynamics)

**Interpretation:** H_out_resid is not capturing information beyond what sig_hat, H_emp,
x_mean already represent. The intervention-sensitive axis is not genuinely independent.
Report this honestly. Path B's contribution is then to confirm that the behavioral phenotypes
(Path A/F) are also predictive of friction-response behavior — which has direct Step 3
relevance even if it does not add a new phenotype dimension.

### Outcome 4 — Weak or absent full-sample structure

Full-sample Path B yields no stable k (Jaccard < 0.75 for all k, or min_cell consistently
< 30 despite N=414).

**Interpretation:** H_out_resid does not form discrete phenotype types when combined with
x_mean and sig_hat. Friction-response diversity in DS5 is distributed continuously. Report
the continuous distribution of H_out_resid by condition and Path F cell. This finding is
consistent with the "behavioral variation is not discretely typed" interpretation and does
not invalidate prior paths.

### Outcome 5 — Reintervention structure exists but control does not (most likely)

Given Path E's Outcome D, and given that reintervention has the highest H_out_resid variance,
this is the most theoretically expected outcome pattern:
- Reintervention: stable Path B clusters
- Control: no stable clusters (or marginal)
- Default: no clustering attempted

**Interpretation:** Friction-response phenotypes are **condition-specific** to the
reintervention context. The individual differences in how participants respond to friction
are activated by — and become distinguishable only in — the context of the wait-period
intervention. This is itself a thesis finding: the reintervention condition does not merely
expose a pre-existing trait; it activates a dimension of individual difference that is
latent or suppressed in other conditions.

---

## 10. Central question: what does condition-mediated intervention-sensitive structure mean for the DS5 phenotype framework?

**The question:** If intervention-sensitive phenotype structure is strongest in reintervention
but collapses in default, what does that mean for the overall DS5 phenotype framework?

**The answer the blueprint must enable:**

The DS5 phenotype framework is a **multi-layered, condition-mediated structure** with three
distinct levels of expressibility:

**Layer 1 — Network topology (NeT / Phase 1):** Condition-stable. The hub-dominated vs.
distributed app-use structure (Profile B vs. A) is a pre-behavioral organizational pattern
that does not depend on which friction condition a participant is in. Phase 1 labels are
condition-independent (this was not explicitly tested but follows from the NeT feature nature).

**Layer 2 — Behavioral dynamics (Path A/F):** Condition-modulated. The three behavioral
phenotypes (C1/C2/C3; B_behav1/2/3) are observable in control and reintervention but are
suppressed — collapsed into an undifferentiated distribution — by the default friction
condition (Path E Outcome D). The default condition acts as a "homogenizer" that eliminates
the override-rate and entropy variance that drives Layer 2 clustering.

**Layer 3 — Friction-response diversity (Path B):** Condition-specific. H_out_resid variance
is lowest in default (std=0.206), higher in control (0.289), and highest in reintervention
(0.300). If Path B phenotypes are only stable in reintervention, this means the
intervention-sensitive dimension is an emergent property of friction exposure — it cannot be
observed in the absence of the reintervention treatment. This is not a methodological failure;
it is the scientific finding.

**What this implies for the DS5 phenotype taxonomy:**

The full DS5 phenotype framework consists of:
- A **condition-stable structural layer** (NeT type) that characterizes the organizational
  context of friction exposure
- A **condition-modulated behavioral layer** (behavioral type) that characterizes dynamic
  response tendencies but is suppressed in the default condition
- A **condition-emergent friction-response layer** (Path B type, if stable) that characterizes
  individual differences in friction response behavior visible specifically in the reintervention
  context

The default friction condition is theoretically important not because it produces a phenotype
structure — it does not — but because it demonstrates that a particular friction design can
effectively eliminate the behavioral and intervention-sensitive heterogeneity that would
otherwise be phenotypically informative. This is a contribution to intervention design theory:
default friction may be a form of behavioral homogenization that reduces the relevance of
individual phenotyping for personalization.

**The thesis implication:** If individual-difference phenotyping is to be used for
personalization (Step 3), the reintervention design is necessary — both to activate and to
observe the individual differences that would make personalization feasible. The default
condition, by collapsing heterogeneity, eliminates the variance that personalization would
need to exploit.

---

## 11. What Path B strictly does NOT do

- **No Step 3 personalization.** Path B describes phenotypes; it does not prescribe friction
  types, thresholds, or person-specific interventions.
- **No causal claims.** "H_out_resid phenotypes are observed in reintervention" ≠ "the
  reintervention treatment caused these phenotypes." The phenotypes may reflect pre-existing
  traits that are activated by the design context.
- **No clustering in the default condition.** The Path E finding is clear; forcing a default
  clustering solution would produce a spurious result.
- **No Profile A within-condition clustering.** N=36–46 per condition; cells would fall below
  N=30.
- **No cross-dataset generalization.** Path B findings apply to DS5 only.
- **No overclaiming orthogonality.** If ARI(Path B vs. Path A) = 0.35, this is partial
  alignment — not independence, not identity. Report it as what it is.

---

## 12. Figures to produce

| Figure | Content |
|---|---|
| `fig_b1_H_out_resid_by_condition.png` | Violin or box plots of H_out_resid split by condition (3 panels); show variance difference prominently |
| `fig_b2_feature_correlations.png` | Correlation matrix heatmap: [H_out_resid, x_mean, sig_hat, H_emp, H_out]; confirms independence of H_out_resid |
| `fig_b3_fullsample_cluster_selection.png` | Silhouette, CH, DB vs. k for full-sample Path B; with Jaccard bootstrap results |
| `fig_b4_fullsample_cluster_profiles.png` | Radar or grouped bar chart of full-sample Path B clusters on [H_out_resid, x_mean, sig_hat] |
| `fig_b5_reintervention_cluster_selection.png` | Same as fig_b3 but within reintervention only |
| `fig_b6_reintervention_cluster_profiles.png` | Cluster profiles within reintervention; overlay chi_behav mean |
| `fig_b7_control_analysis.png` | Control: k-selection result OR descriptive H_out_resid distribution if infeasible |
| `fig_b8_default_descriptive.png` | Default: H_out_resid distribution + overlay by Path F cell; shows collapsed variance |
| `fig_b9_pathb_vs_patha_crosspath.png` | Sankey or stacked bar: Path B full-sample clusters × Path A cluster_behav; shows alignment/orthogonality |
| `fig_b10_H_out_resid_by_cellf_condition.png` | H_out_resid by Path F cell, faceted by condition; tests whether taxonomy predicts intervention response |
| `fig_b11_ari_comparison_heatmap.png` | ARI matrix: Path B full-sample vs. Path A, Phase 1, Path E, within-reintervention |
| `fig_b12_alluvial_pathb_patha_pathf.png` | Alluvial: full-sample Path B → Path A cluster → Path F cell; shows where phenotype dimensions converge or diverge |

---

## 13. Notebook structure (cell outline)

```
[0] Setup — imports, paths, constants, random_state=42

[1] Load data — feature matrix, Path A labels, Path F labels, Path E labels

[2] Merge master dataframe (N=414)
    - Verify: 414 rows, no duplicates on participant_id_canonical
    - Verify: H_out_resid has 0 NaN

[3] Feature correlation analysis
    - Compute Pearson correlation matrix: [H_out_resid, x_mean, sig_hat, H_emp, H_out, chi_behav]
    - Decision: if |r(H_out_resid, x_mean)| > 0.70 or |r(H_out_resid, sig_hat)| > 0.70, adjust feature set
    - fig_b2: correlation heatmap

[4] H_out_resid descriptive inspection
    - Distribution by condition (with std table)
    - H_out_resid by Path A cluster (C1/C2/C3) — preview
    - H_out_resid by Path F cell (B_behav1/2/3, A_all) — preview
    - fig_b1: violin/box by condition

--- Full-sample analysis ---

[5] Full-sample scaling: StandardScaler on [H_out_resid, x_mean, sig_hat]

[6] Full-sample k-selection: k in [2, 3, 4]
    - Silhouette, CH, DB, min_cell per k

[7] Full-sample bootstrap Jaccard (100 bootstraps, 80% sample, top candidate k)

[8] Full-sample cluster assignment and labeling (H_out_resid ascending)

[9] fig_b3: full-sample cluster selection curves

[10] fig_b4: full-sample cluster profiles

--- Condition overlays on full-sample solution ---

[11] Condition distribution: χ² test (Path B clusters × study_condition)

[12] Profile overlay: χ² test (Path B clusters × profile_p1)

[13] Path A overlay: ARI(Path B vs. cluster_behav) — Comparison 1

[14] Path F overlay: χ² test + KW H_out_resid by cell_f — Comparison 6

[15] Path E overlay: ARI(Path B vs. cond_cluster_full) — Comparison 2

[16] Post-hoc overlays: H_emp, mu_hat, sigma_mu_ratio, chi_behav (KW tests)

[17] Psychosocial overlays (KW with Bonferroni)

[18] fig_b9: Path B × Path A cross-path sankey/stacked bar

[19] fig_b11: ARI comparison heatmap

--- Within-reintervention analysis (primary condition) ---

[20] Subset: reintervention (N=135)
     Within-condition scaling on [H_out_resid, x_mean, sig_hat]

[21] Reintervention k-selection: k in [2, 3, 4]

[22] Reintervention bootstrap Jaccard

[23] Reintervention cluster assignment and labeling

[24] fig_b5: reintervention cluster selection

[25] fig_b6: reintervention cluster profiles

[26] Comparison 4: ARI(within-reintervention vs. full-sample, reintervention subset)

[27] Comparison 4b: ARI(within-reintervention Path B vs. Path A cluster_behav in reintervention)

[28] Comparison 4c: ARI(within-reintervention Path B vs. Path E cond_cluster_full in reintervention)

--- Profile B within reintervention (if feasible) ---

[29] Profile B reintervention: N check; k-selection if N feasible

[30] Profile B reintervention: bootstrap Jaccard

[31] Profile B reintervention: ARI vs. Path F B_behav labels (Comparison 6b)

--- Within-control analysis (counterfactual) ---

[32] Subset: control (N=137)
     Within-condition scaling

[33] Control k-selection: k in [2, 3, 4]

[34] Control bootstrap Jaccard

[35] Comparison 5: cross-condition geometry test (centroid projection)

[36] fig_b7: control result (clusters or descriptive)

--- Default — descriptive only ---

[37] Default: H_out_resid descriptive statistics

[38] Default: H_out_resid by Path F cell (KW test within default)

[39] Default: H_out_resid by Path A cluster (KW test within default)

[40] fig_b8: default H_out_resid distribution

--- Cross-condition comparison ---

[41] KW test: H_out_resid across all three conditions

[42] Pairwise Mann-Whitney: control vs. default, control vs. reintervention, default vs. reintervention

[43] fig_b10: H_out_resid by Path F cell × condition (faceted)

[44] fig_b12: alluvial Path B → Path A → Path F

--- Sensitivity: full-sample scaler applied within conditions ---

[45] Apply full-sample scaler to reintervention data; compare ARI to within-condition scaler result

[46] Apply full-sample scaler to control data

--- Output saving ---

[47] Save ds5_intervention_cluster_assignments.csv + .md

[48] Save ds5_intervention_cluster_profiles.csv + .md

[49] Save ds5_intervention_cluster_stability.csv + .md

[50] Save model_run_summary_path_b.md

[51] Verification — confirm all outputs present, no NaN in key columns
```

---

## 14. Output files

All to `outputs/model_outputs/phenotyping/`:

| File | Content |
|---|---|
| `ds5_intervention_cluster_assignments.csv` | Per-participant: `participant_id_canonical`, `study_condition`, `profile_p1`, `cluster_b_full` (full-sample Path B label), `cluster_b_rei` (within-reintervention label, NaN for control/default participants), `cluster_b_con` (within-control label if feasible), `cluster_behav` (Path A), `cell_f` (Path F) |
| `ds5_intervention_cluster_assignments.md` | Companion: unit = participant-level; one row per participant |
| `ds5_intervention_cluster_profiles.csv` | Mean/median/std of all features per Path B cluster (full-sample solution); includes H_out_resid, x_mean, sig_hat, H_emp, chi_behav, mu_hat (where available), sigma_mu_ratio (where available), condition_distribution |
| `ds5_intervention_cluster_profiles.md` | Companion |
| `ds5_intervention_cluster_stability.csv` | k-selection and Jaccard results per analysis level (full-sample, reintervention, control, Profile B within reintervention); feasibility flag per level |
| `ds5_intervention_cluster_stability.md` | Companion |
| `model_run_summary_path_b.md` | Complete run record: feature set used, correlation matrix, k selected per analysis, all ARI comparisons, stability flags, outcome classification (1–5), interpretation summary |
| `figures/fig_b1_H_out_resid_by_condition.png` | |
| `figures/fig_b2_feature_correlations.png` | |
| `figures/fig_b3_fullsample_cluster_selection.png` | |
| `figures/fig_b4_fullsample_cluster_profiles.png` | |
| `figures/fig_b5_reintervention_cluster_selection.png` | |
| `figures/fig_b6_reintervention_cluster_profiles.png` | |
| `figures/fig_b7_control_analysis.png` | |
| `figures/fig_b8_default_descriptive.png` | |
| `figures/fig_b9_pathb_vs_patha_crosspath.png` | |
| `figures/fig_b10_H_out_resid_by_cellf_condition.png` | |
| `figures/fig_b11_ari_comparison_heatmap.png` | |
| `figures/fig_b12_alluvial_pathb_patha_pathf.png` | |

---

## 15. What Path B would let the thesis conclude

**If Outcome 1 (independent phenotypes):**
> "Individual differences in friction-response diversity (H_out_resid) form a distinct
> phenotype dimension orthogonal to both network topology (Phase 1) and behavioral dynamics
> (Path A/F). The DS5 phenotype space is thus characterized by at least three independent
> dimensions: structural context (NeT type), dynamic response tendency (behavioral type),
> and intervention-specific response diversity (friction-response type)."

**If Outcome 2 (partial alignment):**
> "Friction-response diversity partially aligns with behavioral dynamics but adds independent
> variance. The intervention-sensitive phenotype dimension is not fully captured by sig_hat,
> H_emp, and x_mean — H_out_resid provides complementary information that enriches the
> phenotype description, particularly within the reintervention context."

**If Outcome 5 (reintervention-specific, most likely):**
> "Stable friction-response phenotypes emerge within the reintervention condition, where the
> wait-period design activates and makes observable individual differences in how participants
> respond to friction. These differences are not distinguishable in the control condition and
> are suppressed (alongside behavioral heterogeneity) in the default condition. This finding
> suggests that individual-difference phenotyping for personalization requires an experimental
> context that produces the relevant behavioral variance — specifically, a reintervention-style
> friction design rather than a default friction approach."

**Regardless of clustering outcome, Path B establishes:**
- The H_out_resid variance gradient across conditions (std: 0.206 → 0.289 → 0.300) is a
  finding about intervention design: more intensive friction designs produce more observable
  individual-level variation in friction response
- The default condition's heterogeneity collapse (Paths A and B combined) is a robust finding
  that applies across multiple phenotyping axes
- The reintervention condition is the appropriate context for both observing and studying
  individual differences in friction response behavior

---

## 16. Key prior numbers for comparison

| Metric | Value | Source |
|---|---|---|
| H_out_resid: full sample mean | ≈0.000 (by construction) | Feature matrix (residualized) |
| H_out_resid std: control | 0.289 | Feature matrix |
| H_out_resid std: default | 0.206 | Feature matrix |
| H_out_resid std: reintervention | 0.300 | Feature matrix |
| H_out (raw) mean: control | 0.686 | Feature matrix |
| H_out (raw) mean: default | 0.946 | Feature matrix |
| H_out (raw) mean: reintervention | 0.905 | Feature matrix |
| Path A: k selected | 3 | 102_ds5_behavior_only_phenotype.ipynb |
| Path A: ARI vs. Phase 1 | 0.020 | Path A |
| Path E: reintervention Jaccard | 0.959 | 104_ds5_condition_stratified_phenotype.ipynb |
| Path E: default result | ALL REJECTED | Path E |
| Path E: ARI(reintervention vs. Path A) | 0.697 | Path E |
| Path F: ARI Stage2-B vs. Path A | 1.000 | 103_ds5_hierarchical_phenotype.ipynb |
| chi_behav: N complete | 414 (0 NaN) | Feature matrix |
| sigma_mu_ratio: NaN count | ~31.2% | Feature matrix QC |

---

## ACTUAL RESULTS (added 2026-04-20 after execution of notebook 105)

### Correlation gate outcome

| Pair | r | Gate fires? | Decision |
|---|---|---|---|
| H_out_resid vs x_mean | -0.707 | YES (|r| > 0.70) | x_mean DROPPED; H_emp substituted |
| H_out_resid vs sig_hat | 0.023 | No | sig_hat retained |
| H_out_resid vs H_emp | 0.292 | No | H_emp retained |

**Final clustering features:** [H_out_resid, sig_hat, H_emp]

The gate firing on x_mean is substantively meaningful: participants who always override (high x_mean)
have low-entropy friction outcomes relative to their condition (low H_out_resid). The two axes
encode near-identical information. This gates Path B into Outcome 3 territory before clustering begins.

### K-selection results (full-sample, N=414)

| k | Silhouette | CH | min_cell | Jaccard | Flag | Selected |
|---|---|---|---|---|---|---|
| 2 | 0.330 | 224.8 | 187 | 0.935 | STABLE | No |
| **3** | **0.387** | **259.4** | **68** | **0.940** | **STABLE** | **YES** |
| 4 | 0.367 | 281.7 | 64 | 0.915 | STABLE | No |

### K-selection results (within-reintervention, N=135)

| k | Silhouette | min_cell | Jaccard | Flag | Selected |
|---|---|---|---|---|---|
| **2** | **0.325** | **67** | **0.912** | **STABLE** | **YES** |
| 3 | — | 19 | — | REJECTED (min_cell<30) | No |
| 4 | — | 18 | — | REJECTED (min_cell<30) | No |

### K-selection results (within-control, N=137)

| k | Silhouette | min_cell | Jaccard | Flag | Selected |
|---|---|---|---|---|---|
| 2 | 0.379 | 68 | 0.937 | STABLE | No |
| **3** | **0.414** | **30** | **0.808** | **STABLE** | **YES** |
| 4 | — | 21 | — | REJECTED (min_cell<30) | No |

### Full-sample cluster profiles (k=3)

| Cluster | N | H_out_resid | sig_hat | H_emp | x_mean (overlay) | chi_behav (overlay) |
|---|---|---|---|---|---|---|
| B_fr1 | 148 | -0.211 | 0.140 | 1.548 | 0.837 | 19.2 |
| B_fr2 | 198 | -0.003 | 0.281 | 2.423 | 0.673 | 7.4 |
| B_fr3 | 68 | 0.467 | 0.133 | 1.958 | 0.444 | 45.8 |

**Condition distribution (chi²=82.9, p<0.0001):**
- B_fr1: 54.7% control / 12.2% default / 33.1% reintervention
- B_fr2: 16.2% control / 53.5% default / 30.3% reintervention
- B_fr3: 35.3% control / 26.5% default / 38.2% reintervention

**Psychosocial overlays:** All ns after Bonferroni correction (n=6).

### Cross-path ARI comparisons

| Comparison | ARI | Interpretation |
|---|---|---|
| Full-sample Path B vs Path A | **0.725** | HIGH — largely recovers behavioral taxonomy |
| Full-sample Path B vs Phase 1 | 0.032 | LOW — NeT-independent |
| Full-sample Path B vs Path E | 0.237 | LOW-MODERATE |
| Full-sample vs within-rei Path B (rei participants) | 0.611 | MODERATE |
| Full-sample vs within-con Path B (con participants) | 0.753 | HIGH |
| Within-rei Path B vs Path A | 0.697 | Same as Path E reintervention ARI vs Path A |
| **Within-rei Path B vs Path E (rei solution)** | **1.000** | **IDENTICAL cluster assignments** |
| Profile B within-rei vs Path F B_behav labels | 0.711 | HIGH-MODERATE |
| Within-con Path B vs Path A | 0.529 | MODERATE |

### Outcome classification

**Outcome 3 (partial) confirmed:** ARI(full-sample Path B vs Path A) = 0.725. The friction-response
diversity axis is not orthogonal to the behavioral dynamics axis. H_out_resid encodes nearly
the same information as x_mean (r=-0.707), making the Path B taxonomy a re-expression of
the Path A taxonomy under a different primary feature.

**Critical additional finding:** ARI(within-rei Path B vs Path E rei solution) = 1.000. Within
the reintervention context, dropping x_mean and adding H_out_resid yields IDENTICAL cluster
assignments. This confirms that in the condition where individual differences are most observable,
the friction-response diversity and behavioral compliance axes are functionally interchangeable.

**Unexpected finding — chi_behav:** B_fr3 (diverse responder, high H_out_resid) has dramatically
elevated StM friction susceptibility (chi_behav=45.8 vs 7.4–19.2). This connects the friction-
response diversity type directly to the StM theoretical model's tipping-point concept.

**Unexpected finding — default H_out_resid by cell:** KW within default (H=34.3, p<0.0001).
Even in the condition where clustering collapses, the Path F cell taxonomy significantly predicts
H_out_resid direction (B_behav1 highest, B_behav2 lowest). The behavioral types persist as
real individual differences even when the feature space is too compressed for stable clustering.

### Blueprint section that required updating

Section 10 (central question framing) was confirmed but refined:

- The "condition-emergent friction-response layer" is NOT a genuinely independent third layer.
  H_out_resid captures the same variance as x_mean. The DS5 phenotype framework is therefore
  best described as two genuinely independent layers (NeT + behavioral), not three.
- The chi_behav finding (B_fr3 susceptibility = 45.8) was not anticipated in the blueprint.
  It is the most distinctive Path B result and connects friction-response phenotyping directly
  to the StM framework.
- The persistence of H_out_resid ordering across Path F cells even within default was not
  explicitly anticipated. It validates the Path F taxonomy as predictive of friction-response
  behavior even under behavioral homogenization.

### Registered deviation from §4.1/§4.2

The x_mean gate fired as anticipated. Contrary to §4.1 ("H_emp will be used as a post-hoc overlay only")
and §4.2 (which prescribes no replacement), H_emp was substituted as the third primary clustering feature.
Recommended sensitivity check, not yet run: the blueprint-specified 2-feature variant
[H_out_resid, sig_hat], with ARI reported against the shipped 3-feature solution.
