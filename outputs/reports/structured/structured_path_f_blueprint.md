# Structured Path F — Joint Taxonomy Blueprint (hierarchical analog)

**Notebook:** `notebooks/123_structured_hierarchical_phenotype.ipynb`
**Written:** 2026-08-05
**Position:** fourth and last of the four Step 2 exploration notebooks (see
`outputs/reports/structured/structured_step2_exploration_plan.md`). Depends on Path A's and Path C's
already-fitted cluster assignments.
**Output root:** `outputs/model_outputs/structured/phenotyping/path_f/`

---

## Part 0 — Why this is NOT a re-run of DS5's literal Path F design, and not a re-run of Path C's Part 4

DS5's Path F fit a **fresh** behavioral clustering *within* each Stage-1 (NeT) group, because DS5's
Stage 1 and Stage 2 features had never been jointly clustered before — the key validation was whether a
locally-fit clustering matched the globally-fit Path A clustering (DS5's "critical thesis result,"
ARI=1.000 within Profile B).

For Structured, **Path C's Part 4 already fit local NeT sub-clusters within Phase 1's Profile A/B**
(this blueprint's own sibling document). Re-running that here would be a repeat, not a new question.
Instead, Path F asks the question DS5's synthesis used *both* Path A and Path C to answer, but never
built as a single artifact: **what is the actual combined taxonomy when Path A's already-fitted global
behavioral clusters and Path C's already-fitted global NeT clusters are crossed with each other, and is
that combination statistically real or just noise?**

This is a genuine, distinct contribution: neither Path A's `model_run_summary.md` nor Path C's names or
counts the joint cells; this notebook is the first place a combined 2-axis taxonomy is actually produced.
No new k-means fitting is required — this is a cross-tabulation of two already-validated clusterings,
which is more honest than fitting a third, redundant model on the same 36 participants.

---

## Part 1 — Verified inputs (checked against real data before writing anything)

- Path A global clusters (`BehavProfile A/B`, N=41): `behavior_only_cluster_assignments.csv`
- Path C global NeT-only clusters (`NetProfile A/B`, N=45): `net_only_cluster_assignments.csv`
- **Overlap N=36** (exactly Phase 1's population — verified: neither Path A's 5 NeT-ineligible extras nor
  Path C's 9 Phase-1-ineligible extras overlap with each other).
- **Cross-tabulation, computed and verified before writing the notebook:**

  |  | NetProfile A | NetProfile B |
  |---|---|---|
  | **BehavProfile A** | 4 | 18 |
  | **BehavProfile B** | 8 | 6 |

  All four cells have N≥4 — usable, not degenerate (by this project's own precedent, e.g. StM's rarest
  macrostate label had N=1, GaT's rarest phenotype had N=1; a floor of 4 here is comparatively healthy).
- **Fisher's exact test on this table (computed in advance): p=0.029, odds ratio=0.167** — the two axes
  are **not** fully independent, consistent with Path C's ARI=0.173 (weak-but-real association) rather
  than either Path A's ARI=1.000 (full correspondence) or a null 0.

---

## Part 2 — What the notebook does

1. Re-derive the 4-cell taxonomy from the two existing assignment files (no new clustering).
2. Name and describe each cell's mean profile across **both** feature sets (Path A's 6 behavioral +
   Path C's 4 NeT features) — the first place these ever appear together per participant.
3. Report the Fisher's exact independence test with full working (not just the pre-computed number
   above — re-derived in the notebook itself for a clean, reproducible record).
4. State explicitly what this means for a future ABM/GaT initialization (DS5's own stated purpose for
   its 4-cell taxonomy): a 2×2 typology with cell sizes 4/18/8/6 gives four candidate agent archetypes,
   though the smallest (N=4) is too thin to characterize with confidence.

---

## Part 3 — Expected outcome, stated in advance

Given Path A (ARI=1.000) and Path C (ARI=0.173) already establish that the behavioral axis dominates and
the network axis contributes weakly, **the joint taxonomy is expected to be lopsided, not a clean 2×2
grid** — one cell (`BehavProfile A × NetProfile B`) should be substantially larger than the others, since
most of Phase 1's Profile A members share both the majority behavioral type and the majority network
type. This was in fact already visible in Part 1's cross-tab before any code was written (18 of 36 in one
cell) — stated here as a prediction check, not discovered fresh in the notebook.

---

## Part 4 — Output file structure

```
outputs/model_outputs/structured/phenotyping/path_f/
  joint_taxonomy_assignments.csv     # participant_id, BehavProfile, NetProfile, joint_cell
  joint_taxonomy_cell_profiles.csv   # per-cell means across all 10 behavioral+NeT features
  joint_taxonomy_independence_test.csv
  figures/
    fig1_pathf_joint_taxonomy_heatmap.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Non-redundancy check against DS5's literal Path F design AND against Path C's own Part 4 completed
      before writing code
- [x] Cross-tabulation and Fisher's exact test computed and verified against real data before finalizing
      this blueprint
- [x] Expected lopsided-cell-sizes outcome stated in advance
- [x] Notebook 123 implemented and executed

---

## Actual result, added after running (2026-08-05)

**Exact match to the pre-computed Part 1 numbers** (cross-tab 4/18/8/6, Fisher's exact p=0.029, odds
ratio=0.167) — a clean run with no bugs caught, the first of the four exploration notebooks to execute
without a code fix needed.

**Joint taxonomy:** `BehavProfile A × NetProfile B` is the largest cell (n=18, half the population) —
confirms the predicted lopsidedness. The two smallest cells (`BehavProfile A × NetProfile A`, n=4;
`BehavProfile B × NetProfile B`, n=6) are too thin to characterize with confidence on their own.

**The independence test is the substantive addition this notebook makes:** the two axes are **not**
statistically independent (p=0.029) — network membership carries real, detectable information beyond
the dominant behavioral split, even though Path A alone already explains almost all of Phase 1's
structure. This reconciles Path A's ARI=1.000 and Path C's ARI=0.173 into a single coherent picture:
**one dominant axis (behavioral) with a real, weaker, non-independent secondary axis (network)** — not
two fully orthogonal layers like DS5, and not a single axis with network as pure noise either.
