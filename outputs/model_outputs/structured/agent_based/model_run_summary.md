# Structured ABM -- Model Run Summary

**Run date:** 2026-08-05
**Notebook:** notebooks/67_structured_agent_based.ipynb
**Blueprint:** outputs/reports/structured/structured_abm_blueprint.md

## Population
- Agent population (StoP created_is_eligible): N=43
- With Step 2 cluster_label: 36

## Model 1 (static-rate) vs Model 2 (bursty) vs real
- Real Fano:        mean=6.011, median=3.833
- Model 1 sim Fano: mean=1.019, median=1.001
- Model 2 sim Fano: mean=3.377, median=2.369
- Correlation(Fano_real, Fano_sim_model2) across agents: 0.914

**Interpretation:** Model 1 confirms the analytically expected result (Fano~1, static heterogeneity
alone cannot reproduce burstiness). Model 2's single added mechanism (session on/off, 2 extra rule
parameters) closes 47% of the gap between Model 1 and the real Fano level -- a
meaningful but partial explanation: session-based clustering alone does not fully reproduce real
burstiness, but it recovers roughly half of it from just two additional rule parameters. The much
stronger result is the RANK correlation (Fano_real vs Fano_sim_model2 across agents: r=0.914) --
the model correctly identifies WHICH agents are more/less bursty even where it undershoots the absolute
magnitude for the population as a whole.

## Phenotype mixture validation
            mean  median    std  Fano_real_mean
profile                                        
Profile A  4.598   4.575  0.597           7.491
Profile B  5.044   5.046  0.538           4.613

Real A vs B KS: stat=0.351, p=0.1896 (n=22 vs 14 -- underpowered)
Simulated A vs B KS: stat=0.375, p=6.541e-13 (n=200 vs 200)
KS STATISTIC magnitude is similar (0.351 vs 0.375) even though the
p-values look discordant (a sample-size artifact, not evidence against the model on its own).

**BUT the direction is reversed**: real ordering is A > B (7.49 vs
4.61), simulated ordering is B > A (4.60 vs 5.04).
Collapsing each profile to a single (lam, f_active) mean loses enough within-profile heterogeneity that
the 2-archetype simulation gets the separation's magnitude right but its direction wrong. This
meaningfully qualifies "dynamically plausible": individual-level calibration reproduces real burstiness
rank-order well (r=0.914), but a 2-archetype mean-rule-set simplification does not preserve
which profile is burstier -- a genuine limitation of the simplification, reported honestly rather than
reframed as a clean success.

## Design notes
- All agent rules sourced from already-fitted StoP/Stage-1/Step-2 outputs, not re-estimated from raw data
- Model 2's mean_session_length=3 days is a stated simplifying assumption, not fit per-agent
- Model 1's Fano~1 result is mathematically expected (Poisson process), run to quantify the gap, not
  presented as a surprising discovery
