# Deferred-Model Status and Documentation-Gap Note — Structured

**Written:** 2026-08-08
**Overlap check:** Read in full before writing — `outputs/reports/stage4/post_analysis/deferred_models_why_phenotyping_first.md`
and `ds5_gat_abm_deferred_resolution.md` (DS5's deferral-reasoning and deferral-resolution documents,
whose comparison structure this document borrows), `outputs/reports/synthesis/cross_dataset_cas_model_synthesis.md`
§0 (the cross-dataset completion-status table), and `outputs/reports/synthesis/documentation_audit_findings_2026-08-07.md`
§4 (the documentation-gap finding this note tracks and, as verified directly below, updates). **This
document does not exist in any form for Structured yet** — no prior report states plainly that Structured
has zero currently-deferred model families, and the documentation-gap finding on record for Structured is,
as of this writing, out of date and has not been corrected anywhere. Both points are recorded here because
neither has a dedicated home elsewhere.

---

## Part 1 — Structured is the only dataset in this project with zero currently-deferred model families

| Dataset | Model families implemented | Currently deferred / excluded | Reason |
|---|---|---|---|
| DS5 | 7/8 (StM, DyS, StoP, NeT, InT, GaT, ABM) | SyD | Permanently moved to DS6 — DS5 has only 2 survey waves (pre/post), SyD needs 3–4+ |
| DS6 | 7/8 (StoP, NeT, InT, DyS, SyD, StM) | GaT, ABM | Still formally deferred pending further Step 2 work, per CLAUDE.md's DS6 section — not yet unblocked even though DS6 Step 2 (phenotyping) is complete |
| DS4 | 7/8 | SyD | Permanently excluded — no repeated survey waves, a structural data limitation, not a sequencing choice |
| **Structured** | **8/8 — all families implemented** | **None** | — |

Structured is the only dataset in the project's entire cross-dataset table
(`cross_dataset_cas_model_synthesis.md` §0) with a full 8/8 and nothing outstanding. This is worth stating
explicitly rather than leaving implicit in the modeling-plan chronicle, since every other dataset's
"Step 1 status" line carries a permanent asterisk of some kind.

### Structured's own deferral history was narrower than DS5's to begin with

Unlike DS5 (which deferred **both** GaT and ABM pending Step 2 phenotyping — see
`deferred_models_why_phenotyping_first.md` §3–4), Structured deferred **only ABM**. GaT was implemented
as an active, non-deferred family at the same stage as NeT/InT/StoP/DyS/SyD/StM — the eighth status
update in `structured_cas_modeling_plan.md` reports it as "the final active model family" (i.e., the last
of the seven non-deferred families, not a deferred one), built and executed on 2026-08-03, well before
Step 2 phenotyping existed (2026-08-03, later that same day, per the ninth status update). This differs
from DS5, where the reasoning in `deferred_models_why_phenotyping_first.md` §3 explicitly argued GaT's
payoff structure "cannot be estimated without first characterizing behavioral types" and therefore had to
wait. Structured's GaT blueprint reaches a different operational conclusion for the same underlying
theoretical caution (the paper's own §1.3 groups GaT with StM under "requires more careful proxy
definitions," matching DS5's source paper's caution about GaT) — but resolves it by building an explicit
scalar proxy (`commitment_score`) and correlational tests immediately, rather than by waiting for
phenotype labels to exist. **This is a genuine cross-dataset difference in how the same theoretical
caution was operationalized, not an inconsistency to reconcile** — DS5's GaT needed discrete agent types to
define a payoff matix at all; Structured's GaT never built a payoff matrix, so it never needed discrete
types to parameterize one.

### Structured's ABM deferral-and-resolution was a closer match to its own blueprint than DS5's was

DS5's own `ds5_gat_abm_deferred_resolution.md` (2026-08-07) found that DS5's actual GaT/ABM
implementations diverged substantially from what the original 2026-04-18 deferral document predicted
(no payoff/equilibrium apparatus was ever built for GaT at all; ABM ended up calibrated per-individual
rather than per-phenotype-type). Structured's single deferred family, ABM, shows a **closer**
match between blueprint and outcome, though not a perfect one:

- **Predicted and confirmed exactly:** Model 1's Fano≈1 result was stated in the blueprint as
  "mathematically guaranteed, not an empirical finding" before running — confirmed (`Fano_sim,1
  mean=1.019`, per `outputs/model_outputs/structured/agent_based/model_run_summary.md`).
  Model 2 was predicted to be "substantially >1 and much closer to `created_Fano_factor`" — confirmed
  directionally (`Fano_sim,2 mean=3.377` vs. real mean 6.011), though the blueprint did not commit to a
  specific fraction of the gap closed in advance, so "47% of the gap closed" is a post-hoc quantification
  of a directionally-correct prediction, not a number stated beforehand.
- **Not predicted, found only by explicitly checking:** the blueprint's Part 4 stated the phenotype-mixture
  test would show "whether two simple archetypal rule-sets reproduce the separation Step 2 found
  empirically, or does the real separation require more" — a genuinely open question, not a one-sided
  prediction. What was actually found (separation magnitude reproduced, KS 0.351 vs. 0.375, but
  **direction reversed**, real A>B vs. simulated B>A) was not anticipated either way in the blueprint text
  itself; it was caught only because the notebook explicitly checked direction rather than stopping at the
  magnitude match. This matches the same qualitative outcome as DS5's own ABM (a partial, honestly-reported
  limitation rather than a clean confirmation), but Structured's ABM blueprint made fewer, narrower
  advance claims than DS5's GaT/ABM deferral document did, which is part of why the "prediction survived"
  bar is easier to clear here — a difference in how much the blueprint committed to in advance, not a
  difference in how rigorously the result was checked.

**Net comparison:** Structured's smaller, single-family deferral (ABM only) produced a documented outcome
close to what its own blueprint anticipated for the mechanism-level claims, with the same class of
population-level limitation (direction-reversal at the coarsest phenotype-mixture level) that DS5's and
DS4's own ABM implementations independently hit — the "three independent failures of the same kind"
pattern already named in `cross_dataset_cas_model_synthesis.md` §2. Structured's narrower deferral scope
(one family, not two) is itself a difference worth naming: DS5 deferred a whole *mechanism type* it never
ended up building (game-theoretic equilibria), while Structured never had that mechanism type as part of
its deferred scope to begin with.

---

## Part 2 — Documentation-gap tracking, including a correction to the standing audit finding

### What the audit found (2026-08-07)

`documentation_audit_findings_2026-08-07.md` §4 recorded: **"Structured — the largest and most systemic
gap: 48 CSVs across all 8 model families + phenotyping have no individual companion `.md`. Every folder
instead has one shared `model_run_summary.md` covering all its CSVs — a different, older convention than
DS6's per-file standard."** The audit flagged this as "a real policy question, not a hygiene oversight,"
recommending it be settled once in `CLAUDE.md` rather than per-dataset.

### What is actually true as of this writing (verified directly against the file system, 2026-08-08)

**This gap has since been fully closed.** A direct count across every Structured model-output directory
(`outputs/model_outputs/structured/{network_theory,information_theory,stochastic_processes,
dynamical_systems,system_dynamics,statistical_mechanics,game_theory,agent_based,phenotyping}/` and all
four phenotyping sub-paths `path_a/path_c/path_d/path_f/`) finds:

- **47 CSVs total**, **47 individual companion `.md` files total** (one per CSV, verified by exact
  filename match — zero CSVs found without a matching companion), **plus 13 `model_run_summary.md`
  files** (one per folder, retained as the folder-level narrative document, not replaced).
- File timestamps show every individual companion `.md` was written on 2026-08-07 between 21:37 and
  21:56 — i.e., **after** the audit document (also dated 2026-08-07) identified the gap, most plausibly a
  same-day remediation pass, though this document does not have direct evidence of who ran it or exactly
  when relative to the audit's own write time, only the file-modification-time ordering.
- Spot-checked two of the new companions directly (`network_theory/participant_network_metrics.md`,
  `phenotyping/path_f/joint_taxonomy_independence_test.md`) — both are substantive, full-format companion
  docs (unit of observation, column reference table, how-produced, known limitations, load snippet),
  matching this project's standing per-file documentation convention exactly, not placeholder stubs.

**Consequence for the policy question the audit raised:** Structured has now been unilaterally upgraded
to the per-file standard the audit contrasted it against (DS6's convention, established 2026-08-06) —
whether by explicit decision or as a side effect of other work, this document does not attempt to
adjudicate. **The audit's characterization of Structured as "the largest and most systemic gap" in the
project is no longer accurate and should not be repeated in future sessions without re-checking the file
system first** — this is exactly the kind of stale-chronicle risk this project's own working principles
warn against ("verify every number by opening the actual source file, not by trusting the chronicle doc's
own prose"), and it applies to audit documents themselves, not only to blueprints and status updates.

### What remains a genuine, still-open gap elsewhere (for contrast, not fixed here)

Per CLAUDE.md's own "Known documentation gap" note and the audit's §4: **DS5's original Step 1 notebooks
(41–45) still lack companion `.md` files for their primary per-participant CSVs**
(`participant_parameters.csv`, `participant_dynamics_parameters.csv`, `participant_stm_parameters.csv`,
`participant_network_metrics.csv` — only the later v2-revision-arc outputs have companions). That gap is
explicitly marked "leave as-is unless specifically asked to fill it" in CLAUDE.md and is **not** addressed
by this note — it is a pre-existing, accepted exception for DS5's earliest notebooks, structurally
different from Structured's now-closed gap (which was closed, not accepted as a standing exception). DS4
has zero gaps (confirmed in the same audit). DS6 was the dataset that originally established the per-file
convention. **Structured now matches DS4 and DS6's standard; only DS5's pre-April 41–45 outputs remain a
standing, deliberately-unaddressed exception.**

---

## Part 3 — Combined summary

Structured is simultaneously the project's **most complete** dataset by model-family count (8/8, zero
deferred) and, as of this writing, no longer its **documentation exception** — a status that did not exist
anywhere in the project's written record until this note. Both facts matter for the thesis narrative in
different ways: the model-completeness fact is a genuine scientific/scope claim (every one of the eight
CAS families named in the theory paper has been operationalized and executed on this dataset, with results
ranging from strong confirmations — GaT's non-monotonic commitment curve — to genuine nulls — StM's and
GaT's converging path-dependence nulls, Path D's infeasible clustering); the documentation-parity fact is
a project-hygiene claim about this specific repository's own internal consistency, useful mainly for
anyone auditing reproducibility later, and now accurate rather than a known weak point.

---

*Written 2026-08-08 as part of the Structured post-analysis waypoint. No DS5-template equivalent document
covers this exact combination (deferred-status contrast + documentation-gap correction) — it was written
because both facts were found to be true, verified, and previously undocumented during this task, not
because a DS5 counterpart exists to mirror.*
