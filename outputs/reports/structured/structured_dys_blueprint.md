# Structured — Dynamical Systems (DyS) Blueprint

**Notebook:** `notebooks/62_structured_dynamical_systems.ipynb`
**Written:** 2026-08-03
**Position:** 62 in the Structured 60–68 decade. Depends on `structured_task_lifecycle_features.csv`
(Stage 1) directly; does **not** depend on StoP's fitted parameters (see Part 0 — this is a deliberate
departure from the DS5 dependency chain, justified below).
**Depends on:** `outputs/features/structured/structured_task_lifecycle_features.csv`,
`structured_behavioral_clean.csv`
**Output root:** `outputs/model_outputs/structured/dynamical_systems/`

---

## Part 0 — Design principle: why this cannot be a DS5 port, and why it doesn't consume StoP's output

DS5's DyS notebook (`42_ds5_dynamical_systems.ipynb`) took StoP's already-fitted 1D SDE (`mu_hat`,
`sig_hat` of a single bounded override-rate series `X_t`) and asked: in the σ→0 limit, does the
deterministic drift map predict a stable fixed point, and is each participant's behavior closer to
deterministic or stochastic? That is a **single-variable** dynamical-systems reduction of DS5's own
StoP model.

The theory paper's Structured DyS section (§2.2) describes something structurally different — not a
limit of a 1D SDE, but a genuinely **multi-dimensional state-space trajectory**:

> "A user-day could be represented by a vector of planning variables, such as the number of tasks
> created, the proportion of timed tasks, the proportion of inbox tasks, the proportion of completed
> tasks, and the degree of task complexity... different planning styles can be interpreted as
> attractor-like regions in state space. A high-structure attractor may describe users who repeatedly
> create timed tasks... A sparse-consistent attractor... An inbox attractor... A dropout attractor may
> describe users whose activity progressively declines until little or no planning activity remains."
>
> "Example A: ... a user over thirty days... **In the first week**, the user may occupy a high-structure
> region... **In the second week**, unresolved tasks may accumulate... **In the third week**, the user
> may return to structured planning or continue toward inactivity."

Two things follow directly from this text, both different from DS5's approach and from this project's
own StoP notebook for Structured:

1. **The state is a vector (≥4 dimensions), not a scalar.** Porting DS5's single-variable σ-threshold
   eligibility rule would misrepresent what the paper asks for.
2. **The paper's own worked example uses WEEKLY resolution** ("first week... second week... third
   week"), not daily. StoP (notebook 63) deliberately used *daily* resolution because its own paper
   section's worked example was daily ("the number of timed tasks created per user-day"). DyS uses
   *weekly* resolution because its own worked example is weekly. This is not an arbitrary choice — it is
   read directly off each section's own illustrative example, and is a genuine reason the two notebooks
   are not interchangeable and DyS does not need to import StoP's fitted daily parameters.

---

## Part 1 — The weekly state vector

Restricted to tasks with a visible `Task Created` event (`has_creation_event = True`) — see Part 2 for
why, and the resulting caveat.

For each participant, weeks are indexed **relative to that participant's own first observed creation
event** (local calendar day via `event_timezone`, matching the local-day convention established in the
StoP blueprint): `week_idx = (local_date − participant's first creation local_date).days // 7`. This
matches the paper's own narrative ("a user over thirty days... in the first week...") — a
participant-relative timeline, not an absolute calendar week.

For week `w`, over the tasks created that week:

| Dimension | Definition | Paper source |
|---|---|---|
| `n_created_w` | count of tasks created | "the number of tasks created" |
| `timed_share_w` | fraction with `task_type_first == "timed"` | "the proportion of timed tasks" |
| `inbox_share_w` | fraction with `task_type_first == "inbox"` | "the proportion of inbox tasks" |
| `completed_share_w` | fraction that were **ever** later marked completed (using the task's final `lifecycle_status`, not "completed within that same week") | "the proportion of completed tasks" |
| `complexity_w` | mean `subtasks_amount_last` of that week's created tasks | "the degree of task complexity" |

`all_day_share_w` is the algebraic complement (`1 − timed_share_w − inbox_share_w`) and is reported but
not treated as an independent dimension.

**`completed_share_w` explicitly measures eventual fate, not within-week completion** — a task created
in week 3 might not be marked completed until week 9. This is a deliberate reading of "proportion of
completed tasks" as a property of that week's creation cohort, not a same-week outcome; stated explicitly
because the alternative reading (completed within the same week) would silently penalize tasks that
simply haven't had time to be completed yet, especially for weeks near the end of the observation window.

---

## Part 2 — Left-censoring caveat (carried forward, again, from NeT/InT/feature-extraction)

Restricting to `has_creation_event = True` tasks means DyS's weekly state vector reflects only the
**39.3%** of tasks with a visible creation event — for participants with high
`pct_tasks_left_censored` (already computed in `structured_participant_features.csv`), the observed
trajectory is a thin, potentially unrepresentative slice of their true planning portfolio (most of what
they're doing week-to-week involves tasks that already existed before the window). **This is reported
per-participant, not silently absorbed** — `pct_tasks_left_censored` is carried into the output table so
any trajectory result can be checked against how much of that participant's real activity it could see.

---

## Part 3 — Eligibility (verified against this dataset, not copied from StoP or DS5)

```
MIN_WEEKS = 4     # need at least 4 distinct weeks with >=1 created task for a trajectory
```

Verified: 42/61 participants (68.9%) meet this. (For reference: 36/61 (59.0%) meet a stricter
`MIN_WEEKS=6`; `MIN_WEEKS=4` was chosen as the minimum that still supports a meaningful trend estimate
and matches the paper's own 3-week illustrative example without being overly permissive.)

---

## Part 4 — Trajectory metrics (Step 1 scope: descriptive, not clustering)

| Metric | Definition | Paper concept operationalized |
|---|---|---|
| `centroid_*` (5 values) | Mean of each state dimension across the participant's weeks | "where does this user mostly live in state space" |
| `state_space_volatility` | Mean Euclidean distance between consecutive **z-scored** (across the eligible-participant population) weekly vectors | "oscillate between regimes" |
| `volume_trend_slope` | OLS slope of `n_created_w` on `week_idx` | overall regime-level trend (distinct from StoP's *daily* `mu_hat` — weekly resolution, whole-vector context) |
| `dropout_score` | `mean(n_created_w)` in the final quartile of observed weeks minus the first quartile, divided by the participant's own overall mean (a relative, self-normalized decline measure) | "activity progressively declines until little or no planning activity remains" |

## Part 5 — Descriptive region labels (rule-based, Step 1 only — explicitly not a clustering result)

Priority order (documented as FLAG DyS-R1; a "mixed" fallback is kept deliberately rather than forcing
every participant into one of the paper's four illustrative categories):

```
1. dropout_score in the bottom tercile (strong relative decline)      -> "dropout-prone"
2. else state_space_volatility in the top tercile                     -> "oscillatory"
3. else n_created_w mean in bottom tercile AND volatility bottom tercile -> "sparse-consistent"
4. else timed_share centroid top tercile AND completed_share centroid top tercile -> "high-structure"
5. else inbox_share centroid top tercile                              -> "inbox-heavy"
6. else                                                                -> "mixed"
```

---

## Part 6 — Observational subscription-group comparison

Same non-causal caveat as NeT/StoP: `subscription_type_last` reported descriptively against
`state_space_volatility` and `volume_trend_slope`, explicitly not a causal claim.

---

## Part 7 — Output file structure

```
outputs/model_outputs/structured/dynamical_systems/
  weekly_state_vectors_long.csv        # long format: participant_id, week_idx, n_created_w,
                                        # timed_share_w, inbox_share_w, all_day_share_w,
                                        # completed_share_w, complexity_w
  participant_trajectory_metrics.csv   # one row per participant: centroids, state_space_volatility,
                                        # volume_trend_slope, dropout_score, region_label,
                                        # pct_tasks_left_censored (carried from Stage 1), n_weeks,
                                        # is_dys_eligible, subscription_type_last
  subscription_group_summary.csv
  figures/
    fig1_dys_state_space_pca.png        # 2D projection of weekly trajectories (PCA), colored by participant
    fig2_dys_region_label_distribution.png
    fig3_dys_volatility_vs_dropout.png
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Theory paper §2.2 read in full and quoted directly above
- [x] Confirmed DS5's 1D σ-threshold DyS design does not apply; paper's own text specifies a
      multi-dimensional weekly vector instead
- [x] Weekly (not daily) resolution justified from the paper's own worked example, distinguishing DyS
      from StoP's daily resolution rather than treating them as interchangeable
- [x] MIN_WEEKS=4 threshold verified against this dataset's real weekly-activity distribution (42/61 eligible)
- [x] Left-censoring caveat carried forward explicitly (creation-event-only state vector)
- [x] Region labels explicitly flagged as Step 1 descriptive/rule-based, not Step 2 clustering
- [x] Notebook 62 implemented and executed
