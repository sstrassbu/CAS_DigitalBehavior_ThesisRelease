# DS6 — Step 2 Path A′: Behavior-Only Phenotyping (DyS removed)

**Notebook:** `notebooks/141_ds6_behavior_only_phenotype.ipynb`
**Written:** 2026-08-06
**Trigger:** user inspected `fig4_phenotype_profiles_enhanced.png` from the main Step 2 pass
(notebook 140) and asked why Profile A shows nothing on the "Regime changed" axis.
**Depends on:** notebook 140's output (`cluster_assignments.csv`, for the ARI comparison)
and the same 4 remaining Step 1 sources (StoP 73, NeT 74, InT 75, StM 71).
**Output root:** `outputs/model_outputs/ds6/phenotyping_path_a/`

---

## Part 0 — Why the main pass's radar chart looked broken, and why that's a real finding

Verified (not assumed): the main Step 2 k=2 solution is (almost) exactly DyS's
`regime_changed` binary feature — cross-tab confirmed perfect separation (all 125 Profile A
= regime_changed=0, all 102 Profile B = regime_changed=1; see
`ds6_phenotyping_blueprint.md`'s already-recorded "Headline finding 1"). A feature that
perfectly defines a cluster boundary has, by construction, zero within-cluster variance on
that same feature — the radar's individual-line spread and IQR band for that axis
necessarily collapse to a single point for whichever profile sits at 0. This is not a
plotting bug; it is the direct visual signature of one feature dominating a multi-feature
clustering pass, and it is worth acting on rather than just re-styling the chart.

This is exactly the situation DS5's own Path A ("does removing the dominant feature family
change the phenotype structure?") and Structured's own Path A (same question, same name)
were built to answer. DS6 gets its own version here.

---

## Part 1 — Design: drop DyS entirely, not swap in a different DyS feature

**4 features, no DyS:** `h_period` (StoP), `hhi_change` (NeT), `H_emp_baseline` (InT),
`susceptibility` (StM). Matches the DS5/Structured Path A ethos precisely — the test is
"what does the phenotype space look like WITHOUT the dominant family," not "what does it
look like with a different feature FROM the dominant family." Swapping in a different DyS
quantity (e.g. `sig_hat_baseline`) would not answer the actual question being asked.

SyD remains excluded from clustering (unchanged from the main blueprint's Part 1
reasoning) and continues to supply the psychosocial overlay.

---

## Part 2 — Comparison to the main pass (ARI)

Compute the Adjusted Rand Index between this notebook's cluster labels and notebook 140's
`cluster_assignments.csv` labels, on the overlapping participant set. Two possible outcomes,
both informative, neither assumed in advance:

- **High ARI** (structure reproduces without DyS): the phenotype split was never really
  about regime change specifically — the continuous features alone carry the same signal,
  and DyS's binary flag happened to track it closely. Matches Structured's own Path A
  result (ARI=1.000 there, though for a different reason — its NeT features were weak, not
  redundant-with-something-stronger).
- **Low/orthogonal ARI** (structure changes without DyS): the main pass's k=2 split really
  was substantially DyS's own signal, and removing it reveals a different (or no clean)
  structure in the remaining continuous features. Matches DS5's own Path A result
  (ARI=0.020 there — NeT so dominant that removing it produced an orthogonal split).

---

## Part 3 — Output file structure

```
outputs/model_outputs/ds6/phenotyping_path_a/
  phenotype_feature_matrix.csv
  feature_redundancy_report.csv
  cluster_assignments.csv
  cluster_profiles.csv
  ari_comparison.csv            # ARI vs notebook 140's clusters
  psychosocial_overlays.csv
  figures/
    fig1_feature_correlation_matrix.png
    fig2_k_selection_metrics.png
    fig3_pca_biplot.png
    fig4_phenotype_profiles_enhanced.png   # 4 continuous axes, no degenerate binary axis
  model_run_summary.md
```

Each CSV gets its own companion `.md` file per the standing documentation convention.

---

## Implementation readiness checklist

- [x] Root cause of the user's observation verified mathematically before building anything
      (Part 0), not just visually re-styled
- [x] Design matches DS5/Structured's own Path A precedent exactly (drop the dominant
      family, don't substitute within it)
- [x] ARI comparison against the main pass planned as the primary readout, with both
      possible outcomes pre-specified as informative
- [x] Notebook 141 implemented and executed. **Real bug caught during k-selection**: the
      naive fallback (`SELECTED_K = ... else 2`) would have silently forced k=2 even though
      NO k (2, 3, or 4) met the min_cell floor — the exact failure mode Structured's own
      Path D notebook already caught once ("silent k=2 fallback... producing a spurious
      STABLE split"). Investigated before accepting: all 3 k values isolate the SAME
      ~9-participant group, which turned out to be genuine multivariate outliers
      (susceptibility 4–10× the population mean). Fixed by explicitly detecting and
      reporting "NO FEASIBLE k" rather than silently forcing one, and labeling every
      downstream result (bootstrap Jaccard, cluster profiles, radar, ARI) as
      outlier-characterization, not a validated phenotype split.
      **Answer to the triggering question:** ARI(Path A' vs main pass) = 0.0235
      (LOW/ORTHOGONAL) — confirms the main pass's k=2 split really was substantially DyS's
      own `regime_changed` signal; the remaining 4 continuous features alone do not offer a
      competing balanced 2-phenotype structure, only this small outlier group. Coherence
      check: all 9 outliers are in friction conditions (7 default, 2 intervention, 0
      control), directionally matching StM's independently-established significant
      condition effect on susceptibility. See
      `outputs/model_outputs/ds6/phenotyping_path_a/model_run_summary.md`.
