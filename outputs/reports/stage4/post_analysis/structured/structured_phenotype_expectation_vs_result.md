# Phenotype Expectation vs. Phenotype Result — Structured

**Written:** 2026-08-08
**Overlap check:** Read in full before writing — `outputs/reports/stage4/post_analysis/phenotype_expectation_vs_result.md`
(DS5's version, whose Part 1/Part 2 "theory anticipated vs. what was found" structure this document
follows) and, most importantly, `outputs/reports/structured/structured_step2_master_synthesis.md`
(Structured's own equivalent narrative document, already thorough on *how the four exploration paths
relate to each other* and *how Structured's layer structure compares to DS5's*). **This document is
deliberately short and narrow** — it does not re-narrate the master synthesis's cross-path story. Its only
job is the one angle the DS5 template's `phenotype_expectation_vs_result.md` emphasizes that the master
synthesis does not organize explicitly: a direct table of what the theory paper's own text named as
per-family phenotype categories (Part 1), set against what the data-driven clustering actually found
(Part 2), plus one gap the master synthesis does not address at all (Part 3). **For the deeper narrative
of why the axes relate the way they do, read `structured_step2_master_synthesis.md` — this document
points there rather than duplicating it.**

---

## Part 1 — Phenotypes theoretically anticipated

Unlike DS5's source paper (which states its anticipated phenotype dimensions as a handful of *conceptual
constructs* — friction sensitivity, habitual stability, impulsivity, threshold dependence, etc., §4.3),
the Structured paper does something more specific for several families: it names **discrete, worded
phenotype categories directly**, one small typology per model family. These are the literal labels each
Step 1 blueprint's own rule-based descriptive-label cell implements (explicitly **not** Step 2 clustering
— see the Step 1/Step 2 boundary note in Part 3).

| Model family | Paper-named phenotype categories (quoted or closely paraphrased from each blueprint's Part 0/1) | Where implemented |
|---|---|---|
| NeT | "inbox-hub, timeline-centered, rescheduling-loop, or completion-path users" (§2.4) | Not implemented as a discrete label — operationalized instead as continuous `HHI_net`/`rho_self`/`H_trans` |
| InT | "routine planners... diverse planners... context-coupled planners" (§2.5, entropy framed as a phenotyping signature) | Not implemented as a discrete label — operationalized as continuous per-participant entropy values |
| StoP | "drift-dominated... noise-dominated... bursty... stable... decay-prone" (paper's "Example B") | `created_phenotype_label` / `completed_phenotype_label` — rule-based, Step 1, descriptive only |
| DyS | "high-structure attractor... sparse-consistent attractor... inbox attractor... dropout attractor" (§2.2) | `region_label` (`high-structure`, `sparse-consistent`, `inbox-heavy`, `dropout-prone`, plus `oscillatory`/`mixed` — the latter two added because the paper's four categories did not exhaust the observed variety) — rule-based, Step 1, descriptive only |
| SyD | "productive loop... overload loop... balancing loop" (§2.8) | `dominant_loop_label` (`overload-trending`, `productive-trending`, `balanced`) — rule-based, Step 1, descriptive only |
| StM | "inbox-heavy planning, timed-task planning, sparse planning, or completion-oriented planning" (System Stability bullet) | `macrostate_label` (`timed-basic`, `high-structure`, `inbox-heavy`, `all-day-dominant`) — rule-based, Step 1, descriptive only |
| GaT | "commitment-oriented... flexibility-oriented... chronic-deferrer... adaptive-rescheduler... overload-prone" (paper's "Example B") | `phenotype_label` — rule-based, Step 1, descriptive only; `overload-prone` deliberately cross-referenced to SyD's `dominant_loop_label` rather than recomputed |
| ABM | No named typology of its own — the paper frames ABM as consuming *other* models' phenotype signals to build agent types, not producing a new typology | Uses Step 2's Profile A/B, not any Step 1 family's own label |

**Implicit expectation, reading across all seven of these:** the paper anticipates that Structured
planning behavior would sort into **several separate, family-specific discrete typologies** — five
different named category systems (StoP, DyS, SyD, StM, GaT), each with 3–5 categories of its own. Taken
at face value, this reads as an even more fragmented anticipated phenotype space than DS5's own paper,
which named conceptual *dimensions* rather than discrete category systems per family.

---

## Part 2 — Phenotypes actually recovered (Step 2, data-driven)

What Phase 1 and the four exploration paths (A/C/D/F) found, condensed from
`structured_step2_master_synthesis.md` and each path's own `model_run_summary.md`:

- **One dominant, continuous axis — behavioral dynamics.** Phase 1's k=2 split (N=36, bootstrap
  Jaccard=0.775) is driven almost entirely by `state_space_volatility` (DyS), `created_Fano_factor`
  (StoP), and `H_completion` (InT) — Profile A (N=22): high volatility/burstiness/outcome-diversity, low
  backlog growth; Profile B (N=14): the reverse. Path A (dropping NeT entirely, N=41) reproduces this
  split almost perfectly (**ARI=1.000** against Phase 1).
- **One real but secondary, non-independent axis — network topology.** Path C (NeT-only, N=45) reproduces
  Phase 1 weakly (**ARI=0.173**). Path F's cross-tabulation of Path A × Path C (N=36) finds the two axes
  are **not** statistically independent (Fisher's exact p=0.029) — a real, detectable, but clearly
  secondary network contribution.
- **No further independent axis.** Path D (5 secondary features spanning StoP/DyS/InT/StM) found **no
  feasible clustering solution at all** at N=41 — a genuine null, not a weaker echo of Path A.

**Net result: the seven paper-anticipated, family-specific discrete typologies collapse, empirically,
into two continuous axes** — one dominant (behavioral-dynamic), one secondary and coupled (network) — with
a fifth candidate axis (Path D's secondary/robustness features) found to carry no independent structure
at all. This mirrors DS5's own "richer theoretical framework than the data supports" conclusion (DS5:
~8–10 anticipated dimensions collapse to ~3 empirical axes), but the collapse is arguably starker here,
since Structured's paper named entire discrete category systems, not just conceptual dimensions, for five
separate families.

---

## Part 3 — A gap neither the master synthesis nor any Step 2 notebook addresses: the two phenotype layers were never cross-checked against each other

This is the one genuinely new observation this document adds, found by inspecting
`outputs/model_outputs/structured/phenotyping/cluster_assignments.csv` directly: it carries only the raw
feature columns and the Phase 1 `cluster_label`, with **no join to any Step 1 family's own rule-based
descriptive label** (`created_phenotype_label`/`completed_phenotype_label` from StoP, `region_label` from
DyS, `macrostate_label` from StM, `dominant_loop_label` from SyD, `phenotype_label` from GaT). The same is
true of Path A's, Path C's, and Path D's own assignment files.

**Concretely, this means no notebook has ever tested a specific, checkable claim implied by Part 1 and
Part 2 together:** does Phase 1's Profile A (high volatility/burstiness) correspond predominantly to
StoP's `bursty`/`noise-dominated` labels and DyS's `oscillatory` label, while Profile B corresponds to
`stable`/`dropout-prone`? The cluster *profile means* in `cluster_profiles.csv` make this plausible on
inspection (Profile A's mean `created_Fano_factor`=7.49 vs. Profile B's 4.61 is directionally consistent
with Profile A skewing toward StoP's `bursty` label) — but this is an **inference from the raw feature
means, not a verified cross-tabulation**, and should not be reported as a confirmed finding. This is a
concrete, low-cost extension a future session could run directly from already-existing CSVs (a `pd.merge`
+ `pd.crosstab` between `cluster_assignments.csv` and each Step 1 family's own participant table), not a
new analysis requiring new data.

---

## Part 4 — Where expectations and results matched, and where they diverged

### Matched
- **Burstiness/instability as a real phenotype-relevant dimension** — anticipated by StoP's and DyS's own
  named categories (bursty, oscillatory), confirmed as the single dominant empirical axis.
- **Network structure as a real, non-trivial dimension** — anticipated by NeT's own named categories
  (inbox-hub, rescheduling-loop), confirmed as real (Path F's p=0.029) even though secondary.
- **Commitment/flexibility as a genuine, non-trivial behavioral signal** — GaT's paper-anticipated
  trade-off is empirically confirmed as non-monotonic (see `structured_theory_vs_implementation_comparison.md`),
  though `mean_commitment_score`'s contribution to the Phase 1 split specifically is modest (Profile A
  3.03 vs. Profile B 2.71 — a real but smaller gap than the volatility/Fano/completion features).

### Diverged
- **Number of independent typologies.** The paper anticipates 5 separate discrete category systems
  (StoP/DyS/SyD/StM/GaT); the data support 2 continuous axes, one of which (network) is coupled to, not
  independent of, the other.
- **Discrete categories vs. continuous axes.** None of the paper's named discrete labels (bursty, dropout-
  prone, overload-trending, high-structure, commitment-oriented, etc.) were used as clustering *inputs* or
  cross-validated as cluster *outputs* — Step 2 clustered on continuous summary statistics instead
  (Part 3's gap). The paper's own discrete-category framing and the Step 2 continuous-clustering framing
  have never been formally reconciled in this dataset, unlike DS5's Step 2 program, which repeatedly
  cross-tabulated different clustering solutions against each other (Path A vs. Phase 1, Path F cells vs.
  Path A/C, etc.) but had no equivalent discrete "paper-named label" layer to reconcile against in the
  first place, since DS5's own paper named conceptual dimensions, not discrete category systems.
- **Direction of the network-vs-behavioral relationship** — see `structured_step2_master_synthesis.md` §1
  for the full DS5-comparison table; not re-derived here.

---

## Part 5 — What this means for the thesis

The thesis should not claim Structured's data confirm five separate family-specific typologies as the
paper's own worked examples might suggest at a first read. It should claim:
- One dominant continuous phenotype axis (behavioral dynamics: burstiness, volatility, outcome diversity,
  backlog trend) and one real, secondary, statistically-coupled axis (network topology) were identified.
- Every individual model family's own paper-anticipated discrete category system remains a legitimate,
  separately-reported **Step 1 descriptive lens** (and several — StoP's burstiness finding, DyS's
  dropout-prone dominance, GaT's non-monotonic curve — are genuinely confirmed at that level) but was
  never elevated to, or tested against, the Step 2 clustering result.
- This is a structurally different — not better or worse — outcome from DS5's own phenotype-collapse
  finding, and the comparison itself (fully orthogonal layers in DS5 vs. one dominant + one coupled
  secondary layer here) is the single most citable cross-dataset phenotype-structure result in the
  project (see `cross_dataset_cas_model_synthesis.md` §1).

---

*Written 2026-08-08 as part of the Structured post-analysis waypoint, mirroring
`outputs/reports/stage4/post_analysis/phenotype_expectation_vs_result.md`. For the full six-way narrative
of how Phase 1 and Paths A/C/D/F relate, read `structured_step2_master_synthesis.md` — not duplicated
here.*
