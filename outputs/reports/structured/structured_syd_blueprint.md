# Structured — System Dynamics (SyD) Blueprint

**Notebook:** `notebooks/68_structured_system_dynamics.ipynb`
**Written:** 2026-08-03
**Position:** 68 in the Structured 60–68 decade. No hard data dependency on NeT/InT/StoP/DyS (built
directly from `structured_task_lifecycle_features.csv` and `structured_behavioral_clean.csv`), but Part
0.5 below explicitly checks this doesn't just re-describe what those four notebooks already computed.
**Depends on:** `outputs/features/structured/structured_task_lifecycle_features.csv`,
`structured_behavioral_clean.csv`
**Output root:** `outputs/model_outputs/structured/system_dynamics/`

---

## Part 0 — Paper grounding (§2.8, quoted in full)

> "System Dynamics models system-wide behavior through stocks, flows, and reinforcing or balancing
> feedback loops... Stocks may include planned tasks, inbox tasks, unresolved tasks, recurring tasks,
> and completed tasks; flows may include creation, scheduling, completion, rescheduling, and
> abandonment... A productive reinforcing loop may run from task creation to clearer structure, from
> clearer structure to completion, and from completion to continued app use. An overload loop may run
> from excessive task creation to unresolved tasks, from unresolved tasks to rescheduling, and from
> repeated rescheduling to disengagement. A balancing loop may occur when users respond to overload by
> simplifying tasks, reducing task volume, or moving tasks to more realistic time slots."
>
> "Example A: ...model the stock of unresolved tasks. Task creation increases this stock, while
> completion decreases it... If unresolved tasks grow too large, the user may either reduce future task
> creation, reschedule tasks, or disengage from the app."

---

## Part 0.5 — Non-redundancy check against NeT / StoP / DyS (required before building this)

Before writing any code, checked explicitly whether SyD would just relabel outputs the first four
Structured model notebooks already produced:

| Already computed | Notebook | Covers SyD's... | Does NOT cover |
|---|---|---|---|
| Pooled state-transition counts (`timed→moved→completed`, etc.) | NeT (64) | **flows** between states, as edge counts | any notion of a **standing stock accumulating over time** — NeT's edges are event-to-event, not a running total |
| Daily creation/completion count + drift/diffusion/Fano | StoP (63) | **flow rates** over time for two series in isolation | any **relationship between the two series** (does completion flow depend on how much is currently backlogged?) |
| Weekly multi-dim state vector + trajectory region label | DyS (62) | **composition** of what's created each week, and whether *overall activity* trends down | the **backlog itself** — DyS never counts how many tasks are *currently sitting open*; `dropout_score` observes activity decline but does not test whether it followed backlog growth |

**Conclusion: SyD is not redundant.** Its genuinely new contribution is (1) a **stock** — the running
count of currently-open tasks over time, which none of the other three notebooks compute — and (2)
explicit **lagged feedback-loop tests**: does backlog level in week `w` predict a *change* in creation
or completion behavior in week `w+1`? This is a directional, temporal-dependency question NeT (static
transition counts), StoP (single-series drift/diffusion), and DyS (composition + trend, not backlog
level) do not ask.

---

## Part 1 — The stock: `Backlog_w`

For each **non-censored** task (`has_creation_event = True` — same restriction as DyS, for the same
reason: entry time is only known for these), define:

- `entry_week` = participant-relative week of the `Task Created` event (same local-day, relative-week
  convention as DyS notebook 62)
- `exit_week` = participant-relative week of the task's **final** completion-marking event (if its
  `lifecycle_status == "completed"`) or `Task Deleted` event (if `"deleted"`); `None` if
  `lifecycle_status == "unresolved"` (task is still open at the end of the observation window —
  right-censored, handled naturally by a stock model, not a problem)

```
Backlog_w = count of non-censored tasks where entry_week <= w AND (exit_week > w OR exit_week is None)
```

**Verified feasible before writing this into code:** 7,696/10,516 non-censored tasks (73.2%) have a
determinable exit week; the remaining 2,854 (`unresolved`) simply stay in the stock through the last
observed week, which is the mathematically correct treatment for a right-censored open task, not a gap.

**Left-censoring caveat (same pattern as DyS, stated once more because it matters differently here):**
`Backlog_w` is initialized at 0 for each participant's own week 0, but in reality most participants
already had open tasks before the window started (60.7% of all tasks are left-censored). This means
**`Backlog_w` is very likely an undercount of the participant's true backlog**, especially in early
weeks — it measures the backlog *visible within this window*, not the participant's total real backlog.
Reported explicitly, not corrected (no data exists to correct it with).

---

## Part 2 — Feedback-loop tests (pooled across the sample — population-level questions, same design
split established in the InT blueprint: stock/trend = per participant, "does this loop exist at all in
the data" = pooled)

Three tests, directly operationalizing the paper's three named loops:

| Loop (paper's language) | Operationalization | Predicted sign if the loop is real |
|---|---|---|
| **Productive loop**: "completion... to continued app use" | Pearson r pooled across participant-weeks: `completed_count_w` vs. `created_count_{w+1}` | positive — completing tasks this week predicts *more* creation next week |
| **Overload loop**: "unresolved tasks... to repeated rescheduling... to disengagement" | Pearson r: `Backlog_w` vs. `created_count_{w+1}` | negative — high backlog this week predicts *less* creation next week (disengagement) |
| **Balancing loop**: "users respond to overload by simplifying... or moving tasks to more realistic time slots" | Pearson r: `Backlog_w` vs. `reschedule_count_w` (same week, not lagged — a within-week adaptive response) | positive — high backlog co-occurs with more rescheduling activity |

All three reported with `r`, `p`, `n`, and explicitly labeled exploratory/correlational — **no causal
claim**, consistent with every other Structured model notebook's treatment of non-experimental data.

**Addendum, added during implementation (2026-08-03):** the pooled Pearson correlations above conflate
two different sources of covariation — genuine within-person week-to-week timing, and a between-
participant confound (some participants are simply high-volume users in every week, so any two "high
this week" quantities correlate strongly across the pooled sample regardless of any real lagged
relationship). The pooled `productive` loop result (`r=0.9456`) was implausibly strong for a real
week-to-week effect and triggered this check. **Fix: person-mean-center each series before correlating**
(subtract each participant's own mean from their own values — the standard fixed-effects/panel technique
for exactly this confound), reported as `pearson_r_within` alongside the naive `pearson_r`. See actual
results in the model run summary — the within-person correlations are much smaller than the pooled ones,
and the overload loop's sign only matches the paper's own prediction *after* this correction (the pooled
version has the wrong sign). This is the primary result to report; the pooled numbers are kept for
transparency but should not be cited as the headline finding.

---

## Part 3 — Per-participant summary (Step 1 descriptive scope)

- `backlog_mean`, `backlog_peak`, `backlog_trend_slope` (OLS slope of `Backlog_w` over `w`)
- `dominant_loop_label` (rule-based, only for participants meeting the same `MIN_WEEKS=4` eligibility
  DyS used — reusing that threshold here is justified because it is the *same* weekly-resolution object,
  not copied blindly):
  ```
  if backlog_trend_slope in top tercile (backlog clearly growing):        "overload-trending"
  elif backlog_trend_slope in bottom tercile (backlog clearly shrinking): "productive-trending"
  else:                                                                    "balanced"
  ```

---

## Part 4 — Output file structure

```
outputs/model_outputs/structured/system_dynamics/
  backlog_stock_long.csv              # participant_id, week_idx, Backlog_w, created_count_w,
                                       # completed_count_w, deleted_count_w, reschedule_count_w
  participant_syd_summary.csv         # backlog_mean/peak/trend_slope, dominant_loop_label,
                                       # is_syd_eligible, pct_tasks_left_censored (carried forward)
  feedback_loop_tests.csv             # loop_name, X, Y, pearson_r, p_value, n
  figures/
    fig1_syd_backlog_trajectories.png
    fig2_syd_feedback_loop_scatter.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Theory paper §2.8 read in full and quoted directly above
- [x] Explicit non-redundancy check against NeT/StoP/DyS completed (Part 0.5) — confirmed genuinely new
- [x] Backlog computation verified feasible against real data (73.2% of non-censored tasks have a
      determinable resolution week) before writing the design into this document
- [x] Left-censoring undercount caveat stated explicitly, not silently absorbed
- [x] Feedback-loop tests map 1:1 onto the paper's three named loops, each with a predicted sign stated
      in advance (falsifiable, not fit-after-the-fact)
- [x] Notebook 68 implemented and executed
