# v2 Revision Arc — Addendum to the Original Data Usage Map and Phenotype Comparison

**Written:** 2026-08-07
**Purpose:** `model_data_usage_map.md` and `theory_vs_implementation_comparison.md`
(both 2026-04-20) and `phenotype_expectation_vs_result.md` (2026-04-20) were all written
before the DS5_02 "v2" revision arc (notebooks 60, 60b, 61, 62, 63, 64, 107, 108; completed
2026-08-05/06). This addendum extends those three documents' own tables and conclusions with
the v2 material, **without editing the originals**. Full per-notebook methods/results already
exist for every v2 notebook inside the corresponding DS5 paper_prep file
(`ds5_dys_paper_prep.md` §4.5, `ds5_stm_paper_prep.md` §4.5, `ds5_net_paper_prep.md`
[v2 no-self-loop section], `ds5_stop_paper_prep.md` §4.4, `ds5_phenotyping_paper_prep.md`
§3.3) — this document does not repeat that depth. Its job is narrower: for each v2 check,
state (a) what triggered it, (b) whether it materially changed the v1 conclusion, and (c)
what that means for the two original cross-cutting documents it extends.

---

## 1. Why the v2 arc happened at all

The trigger is recorded in CLAUDE.md and confirmed by `phenotype_expectation_vs_result.md`
itself: DS5's original Phase 1 phenotype split (`100_phenotype_exploration.ipynb`, April 2026)
was dominated by two NeT features at or near ceiling (`HHI_net` 0.84–0.86, `rho_self`
0.922–0.924 pooled). `theory_vs_implementation_comparison.md` §NeT already flagged this as a
concern in April ("the DS5 network features may have limited discriminatory power due to
ceiling effects... may be capturing 'which app has OneSec installed on it' rather than true
network topology"). The v2 arc is the direct empirical follow-up to that flagged concern: six
notebooks (60/60b/61/62/63/64) each re-derive one Step 1 or Step 2 quantity using a less
approximate or less ceiling-sensitive method, to test whether the original conclusions were
an artifact of the specific approximations flagged in April.

---

## 2. Per-check verdict: material change or not

| Notebook | What it re-derived | v1 approximation being tested | Verdict | Source of truth |
|---|---|---|---|---|
| 60 (DyS v2) | Genuine KDE-derived potential well V(x); β_v2 = V''(x*) at the primary stable fixed point | v1's `is_dys_eligible = (σ̂ < σ_median)` binary threshold, flagged in April as "conventional, not theoretically derived" | **Partial divergence** — only 66/414 (15.9%) participants have a genuine KDE-detected stable fixed point, far fewer than v1's ~50% (median-split) eligible count | `participant_dynamics_v2.md` |
| 60b (StM v2) | β_v2 = V''(x*), replacing β_behav = 2/σ̂² | FLAG A: "β=2/σ̂² is exact only for a potential-well SDE, not the constant-drift SDE actually fit" — the single most-flagged approximation in the April theory-vs-implementation doc | **Confirms the April concern was worth raising** — v2 uses the data-grounded potential rather than the constant-drift proxy; condition ordering is preserved, so the *qualitative* StM story survives, but the *mechanism* (β from KDE curvature vs. from σ̂ algebra) is genuinely different, exactly as FLAG A anticipated it should be checked | `participant_stm_parameters_v2.md` |
| 61 (NeT v2, no self-loops) | HHI_net/rho_self/H_pi recomputed with self-loops excluded | The April NeT concern verbatim: "ceiling effects... ​ HHI_net/rho_self may be capturing which app has OneSec installed, not true topology" | **Confirms the concern, decisively.** Once self-loops are removed, Profile B (the hub-dominated phenotype) turns out to be overwhelmingly single-app — the large majority of its participants have zero or near-zero cross-app transitions once same-app repeats are excluded. `HHI_net_v2` clusters tightly near 0.5 and `H_trans_v2` medians at 0.0. This is the single clearest confirmation in the whole v2 arc that a specific, named April concern was correct. | `participant_network_metrics_v2_no_selfloop.md` |
| 62 (StoP v2, MLE) | σ̂ via MLE instead of method-of-moments | April's FLAG 2: "MLE deferred" for σ̂/μ̂ estimation | **No material change.** Spearman ρ(σ̂_MLE, σ̂_MoM) = 0.9995; median relative deviation = 1.29%, fully explained by the Bessel correction (ddof=0 vs. ddof=1) — a known, benign estimator artifact, not new information about the underlying behavior. | `participant_parameters_v2_mle.md` |
| 63 (Phenotype v2, GMM k=2) | Re-clustered Phase 1 features with a Gaussian Mixture Model instead of k-means | Implicit April assumption that k-means' hard spherical-cluster boundary was an adequate description of the phenotype structure | **Material change.** ARI(GMM, k-means) = 0.346 (below the 0.70 material-change threshold used elsewhere in this project) — 85/289 (29.4%) of the original k-means Profile B participants are reassigned to GMM's Profile A. Layer 2 orthogonality (the NeT/behavioral-dynamic independence finding) still replicates exactly (ARI=0.000) under GMM, so the *structural* finding survives even though the *specific participant-level assignments* do not. | `ds5_gmm_phase1_assignments.md` |
| 64 (Phenotype v2, GMM k=3) | Extended the GMM to k=3 and to a full BIC/AIC sweep through k=6 | The implicit k=2 choice in both v1 and nb63 | **Bootstrap-stable but not BIC-mandated** — median bootstrap ARI=0.964 across 200 runs (very stable partition), but BIC decreases monotonically through k=6 with no interior minimum, meaning **k=3 is an interpretability choice, not a statistically preferred one**. This corrects an intermediate, since-retracted claim from nb63's own Phase B gate verdict ("BIC minimum at k=3"), which nb64 itself documents was an artifact of stopping an earlier sweep at k=5. | `ds5_gmm_k3_assignments.md` |

---

## 3. What this means for `model_data_usage_map.md` and `theory_vs_implementation_comparison.md`

Neither original document needs a correction — both explicitly flagged the concerns the v2
arc went on to test (FLAG A for StM; the σ-median threshold for DyS; the ceiling-effect
concern for NeT), so nothing here contradicts what April already said. What changes is the
**status** of those flags: they move from "flagged, untested" to "flagged, and empirically
resolved" — three (NeT ceiling effect, StM FLAG A, DyS threshold) were shown to matter in a
first-order way; one (StoP MoM-vs-MLE) was shown not to matter.

`model_data_usage_map.md`'s summary table (§"What is truly behavior-derived vs
questionnaire-dependent") remains valid without modification: every v2 quantity above is
still derived entirely from behavioral event data (or from other model outputs derived from
behavioral events), with no new survey dependency introduced anywhere in the v2 arc.

---

## 4. What this means for `phenotype_expectation_vs_result.md`

That document's Part 2 ("What Step 2 found") described a two-layer structure: Layer 1
(NeT-topological, orthogonal, ARI=0.020 vs. Layer 2) and Layer 2 (behavioral-dynamic,
C1/C2/C3). The v2 arc's most important finding for this document is specifically about
**Layer 1's own internal validity**, not about the two-layer orthogonality claim itself (which
nb63 independently reconfirms at ARI=0.000 under GMM — if anything, more strongly than the
original April k-means-only result).

The no-self-loop finding (notebook 61, above) means Layer 1's headline description — "hub-
dominated (Profile B, 70%) vs. distributed (Profile A, 30%)" — should be read going forward
with an explicit caveat: a large share of what "hub-dominated" measures in the original
(self-loop-inclusive) construction is single-app usage with repeated same-app opens, not
switching behavior *between* multiple apps concentrated on one hub. This does not overturn
the Layer 1/Layer 2 orthogonality finding (that used `HHI_net`/`rho_self` as a *label*, and
the label's stability is unaffected), but it does sharpen what should be claimed about *why*
Profile B looks the way it does in any thesis discussion: "concentrated app-switching
topology" is the v1-faithful description; "predominantly single-app users, with or without
switching" is the more precise v2-informed one.

Separately, the GMM k=3 solution (notebook 64) offers a *third* candidate description of
Layer 2 beyond the original C1/C2/C3 (from the six-path exploration) — G1
(N=153, distributed)/G2 (N=57, near-hub)/G3 (N=204, hub-locked). This is not currently
reconciled against the original Path A/F C1/C2/C3 labels in any existing document; doing so
would require a direct cross-tab (not performed as part of this addendum, and not attempted
here to avoid re-deriving analysis that belongs in a dedicated phenotyping notebook rather
than a post-hoc report). Flagged here as an open reconciliation item for any future DS5
phenotyping work, not resolved.

---

## 5. Net takeaway

The v2 arc functioned exactly as a robustness-check arc should: it did not invalidate any
headline DS5 finding, but it did convert three explicitly-flagged approximations (StM's
FLAG A, DyS's arbitrary median threshold, NeT's ceiling-effect concern) from open caveats into
either confirmed limitations (NeT, most decisively) or confirmed-but-structurally-preserved
approximations (StM, DyS), while ruling out one candidate concern entirely (StoP's MoM vs.
MLE choice was never a real issue). This is the kind of finding this project's own validation
principles ask for explicitly — checking an approximation rather than assuming it away — and
it should be cited as evidence of methodological care in any thesis discussion of DS5's Step 1
robustness, distinct from (and complementary to) the deeper per-family accounts in the
paper_prep documents.

---

*Written 2026-08-07 as part of the DS5 post-analysis update, alongside
`ds5_gat_abm_deferred_resolution.md` and `ds5_step3_personalization_addendum.md`.*
