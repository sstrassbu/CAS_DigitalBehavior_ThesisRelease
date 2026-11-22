# DS4 Stage 4 Step 2 — Phenotyping Blueprint

**Stage 4, Step 2 — Phenotyping**
**Written:** 2026-08-06
**Status: IMPLEMENTED — approved and completed 2026-08-06.** See
`outputs/model_outputs/ds4_phenotyping/model_run_summary.md` for actual executed
results. Blueprint preserved below as the pre-registration record; unmodified except
for this status line.
**Notebook (to be created):** `notebooks/59_ds4_phenotype_exploration.ipynb`
**Notebook numbering note:** DS4's model decade is 50s (51–55). A clean DS5-style
positional shift (Step 2 = 100, DS4 models = DS5+10) would put this at 110 — already
taken by `110_stanford_health_audit.ipynb`. Using 59 instead: inside DS4's own decade,
after the 5 model notebooks (51–55), not colliding with 56–58 (unused, would only ever
be claimed by the explicitly-excluded GaT/ABM/SyD), and not colliding with any other
dataset's numbering (DS5:100, Structured:120, DS6:70s, Stanford Health:110s).
**Producing dataset:** DS4 — Large Naturalistic OneSec Users (N=1,039)
**Prerequisites:** All 5 DS4 Step 1 families (StoP/InT/DyS/StM/NeT) — complete.

---

## 1. Scope decision — verified against real N, not assumed

The project's own established lesson from Structured's Step 2 (see
`memory/feedback_response_style.md` and `structured_phenotyping_blueprint.md`): **match
exploration depth to real cross-model complete-case N, don't default to DS5's six-path
scale.**

**Verified today (2026-08-06):** DS4's cross-model complete-case N — participants with a
valid result in StoP, InT, DyS, *and* StM (all four share StoP's `fit_valid` population
exactly) plus NeT-eligible — is **641/1,039 (61.7%)**. That is a *lower* retention rate
than DS5's own Phase 1 population (414/573 = 72.3%), but a substantially larger absolute
N (641 vs 414), and vastly larger than Structured's 36. Note also that StoP/StM/DyS/InT
all share the identical 641-participant `fit_valid` set, and NeT eligibility is not a
binding constraint on top of it (950 participants are NeT-eligible; all 641 are among
them, so NeT removes nobody).

**Decision: run Phase 1 first — a single curated-feature clustering pass — before
committing to any multi-path exploration.** This mirrors how DS5's *own* Step 2 actually
started (Phase 1 first; the six-path expansion was a decision made only *after* Phase 1
revealed a specific finding worth chasing — one dominant network-topology axis). Deciding
on six paths in advance, before DS4's own Phase 1 result exists, would be planning by
analogy to DS5's outcome rather than DS4's own data — exactly the failure mode this
whole DS4 arc has been built to avoid. If Phase 1 surfaces a comparably rich question,
further paths get their own blueprint at that point, informed by the real result.

---

## 2. Candidate features — one per model family, redundancy-checked before writing this blueprint

| Family | Feature | Why this one, not another from the same notebook |
|---|---|---|
| StoP (53) | `tau_hat` (relaxation time, days) | Most interpretable, DS4-unique StoP quantity (no DS5 equivalent) |
| InT (52) | `H_emp` (empirical binned entropy of X_t) | Non-parametric — unlike `H_SDE`, not a direct formula function of StoP's θ/σ, so it adds genuinely independent information to a StoP-derived feature set |
| DyS (55) | `fixed_point_deviation` (\|x_mean_raw − mu_hat_OU\|) | Measures OU model-fit quality, not reducible to θ or σ alone — DyS's `regime_label` was rejected for this slot since it's a direct binarization of StoP's own θ̂ |
| StM (51) | `chi_OU` (susceptibility) | Combines β_OU and p_use into one composite quantity, distinct from reusing β_OU (which duplicates θ/σ information already present via `tau_hat`) |
| NeT (54) | `rho_self` (self-transition rate, attempts-only) | NeT's most distinctive quantity; continues the headline "excludes app_close_event" finding into the phenotype space |

**Verified pairwise correlations (N=641, 2026-08-06) — no pair exceeds \|r\|=0.49:**

```
                       tau_hat  H_emp  fixed_point_deviation  chi_OU  rho_self
tau_hat                  1.000  0.196                  0.305   0.008    -0.010
H_emp                    0.196  1.000                  0.168  -0.483     0.227
fixed_point_deviation    0.305  0.168                  1.000  -0.242     0.160
chi_OU                   0.008 -0.483                 -0.242   1.000    -0.268
rho_self                -0.010  0.227                  0.160  -0.268     1.000
```

The strongest pair (`H_emp`/`chi_OU`, r=−0.483) is moderate, not severe — both kept, no
feature dropped. This is a genuine 5-dimensional feature set, not 1–2 dominant axes
hiding behind 5 labels.

---

## 3. FLAG decisions

| Flag | Decision | Justification |
|---|---|---|
| FLAG 1 | Phase 1 only (single pass), further paths deferred pending Phase 1 result | §1 — matches real N, avoids planning-by-DS5-analogy |
| FLAG 2 | Standardize (z-score) all 5 features before clustering | Different units/scales (days, bits, probability-deviation, susceptibility, rate) |
| FLAG 3 | K-means with silhouette-based k selection (k=2..6 tested) | Same method as DS5 Phase 1 and Structured's single pass — structural reference, not content |
| FLAG 4 | Bootstrap Jaccard stability check (100 resamples), STABLE threshold ≥0.75 | Same threshold this project has used consistently since DS5 Phase 1 |
| FLAG 5 | Demographic overlay (age, gender_clean from `ds4_survey_features.csv`) is exploratory/secondary | Only 283/1,039 participants have survey data; no Likert scales exist in DS4 (established limitation, same as every DS4 Step 1 notebook) |

---

## 4. Notebook structure — `notebooks/59_ds4_phenotype_exploration.ipynb`

| Cell | Type | Content |
|---|---|---|
| 1 | MD | Scope: Phase 1 only, why (§1); real complete-case N |
| 2 | MD | FLAG decisions table |
| 3 | MD | Feature table + redundancy check (§2), reproduced live in cell 8 |
| 4 | Code | Setup: imports, paths |
| 5 | Code | Load all 5 model outputs; build complete-case table; verify N=641 live |
| 6 | Code | Standardize features (z-score) |
| 7 | Code | Redundancy check: reproduce §2's correlation matrix live |
| 8 | Code | K-selection: silhouette score for k=2..6 |
| 9 | Code | Fit chosen k; bootstrap Jaccard stability (100 resamples) |
| 10 | Code | Cluster profiles: mean/median of each feature per cluster |
| 11 | Code | PCA: variance explained, effective dimensionality |
| 12 | Code | Demographic overlay (exploratory): age/gender by cluster, N=149 of the 641 complete cases (283/1,039 have any survey row) |
| 13 | Code | Export `ds4_phenotype_feature_matrix.csv`, `ds4_cluster_assignments.csv`, `ds4_cluster_profiles.csv` |
| 14 | Code | Export `ds4_feature_redundancy_report.csv`, `ds4_demographic_overlay.csv`, `model_run_summary.md` |
| 15 | Code | Figure 1: silhouette scores by k |
| 16 | Code | Figure 2: cluster profile radar/bar chart (5 features) |
| 17 | Code | Figure 3: PCA scatter, colored by cluster |
| 18 | Code | Figure 4: bootstrap Jaccard distribution |
| 19 | MD | Interpretation and limits |
| 20 | MD | Forward connections — Step 3, or further Step 2 paths if warranted |

---

## 5. Proposed outputs

**Output root:** `outputs/model_outputs/ds4_phenotyping/`

| File | Description | Rows |
|---|---|---|
| `ds4_phenotype_feature_matrix.csv` | Complete-case participants × 5 standardized features | 641 |
| `ds4_cluster_assignments.csv` | Participant → cluster label | 641 |
| `ds4_cluster_profiles.csv` | Per-cluster mean/median of each feature | k rows |
| `ds4_feature_redundancy_report.csv` | Pairwise correlation matrix (§2, live) | 5×5 |
| `ds4_demographic_overlay.csv` | Cluster × age/gender, N=149 of the 641 complete cases | — |
| `model_run_summary.md` | Full run record with real k, silhouette, Jaccard | — |
| `figures/` | 4 figures per §4 | — |

---

## 6. DS4 weakness flags

- ⚠ FLAG I: Complete-case N=641 excludes the 398 participants without a valid StoP fit
  — same attrition-confound caveat as every DS4 Step 1 notebook (long-window survivors
  may differ systematically from short-window dropouts).
- ⚠ FLAG II: No experimental condition — clusters describe naturalistic heterogeneity,
  not a friction-response typology (unlike DS5's condition-stratified paths).
- ⚠ FLAG III: Demographic overlay is thin (283/1,039, no Likert scales) — do not expect
  DS5-level psychosocial interpretability.
- ⚠ FLAG IV: `tau_hat`, `chi_OU` inherit the daily/weekly timescale ambiguity already
  flagged throughout DS4 Step 1 — phenotype clusters describe daily-timescale dynamics
  specifically.

---

## ⚠ IMPLEMENTATION HOLD (historical — resolved 2026-08-06)

This hold applied during blueprint review and has since been cleared; the notebook was
approved and implemented (Phase 1 only, per §1's decision — see
`ds4_step2_exploration_plan.md` for the further-paths decision made after this ran).
Kept below for the historical record.

When approved:
1. Create `notebooks/make_59_ds4_phenotype.py`
2. Run generator, execute notebook, verify against §2's pre-registered numbers
3. Write companion `.md` docs for every output file
4. Update `memory/project_stage.md` and `memory/cross_dataset_strategy.md`
5. Decide, based on the real Phase 1 result, whether further DS4 Step 2 paths are
   warranted — not decided in advance
