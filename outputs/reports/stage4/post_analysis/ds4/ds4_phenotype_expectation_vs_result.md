# Phenotype Expectation vs. Phenotype Result — DS4

**Written:** 2026-08-08
**Overlap check:** Read in full before drafting — `outputs/reports/stage4/post_analysis/phenotype_expectation_vs_result.md` (DS5 template this document mirrors in structure/purpose), `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §1 (already records DS4's phenotype-layer geometry at a cross-dataset comparison level — cited below, not re-derived), `outputs/reports/stage4/step2_phenotyping/ds4_phenotyping_blueprint.md`, `ds4_step2_exploration_plan.md`. This document grounds Parts 1–3 entirely in DS4's own blueprints and executed outputs, not in DS5's numbers or in the cross-dataset synthesis's summary-level framing.
**Purpose:** Compare the phenotype dimensions anticipated by the paper/theory for DS4 against what Step 2 (Phase 1 + Paths A′/C′/F′) actually found.

---

## Part 1 — Phenotypes theoretically expected

Unlike DS5, DS4 has no single consolidated construct-mapping table in its own blueprint set (DS5's §4.3 equivalent). The anticipated phenotype dimensions instead appear piecemeal, each tied to the model family that names it:

| Anticipated dimension | Expected operationalization | Model family / source |
|---|---|---|
| **Behavioral relaxation speed / habitual reversion** | Fast vs. slow return to personal baseline after disruption | StoP (`tau_hat`, `theta_hat_OU`) — DS4's own "no DS5 equivalent" quantity |
| **Potential-well depth ("steep vs. shallow wells")** | Steep wells (high θ̂): fast reversion, harder to shift, but also less susceptible to small perturbations. Shallow wells (low θ̂): slower reversion, more volatile, but more susceptible | StM (`ds4_stm_blueprint.md` §12: "Participants with steep wells... return quickly to baseline — they are harder to shift. Participants with shallow wells... are more susceptible but also more volatile.") |
| **Threshold dependence / susceptibility** | Near-tipping-point participants | StM (`chi_OU`) |
| **Behavioral unpredictability** | Empirical entropy of the daily override-rate distribution | InT (`H_emp`) |
| **Model-fit quality / regime adherence** | How well an OU (mean-reverting, single-attractor) description fits a participant's real dynamics | DyS (`fixed_point_deviation`) |
| **Network centralization / habitual app concentration** | Self-transition rate, attempt-only construction | NeT (`rho_self`) — completing the "5-family feature set... mirrors DS5's Layer 1/Layer 2 structure question" (`ds4_net_blueprint.md` §8) |
| **Named strategic archetypes** | Commitment-oriented, reward-oriented, chronic overrider, adaptive switcher, friction-avoidant | GaT (paper §2.6, quoted in `ds4_gat_blueprint.md` §2) |
| **Long-run adaptation / habit formation** | Directional change in override rate over calendar time | Stage 1 feature `open_rate_change_calendar` — named across multiple DS4 documents (`ds4_features.md`, `cross_dataset_implementation_strategy.md`) as "DS4's strongest dataset-specific contribution" and the project's best-positioned dataset for this construct given 897-day windows |

**Implicit expectation carried over from the project's general framework** (CLAUDE.md's phenotyping principles): multiple, at-least-partially-independent behavioral dimensions (relaxation speed, susceptibility, entropy, model-fit quality, network concentration) combining into a multidimensional profile, not a single label — the same expectation DS5 and Structured were each tested against.

**A DS4-specific expectation not present for DS5:** because DS4's model family is fully rigorous (exact OU Boltzmann bridge, true interior attractor — see `ds4_theory_vs_implementation_comparison.md`), there was an implicit expectation that DS4's phenotype space might be *cleaner* or more clearly structured than DS5's approximation-riddled one — i.e., that resolving DS5's mathematical approximations might also resolve some of DS5's phenotype-structure ambiguity (DS5's own dominant finding was that its 8–10 anticipated dimensions collapsed to ~3 genuinely independent axes).

---

## Part 2 — What Step 2 actually found

### Phase 1 — Global phenotyping (N=641, k=3)

Five features, one per completed model family, redundancy-checked before clustering (no pair exceeds |r|=0.483 — a **genuinely 5-dimensional feature set**, not 1–2 dominant axes hiding behind 5 labels, unlike DS5's Phase 1). k=3 selected via a stability-first correction (silhouette-argmax k=4 was unstable, Jaccard=0.665; k=3 is the highest-silhouette **stable** candidate, Jaccard=0.849).

- **Cluster 0 (N=200):** fast reversion, lowest entropy, best OU model fit, by far the **highest susceptibility** (χ_OU mean 13.88 vs. ~5.5–5.8 for the other two) — participants closest to a behavioral tipping point in the StM sense.
- **Cluster 1 (N=363, largest):** fast reversion, moderate-high entropy, highest self-transition rate (0.753).
- **Cluster 2 (N=78, smallest):** by far the **slowest reversion** (τ̂ mean 1.70 days vs. ~0.6–0.7 for the others) and the **worst OU model fit** (fixed_point_deviation mean 0.038, ~5–7× the other two) — participants whose daily override-rate dynamics are least well described by the OU assumption at all.

PC1+PC2 explain 60.4% of variance; PC1 separates high-entropy/low-susceptibility from low-entropy/high-susceptibility participants, PC2 separates slow-relaxation participants from the rest — a genuinely two-dimensional structure, not one dominant axis. Hierarchical (Ward) clustering triangulates moderately (ARI=0.597 vs. k-means) — real agreement, not identical, not spurious.

### Path A′ — Behavior-only, drop NeT (N=641, k=4)

**ARI vs. Phase 1 = 0.664 (HIGH).** Dropping `rho_self` barely changes the taxonomy — the finer k=4 split mostly subdivides Phase 1's cluster 2 (slow-reversion, poor-fit group) into two more specific groups (one very slow, τ̂=1.90; one with the single worst model fit, fixed_point_deviation=0.069). **DS4's phenotype space is primarily behavior/thermodynamics-driven, not network-driven.**

### Path C′ — Network-focused (N=641, k=3, using only `rho_self` + `I_consec`)

**ARI vs. Phase 1 = 0.047 (near-zero, essentially orthogonal).** This is DS4's cleanest, most stable clustering result of the entire arc (silhouette=0.5147, bootstrap Jaccard=0.9658). Cluster 2 (N=103) stands out with much higher `I_consec` (0.42 vs. ~0.05–0.09 elsewhere) — a genuinely separate signal (predictability of app-to-app transitions, independent of raw self-repetition) that Phase 1's blended feature set (one NeT feature diluted among four behavioral ones) barely captures on its own.

### Path F′ — Joint taxonomy (Path A′ × Path C′, N=641)

**χ² = 31.44, dof=6, p<0.0001** — the two axes are **not independent**, but the association is far from total (min expected cell=4.3, several cells have real but modest counts). The largest standardized residual (+3.06) is Path A′ cluster 0 (highest-susceptibility group) paired with Path C′ cluster 1 (lowest `rho_self`, most network-distributed group) — i.e., DS4's highest-susceptibility behavioral phenotype is *somewhat* over-represented among network-distributed (not hub-locked) participants, a real but partial coupling.

### GaT's independent rule-based phenotypes, as a convergent cross-check (not itself a clustering path)

`gat_phenotype` (rule-based, not clustering) shows strong association with Phase 1's clusters (χ²=136.4, p<0.0001) — chronic_overrider concentrates in Phase 1's highest-susceptibility cluster 0 (131/232=56%). This is convergent validity between two independently-built model families, not a new phenotyping path, but it strengthens confidence that Phase 1's cluster 0 (susceptibility-dominant) is a real, recoverable, cross-method-stable group.

---

## Part 3 — Where expectations and results matched

### Match 1: Susceptibility as a real, recoverable phenotype axis

**Expected:** threshold-dependence / susceptibility as an identifiable phenotype dimension (StM's own framing).
**Found:** YES, strongly. Phase 1's cluster 0 is unambiguously the high-susceptibility group (χ_OU mean 13.88, more than double the other two clusters), and this same group is independently recovered by GaT's rule-based `chronic_overrider` phenotype (χ²=136.4) — two structurally unrelated methods converge on the same participants.
**Match quality:** Strong, and stronger than DS5's equivalent finding, because DS4 has a genuine cross-model convergence check (GaT vs. Phase 1) that DS5's own susceptibility finding did not have in the same form.

### Match 2: Relaxation speed / model-fit quality as a phenotype axis

**Expected:** fast-vs-slow habitual reversion as a meaningful individual-difference dimension (StoP/StM's "well depth" framing).
**Found:** YES — Phase 1's cluster 2 is unambiguously the slow-reversion, poor-model-fit group, and Path A′ subdivides it further into a "very slow" group and a "worst-fit" group when the network feature is removed and one more cluster is allowed.
**Match quality:** Strong, though the theoretical framing anticipated a clean two-way split (steep vs. shallow wells); the data instead shows this dimension co-varying with the OU model's own fit quality (`fixed_point_deviation`) — participants whose reversion is slowest are also the participants the OU model describes worst. This is a real, non-trivial finding not explicitly anticipated: slow reversion and poor OU-model-fit are not conceptually the same thing but travel together empirically.

### Match 3: Network structure as a real, partially independent phenotype dimension

**Expected:** network centralization (habitual app concentration) as one dimension among several (NeT's own framing, "Layer 1/Layer 2" language echoing DS5's).
**Found:** YES, but with a **different dominance direction than DS5**. Path C′ is a real, extremely stable, near-orthogonal axis (ARI=0.047 vs. Phase 1) — network structure is not just noise, it is DS4's cleanest single clustering result. But unlike DS5 (where network topology *dominated* the blended Phase 1 solution, ARI=0.990), DS4's Phase 1 is dominated by the behavioral/thermodynamic features instead (Path A′ ARI=0.664).
**Match quality:** Moderate — the dimension exists and is real, exactly as anticipated, but its *relative* importance in the blended feature space is the opposite of what DS5 found, which was not itself an explicit DS4-specific prediction (the "Layer 1/Layer 2" framing anticipated a two-layer structure in general, not which layer would dominate).

### Match 4: Named strategic archetypes (GaT) are recoverable and behaviorally meaningful

**Expected:** the paper's named phenotypes (commitment-oriented, reward-oriented, chronic overrider, adaptive switcher, friction-avoidant).
**Found:** 4 of 5 are directly operationalized with substantial group sizes (352/304/190/140) and each shows theoretically sensible differentiation on independent outcomes: chronic overriders show highest susceptibility and least adaptation-trajectory change (most behaviorally "locked in," mean |open_rate_change_calendar|=0.080); commitment-oriented and adaptive-switcher participants show more trajectory change (0.156, 0.154).
**Match quality:** Strong for 4/5 named types; the 5th (friction-avoidant) could not be operationalized at all — an honest, stated gap, not a failed prediction, since the paper's own text does not specify a measurable behavioral signature for this type distinct from commitment-oriented.

---

## Part 4 — Where expectations and results differed

### Difference 1: Rigor did not translate into a cleaner or lower-dimensional phenotype space

**Expected (implicit):** because DS4's underlying models are mathematically more rigorous than DS5's (exact OU Boltzmann bridge vs. approximate), the phenotype space might show clearer, better-separated structure.
**Found:** DS4's Phase 1 feature set turned out to be **genuinely more independent** than DS5's (no feature pair exceeds |r|=0.483, vs. DS5's Phase 1 which was effectively 1–2 dominant axes behind 5 labels) — but this did not translate into cleaner cluster separation. Silhouette scores across all of DS4's phenotyping (Phase 1: 0.227–0.275; Path A′: 0.265–0.348; Path C′: 0.40–0.51) are comparable to or only modestly better than DS5's own (DS5's Phase 1 silhouette was in a similar range). **Mathematical rigor in the underlying model family and empirical cluster separability are independent properties** — a genuinely informative, non-obvious finding worth stating in the paper rather than assumed.

### Difference 2: The dominance relationship between network and behavioral axes is reversed relative to DS5, and only partially independent — not a mirror image

**Expected (only implicitly, via the general "Layer 1/Layer 2" framing):** a two-layer structure similar in kind to DS5's.
**Found:** DS4 does have two layers, but the relationship is not simply DS5's inverted. DS5's two layers were **fully orthogonal** (ARI=0.020). DS4's Path F′ shows the two layers are **statistically coupled** (χ²=31.44, p<0.0001) even though each axis considered alone is largely independent of the blended Phase 1 solution's *other* axis. This is a third, distinct phenotype-layer geometry in the project's growing catalogue — see `cross_dataset_cas_model_synthesis.md` §1, which already records DS4 as "coupled, but each individually low-overlap with the blended Phase-1 solution," a genuinely different pattern from DS5's full orthogonality, Structured's strong coupling (Path A ARI=1.000), and DS6's third-axis-dominance pattern. This document adds the underlying mechanics DS5's synthesis doesn't: the coupling is driven specifically by the highest-susceptibility behavioral group being somewhat over-represented among network-distributed (not hub-locked) participants (Path F′'s largest standardized residual, +3.06).

### Difference 3: Adaptation over repeated exposure — measurable in DS4, but not incorporated into the phenotype feature set itself

**Expected:** DS4's 897-day windows were specifically named (in `cross_dataset_implementation_strategy.md` and `ds4_features.md`) as the project's best opportunity to observe "adaptation over repeated exposure" as a phenotype dimension — a construct DS5's 6-week windows could not test at all.
**Found:** `open_rate_change_calendar` is real, computed, and used — but **only as a GaT cross-check** (ANOVA F=35.57, p<0.0001 by `gat_phenotype`), not as one of Phase 1's five clustering features. Phase 1's five features are all instantaneous/aggregate characterizations (relaxation speed, entropy, fit quality, susceptibility, network concentration) — none of them directly encode a trajectory-over-time quantity. This means DS4's headline longitudinal-adaptation capability, repeatedly named elsewhere in the project as DS4's unique strength, was **not built into the phenotype taxonomy itself** — it surfaces only as a validated post-hoc differentiator of GaT's independently-defined rule-based groups. This is a genuine gap between what DS4 could contribute to the phenotype picture and what Phase 1 actually asked it to contribute — worth flagging directly rather than allowing the paper to imply Phase 1 "used" DS4's longitudinal strength.

### Difference 4: Psychosocial/demographic interpretability essentially absent, more severely than DS5's own qualifications anticipated

**Expected:** DS4's blueprints repeatedly and correctly flagged, in advance, that DS4 has "no validated Likert scales" and would have "much less psychosocial content than DS5" (`ds4_stm_blueprint.md` §2.4). This was an accurate expectation set in advance, not a surprise.
**Found:** exactly as expected, and even thinner in practice than the advance caveat implied — the demographic overlay covers only 149/641 (23.2%) of the complete-case phenotyping population (since DS4's survey covers only 283/1,039 participants overall, and phenotyping requires the smaller StoP-valid complete-case population), and the one test run (age by cluster) is null (F=1.564, p=0.213). **DS4's phenotype clusters have essentially zero psychosocial or demographic interpretive content** — a more severe version of an already-correctly-anticipated limitation, not a new finding, but worth stating with its exact magnitude (23.2% coverage, null result) rather than only qualitatively.

### Difference 5: Named strategic archetypes (GaT) turned out to be a restatement of the susceptibility axis, not an independent dimension

**Expected (implicit in the paper's naming of 5 distinct archetypes):** the strategic-archetype framing was presented as adding a genuinely new dimension beyond the thermodynamic/network characterization.
**Found:** the strong GaT-Phase1 convergence (χ²=136.4) is good news for construct validity (two methods find the same group) but bad news for dimensionality — it means `gat_phenotype`'s chronic-overrider/commitment-oriented axis substantially **restates** the StM susceptibility axis rather than adding an independent one, exactly as the cross-dataset synthesis already concludes for DS4's GaT specifically (`cross_dataset_cas_model_synthesis.md` §2: "the trait-like GaT signal that does exist is really a restatement of the StM/susceptibility axis, not an independent one"). The paper should not present GaT's phenotype vocabulary as a 6th independent phenotype dimension alongside Phase 1's five features — it is better described as a differently-labeled view of dimensions Phase 1 already captures (chronic_overrider ≈ high chi_OU), plus one genuinely new piece of information (the adaptation-trajectory differentiation, Difference 3 above).

---

## Part 5 — Did the pipeline itself change what phenotype structure was visible?

**Yes, in the same structural sense DS5's own pipeline did, but with a different specific lesson.**

1. Choosing to include `rho_self` in Phase 1 alongside four thermodynamic/informational features gave the network dimension a real but secondary role in the blended solution — necessary to have run Path A′ and Path C′ separately to see that the network axis, while real and highly stable on its own (Path C′), is not what drives Phase 1's own k=3 split (Path A′ ARI=0.664 shows Phase 1 ≈ behavior-only).

2. Path F′ was only possible, and only informative, because Path A′ and Path C′ were run as fully separate, independently-selected-k clusterings first — exactly mirroring DS5's own Path F precedent (cross Path A × Path C after both exist as real, stable results) rather than being planned as a fixed 4-cell design in advance.

3. **A genuinely DS4-specific pipeline lesson not present in DS5's version of this section:** the phenotyping blueprint's own k-selection correction (rejecting the naive silhouette-argmax k=4 for the stable k=3) directly shaped which cluster structure became "Phase 1" at all — had the naive method been followed, Phase 1 itself would have reported an unstable 4-cluster solution, and every downstream comparison (Path A′'s ARI, Path F′'s cross-tab) would have compared against a different, less trustworthy baseline.

---

## Part 6 — Are the "phenotypes we assumed" and the "phenotypes we found" meaningfully different?

**Short answer: partially, and in a more nuanced way than a simple match/mismatch.**

**Where the assumption held up well:** the individual dimensions named piecemeal across DS4's blueprints (relaxation speed, susceptibility, entropy, model-fit quality, network concentration) all turned out to be real, and — a genuinely positive result relative to DS5 — largely independent of each other in Phase 1's own feature space (no pair exceeds |r|=0.483). DS4 did **not** reproduce DS5's central finding that a rich theoretical vocabulary collapses to ~3 empirically independent axes; DS4's 5-feature set held up as genuinely 5-dimensional.

**Where the assumption did not hold up:** the *relative importance* and *coupling structure* between the network and behavioral layers is a third distinct geometry in this project's catalogue (coupled-but-partial, not fully orthogonal like DS5, not fully dominant like Structured's Path A, not third-axis-dominated like DS6). This was not predictable from DS4's own advance planning documents, which — reasonably — expected a DS5-style Layer 1/Layer 2 structure without predicting which layer would dominate or how tightly coupled they would be.

**What this means for the thesis:** DS4 should not be presented as "confirming DS5's phenotype-layer geometry with more rigorous underlying models." It should be presented as a **third, distinct case** in the growing cross-dataset catalogue of network-vs-behavioral phenotype relationships — behaviorally dominant (like Structured) but with a real, statistically detectable coupling to network structure (unlike Structured's own coupling, which is even stronger, ARI=1.000) and unlike DS5's full orthogonality. The paper's strongest, most defensible claim across all datasets examined so far (DS5, Structured, DS6, DS4) is the one already stated in `cross_dataset_cas_model_synthesis.md` §4: digital-behavior phenotype heterogeneity in this domain does not reduce to one universal network-vs-behavioral template, and DS4 is direct, independent supporting evidence for that claim, not a replication of any single prior dataset's specific pattern.

---

## Source documents

- `outputs/reports/stage4/step2_phenotyping/ds4_phenotyping_blueprint.md`, `ds4_step2_exploration_plan.md`
- `outputs/model_outputs/ds4_phenotyping/model_run_summary.md`, `ds4_phenotype_feature_matrix.md`, `ds4_cluster_profiles.md`, `path_a_feature_matrix.md`, `path_a_cluster_profiles.md`, `path_a_model_run_summary.md`, `path_c_feature_matrix.md`, `path_c_cluster_profiles.md`, `path_c_model_run_summary.md`, `path_f_summary.md`, `path_f_model_run_summary.md`, `ds4_demographic_overlay.md`
- `outputs/model_outputs/ds4_game_theory/participant_gat_phenotypes.md`, `gat_phenotype_crosstab.md`, `model_run_summary.md`
- `outputs/reports/stage4/step1_modeling/ds4_stm_blueprint.md` §12, `ds4_net_blueprint.md` §8, `ds4_gat_blueprint.md` §2
- `outputs/features/ds4/ds4_features.md`
- `outputs/reports/stage4/cross_dataset_implementation_strategy.md`
- `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §1, §2, §4

---

*Written 2026-08-08 as part of the DS4 post-analysis synthesis, mirroring the DS5 template (`outputs/reports/stage4/post_analysis/phenotype_expectation_vs_result.md`).*
