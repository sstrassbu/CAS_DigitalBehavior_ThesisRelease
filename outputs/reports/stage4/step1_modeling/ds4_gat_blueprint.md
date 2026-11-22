# DS4 GaT (Game Theory) Model — Stage 4 Step 1 Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**
**Written:** 2026-08-07
**Status: IMPLEMENTED — approved and completed 2026-08-07.** See
`outputs/model_outputs/ds4_game_theory/model_run_summary.md` for actual executed
results. Blueprint preserved below as the pre-registration record; unmodified except
for this status line.
**Notebook (to be created):** `notebooks/56_ds4_game_theory.ipynb`
**Generator script (to be created):** `notebooks/make_56_ds4_gat.py`
**Producing dataset:** DS4 — Large Naturalistic OneSec Users (N=1,039)
**Model family:** Game Theory (GaT)
**Prerequisites:** None required, but joins StM's `chi_OU` and Step 2's phenotype
clusters for cross-checks where available.

---

## 1. Why GaT is being revisited now

GaT was originally excluded from DS4 Step 1 "pending behavioral profiles" — the same
reason DS5 deferred it. DS4 Step 2 (phenotyping, including the further-exploration
paths) is now complete, so that blocking condition no longer holds. Structured hit this
identical checkpoint and built GaT afterward using a named proxy score (no formal
payoff matrix, since Structured's own paper also lacks observed payoff data). This
blueprint follows the same shape for DS4, grounded in the **OneSec paper's own §2.6**
(quoted below), not ported from Structured's task-planning-specific content.

---

## 2. Paper grounding — quoted from `data_docs/pdfs/One Sec Smartphone-Intervention
Behavior as a Complex Adaptive System.pdf` §2.6

> "Game Theory models choices, strategies, and payoffs in repeated decision situations.
> In the One Sec context, the framework can be used to interpret app-opening attempts
> as repeated conflicts between immediate app access and longer-term self-regulation
> goals."
>
> "Behavioral framing: The model treats opening versus dismissal as a repeated
> strategic choice involving the present self and the future self."
>
> "Repeated interaction: Users may adapt their strategy after successful dismissal,
> repeated override, frustration, or rebound."
>
> "Phenotypes: Users may be described as commitment-oriented, reward-oriented, chronic
> overriders, adaptive switchers, or friction-avoidant users."
>
> "In Game Theory, payoff and utility are also not directly observed, so the model
> should be used as an interpretive framework for repeated self-regulation choices
> rather than as a literal payoff model." (§1.3, the project-wide caution also applied
> to DS5/Structured StM/GaT)
>
> Example B (§2.6): "commitment-oriented users who frequently dismiss, reward-oriented
> users who frequently continue, chronic overriders who repeatedly proceed despite
> friction, and adaptive switchers who modify their behavior after repeated outcomes."

**No formal payoff matrix or Nash equilibrium is built** — matches the paper's own
explicit caution, and matches Structured's precedent. This notebook builds the named
proxy phenotypes and tests their correlational structure only.

---

## 3. DS4-specific construction — verified real data, not guessed

The paper names 4 phenotypes with distinct behavioral signatures. Three DS4 quantities
map to them directly, **checked for redundancy before use**:

| Quantity | Source | Redundancy check |
|---|---|---|
| `rate_opened_intervention_events` | Stage 1 feature (already computed) | Primary reward/commitment axis |
| `p_open_after_dismiss` | Stage 1 feature | **Rejected** — correlates r=0.934 with `rate_opened_intervention_events`, near-tautological, would add nothing |
| `max_consecutive_opens` | Stage 1 feature | Moderate correlation with opened-rate (r≈0.5-0.6) — genuinely adds streak/habituation information beyond the raw rate |
| `substitution_after_dismissal_rate` (**new, computed here**) | `P(app_next ≠ app_current \| outcome=dismissed)`, attempt rows | Real, checked: r=0.086-0.109 with the other quantities — genuinely independent axis |

**Verified (2026-08-07):** pooled substitution-after-dismissal rate = 0.283 — most
dismissals are followed by returning to the *same* app next, not switching. Usable N
(≥5 dismissal-then-next-event pairs) = 989.

**Classification rule** (descriptive, rule-based — matches Structured StoP's own
"Step 1 rule-based, NOT clustering" precedent; formal clustering already happened in
Step 2):

```
if rate_opened_intervention_events >= median:
    if max_consecutive_opens >= top-tertile: "chronic_overrider"
    else:                                     "reward_oriented"
else:
    if substitution_after_dismissal_rate >= top-tertile: "adaptive_switcher"
    else:                                                  "commitment_oriented"
```

**Verified group sizes (N=986):** commitment_oriented=352, chronic_overrider=304,
reward_oriented=190, adaptive_switcher=140 — all four groups substantial, real
cutoffs (median opened-rate=0.682, override tertile=23 consecutive opens, substitution
tertile=0.343).

The paper's 5th named phenotype ("friction-avoidant users") is not separately
operationalized — no DS4 quantity distinguishes "avoids friction situations entirely"
from "commitment-oriented" with the data available; noted as a limitation, not silently
dropped.

---

## 4. FLAG decisions

| Flag | Decision | Justification |
|---|---|---|
| FLAG 1 | No formal payoff matrix / Nash equilibrium | Paper's own explicit caution (§1.3); matches DS5/Structured StM/GaT precedent |
| FLAG 2 | Drop `p_open_after_dismiss` from the construction | Near-tautological with opened-rate (r=0.934) |
| FLAG 3 | `substitution_after_dismissal_rate` computed fresh (new quantity) | Not covered by NeT (which doesn't condition transitions on prior outcome) or any other DS4 Step 1 notebook |
| FLAG 4 | Rule-based classification, not re-clustering | Step 2 already did formal clustering; this is a Step 1 descriptive typology matching the paper's named categories directly |
| FLAG 5 | "Friction-avoidant" phenotype not operationalized | No DS4 quantity distinguishes it from commitment-oriented; reported as a limitation |

---

## 5. Cross-checks planned (correlational, not causal)

- `gat_phenotype` vs StM's `chi_OU` (susceptibility) — do chronic overriders show
  higher susceptibility?
- `gat_phenotype` vs Step 2 Phase 1 / Path A' behavior clusters — do GaT phenotypes
  align with the dynamics-based taxonomy, or add new information?
- Adaptation check (paper's own "adapt their strategy after repeated override" idea):
  DS4 already has `open_rate_change_calendar` (Stage 1, early-vs-late tertile) — test
  whether `adaptive_switcher`-labeled participants show larger `|open_rate_change_calendar|`
  than other phenotypes (a directly paper-motivated, already-available quantity, reused
  not recomputed).

---

## 6. Notebook structure — `notebooks/56_ds4_game_theory.ipynb`

| Cell | Type | Content |
|---|---|---|
| 1 | MD | Scope + paper quotes (§2) |
| 2 | MD | FLAG decisions |
| 3 | MD | DS4 structural cautions (attempt-row convention, no condition) |
| 4 | Code | Setup |
| 5 | Code | Load Stage 1 features; compute `substitution_after_dismissal_rate` from attempt rows |
| 6 | Code | Redundancy check: reproduce `p_open_after_dismiss` vs `rate_opened` correlation live |
| 7 | Code | Classification rule; reproduce real group sizes |
| 8 | Code | Cross-check vs StM `chi_OU` |
| 9 | Code | Cross-check vs Step 2 phenotype clusters (Phase 1 + Path A') |
| 10 | Code | Adaptation check vs `open_rate_change_calendar` |
| 11 | Code | Export outputs |
| 12 | Code | Figures (phenotype distribution, chi_OU by phenotype, cross-tab vs Step 2 clusters) |
| 13 | MD | Interpretation and limits |
| 14 | MD | Forward connections |

---

## 7. Proposed outputs

**Output root:** `outputs/model_outputs/ds4_game_theory/`

| File | Description |
|---|---|
| `participant_gat_phenotypes.csv` | Per participant: 3 input quantities, `gat_phenotype` label |
| `gat_chi_ou_correlation.csv` | Cross-check vs susceptibility |
| `gat_phenotype_crosstab.csv` | Cross-tab vs Step 2 clusters + chi-square |
| `model_run_summary.md` | Full run record |
| `figures/` | 3 figures |

---

## ⚠ IMPLEMENTATION HOLD (historical — resolved 2026-08-07)

This hold applied during blueprint review and has since been cleared; the notebook was
approved and implemented. Kept below for the historical record.
