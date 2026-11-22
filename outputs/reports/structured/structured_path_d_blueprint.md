# Structured Path D — Secondary/Robustness Features Blueprint

**Notebook:** `notebooks/124_structured_dynamic_stochastic_phenotype.ipynb`
**Written:** 2026-08-05
**Position:** third of the four Step 2 exploration notebooks (see
`outputs/reports/structured/structured_step2_exploration_plan.md`). Depends on Path A's cluster
assignments and feature matrix (comparison target and eligibility population), and on Phase 1's
assignments (secondary comparison).
**Output root:** `outputs/model_outputs/structured/phenotyping/path_d/`

---

## Part 0 — Scope (already decided in the exploration plan, restated with verified numbers)

DS5's own synthesis rated Path D its **lowest-yield** path even at N=285 ("confirms Layer 2, doesn't
reveal new dimension"). This notebook is deliberately a **compact robustness check** — same clustering
pipeline as Path A, no additional appended sub-analyses, no new blueprint-level theoretical claims
expected — proportionate to that demonstrated low yield, not an arbitrary cut.

---

## Part 1 — Feature candidates and correlation gate (verified against real data before running)

Six candidates considered (features available but not in Path A's curated 6): `created_mu_hat`
(StoP drift), `created_sigma_mu_ratio` (StoP, **excluded — 27.9% NaN within Path A's own N=41
population**, would shrink N to 29 for one feature; not worth it given this path's already-low expected
yield), `volume_trend_slope` (DyS), `dropout_score` (DyS), `H_hour_creation` (InT), `H_config` (StM),
`persistence_rate` (StM).

**Correlation gate against Path A's 6 core features** (checked before building anything, same principle
as DS5's Path D dropping `H_SDE`/`F_behav` for near-collinearity):

| Candidate | Max \|r\| vs. a Path A core feature | Decision |
|---|---|---|
| `created_mu_hat` | 0.630 (vs. `created_Fano_factor`) | keep |
| `volume_trend_slope` | 0.719 (vs. `created_Fano_factor`) | keep — below DS5's own ~0.9 drop threshold |
| `dropout_score` | 0.479 | keep |
| `H_hour_creation` | 0.445 | keep |
| `H_config` | **0.671 (vs. `H_completion`)** | **drop** |
| `persistence_rate` | 0.441 | keep |

`H_config`'s exclusion is not a new decision — it **replicates** Phase 1's own already-documented finding
that `H_config` correlates r=0.665 with `H_completion` (Phase 1 chose `susceptibility` over `H_config`
for exactly this reason). This run found r=0.671 in the (slightly different, N=41) Path D population —
consistent, not a fresh discovery.

**Final feature set (5):** `created_mu_hat`, `volume_trend_slope`, `dropout_score`, `H_hour_creation`,
`persistence_rate`. **Population: N=41 — identical to Path A**, verified: all 5 features are non-null for
every one of Path A's 41 participants, so this path costs no additional eligibility loss.

---

## Part 2 — Method (identical pipeline to Path A)

Z-score standardize, k=2..4, `min_cell≥10`, silhouette selection, bootstrap Jaccard (100 resamples, 80%),
PCA. **Two comparisons:** ARI against Path A (the primary question — does this add anything beyond the
already-established behavioral axis?) and ARI against Phase 1 (secondary, for completeness).

---

## Part 3 — Expected outcome, stated in advance

Two of the five features (`created_mu_hat`, `volume_trend_slope`) carry a real negative correlation with
`created_Fano_factor` (already in Path A) — both are picking up a related "declining/bursty activity"
signal. **Prediction: moderate-to-high ARI against Path A**, consistent with DS5's own Path D finding
("confirms Layer 2, doesn't reveal new dimension") rather than a new independent axis. If ARI comes out
low instead, that would be the more interesting (and reportable) result, not the expected one.

---

## Part 4 — Output file structure

```
outputs/model_outputs/structured/phenotyping/path_d/
  secondary_feature_matrix.csv
  secondary_cluster_assignments.csv
  secondary_cluster_profiles.csv
  secondary_vs_patha_and_phase1_ari.csv
  figures/
    fig1_pathd_k_selection.png
    fig2_pathd_pca_biplot.png
    fig3_pathd_cluster_profiles.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Correlation gate against Path A's core features completed before writing clustering code
- [x] `H_config` exclusion verified as a replication of Phase 1's own established finding, not new
- [x] `created_sigma_mu_ratio` excluded for NaN cost, verified against the actual population
- [x] Population (N=41, identical to Path A) verified, no additional loss
- [x] Expected ARI-vs-Path-A direction (moderate-to-high) stated in advance
- [x] Notebook 124 implemented and executed

---

## Actual result, added after running (2026-08-05)

**No feasible k.** Every candidate k (2, 3, 4) had `min_cell=1` — each was driven entirely by a single
extreme outlier (`volume_trend_slope=-32.14` for one participant, the same heavy-volume outlier already
named in DyS's own `model_run_summary.md` as "driving most of the spread"). Reported honestly as
infeasible, matching this project's own precedent (DS5's default-condition Path E result) rather than
forced into a degenerate 1-vs-40 split.

**A real bug was caught and fixed before this honest result was reached:** the first implementation
copied the `SELECTED_K = max(valid_ks, ...) if valid_ks else 2` fallback pattern used in Path A and
Phase 1 verbatim. That pattern is safe when at least one candidate k is *close* to feasible, but here
`valid_ks` was empty for a genuine reason (a single outlier dominating every partition), and the silent
fallback to k=2 produced a 1-vs-40 "cluster" with a spuriously high bootstrap Jaccard (0.893) — an
artifact of the outlier being trivially easy to re-isolate under resampling, not a real subgroup. Caught
by reading the printed cluster sizes (`{0: 40, 1: 1}`) before accepting the result, fixed by adding an
explicit `NO_FEASIBLE_K` branch that reports infeasibility directly instead of silently defaulting.
**Two stale output files** (a cluster-profile CSV and figure) from the pre-fix run were also found still
on disk after the corrected notebook execution — the `NO_FEASIBLE_K` branch correctly never regenerates
them, but the earlier buggy run's copies remained and would have misrepresented the corrected result.
Deleted.

**This null result is itself the Path D finding:** DS5's own Path D was already its lowest-yield path at
N=285 (found a stable k=2 that mostly reproduced Path A). Structured's much smaller N does not even
support that much — an honest extension of DS5's own conclusion, not a contradiction of it.
