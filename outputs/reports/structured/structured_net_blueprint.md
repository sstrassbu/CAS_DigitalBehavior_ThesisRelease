# Structured — Network Theory (NeT) Blueprint

**Notebook:** `notebooks/64_structured_network_theory.ipynb`
**Written:** 2026-08-03
**Numbering convention (new, established here):** Structured model notebooks use the decade **60–68**,
mirroring DS5's family-code offsets within 41–48 (StM/DyS/StoP/NeT/InT/GaT/ABM/SyD = positions 1–8)
shifted by +20: **61 StM · 62 DyS · 63 StoP · 64 NeT · 65 InT · 66 GaT · 67 ABM · 68 SyD.** This keeps
the same family→number mapping across datasets without colliding with DS1(20)/DS4(30)/DS5(41–48)/DS6(50)
ranges. Recorded here and in memory so future sessions don't have to re-derive it.
**Depends on:** `outputs/features/structured/structured_task_lifecycle_features.csv`,
`structured_behavioral_clean.csv` (notebook 16/17 outputs)
**Output root:** `outputs/model_outputs/structured/network_theory/` (dataset-scoped, unlike DS5's
un-prefixed `outputs/model_outputs/network_models/` — necessary now that more than one dataset
populates `model_outputs/`)

---

## Part 0 — Why NeT first for Structured

Per `structured_cas_modeling_plan.md` §5–6: NeT is the strongest candidate model family for this
dataset because the full three-class event lifecycle (Created/Updated/Deleted, with detailed
`update_type` change tags) is available — the paper's own "full value" scenario, not its weaker
creation-only baseline. It has no dependency on any other model family, unlike StM (needs StoP/DyS
first) or ABM (needs a phenotyping pass first).

**Correction carried in from feature extraction (2026-08-03):** 60.7% of tasks are left-censored (no
visible `Task Created` event). This does not block NeT — state-to-state transitions remain valid
for all tasks — but it does mean the "entry state" for most task sequences is "first observed state,"
not "true creation state." This must be flagged in every place entry-state statistics are reported.

---

## Part 1 — Theory-to-data translation

The theory paper's Table 1 (NeT row) states: *"Build task-state transition networks, e.g., created →
inbox, inbox → timed, timed → moved, moved → completed, or timed → unresolved. Identify central states
and loops."* §2.4 elaborates: nodes = task states (inbox, timed, all-day, moved, recurring, completed,
unresolved); edges = movement between states; phenotypes = inbox-hub, timeline-centered,
rescheduling-loop, or completion-path users.

| Theoretical quantity | Structured variable / engineered quantity | Mapping type | Confidence |
|---|---|---|---|
| Node (task state) | One of a 7-state vocabulary derived from `event_type` + `update_type_list_str` + `task_type` (defined in Part 2) | Derived | High — deterministic rule, documented below |
| Directed edge (state_i → state_j) | Consecutive state labels within one task's chronologically ordered events | Derived | Medium-High — same "temporal succession ≠ causal interaction" caveat as DS5 NeT applies here |
| Edge weight | Count of state_i → state_j transitions, pooled across all of a participant's tasks | Derived | High |
| Hub-dependence | HHI_net = Σ(s_i^out/M)² (same formula as DS5 NeT) | Derived | High |
| Self-loop share | ρ_self = Σ W_ii / M — here means "task stayed in the same state across consecutive events" (e.g. repeated cosmetic edits without a structural change) | Derived | High |
| Transition entropy | H_trans (same formula as DS5 NeT) | Derived | Medium — small state vocabulary (7) means H_trans is naturally bounded low (max ≈ log2(7) ≈ 2.8 bits) |
| Stationary distribution | π (same eligibility rule as DS5: M≥50, ergodic T) | Derived | Low-Medium — same caveat as DS5: descriptive summary only, not a long-run equilibrium claim |
| "Rewiring by friction" (paper's DS5 framing) | **Not applicable** — Structured has no experimental condition. Nearest analog: `subscription_type_last` (free/pro) as an observational (non-causal) comparison group | Proxy | Low — purely observational, no randomization |

---

## Part 2 — State vocabulary and edge-engineering specification

This is the most important pre-implementation decision, mirroring DS5 NeT blueprint Part 3.

### 2.1 The 7-state vocabulary

`{inbox, timed, all_day, moved, completed, reopened, deleted}`

Chosen to match the theory paper's own example sequence exactly (`created→inbox→timed→moved→
completed`), while keeping the graph small enough to be interpretable at N=61 participants.
`inbox`/`timed`/`all_day` double as both the "entry" state (from Task Created) and the task's
structural category at any later point — a task's node label is its *current* type unless a more
specific event (reschedule, completion, reopen, deletion) applies.

### 2.2 Per-event state mapping (priority order — first match wins)

```
1. event_type == "Task Deleted"                          -> "deleted"      (terminal)
2. "task_completed"   in update_type tags                -> "completed"
3. "task_uncompleted"  in update_type tags                -> "reopened"
4. {"date_changed","start_time_changed"} ∩ tags != {}     -> "moved"
5. otherwise (Task Created, or Task Updated with          -> task_type at this event
   type_changed / recurrence_changed / notes_changed /       (inbox / timed / all_day)
   subtasks_changed / duration_changed / title_changed /
   color_changed / icon_changed / energy_level_changed /
   or an empty update_type list)
```

**FLAG NET-S1 (state priority order):** completion/reopening/deletion always dominate a reschedule or
cosmetic edit in the same event, because only one `update_type` combination is ever observed to include
`task_completed` alongside other tags in this data (verified: `task_completed` appears only as a
single-tag update in the raw `update_type` value counts) — so this priority order rarely has to
adjudicate a genuine conflict. Documented explicitly so the rule is auditable, not because ties are
common.

**FLAG NET-S2 (cosmetic edits collapse to current type):** An update event that only changes color,
icon, notes, subtasks, duration, title, or recurrence — with no reschedule/completion/type change —
maps to the task's current `inbox`/`timed`/`all_day` state, i.e. it produces a **self-loop**, not a new
node. This is a deliberate choice: it means `ρ_self` (self-transition share) captures "how much a task
gets fiddled with while structurally unchanged," directly comparable in spirit to DS5's `rho_self`
("same-app repetition").

### 2.3 What counts as an edge

For each `task_id`, sort its events by `event_timestamp_utc` and map each event to a state label
(§2.2). Each consecutive pair of state labels (state[t] → state[t+1]) is one transition observation.
Single-event tasks contribute a node visit but zero edges.

**FLAG NET-S3 (self-loops included):** Same as DS5 FLAG S1 — self-loops are kept, not filtered, because
they carry real signal (repeated fiddling on a stable task).

### 2.4 What counts as an edge — granularity

**FLAG NET-G1 (task-then-participant pooling):** Edges are built per-task (a task's own chronological
event sequence), then **pooled across all of a participant's tasks** into one participant-level
transition graph. This differs from DS5, where edges were built directly at the participant level
(single continuous event stream, no task-like sub-unit). Structured's natural sub-unit is the task, so
pooling task-level sequences up to the participant level is the correct analog — it avoids treating two
unrelated tasks' consecutive events (e.g. task A's last event followed immediately in wall-clock time by
task B's first event) as a spurious transition, which a naive whole-participant-timeline approach would
introduce.

### 2.5 Left-censoring caveat (carried from feature extraction)

For left-censored tasks (`has_creation_event == False`, 60.7% of tasks), the first state in the
sequence is whatever state the task was first *observed* in, not its true original state. The edge
FROM that first state is not fabricated (it's a real observed transition to the second state), but the
implied "entry point" distribution (how tasks are born: inbox vs. timed vs. all_day) is only reliable
for the 39.3% non-censored subset. **Report entry-state distribution separately for censored vs.
non-censored tasks; do not pool them for that specific statistic.**

### 2.6 Minimum transition threshold

**FLAG NET-T1 (mirrors DS5 FLAG NET1):** MIN_TRANSITIONS = 20 pooled transitions per participant to
compute network metrics; MIN_TRANSITIONS = 50 and ergodic T for stationary distribution π. Given
participant event counts range 4–11,293 (median 214, from the inspection notebook), expect a much
higher eligible fraction than DS5's ~60-70% — most Structured participants have far more events than
DS5's short friction-intervention windows.

---

## Part 3 — Per-participant metrics (identical formulas to DS5 NeT for cross-project consistency)

| Metric | Symbol | Formula | Notes |
|---|---|---|---|
| Number of nodes visited | n_nodes | count of distinct states visited | ≤ 7 by construction |
| Number of unique edges | n_edges | count of distinct (state_i, state_j) pairs observed | ≤ 49 |
| Total transitions | M | Σ edge counts | pooled across all of participant's tasks |
| Eligibility | is_net_eligible | M ≥ 20 | |
| Network Herfindahl | HHI_net | Σ_i (s_i^out/M)² | hub-dependence of state flow |
| Top-1 / top-3 state share | top1_share_net / top3_share_net | | |
| Self-transition share | rho_self | Σ_i W_ii / M | "fiddling without structural change" rate |
| Transition entropy | H_trans | −Σ_i (s_i^out/M) Σ_j T_ij log2(T_ij) | bounded by log2(7)≈2.81 bits |
| Stationary distribution eligibility | is_stationary_eligible | M ≥ 50, ergodic T | |
| Stationary entropy | H_pi | −Σ π_i log2(π_i) | NaN if not eligible |
| Completion-reachability | reaches_completed | "completed" ∈ visited states | direct, not derived |
| Deletion-reachability | reaches_deleted | "deleted" ∈ visited states | direct, not derived |

---

## Part 4 — Weakness flags (explicit, mirrors DS5 NeT Part 6)

- **FLAG W1 — Left-censoring bias on entry-state statistics.** See §2.5. Do not claim "X% of tasks are
  born in the inbox" using the full task set; use the 39.3% non-censored subset only for that claim.
- **FLAG W2 — Temporal adjacency ≠ causal interaction.** Same language requirement as DS5: "Edges
  represent temporal succession in the observed event log, not a causal claim about why a task moved
  between states."
- **FLAG W3 — Markov assumption unverified.** T assumes the next state depends only on the current
  state. Not tested against a higher-order alternative in Step 1.
- **FLAG W4 — Small state vocabulary bounds all entropy/HHI comparisons.** With only 7 possible states
  (vs. DS5's 5-50+ apps per participant), H_trans and HHI_net have a much narrower possible range here.
  Do not directly compare Structured NeT entropy values to DS5 NeT entropy values — different state
  spaces, not comparable magnitudes (consistent with this project's "no forced cross-dataset
  harmonization" principle).
- **FLAG W5 — No experimental condition.** Unlike DS5, there is no randomized friction condition to
  compare networks against. `subscription_type_last` (free/pro) is the only available grouping variable,
  and it is purely observational — any free-vs-pro network difference could reflect selection
  (who upgrades) rather than any causal effect of the subscription tier itself.
- **FLAG W6 — Stationary distribution is descriptive only**, exactly as documented for DS5 (short
  observation windows relative to a true long-run equilibrium claim — though Structured windows are
  typically longer than DS5's, so this flag is weaker here than in DS5).

---

## Part 5 — Output file structure

```
outputs/model_outputs/structured/network_theory/
  participant_network_metrics.csv       # one row per participant (61)
  transition_edge_list.csv              # long format: participant_id, state_from, state_to, count, weight
  entry_state_distribution.csv          # non-censored tasks only, per Part 2.5
  subscription_group_summary.csv        # free vs pro mean network metrics (FLAG W5 caveats apply)
  figures/
    fig1_net_hhi_h_trans_distribution.png
    fig2_net_pooled_state_graph.png
    fig3_net_subscription_group_comparison.png
  model_run_summary.md
```

### participant_network_metrics.csv — column specification

`participant_id, n_unique_tasks, n_nodes, n_edges, M_transitions, is_net_eligible, HHI_net,
top1_share_net, top3_share_net, rho_self, H_trans, is_stationary_eligible, H_pi, reaches_completed,
reaches_deleted, subscription_type_last`

---

## Part 6 — Notebook structure plan

1. Header + scope statement (goal: build participant-level task-state transition networks; not-goal:
   causal inference, community detection, higher-order Markov)
2. FLAG decisions table (reproduce Part 2/3 flags)
3. Proxy warning cell (reproduce Part 4 flags)
4. Load `structured_task_lifecycle_features.csv` + `structured_behavioral_clean.csv`
5. State-mapping function + per-task edge list construction (Part 2.2–2.4)
6. Left-censoring entry-state check (Part 2.5) — separate report for censored vs non-censored
7. Pool to participant-level transition matrices; apply MIN_TRANSITIONS threshold
8. Compute per-participant metrics (Part 3); sanity checks (T rows sum to 1, HHI in [0,1])
9. Stationary distribution (where eligible)
10. Pooled-network visualization (all participants combined, weighted by total flow)
11. Subscription-group (free/pro) descriptive comparison — explicitly labeled observational, not causal
12. Save outputs + `model_run_summary.md`

---

## Implementation readiness checklist

- [x] `structured_cas_modeling_plan.md` reviewed — NeT confirmed as first model
- [x] Feature extraction outputs available (`structured_task_lifecycle_features.csv`)
- [x] Left-censoring finding accounted for in design (§2.5, FLAG W1)
- [x] State vocabulary and edge rules fully specified before any code (this document)
- [x] Notebook 64 implemented and executed
