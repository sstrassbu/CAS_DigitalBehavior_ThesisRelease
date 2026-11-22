# DS5 GaT — Model Run Summary

**Run timestamp:** 2026-08-06 03:39:26
**Notebook:** notebooks/46_ds5_game_theory.ipynb
**Model:** Game Theory (GaT), Step 1 — descriptive commitment + strategy classification
**Dataset:** DS5 — German Adolescents RCT (N=573)

---

## FLAG decisions

| Flag | Decision |
|---|---|
| FLAG G1 | commitment_score = rate_not_opened (behavioral proxy, not utility) |
| FLAG G2 | Strategy thresholds descriptive (not equilibrium-derived) |
| FLAG G3 | No observed payoffs |
| FLAG G4 | Adaptation = calendar-third change, not sequential update |

## Population

- Total participants: 573
- With phenotype (Profile A/B): 414

## Commitment score by condition

| Condition | N | Mean | Median |
|---|---|---|---|
| control | 184 | 0.236 | 0.152 |
| default | 197 | 0.471 | 0.396 |
| reintervention | 187 | 0.390 | 0.298 |

ANOVA: F=40.994, p=0.0000

## Strategy distribution

- chronic_override: 144 (25.1%)
- reward_oriented: 141 (24.6%)
- adaptive_switcher: 108 (18.8%)
- commitment_oriented: 105 (18.3%)
- mixed: 75 (13.1%)

## Commitment by phenotype

| Profile | N | Mean | Median | Cohen d vs A |
|---|---|---|---|---|
| Profile A | 125 | 0.353 | 0.304 | — |
| Profile B | 289 | 0.316 | 0.263 | 0.179 |

Welch t: t=1.627, p=0.1052

## Adaptation direction

- stable: 340 (59.3%)
- rebounding_toward_open: 184 (32.1%)
- adapting_toward_dismissal: 49 (8.6%)

## Output files

| File | Description |
|---|---|
| participant_gat_parameters.csv | Per-participant commitment score, strategy, adaptation |
| figures/fig1_gat_commitment_by_condition.png | Violin + strategy bar by condition |
| figures/fig2_gat_commitment_by_phenotype.png | Violin + strategy bar by phenotype |
| figures/fig3_gat_adaptation_by_condition.png | Temporal adaptation histogram |

## Known limitations

1. FLAG G1: commitment_score is a behavioral ratio — not a formal payoff utility measure
2. FLAG G2: Strategy thresholds (60%/30%) are interpretive; results are threshold-sensitive
3. FLAG G3: No payoff data directly observed; strategy interpretation requires theoretical framing
4. The open/dismiss decision is treated as one-dimensional; substitution (close) behavior not separately modeled
5. No sequential strategy-state model (Bayesian updating); adaptation captured as aggregate calendar-period change only
