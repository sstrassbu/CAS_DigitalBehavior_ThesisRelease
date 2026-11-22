# Structured — Agent-Based Modeling (ABM) Blueprint

**Notebook:** `notebooks/67_structured_agent_based.ipynb`
**Written:** 2026-08-05
**Position:** 67 in the Structured 60–68 decade — the final deferred model family, unblocked now that
Step 2 phenotyping exists (`outputs/model_outputs/structured/phenotyping/`), matching this project's own
established rule (DS5: "ABM deferred until phenotyping").
**Depends on:** `structured_participant_features.csv`, `participant_stop_parameters.csv` (StoP),
`cluster_assignments.csv` + `cluster_profiles.csv` (Step 2 phenotyping)
**Output root:** `outputs/model_outputs/structured/agent_based/`

---

## Part 0 — Paper grounding (§2.7, quoted) and why this is not redundant with StoP or Step 2

> "Agent-Based Modeling is especially suitable for Structured because the dataset is expected to contain
> heterogeneous users who may use the same planning tool in very different ways... These rules do not
> need to be psychologically complex at first. They can be simple probabilities estimated from data...
> **The value of ABM is that it can test whether simple local rules are sufficient to reproduce larger
> observed patterns.**"
>
> "ABM can also be used after other models have extracted empirical features. Information Theory may
> identify low-entropy versus high-entropy planners; Stochastic Processes may identify bursty or
> drift-dominated planners; Network Theory may identify inbox-centered or rescheduling-loop users. These
> features can then inform the rules or types used in an agent-based simulation."
>
> "ABM is not only a descriptive tool, but a way to examine whether proposed planning phenotypes are
> **dynamically plausible**."

**Not redundant with StoP:** StoP *estimated* drift/diffusion/Fano from the real observed daily series
(a descriptive/inferential exercise). ABM *generates* synthetic series from simple, explicit mechanisms
and asks whether those mechanisms can *reproduce* what StoP found — a generative/explanatory exercise,
answering a different question ("is simple heterogeneity sufficient to explain this?" vs. "what does the
real data look like?").

**Not redundant with Step 2 phenotyping:** clustering *described* two profiles from observed data. ABM
*tests* whether a simple two-type agent population, built from each profile's own empirical rule
parameters, can regenerate the aggregate patterns seen in the full sample — the paper's own "dynamically
plausible" validation, which clustering alone cannot answer.

---

## Part 1 — Agent rules, extracted from already-fitted quantities (not re-estimated from raw data)

Per the paper's own instruction to let prior models inform ABM's rules, every rule parameter below is
read directly from existing Step 1/Step 2 outputs — no new estimation from `structured_behavioral_clean.csv`:

| Rule | Source | Column |
|---|---|---|
| Mean daily creation rate `λ` | StoP | `created_mean_N` |
| Active-day fraction `f_active` | StoP | `created_n_active_days / created_span_days` |
| Observation length `T` | StoP | `created_span_days` |
| Task-type shares (`p_timed`, `p_inbox`, `p_all_day`) | Stage 1 features | `share_task_type_*` |
| Completion probability | Stage 1 features | `pct_tasks_completed` |
| Reschedule probability | Stage 1 features | `reschedule_rate` |
| Target for validation: real burstiness | StoP | `created_Fano_factor` |
| Target for validation: phenotype membership | Step 2 | `cluster_label` (Profile A/B) |

**Population:** StoP `created_is_eligible` participants, **N=43** (verified) — the same population StoP
itself validated Fano factors on, so the simulation-vs-real comparison in Part 3 is apples-to-apples.
36/43 also have a Step 2 `cluster_label` (full overlap with the phenotyping population — verified, no
additional eligibility loss for Part 4).

---

## Part 2 — Model 1: static-rate agents (the naive-heterogeneity baseline)

Each agent `i` simulates `T_i = created_span_days_i` days; each day, task count `N_t ~ Poisson(λ_i)`
independently (memoryless — no session structure, no temporal clustering). Agents differ from each other
(heterogeneous `λ_i` across the population) but each agent's own day-to-day behavior is homogeneous.

**Expected result, stated in advance (not discovered after running):** a Poisson process has
`Var = Mean` by construction, so `Fano_sim,1 ≈ 1` for every agent regardless of `λ_i`. This is
mathematically guaranteed, not an empirical finding — the simulation is run anyway (not skipped) because
it turns the abstract fact into a **concrete, quantified comparison** against the real distribution
(`created_Fano_factor`, mean≈6.0, verified in notebook 63), showing exactly how large the gap is between
"agents that only differ from each other" and the real population's actual burstiness.

---

## Part 3 — Model 2: two-state (session on/off) bursty agents

Adds the **minimum additional mechanism** needed to test whether within-agent temporal clustering (not
just between-agent heterogeneity) is what generates real-world burstiness — directly operationalizing
the paper's "test whether simple local rules are sufficient."

```
State S_t in {ON, OFF} (Markov chain)
P(OFF -> ON) = p_on
P(ON -> OFF) = p_off = 1 / mean_session_length   (mean_session_length = 3 days, a stated simplifying
                                                    assumption -- NOT fit per-agent, keeping the rule
                                                    "simple" per the paper's own framing; flagged as a
                                                    candidate for a future sensitivity check, not pursued
                                                    here)
Steady-state P(ON) = f_active_i  =>  p_on = p_off * f_active_i / (1 - f_active_i)
                                      (f_active_i clipped to [0.05, 0.95] for numerical stability --
                                       verified against real data: min observed f_active = 0.035, max =
                                       0.993, so only the extremes are affected by clipping)
While ON: N_t ~ Poisson(lambda_ON_i), where lambda_ON_i = lambda_i / f_active_i
          (so the long-run mean rate still matches the agent's real created_mean_N)
While OFF: N_t ~ Poisson(0.05)  (near-zero, not exactly zero -- avoids a degenerate all-or-nothing series)
```

**Expected result, stated in advance:** `Fano_sim,2` should be substantially `>1` and much closer to
`created_Fano_factor` than Model 1 — testing whether this single, simple addition (session clustering,
still just two rules: enter-session and exit-session probabilities) closes most of the gap, or whether
real burstiness requires something even the session mechanism can't capture (a legitimate possible
outcome, not a foregone conclusion — the point of running both models is to find out, not to confirm a
predetermined story).

---

## Part 4 — Phenotype mixture validation (paper's Example A/B, directly)

Using Step 2's `cluster_profiles.csv` (Profile A mean rules, Profile B mean rules) and real mixture
proportion (22/36 Profile A, 14/36 Profile B — verified), simulate a population of Model-2 agents split
into exactly two **types** (not 36 individually-calibrated agents, but 2 archetypal rule sets, matching
the paper's own Example A: *"One agent type creates many timed tasks... Another creates few tasks but
does so consistently..."*). Compare the simulated population's Fano-factor distribution (by type) against
the real Profile A vs. Profile B Fano distributions — this is the paper's own "dynamically plausible"
test: do two simple archetypal rule-sets reproduce the separation Step 2 found empirically, or does the
real separation require more than these two profiles' mean rates can generate?

**Actual result, added after running (2026-08-05):** the separation's *magnitude* is well reproduced
(KS statistic 0.351 real vs. 0.375 simulated — the right comparison, since p-values aren't comparable
across the very different real (n=22/14) vs. simulated (n=200/200) sample sizes) — but the *direction*
is reversed: real ordering is Profile A > Profile B (mean Fano 7.49 vs. 4.61), simulated ordering is
Profile B > Profile A (5.04 vs. 4.60). Collapsing each profile to a single mean `(λ, f_active)` pair
loses enough within-profile heterogeneity to get the direction wrong even while getting the separation
size right. This was caught by explicitly checking direction, not just accepting the magnitude match —
a genuine, reported limitation of the 2-archetype simplification, not a data or code error.

---

## Part 5 — Output file structure

```
outputs/model_outputs/structured/agent_based/
  agent_rule_parameters.csv          # participant_id, all extracted rule params, real Fano, cluster_label
  simulation_results_model1.csv      # participant_id, Fano_sim_model1
  simulation_results_model2.csv      # participant_id, Fano_sim_model2
  phenotype_mixture_validation.csv   # Profile A/B: real vs. simulated Fano summary stats
  figures/
    fig1_abm_fano_model_comparison.png     # real vs Model 1 vs Model 2 Fano distributions
    fig2_abm_example_trajectories.png      # a few example simulated daily series (both models)
    fig3_abm_phenotype_mixture.png         # Part 4 result
  model_run_summary.md
```

---

## Implementation readiness checklist

- [x] Theory paper §2.7 read in full and quoted directly above
- [x] Explicit non-redundancy check against StoP (estimation vs. generation) and Step 2 (description vs.
      dynamic-plausibility test) completed before writing any code
- [x] All agent rules sourced from already-fitted Step 1/Step 2 quantities, not re-estimated from raw
      behavioral data — matches the paper's own instruction
- [x] Population (N=43) and phenotype overlap (36/43) verified against real data before finalizing
- [x] Both models' expected results stated in advance (Model 1 ≈1 by mathematical necessity; Model 2
      expected closer but not guaranteed to fully close the gap) — falsifiable, not fit-after-the-fact
- [x] Model 2's one simplifying assumption (fixed 3-day mean session length) explicitly flagged as a
      simplification, not silently hidden
- [x] Notebook 67 implemented and executed
