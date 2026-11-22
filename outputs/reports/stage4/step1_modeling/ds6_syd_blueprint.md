# DS6 — System Dynamics (SyD) Blueprint

**Notebook:** `notebooks/78_ds6_system_dynamics.ipynb`
**Written:** 2026-08-06
**Position:** 78 in the DS6 70s decade. Depends on StoP (73, mean_N/mu_hat) and DyS (72,
regime labels), both complete. Uses DS6's repeated psychosocial survey waves — the specific
reason SyD was deferred *from DS5 to DS6* in the first place
(`stage4_implementation_plan.md`: "SyD (48): defer to DS6 — requires repeated survey
waves").
**Depends on:** `outputs/model_outputs/ds6/stochastic_processes/participant_stop_parameters.csv`,
`outputs/model_outputs/ds6/dynamical_systems/participant_regime_classification.csv`,
`outputs/features/ds6/ds6_prepost_features.csv`, `outputs/features/ds6/ds6_survey_features.csv`
**Output root:** `outputs/model_outputs/ds6/system_dynamics/`

---

## Part 0 — Non-redundancy check (done before any code, per Structured SyD precedent)

`structured_syd_blueprint.md` opened with an explicit check that its backlog stock wasn't a
re-description of what NeT/StoP/DyS already computed. Same check here:

- StoP (73): daily attempt-count drift/diffusion/burstiness, per period. Purely behavioral,
  event-log-derived.
- NeT (74): app-transition network structure, per period. Purely behavioral.
- InT (75): entropy of app/hour/count distributions, per period. Purely behavioral.
- DyS (72): deterministic-regime classification from StoP's parameters. Purely behavioral.

**None of the four touch the psychosocial survey data as anything other than an exploratory
correlation target** (each notebook ran ~10-14 uncorrected correlations against
`addiction_index_pre`/`self_control_index_pre`, all near-null). None treats a psychosocial
score as a **stock** that accumulates/depletes, and none tests whether behavioral flows
predict psychosocial **change** (only static wave-1 levels were ever correlated). SyD is the
first DS6 notebook to use `addiction_index_change`/`self_control_index_change` (from
`ds6_prepost_features.csv`) as a formal stock-flow quantity. Confirmed non-redundant.

---

## Part 1 — Theory grounding (paper §2.8, quoted directly)

> "Stocks may include habit strength, accumulated successful dismissals, accumulated
> overrides, **app-use pressure**, intervention exposure, and disengagement."
>
> "...Successful dismissals decrease the stock or increase a **competing stock of
> self-regulation**."

DS6 cannot use "accumulated successful dismissals" or "accumulated overrides" (no outcome
variance — same limitation carried through every DS6 Step 1 notebook). Uses the paper's
other two explicitly-named stocks, which DS6's survey data operationalizes directly:

```
Stock 1 — "app-use pressure":     addiction_index   (wave 1 = baseline level, wave 2 = post level)
Stock 2 — "self-regulation":      self_control_index (wave 1 = baseline level, wave 2 = post level)
Net flow over the study window:   addiction_index_change, self_control_index_change
                                   (already computed in ds6_prepost_features.csv, N=188)
```

**Behavioral flow inputs** (from StoP/DyS, the paper's "attempts" flow): `mean_N_baseline`,
`mu_hat_baseline`, `volume_change` (= mean_N_intervention − mean_N_baseline, StoP/NeT's own
bridge quantity), and DyS's `regime_baseline`/`regime_intervention` labels.

---

## Part 2 — Two feedback-loop hypotheses (paper-grounded, both testable, neither assumed)

**Loop 1 — "pressure reinforcement":** higher baseline attempt volume/drift feeds the
app-use-pressure stock, predicting a WORSE (more positive) `addiction_index_change`.

**Loop 2 — "self-regulation correction":** a larger behavioral volume REDUCTION
(`volume_change`, typically negative per StoP's own headline finding) feeds the
self-regulation stock, predicting a BETTER (more positive, since positive =
improvement per the sign convention already fixed in `ds6_prepost_features.csv`)
`self_control_index_change`.

Both are named directly by the paper's own text (habit-reinforcement vs. self-regulation
competing stocks) — not invented framings.

---

## Part 3 — Regression-to-the-mean caution (DS6's analog of Structured's demeaning lesson)

Structured's SyD notebook found a pooled feedback-loop correlation (r=0.95) that was almost
entirely a between-participant volume confound, resolved only by person-demeaning
(`stage4_implementation_plan.md` / project memory: "always compute a within-participant
version before trusting any pooled cross-sectional-looking correlation on panel data").

DS6 has only 2 survey waves per participant, not a weekly panel — person-demeaning in
Structured's sense does not apply the same way (a 2-point series demeaned is just the change
score, which `addiction_index_change` already is). But an analogous confound exists here:
**participants with more extreme baseline psychosocial scores mechanically show more
"change" via regression to the mean**, independent of any real feedback loop. Required
check, applied before trusting either loop's raw correlation: compute BOTH the raw
Pearson correlation (behavioral flow vs. change score) AND the partial correlation
controlling for the corresponding baseline level (`addiction_index_pre` /
`self_control_index_pre`). Only the partial (baseline-adjusted) result is treated as
evidence for or against a loop; the raw correlation is reported for transparency but
explicitly flagged as confoundable.

---

## Part 4 — Output file structure

```
outputs/model_outputs/ds6/system_dynamics/
  participant_stock_flow.csv       # one row per participant (N=188, prepost-eligible):
                                    # addiction_index_{pre,post,change}, self_control_index_{pre,post,change},
                                    # mean_N_baseline, mu_hat_baseline, volume_change,
                                    # regime_baseline, regime_intervention, study_condition
  feedback_loop_tests.csv          # 3 rows (Loop 1 tested with two flow variables,
                                    # Loop 2 with one): raw r/p, partial r/p
                                    # (controlling for baseline level), n
  regime_stock_summary.csv         # mean addiction/self_control change by DyS regime_baseline
  condition_stock_summary.csv      # mean addiction/self_control change by study_condition
  figures/
    fig1_syd_loop1_scatter.png
    fig2_syd_loop2_scatter.png
    fig3_syd_regime_stock_comparison.png
    fig4_syd_raw_vs_partial_correlation.png
  model_run_summary.md
```

Each CSV gets its own companion `.md` file, per the documentation convention established
2026-08-06 and recorded as the standing default for all future DS6 model_outputs.

---

## Implementation readiness checklist

- [x] Non-redundancy check done first (Part 0) — confirmed no prior DS6 notebook used
      psychosocial CHANGE as a stock
- [x] Paper §2.8 quoted directly; both stocks (app-use pressure, self-regulation) are
      paper-named, not invented
- [x] Two loop hypotheses stated before running, both paper-grounded
- [x] Regression-to-the-mean confound identified as DS6's analog of Structured's
      demeaning lesson, with a concrete mitigation (partial correlation) planned in advance
- [x] Notebook 78 implemented and executed. **Both feedback loops are genuine null
      results**, before and after the regression-to-the-mean partial-correlation control
      (Loop 1 partial r=0.057 p=0.45 / r=-0.111 p=0.14; Loop 2 partial r=0.093 p=0.22;
      condition ANOVA F=1.225 p=0.296). Reported honestly as null, not reframed —
      consistent with the mostly-null psychosocial pattern across every other DS6 Step 1
      notebook. See `outputs/model_outputs/ds6/system_dynamics/model_run_summary.md`.
