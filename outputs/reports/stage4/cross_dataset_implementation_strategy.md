# Cross-Dataset Implementation Strategy — Stage 4

**Written:** 2026-04-17  
**Purpose:** Persistent planning document recording the agreed cross-dataset sequencing
strategy for Stage 4 Step 1 and beyond. Read this before starting any new dataset or
model family to confirm you are working in the correct order.

**⚠ Status note (added 2026-08-07):** This document's "current phase" framing (DS5 Step 1)
describes state as of 2026-04-17. DS5 Step 1+2 and a full `_v2` revision arc (including
GaT/ABM, corrected below) are now complete; DS4 has all 8 CAS families implemented; DS6 Step
1 (7 families) and Step 2 are complete; Structured and Stanford Health dataset categories have
also been added since this was written. The dependency-chain reasoning and DS4 notebook
numbering below (51–55) were verified still accurate as of this audit (2026-08-07) — DS4's
real notebooks are 51 StM / 52 InT / 53 StoP / 54 NeT / 55 DyS / 56 GaT / 57 ABM / 59
phenotyping, matching this document's dependency logic. See `CLAUDE.md` for current status.

---

## Agreed strategy in one sentence

Complete all selected model families on DS5 first. Then do Step 2 (phenotyping) and
early Step 3 (personalization exploration) on DS5. Only then move to DS4 for validation,
deeper longitudinal analysis, and extension of DS5 findings.

---

## Phase 1 — Complete DS5 model family implementation (current phase)

### What this means

Implement all feasible CAS model families on DS5 before touching any other dataset.

The planned DS5 Step 1 notebooks are:

| Notebook | Model | Status |
|---|---|---|
| 41_ds5_statistical_mechanics.ipynb | StM | **COMPLETE** |
| 42_ds5_dynamical_systems.ipynb | DyS | **COMPLETE** |
| 43_ds5_stochastic_processes.ipynb | StoP | **COMPLETE** |
| 44_ds5_network_models.ipynb | NeT | **COMPLETE** |
| 45_ds5_information_theory.ipynb | InT | **COMPLETE** |
| 46_ds5_game_theory.ipynb | GaT | **COMPLETE (2026-08-06, DS5_02 Phase C)** |
| 47_ds5_agent_based.ipynb | ABM | **COMPLETE (2026-08-06, DS5_02 Phase C)** |
| 48_ds5_system_dynamics.ipynb | SyD | Deferred to DS6 — requires repeated survey waves (DS6's own SyD, notebook 78, is now complete) |

**Historical note (as of the original 2026-04-17 writing): DS5 Step 2 — Phenotyping
(`100_phenotype_exploration.ipynb`) was the next step. All active DS5 Step 1 notebooks were
complete; GaT/ABM/SyD were formally deferred. GaT and ABM were subsequently completed
2026-08-06 as part of the DS5_02 revision branch's Phase C — see `CLAUDE.md` for current
status; SyD remains deferred for DS5 specifically.**

### Why DS5 first

1. **Only RCT in the project.** DS5 is the only dataset with randomized condition assignment
   (control / default / reintervention). All model families can be interpreted against a true
   reference condition. No other dataset provides this.

2. **Richest psychosocial measures.** DS5 has validated FoMO, belonging, ostracism, and
   digital wellbeing scales — the only dataset where model parameters can be correlated
   against meaningful individual-difference variables.

3. **Cross-model consistency already established.** The completed StoP↔InT↔DyS↔StM
   quadrangle provides a coherent multi-model characterization of DS5 behavioral dynamics.
   NeT, GaT, and ABM should be implemented on the same dataset to complete the family
   before moving on.

4. **Foundation for comparison.** DS5 findings define what the CAS model families produce
   under controlled, experimental conditions. This baseline is needed to interpret DS4's
   naturalistic data correctly — without DS5 first, there is no reference point.

5. **Step 2 requires Step 1 completeness.** Phenotyping (Step 2) will use model parameters
   as features. If the DS5 model family is only partially complete when phenotyping starts,
   the phenotype feature space is incomplete. Complete DS5 Step 1 first.

---

## Phase 2 — DS5 Step 2 and early Step 3

### What this means

After all feasible DS5 Step 1 models are complete, transition to:

- **Step 2 (phenotyping):** Use DS5 model parameters as features for behavioral subgroup
  discovery. Primary notebook: `100_phenotype_exploration.ipynb`. Key feature dimensions
  from completed Step 1: σ̂, μ̂, H_emp, β_behav, χ_behav, F_behav, is_dys_eligible,
  H_SDE, H_out, H_app.

- **Early Step 3 (personalization exploration):** Exploratory intervention fitting on DS5
  using DS5 phenotype profiles. Which phenotype benefits most from which friction type?
  DS5 is the only dataset where friction type (condition) is experimentally assigned,
  making it the correct first Step 3 dataset.

DS5 should remain the primary discovery and interpretation dataset through Steps 2 and 3
before extending findings to DS4 or DS6.

---

## Phase 3 — DS4 for validation and deeper analysis

### What this means

After DS5 Step 1 (and ideally DS5 Step 2) are complete, move to DS4.

DS4's role is fundamentally different from DS5's role:

| DS5 role | DS4 role |
|---|---|
| Discovery and interpretation | Validation and extension |
| Experimental (RCT) | Naturalistic (observational, self-selected) |
| Short windows (7–45 days) — approximations | Long windows (up to 897 days) — rigorous estimation |
| Approximate Boltzmann bridge (FLAG A) | Rigorous OU Boltzmann bridge (FLAG A resolved) |
| Condition comparisons | Within/cross-participant heterogeneity |
| N=414 eligible (Step 1) | N~600-800 eligible (MIN_DAYS=30 est.) |
| Fixed-point approximation (boundary only) | True interior attractors (OU: X* = μ) |

### Why DS4 later

1. **DS4 requires DS5 findings as context.** The DS4 analysis is most valuable when it can
   answer: "does what we found in DS5 (under experimental conditions) also appear in DS4
   naturalistic data?" Without DS5 results, DS4 is an isolated analysis.

2. **DS4 resolves DS5 approximations.** The OU process on DS4 makes β rigorous (resolves
   FLAG A), enables reliable individual V(x) estimation (resolves FLAG B), and provides
   true interior attractors (resolves DyS boundary limitation). These resolutions are most
   meaningful when contrasted with the DS5 approximations they improve upon.

3. **DS4 has no psychosocial scales.** DS4 survey features are mostly demographic and
   qualitative flags — no validated Likert scales. The interpretive richness that DS5
   enables (FoMO correlations, belonging, ostracism) is not available in DS4. DS4 is
   therefore more suited to structural validation than psychological interpretation.

4. **DS4 has no experimental condition.** Condition-level comparisons — the primary DS5
   finding (friction raises σ̂) — are not possible in DS4. DS4 results describe
   heterogeneity across self-selected users, not friction effects.

### What DS4 adds over DS5

- **Longitudinal depth:** Adaptation, habit formation, and long-run behavioral stability
  are only observable with 897-day windows. DS4 is the primary dataset for these constructs.
- **Rigorous thermodynamics:** OU process makes StM exact; DyS can demonstrate true
  convergence to an interior attractor.
- **Robustness check:** Do DS5 behavioral profiles (deterministic vs stochastic regime,
  high vs low entropy) replicate in a naturalistic non-experimental sample?
- **Relaxation time τ = 1/θ:** A new behavioral quantity not estimable in DS5 — how long
  does a behavioral displacement take to decay?

---

## DS4 implementation order — dependency chain

### ⚠ Critical: do not start DS4 StM before DS4 StoP

The DS4 StM notebook (51) requires OU parameters (μ̂_OU, θ̂_OU, σ̂_OU) that must come from
DS4 StoP (53). DS4 StM cannot precede DS4 StoP.

The correct DS4 model order follows the same dependency logic as DS5:

```
DS4 StoP (53)
  └── DS4 InT (52)    — requires H_SDE from OU σ̂
  └── DS4 DyS (55)    — requires σ̂, θ̂ for OU-based regime partition
  └── DS4 StM (51)    — requires σ̂, θ̂ for rigorous β_OU
                       (blueprint already written: outputs/reports/stage4/ds4_stm_blueprint.md)
  └── DS4 NeT (54)    — requires sequence engineering; app_next/app_prev transition matrices
```

### Blocked notebooks

| Notebook | Blocked by |
|---|---|
| DS4 InT (52) | DS4 StoP (53) — needs σ̂ for H_SDE bridge |
| DS4 DyS (55) | DS4 StoP (53) — needs OU σ̂, θ̂ for regime partition |
| DS4 StM (51) | DS4 StoP (53) — needs OU μ̂, θ̂, σ̂ for β_OU |
| DS4 NeT (54) | Sequence engineering — app_next/app_prev; no other DS4 model dependency |

**First DS4 notebook to implement: DS4 StoP (53) — the OU stochastic process model.**

---

## Future handoff rule — before any DS4 work begins

Whenever a new session begins DS4 implementation work, the following must be done before
writing any code:

1. **Read** `outputs/reports/stage4/stage4_implementation_plan.md` — master planning document
   with all FLAG decisions, model family ordering, and cross-notebook connections.

2. **Read** the relevant DS4 blueprint file for the intended model. Blueprints are at:
   - DS4 StM: `outputs/reports/stage4/ds4_stm_blueprint.md` (written 2026-04-17)
   - DS4 StoP: blueprint not yet written — write it before implementing
   - DS4 InT / DyS / NeT: blueprints not yet written — write them before implementing

3. **Verify the dependency chain.** Confirm that all prerequisite DS4 notebooks are
   complete before starting the intended notebook. Use the blocked-notebooks table above
   as a checklist.

4. **Check DS5 status.** Confirm that DS5 Step 1 is sufficiently complete to justify
   moving to DS4. The minimum threshold: DS5 NeT should be complete; DS5 GaT/ABM/SyD
   deferred decisions should be recorded.

5. **Do not implement DS4 StM first.** DS4 StM has a complete blueprint but it is a
   downstream notebook. DS4 StoP comes first. Starting DS4 StM without DS4 StoP violates
   the dependency chain and produces an inconsistent output structure.

---

## Dataset role summary

| Dataset | Primary role in this project | When to use |
|---|---|---|
| **DS5** | Discovery, interpretation, experimental baseline | Phase 1 (current): complete all Step 1 models; Phase 2: phenotyping and early personalization |
| **DS4** | Validation, longitudinal extension, rigorous estimation | Phase 3: after DS5 Step 1 complete; implement in dependency order starting with DS4 StoP |
| **DS6** | Substitution dynamics (app_prev/app_next2), repeated waves | After DS4; DS6 enables SyD (repeated surveys); different behavioral proxy; group_id session structure verified non-functional 2026-08-05 |
| **DS1** | Cross-dataset reference, cleanest friction denominator | Last; simplest structure; validates generalizability |

---

## Cross-dataset reading list before implementation

Before starting any non-DS5 dataset work:

- `data_docs/modeling_cautions.md` — structural warnings for all datasets
- `data_docs/stage1_feature_qc_notes.md` — QC notes from Stage 1 preprocessing
- `outputs/reports/stage3/recommended_first_modeling_pass.md` — Stage 3 modeling readiness assessment
- `outputs/reports/stage4/stage4_implementation_plan.md` — master Stage 4 plan

For DS4 specifically:
- `outputs/features/ds4/ds4_features.md` — DS4 feature definitions and event class structure
- `outputs/reports/stage4/ds4_stm_blueprint.md` — StM blueprint (already written; read before DS4 StM)
