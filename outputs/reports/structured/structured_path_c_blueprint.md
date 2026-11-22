# Structured Path C — Network-Substructure Blueprint (Layer 1 analog)

**Notebook:** `notebooks/121_structured_network_subphenotype.ipynb`
**Written:** 2026-08-05
**Position:** second of the four Step 2 exploration notebooks (see
`outputs/reports/structured/structured_step2_exploration_plan.md`).
**Depends on:** `participant_network_metrics.csv` (NeT), `H_state_marginal` from
`participant_entropy_metrics.csv` (InT), Phase 1's `cluster_assignments.csv`, and now Path A's
`behavior_only_cluster_assignments.csv` (comparison targets, not features).
**Output root:** `outputs/model_outputs/structured/phenotyping/path_c/`

---

## Part 0 — Non-redundancy check, and why the design differs from DS5's Path C

DS5's Path C asked: within the dominant hub-locked profile, is there network sub-structure? That
question presupposed a NeT-dominated Phase 1 — true for DS5, **not** true for Structured (established in
Path A's blueprint Part 0 and **now confirmed empirically**: Path A's ARI vs. Phase 1 = 1.000, meaning
the behavioral-dynamics features alone almost perfectly reproduce Phase 1). Given that, Path C's design
here is reframed as the complementary, falsifiable test: **if Path A already fully explains Phase 1, does
NeT alone explain anything at all?** Two sub-questions, both DS5-precedented:

1. **Full-sample NeT-only clustering (DS5's "NeT-only robustness check")** — cluster on NeT features
   alone, independent of Phase 1, and compare via ARI.
2. **Sub-clustering within Phase 1's Profile A/B (DS5's core Path C question)** — is there network
   sub-structure the dominant behavioral split doesn't already capture?

---

## Part 1 — Population and features (verified against real data)

**Full-sample NeT-only clustering:** N=45 (`is_net_eligible`).
**Sub-clustering:** within Phase 1 Profile A (N=22) and Profile B (N=14) — **all 36 Phase 1 participants
are already NeT-eligible** (verified: 22/22, 14/14, zero loss), so no additional eligibility filtering
needed for this part.

**Features:** `HHI_net`, `rho_self`, `H_trans`, `H_state_marginal`. `top1_share_net` is **excluded** —
verified r=0.961 with `HHI_net` in this population (near-total collinearity, worse than DS5's own
"partially redundant" caution about the same pair). `H_state_marginal` is Structured's InT-computed
analog of DS5's `H_app` (state-marginal entropy from the same edge list NeT built — this is exactly the
quantity the NeT-InT bridge, `I_consec_state = H_state_marginal − H_trans`, already uses). Verified
present for all 45 NeT-eligible participants (built directly from NeT's own edge list, so no additional
eligibility loss). `I_consec_state` itself is excluded, same as DS5's own rule, since it is the
difference of two included features. **Known correlation, flagged not dropped:** `H_trans` vs.
`H_state_marginal`, r=0.715 in this population — conceptually distinct (conditional-transition entropy
vs. marginal-state entropy), retained per the same precedent used for Phase 1's own flagged-but-retained
pairs.

---

## Part 2 — Method

**Full-sample (N=45):** same procedure as Path A — z-score, k=2..4, `min_cell≥10`, silhouette selection,
bootstrap Jaccard (100 resamples, 80%), PCA. ARI against Phase 1 computed on the N=36 overlap, and
against Path A's clusters on the same overlap (a second, independent check of the same underlying claim).

**Within-profile sub-clustering (N=22 and N=14):** k=2 only tested (higher k is not meaningfully
supportable at this N). **`min_cell` floor scaled down proportionally**, not silently loosened: Phase 1
used `min_cell≥10` for N=36 (ratio ≈0.28); applying the same ratio gives `min_cell≥6` for N=22 and
`min_cell≥4` for N=14. These are used explicitly, stated here, not adjusted after seeing results.
Bootstrap Jaccard still computed and reported, but **any resulting split is treated as tentative by
construction** given DS5's own Profile-A sub-clustering (N=125, six times larger) was already only
"tentative" (Jaccard=0.835, std=0.157).

---

## Part 3 — Expected outcome, stated in advance (falsifiable, and now doubly motivated)

**Full-sample NeT-only clustering vs. Phase 1: predicted LOW ARI** — the mirror image of DS5's 0.990.
This is now a stronger prediction than when Path A's blueprint was written, since Path A's actual result
(ARI=1.000 against Phase 1) makes it very likely NeT-only structure is close to orthogonal to Phase 1 (if
NeT alone reproduced Phase 1 as well as behavior alone does, Phase 1 would have to be capturing two
different things equally well, which is possible but would itself be a separate, interesting finding to
report honestly if it happens — not assumed away).

**Within-profile sub-structure: predicted weak or absent**, given DS5's own struggle to find robust
sub-structure even at 6-9x this N, and given NeT features are not what's driving the Structured split to
begin with (so removing the dominant grouping first and looking for a secondary NeT axis is asking for a
signal that may not exist at all in this N).

---

## Part 4 — Output file structure

```
outputs/model_outputs/structured/phenotyping/path_c/
  net_only_feature_matrix.csv          # N=45, 4 features
  net_only_cluster_assignments.csv     # participant_id, cluster_label
  net_only_cluster_profiles.csv
  net_only_vs_phase1_and_patha_ari.csv # two-row ARI comparison
  profileA_net_subcluster.csv          # N=22 sub-clustering result + feasibility verdict
  profileB_net_subcluster.csv          # N=14 sub-clustering result + feasibility verdict
  figures/
    fig1_pathc_k_selection.png
    fig2_pathc_pca_biplot.png
    fig3_pathc_cluster_profiles.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Non-redundancy check vs. DS5's Path C and vs. Path A's own result completed before writing code
- [x] `top1_share_net` collinearity (r=0.961 with HHI_net) verified and excluded
- [x] `H_state_marginal` (Structured's H_app analog) verified present for all 45, correlation with
      `H_trans` flagged not dropped
- [x] Sub-cluster `min_cell` floors scaled proportionally from Phase 1's own rule, stated in advance
- [x] Both predictions (low full-sample ARI; weak/absent sub-structure) stated before running
- [x] Notebook 121 implemented and executed

---

## Actual result, added after running (2026-08-05)

**Full-sample NeT-only (N=45), k=2 selected** (silhouette=0.293; k=3 also clears min_cell≥10 but has
lower silhouette). Bootstrap Jaccard=0.822, STABLE.

**ARI(Path C vs. Phase 1) = 0.173** (DS5's equivalent: 0.990) — **low, as predicted, but not as close to
zero as DS5's orthogonal case (0.020).** Classified PARTIAL rather than fully CONFIRMED-orthogonal: NeT
structure carries some real signal (cross-tab shows a lean, not a clean split) but is clearly dominated
by the behavioral axis — Path A's ARI=1.000 against the same Phase 1 target is categorically stronger.
Triangulating both results together: **Structured's Phase 1 split is overwhelmingly behavioral, with a
weak secondary network contribution** — a more nuanced picture than "network doesn't matter at all,"
but the same directional conclusion as Path A's headline finding, arrived at independently.

**Within-profile sub-clustering:** both Profile A (N=22, 12/10 split) and Profile B (N=14, 8/6 split)
produced bootstrap-stable splits (Jaccard=0.872 and 0.965) that clear their own N-scaled `min_cell`
floors — but per this blueprint's Part 2, both are reported as tentative regardless of the stability
numbers, given DS5's own Profile A sub-cluster (6-9x this N) was already only "tentative." No claim of a
confident 4-cell taxonomy is made from this alone; Path F will test whether this sub-structure survives
independently.
