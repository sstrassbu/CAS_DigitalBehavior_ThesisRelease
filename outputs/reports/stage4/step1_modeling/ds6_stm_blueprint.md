# DS6 — Statistical Mechanics (StM) Blueprint

**Notebook:** `notebooks/71_ds6_statistical_mechanics.ipynb`
**Written:** 2026-08-06
**Position:** 71 in the DS6 70s decade. Last active DS6 Step 1 model family — closes all 7
(StoP, NeT, InT, DyS, SyD, StM implemented; GaT/ABM remain deferred pending Step 2, matching
DS5/Structured precedent). Depends on InT (75, for the H_app/H_hour marginal-vs-joint
sanity check), not StoP directly (same independence Structured's StM notebook had from its
own StoP).
**Depends on:** `outputs/cleaned/ds6_behavioral_clean.csv`,
`outputs/model_outputs/ds6/information_theory/participant_entropy_metrics.csv`
**Output root:** `outputs/model_outputs/ds6/statistical_mechanics/`

---

## Part 0 — Why this is not a DS5 port, and not a Structured port either

DS5's StM built a literal two-state (opened/not-opened) Boltzmann apparatus:
`β_behav = 2/σ̂²`, `T_behav`, `Z_2state`, `F_behav` — defensible there because DS5's StoP
state variable is a bounded [0,1] rate that plausibly approximates a two-state occupation
probability. Structured's own StM notebook explicitly refused to port this (the paper
cautions against literal energy/temperature/equilibrium variables), building a discrete
multi-property macrostate space instead, with no β/T/Z/F apparatus and no dependency on its
own StoP output.

**DS6 has an even weaker case for DS5's bridge than Structured did:** DS6's StoP state
variable (daily attempt count) is not bounded at all on the upper side (§ blueprint 73,
Part 0) — the two-state occupation-probability interpretation behind `β=2/σ̂²` doesn't apply
even as a loose analogy. DS6 follows Structured's departure, for an even more direct reason:

- **No β_behav/T_behav/Z/F apparatus built.**
- **No dependency on StoP's output** (matching Structured's own StM independence from its
  StoP notebook) — this notebook uses only the raw behavioral log and InT's entropy outputs.

---

## Part 1 — Theory grounding (paper §2.1, quoted directly)

> "Properties such as condition, target app, time, prior attempts, and resolution code
> define the event-state configuration... a single opening attempt is... represented as a
> configuration of behavioral features: the target app, the experimental condition, whether
> the breathing delay occurred, the time of day, the prior outcome, and the current
> resolution."
>
> "...this model must be used carefully because physical quantities such as energy or
> temperature are not directly observed... They should be treated as behavioral analogies or
> derived proxy quantities, not literal measurements."

DS6 cannot use "resolution code" or "prior outcome" (no outcome variance — the limitation
carried through every DS6 Step 1 notebook). Uses the paper's other two named configuration
properties directly: **target app** and **time of day**.

---

## Part 2 — Microstate definition: joint (app, hour-bucket) configuration

```
Microstate = (app_name, hour_bucket)
hour_bucket ∈ {night(0-5), morning(6-11), afternoon(12-17), evening(18-23)}
             -- reuses the exact boundaries already established in Stage 1's
                morning_event_share (06-11) / evening_event_share (18-23) features,
                not new bucket choices invented here
```

**Non-redundancy check (matching Structured's StM precedent of checking before building):**
InT (75) already computed marginal entropies `H_app` and `H_hour` separately, per period.
This notebook's joint entropy `H_joint = H(app_name, hour_bucket)` is NOT redundant with
either marginal — it captures co-occurrence structure (does this participant open specific
apps at specific times, or is app choice independent of time?) that neither marginal alone
can show. Standard identity, used as a **mandatory sanity gate** (same discipline that
caught two real bugs in the InT notebook's own NeT-InT bridge): `H_joint >= max(H_app,
H_hour)` for every participant, every period — checked, not assumed.

---

## Part 3 — Three macrostate summaries per participant × period (no β/T/Z/F)

```
H_joint^(period)         = Shannon entropy (bits) of the (app, hour_bucket) joint distribution
dominant_config^(period) = the single most frequent (app, hour_bucket) pair
dominant_config_share    = that pair's share of all events in the period
```

**Persistence** (paper: "stable regimes," "path-dependent... behavior remains changed"):

```
config_persistent = 1 if dominant_config_baseline == dominant_config_intervention, else 0
```

DS6-specific — no DS5 or Structured equivalent — because it requires the baseline/
intervention period structure only DS6 has among this project's OneSec datasets.

**Susceptibility** (paper: "friction-sensitive user may show a large shift... after a
relatively small intervention" — reframed here across DS6's period boundary rather than
DS5's between-condition contrast, consistent with every other DS6 notebook's period-first
design):

```
susceptibility = Jensen-Shannon divergence(P_baseline(app,hour), P_intervention(app,hour))
```

JS divergence is bounded [0,1] bit, symmetric, and well-defined even when the two
distributions have different supports (unlike KL divergence) — appropriate here since a
participant's app set can differ between periods. A standard, established measure, not
invented for this notebook.

---

## Part 4 — Output file structure

```
outputs/model_outputs/ds6/statistical_mechanics/
  participant_macrostate_metrics.csv   # one row per participant: H_joint_<period>,
                                        # dominant_config_<period>, dominant_config_share_<period>,
                                        # config_persistent, susceptibility, study_condition
  int_bridge_check.csv                 # per-participant H_joint vs H_app/H_hour sanity gate
  condition_macrostate_summary.csv     # study_condition x study_period summary
  susceptibility_psychosocial_correlations.csv  # susceptibility vs addiction/self_control indices
  figures/
    fig1_stm_hjoint_by_period.png
    fig2_stm_persistence_distribution.png
    fig3_stm_susceptibility_distribution.png
    fig4_stm_int_bridge_scatter.png
  model_run_summary.md
```

Each CSV gets its own companion `.md` file per the standing documentation convention.

---

## Implementation readiness checklist

- [x] Confirmed DS5's β=2/σ̂² bridge does not transfer (DS6's StoP variable isn't bounded,
      an even weaker case than Structured's) — no β/T/Z/F apparatus built, matching
      Structured's own departure
- [x] Paper §2.1 quoted directly; microstate = (app, hour) matches the paper's own named
      configuration properties (target app, time of day)
- [x] Non-redundancy vs InT's marginal entropies confirmed before building (joint vs
      marginal, same resolution pattern as Structured's InT-vs-StM split)
- [x] H_joint >= max(H_app, H_hour) planned as a mandatory sanity gate, not assumed
- [x] Persistence and susceptibility both identified as DS6-specific (period-boundary-based),
      not DS5/Structured ports
- [x] Notebook 71 implemented and executed. Two bugs found and fixed (sanity-gate
      comparability: H_joint's 4-bucket hour vs InT's 24-value H_hour; then an assertion
      NaN-handling bug in the fix's own validation code) — both caught before results were
      trusted. **Headline: control shows significantly lower susceptibility than either
      friction condition** (control=0.028 vs default=0.070 p=0.0011, vs
      intervention=0.052 p=0.0075; default vs intervention ns) — DS6's first clearly
      condition-differentiated (not just period-differentiated) result across all of Step 1.
      **This closes DS6 Step 1 for all 7 active model families**
      (StoP/NeT/InT/DyS/SyD/StM + GaT/ABM formally deferred). See
      `outputs/model_outputs/ds6/statistical_mechanics/model_run_summary.md`.
