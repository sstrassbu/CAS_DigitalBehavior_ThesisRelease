# Structured — Information Theory (InT) Blueprint

**Notebook:** `notebooks/65_structured_information_theory.ipynb`
**Written:** 2026-08-03
**Position:** 65 in the Structured 60–68 decade (see `structured_net_blueprint.md` Part 0 for the
numbering convention). No dependency on NeT (64), but reuses one NeT output for a cross-model bridge
(Part 5 below).
**Depends on:** `outputs/features/structured/structured_task_lifecycle_features.csv`,
`structured_participant_features.csv`, `structured_behavioral_clean.csv`,
`outputs/model_outputs/structured/network_theory/participant_network_metrics.csv`
**Output root:** `outputs/model_outputs/structured/information_theory/`

---

## Part 0 — Design principle for this notebook

**This is not a port of `45_ds5_information_theory.ipynb`.** DS5's InT notebook computed entropy over
constructs specific to the OneSec friction domain (`H_out` = intervention-outcome entropy, `H_emp` =
binned empirical entropy of a friction-response time series `X_t`, `H_SDE` = a bridge to DS5's already-
completed StoP model). None of those constructs exist here — Structured has no intervention outcome,
no `X_t` override-rate series, and no StoP model yet (StoP is notebook 63, not yet built). Copying that
structure would fabricate quantities this dataset doesn't support.

Instead, every entropy and mutual-information quantity below is taken directly from the theory paper's
own InT section (`Structured Planning as a Complex Adaptive System.pdf` §2.5, reproduced here):

> "Entropy could be computed over task types... Entropy could also be computed over creation sources,
> time of day, recurrence patterns, alert use, task categories, energy levels, or completion outcomes...
> Mutual information can extend this analysis by asking whether one variable reduces uncertainty about
> another. For example, task type may reduce uncertainty about completion; energy level may reduce
> uncertainty about movement or delay; creation source may reduce uncertainty about whether a task is
> placed in inbox or timeline; and time of day may reduce uncertainty about what kind of task is
> created."
>
> "This makes Information Theory especially promising for the first implementation because many entropy
> measures can be calculated from task-created data alone. If lifecycle events are available, the same
> logic can be extended to uncertainty in movement, rescheduling, and completion trajectories."

Two of the paper's named dimensions (**alert use, energy level, task category**) are not implementable —
confirmed absent from the export in `structured_cas_modeling_plan.md` §2. Every other named dimension
is implemented below. Because lifecycle events (Updated/Deleted) *are* available here — the paper's own
"if lifecycle events are available" condition — the reschedule/completion extension is implemented too,
not deferred.

---

## Part 1 — Two different statistical objects, matched to how the paper frames each

The paper frames entropy as a **per-user phenotyping signature** ("routine planners... diverse
planners... context-coupled planners") and mutual information as **general dependency-structure
questions** ("task type may reduce uncertainty about completion" — a population-level claim, not phrased
as a per-user profile dimension). This notebook follows that distinction exactly:

- **Entropy measures → computed per participant** (feeds phenotyping, matches paper's phenotype framing)
- **Mutual information tests → computed pooled across the whole sample** (answers the paper's three
  named dependency questions as population-level findings; per-participant contingency tables for a
  12-category `update_method` or 24-hour bins would be far too sparse to be meaningful at N≈60-500 tasks/participant)

---

## Part 2 — Entropy measures (per participant)

| # | Paper dimension | Structured quantity | Unit | Data used | Threshold |
|---|---|---|---|---|---|
| 1 | Task type | `H_type_last` — entropy of `task_type_last` across all of a participant's tasks | task-level | all tasks | n_tasks ≥ 10 |
| 2 | Task type (creation-time, more literal reading of "task type" as an at-creation property) | `H_type_first` — entropy of `task_type_first`, non-censored tasks only | task-level | `has_creation_event=True` tasks only | n_noncensored ≥ 5 |
| 3 | Creation source | `H_creation_source` — entropy of `update_method` at each task's `Task Created` event | task-level | non-censored tasks only | n_noncensored ≥ 5 |
| 4 | Time of day | `H_hour_creation` — entropy of the hour-of-day (0–23) of each task's `Task Created` event | event-level (one per non-censored task) | non-censored tasks only | n_noncensored ≥ 5 |
| 5 | Recurrence patterns | `H_recurrence` — Bernoulli entropy of `recurrence_use_rate` (already computed in `structured_participant_features.csv`) | derived from a rate, not raw counts | all tasks | n_tasks ≥ 10 |
| 6 | Completion outcomes | `H_completion` — entropy of the 3-class `lifecycle_status` distribution (completed/deleted/unresolved) | task-level | all tasks | n_tasks ≥ 10 |
| 7 | "movement... trajectories" (paper's lifecycle-events extension) | `H_reschedule` — Bernoulli entropy of the share of tasks with ≥1 reschedule event (`n_reschedule_events > 0`) | derived from a rate | all tasks | n_tasks ≥ 10 |
| — | Alert use | **Not implemented — `task_alerts` absent from export** | — | — | — |
| — | Task category | **Not implemented — `category`/`topic` absent from export** | — | — | — |
| — | Energy level | **Not implemented — `task_energy_level` absent from export** | — | — | — |

**Threshold justification (not copied from DS5):** checked directly against this dataset's actual
per-participant task counts (median 123 tasks, median 60 non-censored tasks per participant): a
`n_tasks ≥ 10` threshold retains 53/61 participants (86.9%); a `n_noncensored ≥ 5` threshold retains
53/61 (86.9%) for creation-dependent measures. Both were chosen from the observed distribution, not
reused from DS5's `MIN_DAYS=7` (a time-window threshold that has no equivalent meaning here — Structured
entropy measures are volume-based, not window-based).

**Known imbalance to flag before running, not after:** from the NeT notebook's entry-state result,
`inbox` is the creation state for only 1.4% of non-censored tasks. `H_type_first` will therefore be low
for nearly all participants by construction (task_type is overwhelmingly `timed`) — this is a real
finding (Structured users plan almost exclusively with explicit times), not a threshold artifact, but
should not be over-read as "low entropy = highly routine planner" without checking the raw distribution
first.

---

## Part 3 — Mutual information tests (pooled, population-level)

Exactly the three dependency pairs the paper names, plus an explicit note on the one it names that
cannot be tested here:

| Paper's claim | X | Y | Computable? |
|---|---|---|---|
| "task type may reduce uncertainty about completion" | `task_type_last` (3-class) | `lifecycle_status` (3-class) | Yes |
| "creation source may reduce uncertainty about whether a task is placed in inbox or timeline" | `update_method` at creation (12-class) | entry placement — binary `inbox` vs `timeline` (`timed`+`all_day` collapsed, matching the paper's own binary "inbox or timeline" phrasing), non-censored tasks only | Yes, but see power caveat below |
| "time of day may reduce uncertainty about what kind of task is created" | creation hour, binned into `night(0-5)/morning(6-11)/afternoon(12-17)/evening(18-23)` (reuses the same quadrant convention as the shared `temporal_features` utility used by DS1/4/5/6) | `task_type_first` (3-class), non-censored tasks only | Yes |
| "energy level may reduce uncertainty about movement or delay" | `task_energy_level` | reschedule occurrence | **No — energy level not in export.** Reported as not-implementable, not silently skipped. |

**Power caveat, stated in advance:** the inbox-vs-timeline test has a severely imbalanced target
(1.4% inbox / 98.6% timeline) — MI is still well-defined and will be computed, but a near-zero or
near-degenerate result should be attributed to class imbalance, not necessarily to a genuine absence of
dependency. A supplementary 3-class version (`inbox`/`timed`/`all_day` un-collapsed) is also reported for
comparison, closer to the actual task_type variable used elsewhere in this project.

**Metric reported for each pair:** raw MI in bits, and MI normalized by `H(Y)` (the "uncertainty
reduction fraction," 0 = X tells you nothing about Y, 1 = X fully determines Y) — the normalized version
is more interpretable across pairs with different target cardinalities.

---

## Part 4 — What is deliberately deferred, and why

- **No `H_SDE`-style bridge to StoP.** DS5's InT notebook bridged to its own already-completed StoP
  model. Structured's StoP (notebook 63) does not exist yet. Fabricating a bridge to a non-existent
  model would misrepresent the analysis. When StoP is implemented, this notebook (or an addendum) should
  revisit whether a `sig_hat`-based entropy bridge is meaningful for Structured's task-volume time
  series — flagged forward, not built now.
- **No binned empirical entropy of a continuous override-rate series (`H_emp` in DS5).** There is no
  equivalent continuous per-day behavioral quantity for Structured at this stage (that would require
  StoP's daily aggregation first).
- **Second-order / conditional entropy chains beyond the three named MI pairs** (e.g. entropy of
  `update_method → task_type → completion` as a full chain) are not implemented — the paper names three
  specific pairs; going beyond them would be adding scope the paper doesn't ask for.

---

## Part 5 — NeT–InT bridge (legitimate now, because NeT already exists)

DS5 established a general, reusable identity for this kind of cross-model bridge: for a first-order
Markov chain over states with marginal state distribution p(s) and transition-conditional entropy
`H_trans` (already computed per participant in NeT, `outputs/model_outputs/structured/network_theory/participant_network_metrics.csv`):

```
H_state_marginal = -Σ_s q(s) log2(q(s))         # q(s) = TARGET-state (state_to) distribution --
                                                  # NOT the raw marginal over every observed per-event
                                                  # state label (see implementation note below)
I_consec_state = H_state_marginal - H_trans      # mutual information between consecutive states
```

**Implementation note (caught during build, 2026-08-03):** the first implementation attempt computed
`H_state_marginal` from the raw entropy of every observed per-event state label, which wrongly includes
the 15,301 single-event tasks that contribute a state label but zero transitions (they never appear in
NeT's `W` matrix at all). That marginal is not the one `H_trans` conditions against, and the chain-rule
inequality `H(Y) ≥ H(Y|X)` failed for several participants (min `I_consec_state = -0.676`, impossible).
Fixed by computing `H_state_marginal` from the `state_to` column of the exact same edge list used to
build NeT's transition matrix — the correct target-distribution marginal, which is mathematically
guaranteed to be ≥ `H_trans`. Verified: 0 violations across all 45 NeT-eligible participants after the
fix. Recorded here so this is not re-derived incorrectly in a future session.

`H_state_marginal ≥ H_trans` always (conditioning cannot increase entropy) — this is a property of the
mathematics, not a Structured-specific claim, and is checked as a sanity test, not treated as a novel
finding. `I_consec_state` measures how much knowing the current task state reduces uncertainty about the
next one — directly analogous to DS5's `I_consec = H_app − H_trans`, but built from data that already
exists in this project's own NeT output rather than fabricated ahead of schedule. This is implemented
here (not deferred) precisely because NeT is already complete, unlike the StoP bridge above.

---

## Part 6 — Output file structure

```
outputs/model_outputs/structured/information_theory/
  participant_entropy_metrics.csv       # one row per participant: H_type_first, H_type_last,
                                         # H_creation_source, H_hour_creation, H_recurrence,
                                         # H_completion, H_reschedule, H_state_marginal, H_trans (joined
                                         # from NeT), I_consec_state
  mutual_information_pooled.csv         # one row per tested pair: X, Y, MI_bits, H_Y_bits,
                                         # normalized_MI, n, notes
  figures/
    fig1_int_entropy_distributions.png
    fig2_int_mi_pooled_summary.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Theory paper §2.5 read in full and quoted directly above — every implemented quantity traces to it
- [x] Confirmed which paper-named dimensions are unavailable (alerts, energy level, category) — not
      silently dropped, explicitly listed
- [x] Thresholds derived from this dataset's actual task-count distribution, not copied from DS5
- [x] Entropy (per-participant, phenotyping) vs. MI (pooled, dependency-structure) split justified from
      how the paper itself frames each construct
- [x] NeT-InT bridge confirmed legitimate (NeT already complete); StoP bridge explicitly deferred, not built
- [x] Notebook 65 implemented and executed
