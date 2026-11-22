# Structured — Game Theory (GaT) Blueprint

**Notebook:** `notebooks/66_structured_game_theory.ipynb`
**Written:** 2026-08-03
**Position:** 66 in the Structured 60–68 decade — the final active model family (ABM remains deferred
until a phenotyping stage exists, same logic as DS5).
**Depends on:** `outputs/features/structured/structured_task_lifecycle_features.csv`,
`structured_participant_features.csv`, `structured_behavioral_clean.csv`
**Output root:** `outputs/model_outputs/structured/game_theory/`

---

## Part 0 — Paper grounding (§2.6, quoted) and the same caution StM required

> "Game Theory can be applied to Structured by framing planning as a repeated decision problem. When
> creating a task, a user can choose a more committed strategy, such as assigning it a specific time,
> duration, alert, recurrence, or subtasks. Alternatively, the user can choose a more flexible strategy,
> such as leaving the task in the inbox, making it all-day, or avoiding detailed task structure. Neither
> strategy is inherently better. The meaning depends on the user's goals, task context, and later
> outcomes."
>
> "Rescheduling can be interpreted either as adaptive strategy adjustment or as deferral, depending on
> whether it leads to later completion or repeated postponement."

The paper's own §1.3 groups GaT with StM under the same implementation caution: both "are conceptually
valuable, but require more careful proxy definitions" because their defining quantities are not directly
observed in the log data. For StM that meant no literal β/T/Z/F apparatus (see
`structured_stm_blueprint.md` Part 0). For GaT it means the same discipline applied to "payoff" and
"utility": **no formal game matrix, best-response analysis, or equilibrium concept is built here.**
What *is* built: an explicit, named **commitment index** (a proxy, not a utility function) and
correlational tests of how it relates to observed outcomes — descriptive game-theoretic *framing*, not
a solved game.

---

## Part 0.5 — Non-redundancy check against StM, NeT, SyD

| Already computed | Notebook | Covers | GaT's distinct contribution |
|---|---|---|---|
| `structural_config`, macrostate label, susceptibility | StM (61) | Joint configuration entropy/stability; completion sensitivity to *which* configuration a task has | A single ordered **commitment scalar** (not a categorical configuration) explicitly built to test the paper's flexibility-vs-commitment **trade-off**, including whether the relationship is even monotonic — StM never asked whether *more* structure is *better* |
| Inbox tasks deleted ~19% vs. timed ~1.9% (entry-state finding) | NeT (64) | A single descriptive rate comparison across 2 categories (task_type) | A continuous 6-level (0–5) commitment index across *all* structural dimensions simultaneously, testing the full trade-off curve, not just type |
| `reschedule_rate`, `dominant_loop_label` (overload-trending etc.) | SyD (68) | Backlog-level system dynamics of rescheduling | GaT reuses `reschedule_rate` as an input to phenotype labels but asks a different question: does rescheduling *change a user's subsequent commitment choices* (adaptive strategy vs. deferral), not backlog-level feedback |

**Conclusion: not redundant.** The commitment index and the trade-off-curve test are genuinely new; the
phenotype labels reuse existing per-participant rates as inputs (not recomputation) where the paper's
own named types overlap with quantities already justified elsewhere in this project.

---

## Part 1 — Commitment index (explicit proxy, not a utility function)

Built directly from the paper's own list of commitment signals — "a specific time, duration, alert,
recurrence, or subtasks" — using every one of those that is available (alerts confirmed absent from the
export, as documented throughout this project):

```
commitment_score = temporal_commitment(0=inbox, 1=all_day, 2=timed)
                  + is_recurring (0/1)
                  + has_subtasks (0/1)
                  + long_duration (0/1 — timed tasks only, 1 if duration_min_last > median; 0 for
                                    non-timed tasks, since duration commitment doesn't apply to them)
```

Range 0 (inbox, no structure) – 5 (timed + recurring + subtasks + above-median duration).

**Verified before finalizing:** `commitment_score` distribution across all 26,729 tasks is well spread
(not degenerate): 256 tasks at 0, up to 11,863 at 3 (the mode), tapering to 644 at 5.

---

## Part 2 — The trade-off curve (headline test)

Completion and deletion rate computed **per commitment_score value** (0–5), pooled across the sample —
verified before writing this design down:

| commitment_score | completion rate | deletion rate |
|---|---|---|
| 0 | 36.7% | 38.7% |
| 1 | 40.2% | 21.4% |
| 2 | **79.0%** | **5.0%** |
| 3 | 66.3% | 9.3% |
| 4 | 72.7% | 10.9% |
| 5 | 58.7% | 18.2% |

**This relationship is non-monotonic** — completion peaks at moderate commitment (score 2: simply
`timed`, without additional recurrence/subtasks/long-duration) and *declines* at maximum commitment
(score 5). Both minimal commitment (0–1) and maximal commitment (4–5) show worse outcomes than the
middle. **A single linear correlation coefficient would misrepresent this** (a U-shaped/inverted-U
relationship can have a near-zero linear correlation despite a strong real effect) — the binned rate
table is reported as the primary evidence, with a linear correlation reported alongside only as a
secondary, explicitly-caveated summary statistic, not the headline number.

This directly operationalizes the paper's own framing: *"Neither strategy is inherently better... A
timed task with an alert may represent a stronger commitment to future action, but it also creates a
higher expectation for execution."* The data are consistent with over-commitment (recurring + subtasks +
long duration, stacked on top of an already-timed task) being associated with *worse*, not better,
completion outcomes — plausibly because heavily-structured tasks tend to be larger, more aspirational
commitments (recurring habits, multi-step projects) that are intrinsically harder to finish, not because
structure itself is unhelpful.

**Within-participant check applied proactively** (the SyD/StM lesson, now applied before running rather
than after finding a suspicious result): report both the pooled binned pattern and a person-mean-centered
version, since a between-participant confound (some participants generally both use higher commitment
*and* complete more) could otherwise inflate or distort the pooled pattern.

---

## Part 3 — Phenotype labels (paper's Example B, rule-based, Step 1 descriptive scope)

Reuses already-computed per-participant rates rather than recomputing them, for participants with
`n_tasks ≥ 10` (same threshold justified in InT/StM):

```
mean_commitment_score, reschedule_rate, pct_tasks_completed  (from Stage 1 features + this notebook)

if mean_commitment_score in top tercile:                                    "commitment-oriented"
elif mean_commitment_score in bottom tercile:                                "flexibility-oriented"
elif reschedule_rate in top tercile and pct_tasks_completed in bottom tercile: "chronic-deferrer"
elif reschedule_rate in top tercile and pct_tasks_completed in top tercile:    "adaptive-rescheduler"
else:                                                                          "mixed"
```

**"Overload-prone"** (the paper's fifth named GaT phenotype) is **not recomputed here** — it is already
covered by SyD's `dominant_loop_label = "overload-trending"` (`structured_syd_blueprint.md`); this
notebook cross-references that result rather than duplicating it under a new name.

---

## Part 4 — Strategy adaptation after rescheduling ("adaptive strategy adjustment... or deferral")

For each non-censored task in creation order, `prior_reschedule_flag` = whether the immediately
preceding task (same participant) had ≥1 reschedule event. Tests whether `commitment_score` of the
*current* task differs following a preceding reschedule — pooled and within-participant (same
discipline as Part 2 and as StM's path-dependence test, but asking about *commitment level* after a
*reschedule* specifically, not *structure presence* after a *non-completion streak* — a related but
distinct trigger and a distinct outcome measure).

---

## Part 5 — Output file structure

```
outputs/model_outputs/structured/game_theory/
  commitment_outcome_curve.csv        # commitment_score, completion_rate, deletion_rate, unresolved_rate, n
  participant_gat_summary.csv         # mean_commitment_score, is_gat_eligible, phenotype_label
  strategy_adaptation_test.csv        # pooled_r, within_participant_r, p-values, n (Part 4)
  figures/
    fig1_gat_commitment_outcome_curve.png
    fig2_gat_phenotype_distribution.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Theory paper §2.6 read in full and quoted; §1.3's shared StM/GaT proxy caution applied identically
- [x] Explicit non-redundancy check against StM/NeT/SyD completed before writing any code
- [x] Commitment index built strictly from the paper's own named signals (alerts excluded, confirmed
      unavailable)
- [x] Trade-off curve verified against real data before finalizing the design — confirmed non-monotonic,
      which shaped the decision to report the binned curve as primary evidence rather than a single
      linear correlation
- [x] Within-participant check designed in from the start (proactive application of the SyD/StM lesson)
- [x] "Overload-prone" phenotype explicitly cross-referenced to SyD rather than recomputed
- [x] Notebook 66 implemented and executed
