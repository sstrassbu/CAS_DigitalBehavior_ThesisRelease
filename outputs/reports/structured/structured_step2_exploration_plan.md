# Structured Step 2 — Systematic Phenotype Exploration Plan

**Written:** 2026-08-05
**Mirrors:** `outputs/reports/stage4/ds5_step2_phenotype_exploration_plan.md` (DS5's six-path plan) and
its outcome, `outputs/reports/stage4/post_analysis/ds5_step2_master_synthesis.md` (the "two orthogonal
layers" finding). This document maps each DS5 path onto Structured, adapts where a construct genuinely
transfers, and explicitly declines to port where it does not — rather than forcing a schema Structured's
data cannot support.
**Status:** Planning document — **execution complete** (2026-08-05). All four adapted paths (A, C, D, F)
described below were implemented and executed; see `structured_step2_master_synthesis.md` for the
consolidated findings and each `structured_path_[a|c|d|f]_blueprint.md` for per-path results appended
after running. This plan document itself was not rewritten after execution — read it as the design
rationale, and the synthesis note as the outcome.

---

## 0. Why this exists

Structured's Phase 1 phenotyping (`notebooks/120_structured_phenotype_exploration.ipynb`) was
deliberately scoped to **one** clustering pass, not DS5's six-path exploration, justified at the time by
sample size (N=36 complete-case vs. DS5's N=414). That scoping decision is being revisited now at the
user's request: run the rest of what DS5 did, adapted to what Structured's data can actually support.

**Critical difference from a literal port:** DS5 is an RCT with three friction conditions and a defined
intervention-outcome variable (`H_out`). Structured is a retrospective, non-experimental dataset with no
friction intervention at all — the behavioral object is task planning, not app-opening friction. Two of
DS5's six paths (B and E) are built entirely around constructs that do not exist here. Section 2 below
treats each path on its own merits rather than assuming all six transfer.

---

## 1. Verified population numbers (checked against the real CSVs before writing anything below)

| Population | N | Definition |
|---|---|---|
| Phase 1 complete-case (existing, notebook 120) | 36 | all 7 curated features eligible |
| Behavior-only (drop NeT requirement) | 41 | InT ∩ StoP ∩ DyS ∩ SyD ∩ StM ∩ GaT eligible |
| NeT-eligible (existing, notebook 64) | 45 | ≥20 pooled transitions |
| NeT-eligible ∩ Phase 1 | 36 / 36 | **all** Phase 1 participants are already NeT-eligible — no loss |
| NeT-eligible, not in Phase 1 | 9 | excluded from Phase 1 by some other model's eligibility gate |
| Phase 1 Profile A / B sizes | 22 / 14 | from `cluster_assignments.csv` |
| Phase 1 subscription split | pro=25, free=11 | free arm is very thin |
| Behavior-only (N=41) subscription split | pro=29, free=12 | still very thin |

These numbers replace placeholder estimates in every section below — no path design here relies on an
unverified guess.

---

## 2. Path-by-path mapping

### Path C → Structured NeT-substructure check — PORTS, adapted

**DS5 question:** within the dominant hub-locked profile, is there network sub-structure?
**Structured adaptation:** Structured's Phase 1 split is **not** NeT-dominated the way DS5's was — DS5's
Profile A/B gap on HHI_net was 0.545 vs. 0.978 (huge); Structured's is 0.505 vs. 0.573 (modest). The
features that actually separate Structured's Profile A/B are `state_space_volatility` (1.71 vs. 0.55) and
`created_Fano_factor` (7.49 vs. 4.61) — behavioral-dynamics features, not network features. **This is
itself a genuine finding worth stating explicitly: Structured's dominant phenotype axis looks like DS5's
Layer 2 (behavioral), not DS5's Layer 1 (network) — the opposite emphasis.**

Given that, the direct DS5-Path-C question ("sub-structure within the NeT-driven profile") doesn't
map cleanly, because there is no NeT-driven profile here yet to sub-divide. Adapted design:
1. Cluster on NeT-only features (`HHI_net`, `rho_self`, `H_trans`, `top1_share_net`) across the full
   NeT-eligible population (N=45) — independent of Phase 1 — analogous to DS5's "full-sample NeT-only
   robustness check."
2. Compare via ARI against Phase 1 labels for the 36 participants who have both.
3. **Falsifiable prediction, stated in advance:** if Structured's Phase 1 split really is behaviorally-,
   not network-, driven, ARI(NeT-only clusters vs. Phase 1) should be **low** — the opposite of DS5,
   where NeT-only clustering reproduced Phase 1 almost perfectly (ARI=0.990).
4. Sub-cluster within Phase 1 Profile A (N=22) and Profile B (N=14) using the same NeT features, exactly
   as DS5 did — but flag in advance that N=14–22 is far below DS5's N=125–289, so any k≥2 split found
   here is tentative by construction, not a confident finding.

**Notebook:** `121_structured_network_subphenotype.ipynb`

---

### Path A → Structured behavior-only phenotyping — PORTS, this is the user's named example

**DS5 question:** what phenotype structure emerges when network topology is excluded?
**Structured adaptation:** direct port. Features: `H_completion` (InT), `created_Fano_factor` (StoP),
`state_space_volatility` (DyS), `backlog_trend_slope` (SyD), `susceptibility` (StM),
`mean_commitment_score` (GaT) — the same 6 curated Phase 1 features minus `HHI_net`. Population: **N=41**
(verified above), a real gain of 5 over Phase 1's complete-case 36.

**Expected outcome, stated in advance:** given the finding above (Structured's Phase 1 split already
looks behaviorally-driven, not network-driven), Path A here may show **higher** ARI against Phase 1 than
DS5's near-zero (0.020) — DS5's Path A was orthogonal to its Phase 1 specifically because Phase 1 was
network-dominated; Structured's Phase 1 may already substantially resemble what dropping NeT produces.
This is a genuine, falsifiable, pre-stated prediction — not fit after running.

**Notebook:** `122_structured_behavior_only_phenotype.ipynb` — built first (highest expected value,
directly what was asked for, best-powered population).

---

### Path F → Structured hierarchical two-stage — PORTS, flagged as likely fragile

**DS5 question:** does Stage 1 (network split) × Stage 2 (behavioral sub-split within each) reveal richer
structure than either alone?
**Structured adaptation:** Stage 1 = Phase 1 Profile A/B (N=22/14). Stage 2 = behavioral sub-clustering
within each stage using the Path A feature set. **Stated in advance:** DS5 found even N=125 (Profile A)
sub-clustering marginal (Jaccard=0.744). Structured's stage-1 groups are 14 and 22 — roughly a sixth to a
ninth of DS5's smallest stage-1 group. A stable k≥2 sub-split within either is unlikely; the realistic,
useful output of this notebook may be "no stable sub-structure at this N," reported as a legitimate
finding per this project's standing "no forced outcome" principle, not a failure to fix.

**Notebook:** `123_structured_hierarchical_phenotype.ipynb` — built after 121+122 exist, since it
consumes both.

---

### Path D → Structured secondary/robustness features — PORTS, scoped down

**DS5 question:** does drift/impulsivity/circadian structure (secondary features beyond the core set)
add a genuinely new dimension?
**Structured adaptation:** secondary features available but not in the curated 7: `created_mu_hat`,
`created_sigma_mu_ratio` (StoP), `volume_trend_slope`, `dropout_score` (DyS), `H_hour_creation` (InT),
`H_config` / `persistence_rate` (StM). **Scoping decision:** DS5's own synthesis rated Path D as its
lowest-yield path ("confirms Layer 2, doesn't reveal new dimension") even with N=285. Given Structured's
much smaller populations for these secondary features, this is built as a **compact robustness notebook**
(ARI against Path A, feature-correlation gate, no new blueprint-level theoretical claims expected) rather
than a full six-figure treatment — proportionate to its own DS5 precedent's demonstrated low yield, not
arbitrarily cut.

**Notebook:** `124_structured_dynamic_stochastic_phenotype.ipynb` — built after 122 (Path A analog), since
it is explicitly a robustness check against it.

---

### Path E → Structured subscription-stratified — PORTS ONLY AS A SHORT, EXPECTED-NULL CHECK

**DS5 question:** does phenotype structure differ across randomized friction conditions?
**Structured has no randomized conditions.** The only available stratifying variable is
`subscription_type_last` (free/pro) — already used throughout Step 1 as "observational only, no causal
claim" (subscription is self-selected, not assigned). Verified split: **11 free / 25 pro** at Phase 1
N=36; **12 free / 29 pro** at the Path A population N=41.

**This is not a meaningful replication of Path E's actual question** (condition-invariance under random
assignment) — it is at best a weak descriptive check of whether the free-tier minority looks different.
DS5's own condition arms (N≈100–140) already found one of three infeasible; Structured's free arm (N=11–12)
is 8-12x smaller than that. **Predicted outcome, stated in advance: infeasible or unstable clustering in
the free subgroup**, reported honestly as a null/underpowered result if that's what happens, not
suppressed or forced into a false-positive split.

**Scoping decision:** given this, Path E is built as a **short supplementary check**, not a full notebook
with its own blueprint — a few cells appended to the end of `122_structured_behavior_only_phenotype.ipynb`
(within-subscription-group clustering attempt + explicit feasibility verdict), not a separate numbered
notebook. This keeps effort proportionate to the very limited question this data can actually answer.

---

### Path B → Structured intervention-sensitive — DOES NOT PORT, not built

**DS5 question:** does friction-outcome-response variability (`H_out_resid`) define its own phenotype
axis, independent of behavioral dynamics?
**Why this has no Structured analog:** `H_out` is entropy over friction intervention outcomes
(opened/dismissed/closed) — Structured has no friction intervention, no intervention-exposure events, and
no outcome variable of this kind. There is no proxy construction that would not be fabricating an
intervention-response variable Structured's data does not contain. The closest adjacent construct
already implemented is GaT's `commitment_score` → completion-outcome relationship (Step 1, notebook 66),
which answers a related but different question ("does task structure predict completion") and is not a
response-*variability* measure the way `H_out_resid` is.

**Decision: not built.** Documented here, in the same spirit as InT's explicit "task_energy_level →
reschedule_occurrence: NOT IMPLEMENTABLE" entry — an honest absence, not a silently skipped path.

---

## 3. Summary: what gets built

| DS5 Path | Structured status | Notebook | Population |
|---|---|---|---|
| C (network sub-phenotyping) | Adapted | `121_structured_network_subphenotype.ipynb` | N=45 (NeT-only), 22/14 (within Phase 1) |
| A (behavior-only) | Direct port | `122_structured_behavior_only_phenotype.ipynb` | N=41 |
| F (hierarchical) | Adapted, likely fragile | `123_structured_hierarchical_phenotype.ipynb` | 22/14 |
| D (dynamic/stochastic) | Scoped down | `124_structured_dynamic_stochastic_phenotype.ipynb` | ≤41 |
| E (condition-stratified) | Shrunk to a short check | appended to notebook 122 | 12/29 |
| B (intervention-sensitive) | **Not portable — not built** | — | — |

**Execution order:** 122 (Path A analog) first — highest value, best-powered, directly what was named as
the example — then 121 (Path C analog), then 124 (Path D analog, depends on 122), then 123 (Path F
analog, depends on both 121 and 122). Path E's short check rides along inside 122.

Each notebook gets its own blueprint (`structured_path_a_blueprint.md` etc.) before code, following this
project's established discipline, with a companion `.md` for every output file. After all four notebooks
run, a synthesis note mirroring `ds5_step2_master_synthesis.md` will state whether Structured shows the
same "two orthogonal layers" structure DS5 found, or something different — including the possibility,
already flagged above, that Structured's layers are inverted relative to DS5's (behavioral axis dominant,
network axis subtle) rather than mirroring DS5's network-dominant finding.

---

## 4. What would make this a weaker or stronger thesis contribution

**Weaker if:** every adapted path just reproduces Phase 1 (all ARIs near 1.0) — would mean N=36-41 and
7 correlated features don't have enough independent structure to reveal anything beyond the single global
split already found. This is a real, stated risk given DS5 needed N=414 to find genuinely orthogonal
layers.

**Stronger if:** Path A (behavior-only) or Path C (NeT-only) shows a meaningfully different grouping from
Phase 1 (low-to-moderate ARI) — would demonstrate Structured also has more than one axis of individual
difference, just organized differently than DS5's (behavioral-dominant vs. DS5's network-dominant), which
would itself be a genuine, reportable cross-dataset contrast.

Both outcomes are informative and will be reported as found, not steered toward either.
