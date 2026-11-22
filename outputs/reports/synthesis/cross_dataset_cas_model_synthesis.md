# Cross-Dataset, Cross-Model-Family Synthesis

**Written:** 2026-08-07
**Trigger:** User-requested synthesis across all datasets and all 8 CAS model families,
produced as part of a full documentation audit (see companion audit notes referenced
throughout). This is the project's first synthesis that spans *every* dataset category at
once — prior synthesis documents (`ds5_step2_master_synthesis.md`,
`structured_step2_master_synthesis.md`) are each scoped to one dataset.
**Status:** Findings synthesis + forward-looking implementation proposal. Confirmed facts
(recomputed or cross-checked against saved CSVs during this audit pass) are marked as such;
everything under §4–§5 is interpretation and proposal, explicitly separated per this
project's own "separate confirmed facts from inferred interpretations" convention.

---

## 0. What exists, as of this writing

| Dataset | N (analysis) | Design | Step 1 (8 families) | Step 2 (phenotyping) | Step 3 (personalization) |
|---|---|---|---|---|---|
| **DS5** | 414/573 | 3-arm RCT (control/default/reintervention) | 7/8 complete (SyD deferred to DS6) | Complete — 6-path exploration + v2 revision arc | **Started** — blueprint + executed notebook (`200_ds5_personalization_exploration.ipynb`) |
| **Structured** | 36–61 (family-dependent) | Naturalistic, no conditions | 8/8 complete | Complete — single pass + 4-path exploration | Not started (no randomized arms to test — see §3) |
| **DS6** | 227–243 | Naturalistic, baseline→intervention *period* (no parallel arms) | 7/8 complete (GaT/ABM deferred) | Complete — single pass + Path A′ | Not started |
| **DS4** | 641–1,039 | Naturalistic, no conditions, N=1,039 largest cohort | 7/8 complete (SyD excluded — no repeated survey waves) | Complete — Phase 1 + 3 exploration paths | Not started |
| **Stanford Health** | N=1 (participant 4) | Naturalistic + continuous physiology | 2/8 attempted (DyS+StoP outlook, exploratory) | Not started (N=1) | Not applicable yet |

DS1 has Stage 0/1 (audit + feature extraction) only — no CAS modeling has been attempted on
it, so it does not appear in the tables below.

---

## 1. Phenotype structure, compared across datasets (confirmed)

The single most important cross-dataset pattern this audit surfaced is that **the
relationship between a network/topological phenotype axis and a behavioral-dynamic
phenotype axis is different in every dataset that has both** — this is not a minor
implementation detail, it is itself a finding.

| Dataset | Dominant axis | Secondary axis | Relationship | Evidence |
|---|---|---|---|---|
| DS5 | Network topology (NeT: `HHI_net`, `rho_self`) | Behavioral-dynamic (StoP/DyS/StM: `sig_hat`, `H_emp`, `x_mean`) | **Fully orthogonal** | ARI(Path A vs Phase 1) = 0.020 |
| Structured | Behavioral-dynamic | Network (NeT) | **Coupled, not independent** | Path A ARI vs Phase1 = 1.000; Path F Fisher's exact p=0.029 |
| DS4 | Behavioral/thermodynamic (StoP/StM/DyS) | Network (after removing internal NeT collinearity) | **Coupled, but each individually low-overlap with the blended Phase-1 solution** | Path A′ ARI=0.664; Path C′ ARI=0.047; Path F′ chi2 p<0.0001 |
| DS6 | A third thing entirely: DyS's binary `regime_changed` | StoP/NeT/InT/StM residual features | **Regime-change axis dominates**, near-perfect separation | Cross-tab: 125/102 split ≈ exactly `regime_changed`; removing it (Path A′) gives only an outlier-detection result, ARI=0.024 vs main pass |

**Interpretation (not fact):** four datasets, three qualitatively different phenotype-layer
geometries (fully orthogonal / coupled / dominated-by-a-third-axis). This argues against a
single universal "network vs. behavioral" phenotype template and supports this project's own
existing design principle — multidimensional profiles over fixed labels — with empirical
grounding rather than just being a stated preference.

**Resolved (2026-08-07, same day):** DS5's Step 3 notebook (`200_...ipynb`) originally called
its moderator "pre-existing Path C." Traced directly in notebook 101's own source (cells
32–37, "Figure C7 — Full-sample NeT-only clustering, robustness check for Phase 1 split"):
Path C genuinely computed **two** things, not one — its famous within-profile B1/B2 (Profile
B) / A1/A2 (Profile A) sub-clustering, *and* a separate full-sample 2-cluster NeT-only
baseline, saved as `cluster_net_only` inside `ds5_net_subcluster_assignments.csv`. Notebook
200 loads exactly that second, genuinely pre-existing column — nothing was mislabeled or
recomputed. The only real problem was that bare "Path C" collides with the more-cited
sub-clustering result in a reader's head. Renamed the notebook-200-local token to **"NetC"**
(parallel to "Net2," the strict two-feature sensitivity computed fresh in the same notebook),
with one anchor sentence preserving full provenance back to notebook 101/Figure C7. Notebook
re-executed; all 3 figures, both `.md` docs, and all CSVs regenerated with the new label; all
numbers unchanged (`ARI=1.00`, `Holm p=0.2806/0.2806/0.0191`, etc. — a pure relabeling).

---

## 2. What each model family found, compared across datasets (confirmed)

### StoP (Stochastic Processes)
Every dataset with any temporal granularity shows **overdispersion / burstiness**, not a
simple homogeneous-rate process: Structured's Fano factor >1 for 95–98% of participants
(explicit headline finding); DS6's Fano median 6.6 (baseline) / 3.3 (intervention); DS4's
daily-vs-weekly θ̂ correlation of only r=0.316 is arguably a manifestation of the same
non-Markovian structure at a different timescale. DS5's constant-drift model (the simplest
of the four) is the one place this wasn't tested directly, since its state variable is a
bounded rate, not a count.

### NeT (Network Theory)
**Every dataset that built a construction-sensitive network metric needed a correction before
the metric was trustworthy** — DS4's `app_close_event` inflating `rho_self` to 0.96 before
being excluded (true value 0.62–0.68); DS6's `app_next` mechanically echoing the current row
99.3% of the time before `app_prev` was used instead. This is a recurring methodological
throughline, not one dataset's idiosyncrasy: raw same-app-repetition signals in event logs of
this kind are systematically inflated by logging mechanics, in a way that would not be
obvious without checking.

### InT (Information Theory) — the NeT–InT bridge bug, found three times independently
Structured, DS6, and DS4 **each independently hit the identical bug class**: computing
`I_consec = H_target − H_transitions` with the wrong marginal population produces an
impossible negative mutual information. All three were fixed the same way (use the
transition-consistent marginal — destination/attempts-only, matching whichever population
`H_transitions` was computed over). This is the single most-repeated lesson in the project's
own build history, and DS6's own InT notebook explicitly noted it should have applied the
already-known fix immediately rather than re-deriving it from a wrong side first.

### DyS (Dynamical Systems)
The qualitative regime language available to each dataset is a direct consequence of which
side(s) of the state variable are bounded — this is a clean theoretical point, not just an
implementation quirk:
- DS5 (bounded both sides, [0,1] rate) → boundary fixed points only, hedged language
  (`predicted_boundary_fp`, never "attractor").
- DS4 (bounded below only, OU on an unbounded rate) → a **true interior attractor**,
  unhedged language justified (`corr(x_mean_raw, mu_hat_OU)=0.9925`).
- DS6 (bounded below only, unbounded count) → an **asymmetric 3-way regime space**
  (declining / growing / resting) that neither DS5 nor DS4's state-space shape can produce.

### StM (Statistical Mechanics) — a convergent cross-dataset finding
DS5 (approximate β=2/σ̂², bounded rate) and DS4 (exact β=2θ/σ̂², OU) both built full
thermodynamic apparatus; Structured and DS6 both explicitly declined it (discrete/unbounded
state spaces don't support a literal Boltzmann bridge) but still extracted a
configurational-entropy-based susceptibility. **Where a condition/period contrast exists, the
direction agrees across two independently-built model families on two independent datasets:**
DS5's friction conditions show *lower* β (hotter/less rigid) than control; DS6's friction
conditions show *higher* susceptibility than control (p=0.0011/0.0075). Both point the same
way — **friction appears to destabilize behavioral regularity, not just suppress its rate.**
This is the strongest convergent cross-model, cross-dataset finding in the whole project.

### GaT (Game Theory)
DS5, Structured, and DS4 **all three** independently concluded there is no directly-observed
payoff/utility structure in this kind of data (Stanford Health's readiness assessment reached
the same conclusion on paper) — 4-for-4 across every dataset assessed. Where phenotype-level
GaT effects were found, a consistent theme emerges: GaT-derived labels track **condition/state
more than stable trait** — DS5's `strategy` label is itself the reason its own Step 3
blueprint had to exclude it as a moderator (§3 below); DS4's `chronic_overrider` phenotype
converges with its own independently-built Step 2 high-susceptibility cluster (a genuine
cross-model validation), suggesting the trait-like GaT signal that *does* exist is really a
restatement of the StM/susceptibility axis, not an independent one.

### ABM (Agent-Based Modeling) — three independent failures of the same kind
DS5's validation gate fails (ρ=0.428, ergodic pull toward 0.5 in a bounded SDE over 30-day
horizons); DS4's gate fails in a different way (simulated weekly/daily ratio moves in the
**wrong direction**, 0.84 vs real 1.49); Structured's succeeds on individual rank
(r=0.914) but fails on population magnitude and **reverses direction** at the 2-archetype
level. All three are honestly reported as genuine limitations, not reframed. The consistent
pattern — a simple agent built purely from each individual's own already-fitted parameters
under-reproduces some real structure — suggests real behavioral regularity in this domain is
not fully captured by single-timescale SDE/rate parameters; DS4's own daily/weekly divergence
is probably the cleanest direct evidence of *what* is missing (multi-timescale structure).

### SyD (System Dynamics)
Only Structured and DS6 have implemented this (DS5 deferred it to DS6 by design; DS4 excluded
for a permanent data reason; Stanford Health not yet attempted). Both implementations
independently rediscovered the same general lesson already on record in this project's own
history: a pooled cross-sectional-looking correlation on panel data can be almost entirely a
between-participant volume confound, and only the within-person/regression-to-mean-controlled
version should be trusted. Two-for-two on that specific methodological point; too thin a
sample (2 datasets) to say more about SyD substantively across datasets yet.

---

## 3. Step 3 (Personalization) — the newest development, and what it teaches methodologically

DS5's new Step 3 blueprint proposed `profile_p1` (the Phase 1 NeT-based phenotype) as a
"condition-independent, outcome-feature-free" moderator, based on it being empirically
condition-independent (χ²=1.22, p=0.545) and (per the blueprint's own §4) "built from
`HHI_net`/`rho_self` only."

**The executed notebook checked that second premise directly and found it was wrong.**
`profile_p1` was actually constructed from five features (`sig_hat`, `H_emp`, `x_mean`,
`HHI_net`, `rho_self`) and named by ascending `x_mean` — meaning every legacy interaction
test using `profile_p1` (or the related `profile_k3` GMM solution, built from the same five
features) is contaminated by moderator–outcome feature overlap: `x_mean` entered the
moderator's own construction *and naming*; `commitment_score` correlates −0.98 with `x_mean`;
`chi_behav` is deterministic in `sig_hat` and `x_mean`, both of which entered `profile_p1`.

The notebook corrected course mid-implementation — using a genuinely outcome-free moderator
instead (a NeT-only "distributed vs. hub-locked" split, cross-validated against an
independently-built strict `HHI_net`+`rho_self`-only clustering, ARI=1.00) — and reported:

- **No detectable phenotype × condition interaction on override rate** (`x_mean`, Holm
  p=0.281) or on the independently-computed replication outcome (`commitment_score`, Holm
  p=0.281).
- **A small, Holm-significant interaction on behavioral susceptibility** (`chi_behav`, Holm
  p=0.019, partial η²=0.025) — the one outcome with no feature overlap with the moderator at
  all, so not subject to the same leakage concern.
- Explicit, stated limits: not a validated per-user recommender, not a causal claim, phenotype
  measured during (not before) the study period, and the ABM's own gate failure rules out a
  credible simulated-counterfactual extension for now.

**This is a strong example of the project's established "catch it with your own sanity check
before trusting the result" discipline extending, for the first time, to a Step 3 blueprint's
own causal-safety reasoning, not just to a Step 1 bridge formula.** It is also, as far as this
audit found, the first time a *blueprint's* premise (as opposed to a notebook's
implementation) was shown to be wrong by the notebook that followed it — worth naming
explicitly as a project-level lesson: a blueprint's stated "this feature is safe because X"
claim should be re-verified computationally during implementation, not taken as already
established just because it appears in an approved planning document.

No other dataset has a randomized arm, so none can currently run the DS5-style interaction
test in its literal form — see §5 for what a same-spirit test could look like on each.

---

## 4. What this could mean (interpretation — clearly separated from the facts above)

1. **Digital-behavior heterogeneity in this domain does not reduce to one universal
   phenotype axis.** The network/behavioral relationship differs qualitatively across all
   four datasets tested. A thesis claim of the form "smartphone-use phenotypes are
   fundamentally X-dimensional" would be overstated; the honest claim is that *at least* two
   recurring dimensions exist, and how they relate is itself context-dependent — a
   genuinely new argument for this project's existing "multidimensional profile, not fixed
   label" design principle, now backed by four independent replications rather than being a
   stated preference alone.

2. **Friction interventions look like they inject noise/instability into a metastable
   habitual attractor, more than they suppress a rate.** This reframing is supported by two
   independently-built model families (StM's β/susceptibility) on two independent datasets
   (DS5, DS6) pointing the same direction. It is a mechanistic claim worth stating explicitly
   in the thesis discussion, distinct from (and complementary to) the simpler "friction
   reduces override rate" descriptive finding already established at Stage 1.

3. **The repeated ABM shortfall (3/3 datasets) is itself informative, not just a limitation
   to note in passing.** It suggests the behavioral regularity that does exist is not
   reducible to the same single-timescale SDE parameters that describe each individual's own
   marginal statistics — there is cross-timescale structure (DS4's daily/weekly divergence
   being the cleanest single piece of evidence) a simple local-rule agent does not capture.
   This motivates a genuinely new theoretical direction — multi-timescale or hierarchical
   generative models — as a citable "future work" claim grounded in three independent
   empirical failures, not a single dataset's quirk.

4. **If personalization has traction anywhere in this data, DS5's Step 3 result suggests it
   is more likely to show up in "who is near a behavioral tipping point" (susceptibility)
   than in "who overrides friction more" (a level effect).** This is a specific, falsifiable,
   non-obvious steer for where the *other* datasets' eventual Step 3 work should look first
   (see below), rather than defaulting to the most intuitive outcome (override rate) again.

---

## 5. How this could be implemented — concrete next steps

Each proposal below follows the same discipline DS5's Step 3 blueprint (and its own
mid-implementation correction) established: **check the candidate moderator for
outcome-feature overlap and condition-association before trusting it as a moderator**, don't
assume a Step 1/2 label is safe just because it was validated for a *different* purpose.

- **DS6 — `notebooks/210_ds6_personalization_exploration.ipynb`.** DS6 has no randomized
  arms, but it does have a genuine two-period design (baseline→intervention) and the
  project's only significant psychosocial phenotype interaction so far
  (`self_control_index_change` differs by the `regime_changed`-dominated cluster,
  p=0.018 Bonferroni). Proposed test: does a *baseline-only* phenotype (built from features
  measured before the intervention period, e.g. StM `susceptibility_baseline` or NeT
  `HHI_net_baseline` — explicitly NOT `regime_changed`, which is itself defined across both
  periods and would be circular here) moderate the psychosocial change outcome? This is a
  stronger causal position than DS5's own Step 3 test, since DS6's moderator candidates can
  genuinely precede the period contrast, unlike DS5's phenotype (measured during the study).

- **DS4 — `notebooks/220_ds4_personalization_exploration.ipynb`.** No randomized arms and no
  period contrast, but very large N and long windows. Reframe the question from "which
  condition works better for whom" (not available) to "does an individual's own longitudinal
  *adaptation slope* (`open_rate_change_calendar`, an existing validated Stage-1 feature)
  differ by phenotype?" Candidate moderator: Path C′ (`rho_self`+`I_consec`, the
  near-orthogonal, most-stable clustering in the whole DS4 arc, Jaccard=0.966) — check first
  for overlap with `open_rate_change_calendar` before using it, following the same discipline
  DS5's notebook 200 established.

- **Structured — `notebooks/230_structured_personalization_exploration.ipynb`.** No
  randomized arms, but GaT already found a real non-monotonic commitment→completion curve
  (peak at moderate commitment, decline at maximum). Proposed test: does the location or
  height of that peak differ by phenotype (Path A behavior-dominant vs. Path C network
  axis)? This would be Structured's own version of "does phenotype moderate an
  already-established effect," mirroring DS5's structure without porting its content —
  consistent with this project's standing "ground every new analysis in the dataset's own
  material, don't port" discipline.

- **Stanford Health — the differentiated long-term direction.** Once the cohort grows beyond
  N=1, this is the only dataset in the entire project that could support a genuinely new
  Step 3 dimension none of the others can: a **real-time physiological trigger** (e.g., only
  surface friction when HRV/arousal indicates reduced self-control reserve) rather than a
  purely retrospective behavioral phenotype. This should be elevated in the thesis as the
  single most differentiated future direction the project's data infrastructure enables,
  building on the already-validated (if null, for N=1) DyS+StoP outlook method.

- **A cross-dataset model-level replication check, once ≥2 of the above exist.** DS5's Step 3
  finding — network topology does not moderate a behavioral *level*, but may relate to
  *susceptibility* specifically — is a specific, transferable claim. Once DS6 and/or DS4's
  own Step 3 notebooks exist, test whether their own susceptibility-like quantities
  (`chi_OU` for DS4, `susceptibility` for DS6/Structured) show the same phenotype-linked
  pattern DS5 found. This would be the project's first genuine cross-dataset **model-level**
  validation (as opposed to each dataset separately supporting the same *kind* of modeling),
  and is exactly the kind of claim this project's own validation principles ask for:
  "when several models can explain similar observable behavior, note this explicitly instead
  of overstating certainty" — a replication attempt is how that gets tested rather than
  merely stated.

---

## 6. Caveats that apply to every proposal in §5

- All of the above remain associational, not causal, for every dataset except DS5 (and even
  DS5's result is scoped to "condition effect differs by observed phenotype," not "assigning
  friction by phenotype would improve outcomes" — see `ds5_step3_personalization_blueprint.md`
  §10 for the full interpretive-scope argument, which generalizes directly to every proposal
  above).
- None of the ABM-based simulated-counterfactual ideas implied by "Framework C" in DS5's
  blueprint should be attempted on any dataset until the underlying generative-model gap
  documented in §2 above (ABM) is separately addressed — a simulated counterfactual inherits
  whatever structure the agent fails to capture.
- Every proposed notebook above should re-run the same moderator-safety checks DS5's own
  Step 3 notebook performed (condition/period independence of the candidate moderator,
  feature-overlap check against the candidate outcome) as a first step, not an afterthought —
  this is precisely the check that caught the `profile_p1` leakage problem in DS5's own case.

---

## 7. Item closed since the first version of this synthesis

The "Path C" naming question flagged in §1 (first version of this report) is now resolved —
see §1's "Resolved" note. Renamed to "NetC" throughout `notebooks/200_ds5_personalization_exploration.ipynb`
and its outputs; nothing else required correction.
