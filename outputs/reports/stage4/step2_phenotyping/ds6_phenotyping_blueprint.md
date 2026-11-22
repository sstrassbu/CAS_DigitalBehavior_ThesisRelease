# DS6 — Step 2 Phenotyping Blueprint

**Notebook:** `notebooks/140_ds6_phenotype_exploration.ipynb`
**Written:** 2026-08-06
**Depends on:** all 6 completed DS6 Step 1 model families (StoP 73, NeT 74, InT 75, DyS 72,
SyD 78, StM 71) — the DS6 Step 1 arc closed the same day this blueprint was written.
**Output root:** `outputs/model_outputs/ds6/phenotyping/`

---

## Part 0 — Scope decision: one clustering pass, not DS5's six-path exploration

Same decision rule already on record for Structured ("match rigor to N, don't blindly
replicate DS5's scale of exploration" — `structured_phenotyping_blueprint.md`). DS6's
complete-case N across the chosen feature set (below) will land in the low-to-mid 200s —
healthier than Structured's N=36, but this is still DS6's FIRST phenotyping pass on
features that have never been jointly examined before. One well-checked clustering pass,
not a six-path exploration, matching Structured's precedent for the same underlying reason
(first pass, not yet validated) rather than purely an N-driven decision.

---

## Part 1 — Feature selection: 5 behavioral features, not 6

DS6 has 6 completed active model families, but **SyD does not contribute a core clustering
feature** — a deliberate departure from the DS5/Structured pattern (which used exactly one
feature per completed family), explained below.

| Feature | Family | Source file | Column |
|---|---|---|---|
| `h_period` | StoP | `stochastic_processes/participant_stop_parameters.csv` (also present in NeT's bridge file) | `h_period` |
| `hhi_change` | NeT | `network_models/stop_net_period_comparison.csv` | `hhi_change` |
| `H_emp_baseline` | InT | `information_theory/participant_entropy_metrics.csv` | `H_emp_baseline` |
| `regime_changed` | DyS | derived from `dynamical_systems/participant_regime_classification.csv` | `1 if regime_baseline != regime_intervention else 0` |
| `susceptibility` | StM | `statistical_mechanics/participant_macrostate_metrics.csv` | `susceptibility` |

**Why SyD is excluded from the core feature set:** re-examining what SyD (78) actually
produced that is genuinely its OWN, not reused from another family — `mean_N_baseline`,
`mu_hat_baseline`, `volume_change`, `regime_baseline`/`regime_intervention` are all reused
directly from StoP/DyS (SyD's own blueprint Part 0 confirmed this: SyD's role was to test
those existing behavioral quantities against a NEW target, not to produce a new behavioral
quantity of its own). SyD's only genuinely novel per-participant outputs are
`addiction_index_change`/`self_control_index_change` — both psychosocial, not behavioral.

**DS5 and Structured both kept psychosocial variables OUT of the core clustering feature
set entirely**, reserving them for a post-hoc overlay test (DS5 Phase 1: σ̂/μ̂/H_emp/etc.,
9 behavioral features, psychosocial tested only as an overlay; Structured: 7 behavioral
features, same pattern). Given SyD's own output is inherently psychosocial, the
precedent-consistent choice is: **SyD's role in DS6 Step 2 is to supply the overlay
variables**, not a 6th clustering feature. This is arguably a *better*-grounded overlay than
DS5/Structured's own (which used static wave-1 pre-scores) — DS6's overlay uses the actual
psychosocial CHANGE scores, a more meaningful dynamic quantity given the repeated-wave
design SyD itself was built to exploit.

---

## Part 2 — Redundancy check (to be run, not assumed)

Three of the five features (`hhi_change`, `susceptibility`, and to a lesser extent
`H_emp_baseline`) all touch "how much did this participant's app/time usage pattern
change or vary" from different angles — genuine risk of redundancy. Checked empirically in
the notebook (pairwise correlation matrix, |r|>0.6 flag threshold, same as DS5/Structured
precedent) before trusting the 5-feature set as non-redundant, not assumed from the
feature *descriptions* alone.

---

## Part 3 — K-selection and stability

Same method as Structured (`k=2..4`, `MIN_CELL` scaled to this notebook's actual N, not
copied from either DS5's 30 or Structured's 10 without checking); bootstrap Jaccard
stability (100 resamples, 80% subsample); PCA sanity check on variance explained.

---

## Part 4 — Radar chart (adapted from `notebooks/100_phenotype_exploration.ipynb` cell 26,
reused via Structured's own already-adapted version in `notebooks/120_...ipynb`)

Same visual design (individual spaghetti lines, IQR band, bold mean line, boxed axis
labels, concentric section-layer rings, dark polar grid). 5 axes (not 7 or 9) map 1:1 onto
the 5 features above. Section-layer grouping (documented before running, not decided
post-hoc): "Volume & Predictability" (StoP `h_period`, InT `H_emp_baseline`), "Structure
Change" (NeT `hhi_change`, StM `susceptibility`), "Regime" (DyS `regime_changed`) — a
2-2-1 split reflecting which pairs of quantities are conceptually closest (also the pair
most likely to show correlation in the Part 2 redundancy check).

---

## Part 5 — Psychosocial overlay (SyD's role, per Part 1)

`addiction_index_change`/`self_control_index_change` (from SyD's `participant_stock_flow.csv`,
N=188) tested against cluster membership via Kruskal-Wallis, Bonferroni-corrected — same
statistical approach as DS5/Structured's overlays, applied to SyD's own change-score output
instead of static pre-scores.

---

## Part 6 — Output file structure

```
outputs/model_outputs/ds6/phenotyping/
  phenotype_feature_matrix.csv     # complete-case feature matrix (5 features + IDs)
  feature_redundancy_report.csv    # pairwise correlation matrix
  cluster_assignments.csv          # participant_id, cluster_label, all 5 features
  cluster_profiles.csv             # per-cluster mean/median/std for all 5 features
  psychosocial_overlays.csv        # Kruskal-Wallis results, addiction/self_control change
  figures/
    fig1_feature_correlation_matrix.png
    fig2_k_selection_metrics.png
    fig3_pca_biplot.png
    fig4_phenotype_profiles_enhanced.png   # priority deliverable, matches DS5/Structured style
  model_run_summary.md
```

Each CSV gets its own companion `.md` file per the standing documentation convention.

---

## Implementation readiness checklist

- [x] Scope decision (one pass, not six-path) justified explicitly, matching Structured's
      precedent reasoning, not just copied
- [x] SyD's exclusion from the core feature set is a deliberate, explained architectural
      decision (matching the DS5/Structured behavioral-features/psychosocial-overlay split),
      not an oversight
- [x] Redundancy risk among 3 of 5 features flagged BEFORE running, to be checked empirically
- [x] Radar chart section-layer grouping decided before running
- [x] Notebook number checked against concurrent sessions before writing any code —
      130s decade found already claimed by a concurrent DS4 Step 2 exploration
      (`131_ds4_behavior_only_phenotype.ipynb` and 132/133 reserved per
      `ds4_step2_exploration_plan.md`); DS6 uses **140** instead, the next free round decade
- [x] Notebook 140 implemented and executed. One bug found and fixed (f-string
      double-brace escaping error in the model_run_summary generation code — a mechanical
      bug, not a data/theory issue). Feature redundancy check ran clean (no |r|>0.6, the
      pre-registered concern was checked and not confirmed). k=2 selected (silhouette=0.296,
      min_cell constraint ruled out k=3/k=4). Bootstrap Jaccard=0.714, **MARGINAL** (not
      STABLE) — reported honestly, not rounded up. **Headline 1:** the k=2 split is
      (almost) exactly DyS's `regime_changed` binary feature (perfect separation) — parallels
      DS5's own finding that one family (NeT) dominated its phenotype space. **Headline 2:**
      `self_control_index_change` differs significantly by cluster even after Bonferroni
      correction (p=0.018) — the FIRST significant psychosocial result in the entire DS6
      program; stable-regime participants improve (+0.164), regime-changed participants
      worsen (−0.086). See
      `outputs/model_outputs/ds6/phenotyping/model_run_summary.md`.
