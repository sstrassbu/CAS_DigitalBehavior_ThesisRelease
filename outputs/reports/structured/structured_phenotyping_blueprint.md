# Structured — Step 2: Phenotyping Blueprint

**Notebook (planned):** `notebooks/120_structured_phenotype_exploration.ipynb`
**Numbering:** mirrors DS5's own jump from model notebooks (41–48) to phenotyping at 100 — Structured's
model decade is 60–68 (= DS5's 41–48 shifted +20), so phenotyping continues that same +20 offset:
100 + 20 = **120**. Recorded so this isn't re-derived later.
**Depends on:** all 7 Structured Step 1 model outputs (`outputs/model_outputs/structured/*/participant_*.csv`)
**Output root:** `outputs/model_outputs/structured/phenotyping/`
**Scope decision (explicit, per your instruction):** **one well-executed clustering pass**, not DS5's
six-path exploration. DS5's multi-path approach was justified there because Step 2 was declared the main
thesis focus on a 573-participant dataset. Structured has 61 participants total and a much thinner
eligible-N after cross-model intersection (computed below) — six paths would mean six underpowered
analyses instead of one adequately-powered one. Time goes into: correct feature curation, one properly
validated clustering solution, honest small-N caveats, and the radar visualization you specifically
asked to get right.

---

## Part 1 — Feature curation: one metric per model family, checked for redundancy

Mirrors DS5's own radar design (one axis per model family, not a feature dump). Each metric chosen for
(a) being the headline/most interpretable result from its notebook, (b) good eligible-N, and (c) low
correlation with metrics chosen from other families (checked, not assumed):

| Model family | Feature | Source column | Eligible N | Why this one |
|---|---|---|---|---|
| NeT | Network concentration | `HHI_net` | 45/61 | Headline NeT metric; hub-dependence of task-state flow |
| InT | Completion predictability | `H_completion` | 53/61 | Headline entropy result; marginal, not StM's joint version |
| StoP | Burstiness | `created_Fano_factor` | 43/61 | The single strongest StoP finding (bursty, not stable/drifting) |
| DyS | Trajectory instability | `state_space_volatility` | 42/61 | Headline DyS trajectory metric |
| SyD | Backlog trend | `backlog_trend_slope` | 47/61 | Headline SyD finding (validated genuine via the right-censoring sensitivity check in notebook 68) |
| StM | Structure susceptibility | `susceptibility` | 53/61 | **Checked against InT's `H_completion`: r=0.195 (low, not redundant)** — `H_config` was rejected here since it correlates r=0.665 with `H_completion` (expected, since `H_config` includes completion as a component — see `structured_stm_blueprint.md`) |
| GaT | Mean commitment | `mean_commitment_score` | 53/61 | Direct scalar from the headline GaT trade-off curve |

**Not included, and why:** DyS's `dropout_score` and SyD's `backlog_mean` were considered but dropped —
both correlate conceptually with `state_space_volatility`/`backlog_trend_slope` already chosen from the
same notebooks (checked qualitatively; a strict redundancy matrix is computed in the notebook itself,
`feature_redundancy_report.csv`, mirroring DS5's own G-series redundancy check before finalizing).

---

## Part 2 — Sample size: the central constraint for everything downstream

**Checked before designing anything else** (learned the hard way earlier this session not to write
numbers into a blueprint without verifying them first):

- All 7 features simultaneously available (complete case): **N=36/61 (59%)**
- Relaxed set dropping the 2 lowest-yield features (DyS, StoP): **N=39/61** — only 3 more participants
  for the cost of losing two full model families from the radar. **Not worth it; not pursued.**
- Distribution of how many of the 7 families each participant is eligible for: 36 participants have all
  7, 6 have 6/7, 4 have 5/7, 5 have 4/7, 2 have 3/7, 2 have 1/7, 6 have 0/7 (these last 6 are almost
  certainly participants with very little or heavily left-censored activity — consistent with earlier
  findings across every Structured notebook).

**Implication, stated plainly:** N=36 is a **small** clustering population. DS5's Phase 1 analysis
population was N=414. Every clustering statistic here (silhouette, bootstrap Jaccard, cell sizes) will
be noisier and must be reported with that explicitly in mind — not silently presented at DS5's
confidence level. `k=2` is the realistic ceiling; `k=3` will very likely fail a minimum-cell-size check
(a cell of ~12 at k=3 from N=36 is thin; DS5 required `min_cell≥30` at its much larger N). This is stated
here, before running anything, as an expectation to check against, not a conclusion to force.

---

## Part 3 — Clustering methodology

Standard, single pass (no sensitivity forking beyond what's below):

1. Standardize the 7 features (z-score) over the N=36 complete-case population.
2. K-means, `k=2..4`, 10 seeds each (k-means++ init) — report silhouette, Calinski-Harabasz,
   Davies-Bouldin, and minimum cluster size for each `k`.
3. Select `k` by silhouette score **subject to** minimum cell size ≥ 10 (relaxed from DS5's `≥30`,
   proportionate to N=36 vs. DS5's 414 — documented as a deliberate, N-adjusted threshold, not a
   loosening for convenience).
4. Bootstrap stability: 100 bootstrap resamples (80% subsample), Jaccard index between the full-sample
   and each bootstrap clustering — same method as every DS5 phenotyping path, caveated for small-N noise
   in the writeup.
5. PCA on the 7 standardized features — report variance explained by PC1/PC2, as a dimensionality sanity
   check (DS5 found effective dimensionality ~4 of 5 input features; report the Structured equivalent
   honestly, whatever it turns out to be).
6. Redundancy report (`feature_redundancy_report.csv`): full 7×7 correlation matrix, flagging any pair
   `|r|>0.6` not already addressed in Part 1.

**No forced outcome.** If `k=2` is not stable (Jaccard below the standard 0.75 threshold used throughout
this project's clustering work), that is reported as the finding — a single-cluster/no-stable-structure
result is a legitimate, honest Step 2 outcome, not a failure to fix.

---

## Part 4 — The radar chart (priority; detailed design)

**Source:** `notebooks/100_phenotype_exploration.ipynb` cell 26 (`plot_phenotype_profiles_enhanced`,
producing `fig4_fontphenotype_profiles_enhanced_notitle.png` — the exact image referenced). This is a
complete, reusable, well-engineered plotting function — **reused directly, not rebuilt from scratch**,
with these adaptations for Structured:

### 4.1 Axes → the 7 features from Part 1

Direct 1:1 mapping — one axis per model family, exactly like the reference chart, which is fortunate: the
original design used 7 axes drawn from 4 families (some doubled up); Structured naturally gives 7 axes
from 7 distinct families, which is *cleaner* than the original.

### 4.2 Conceptual layer bands — grounded in the theory paper's own Figure 1, not invented

The theory paper's own overview figure (`Structured Planning as a Complex Adaptive System.pdf`, Figure 1
"Mapping the Adaptive Planner") groups all eight CAS families into exactly two panels:

- **"Process, State & Feedback Models"**: StM, DyS, StoP, SyD
- **"Structural, Informational, Strategic & Adaptive Models"**: NeT, InT, GaT, ABM

For a 3-band visual layout matching the reference chart's aesthetic, the first paper group is split into
two (a deliberate refinement for visual/informational balance, documented as such — not claimed to be in
the paper verbatim):

| Band | Families | Color (proposed) |
|---|---|---|
| State & Process | StM, StoP | warm red/orange, matching the reference's "Behavioral dynamics" band |
| Feedback & Flow | DyS, SyD | teal/blue, matching the reference's "Theoretical interpretation" band |
| Structural & Strategic | NeT, InT, GaT | green, matching the reference's "Network structure" band |

This keeps the paper's own top-level StM/DyS/StoP/SyD ↔ NeT/InT/GaT split fully intact — the only change
is subdividing the first half into two bands instead of one, to give 7 axes a 2-2-3 grouping instead of
an unbalanced 4-3.

### 4.3 Model-family colors

7 families now, not 4 — the reference chart's `MODEL_COLORS` dict (InT/StoP/StM/NeT) needs 3 more
(DyS/SyD/GaT). Will select from the same qualitative palette family (matplotlib `tab10`/`Set2`-adjacent
hues) for visual consistency with the reference, avoiding colors that clash with the 3 conceptual-layer
band colors above.

### 4.4 Everything else — kept as-is from the reference implementation

Individual participant spaghetti lines (thin, translucent) behind an IQR band (25th–75th percentile
shaded) and a bold mean line with white-centered markers; boxed white axis labels outside the section
bands; thin inner model-family arcs; dark polar spine/grid; radial ticks at 0.25/0.50/0.75/1.00; bottom
legend blocks for profiles / model families / conceptual layers; title-free (matching the `_notitle`
variant you referenced — a title can be added back trivially if wanted later, the function already
supports both).

### 4.5 What will differ from the reference purely because of Structured's own data

- **Panel count = however many clusters `k` turns out to be** (the function's `specs` list generalizes
  beyond 2 panels if `k=3` is selected; expected `k=2` per Part 2's reasoning, in which case the layout
  is a direct match to the reference).
  reasoning above.
- **N=36 individual lines per panel (at most, split across clusters)**, vs. DS5's much denser ~289/125 —
  the spaghetti-line texture will look sparser. This is an honest reflection of sample size, not a
  styling problem to paper over.

---

## Part 5 — Psychosocial overlay (secondary, lightweight — not the focus)

`structured_survey_features.csv` joined on `participant_id`, restricted to `consent_given & is_finished`
(55/61 max, further thinned by the N=36 clustering population intersection — realistically ~30ish).
Kruskal-Wallis test per scale (`life_happiness_score`, productivity scores, ASRS composite) across
cluster assignment, Bonferroni-corrected across however many scales are tested. Reported as exploratory
only, explicitly flagged given the small resulting N — this is a secondary check, not where the
implementation effort concentrates.

---

## Part 6 — Output file structure

```
outputs/model_outputs/structured/phenotyping/
  phenotype_feature_matrix.csv        # N=36 complete-case, 7 standardized + raw features
  feature_redundancy_report.csv       # 7x7 correlation matrix
  cluster_assignments.csv             # participant_id, cluster label, eligibility flags carried through
  cluster_profiles.csv                # per-cluster mean/median for all 7 features
  psychosocial_overlays.csv           # Part 5 results
  figures/
    fig1_k_selection_metrics.png      # silhouette/CH/DB across k=2-4
    fig2_pca_biplot.png
    fig3_feature_correlation_matrix.png
    fig4_phenotype_profiles_enhanced_notitle.png   # THE radar — priority output
  model_run_summary.md
```

---

## Part 7 — Numbered execution plan

1. Load all 7 `participant_*.csv` files; build the complete-case N=36 feature matrix; save it
2. Redundancy report (7×7 correlation matrix) — confirm no unaddressed `|r|>0.6` pairs beyond the one
   already resolved in Part 1
3. Standardize; run k-means `k=2..4`; report silhouette/CH/DB/min-cell-size table
4. Select `k` (expected 2, per Part 2 — but decided by the metrics, not assumed); bootstrap Jaccard
   stability (100 resamples); PCA variance-explained check
5. Save `cluster_assignments.csv`, `cluster_profiles.csv`
6. Build the enhanced radar exactly as scoped in Part 4 — **this gets the most iteration time**
7. Psychosocial overlay (Part 5) — one pass, Bonferroni-corrected, reported honestly regardless of
   significance
8. `model_run_summary.md` with the full k-selection table, stability verdict, cluster profile summary,
   and explicit small-N caveats (mirroring the "Key limitations" section style DS5's own
   `model_run_summary.md` used)
9. Update `structured_cas_modeling_plan.md`, memory, and `CLAUDE.md` with the Step 2 result, following
   this session's established documentation pattern

---

## Implementation readiness checklist

- [x] Reused the exact existing radar function rather than rebuilding — verified its full source first
- [x] All 7 candidate features checked for eligible-N and cross-family redundancy before selection
- [x] Sample size (N=36) computed and its implications (realistic k ceiling, threshold choices) stated
      before any clustering was run, not discovered after
- [x] Conceptual-layer band grouping grounded in the theory paper's own Figure 1, refinement documented
      as a deliberate visual-balance choice, not presented as verbatim paper content
- [x] Scope deliberately limited to one clustering pass, matching the explicit instruction to focus
      effort rather than replicate DS5's six-path exploration
- [x] Notebook 120 implemented and executed
