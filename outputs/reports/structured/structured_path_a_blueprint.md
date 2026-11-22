# Structured Path A — Behavior-Only Phenotyping Blueprint (Layer 2 analog)

**Notebook:** `notebooks/122_structured_behavior_only_phenotype.ipynb`
**Written:** 2026-08-05
**Position:** first of the four Step 2 exploration notebooks (see
`outputs/reports/structured/structured_step2_exploration_plan.md` for the full six-path mapping and why
Paths B/E are not built as full paths).
**Depends on:** the six non-NeT Step 1 participant tables (InT, StoP, DyS, SyD, StM, GaT) and Phase 1's
`cluster_assignments.csv` (comparison only, not an input feature).
**Output root:** `outputs/model_outputs/structured/phenotyping/path_a/`

---

## Part 0 — Non-redundancy check against Phase 1 (before any code)

Phase 1 (`notebooks/120_structured_phenotype_exploration.ipynb`) clustered on 7 features, one per model
family, including `HHI_net` (NeT). Path A asks a different, specific question: **what does the phenotype
structure look like when the network-topological feature is excluded entirely?** — DS5's own Path A
precedent. This is not a re-run of Phase 1 with a different N; it is a test of whether the network axis
was *driving* the Phase 1 split or merely *co-occurring* with it.

**Already known before running (from the exploration plan's Part 1 numbers and Phase 1's own
`cluster_profiles.csv`):** Structured's Phase 1 A/B gap on `HHI_net` (0.505 vs. 0.573) is far smaller
than DS5's Phase 1 gap (0.545 vs. 0.978). This makes a specific, falsifiable prediction possible before
running anything (Part 4 below).

---

## Part 1 — Population (verified against real data, not estimated)

Eligibility = complete-case across the six non-NeT Step 1 eligibility flags:
`is_net_eligible` **excluded on purpose** ∩ InT (`H_completion` non-null) ∩ `created_is_eligible` (StoP)
∩ `is_dys_eligible` ∩ `is_syd_eligible` ∩ `is_stm_eligible` ∩ `is_gat_eligible`.

**N = 41** (verified by direct set intersection on the real CSVs) — a genuine gain of 5 participants over
Phase 1's N=36, confirming NeT eligibility was not the binding constraint (DyS at 42/61 and StoP at
43/61 are tighter than NeT at 45/61).

No missing values in the resulting 41×6 feature matrix (verified).

---

## Part 2 — Features

| Feature | Source model | Notes |
|---|---|---|
| `H_completion` | InT | outcome-diversity entropy |
| `created_Fano_factor` | StoP | burstiness |
| `state_space_volatility` | DyS | weekly trajectory volatility |
| `backlog_trend_slope` | SyD | backlog growth rate |
| `susceptibility` | StM | completion-rate sensitivity to task structure |
| `mean_commitment_score` | GaT | commitment-signal index |

Same 6 features as Phase 1 minus `HHI_net` — deliberately, to isolate the network axis's contribution.

**Known correlated pair, carried over from Phase 1's own redundancy check, not newly discovered:**
`H_completion` vs. `state_space_volatility`, r=0.633 in this N=41 population (was r=0.68 at Phase 1's
N=36 — consistent). Both retained, per Phase 1's precedent (the pair was flagged, not dropped, since
each still traces to a distinct model family per the "one feature per family" design principle).

---

## Part 3 — Method (identical procedure to Phase 1, for direct comparability)

1. Z-score standardize all 6 features.
2. K-means, k=2..4 (k=4 is the practical ceiling: N=41 with `min_cell≥10` allows at most 4 roughly-even
   groups; tested, not assumed).
3. Select k by silhouette score, subject to the `min_cell≥10` feasibility floor used throughout this
   project's clustering work.
4. Bootstrap stability: 100 resamples, 80% subsample, Jaccard via Hungarian-matched cluster labels.
   Stability threshold: ≥0.75 = STABLE (same threshold as Phase 1 and all six DS5 paths).
5. PCA on the 6 standardized features, reported for dimensionality context.
6. **Comparison to Phase 1:** ARI between Path A's cluster labels and Phase 1's cluster labels, computed
   on the 36-participant intersection.

---

## Part 4 — Expected outcome, stated in advance (falsifiable)

DS5's Path A was **orthogonal** to its Phase 1 (ARI=0.020) specifically because DS5's Phase 1 was almost
entirely NeT-driven — removing NeT features removed the thing that was creating the split, so a
different, independent structure emerged.

Structured's Phase 1 is **not** strongly NeT-driven (Part 0). **Prediction: Path A's clusters should
show higher ARI against Phase 1 than DS5's 0.020** — plausibly moderate-to-high, since the features doing
the separating in Phase 1 (volatility, Fano, completion entropy) are exactly the features Path A is built
from. If ARI comes out low despite this reasoning, that would itself be a real, reportable surprise, not
suppressed or reframed.

This also bears on Path C's own advance prediction (see `structured_path_c_blueprint.md`): if Path A
reproduces Phase 1 well, Path C's independent NeT-only clustering should predict Phase 1 *poorly* — the
two predictions are two sides of the same underlying claim (Structured's dominant axis is behavioral, not
network) and will be checked against each other once both notebooks exist.

---

## Part 5 — Path E analog: subscription-stratified check (appended, not a separate notebook)

Per the exploration plan's explicit scoping decision: DS5's Path E used three randomized friction
conditions; Structured has none. The only available stratifier, `subscription_type_last` (free/pro), is
observational and already used elsewhere only as a descriptive comparison.

**Verified split in this population:** 29 pro / 12 free.

**Design:** attempt k=2 k-means separately within the pro subgroup (N=29) and the free subgroup (N=12).
**Prediction, stated in advance: the free subgroup (N=12) is very likely infeasible** — below any
reasonable `min_cell` floor for even a 2-way split, let alone a bootstrap-stable one. This is run anyway
(cheap, a few cells) specifically to convert that expectation into a documented, verified result rather
than an assumption — consistent with how Model 1 was still run in the ABM notebook despite its result
being mathematically predictable in advance.

---

## Part 6 — Output file structure

```
outputs/model_outputs/structured/phenotyping/path_a/
  behavior_only_feature_matrix.csv     # participant_id, 6 features
  behavior_only_cluster_assignments.csv  # participant_id, cluster_label
  behavior_only_cluster_profiles.csv     # per-cluster mean/median/std
  behavior_only_vs_phase1_ari.csv        # single-row ARI comparison result
  subscription_stratified_check.csv      # feasibility verdict per subgroup (Path E analog)
  figures/
    fig1_patha_k_selection.png
    fig2_patha_pca_biplot.png
    fig3_patha_cluster_profiles.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Non-redundancy check against Phase 1 completed before writing code (Part 0)
- [x] Population (N=41) verified against real data, not estimated
- [x] Known feature redundancy (H_completion/state_space_volatility) carried forward, not re-litigated
- [x] Expected ARI-vs-Phase1 direction stated in advance, falsifiable
- [x] Path E analog scoped explicitly as a short appended check, with infeasibility predicted in advance
- [x] Notebook 122 implemented and executed

---

## Actual result, added after running (2026-08-05)

**N=41, k=2 selected** (silhouette=0.237; k=3/k=4 both fail the min_cell≥10 floor). **Bootstrap Jaccard
0.885, STABLE.**

**The central Path A question, answered decisively: ARI(Path A vs. Phase 1) = 1.000 on the N=36
overlap** — a perfect cross-tabulation (Phase 1 Profile A's 22 = BehavProfile A's 22 minus the 2 gained
from dropping NeT; Profile B's 14 = BehavProfile B's 14 minus 3 gained). This **confirms** the prediction
stated in Part 4: Structured's Phase 1 split is driven almost entirely by the behavioral-dynamics
features, not by `HHI_net`/NeT — the mirror image of DS5, where Path A was orthogonal to a NeT-dominated
Phase 1 (ARI=0.020).

**Path E analog:** free subgroup (N=12) k=2 gave a 9/3 split, min_cell=3 — correctly ruled infeasible
against this notebook's own min_cell≥10 floor (a bug was caught and fixed here: the first implementation
used an ad hoc `min_cell<3` gate for this one check, inconsistent with the min_cell≥10 standard used
everywhere else in the notebook, which would have wrongly reported a 9/3 split as "feasible, STABLE"
based on a bootstrap Jaccard=0.869 that was really just repeatedly re-isolating the same 3 outlier
points). Pro subgroup (N=29) k=2 gave 15/14, min_cell=14 — genuinely feasible, bootstrap Jaccard=0.895,
STABLE.

**Two implementation bugs caught before/during first run, not after:** (1) an f-string double-brace
escaping error in the `model_run_summary.md`-generation cell that would have printed literal `{k}`
placeholders instead of real k-selection numbers — caught by tracing the escaping convention against the
working `build_120_phenotype.py` precedent before ever executing; (2) the Path E feasibility gate
inconsistency described above, caught by reading the printed output and noticing it granted "STABLE" to
a 9/3 split that the rest of the same notebook would reject outright.
