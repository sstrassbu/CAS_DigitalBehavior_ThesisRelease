# DS6 — Information Theory (InT) Blueprint

**Notebook:** `notebooks/75_ds6_information_theory.ipynb`
**Written:** 2026-08-06
**Position:** 75 in the DS6 70s decade. Depends on StoP (73, for the H_SDE bridge and the
zero-filled daily count series) and NeT (74, for the H_trans/InT-NeT bridge). Both are
already complete, so this notebook is unblocked.
**Depends on:** `outputs/cleaned/ds6_behavioral_clean.csv`,
`outputs/features/ds6/ds6_behavior_features.csv`,
`outputs/model_outputs/ds6/stochastic_processes/` (sig_hat, daily_series_long),
`outputs/model_outputs/ds6/network_models/` (H_trans)
**Output root:** `outputs/model_outputs/ds6/information_theory/`

---

## Part 0 — Why this is not a mechanical DS5 port

DS5's InT notebook computed five entropy dimensions: H_out (outcome entropy), H_app, H_hour,
H_emp (binned X_t), H_SDE (Gaussian bridge from StoP sig_hat). DS6 shares the same theory
paper section (§2.5 is generic across all OneSec datasets, unlike Structured which needed
its own paper), so the *menu* of possible measures is the same — but not every DS5 measure
transfers, and one DS6-specific test is added that DS5 didn't do.

- **H_out does NOT transfer.** DS6 has no dismiss/close outcome (`event_outcome_simple` is
  'opened' for all 353,796 rows) — entropy over a single-category distribution is 0 by
  definition, a constant, not a measurement. Excluded entirely, not computed-and-discarded.
- **H_app, H_hour, H_emp, H_SDE all transfer**, but every one of them must be split by
  `study_period` (baseline/intervention) — DS6's defining structural feature that DS5 has no
  equivalent for — to stay consistent with the StoP (73) and NeT (74) notebooks, which
  already report every quantity per period. A pooled-only H_app/H_hour would be a step
  backward relative to what's already been established for this dataset.
- **New: one pooled mutual-information test**, `MI(study_period; app_name)`. DS5 deferred
  MI/KL entirely (FLAG 4, "MI/KL deferred"). DS6 has a specific, paper-grounded reason to
  include one: the paper's own §2.5 text names "time of day may reduce uncertainty about
  [app choice]" as an example MI application, and NeT (74) already found a significant
  period-level shift in network concentration (HHI_net). Testing whether `study_period`
  measurably reduces uncertainty about *which app* is opened, pooled across the sample, is
  the natural population-level counterpart to that per-participant network finding — not
  filler, a direct follow-up question the prior notebook raised.

---

## Part 1 — Theory grounding (paper §2.5, quoted directly)

> "Entropy can be computed for target app, resolution code, time of day, condition-specific
> outcomes, app category, or user-day response states."
>
> "Mutual information can estimate how strongly condition, target app, prior outcome, or
> time reduces uncertainty about opening versus dismissal... Time of day may reduce
> uncertainty if nighttime attempts are more likely to be opened than daytime attempts."

DS6 cannot use "resolution code" or "condition-specific outcomes" (no outcome variance) or
MI-toward-"opening versus dismissal" (same reason). It can use "target app," "time of day,"
and "user-day response states" (StoP's `N_t`) directly — these are the measures implemented
below.

---

## Part 2 — Entropy measures (all split by study_period)

```
H_app^(period)   = Shannon entropy (bits) of the app_name distribution within that period
                    -- reuses Stage 1's app_entropy_baseline/app_entropy_intervention directly
                       (DS5's own InT notebook did the same: "re-framed Stage 1 features",
                       not recomputed from scratch)

H_hour^(period)  = Shannon entropy (bits) of the hour_of_day distribution within that period
                    -- NOT available pre-split in Stage 1 (only pooled hour_entropy exists);
                       computed fresh here, per period

H_emp^(period)   = Shannon entropy (bits) of the BINNED daily N_t series (from StoP's
                    daily_series_long.csv). K=10 bins, same as DS5's H_emp -- but DS5 used
                    K=10 FIXED-width bins over [0,1] because X_t is bounded there. DS6's N_t
                    is an unbounded count ranging 1-333 events/day across participants, so a
                    fixed global bin range would be meaningless (FLAG InT-1). Uses K=10
                    QUANTILE bins computed per-participant on that participant's own N_t
                    values (pd.qcut, duplicates dropped when a participant has fewer than 10
                    distinct values -- effective K reported per participant, not silently
                    padded).

H_SDE^(period)   = Gaussian differential entropy bridge from StoP's sig_hat:
                    H_SDE = 0.5 * log2(2*pi*e*sig_hat^2)
                    -- same bridge equation as DS5 (paper gap, not yet formalized in the
                       conceptual paper -- same caveat DS5's InT notebook recorded)
```

**Minimum data:** inherits each period's StoP/Stage-1 eligibility — H_SDE/H_emp are NaN
wherever `sig_hat_<period>` is NaN (StoP ineligible, <7 active days); H_app/H_hour use the
Stage-1 feature table's own eligibility (effectively all 243, since app_entropy has 0.4% NaN
only).

---

## Part 3 — NeT–InT bridge: I_consec = H_app − H_trans

Same bridge relationship DS5's InT-NeT notebooks established
(`stage4_implementation_plan.md`: "InT-NeT bridge verified: r(H_app, H_trans)=0.945"), applied
per period here using NeT's (74) `H_trans_baseline`/`H_trans_intervention`. Sanity check:
`I_consec >= 0` for all participants (mutual information cannot be negative) — this exact
check caught a real bug in Structured's own NeT-InT bridge implementation (wrong marginal
distribution), so it is treated here as a mandatory gate, not a formality.

---

## Part 4 — Mutual information: does study_period reduce uncertainty about app choice?

**Pooled, not per-participant** (matching the paper's own population-level framing of MI
questions, and Structured's InT precedent of computing MI pooled while entropy stays
per-participant):

```
I(period; app) = H(app) - H(app | period)
               = H(app) - [ p(baseline)*H(app|baseline) + p(intervention)*H(app|intervention) ]
```

Computed on the full pooled event table (353,796 rows, not per-participant). Normalized
mutual information (`I / H(app)`) also reported, following Structured InT's precedent of
flagging when raw MI is inflated by class imbalance — checked here too before over-reading
the result (DS6's period split is roughly balanced, ~45%/55%, unlike Structured's severe
inbox-vs-timeline imbalance, so large inflation is not expected, but checked rather than
assumed).

---

## Part 5 — Output file structure

```
outputs/model_outputs/ds6/information_theory/
  participant_entropy_metrics.csv    # one row per participant: H_app/H_hour/H_emp/H_SDE for
                                      # BOTH periods, I_consec for both periods, study_condition
  condition_period_summary.csv       # study_condition x study_period x entropy-measure table
  net_int_bridge_check.csv           # per-participant I_consec validity check (both periods)
  mutual_information_summary.csv     # single-row: I(period;app), H(app), normalized MI
  psychosocial_entropy_correlations.csv  # entropy measures vs addiction_index_pre/self_control_index_pre
  figures/
    fig1_int_entropy_by_period.png
    fig2_int_hsde_hemp_bridge.png
    fig3_int_net_bridge_scatter.png
    fig4_int_condition_period_comparison.png
  model_run_summary.md
```

Each CSV above gets its own companion `.md` file (matching DS5 InT's precedent and the
StoP/NeT companion docs already written this session for `outputs/model_outputs/ds6/`), not
just the umbrella `model_run_summary.md`.

---

## Implementation readiness checklist

- [x] Confirmed H_out does not transfer (single-category distribution, entropy≡0) — excluded,
      not computed-and-discarded
- [x] Paper §2.5 quoted directly; every implemented measure traces to a named paper example
- [x] Period split applied consistently with StoP (73) and NeT (74), not just pooled
- [x] New MI test justified by a specific link to NeT's already-completed finding, not
      generic scope creep
- [x] NeT-InT bridge sanity check (I_consec >= 0) planned as a mandatory gate, per the
      Structured InT precedent where this exact check caught a real bug
- [x] Notebook 75 implemented and executed. Two-attempt bug fixed on the NeT-InT bridge
      (Stage-1 app_entropy, then app_from marginal both failed the I_consec>=0 gate; app_to
      marginal is correct) — 0 violations across 486 participant-periods after the fix.
      Headline 1: r(H_SDE,H_emp)=0.583/0.719 (both periods) supports the Gaussian-increment
      assumption behind StoP. Headline 2: pooled MI(study_period;app_name)=0.0003 bits, a
      genuine null that does not contradict NeT's per-participant HHI_net-volume finding
      (different quantities — see model_run_summary.md). See
      `outputs/model_outputs/ds6/information_theory/model_run_summary.md`.
