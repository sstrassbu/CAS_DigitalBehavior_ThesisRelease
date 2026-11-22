# participant_network_metrics.csv

## Contents
Per-participant app-transition network metrics for DS6, computed separately for the
baseline and intervention periods.

## Unit of observation
One row per participant (N=243).

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | str | Canonical participant identifier |
| `study_condition` | str | control / default / intervention |
| `n_nodes_baseline` | int | Distinct apps visited in the baseline-period transition graph |
| `M_transitions_baseline` | int | Total transitions (edges) observed in baseline |
| `is_net_eligible_baseline` | bool | True if M_transitions_baseline >= 20 (MIN_TRANSITIONS) |
| `is_stationary_eligible_baseline` | bool | True if M_transitions_baseline >= 50 AND the empirical chain converged to a valid stationary distribution |
| `HHI_net_baseline` | float | Herfindahl index of node out-degree share (hub concentration); higher = more concentrated on few apps |
| `top1_share_net_baseline` | float | Out-flow share of the single most-used app |
| `rho_self_baseline` | float | Pooled self-loop rate (same-app-to-same-app transitions / total) |
| `H_trans_baseline` | float | Entropy (bits) of the transition structure |
| `H_pi_baseline` | float | Entropy (bits) of the stationary distribution; NaN if not stationary-eligible |
| `n_nodes_intervention` ... `H_pi_intervention` | — | Same 9 metrics, intervention period |

## Production
- Source: `outputs/cleaned/ds6_behavioral_clean.csv`
- Producing notebook: `notebooks/74_ds6_network_models.ipynb`
- Blueprint: `outputs/reports/stage4/step1_modeling/ds6_net_blueprint.md`
- Stage: Stage 4, Step 1

## Cleaning / derivation steps applied
- Transitions self-derived via `shift(-1)` on rows sorted by `[participant_id_canonical, event_timestamp_utc]`, computed separately per `study_period` so transitions never cross the baseline/intervention boundary. **Deliberately NOT built from the pre-engineered `app_next` column** — verified 2026-08-06 that `app_next` mechanically echoes the current row's own app_name 99.3% of the time and does not represent a real next-app choice (see `data_docs/modeling_cautions.md` §6).
- Nodes = target apps (paper §2.4 Example A). Self-loops included (FLAG NET-2).
- Stationary distribution via power iteration (2000 max steps, convergence tolerance 1e-9); reported only where the residual is below 1e-6 and probability mass sums to >0.5, else NaN (FLAG NET-3).

## Known limitations
- Small closed app vocabulary (10 apps globally, mean 3.65/participant) likely inflates HHI_net relative to DS1/DS4 independent of any behavioral effect — flagged before running, only partly confirmed (observed HHI_net is moderate, ~0.50, not pushed to ceiling).
- Edges are temporal adjacencies between logged One Sec events, not causal substitution or the participant's complete smartphone ecology (paper §2.4 explicit caution).
- `study_condition` is quasi-experimental (cohort-level), not individually randomized.

## Load example
```python
import pandas as pd
from pathlib import Path
df = pd.read_csv(Path('outputs/model_outputs/ds6/network_models/participant_network_metrics.csv'))
```
