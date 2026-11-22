# Theory vs. Implementation Comparison — DS4 Model Families

**Written:** 2026-08-08
**Overlap check:** Read in full before drafting — `outputs/reports/stage4/post_analysis/theory_vs_implementation_comparison.md` (DS5 template this document mirrors in structure), `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §2 (cross-dataset per-family findings — cited below rather than re-derived), `outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md` (contains the corrected DS4 ABM number used in this document). This document goes deeper into DS4-specific mechanics, numbers, and per-family theory fidelity than the cross-dataset synthesis attempts to.
**Purpose:** Compare the theoretical model-to-behavior translation intended by the paper (`One Sec Smartphone-Intervention Behavior as a Complex Adaptive System.pdf`) against what was actually implemented in DS4's notebooks; assess faithfulness, approximations, and divergences.

---

## Background

DS4 is framed by this project as the dataset where several of DS5's approximations become resolvable, not merely repeatable — long observation windows (up to 897 days, median 66, mean 97) make a mean-reverting Ornstein–Uhlenbeck (OU) process identifiable for the first time in the project, which in turn makes the Boltzmann bridge exact rather than approximate and gives Dynamical Systems a genuine interior attractor rather than a boundary approximation. This "rigor ladder" framing (DS5 approximate → DS4 exact) is explicit in `ds4_stm_blueprint.md` §1 and §10, and is the organizing idea behind most of DS4's theory-vs-implementation story.

The state variable `X_t = n_opened / n_events` (restricted to `intervention_event_class == 'intervention_event'` rows, outcome in `{opened, dismissed}`) is DS4's own construction — narrower and cleaner than DS5's pooled-outcome state variable, but it inherits the same fundamental proxy caveat: it is a behavioral rate from event logs, not a directly observed psychological state. Every quantity below inherits this limitation regardless of how exact the surrounding mathematics becomes.

DS4 has **no experimental condition** (self-selected, naturalistic OneSec usage) — every "theory intended a condition/field effect" comparison below is structurally unavailable, not merely unobserved.

---

## StoP — Stochastic Processes

### Theory intended

The paper frames individual behavior via a stochastic differential equation; DS5's short windows forced a constant-drift simplification. The theoretically richer Ornstein–Uhlenbeck process `dX_t = θ(μ − X_t)dt + σdW_t` — with mean-reversion rate θ, long-run mean μ, and diffusion σ — was always the intended fuller model, deferred in DS5 specifically because θ needs enough independent return-to-baseline cycles to estimate (`ds4_stop_blueprint.md` §1).

### What was implemented

- **Used:** Full OU process, estimated via closed-form conditional MLE (AR(1) OLS regression of `X_{t+1}` on `X_t`, restricted to consecutive-day pairs) — exact for fixed Δt=1, not an approximation
- **Population:** 1,039 total → 786 meet MIN_DAYS=30 → 785 retain ≥10 consecutive pairs → **641 (81.7%) produce a valid mean-reverting fit** (`0<φ̂<1`)
- **Headline finding:** median relaxation time τ̂ = 0.63 days at daily resolution

### Assessment

**Stayed close to theory, and resolves a DS5 simplification:** the OU model DS5 had to defer is fully implemented here, with a genuinely exact estimator (OLS-as-MLE for a linear-Gaussian AR(1) model, not an approximation of MLE). This is the strongest "resolves a DS5 flag" story anywhere in DS4's Step 1.

**A real, unresolved empirical surprise, not a theoretical failure:** the median relaxation time (0.63 days) is nearly two orders of magnitude faster than the blueprint's own illustrative pre-registration example ("if τ̂=14 days...", `ds4_stm_blueprint.md` §4, written before any DS4 OU fit existed). The notebook's own weekly-aggregation sensitivity check found a **meaningfully different** answer at weekly resolution (median τ̂≈0.91 weeks ≈ 6.4 days) with only **r=0.316** correlation between daily- and weekly-fitted θ̂ per participant (n=291 with both fits valid). Two honest readings are stated side by side in the blueprint and carried through every downstream notebook (genuine fast habitual reversion vs. daily-ratio sampling noise) — neither is silently preferred. This divergence is not resolved anywhere in DS4's Step 1; it propagates as an open caveat into InT, DyS, and StM (each explicitly states "daily-timescale specific, not proven timescale-independent").

**18.3% invalid-fit rate is reported, not absorbed:** of 785 fit attempts, 144 fail the mean-reverting criterion (`φ̂` outside (0,1)) and get `NaN`, not an imputed value — the funnel is reported explicitly at every downstream stage rather than silently shrinking the "eligible" population.

**Main approximation to defend in the paper:** the daily/weekly divergence itself. The paper should state plainly that DS4's OU parameters describe daily-timescale dynamics specifically, and that a genuinely open question — real multi-timescale structure vs. small-sample-ratio noise — remains unresolved. The ABM notebook (57) was later built specifically to test this question generatively (see below) and also failed to resolve it.

---

## InT — Information Theory

### Theory intended

Same Shannon-entropy "behavioral portfolio" framing as DS5: outcome entropy for friction-response diversity, app/hour entropy for behavioral breadth and context, and a bridge entropy connecting the stochastic model to information theory.

### What was implemented

- **H_out_intervention** (2-category, intervention_event class only) and **H_out_all_classes** (4-category, deliberately mixing all 3 event classes as an explicitly-caveated exploratory comparison) — both computed correctly
- **H_app, H_hour** — reused directly from Stage 1 features
- **H_emp** — K=10 binned entropy of daily X_t, same convention as DS5 for method comparability
- **H_SDE** — the **exact** OU stationary-distribution differential entropy `0.5·log2(2πe·σ̂²/(2θ̂))`, not an approximation
- **MI(intervention_type; outcome)** — a DS4-unique addition (6 logged intervention types, no DS5/other-dataset equivalent)

### Assessment

**A genuine theoretical upgrade over DS5, not just a port:** DS5's `H_SDE = 0.5·log2(2πe·σ̂²)` treats the diffusion increment as if it had a well-defined stationary distribution, which its constant-drift SDE does not actually have — an approximation, explicitly flagged (FLAG A) in DS5's own StM notebook. DS4's OU process has an *exact* Gaussian stationary distribution `N(μ,σ²/2θ)`, so DS4's `H_SDE` formula is the literal, exact differential entropy of that distribution. This is one of the cleanest "DS4 resolves a DS5 approximation" cases in the whole arc.

**Bridge validated, and consistent in direction with DS5:** `r(H_emp, H_SDE) = 0.721` (n=641) — comparable in magnitude to DS5's own `r(H_SDE,H_emp)=0.650`, a reassuring cross-dataset sanity check even though the two formulas are not literally the same quantity (one exact, one approximate).

**A carried-forward caveat, correctly propagated rather than dropped:** `H_SDE` uses daily-scale `σ̂_OU`/`θ̂_OU` only — the notebook explicitly states this inherits StoP's daily/weekly divergence and should not be read as timescale-independent. This caveat is repeated verbatim in DyS's and StM's own interpretation cells — a genuine example of a documented limitation actually propagating through the dependency chain rather than being restated once and forgotten.

**A modest, well-motivated new addition:** `MI(intervention_type;outcome)` = 0.0010 bits — a near-zero but non-negative mutual information, meaning intervention type barely predicts outcome (`rotatePhone` shows the highest opened-rate, 80%, but n=10 events, too small to trust; `blackScreen` and `breathingExercise`-family types cluster around 61–67% opened). Reported without causal overclaiming (§2, item 7) — intervention type is not randomly assigned, so this cannot support a "which intervention type works best" claim.

**Redundancy handled honestly, not hidden:** `r(H_out_intervention, mu_hat_OU) = −0.631` — real, moderate-strong overlap (expected, since both trace back to the same opened-proportion), reported and kept, not dropped or treated as fully independent evidence.

---

## DyS — Dynamical Systems

### Theory intended

In the σ→0 limit, the SDE reduces to a deterministic dynamical system with fixed points corresponding to stable behavioral equilibria. DS5's constant-drift SDE only produces a *boundary* fixed point in this limit (X*=0 or 1), forcing hedged language (`predicted_boundary_fp`, never "attractor").

### What was implemented

- **X\* = μ̂_OU**, taken directly from StoP's own fitted OU mean — a genuine **interior** fixed point, not a boundary approximation, because the OU deterministic skeleton `dX/dt=θ(μ−X)` has exactly this fixed point whenever θ>0 (already guaranteed by StoP's `fit_valid` criterion)
- **Regime split:** `theta_hat_OU` median (1.587/day) → `high_control` (n=321) / `low_control` (n=320)
- **Fixed-point validation:** `x_mean_raw` (simple empirical mean of daily X_t) vs. `mu_hat_OU` — **corr=0.9925**, mean absolute deviation 0.0108 (n=641)
- **InT bridge:** `behaviorally_deterministic` = high_control AND low H_emp — `corr(theta_hat_OU, H_emp) = −0.176`

### Assessment

**The central theoretical claim is genuinely earned, not just relabeled:** DS4 can use the word "attractor" where DS5 explicitly could not, and the fixed-point validation (corr=0.9925) is a real, strong empirical confirmation that the OU fit's implied long-run mean matches the simple empirical mean of the data — this is not a tautology (the OU fit could have diverged from the raw mean if the model were badly misspecified) and it passed. This is the strongest, most unambiguous "theory upgrade validated by data" result in DS4's Step 1.

**The InT bridge is honestly reported as weak, not oversold:** DS5's own DyS-InT-style bridges (e.g., between DyS-eligibility and H_emp) were moderate; DS4's equivalent (`θ̂` vs `H_emp`, r=−0.176) is weak. The notebook and its `model_run_summary.md` state this plainly ("weak, reported honestly, not a strong cross-validation") rather than reframing a modest correlation as confirmatory.

**A genuinely different (not merely smaller) structural constraint than DS5's DyS:** because the OU process is linear-in-drift by construction, there is exactly **one** fixed point per participant, always. The blueprint is explicit that this is "a genuinely single-well system, not a simplification being deferred" (§3, FLAG 4) — i.e., DS4's DyS cannot in principle discover bistability even if it existed behaviorally, a structural ceiling worth stating plainly in the paper rather than treating as an oversight.

**Main approximation to defend:** the median-θ̂ regime split (`high_control`/`low_control`) is, like DS5's σ-median split, a conventional 50/50 partition rather than a theoretically derived threshold for "genuinely deterministic." Unlike DS5, however, this split is at least built on a parameter (θ̂) that directly measures the theoretical quantity of interest (mean-reversion strength) rather than a proxy for it (DS5's σ̂ measures noise, only indirectly related to determinism strength).

---

## StM — Statistical Mechanics

### Theory intended

The Boltzmann bridge: stationary distribution `P_inf(x) ∝ exp(−2V(x)/σ²)`, inverse temperature `β = 2θ/σ²`, susceptibility `χ = β·p·(1−p)` near a two-state approximation. DS5 built this as an explicit approximation (FLAG A) because its constant-drift SDE has no true confining potential.

### What was implemented

- **β_OU = 2θ̂_OU/σ̂_OU²** — exact for the OU model (median 36.55, n=641)
- **V(x) = (θ̂/2)(x−μ̂)²** — individual-level, exact closed form, no KDE required (a first in this project — DS5's V(x) needed noisy empirical KDE)
- **χ_OU = β_OU·p_use·(1−p_use)**, **F_OU**, **T_OU** — derived exactly as in DS5's formula, but on rigorous inputs
- **H_StM** — joined directly from InT's `H_SDE` (verified identical to floating-point precision, 4.4e-16 max difference — not merely correlated, mathematically the same quantity for DS4) rather than recomputed

### Assessment

**FLAG A is genuinely resolved here, not merely reworded:** DS5's StM notebook had to say "this is a behavioral analog, not rigorous thermodynamics" as its central caveat. DS4's blueprint states, correctly, "this notebook resolves DS5's FLAG A" — the OU process's stationary distribution really is Gaussian, so β_OU really is the Boltzmann inverse temperature of an exact confining quadratic potential. This is the single cleanest example in the whole DS4 arc of a documented DS5 limitation being fully closed rather than just improved.

**A new caveat opened exactly where the old one closed (FLAG VI):** because β_OU/χ_OU/H_StM are built entirely from StoP's daily-scale θ̂/σ̂, they inherit the daily/weekly divergence problem in full. The blueprint is explicit that "behavioral temperature" should not be presented as timescale-independent. This is not a weaker version of DS5's FLAG A — it is a different limitation, correctly not conflated with the resolved one.

**A modest, correctly-labeled internal null result:** `beta_OU` barely differs by DyS's `regime_label` (`high_control` mean=48.2 vs `low_control` mean=49.1) despite both being built from `theta_hat_OU` — because β_OU also folds in σ̂, the two splits diverge. Reported as-is in the companion doc ("Not a strong differentiator; reported as-is, not forced into a narrative") rather than searched-for significance.

**Descriptive, explicitly-non-comparable cross-dataset number, correctly caveated both ways:** DS4's median β_OU (36.5, exact) vs. DS5's median β_behav (60.9, approximate) are reported side by side purely for descriptive interest, with the comparison explicitly labeled not-directly-comparable because the underlying SDEs differ. This is the correct level of caution — a naive reader could otherwise conclude DS4 participants are "cooler" than DS5's, which the different-model caveat rules out as a valid inference.

**Main approximation still present:** `V(x)` is exact *for the OU model assumption* — but the OU assumption itself is a model choice, not a verified behavioral law. The blueprint's own FLAG III states this should be labeled "OU model-implied energy landscape," not "true behavioral energy landscape" — a genuinely important distinction the paper must preserve, since "exact" here means "exact given the model," not "exact given the participant's real underlying process."

---

## NeT — Network Theory

### Theory intended

Same as DS5: characterize app-switching as a directed weighted network — concentration (HHI), self-loop rate (habitual repetition), transition entropy (switching diversity), and a mutual-information bridge to InT (`I_consec = H_app − H_trans`).

### What was implemented

- **Attempt-rows-only sequence construction** (`intervention_event` + `no_intervention`, excluding `app_close_event`) — a DS4-specific decision, verified before writing the blueprint, not a DS5 port
- **T_ij, ρ_self, H_trans, HHI_net** — same formal definitions as DS5. **π and H_pi are NOT** — DS4 pads to a fixed 21-state grid with absorbing rows for unvisited states and omits DS5's residual/irreducibility gate, which invalidates the shipped `H_pi`.
- **I_consec = H_app_attempts − H_trans**, where `H_app_attempts` is a freshly-computed marginal (see below) — verified ≥0 for all 950 eligible participants

### Assessment

**The single most consequential construction decision in DS4's whole Step 1, correctly caught before it could corrupt every downstream network number:** naively pooling all three event classes into one timestamp-ordered sequence gives `ρ_self=0.743`. Breaking this down by class-pair transition revealed why: an `intervention_event` immediately followed by an `app_close_event` has `ρ_self=0.959` (n=348,028) — this is a **logging artifact** (friction shown on app X, then X's own close event fires as the next logged row), not a behavioral decision to stay on the same app. The blueprint's own decision to exclude `app_close_event` entirely from the NeT sequence (verified `ρ_self` drops to 0.624 on attempt rows only) is a genuinely theory-preserving fix — it protects the construct validity of "self-transition rate as habitual repetition" against a construction artifact that would have inflated it by a factor comparable to DS5's own high self-loop rate, for entirely mechanical reasons. See `ds4_bug_discoveries_and_fixes_chronicle.md` for full detail.

**A second, independent bridge bug, caught by the mandatory sanity gate rather than missed:** the first `I_consec = InT's (all-events) H_app − H_trans` produced 138/950 (14.5%) impossible negative values. Root cause verified concretely on one participant: InT's `H_app` used a differently-scoped population (all events including `app_close_event`) than `H_trans`'s attempts-only population. Fixed by computing `H_app_attempts` fresh, on the identical population `H_trans` uses. This is the same bug class the cross-dataset synthesis already documents as recurring across Structured and DS6 — DS4 is the third independent occurrence of "wrong marginal population" in an InT-NeT bridge, and it was caught the same way each time: a mandatory non-negativity gate, checked before trusting the result.

**Faithful to theory, honestly caveated in magnitude:** `ρ_self≈0.62–0.68` (median 0.680 on the eligible population) is explicitly not compared in raw magnitude to DS5's ≈0.92 — the notebook and companion docs state this repeatedly, since the two datasets' sequence-construction rules differ structurally (DS5 never had a close-tail class to exclude). This is the correct response to a superficially large cross-dataset gap: attribute it to construction differences rather than imply DS4 participants show less habitual repetition than DS5's.

**Main approximations carried unchanged from DS5:** first-order Markov assumption (unverified, same open question); no time-gap filter between consecutive attempt rows (same FLAG G1 class as DS5); self-loops included in the transition matrix (matches DS5's own choice, now more meaningful given `app_close_event` is already excluded).

---

## GaT — Game Theory

### Theory intended

Per the paper's own §2.6 (quoted in `ds4_gat_blueprint.md` §2): app-opening attempts framed as repeated conflicts between present-self and future-self, with users describable as commitment-oriented, reward-oriented, chronic overriders, adaptive switchers, or friction-avoidant. The paper's own §1.3 explicitly cautions that payoff/utility are not directly observed in this kind of data and the model "should be used as an interpretive framework... rather than a literal payoff model."

### What was implemented

- **No formal payoff matrix or Nash equilibrium** — matches the paper's own explicit caution, and matches DS5's and Structured's precedent for the same model family
- **Rule-based classification** into 4 of the paper's 5 named phenotypes, using `rate_opened_intervention_events` (median split), `max_consecutive_opens` (top-tertile split), and a freshly-computed `substitution_after_dismissal_rate` (top-tertile split) — deliberately not re-clustering, since Step 2 already performed formal clustering
- **`p_open_after_dismiss` dropped** (r=0.934 with the opened-rate, near-tautological)
- Three correlational cross-checks: `chi_OU` by phenotype (StM susceptibility), phenotype × Phase 1 cluster (crosstab), `|open_rate_change_calendar|` by phenotype (adaptation)

### Assessment

**Theory-faithful in restraint, not just in labeling:** the decision not to build a payoff matrix is not a simplification made under time pressure — it is a direct, correctly-cited application of the paper's own stated caution (§1.3), matching the identical decision made independently for DS5 and Structured. The cross-dataset synthesis already records this as a 4-for-4 pattern (DS5, Structured, DS4, and Stanford Health's readiness assessment) — a converging, honestly-reported theoretical limit of this model family for this kind of data, not a DS4-specific shortfall.

**Real, substantial cross-model convergent validity — the strongest cross-family finding in DS4's GaT:** chronic-overrider phenotype associates strongly with Phase 1's independently-built high-susceptibility cluster (χ²=136.4, p<0.0001; 131/232=56% of that cluster is chronic_overrider) and with higher `chi_OU` directly (ANOVA F=12.09, p<0.0001; chronic overriders mean χ_OU=10.01 vs. commitment-oriented mean=7.01). Two independently-constructed model families — one a rule-based typology built from raw behavioral rates, the other a formal clustering built from thermodynamic parameters — converge on the same at-risk group. This mirrors the cross-dataset synthesis's own observation that DS4's GaT chronic-overrider phenotype "converges with its own independently-built Step 2 high-susceptibility cluster... suggesting the trait-like GaT signal that does exist is really a restatement of the StM/susceptibility axis, not an independent one" — an honest, not-overclaimed reading: this is convergence between two lenses on the same underlying axis, not evidence of two independent constructs both being real.

**An explicit, undisguised gap:** the paper's 5th named phenotype ("friction-avoidant") is not operationalized at all — no DS4 quantity distinguishes it from commitment-oriented. Stated as a limitation (FLAG 5), not silently dropped from the phenotype vocabulary.

**Main approximation to defend:** the classification thresholds (median, tertile cutoffs) are conventional, not theoretically derived — the same class of caveat as DS4's DyS regime split and DS5's own k-selection thresholds. This is consistent with the project-wide pattern of using magnitude-based splits where no principled threshold exists in the theory.

---

## ABM — Agent-Based Modeling

### Theory intended

Per the paper's §2.7 (quoted in `ds4_abm_blueprint.md` §2): heterogeneous rule-based agents whose local behavior should reproduce macro-level patterns; "Empirical features from Information Theory, Stochastic Processes, and Network Theory can be used to inform the agent types and rules."

### What was implemented

- **One agent per real participant**, parameterized directly by that participant's own already-fitted StoP (μ̂,θ̂,σ̂) — not a phenotype-derived discrete agent type
- **Model 1:** pure discrete-time OU agent, no added mechanism
- **Model 2:** Model 1 + an illustrative (not fitted) weekly-periodic drift modulation
- **Validation target:** does simulating from Model 1/2 and refitting weekly reproduce StoP's own real daily-vs-weekly θ̂ divergence, or does a pure daily-OU agent predict tighter daily-weekly consistency than what real participants show?

### Assessment

**A DS4-specific validation target, not a ported one — this is a theoretically well-motivated design choice:** rather than reusing Structured's Fano-factor burstiness target (which has no DS4 analog, since DS4's StoP is a mean-reverting rate process, not a count process), the ABM blueprint identified StoP's own already-documented open question (the daily/weekly θ̂ divergence, r=0.316) as DS4's natural ABM validation target. This is exactly the paper's own framing — "test whether simple local rules are sufficient to reproduce broader observed patterns" — applied to a question this project's own prior work had already surfaced as unresolved, rather than invented for the ABM notebook.

**A genuine, structurally interesting negative result, reported honestly, with a corrected number:** neither model reproduces the real divergence — worse, both get the *direction* wrong. Real participants show weekly τ̂ ≈1.5× their daily τ̂ (ratio 1.49); Model 1 produces weekly τ̂ *smaller* than daily (ratio 0.84); Model 2 makes this worse (ratio 0.69). The daily-weekly correlation collapses in simulation (0.316 real → 0.019 Model 1 → −0.00 Model 2) — simulated daily and weekly dynamics become statistically unrelated, unlike real participants. **Only 133/641 (20.7%)** of Model 1's simulated series produce a valid mean-reverting weekly refit at all (corrected figure — see the note below), versus 291/641 (45.4%) of real participants; simulated weekly dynamics are less reliably mean-reverting than real ones too.

**A documentation-accuracy correction, verified directly against the source file for this document:** `participant_abm_simulation_results.md` currently and correctly states "only 133/641 (20.7%) of Model 1's simulated series produce a valid mean-reverting weekly refit at all," with an explicit reconciliation note explaining that the `n=113` figure appearing in the comparison table (`abm_model_comparison_summary.csv`/`.md`) is a *stricter* population (series with **both** a valid daily *and* valid weekly refit — required for the correlation/ratio calculation) — for real participants these two counts happen to coincide (291=291, since the real daily refit is valid 100% of the time), which is exactly what made the conflation between "weekly-valid at all" and "valid on both" easy to miss for Model 1, where only 549/641 (85.6%) of simulated daily refits converge, so the two counts diverge (113 vs. 133). This matches the correction already recorded in `outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md` item 1, verified here directly against the current companion `.md` rather than taken on trust from that audit note.

**Consistent with a project-wide pattern, not an isolated DS4 failure:** the cross-dataset synthesis records this as one of "three independent failures of the same kind" (DS5's ABM gate fails at ρ=0.428; DS4's fails in a different way — wrong direction, 0.84/0.69 vs. real 1.49; Structured's succeeds on individual rank but reverses direction at the population level). DS4's own contribution to this pattern is arguably the cleanest evidence for *why* these simple agents fail: the daily/weekly divergence itself is direct evidence of multi-timescale structure that a single-timescale OU parameterization cannot generate by construction, regardless of which participant's numbers are plugged in.

**Main limitation to state plainly:** this is a recoverability/sufficiency test on an already-open StoP question, not an independent behavioral claim — a negative result here says "a pure local-rule OU agent does not explain the observed multi-timescale structure," not "no simple agent could ever explain it." Model 2's specific addition (day-of-week periodicity, amplitude 0.1, illustrative not fitted) is one plausible mechanism among many; its failure does not rule out others (e.g., regime-switching θ, non-stationary drift).

---

## Phenotyping — Clustering Methods

### Theory intended

Same as DS5: discover behavioral subgroups along theoretically meaningful dimensions. For DS4 specifically, the paper-motivated dimensions are named piecemeal across the model blueprints rather than in one consolidated phenotype table (unlike DS5's own §4.3): StM's blueprint names "potential well depth" (steep=fast-reverting-but-hard-to-shift vs. shallow=slower-but-more-susceptible) as a phenotyping dimension; GaT's blueprint quotes the paper's own 5 named phenotype archetypes; NeT's blueprint frames its own metrics as completing a "Layer 1/Layer 2" structure question mirroring DS5's.

### What was implemented

- **Phase 1:** one curated feature per model family (`tau_hat`/StoP, `H_emp`/InT, `fixed_point_deviation`/DyS, `chi_OU`/StM, `rho_self`/NeT), redundancy-checked before clustering (max |r|=0.483), k-means with **stability-first** k selection (silhouette AND bootstrap Jaccard, not silhouette alone)
- **Path A′:** drop `rho_self`, test whether the taxonomy depends on network structure
- **Path C′:** NeT-only, using the two non-redundant NeT quantities (`rho_self`, `I_consec` — `HHI_net`/`H_trans` excluded as near-mechanically redundant with `rho_self`, r=0.867/−0.950)
- **Path F′:** cross-tabulate Path A′ × Path C′, test independence

### Assessment

**A real methodological correction made and reported, not glossed over:** the phenotyping blueprint's own FLAG 3 specified "silhouette-based k selection." Run literally, this would have selected k=4 (highest silhouette, 0.2747) — but k=4's own bootstrap Jaccard was 0.665, below the project's established 0.75 stability threshold. Rather than ship the highest-silhouette-but-unstable solution, every candidate k (2–6) was checked for both criteria, and k=3 (silhouette=0.2608, Jaccard=0.8486, STABLE) was selected instead. This is documented explicitly in `ds4_phenotype_feature_matrix.md` as "a real methodological correction made during implementation," matching this project's established precedent from DS5's own Phase 1 (which faced an analogous silhouette-vs-stability conflict).

**A genuinely different empirical structure from both prior datasets, not a replication of either:** Path A′ (drop NeT) recovers Phase 1's taxonomy closely (ARI=0.664 using Path A′'s own final k=4) — DS4 sits **between** DS5 (network-dominated Phase 1, its own Path A near-orthogonal at ARI=0.020) and Structured (behavior-dominated, Path A fully recovers Phase 1 at ARI=1.000). Path C′ (NeT-only) is close to orthogonal to Phase 1 (ARI=0.047) and is DS4's cleanest, most stable clustering result of the whole arc (Jaccard=0.966). Path F′ finds the two axes are statistically coupled but not identical (χ²=31.44, dof=6, p<0.0001, min expected cell=4.3). This "dominant-but-not-exclusive behavioral axis, real-but-secondary network axis, statistically coupled not fully orthogonal" picture is a genuinely new geometry in the project's growing catalogue (see `ds4_phenotype_expectation_vs_result.md` for the full discussion).

**A resolved same-day numeric inconsistency, documented transparently:** the exploration plan's own preliminary ARI figure (0.724, a same-k=3 comparison computed during planning before k=4 was chosen as Path A′'s final answer) differs from the executed notebook's real reported ARI (0.664, using Path A′'s own stability-selected k=4). Both companion docs (`ds4_step2_exploration_plan.md`'s status note and `path_a_feature_matrix.md`'s "Known limitations") state which number is the primary, executed figure (0.664) and why the two differ — this is exactly the kind of small numeric drift between a planning document and an executed notebook that this project's own convention requires surfacing rather than silently reconciling.

**Where the demographic overlay is honestly thin:** age (N=149/641, F=1.564, p=0.213) and gender are the only survey-derived overlay variables available at all — DS4 has no Likert-scale psychosocial measures, a structural limitation stated in the blueprint's FLAG III and reiterated in the demographic-overlay companion doc. This is a much thinner interpretive layer than DS5's psychosocial overlays (FoMO, belonging, ostracism), and the paper should not imply DS4's phenotypes carry comparable psychosocial interpretability.

---

## Overall assessment: which models were theory-faithful vs approximated

| Model | Theory faithfulness | Primary approximation / open question | Should be defended in paper? |
|---|---|---|---|
| StoP | **HIGH** | OU model exact and identifiable, but daily/weekly relaxation-time divergence (r=0.316) is a real, unresolved open question | Yes — the OU upgrade over DS5's constant-drift model should be stated explicitly as a resolution; the daily/weekly divergence should be stated as unresolved, not glossed over |
| InT | **HIGH** | `H_SDE` is exact for DS4 (unlike DS5's approximation) but inherits the daily-timescale caveat; `H_out_all_classes` deliberately mixes event classes for exploratory contrast only | Yes — the exact-vs-approximate H_SDE contrast with DS5 is a genuine theoretical result worth a paper section |
| DyS | **HIGH** | True interior attractor (validated, corr=0.9925) but the OU model structurally permits only one fixed point per participant — a real ceiling, not a deferred feature; InT bridge weak (r=−0.176) | Yes — the "true attractor" result and its single-well structural ceiling both belong in the paper |
| StM | **HIGH** | β_OU exact (FLAG A resolved) but daily-timescale-specific (new FLAG VI); V(x) exact given the OU model assumption, not given the participant's true process | **Requires an explicit paper section** — the FLAG A resolution is one of DS4's headline contributions and should be contrasted directly with DS5's approximation |
| NeT | **HIGH** | Attempt-rows-only construction (excludes 47% of raw events) is deliberate and verified, not oversight; first-order Markov and no-time-gap-filter caveats carried unchanged from DS5 | Yes — the `app_close_event` exclusion finding and the I_consec bridge-fix are both genuine methodological contributions worth stating |
| GaT | **MODERATE-HIGH** | No formal payoff apparatus (matches paper's own caution); rule-based thresholds are conventional; 1 of 5 named phenotypes not operationalized | Yes — state the deliberate absence of formal game-theoretic machinery as a theory-consistent choice, and name the friction-avoidant gap explicitly |
| ABM | **MODERATE** (faithful in design, negative in result) | Single-agent-per-participant, no phenotype-derived types (diverges from the pre-registered deferral plan); genuine gate failure, wrong direction | Yes — report as a genuine negative/informative result, consistent with the project-wide 3-for-3 ABM shortfall pattern, not reframed as a partial success |
| Phenotyping | **HIGH** | Conventional k-selection thresholds (same class of caveat as DS5); demographic overlay thin, no psychosocial content available at all | Yes — standard methods, justify briefly; be explicit that DS4's phenotype interpretability ceiling is lower than DS5's due to survey design, not methodology |

---

## What should be explicitly added to the paper before submission

1. **The OU-vs-constant-drift "rigor ladder" narrative** — DS4 resolves DS5's FLAG A (approximate β) and DS5 DyS's boundary-only fixed-point limitation; this should be stated as a direct, cited comparison, not left implicit across separate model sections.
2. **The daily/weekly relaxation-time divergence (r=0.316) as an open, cross-notebook-propagated question** — it appears in StoP, InT, StM, and motivates the ABM notebook's entire design; the paper should name it once, explicitly, as unresolved rather than letting each section re-state it as a local caveat.
3. **The exact OU stationary-distribution differential entropy formula** (`H_SDE = 0.5·log2(2πe·σ̂²/2θ̂)`) — not in the paper's current equation set, and mathematically distinct from DS5's approximate version of the same-named quantity.
4. **The `app_close_event` exclusion finding for NeT** — a genuine, verified, DS4-specific construction decision (naive `ρ_self`=0.743 vs. corrected 0.624) that materially changes a headline network statistic; this methodological point generalizes to any future dataset with a similar close-tail logging architecture.
5. **The single-fixed-point structural ceiling of DS4's DyS** — the OU model cannot in principle discover bistable/multi-well dynamics; state this as a property of the chosen model family, not a data limitation.
6. **The ABM's negative, direction-reversing result** — should be cited alongside DS5's and Structured's own ABM shortfalls as a converging, cross-dataset finding about the limits of single-timescale local-rule agents, per `cross_dataset_cas_model_synthesis.md` §2.
7. **The GaT-StM convergent-validity finding** (chronic_overrider ↔ high-susceptibility cluster) — a genuine cross-model validation worth a sentence in the paper's discussion of construct convergence.

---

## Source documents

- `outputs/reports/stage4/step1_modeling/ds4_stop_blueprint.md`, `ds4_int_blueprint.md`, `ds4_dys_blueprint.md`, `ds4_stm_blueprint.md`, `ds4_net_blueprint.md`, `ds4_gat_blueprint.md`, `ds4_abm_blueprint.md`
- `outputs/reports/stage4/step2_phenotyping/ds4_phenotyping_blueprint.md`, `ds4_step2_exploration_plan.md`
- `outputs/model_outputs/ds4_stochastic_processes/model_run_summary.md`, `participant_parameters.md`
- `outputs/model_outputs/ds4_information_theory/model_run_summary.md`, `participant_entropy_metrics.md`
- `outputs/model_outputs/ds4_dynamical_systems/model_run_summary.md`
- `outputs/model_outputs/ds4_statistical_mechanics/model_run_summary.md`, `participant_ds4_stm_parameters.md`
- `outputs/model_outputs/ds4_network_models/model_run_summary.md`, `participant_network_metrics.md`
- `outputs/model_outputs/ds4_game_theory/model_run_summary.md`, `participant_gat_phenotypes.md`, `gat_phenotype_crosstab.md`
- `outputs/model_outputs/ds4_agent_based/model_run_summary.md`, `participant_abm_simulation_results.md`, `abm_model_comparison_summary.md`
- `outputs/model_outputs/ds4_phenotyping/ds4_phenotype_feature_matrix.md`, `path_a_feature_matrix.md`, `path_c_cluster_profiles.md`, `path_f_summary.md`
- `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §2
- `outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md` item 1 (ABM number correction)

---

*Written 2026-08-08 as part of the DS4 post-analysis synthesis, mirroring the DS5 template (`outputs/reports/stage4/post_analysis/theory_vs_implementation_comparison.md`).*
