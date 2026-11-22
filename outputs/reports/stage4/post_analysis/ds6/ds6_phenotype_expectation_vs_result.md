# Phenotype Expectation vs. Phenotype Result — DS6

**Written:** 2026-08-08
**Overlap check:** Read in full — `outputs/reports/stage4/post_analysis/phenotype_expectation_vs_result.md`
(DS5 template, mirrored here), `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md`
§1 (already documents DS6's `regime_changed`-dominated axis as one of four qualitatively
different cross-dataset phenotype-layer geometries — cited, not re-derived).
**Scope of this file:** DS6-only, at a level of numerical detail the cross-dataset synthesis
does not attempt (exact cross-tab counts, exact overlay statistics, the full Path A′ outlier
narrative). The cross-dataset document's framing of DS6 ("a third thing entirely: DyS's
binary `regime_changed`... dominates, near-perfect separation") is the correct one-sentence
summary; this document is the full account behind that sentence.

---

## Part 1 — Phenotypes theoretically anticipated

### What the paper's construct-mapping framework anticipates, reinterpreted for DS6's data constraints

DS6 shares the same generic anticipated phenotype dimensions as every OneSec-family dataset
in this project (construct mapping is dataset-independent), but — as throughout DS6's Step 1
build — several of the paper's default operationalizations require an outcome variable DS6
does not have. The table below shows, for each anticipated dimension, both DS5's
operationalization (for comparison) and DS6's actual available operationalization.

| Anticipated dimension | DS5 operationalization | DS6 operationalization | Model family |
|---|---|---|---|
| Friction/period sensitivity | `x_mean`, `H_out` | `h_period`, `hhi_change`, `susceptibility` — all **change** quantities, not levels | StoP, NeT, StM |
| Habitual stability / attractor strength | Low σ̂, `is_dys_eligible` | `regime_changed=0` (stable regime across the boundary), low `sig_hat` | DyS |
| Impulsivity / noise dominance | σ̂, `sigma_mu_ratio` | `sig_hat`, `Fano_factor` (not used directly in clustering, only via `regime`) | StoP |
| Threshold dependence / susceptibility | `chi_behav` (mean-field χ formula, requires β) | `susceptibility` (Jensen–Shannon divergence — no β apparatus exists) | StM |
| Context dependence | `H_hour` | `H_emp_baseline` used in clustering; `H_hour` computed but **not** included as a clustering feature | InT |
| Adaptation over repeated exposure | `mu_hat` ≈ 0, unidentifiable in DS5's 6-week window | **Directly testable** via `h_period` and the regime-transition matrix — DS6's real before/after design is structurally suited to this, unlike DS5 | StoP, DyS |
| Override tendency | `x_mean`, `rho_self` | **Not testable at all** — no outcome variance means there is no override/dismissal event to have a tendency toward; closest surviving analog is `rho_self`/`hhi_change` (habitual app concentration, not override) | NeT |
| Substitution tendency | `H_app`, `H_trans`, `I_consec` | `H_trans`, `I_consec` (bridge exists, not used as a clustering feature) | NeT, InT |
| Network centralization | `HHI_net`, `rho_self` | `hhi_change` (the period-to-period shift is used, not the level) | NeT |
| Feedback-loop dominance | `is_dys_eligible`, `F_behav` | `regime` labels (declining/growing/resting); SyD's two loop tests (both null) | DyS, SyD |

**A structural observation not present in the DS5 template, because DS5's design does not
allow it:** four of DS6's five Step 2 clustering features (`h_period`, `hhi_change`,
`regime_changed`, `susceptibility`) are **change scores across the baseline→intervention
boundary**, not point-in-time levels. Only `H_emp_baseline` is a level. DS5's Phase 1 features
(`sig_hat`, `H_emp`, `x_mean`, `HHI_net`, `rho_self`) are all levels or trait-like snapshots —
DS5 has no within-subject period design to build change scores from. **DS6 phenotypes
primarily on behavioral change; DS5 phenotypes primarily on behavioral level.** This is a
genuine, dataset-structural difference in what kind of phenotype axis is even available to
be discovered, not an analytical choice made independently of the data.

**Implicit expectation (same as DS5's framework):** the paper's construct-mapping table
presents 8–10 dimensions as largely parallel and non-redundant. DS6 had not, as of this
writing, run more than one clustering pass plus one follow-up (Path A′) — far short of DS5's
six-path exploration — so the "are these dimensions really independent in this dataset"
question is only partially answered for DS6 so far (see Part 3).

---

## Part 2 — What Step 2 actually found

### Main pass (notebook 140): k=2, N=227

- **Profile A (N=125), Profile B (N=102)**, silhouette=0.296, bootstrap Jaccard (100
  resamples, 80% subsample) = **0.714 — MARGINAL**, not STABLE (the project's 0.75 threshold)
- **Cross-tab against DyS's `regime_changed` shows perfect separation**: all 125 Profile A
  participants have `regime_changed=0` (stable regime across the boundary); all 102 Profile B
  participants have `regime_changed=1` (regime shifted). Verified directly from
  `cluster_assignments.csv`, not assumed from the cluster means.
- Cluster means still show real (if secondary) differences on the other 4 features: Profile A
  `h_period`=0.124 vs Profile B 0.033; `hhi_change`=0.004 vs 0.020; `susceptibility`=0.030 vs
  0.066 — Profile B is directionally more volatile on every other axis too, but the binary
  `regime_changed` split is what defines the cluster boundary itself.
- **Psychosocial overlay (N=176, SyD's role): `self_control_index_change` differs
  significantly by cluster, surviving Bonferroni correction** (H=6.82, p_raw=0.009,
  p_bonferroni=0.018). Profile A (stable regime) mean change = **+0.164** (improvement);
  Profile B (regime changed) mean change = **−0.086** (worsening). `addiction_index_change`
  shows no such difference (p=0.847).
- This is **the first statistically significant psychosocial result anywhere in the DS6 Step
  1+2 program** — every prior psychosocial correlation (StoP, NeT, InT, StM, and SyD's own
  two loop tests) had been null.

### Path A′ (notebook 141): DyS removed entirely, N=227

- Triggered by a user observation, not a pre-planned step: inspecting the main pass's radar
  chart, Profile A showed zero spread on the "regime changed" axis — verified as the direct,
  correct visual consequence of perfect separation (a feature that defines a cluster boundary
  has, by construction, zero within-cluster variance on itself), not a plotting bug.
- **No feasible k**: k=2, k=3, and k=4 all isolate the **same ~9-participant group**
  (min_cell=9 at every k tested) — a genuine multivariate-outlier signature (`susceptibility`
  4–10× the population mean, combined with elevated `hhi_change`), not evidence of a real
  second phenotype. The k=2 "Profile A′/B′" split (218 vs. 9) is reported explicitly as an
  **outlier characterization, not a validated cluster solution** — the notebook caught and
  avoided the same silent-fallback failure mode Structured's own Path D notebook had already
  hit once (a naive `else 2` default would have forced k=2 despite no k meeting the min-cell
  floor).
- **ARI(Path A′ vs. main pass) = 0.0235 — LOW/ORTHOGONAL.** This is the direct answer to the
  triggering question: the main pass's k=2 split really was substantially DyS's own
  `regime_changed` signal; the remaining 4 continuous features do not offer a competing
  balanced 2-phenotype structure on their own.
- **Coherence check**: all 9 outliers are in friction conditions (7 default, 2 intervention,
  **0 control**) — small N, too small for its own formal test, but directionally matches
  StM's (71) independently-established, separately-significant condition effect on
  susceptibility (control significantly lower than either friction arm, p=0.0011/0.0075).
  This is an individual-level echo of a population-level finding from a completely different
  analysis.
- Psychosocial overlay on this pass: both scales null (`addiction_index_change` p=0.397,
  `self_control_index_change` p=0.841) — the significant main-pass result was tied to the
  `regime_changed` split specifically and does not reappear once that split is removed.

---

## Part 3 — Where expectations and results matched

### Match 1: Threshold dependence / susceptibility as a real phenotype-adjacent dimension

**Expected:** near-tipping-point users identifiable as a distinct type (StM's `chi_behav` in
DS5). **Found:** confirmed twice, independently: (a) StM's own condition-level ANOVA
(F=5.437, p=0.0049) found friction conditions show significantly higher susceptibility than
control; (b) Path A′'s multivariate-outlier group — the most extreme individual
susceptibility values in the whole dataset — is exclusively drawn from friction conditions
(0/9 in control). **Match quality: strong**, and unusually well-triangulated for DS6 (a
population-level ANOVA and an individual-level clustering outlier group point the same
direction, from two independently-built analyses).

### Match 2: Adaptation over repeated exposure is directly testable in DS6, unlike DS5

**Expected:** directional behavioral drift as a phenotype dimension. **Found:** DS6's real
before/after period design makes this testable in a way DS5's short 6-week window could not
(DS5: μ̂ ≈ 0 for virtually all participants, an unidentifiability finding, not a null result).
DS6's `regime_changed` (whether a participant's DyS regime shifts across the boundary) IS
exactly this adaptation signal, and it turned out to be strong enough to dominate the entire
phenotype space. **Match quality: strong on testability, but the result immediately produced
the same kind of single-family dominance DS5 found with NeT** (see Difference 1 below) — the
paper's expectation that this would be "one dimension among several" did not survive contact
with the data.

### Match 3: Habitual/network concentration as a phenotype-relevant dimension

**Expected:** hub dependence / concentration as an individual-difference dimension.
**Found:** `hhi_change` differs directionally between profiles (0.004 vs 0.020) and
contributes to NeT's own independently-established StoP-NeT bridge finding
(`corr(HHI_net change, daily-volume change) = −0.213`), but is not itself the dominant
clustering axis. **Match quality: moderate** — present and directionally consistent, but
secondary to `regime_changed`, not co-equal.

---

## Part 4 — Where expectations and results differed

### Difference 1: One family (DyS) dominates the phenotype space — same *kind* of result as DS5, different dominant family

DS5's Phase 1 was dominated by NeT (`HHI_net`, `rho_self`; ARI vs. Phase 1 for a
NeT-only clustering ≈ 0.990). DS6's main pass is dominated by DyS's `regime_changed`
(perfect 125/102 cross-tab separation). **The paper's framework in both datasets implied a
roughly co-equal multi-dimensional space; both datasets instead found one family's signal
overwhelming the others.** This is now a 2-for-2 project-wide pattern (also echoed, with a
third variant, in Structured's coupled-not-orthogonal finding and DS4's blended-Phase-1
finding — see `cross_dataset_cas_model_synthesis.md` §1) — worth stating as a recurring
methodological lesson: **a joint clustering pass across model-family outputs should always
be checked against a "remove the apparently dominant family" comparison before its structure
is trusted**, not treated as confirmation that all input families contributed meaningfully.

### Difference 2: Override tendency — not a weak signal in DS6, a structurally absent construct

DS5 found override tendency (`x_mean`) collinear with `H_out_resid` (r=−0.707) but still a
real, primary Layer 2 axis. **DS6 cannot test this dimension at all** — there is no dismiss/
close outcome to build an override rate from, at any granularity. This is a stronger and more
absolute gap than any DS5 phenotype-dimension weakness: DS5's "friction sensitivity as a
unified concept" difference (its own Difference 5) was about multiple non-equivalent
operationalizations existing; DS6's gap is that zero operationalizations exist.

### Difference 3: Phenotype stability is markedly weaker in DS6 than in DS5

DS5's Phase 1 bootstrap Jaccard = 0.995 (very stable). DS6's main pass = **0.714, MARGINAL**
— reported honestly as such in the model_run_summary, not rounded up. This means the DS6
phenotype boundary itself is noisier than DS5's, independent of which features drive it. Any
downstream claim built on DS6's Profile A/B split (including the Bonferroni-significant
psychosocial overlay) inherits this instability and should be stated with a correspondingly
weaker confidence than the equivalent DS5 claim.

### Difference 4: DS6's phenotype exploration is, honestly, less mature than DS5's at this point

DS5 ran six systematic paths (A–F) plus a full "v2" revision arc (`60`–`64`) before its
phenotype conclusions were treated as settled. DS6 has run one main pass plus one triggered
follow-up (Path A′) — closer to Structured's single-pass-plus-4-path scope, but even
Structured completed all four of its planned paths. DS6 has not yet tested a condition-
stratified path (DS5's Path E — directly available in DS6 since `study_condition` is native
to the behavioral file), a network-substructure path (DS5's Path C — NeT-only clustering), or
a hierarchical joint taxonomy (DS5's Path F). **The claim "DS6's dominant phenotype axis is
regime change" should be read as the current best evidence, not a conclusion with DS5's level
of validation behind it.**

### Difference 5: DS6 phenotypes on change, DS5 phenotypes on level — an unplanned but real structural contrast

As noted in Part 1, DS6's clustering feature set is overwhelmingly built from
baseline→intervention **change** quantities, while DS5's is built from within-study **level**
quantities. Neither dataset's blueprint stated this as an intentional design contrast — it
falls directly out of what each dataset structurally has available (DS6's real period design
vs. DS5's condition-only design). It is nonetheless a genuine, citable methodological
difference in what "phenotype" means across the two datasets: DS6 profiles answer "who
changed more," DS5 profiles answer "who tends to sit where."

---

## Part 5 — Whether the modeling pipeline changed the phenotype picture

**Yes, in the same structural way DS5's did, via a different mechanism:**

1. Including `regime_changed` in the main pass made DyS's binary signal the effective sole
   determinant of cluster membership — a joint 5-feature clustering pass conflated one
   family's dominant binary signal with four other continuous features' weaker, more
   gradual signal, exactly as DS5's Phase 1 conflated NeT's dominant continuous signal with
   StoP/InT/StM's weaker one.
2. Path A′ was necessary to reveal this, the same way DS5's six-path exploration was
   necessary to disentangle its own NeT/behavioral conflation. Without Path A′, one might
   conclude DS6 has "two roughly balanced phenotypes with several contributing dimensions" —
   the data instead show one binary dominant axis and, absent it, no competing balanced
   structure at all (only a small outlier group).
3. The psychosocial overlay result is the clearest illustration that the phenotype, not any
   single Step 1 family alone, carries the practically important signal: no bivariate
   correlation across StoP/NeT/InT/StM/SyD ever reached significance, but the 2-cluster
   phenotype (built by combining 5 features) immediately did (`self_control_index_change`,
   p_bonferroni=0.018). This is the DS6 analog of the point DS5's own Step 2 synthesis makes
   about the value of phenotyping over single-model bivariate correlation.

---

## Part 6 — Summary: are the phenotypes assumed and the phenotypes found meaningfully different?

**Yes, in three ways, two of which parallel DS5's own conclusions and one of which is new to
DS6:**

**Way 1 (parallels DS5) — one family's signal dominates a nominally multi-dimensional
space.** DS5: NeT. DS6: DyS's `regime_changed`. Different family, same structural lesson.

**Way 2 (parallels DS5) — a construct the paper treats as central turns out to be either
unidentifiable or absent, not just weak.** DS5: adaptation-over-exposure was unidentifiable
in a 6-week window. DS6: override tendency is not a testable construct at all, at any
granularity, because the underlying outcome variable does not exist.

**Way 3 (new to DS6) — the type of phenotype axis available is structurally determined by
which design feature (period vs. condition) a dataset actually has**, not by the paper's
construct list. DS6's real before/after period design makes it the one dataset in this
project's OneSec-family group that can phenotype on genuine within-person change rather than
cross-sectional level — and it does, whether or not that was the paper's original framing
intent.

**What this means for the thesis:** the DS6 phenotype chapter should state plainly that (a)
its dominant axis (regime change) is a genuine, statistically significant, but singular
finding rather than a rich multi-dimensional typology; (b) the Bonferroni-significant
`self_control_index_change` overlay is DS6's strongest single result across the whole Step
1+2 program and should be foregrounded, with the explicit caveat that the phenotype boundary
itself is only marginally stable (Jaccard=0.714); and (c) DS6's phenotype exploration remains
less thoroughly cross-validated than DS5's at this point in the project (one pass + one
follow-up vs. six systematic paths + a revision arc) — a scope gap, not a quality defect in
what has been done so far.

---

*Written 2026-08-08 as part of the DS6 post-analysis reporting set.*
