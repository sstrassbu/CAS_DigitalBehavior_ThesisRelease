# Structured Retrospective Dataset — CAS Modeling Plan & Data-Sufficiency Analysis

**Status update (2026-08-05, fourteenth update — Path F complete, all four Step 2 exploration notebooks
now done):** Blueprint: `structured_path_f_blueprint.md`. Notebook:
`notebooks/123_structured_hierarchical_phenotype.ipynb`. Outputs:
`outputs/model_outputs/structured/phenotyping/path_f/`. Deliberately **not** a re-run of DS5's literal
Path F (fresh within-group clustering) nor of Path C's own Part 4 (already did local NeT sub-clustering)
— instead crosses Path A's and Path C's already-fitted global clusterings into the first actual named
joint taxonomy, with an independence test.

**Joint taxonomy (N=36): BehavProfile × NetProfile cross-tab = 4 / 18 / 8 / 6** (largest cell:
BehavProfile A × NetProfile B, half the population — matches the lopsidedness predicted in the blueprint
before running). **Fisher's exact test: p=0.029, odds ratio=0.167 — the two axes are NOT independent.**
This is the notebook's substantive contribution: it reconciles Path A's ARI=1.000 and Path C's ARI=0.173
into one coherent picture — **one dominant axis (behavioral) with a real, statistically detectable,
weaker secondary axis (network) that is not simply noise.** Clean run, no bugs — the first of the four
exploration notebooks to execute correctly without a fix.

**All four Step 2 exploration notebooks (A/C/D/F) are now complete.** Path B (intervention-sensitive) was
never built — no Structured analog exists. Path E (condition-stratified) was folded into Path A as a
short appended check. Summary across all four: Structured's phenotype structure is dominated by
behavioral dynamics (opposite emphasis from DS5's network-dominant finding), with network topology
playing a real but secondary, statistically-detectable role (Path F), and the secondary/robustness
feature set (Path D) showing no independent structure of its own at this N. A full synthesis note
mirroring `ds5_step2_master_synthesis.md` is the next step.

---

**Status update (2026-08-05, thirteenth update — Path D complete, a genuine null result):** Blueprint:
`structured_path_d_blueprint.md`. Notebook: `notebooks/124_structured_dynamic_stochastic_phenotype.ipynb`.
Outputs: `outputs/model_outputs/structured/phenotyping/path_d/`. Five secondary features
(`created_mu_hat`, `volume_trend_slope`, `dropout_score`, `H_hour_creation`, `persistence_rate`; `H_config`
dropped, replicating Phase 1's own r=0.665 H_config/H_completion redundancy finding), N=41 (identical to
Path A).

**Result: no feasible k.** Every candidate k (2, 3, 4) had `min_cell=1` — every partition was driven by a
single extreme outlier (`volume_trend_slope=-32.14`, the same participant DyS's own report already named
as "driving most of the spread"). Reported as infeasible, matching this project's own default-condition
precedent from DS5's Path E, rather than forced into a degenerate split.

**A real bug was caught before reaching that honest result:** the k-selection fallback
(`max(valid_ks,...) if valid_ks else 2`, copied verbatim from Path A/Phase 1) silently defaulted to k=2
when `valid_ks` was empty, producing a 1-vs-40 "cluster" with a spuriously high bootstrap Jaccard (0.893)
— an artifact of an isolated outlier being trivially easy to re-isolate under resampling. Caught by
reading the printed cluster sizes before accepting the result; fixed with an explicit `NO_FEASIBLE_K`
branch. Two stale output files from the pre-fix run (a cluster-profile CSV and its figure) were also
found still on disk after the corrected run and deleted — the fix correctly stops generating them, but
the earlier run's copies had not been cleaned up.

**This null result is itself the finding, consistent with and extending DS5's own conclusion:** DS5's own
Path D was already its lowest-yield path at N=285 (found a stable k=2 that mostly reproduced Path A).
Structured's much smaller N does not even support that much.

---

**Status update (2026-08-05, twelfth update — Path C / Layer 1 analog complete):** Blueprint:
`structured_path_c_blueprint.md`. Notebook: `notebooks/121_structured_network_subphenotype.ipynb`.
Outputs: `outputs/model_outputs/structured/phenotyping/path_c/`. Reframed from DS5's original Path C
question (DS5 asked about substructure within a NeT-*dominated* profile; Structured's isn't one) into a
direct triangulation test against Path A's result.

**Full-sample NeT-only clustering (N=45, features HHI_net/rho_self/H_trans/H_state_marginal,
`top1_share_net` dropped for r=0.961 collinearity with HHI_net): k=2, bootstrap Jaccard=0.822 STABLE.
ARI(Path C vs. Phase 1) = 0.173** (DS5's equivalent was 0.990). Low as predicted, but not as close to
zero as DS5's fully-orthogonal case (0.020) — classified PARTIAL, not CONFIRMED-orthogonal: NeT carries
some real signal, just clearly secondary to the behavioral axis Path A already showed dominates
(ARI=1.000). **Two independent notebooks now triangulate the same conclusion: Structured's phenotype
structure is overwhelmingly behavioral-dynamic, with network topology playing a real but minor role — the
inverse emphasis from DS5.**

Sub-clustering within Phase 1's Profile A (N=22) and Profile B (N=14) on NeT features alone both produced
bootstrap-stable 2-way splits (Jaccard=0.872, 0.965) using N-scaled `min_cell` floors (6 and 4,
proportionally derived from Phase 1's own N=36→min_cell=10 rule) — but per the blueprint, reported as
tentative regardless of the stability numbers, matching DS5's own caution at 6-9x this N. Path F will
test whether this sub-structure holds up independently.

---

**Status update (2026-08-05, eleventh update — Step 2 exploration begun: Path A / Layer 2 analog
complete):** Following the full sanity-check audit of all 8 model families (all headline numbers
recomputed directly from the CSVs and confirmed correct — see the blueprint checklists, now all closed
out), the user requested extending Step 2 phenotyping to mirror DS5's six-path exploration
(`outputs/reports/stage4/ds5_step2_phenotype_exploration_plan.md`,
`.../post_analysis/ds5_step2_master_synthesis.md`). A mapping document,
`structured_step2_exploration_plan.md`, adapts each DS5 path to what Structured's data can actually
support rather than porting all six mechanically: **Path B (intervention-sensitive) does not port at
all** — it needs `H_out`, friction-outcome entropy, and Structured has no friction intervention; **Path E
(condition-stratified) shrinks to a short appended check** — DS5 used three randomized RCT arms,
Structured's only stratifier is observational free/pro subscription (11-12 free at this N, already far
below where even DS5's own thinnest condition arm, N≈137, struggled). Paths A, C, D, F port with
adaptation and get their own notebooks (122, 121, 124, 123).

**Path A (behavior-only, Layer 2 analog) — complete.** Blueprint: `structured_path_a_blueprint.md`.
Notebook: `notebooks/122_structured_behavior_only_phenotype.ipynb`. Outputs:
`outputs/model_outputs/structured/phenotyping/path_a/`. Population N=41 (6 non-NeT curated features;
confirmed NeT eligibility was not the binding constraint — DyS/StoP are tighter). k=2 selected
(silhouette=0.237; k=3/4 fail min_cell≥10), bootstrap Jaccard=0.885 **STABLE**.

**Headline result — the central Path A question, answered decisively: ARI(Path A vs. Phase 1) = 1.000**
on the N=36 overlap (perfect cross-tabulation). This is the **mirror image of DS5**: DS5's Path A was
orthogonal to its Phase 1 (ARI=0.020) because DS5's Phase 1 was NeT-dominated; Structured's Phase 1 was
already shown (Part 0 of the blueprint, verified against `cluster_profiles.csv` before running anything)
to have only a weak NeT gap (HHI_net 0.505 vs. 0.573) compared to its behavioral-feature gaps
(state_space_volatility 1.71 vs. 0.55, Fano 7.49 vs. 4.61) — so removing NeT entirely removed almost
nothing from the split. **Structured's dominant phenotype axis is behavioral-dynamic, not
network-topological — the opposite emphasis from DS5.** This was a stated, falsifiable prediction before
running (blueprint Part 4), not a post-hoc explanation.

**Path E analog result:** free subgroup (N=12) k=2 → 9/3 split, min_cell=3, correctly ruled infeasible.
Pro subgroup (N=29) k=2 → 15/14, min_cell=14, genuinely feasible, bootstrap Jaccard=0.895 STABLE.

**Two bugs caught and fixed:** (1) an f-string double-brace escaping mistake in the summary-generation
cell, caught before execution by checking the escaping convention against the working
`build_120_phenotype.py` precedent; (2) the Path E feasibility gate initially used an inconsistent
`min_cell<3` bar (vs. the `min_cell≥10` floor used everywhere else in the same notebook), which would
have mislabeled the free subgroup's 9/3 split as "feasible, STABLE" — caught by noticing the printed
bootstrap Jaccard (0.869) looked suspiciously high for such a lopsided split, and confirming the gate was
inconsistent with the rest of the notebook's own standard. Fixed to use the same `MIN_CELL=10` throughout.

---

**Status update (2026-08-05, tenth update — ALL 8 CAS MODEL FAMILIES NOW COMPLETE FOR STRUCTURED):**
Agent-Based Modeling (ABM), the final deferred family, is now implemented and executed — unblocked by
Step 2 phenotyping per this project's own established rule. Notebook:
`notebooks/67_structured_agent_based.ipynb`. Blueprint: `structured_abm_blueprint.md`. Outputs:
`outputs/model_outputs/structured/agent_based/`.

**Design:** not redundant with StoP (estimation vs. generation) or Step 2 (description vs.
dynamic-plausibility testing) — checked explicitly before coding. Two generative models, both with
expected results stated in the blueprint *before* running: Model 1 (static per-agent Poisson rate, no
temporal structure) as a naive-heterogeneity baseline; Model 2 (two-state session on/off, one added
mechanism, one simplifying assumption — fixed 3-day mean session length) as the test of whether minimal
added structure closes the gap to real burstiness. All agent rules read directly from already-fitted
StoP/Stage-1/Step-2 outputs, not re-estimated from raw data, per the paper's own instruction.

**Results:**
- Model 1: Fano≈1.02 (confirms the mathematically expected Poisson result; not a discovery, a
  quantified baseline) vs. real Fano≈6.01 — confirms static heterogeneity alone cannot explain observed
  burstiness.
- Model 2: Fano≈3.38 — closes **47% of the gap** between Model 1 and real (a real bug caught before
  reporting: a first draft's hard-coded interpretation text said "closes most of the gap" based on a
  sloppy threshold; the actual, correctly computed figure is under half).
- **Strongest result: individual-agent rank correlation (real Fano vs. Model 2 simulated Fano) = 0.914.**
  The model identifies *which* agents are burstier than others very well, even though it undershoots the
  *population-level magnitude* — an honest, nuanced two-part finding rather than a single pass/fail verdict.
- Phenotype mixture test (Profile A/B as two archetypal agent types, real mixture proportion): separation
  *magnitude* well reproduced (KS statistic 0.351 real vs. 0.375 simulated — comparable, unlike the
  p-values, which are not comparable given the very different real n=22/14 vs. simulated n=200/200) —
  **but direction is reversed** (real: A > B, 7.49 vs. 4.61; simulated: B > A, 5.04 vs. 4.60). Caught by
  explicitly checking direction rather than accepting the magnitude match at face value. Collapsing each
  profile to a single mean rule-set loses enough within-profile heterogeneity to flip which group looks
  burstier — a genuine, reported limitation, not reframed as a clean success.

**Two implementation bugs caught before running, both from reviewing the simulation code rather than
its output:** (1) `p_on` (a Markov transition probability) could mathematically exceed 1.0 for
high-`f_active` agents — didn't crash anything but was fixed to a proper `[0,1]`-clipped probability for
correctness; (2) the phenotype-mixture simulation used Python's built-in `hash()` for a per-profile RNG
seed offset, which is randomized per-process by default and would have made the simulation
non-reproducible run-to-run — fixed with a deterministic seed mapping.

**Overall interpretation:** simple local rules are *partially* sufficient (strong individual rank
reproduction, meaningful but incomplete magnitude reproduction, direction-reversed at the coarsest
2-archetype level) — a genuinely mixed, honestly-reported result consistent with this project's
practice of not reframing partial or null findings as clean successes.

**All 8 CAS model families (NeT, InT, StoP, DyS, SyD, StM, GaT, ABM) are now implemented for
Structured — Step 1 and Step 2 are both complete.**

---

**Ninth status update (2026-08-03):** Phenotyping across all 7
Step 1 model families is now implemented and executed. Notebook:
`notebooks/120_structured_phenotype_exploration.ipynb`. Blueprint (scoped deliberately to one clustering
pass, not DS5's six-path exploration, given Structured's much smaller N):
`structured_phenotyping_blueprint.md`. Outputs: `outputs/model_outputs/structured/phenotyping/`.

**Sample:** N=36/61 (59%) complete-case across all 7 curated features (one per model family: `HHI_net`
[NeT], `H_completion` [InT], `created_Fano_factor` [StoP], `state_space_volatility` [DyS],
`backlog_trend_slope` [SyD], `susceptibility` [StM], `mean_commitment_score` [GaT] — each checked for
redundancy against the others before inclusion; `susceptibility` was picked over StM's `H_config` for
exactly this reason, r=0.195 vs. r=0.665 against InT's `H_completion`). Checked relaxing eligibility to
gain N — only 36→39, not worth losing 2 full model families from the radar, so not pursued.

**Clustering result:** k=2 selected (only k meeting the N-adjusted minimum-cell-size≥10 threshold;
silhouette=0.213). **Bootstrap Jaccard stability = 0.775 (STABLE)** over 100 resamples — a real,
reasonably robust two-cluster structure despite the small N. PC1+PC2 explain 56.9% of variance
(indicating genuine multi-dimensionality across the 7 curated features, not just 1-2 dominant axes).
One redundant pair surfaced by the notebook's own check that wasn't caught at design time:
`H_completion` (InT) correlates r=0.68 with `state_space_volatility` (DyS) — noted as a limitation, not
fatal (both still retained; only pairs the design explicitly checked were guaranteed clean in advance).

**Profile A (N=22) vs. Profile B (N=14) — a genuine cross-model finding invisible in any single Step 1
notebook:** Profile A is higher on `state_space_volatility` (1.71 vs. 0.55), `created_Fano_factor` (7.49
vs. 4.61), and `H_completion` (1.16 vs. 0.57) — the more volatile, bursty, less-predictable-outcome
group — **but has a much slower backlog growth trend** (`backlog_trend_slope` 2.04 vs. 5.96) than the
calmer Profile B. The "steadier" profile accumulates backlog faster; the "burstier" one appears to use
its burst episodes to keep backlog in check. This is exactly the kind of relationship Step 2 phenotyping
is meant to surface — no single Step 1 model computed both a volatility measure and a backlog measure
together.

**Psychosocial overlay (N=33, exploratory, secondary per the blueprint's explicit scoping):** no scale
survives Bonferroni correction. `pct_planned_tasks_completed_num` is nominally significant before
correction (raw p=0.028) but not after (p=0.14) — consistent with DS5's own Step 2 finding that
psychosocial overlays were mostly null even at N=573; not over-read here at N=33.

**The radar chart** (`fig4_phenotype_profiles_enhanced_notitle.png`) required 3 layout iterations after
the first draft: the "Model families" legend (7 entries, vs. the DS5 original's 4) initially collided
with axis labels and chart data on both sides. Fixed via a 2-column legend layout, enlarged figure
height, and retuned margins/anchor positions — iterated until visually clean, matching the reference
image's polish level, per the explicit priority placed on this output.

---

**Eighth status update (2026-08-03):** Game Theory
(GaT), the final active model family, is now implemented and executed. Notebook:
`notebooks/66_structured_game_theory.ipynb`. Blueprint: `structured_gat_blueprint.md`. Outputs:
`outputs/model_outputs/structured/game_theory/`. **All 7 active Structured model families
(NeT/InT/StoP/DyS/SyD/StM/GaT) are now complete; ABM remains deferred until a phenotyping stage exists,
matching this project's DS5 precedent.**

Per the paper's §1.3 caution grouping GaT with StM (both "require more careful proxy definitions"), no
formal game matrix, best-response analysis, or equilibrium concept was built — an explicit named
`commitment_score` proxy (0–5, built strictly from the paper's own listed signals: temporal type,
recurrence, subtasks, duration — alerts excluded, confirmed unavailable) and correlational outcome tests
instead. An explicit non-redundancy check against StM/NeT/SyD confirmed the commitment index and
trade-off-curve test were genuinely new before any code was written.

**A real bug was caught by cross-checking the full printed output against the generated summary, not by
a built-in assertion this time:** two unrelated within-participant correlation tests (commitment↔outcome
in one section, reschedule↔commitment in another) reused the same variable names (`r_within`/`p_within`),
so the auto-generated `model_run_summary.md` silently reported the *second* test's numbers under the
*first* test's heading. Caught by reading the full notebook output line-by-line and noticing the printed
value from the earlier cell (`r=0.0633`) didn't match the summary's value (`r=0.0113`) for what was
supposed to be the same statistic. Fixed by renaming the second test's variables; verified the summary
now matches each section's own printed output.

**Key GaT results:**
- **Headline finding — the commitment-outcome relationship is genuinely non-monotonic**, verified
  against real data before the blueprint was finalized: completion rate rises sharply from minimal
  commitment (score 0–1: 37–40%) to moderate commitment (score 2, simply `timed` with nothing extra:
  **79.0%**, the sample-wide peak), then *declines* at higher commitment (score 3: 66%, score 5: 59%).
  Deletion rate mirrors this in reverse (lowest at score 2: 5.0%; rises again at score 5: 18.2%). A
  single pooled linear correlation is essentially zero (`r=-0.005`, n.s.) and would have completely
  missed this — the binned curve was reported as the primary evidence specifically because the
  relationship isn't linear, decided in the blueprint before running anything.
- Within-participant version (demeaning to rule out a between-participant confound, the now-standard
  check from SyD/StM): the same non-monotonic *shape* persists (peak at 2, dip at 3, partial recovery at
  4, drop at 5), and the overall linear summary becomes small but highly significant (`r=0.063,
  p=4.5×10⁻²⁵`, n=26,680) — the non-monotonic pattern is not a between-participant artifact.
- Directly consistent with the paper's own framing: *"Neither strategy is inherently better... a timed
  task with an alert may represent a stronger commitment... but also creates a higher expectation for
  execution."* The data support over-commitment (stacking recurrence + subtasks + long duration on top
  of an already-timed task) being associated with *worse* outcomes, not better — plausibly because
  heavily-structured tasks tend to be larger, more aspirational commitments that are intrinsically
  harder to finish.
- Phenotype labels (N=53 eligible): `commitment-oriented` and `flexibility-oriented` exactly tied at
  18 each, `mixed` at 12, `chronic-deferrer` at 4, `adaptive-rescheduler` rare (1). The paper's 5th named
  phenotype, "overload-prone," was deliberately **not recomputed** — already covered by SyD's
  `dominant_loop_label="overload-trending"`, cross-referenced rather than duplicated.
- **Strategy adaptation after rescheduling: another genuine null result**, converging with StM's null
  path-dependence finding. Neither pooled (`r=-0.003, p=0.78`) nor within-participant (`r=0.011,
  p=0.25`) shows rescheduling a task predicts a meaningfully different commitment level for the *next*
  task. Combined with StM's null on structure-after-non-completion-streaks, this project now has two
  independent, converging null results on "does this dataset show evidence of tactical learning from
  recent outcomes at the task-to-task level" — the honest answer, so far, is no.

---

**Seventh status update (2026-08-03):** Statistical Mechanics (StM) is now implemented and
executed — the largest departure from DS5 in this project so far. Notebook:
`notebooks/61_structured_statistical_mechanics.ipynb`. Blueprint: `structured_stm_blueprint.md`.
Outputs: `outputs/model_outputs/structured/statistical_mechanics/`.

**Central design decision:** the theory paper's own §2.1 explicitly cautions that "energy, temperature,
and equilibrium are not directly observed in task-log data... must be treated as analogy-based
constructs... not literal physical variables" — noticeably more cautious language than DS5's source
paper used. **No literal β/T/Z/F thermodynamic apparatus was built** (DS5's `β_behav = 2/σ̂²` formula has
no mathematical basis for Structured's discrete multi-property configuration space, and this notebook
does not consume StoP's output at all). Instead, the paper's own named constructs — stability,
susceptibility, path dependence — are operationalized with direct statistical measures. An explicit
non-redundancy check against InT (marginal vs. joint entropy) and DyS (continuous trajectory vs.
discrete macrostate persistence) was completed before writing any code.

**Two real design bugs were caught by the notebook's own built-in sanity check, both material:**
1. First draft defined the microstate without completion status, then invalidly compared its entropy
   against InT's `H_completion` marginal — 21/53 "violations" that were really just an invalid
   comparison (completion wasn't part of the config being tested). Fixed by using two configurations:
   `full_config` (5 properties, matches the paper's list exactly, including completion) for
   entropy/macrostate, and a completion-excluded `structural_config` reserved for the susceptibility
   analysis (where completion is the outcome being predicted, not a config component — including it
   there would make the test circular).
2. Even after adding completion, 4/53 violations remained — traced to using a *binary*
   completed-vs-not flag while InT's `H_completion` marginal is the *3-class* `lifecycle_status`
   (completed/deleted/unresolved); collapsing categories can only reduce entropy relative to the finer
   marginal being compared against. Fixed by using the 3-class variable directly. **0 violations after
   both fixes**, verified across all 53 eligible participants.

**Key StM results:**
- Macrostate labels: `timed-basic` most common (33/53, 62%), `high-structure` next (19/53, 36%),
  `inbox-heavy` rare (1/53) — consistent with every other Structured notebook's finding that inbox is
  barely used as a planning mode.
- Macrostate persistence (week-to-week stability of the dominant task type): mean 0.953, median 1.0 —
  very high, but flagged as likely a **ceiling effect**: since `timed` already dominates ~93-97% of
  weekly activity for most participants (per InT/NeT), there is rarely a viable alternative type for the
  dominant label to shift to. High persistence here is expected given the skew already documented
  elsewhere, not necessarily a novel stability finding on its own.
- Susceptibility (completion-rate sensitivity to configuration): mean 0.015, modest and variable
  (0–0.096) — task structure has some but not a large influence on completion likelihood, for most users.
- Supplementary duration check: short-duration timed tasks complete slightly more often than long-duration
  ones (0.553 vs. 0.525 mean rate) — small, descriptive, not tested for significance.
- **Path dependence: a genuine null result.** Pooled `r=-0.022` (nominally `p=0.022` but a negligible
  effect size); within-participant `r=-0.0018`, `p=0.85` — essentially zero. The paper's named
  "path-dependent changes after repeated unresolved tasks" phenotype is **not supported** in this data —
  a non-completion streak does not meaningfully predict whether the next task gets extra structure.
  Reported as a null finding, not reframed to look more positive.

---

**Sixth status update (2026-08-03):** System Dynamics (SyD) is now implemented and executed.
Notebook: `notebooks/68_structured_system_dynamics.ipynb`. Blueprint (includes an explicit
**non-redundancy check against NeT/StoP/DyS before building**, confirming SyD adds a genuinely new
quantity — a running backlog *stock*, not a re-description of transitions/flow-rates/composition
already computed): `structured_syd_blueprint.md`. Outputs:
`outputs/model_outputs/structured/system_dynamics/`.

**Two real methodological issues were caught and resolved during implementation, both material to how
the results should be read:**

1. **13 task_ids had duplicate `Task Created` events** (~0.5 seconds apart — a client-side double-fire
   logging artifact, verified, not a genuine re-creation). Fixed by deduplicating to the earliest event
   per task before any downstream computation.
2. **`backlog_trend_slope` was positive for all 47 eligible participants** (min 0.014) — suspicious
   enough to check rather than report as-is. Verified the resolution-latency distribution first (median
   0.66 days, 90th percentile ~5 days among tasks that do resolve — short), which would only bias the
   final ~1 week of each trajectory, not the whole thing. A trim-the-final-week sensitivity check showed
   93.6% sign agreement between raw and trimmed slope — **the positive trend is a genuine structural
   finding, not primarily a right-censoring artifact.** Most plausible driver: 26.8% of non-censored
   tasks never resolve within the window at all, creating a persistent accumulating floor regardless of
   how fast the rest of the workload turns over.

**Key SyD results:**
- Backlog stock (`Backlog_w`, non-censored tasks only, same left-censoring undercount caveat as DyS):
  mean 32.1, peak up to 352 for the heaviest participant; trend slope positive for essentially everyone,
  confirmed genuine per the sensitivity check above.
- Dominant loop labels (descriptive, tercile-based): `overload-trending` and `productive-trending` tied
  at 16/47 each, `balanced` at 15/47.
- **Feedback-loop tests required a second correction beyond the first two bugs**, caught by inspecting
  the results rather than accepting them: the pooled `productive`-loop correlation (`r=0.9456`) was
  implausibly strong for a real week-to-week effect. Added a person-mean-centered ("within-participant")
  version to isolate genuine lagged timing from a between-participant volume confound (some participants
  are simply high-volume every week). Results:
  - **Productive loop** (completion → next-week creation): pooled `r=0.95` → within-person `r=0.12`.
    Pooled number was almost entirely the volume confound; a real, much weaker positive effect remains.
  - **Overload loop** (backlog → reduced next-week creation, paper predicts negative): pooled `r=0.42`
    (wrong sign) → within-person `r=-0.18` (**correct sign, only after the correction**) — the paper's
    predicted overload/disengagement pattern is genuinely present, but only visible once the
    between-participant confound is removed.
  - **Balancing loop** (backlog → same-week rescheduling, paper predicts positive): pooled `r=0.47` →
    within-person `r=-0.11` — **does not replicate in the correct direction** once properly analyzed;
    higher-than-usual backlog for a given participant is, if anything, associated with slightly less
    rescheduling that week, not more.
- Headline methodological takeaway for any future pooled analysis on this dataset: **always check a
  within-participant version before trusting a pooled correlation** — two of three loop tests here would
  have been reported wrong (one overstated, one wrong-signed) without it.

---

**Fifth status update (2026-08-03):** Dynamical Systems (DyS) is now implemented and executed.
Notebook: `notebooks/62_structured_dynamical_systems.ipynb`. Blueprint (deliberately NOT a port of
DS5's DyS — DS5 reduced its own 1D StoP SDE to a σ→0 deterministic limit; the paper's own Structured DyS
section describes a genuinely multi-dimensional **weekly** state-space trajectory instead, and this
notebook does not consume StoP's fitted daily parameters at all): `structured_dys_blueprint.md`.
Outputs: `outputs/model_outputs/structured/dynamical_systems/`.

**Key DyS results:**
- 5-dimensional weekly state vector, every dimension named in the paper's own Example A (`n_created_w`,
  `timed_share_w`, `inbox_share_w`, `completed_share_w`, `complexity_w`), built from non-censored task
  creations only, participant-relative week indexing (local calendar day via `event_timezone`, same
  convention as StoP).
- Eligibility (`MIN_WEEKS=4`, verified against real weekly-activity data): 42/61 (68.9%) — 4
  participants have zero non-censored creation events and are automatically ineligible.
- **A real reporting bug was caught and fixed during implementation:** the first run silently dropped
  those 4 fully-censored participants from the eligibility denominator entirely (reporting "42/57,
  73.7%" instead of the correct "42/61, 68.9%") rather than counting them as ineligible. Fixed by adding
  them back explicitly as ineligible rows, matching the convention already established in the NeT
  notebook. Both notebook and blueprint now agree on 68.9%.
- Descriptive (Step 1, rule-based, not clustering) region labels: `dropout-prone` most common (14/42,
  33%, by tercile construction), followed by `mixed` (9), `oscillatory` (8), `inbox-heavy` (6),
  `sparse-consistent` (3), `high-structure` rarest (2) — matches the StoP finding that stability is the
  exception: almost no one lands in the paper's "stable structured planner" category.
- Mean `dropout_score` is negative (−0.243) and mean `volume_trend_slope` is negative (−1.10) — a mild
  overall tendency toward declining weekly creation volume across the sample, though both metrics have
  wide, outlier-driven ranges (min `volume_trend_slope` = −32.1, one heavy-volume participant driving
  most of the spread) — reported as a distributional caveat, not smoothed over.
- Left-censoring caveat check (Part 2 of blueprint): correlation between `state_space_volatility` and
  `pct_tasks_left_censored` = 0.254 — weak-to-moderate; high-censoring participants' trajectories are
  somewhat more volatile, plausibly because their creation-based state vector is a thinner, less
  representative slice of their true task portfolio, not necessarily because they are genuinely more
  erratic planners. Flagged, not resolved.
- PCA of the weekly state space: 62.9% variance explained by the first 2 components.
- Free-vs-pro (observational only): no strong or consistent separation on any trajectory metric.

---

**Fourth status update (2026-08-03):** Stochastic Processes (StoP) is now implemented and
executed. Notebook: `notebooks/63_structured_stochastic_processes.ipynb`. Blueprint (deliberately NOT a
port of DS5's StoP — DS5 modeled a bounded daily override *rate*; the paper's own StoP example for
Structured is an unbounded daily *count*, "the number of timed tasks created per user-day"):
`structured_stop_blueprint.md`. Outputs: `outputs/model_outputs/structured/stochastic_processes/`.

**Key StoP results:**
- Two daily state variables, both named in the paper's own Temporal Role sentence: `N_t^created`
  (timed-task creation count) and `N_t^completed` (completion-marking count), both binned by each
  event's own **local calendar day** via `event_timezone` (verified necessary: 24/61 participants have
  >1 distinct timezone across their events — naive UTC-day binning would have misclassified genuine
  same-session activity into different days).
- Eligibility (`MIN_SPAN_DAYS=14`, `MIN_ACTIVE_DAYS=5`, verified against this dataset's own local-day
  distributions, not DS5's differently-defined span-based `MIN_DAYS=7`): 43/61 (70.5%) for `N_t^created`,
  38/61 (62.3%) for `N_t^completed`.
- `mu_hat` (drift) near zero for both series (median 0.000) — no strong net trend in planning volume
  for most participants over the observation window.
- **`Fano_factor` (new metric, not used in DS5 — count-process-specific burstiness measure): mean ≈ 6,
  with 97.7% (`N_t^created`) and 94.7% (`N_t^completed`) of eligible participants showing Fano > 1.**
  This directly and clearly answers the paper's own StoP framing question ("is planning behavior mainly
  stable, drifting, noisy, or bursty?") — the answer is overwhelmingly **bursty**, not stable or steadily
  trending, for nearly this entire sample.
- Descriptive (Step 1, rule-based, NOT a Step 2 clustering result) phenotype labels: `noise-dominated`
  is the plurality (~40-49%), drift categories (`growth-drift`/`decay-drift`) combined ~35%, `bursty`
  ~14-18%, and **`stable` is the rarest label (1-3 participants)** — stability is the exception, not the
  rule, for this population's planning behavior.
- Free-vs-pro (observational only): free-tier participants show higher `sig_hat` and `Fano_factor` than
  pro-tier — descriptive, no causal claim (subscription is not randomized; could reflect selection).

DyS (notebook 62) and StM (notebook 61) depend on this notebook's output per the established dependency
chain (mirrors DS5: `cross_dataset_strategy.md`) — their own blueprints, when written, must independently
re-derive from the paper's DyS/StM sections which of these StoP quantities (if any) are the right input,
rather than assuming DS5's own DyS/StM design (σ-threshold regime classification, β≈2/σ̂² approximation)
transfers unchanged.

---

**Third status update (2026-08-03):** Information Theory (InT) is now implemented and executed.
Notebook: `notebooks/65_structured_information_theory.ipynb`. Blueprint (deliberately NOT a port of
DS5's InT notebook — every quantity traces to the theory paper's own §2.5 text, quoted in full in the
blueprint): `structured_int_blueprint.md`. Outputs: `outputs/model_outputs/structured/information_theory/`.

**Key InT results:**
- Entropy measures computed per participant (53-61/61 eligible depending on threshold), matching the
  paper's phenotyping framing: `H_type_first` (mean 0.20 bits, low — 93% of tasks are created `timed`),
  `H_creation_source` (mean 0.65 bits — `add_button`/`note_button` dominate but with real spread),
  `H_hour_creation` (mean 2.89 of max 4.58 bits — planning happens across a genuinely wide span of the
  day, not concentrated), `H_recurrence` (mean 0.54 bits, Bernoulli), `H_completion` (mean 0.96 of max
  1.58 bits — outcome diversity is real, not everyone is completion-dominated), `H_reschedule` (mean
  0.58 bits, Bernoulli).
- Mutual information tested exactly the three pairs the paper names (pooled across the whole sample,
  matching the paper's population-level framing of these as dependency questions, not per-user profile
  dimensions): task_type→completion (MI=0.036 bits, 3.2% of completion's uncertainty explained — weak),
  creation_source→inbox/timeline placement (MI=0.094 bits, 88.7% normalized — **inflated by severe
  class imbalance, 1.4% inbox**, flagged in the blueprint *before* running, confirmed after; the
  supplementary 3-class version gives a more honest 34.5%), time-of-day→task_type (MI=0.011 bits, 2.8%
  — very weak). The paper's fourth named pair (energy level→movement/delay) is explicitly reported as
  not-implementable, not silently omitted.
- NeT-InT bridge (`I_consec_state = H_state_marginal − H_trans`, legitimate now that NeT exists):
  **a real bug was caught and fixed during implementation** — the first attempt used the wrong marginal
  distribution (all raw per-event state labels, which wrongly includes 15,301 single-event tasks that
  contribute zero transitions), producing a mathematically impossible negative mutual information for
  some participants. Fixed by using the target-state (`state_to`) marginal from the same edge list NeT
  built. Verified: 0 chain-rule violations across all 45 eligible participants after the fix. Mean
  `I_consec_state` = 0.362 bits. Full account in `structured_int_blueprint.md` Part 5.

---

**Second status update (2026-08-03):** Network Theory (NeT) — the first model family — is now
implemented and executed. Notebook: `notebooks/64_structured_network_theory.ipynb`. Blueprint (full
FLAG rationale, written before any code): `structured_net_blueprint.md`. Outputs:
`outputs/model_outputs/structured/network_theory/` (`participant_network_metrics.csv`,
`transition_edge_list.csv`, `entry_state_distribution.csv`, `subscription_group_summary.csv`,
`model_run_summary.md`, 3 figures).

**Key NeT results:**
- 45/61 participants (73.8%) NeT-eligible (≥20 pooled task-state transitions); only 8/61 (13.1%)
  stationary-eligible — markedly lower than DS5's 66.4%, because the 7-state vocabulary makes many
  participants' transition matrices non-ergodic (e.g. `deleted` is near-absorbing), not because of thin
  data.
- HHI_net mean 0.534, rho_self mean 0.373, H_trans mean 1.284 bits (of a max possible 2.807) — **not
  comparable in magnitude to DS5 NeT values** (different state-space size; see FLAG W4).
- Entry-state distribution, non-censored tasks only: 93.4% `timed`, 5.3% `all_day`, 1.4% `inbox` — users
  overwhelmingly create tasks already scheduled, essentially bypassing the inbox as an entry point.
- **Left-censored tasks' first-observed state is 60.9% `completed`** — most pre-existing tasks captured
  by this window are being closed out, not actively worked on. A genuinely new finding, not visible
  before this notebook.
- **Pooled transition matrix confirms the theory paper's own illustrative example** (`timed → moved →
  completed`): `moved` is the dominant intermediate hub (timed→moved 2,919; moved→completed 2,794;
  moved→moved self-loop 4,760 — heavy repeated rescheduling).
- `inbox` tasks are deleted at ~19.1% of their outgoing flow vs. ~1.9% for `timed` tasks — inbox tasks
  are far more abandonment-prone than scheduled ones (relevant to the GaT flexibility-vs-commitment
  framing in §3.6 below).
- Free-vs-pro and reaches-completed/reaches-deleted comparisons are reported as **purely descriptive**
  (no significance test run; small subgroup N) — see `model_run_summary.md` for exact numbers.

Stage 1 feature extraction summary (from the first status update) still applies below; no earlier
finding in this report has been invalidated by the NeT implementation, only extended.

---

**Original status update (2026-08-03, first update):** Stage 1 feature extraction is now complete
(`notebooks/17_structured_feature_extraction.ipynb`, `src/features/structured_features.py`,
`outputs/features/structured/`). This surfaced the left-censoring finding in §3.1 below (not visible
during inspection) and answered the self-report-vs-behavior construct-validity question from the
original §4/§7 draft: **r = 0.127** between self-reported and behaviorally-derived task completion
rate (N=54, weak/near-null). No model-family notebooks (NeT/InT/StoP/DyS/SyD/StM/GaT/ABM) have been
implemented yet — the sufficiency assessment below still applies to those.
Companion to `structured_retrospective_dataset_audit.md` (inspection + cleaning findings) and
`data_docs/pdfs/Structured Planning as a Complex Adaptive System.pdf` (theoretical framework).

This report exists to answer one question before any Stage-4-style modeling work starts on this
dataset: **given what is actually in `retro_behavioraldata_2026_07_22.csv` and
`retro_surveydata_2026_07_22.csv`, which of the eight CAS model families proposed in the theory paper
are actually implementable, and with what caveats?**

---

## 1. Theoretical framework being tested

`Structured Planning as a Complex Adaptive System.pdf` (Strassburger, Schmiedmayer & Grüning) proposes
applying the same eight CAS model families used elsewhere in this project — Statistical Mechanics
(StM), Dynamical Systems (DyS), Stochastic Processes (StoP), Network Theory (NeT), Information Theory
(InT), Game Theory (GaT), Agent-Based Modeling (ABM), and System Dynamics (SyD) — to digital task
planning instead of smartphone-friction behavior. The shared behavioral episode across all eight models
is: *a user externalizes an intention by creating a task, assigns it more or less structure, and across
time the task remains stable, is modified, moved, completed, rescheduled, returned to the inbox, or
left unresolved.*

The paper's own §1.3 ("Implementation Potential") already anticipates a two-tier data-availability
scenario:
- **Weaker case:** only `Task Created` data available → network built from creation pathways and
  initial task structure only.
- **Full-value case:** `Task Created` **and** update/movement/rescheduling/completion events available →
  full task-lifecycle transition networks become possible, and Information Theory/Stochastic
  Processes/Dynamical Systems gain a genuine temporal dimension.

**This export is the full-value case.** All three event classes are present: `Task Created` (10,529),
`Task Updated` (40,718, with a detailed `update_type` change-log), `Task Deleted` (2,439). This is the
single most important sufficiency finding of this report.

---

## 2. Critical finding: the actual export is narrower than its own codebook promises

The one codebook document available (`Retrospective_Study_Structured_Task_Created.pdf`) documents a
24-property `Task Created` PostHog event schema, including fields such as `task_energy_level`,
`task_alerts`, `task_alert_sound`, `task_completed`, `task_is_in_inbox`, `task_has_custom_symbol`,
`task_has_custom_theme`, `task_theme`, `task_is_all_day`, `task_time`, `task_relative_day`,
`task_event_source`, and `task_is_detached`.

**None of these fields are present in the actual behavioral CSV.** The real export contains only 14
task-related columns: `task_id`, `task_type`, `task_name` (100% empty), `task_color`, `task_icon`,
`task_start_at`, `task_end_at`, `task_timezone`, `task_duration`, `task_is_recurring`,
`recurrence_unit`, `recurrence_interval`, `task_has_notes`, `subtasks_amount`.

This matters directly for the theory paper's Table 1, which explicitly lists "energy level" and
"alerts" as inputs to Statistical Mechanics, Information Theory, and Game Theory. **Neither is
available.** Any implementation must either drop these dimensions or find a different proxy — there is
no `task_energy_level` or `task_alerts` column to fall back on, and no completion flag (`task_completed`)
either (see §3.4 for how completion is nonetheless recoverable).

The Qualtrics consent text also states "topic categories" are recorded as a task characteristic
(§3.3.1 of the theory paper's embedded draft) — there is no `category` or `topic` column in the export
either. Treat all three (energy level, alerts, category) as **promised-but-unavailable** constructs.

---

## 3. Per-model feasibility assessment

Legend: 🟢 directly implementable now · 🟡 implementable with an explicit proxy/derivation step ·
🔴 not implementable from this data alone.

### 3.1 Network Theory (NeT) — 🟢 strongest candidate, with one important correction
The paper's own "full value" scenario is met — `task_id` is stable and never shared across
participants, and `update_type_list_str` gives fine-grained edge labels (`date_changed`,
`start_time_changed`, `type_changed`, `recurrence_changed`, `color_changed`, `icon_changed`,
`notes_changed`, `duration_changed`, `title_changed`, `subtasks_changed`, `energy_level_changed` —
note: the *event that energy level changed* is logged even though the energy level *value itself* is
not exported, an odd but real asymmetry) plus task-level `task_completed` / `task_uncompleted`
transitions.

**Correction (found during feature extraction, 2026-08-03, not visible during inspection):** "full
per-task lifecycles" was too strong a claim. **60.7% of tasks (16,213/26,729) are left-censored** —
their first visible event is `Task Updated` or `Task Deleted`, never `Task Created` — because these
are existing users with pre-existing task histories, not fresh signups. Full created→...→resolved
lifecycle reconstruction is only possible for the 10,516 non-censored tasks. **This does not weaken
state-to-state transition analysis** (timed→moved, moved→completed, etc. remain valid for all tasks
within the observed window) — it only limits the "entry point"/creation-channel dimension of the
network to the non-censored subset. NeT remains the strongest candidate model family here; the
transition-graph richness is still materially greater than DS5's first-order app-transition network,
which had no lifecycle-completion signal at all. See `structured_task_lifecycle_features.md` for the
full derivation and `has_creation_event` flag.

### 3.2 Information Theory (InT) — 🟢 highly feasible
Entropy is computable over `task_type`, `update_method` (creation/edit channel), `event_timezone` /
time-of-day, `recurrence_unit`, `task_is_recurring`, and completion outcome (once derived, §3.4).
Entropy over `task_alerts` and `category` is not possible (unavailable). Mutual information between
`update_method` and completion, or between `task_type` and completion, is directly testable.

### 3.3 Stochastic Processes (StoP) — 🟢 feasible
Daily/weekly time series of task-creation counts, timed-task share, completion-marking counts, and
inbox-use rate can be built directly from `event_timestamp_utc` + `event_type`. Drift vs. diffusion
decomposition (as done for DS5) is directly transferable. Caveat: activity spans are uneven (9/61
participants have <7 days of data) — a minimum-observation threshold analogous to DS5's `MIN_DAYS=7`
will again exclude a nontrivial fraction of participants.

### 3.4 Dynamical Systems (DyS) — 🟡 feasible, with one required derivation
State-space variables (task volume, timed-task share, inbox share, completion rate, movement rate,
recurrence use, task complexity via `subtasks_amount`) are all constructible. **Completion rate is not
a stored column — it must be derived** from `update_type_list_str` containing `task_completed` (with
`task_uncompleted` as a later "undo" event that must be checked for, since it can flip the state back).
This has now been implemented in `src/features/structured_features.py::build_task_lifecycle_features`
using last-transition-wins logic: 18,931/26,729 tasks (70.8%) were ever marked completed, and 678 of
those (3.6%) were later un-completed — a meaningful "undo" fraction correctly handled by taking the
chronologically last completion-relevant tag rather than "ever completed." Task-level pooled outcome
distribution: 70.2% completed, 20.7% unresolved, 9.1% deleted (see
`outputs/features/structured/structured_task_lifecycle_features.csv`). Alert-use cannot be included (unavailable).

### 3.5 System Dynamics (SyD) — 🟡 feasible at the aggregate/conceptual level
Stocks (inbox/timed/all-day backlog, unresolved tasks, recurring tasks) and flows (creation,
scheduling changes, completion, rescheduling, **abandonment**) map cleanly onto the event log.
`Task Deleted` directly and unambiguously represents the "abandonment" flow the paper describes
conceptually (2,439 deletion events / 2,426 unique deleted tasks) — this is a genuine advantage over
the paper's more speculative framing, since deletion is an observed event, not an inferred state.
Completion (again derived per §3.4) represents the "productive loop" flow. This is well suited to a
conceptual/descriptive System Dynamics pass rather than a formally fitted stock-flow simulation.

### 3.6 Game Theory (GaT) — 🟡 feasible only as a coarse commitment index
The paper frames GaT around a flexibility-vs-commitment trade-off using timing, alerts, duration,
recurrence, and subtasks as commitment signals. With `task_alerts` unavailable, the commitment index
must be built from `task_type` (timed > all_day > inbox), `task_duration_min`, `recurrence_unit`, and
`subtasks_amount` alone — a weaker signal than the paper's full proposal. Still directly computable;
just flag the missing alert dimension explicitly wherever this index is used.

### 3.7 Statistical Mechanics (StM) — 🟡 feasible with a redefined microstate, energy level unavailable
The paper's proposed "task configuration as microstate" is still constructible from `task_type`,
`recurrence`, `notes`, `subtasks`, and completion — but **not** from `energy_level`, which the paper
explicitly lists as a StM input and which is not in the export. Any β/temperature-style quantity here
would need a different proxy than DS5's σ̂-based approach (DS5 had a continuous behavioral-noise
estimate from SDE fitting; Structured has no equivalent continuous quantity without first building the
DyS/StoP layer). **Recommend implementing StM after DyS/StoP**, not before, mirroring the DS5
dependency order documented for this project (StoP-derived quantities feed StM's β approximation).

### 3.8 Agent-Based Modeling (ABM) — 🔴 not implementable directly from raw data
Requires empirically estimated per-user rule probabilities (timed-task-creation rate, inbox-use rate,
completion rate, reschedule rate, disengagement rate) as inputs — these must come from Stage 1 feature
extraction and/or a completed StoP/DyS/NeT pass first. Consistent with this project's existing rule
(DS5 notebooks 46/47 — GaT/ABM — were deferred until phenotyping existed); the same deferral logic
applies here, likely more strongly given the smaller N.

---

## 4. Survey / psychosocial construct mapping

The intake survey offers demographic, motivational, and self-report psychopathology-adjacent measures
that could serve as **exploratory overlay correlates** on top of behavioral phenotypes (in the same
spirit as DS5's psychosocial overlays on phenotype clusters) — not as primary outcomes.

| Construct (theoretical) | Proxy available | Caveat |
|---|---|---|
| Planning motivation / goals | `app_goals` (multi-select free text categories) | Not a validated scale; simple category-membership only |
| General life satisfaction | `life_happiness_score` (1–7) | Single item, not a validated wellbeing scale |
| Productivity self-perception | `productivity_happiness_score`, `productivity_importance_general_score`, `productivity_importance_personal_score`, `productivity_rating_vs_others_score` | Single items; face-valid but unvalidated |
| Self-reported planning behavior | `pct_tasks_planned_num`, `pct_planned_tasks_completed_num` | Self-report, not validated against actual behavioral completion rate — **worth a direct empirical check**: does self-reported completion % correlate with the behaviorally-derived completion rate (§3.4)? This is a genuine construct-validity test this dataset uniquely supports. |
| Autism / ADHD traits | `autism_status`, `adhd_status` (self-report categorical) + `asrs_*_score` (ASRS-v1.1 Part A, ordinally recoded 0–4) | Screener only, not diagnostic; ASRS items are 54.7% missing (more than base survey attrition, cause unconfirmed); ordinal recode is **not** the official ASRS clinical scoring algorithm (different per-item thresholds) |

**Sample size caution:** only 65/117 survey responses are both consented and finished; of those, the
overlap with participants who also have behavioral data is **55/61** behavioral participants (6
behavioral participants have survey records that are either unfinished or non-consenting-adjacent).
Any psychosocial-correlate analysis on this dataset will be working with N≈55 at best — smaller than
any DS1/DS4/DS5/DS6 psychosocial analysis in this project. Treat all such correlations as exploratory
and likely underpowered, consistent with how DS5 psychosocial overlays were already treated cautiously.

---

## 5. Overall sufficiency verdict

**The data are sufficient to implement five of the eight model families (NeT, InT, StoP, DyS, SyD)
with only minor, clearly-documented proxy substitutions, and a sixth (GaT) with a weakened but still
meaningful signal.** StM should be implemented after StoP/DyS (dependency, not blocker). ABM should be
deferred until a phenotyping stage exists, mirroring this project's existing DS5 sequencing logic.

The two structural gaps that matter most (`task_energy_level`, `task_alerts` — both present in the
codebook, both absent from the export) affect StM and GaT specifically, not NeT/InT/StoP/DyS/SyD. This
means the **strongest and most novel opportunity in this dataset — full task-lifecycle network
modeling via NeT, enabled by having Updated *and* Deleted events, not just Created — is fully
supported**, and is in fact stronger here than in the DS5 NeT implementation (which had no equivalent
lifecycle-completion signal).

The single most important *derivation gap* rather than *missing-data gap* is that **completion status
is an event to reconstruct (`task_completed`/`task_uncompleted` transitions in `update_type`), not a
stored column** — this must be handled correctly (last-transition-wins, not "ever completed") in Stage
1 feature extraction, or every completion-rate-based feature across DyS/StM/SyD/GaT will be silently
wrong.

---

## 6. Proposed implementation order (not yet started)

Mirroring the DS1/DS4/DS5/DS6 pairing convention (`0X_datasetN_inspection` / `0X_datasetN_cleaning`,
then `1X_datasetN_feature_extraction`, then model notebooks), and this project's existing dependency
logic (StoP-derived quantities feed StM; phenotyping precedes ABM):

1. `notebooks/17_structured_feature_extraction.ipynb` — per-participant and per-task-lifecycle
   features: task volume, type-share, completion rate (derived, last-state-wins), movement/reschedule
   rate, recurrence use, task complexity, lifecycle transition counts. This is a prerequisite for
   every model below, not a model notebook itself.
2. Network Theory (NeT) — build task-state transition graphs; likely the flagship result given full
   lifecycle data
3. Information Theory (InT) — entropy over task_type/update_method/timing/completion; cheap, high
   signal, no dependency on other models
4. Stochastic Processes (StoP) — daily/weekly planning trajectories, drift/diffusion decomposition
5. Dynamical Systems (DyS) — state-space trajectories using StoP output
6. System Dynamics (SyD) — conceptual stock/flow description using NeT + completion/deletion data
7. Statistical Mechanics (StM) — after StoP/DyS exist, using a redefined (non-energy-level) microstate
8. Game Theory (GaT) — coarse commitment index; can run any time after step 1
9. Agent-Based Modeling (ABM) — deferred until a phenotyping pass exists (same logic as DS5)

**This ordering is a proposal, not a decision** — flagging for confirmation before any notebook beyond
inspection/cleaning is built, consistent with this project's practice of agreeing on modeling sequence
before implementation.

---

## 7. Open questions to resolve before Stage 1 feature extraction

1. Should Structured be compared against the OneSec datasets (DS1/4/5/6) on any shared dimension (e.g.
   entropy, network centralization), or treated as a fully independent dataset per this project's
   "no forced harmonization" principle? The behavioral object (task planning vs. app-opening friction)
   is different enough that forcing a shared feature schema risks the kind of "dishonest unified view"
   this project explicitly avoids.
2. Is the ~3-month-vs-~4.75-month discrepancy between the consent text and the observed data range
   worth flagging to the data-collection team, or is it within normal extraction-window variance?
3. Should the 6 behavioral participants without a fully consented+finished survey response be excluded
   from any behavioral-only analysis, or is `in_behavioral` alone (with no psychosocial overlay)
   sufficient for behavior-only model families (NeT, InT, StoP, DyS)? Recommendation: behavior-only
   models can use all 61; only overlay/correlate analyses need the 55-participant intersection.
4. **[Answered 2026-08-03]** Does self-reported planning behavior track logged behavior? Tested via
   `pct_planned_tasks_completed_num` vs. behaviorally-derived `pct_tasks_completed`: **r = 0.127**
   (N=54) — weak/near-null. Self-report should not be treated as a validation check for behavioral
   completion features, or vice versa; report both independently.
5. **[New, from feature extraction]** `pct_tasks_left_censored` varies from 0% to 100% across
   participants (median 42.9%). Should a minimum-non-censored-task threshold be applied before any
   creation-channel or full-lifecycle analysis, analogous to DS5's `MIN_DAYS=7` filter? No threshold
   has been applied yet in `structured_participant_features.csv`.
