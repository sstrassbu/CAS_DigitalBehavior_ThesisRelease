# DS4 ABM (Agent-Based Modeling) Model — Stage 4 Step 1 Blueprint

**Stage 4, Step 1 — Theoretical and Conceptual Modeling**
**Written:** 2026-08-07
**Status: IMPLEMENTED — approved and completed 2026-08-07.** See
`outputs/model_outputs/ds4_agent_based/model_run_summary.md` for actual executed
results. Blueprint preserved below as the pre-registration record; unmodified except
for this status line.
**Notebook (to be created):** `notebooks/57_ds4_agent_based.ipynb`
**Generator script (to be created):** `notebooks/make_57_ds4_abm.py`
**Producing dataset:** DS4 — Large Naturalistic OneSec Users (N=1,039)
**Model family:** Agent-Based Modeling (ABM)
**Prerequisites:** DS4 StoP (53) — complete, output loaded directly. This is the last
of the originally-excluded DS4 families to be revisited (SyD stays excluded — DS4 has
no repeated survey waves, a hard data constraint unrelated to phenotyping).

---

## 1. Why ABM is being revisited now, and what changed

ABM was excluded because it "needs DS4 Step 2 phenotyping output" as agent inputs. Step
2 (Phase 1 + Paths A′/C′/F′) is now complete. Structured hit this identical checkpoint
and built ABM afterward, sourcing all agent rules from already-fitted outputs rather
than re-estimating from raw data — this blueprint follows that same discipline, but the
actual validation target is DS4-specific, not ported.

---

## 2. Paper grounding — quoted from the OneSec paper §2.7

> "Agent-Based Modeling explains macro-level patterns as emerging from the local
> behavior of heterogeneous rule-based agents... users can be represented as
> heterogeneous smartphone-user agents who follow different app-opening, dismissal,
> switching, and adaptation rules."
>
> "Agent rules: Rules may include probabilities of target-app attempts, continuation,
> dismissal, return after dismissal, switching, or disengagement."
>
> "The value of ABM is that it can test whether simple local rules are sufficient to
> reproduce broader observed patterns... Empirical features from Information Theory,
> Stochastic Processes, and Network Theory can be used to inform the agent types and
> rules."
>
> Example B (§2.7): "ABM can operationalize user profiles as rule-based agents and then
> test whether these profiles are dynamically plausible."

---

## 3. DS4-specific validation target — not ported from Structured

Structured's ABM tested whether simple agents reproduce real **burstiness (Fano
factor)** — a StoP-specific target that doesn't exist for DS4 (DS4's StoP is a
mean-reverting OU process, not a count process). DS4 needs its own target, and one is
already sitting in this project's own findings:

**StoP's headline finding:** DS4's daily-fitted relaxation time (median τ̂≈0.63 days)
diverges sharply from the weekly-fitted one (median τ̂≈0.91 weeks), with only r=0.316
correlation between daily and weekly θ̂ per participant
(`participant_parameters_weekly_sensitivity.md`). This was flagged throughout Step 1 as
an *open, unresolved* question — a real emergent property of the data, not built into
the OU model by construction.

**ABM's question:** if each participant is modeled as a pure discrete-time OU agent
using their own already-fitted daily (μ̂, θ̂, σ̂) — the simplest possible agent, no added
mechanism — does simulating from it and re-fitting weekly reproduce the *real* observed
daily/weekly divergence, or does a pure daily-OU agent predict much tighter
daily-weekly consistency than what real participants show? This directly tests "are
simple local (daily) rules sufficient to reproduce the broader (weekly) observed
pattern" — the paper's own framing, applied to DS4's own actual open question.

---

## 4. FLAG decisions

| Flag | Decision | Justification |
|---|---|---|
| FLAG 1 | Agent parameters = each real participant's own fitted (μ̂,θ̂,σ̂) from StoP, not re-estimated | Paper's own instruction to use already-fitted StoP/InT/NeT outputs |
| FLAG 2 | Model 1 (baseline): pure fixed-parameter discrete OU agent, no added mechanism | Simplest agent — tests whether daily OU dynamics alone explain the real divergence |
| FLAG 3 | Model 2 (one added mechanism): Model 1 + a weekly-periodic drift modulation (day-of-week effect on μ) | Mirrors Structured's "1 added mechanism, 1 simplifying assumption" complexity ladder — simplest plausible extension if Model 1 fails |
| FLAG 4 | Validation = compare simulated daily-vs-weekly θ̂ divergence (magnitude + correlation) to the real StoP numbers, not re-derive new statistics | Uses StoP's own already-computed real numbers as ground truth |
| FLAG 5 | Simulated series length = each participant's own real `n_days_obs` | Fair comparison — same amount of simulated data as was available for the real fit |

---

## 5. Theory-to-data mapping

| Quantity | Source |
|---|---|
| Agent (μ̂,θ̂,σ̂) | StoP `participant_parameters.csv`, `fit_valid=True` rows only |
| Simulated daily path | `X_{t+1} = μ̂ + (X_t-μ̂)·e^{-θ̂} + noise`, same discrete OU recursion StoP itself used to derive the estimator |
| Simulated weekly refit | Same weekly-aggregation + AR(1) method as StoP's own `participant_parameters_weekly_sensitivity.csv` |
| Real target | StoP's own real daily `theta_hat_OU`/`tau_hat` and weekly `theta_hat_OU_weekly`/`tau_hat_weekly` |

---

## 6. Notebook structure — `notebooks/57_ds4_agent_based.ipynb`

| Cell | Type | Content |
|---|---|---|
| 1 | MD | Scope + paper quotes |
| 2 | MD | FLAG decisions |
| 3 | MD | Validation target explanation (§3) |
| 4 | Code | Setup; load StoP's real daily + weekly output |
| 5 | Code | Model 1: simulate discrete OU per valid-fit participant using their own (μ̂,θ̂,σ̂), length=n_days_obs |
| 6 | Code | Model 1: aggregate simulated daily path to weekly, refit weekly OU (same method as StoP) |
| 7 | Code | Model 1 validation: compare simulated vs real daily/weekly θ̂ divergence (ratio, correlation) |
| 8 | Code | Model 2: add weekly-periodic drift modulation; repeat simulate+refit+validate |
| 9 | Code | Side-by-side Model 1 vs Model 2 vs real comparison table |
| 10 | Code | Export outputs |
| 11 | Code | Figures: simulated vs real weekly τ̂ distributions; simulated vs real daily-weekly correlation scatter |
| 12 | MD | Interpretation and limits — report honestly whether either model closes the gap, partial, or not at all (matching Structured's own "partially sufficient" honest framing) |
| 13 | MD | Forward connections |

---

## 7. Proposed outputs

**Output root:** `outputs/model_outputs/ds4_agent_based/`

| File | Description |
|---|---|
| `participant_abm_simulation_results.csv` | Per participant: real daily/weekly θ̂, Model 1 simulated daily/weekly θ̂, Model 2 simulated daily/weekly θ̂ |
| `abm_model_comparison_summary.csv` | Aggregate comparison: real vs Model 1 vs Model 2 divergence magnitude + correlation |
| `model_run_summary.md` | Full run record |
| `figures/` | 2 figures |

---

## 8. DS4 weakness flags

- ⚠ FLAG I: Only `fit_valid=True` participants (641) can be simulated — inherits
  StoP's own eligibility population and attrition caveat.
- ⚠ FLAG II: Model 2's weekly-periodic mechanism is one plausible addition among many
  (day-of-week is the simplest, not the only, candidate) — a negative result does not
  rule out other mechanisms.
- ⚠ FLAG III: This is a recoverability/sufficiency test, not a claim that participants
  literally follow an OU process — same model-assumption caveat as StoP/DyS/StM.

---

## ⚠ IMPLEMENTATION HOLD (historical — resolved 2026-08-07)

This hold applied during blueprint review and has since been cleared; the notebook was
approved and implemented. Kept below for the historical record.
