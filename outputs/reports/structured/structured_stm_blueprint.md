# Structured — Statistical Mechanics (StM) Blueprint

**Notebook:** `notebooks/61_structured_statistical_mechanics.ipynb`
**Written:** 2026-08-03
**Position:** 61 in the Structured 60–68 decade. Depends on `structured_task_lifecycle_features.csv`
directly (per this project's dependency chain, StM was expected to depend on StoP's output — but see
Part 0 for why that DS5-specific dependency does not transfer here).
**Depends on:** `outputs/features/structured/structured_task_lifecycle_features.csv`,
`structured_behavioral_clean.csv`
**Output root:** `outputs/model_outputs/structured/statistical_mechanics/`

---

## Part 0 — Design principle: the largest departure from DS5 so far, and why

DS5's StM notebook (`41_ds5_statistical_mechanics.ipynb`) built a literal two-state Ising-like
thermodynamic apparatus on top of its own StoP model: an inverse temperature `β_behav = 2/σ̂²` (derived
from StoP's fitted diffusion parameter, flagged there as `CRITICAL FLAG A: an approximation`), a
two-state partition function `Z_2`, a free energy `F_behav`, and a susceptibility `χ_behav = β·p·(1−p)`.

**The Structured theory paper's own §2.1 explicitly cautions against this for Structured data**, in
language noticeably more careful than DS5's own source paper:

> "The model must be used carefully, because quantities such as energy, temperature, and equilibrium are
> not directly observed in task-log data. **They would need to be treated as analogy-based constructs or
> derived proxy quantities rather than literal physical variables.**"

Two consequences follow directly:

1. **No literal β/T/Z/F apparatus is built here.** DS5's `β_behav = 2/σ̂²` formula has no mathematical
   justification for Structured — it was derived specifically from a bounded-rate constant-drift SDE
   (DS5's own StoP model), and Structured's StoP model (notebook 63) fits an unbounded daily *count*
   process instead, which does not reduce to the same two-state Boltzmann bridge DS5 used. Forcing that
   formula onto count data would be a much less defensible transplant than any design choice made in the
   four Structured model notebooks built so far. **This notebook does not consume StoP's output at all.**
2. **The microstate itself is a different kind of object.** DS5's microstate was binary
   (opened / not-opened, a single outcome). The Structured paper's own worked example defines a
   microstate as a **joint task configuration** — multiple properties combined:

> "a task is not only counted as 'created' or 'completed,' but is represented as a configuration of
> properties: whether it is timed or all-day, whether it remains in the inbox, whether it has a
> duration, whether it is recurring, whether it has notes or subtasks, whether it has alerts, and
> whether it is eventually marked as completed... Each task configuration can be treated as a
> microstate."

What *is* implemented, using statistical/empirical measures rather than a literal thermodynamic model,
directly following the paper's own named constructs (stability, susceptibility, path dependence) instead
of DS5's β/T/Z/F machinery: **joint configuration entropy, macrostate concentration and persistence, a
susceptibility measure (completion-rate sensitivity to configuration), and a path-dependence test.**

---

## Part 0.5 — Non-redundancy check against InT and DyS

| Already computed | Notebook | What it covers | What StM adds |
|---|---|---|---|
| `H_type_last`, `H_completion`, `H_recurrence`, etc. | InT (65) | **Marginal** entropy of one property at a time (task type alone, completion alone, ...) | The **joint** entropy of the full multi-property configuration together — a genuinely higher-dimensional object; verified below that joint entropy ≥ any marginal, as it must be |
| Weekly 5-dim composition vector + continuous trajectory volatility | DyS (62) | Continuous **share**-based weekly state, Euclidean-distance volatility | A **discrete** macrostate (the single dominant configuration) and its **persistence** — does the *same* dominant regime repeat week to week, a different, coarser stability question than DyS's continuous drift-through-state-space framing |
| — | — | Neither InT nor DyS asks whether completion *probability* depends on task structure for a given user, or whether structure changes after a non-completion streak | **New**: susceptibility (completion-rate sensitivity to configuration) and a path-dependence test — both explicitly named phenotypes in the paper's StM section that no other notebook covers |

**Conclusion: not redundant.** Confirmed before writing any code.

---

## Part 1 — The microstate: joint task configuration

**Two related configurations, not one — a correction made during implementation, recorded here.** The
paper's own property list explicitly includes completion status: *"whether it is timed or all-day...
whether it is recurring, whether it has notes or subtasks... and whether it is eventually marked as
completed."* An initial draft of this notebook defined the microstate without completion, then compared
its entropy `H_config` against InT's `H_completion` marginal — an invalid comparison, since completion
wasn't part of the config being compared — which produced a chain-rule "violation" in 21/53 participants
and caught the design gap. Fixed by using two configurations for two different purposes:

```
full_config       = (task_type_last, task_is_recurring_ever, task_has_notes_last, has_subtasks, lifecycle_status)
                     -- matches the paper's property list; used for H_config, macrostate, persistence.
                     Uses the full 3-class lifecycle_status (completed/deleted/unresolved), NOT a binary
                     completed-vs-not collapse -- a second correction made during implementation: an
                     earlier attempt used a binary flag, which still failed the chain-rule check against
                     InT's H_completion (4/53 violations) because collapsing categories only reduces
                     entropy relative to the finer 3-class marginal being compared against. Must match
                     InT's own variable exactly for the sanity check in Part 2 to be valid.
structural_config = (task_type_last, task_is_recurring_ever, task_has_notes_last, has_subtasks)
                     -- completion deliberately excluded; used ONLY for the susceptibility analysis
                     (Part 4), where completion is the predicted outcome, not a config component --
                     including it there would make "does completion depend on configuration" circular
```

Both available for **every** task regardless of censoring status (unlike creation-time properties used
by InT/DyS/SyD, which require `has_creation_event=True`), using each task's **last-known** state.
`has_subtasks = subtasks_amount_last > 0`. `task_alerts` and `task_energy_level` are excluded from both —
confirmed absent from the export (`structured_cas_modeling_plan.md` §2), exactly as the paper's own list
names them but this dataset cannot supply them.

**Verified before finalizing (structural_config space):** 20 of the 24 mathematically possible
combinations (`3 task_type × 2 recurring × 2 notes × 2 subtasks`) are actually observed in the data.
Distinct structural configurations observed per participant range 2–15 (median 4) — consistent with the
paper's own framing that most of the configuration space is sparse and only a few configurations
dominate any one user's behavior. (`full_config` adds the completion dimension on top, doubling the
possible space to 48; reported separately in the notebook, same sparsity pattern expected.)

Duration is deliberately **not** included in the core configuration (it is only meaningfully defined for
`timed` tasks, which would break a uniform configuration definition across task types) — instead used as
a **supplementary** susceptibility check within timed tasks only (Part 4).

---

## Part 2 — Macrostate: dominant configuration, concentration, and label

For each participant with `n_tasks ≥ 10` (same threshold already justified for task-level entropy
measures in the InT blueprint — reused because it is the same kind of object, not copied from DS5):

- `H_config` = Shannon entropy of the `full_config` distribution (verified `≥` the InT marginal entropy
  of each of its own five component properties — `H_type_last`, `H_completion`, and the binary entropy
  of `task_is_recurring_ever` — as the chain rule of entropy requires for variables that are genuinely
  part of the joint distribution being compared; checked in the notebook, not assumed, after both the
  InT bridge bug and this notebook's own initial config-vs-completion mismatch taught this project not
  to assume entropy inequalities hold without checking exactly which variables are being compared)
- `n_distinct_configs`, `top1_config_share` (HHI-style concentration on the single most common
  configuration)
- `macrostate_label`, directly from the paper's own named regimes (System Stability bullet: "inbox-heavy
  planning, timed-task planning, sparse planning, or completion-oriented planning"):
  ```
  if top config's task_type == "timed" and (recurring or notes or has_subtasks): "high-structure"
  elif top config's task_type == "timed":                                        "timed-basic"
  elif top config's task_type == "inbox":                                        "inbox-heavy"
  elif top config's task_type == "all_day":                                      "all-day-dominant"
  ```

---

## Part 3 — Macrostate persistence across weeks ("how stable is this macrostate... across repeated
weeks" — paper's Example A, verbatim)

Reuses the participant-relative weekly indexing already established in DyS/StoP/SyD. For each week,
determine the dominant `task_type` among that week's created (non-censored) tasks; `persistence_rate` =
fraction of consecutive week-pairs where the dominant type is unchanged. Same `MIN_WEEKS=4` eligibility
already verified for DyS/SyD (same weekly-resolution object).

---

## Part 4 — Susceptibility ("differences in the sensitivity of the user's planning system to
task-structure parameters" — paper, verbatim)

For each eligible participant, group their tasks by configuration (using the top 3 most frequent
configurations, to keep cell sizes usable) and compute completion rate within each group.
`susceptibility` = variance of completion rate across these groups, weighted by group frequency — high
variance means completion strongly depends on which configuration a task has (structure-sensitive);
near-zero variance means completion is roughly configuration-independent for that person.

**Supplementary check (duration, timed tasks only):** completion rate for below-median vs. above-median
`task_duration_min_last` among each participant's `timed` tasks, reported separately since duration
cannot be folded into the core configuration.

---

## Part 5 — Path dependence ("path-dependent changes after repeated unresolved tasks" — paper,
verbatim)

For each non-censored task, in creation order per participant, compute `streak_length` = the number of
immediately preceding non-censored tasks (same participant) that ended `unresolved` or `deleted` (i.e.,
did not complete). Test whether `streak_length` predicts the current task having **any** extra structure
(`recurring or notes or has_subtasks`, binary). **Learning directly applied from the SyD notebook**:
report both the pooled correlation and a person-mean-centered (within-participant) version, since SyD
demonstrated a pooled panel correlation can be badly confounded by between-participant volume/structure
differences and even show the wrong sign.

---

## Part 6 — Output file structure

```
outputs/model_outputs/structured/statistical_mechanics/
  participant_stm_summary.csv       # H_config, n_distinct_configs, top1_config_share, macrostate_label,
                                     # persistence_rate, susceptibility, is_stm_eligible, is_persistence_eligible
  configuration_counts_long.csv     # participant_id, config tuple (4 cols), count, completion_rate
  path_dependence_test.csv          # pooled_r, within_participant_r, p-values, n (Part 5)
  figures/
    fig1_stm_config_entropy_vs_int_marginals.png   # sanity check: H_config >= each InT marginal
    fig2_stm_macrostate_label_distribution.png
    fig3_stm_susceptibility_distribution.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Theory paper §2.1 read in full and quoted directly above, including its explicit caution against
      literal energy/temperature/equilibrium variables
- [x] Confirmed DS5's β=2/σ̂² formula and two-state apparatus do not transfer — different microstate type
      (joint multi-property configuration, not binary outcome), different/no StoP dependency
- [x] Explicit non-redundancy check against InT (marginal vs. joint entropy) and DyS (continuous
      trajectory vs. discrete macrostate persistence) completed before writing any code
- [x] Configuration space and per-participant task counts verified against real data (20/24 configs
      observed; 53/61 participants meet the reused `n_tasks≥10` threshold)
- [x] Path-dependence test designed with the pooled-vs-within-participant check from the start,
      applying the SyD lesson proactively rather than discovering the need for it after the fact
- [x] Notebook 61 implemented and executed
