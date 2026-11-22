# DS5 ABM — Model Run Summary

**Run timestamp:** 2026-08-06 03:40:06
**Notebook:** notebooks/47_ds5_agent_based.ipynb
**Model:** Agent-Based Model (ABM), Step 1 — SDE agent validation
**Dataset:** DS5 — German Adolescents RCT (N=573)
**Simulation:** N_DAYS=30, RNG_SEED=42

---

## FLAG decisions

| Flag | Decision |
|---|---|
| FLAG AB1 | Agent rules = StoP SDE — not an independent structural model |
| FLAG AB2 | No agent interaction, social influence, or learning |
| FLAG AB3 | SDE boundary is clipping/censoring (not reflection); induces ~11% point mass at each of 0 and 1, which partially mimics an absorbing state |
| FLAG AB4 | Simulation validates StoP parameterization, not a new generative claim |
| FLAG AB5 | No substitution/redirect behavior (no redirect data in DS5) |

## Population

- Total eligible agents (with StoP params): 414
- With phenotype (Profile A/B): 414

## Individual agent validation (primary)

- Spearman ρ (observed vs simulated x_mean) = 0.4284
- RMSE = 0.2411
- Gate (rho ≥ 0.8): **FAIL ✗** — genuine structural limitation, not a bug

**Why the gate fails — SDE boundary ergodics:** A bounded random walk with clip-to-[0,1] converges
to an ergodic mean near 0.5 when noise σ is large relative to drift μ. Participants with observed
x_mean far from 0.5 (e.g., x_mean≈0.85) get pulled toward 0.5 in 30-day simulations regardless of
their initial state. Since DS5 participants have substantial σ_hat (median≈0.19) and small |μ_hat|
(median≈0.006), the 30-step simulation regresses to the boundary ergodic — systematically
underestimating high-x_mean participants. The StoP incremental fitting captures short-term dynamics;
30-day trajectory means are dominated by boundary behavior that the SDE does not accurately
model at longer horizons. This is an honest null finding: the SDE agent rules do NOT reproduce
individual-level trajectory means when extrapolated beyond the observation window length.

## Individual-agent simulation, grouped by profile (414 individually-parameterised agents)

| Profile | Obs mean x | Sim mean x |
|---|---|---|
| Profile A | 0.6688 | 0.5549 |
| Profile B | 0.7052 | 0.6025 |

## Archetype pool simulation (200 agents per profile, at each profile's median mu_hat/sig_hat/x0)

| Profile | Obs mean x | Archetype-pool sim mean x |
|---|---|---|
| Profile A | 0.6688 | 0.6615 |
| Profile B | 0.7052 | 0.6460 |

The two simulations disagree on direction. The individual-agent simulation preserves the
observed ordering (B > A); the archetype pool REVERSES it (A > B), because the two profiles'
median parameters are nearly identical and the pool difference is Monte-Carlo noise only
(t = 0.822, p = 0.4114).

## Phenotype archetype separation

Simulated trajectories reproduce Profile A/B separation in x_mean direction:
see fig3_abm_archetype_separation.png

## Limitations

1. FLAG AB1: SDE agent rules are not an a priori behavioral model — the ABM validates StoP, it does not independently predict from first principles
2. FLAG AB2: Real smartphone use is embedded in social and environmental contexts not captured here
3. FLAG AB3: The absorbing-state behavior at x_mean=0 or 1 is not modeled (only soft clipping)
4. FLAG AB5: Substitution (redirecting to another app) is not modeled — no DS5 redirect data
5. N_DAYS=30 may not match individual observation windows; trajectory length is standardized, not participant-specific

## Output files

| File | Description |
|---|---|
| participant_abm_summary.csv | Per-agent observed vs simulated x_mean (all eligible agents) |
| figures/fig1_abm_validation.png | Scatter + archetype pool + burstiness |
| figures/fig2_abm_condition_params.png | μ_hat and σ_hat by condition |
| figures/fig3_abm_archetype_separation.png | Phenotype separation obs vs sim |
