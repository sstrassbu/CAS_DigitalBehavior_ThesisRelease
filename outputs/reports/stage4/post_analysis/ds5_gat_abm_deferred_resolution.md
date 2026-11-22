# GaT / ABM Deferral — Resolved, and Compared Against the Original Plan

**Written:** 2026-08-07
**Purpose:** `deferred_models_why_phenotyping_first.md` (2026-04-18) laid out, in detail, why
Game Theory (GaT) and Agent-Based Modeling (ABM) were deferred until after Step 2
phenotyping, and made specific predictions about *how* phenotyping would be used once they
were implemented. Both notebooks were built on 2026-08-06/07 (`46_ds5_game_theory.ipynb`,
`47_ds5_agent_based.ipynb`). This document closes the loop: it checks the original reasoning
against what was actually built, and states plainly where the plan held and where it did not.
It does **not** re-derive GaT/ABM's methods, results, or figures — that material is already
documented in full in `outputs/reports/paper_prep/ds5_gat_paper_prep.md` and
`ds5_abm_paper_prep.md`, which are more current and more detailed than anything below. This
document's only job is the before/after reconciliation.

---

## 1. What the deferral document predicted

`deferred_models_why_phenotyping_first.md` §3–4 made two concrete, falsifiable predictions:

**For GaT:** phenotyping would first identify discrete profiles (illustrated with 3
hypothetical types — "stable self-regulators," "chronic over-riders," "susceptible/near-
tipping-point"), and GaT would then become a **within-phenotype equilibrium analysis**:
build a payoff matrix and compute an equilibrium *separately for each cluster*, rather than
running one pooled analysis. Quote: "GaT will use the cluster labels as agent-type
definitions. Notebook 46 will then implement payoff matrices and equilibrium analysis for
each cluster separately, rather than for all participants pooled."

**For ABM:** Step 2's cluster profiles would supply discrete **agent types** (3–4 of them,
each with an illustrative parameter vector), and each agent type would run the ABM's
behavioral rules; StoP's per-participant `mu_hat`/`sig_hat` and NeT's transition matrix would
additionally calibrate those type-level rules. Quote: "Notebook 47 will define agent types
from Step 2 cluster profiles, calibrate agent parameters from Step 1 model outputs, and
simulate the population-level response distribution."

Both predictions assumed the phenotype axis identified by Step 2 (NeT's `profile_p1` Profile
A/B split, and/or the C1/C2/C3 behavioral-dynamic axis) would supply the primary structuring
variable for both models.

---

## 2. What was actually built, and where it diverges

### GaT — the payoff/equilibrium apparatus was never built at all

The implemented `46_ds5_game_theory.ipynb` explicitly declines to construct any payoff
matrix, best-response function, or equilibrium concept (FLAG G3, stated directly in the
notebook and in `ds5_gat_paper_prep.md` §2). This is a larger divergence from the original
plan than a simple simplification — the entire mechanism the deferral document argued
phenotyping would unlock ("payoff matrices and equilibrium analysis for each cluster
separately") does not exist in the implementation. Instead, `profile_p1` (Profile A/B) is
used exactly once, as a **post-hoc two-group overlay** on a purely descriptive quantity
(`commitment_score` = rate of not-opening), tested with a Welch t-test.

The result of that overlay is also the opposite of what the deferral document's illustrative
example implied. The 2026-04-18 document sketched Profile A/B/C as *payoff-relevant* types
whose behavior should differ sharply under a game-theoretic reading. What was actually found:
**no significant phenotype effect** (Profile A mean=0.353 vs. Profile B mean=0.316; Welch
t=1.627, p=0.105, d=0.179 — small and non-significant), against a **strong condition effect**
on the same variable (F=40.99, p<0.001). Phenotyping did not "unlock" a within-phenotype
equilibrium story for GaT — if anything, it demonstrated that this particular phenotype axis
is *not* the relevant heterogeneity dimension for the commitment-score outcome, and that
condition (not pre-existing network topology) is what drives it.

### ABM — individual-level calibration, not phenotype-level agent types

The implemented `47_ds5_agent_based.ipynb` also diverges from the plan, but in the opposite
direction: rather than collapsing participants into 3–4 discrete phenotype-derived agent
types (as the deferral document's Profile A/B/C sketch proposed), it calibrates **one agent
per participant**, using that participant's own already-fitted StoP SDE parameters
(`mu_hat`, `sig_hat`) directly — i.e., the *individual* parameter granularity Step 1 already
produced, not a phenotype-reduced abstraction. `profile_p1` is used only for a secondary,
descriptive "does the phenotype rank order reproduce" check, not as the generative agent-type
definition the original plan called for.

This turned out to matter for the result: the ABM's validation gate **fails** (Spearman
ρ=0.428 between observed and simulated `x_mean`, against a pre-registered ρ≥0.80 threshold)
— a bounded SDE agent with realistic σ/μ ratios converges ergodically toward 0.5 over a
30-day simulated horizon regardless of starting parameters, systematically underestimating
high-rate participants by roughly 11 percentage points (full mechanism in
`ds5_abm_paper_prep.md` §5). The phenotype *rank order* (Profile B > Profile A) is still
reproduced, but the absolute values are not — meaning the one part of the original plan that
*was* followed (using phenotype for a validation check) is also the one part of the ABM
result that still held up.

---

## 3. What the phenotyping-first sequencing decision itself looks like in hindsight

The sequencing argument in §5.1 of the deferral document — GaT and ABM should not be
attempted before Step 2, because doing so would only support pooled average-treatment-effect
claims that add nothing beyond what Step 1 already provides — is **not falsified** by any of
the above. Both notebooks, once built, did use Step 2 and/or Step 1 outputs as inputs (GaT via
the `profile_p1` overlay and the Stage 1 behavior-feature table; ABM via per-participant StoP
parameters). Neither was attempted on raw, uncharacterized behavioral counts. The sequencing
was correct in the narrow sense that it was logistically necessary (both notebooks needed
Step 1/2 outputs to exist as input files) — but the *specific mechanism* imagined for how
phenotyping would be used (discrete agent types, per-cluster equilibria) did not survive
contact with implementation for either model family.

The honest summary: phenotyping-first was the right sequencing decision for structural
reasons (dependency on Step 1/2 output files), but the deferral document's illustrative
Profile A/B/C examples should be read as motivating narrative, not as a prediction that
came true. Both GaT and ABM ended up simpler and more individual-grounded than planned, and
both produced genuine null/negative results (GaT: no phenotype effect; ABM: gate failure)
rather than the richer heterogeneity story the deferral document anticipated. This is
consistent with — and worth citing alongside — the cross-dataset pattern already recorded in
`outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md` §2 (GaT: "4-for-4" no
observed payoff structure across every dataset assessed; ABM: "three independent failures of
the same kind" across DS5/DS4/Structured).

---

## 4. SyD — the third deferred model, status check

`deferred_models_why_phenotyping_first.md` §2 deferred System Dynamics (SyD) to DS6 for a
structural reason unrelated to phenotyping: DS5 has only two survey waves (pre/post), and SyD
needs at least 3–4 waves to identify a feedback-loop structure. This reasoning has since been
confirmed correct and acted on: DS6's SyD notebook (`78_ds6_system_dynamics.ipynb`) was
implemented and completed on 2026-08-06, using `addiction_index_change` and
`self_control_index_change` as formal stock quantities — exactly the kind of repeated-wave
psychosocial measurement DS5 lacks. DS6's SyD result was a genuine null (both feedback-loop
hypotheses non-significant after regression-to-the-mean control), which does not bear on
whether the deferral reasoning itself was sound — it was, and the dataset match (DS6 over
DS5) was the correct call.

---

## 5. Net assessment

| Deferred model | Original prediction | What was actually built | Prediction survived? |
|---|---|---|---|
| GaT | Payoff matrix + equilibrium, computed separately per phenotype cluster | No payoff/equilibrium apparatus at all; phenotype used only as a post-hoc overlay on a descriptive ratio | **No** — mechanism never built; overlay found null, not the anticipated split |
| ABM | 3–4 discrete phenotype-derived agent types, calibrated from Step 1 + Step 2 | One agent per participant, calibrated from individual Step 1 (StoP) parameters only; phenotype used only for a secondary rank-order check | **No** — finer-grained than planned; the one phenotype-based check that *was* kept (rank order) is the part of the result that held up |
| SyD | Deferred to DS6 for a structural (survey-wave) reason, unrelated to phenotyping | Implemented on DS6, exactly as planned | **Yes** |

Phenotyping-first was justified as a sequencing/dependency decision, not because it produced
the specific discrete-agent-type or per-cluster-equilibrium mechanisms envisioned when the
deferral was written. Both GaT and ABM are best read, per the cross-dataset synthesis, as
confirmatory/organizing analyses layered on quantities other Step 1 families already
established, rather than as the phenotype-driven discovery engines the original plan
anticipated.

---

*Written 2026-08-07 as part of the DS5 post-analysis update, alongside
`ds5_v2_revision_and_phenotype_addendum.md` and `ds5_step3_personalization_addendum.md`. Full
GaT/ABM methods and results: `outputs/reports/paper_prep/ds5_gat_paper_prep.md`,
`ds5_abm_paper_prep.md`.*
