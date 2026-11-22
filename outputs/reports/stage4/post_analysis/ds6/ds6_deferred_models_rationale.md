# Deferred Models Rationale — DS6 (GaT and ABM), as of 2026-08-08

**Overlap check:** Read in full — `outputs/reports/stage4/post_analysis/deferred_models_why_phenotyping_first.md`
(DS5's original deferral reasoning, for the general logic pattern DS6's plan reused) and
`outputs/reports/stage4/post_analysis/ds5_gat_abm_deferred_resolution.md` (DS5's own
resolution document, cited below rather than re-derived — it already covers DS5's GaT/ABM
methods, results, and timing in full). **Scope of this file:** whether DS6's GaT/ABM
deferral is still just "waiting on Step 2," or something else, verified directly against the
current repository state rather than assumed from the plan document — this is a status check
plus a substantive comparison of DS6's structural situation to DS5's and Structured's, not a
resolution document (there is nothing to resolve yet: DS6's GaT/ABM notebooks do not exist).

---

## 1. Verified current status (checked directly, not assumed from any planning document)

```
$ find . -iname "*ds6*gat*" -o -iname "*ds6*agent*"
(no results)
$ ls notebooks/ | grep ds6
14_ds6_feature_extraction.ipynb
50_ds6_model_prototypes.ipynb
71_ds6_statistical_mechanics.ipynb
72_ds6_dynamical_systems.ipynb
73_ds6_stochastic_processes.ipynb
74_ds6_network_models.ipynb
75_ds6_information_theory.ipynb
78_ds6_system_dynamics.ipynb
140_ds6_phenotype_exploration.ipynb
141_ds6_behavior_only_phenotype.ipynb
$ ls outputs/model_outputs/ds6/
dynamical_systems  information_theory  network_models  phenotyping
phenotyping_path_a  statistical_mechanics  stochastic_processes  system_dynamics
```

**`76_ds6_game_theory.ipynb` and `77_ds6_agent_based.ipynb` do not exist.** There is no
`outputs/model_outputs/ds6/game_theory/` or `outputs/model_outputs/ds6/agent_based/`
directory. There is no DS6 GaT or ABM blueprint anywhere in `outputs/reports/`. The only
mentions of notebooks 76/77 anywhere in the repository are the reserved-slot lines in
`outputs/reports/stage4/ds6_step1_plan.md` itself (the numbering table and the "deferred,
pending Step 2" status line) — no planning work beyond that reservation has been done.

**This is a plain fact, not an inference:** as of this writing, GaT and ABM are the only two
of DS6's eight nominal CAS model-family slots with zero implementation artifacts of any kind
(no blueprint, no notebook, no output directory, no companion documentation).

---

## 2. What the original DS6 plan said, and whether its stated precondition has been met

`ds6_step1_plan.md` §4, point 7 (written 2026-08-06, before any DS6 model existed):

> "GaT (76), ABM (77) — deferred, same reasoning as DS5: GaT awaits behavioral profiles from
> Step 2 phenotyping; ABM needs prior model characterization."

This is a direct restatement of DS5's own deferral logic
(`deferred_models_why_phenotyping_first.md` §3–4): GaT needs discrete behavioral profiles to
parameterize a payoff structure per group; ABM needs both Step 1 parameter characterization
and Step 2 profile/agent-type definitions.

**That stated precondition has been satisfied for DS6 since 2026-08-06** — the same day the
plan was written. DS6 Step 2 phenotyping (notebook 140, the main pass) and its follow-up
(notebook 141, Path A′) were both completed and fully documented that same day, per this
project's own status record (`ds6_step1_plan.md`'s own "Status" table; corroborated directly
by the `model_run_summary.md` "Run at" timestamps for both notebooks:
`2026-08-06 14:48:39` for 140 and `2026-08-06 15:42:12` for 141). As of this writing
(2026-08-08), that is **two days** during which the stated blocking condition for both GaT
and ABM has been cleared, with no DS6 GaT/ABM work begun.

---

## 3. Comparison to DS5 and Structured's own GaT/ABM timing

Per `ds5_gat_abm_deferred_resolution.md` (not re-derived here, only compared): DS5's GaT and
ABM notebooks (46, 47) were built on **2026-08-06/07** — essentially immediately following
the completion of DS5's own Step 2 phenotype-revision arc (the "v2" notebooks, `60`–`64`,
which closed 2026-08-05/06). Per CLAUDE.md's own Structured narrative, Structured's GaT and
ABM were likewise built in direct sequence once Structured's own single-pass Step 2 completed
— "Step 1 and single-pass Step 2 are both complete" is immediately followed in the project's
own record by GaT then ABM, with no gap noted between phenotyping completion and GaT/ABM
implementation in either case.

**DS6 is therefore the first dataset in this project where GaT/ABM completion has not
followed Step 2 phenotyping completion in the same working session or the next one.** Both
DS5 and Structured moved from "Step 2 done" to "all 8 families implemented" without an
apparent gap; DS6 has now gone two days with Step 2 done and GaT/ABM untouched.

---

## 4. Two candidate explanations — separated explicitly as interpretation, not fact

Nothing in the repository states *why* DS6's GaT/ABM work has not started. The two
explanations below are offered as reasoned interpretation, clearly marked as such, not as
confirmed facts the way the status check in §1 is.

### 4a. A scheduling / attention gap (plausible, not GaT/ABM-specific)

Immediately after DS6 Step 2 closed on 2026-08-06, the same day and the two days following
were occupied by: the DS6 sanity-check audit (2026-08-06), DS6 Path A′ (2026-08-06), a
full cross-dataset documentation and figure audit spanning every dataset in the project
(2026-08-07), the start of Stanford Health Study work (2026-08-07), and this post-analysis
reporting task itself (2026-08-07/08). CLAUDE.md's own DS6 section explicitly notes "this
repo runs multiple concurrent Claude Code sessions" — a documented project-level fact, not
speculation. Under this explanation, DS6's GaT/ABM gap is simply that project attention moved
elsewhere before circling back, the same way DS4/DS1 work has also not resumed since DS6
started. This explanation requires no DS6-specific technical obstacle and is consistent with
the plan document's own closing line: "Not yet discussed: DS6 Step 3 (personalization,
matching DS5's precedent) or a return to DS4/DS1 per the project's original dataset order" —
GaT/ABM simply were not yet discussed either.

### 4b. A genuine, DS6-specific operationalization obstacle for GaT (not for ABM)

DS5's implemented GaT (per `ds5_gat_abm_deferred_resolution.md` §2) never built a formal
payoff matrix or equilibrium concept at all — it used `commitment_score = rate_not_opened`,
an **outcome-variance-dependent** descriptive proxy (the rate at which a participant does
*not* open despite friction), tested as a post-hoc phenotype overlay. Structured's own GaT
used a comparably outcome-dependent `commitment_score`, built from its own genuine completion-
outcome variable (task completion, derivable from `update_type` transitions).

**DS6 has no outcome variable of any kind** — this is the same structural fact
(`data_docs/modeling_cautions.md` §6) that forced every other DS6 family to substitute a
different quantity for its DS5 analog (see `ds6_model_data_usage_map.md`'s substitution
table). DS5's specific `commitment_score` proxy **cannot transfer to DS6 in any form** —
there is no "did not open" event to count. A DS6 GaT notebook would need an entirely new,
not-yet-designed outcome-free proxy (candidates that would need to be evaluated from
scratch — none has been attempted or blueprinted anywhere in the DS6 file record — might
include period-level volume reduction as a "cooperate" signal, or `hhi_change`/regime
stability as a commitment analog). This is a **more severe** design obstacle than either DS5
or Structured faced, since both of those datasets at least had *an* outcome-based candidate
to build a descriptive proxy from, however far from a formal game-theoretic apparatus.

**ABM does not share this obstacle.** DS5's ABM (per `ds5_gat_abm_deferred_resolution.md`
§2) calibrates one agent per participant directly from that participant's own already-fitted
StoP SDE parameters (`mu_hat`, `sig_hat`) — DS6 already has exactly this kind of per-
participant StoP output (`participant_stop_parameters.csv`, `mu_hat_*`/`sig_hat_*` per
period), fully analogous in kind to DS5's. There is no missing-outcome-variable obstacle
specific to ABM the way there is for GaT. **This asymmetry is worth stating plainly: whatever
is holding back DS6's GaT may be a real, substantive design problem; whatever is holding back
DS6's ABM does not appear to be.**

---

## 5. Net assessment

| Question | Answer |
|---|---|
| Do DS6 GaT/ABM notebooks exist? | **No** — verified directly, not assumed |
| Has the plan's stated precondition (Step 2 complete) been met? | **Yes**, since 2026-08-06 — two days before this writing |
| Did DS5/Structured show a similar gap between Step 2 completion and GaT/ABM? | **No** — both moved to GaT/ABM in the same or next session |
| Is there a documented technical reason for DS6's gap? | **No** — nothing in the repository states one |
| Is there a plausible undocumented technical reason, specific to GaT? | **Yes, plausible** — DS5's `commitment_score` proxy cannot transfer to DS6 (no outcome variable at all); a replacement proxy has not been designed |
| Is there a plausible undocumented technical reason, specific to ABM? | **No** — DS6 already has the same per-participant StoP calibration input DS5's ABM used; no missing-data obstacle identified |

**Plain statement:** this is a genuine, currently open gap in the DS6 program, not a resolved
or well-explained extension of the original deferral. It should not be read as evidence that
DS6's Step 2 phenotyping was somehow insufficient to unblock GaT/ABM (per §2, it was, on the
plan's own stated terms) — it is better read as an unstarted piece of work, with GaT facing a
real, unaddressed design question (a replacement for `commitment_score`) that ABM does not.
If DS6 work resumes on these two families, ABM could plausibly proceed directly following the
DS5/Structured pattern (one agent per participant, calibrated from StoP parameters, checked
against Step 2 cluster profiles for a rank-order or magnitude validation); GaT would need a
new blueprint section addressing the missing-outcome-variable problem before implementation
could begin at all, since DS5's own solution to that same generic problem does not
carry over.

---

*Written 2026-08-08 as part of the DS6 post-analysis reporting set.*
