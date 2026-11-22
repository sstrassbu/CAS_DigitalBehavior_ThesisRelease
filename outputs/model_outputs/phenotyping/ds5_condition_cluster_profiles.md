# ds5_condition_cluster_profiles.csv

## What this file contains
Mean/median/std of behavioral features per within-condition cluster (Path E).
One row per within-condition cluster (across all three conditions).

## Column reference
| Column | Type | Description |
|---|---|---|
| condition | str | Experimental condition |
| within_cond_cluster | str | Cluster label (e.g. CON_C1, DEF_C2) |
| N | int | Cluster size |
| sig_hat_mean/median/std | float | Noise/diffusion parameter |
| H_emp_mean/median/std | float | Behavioral entropy |
| x_mean_mean/median/std | float | Override rate |
| H_hour_mean/median/std | float | Temporal entropy (overlay only) |
| HHI_net_mean/median/std | float | Network HHI (overlay only) |
| rho_self_mean/median/std | float | Self-loop fraction (overlay only) |

## How produced
Notebook: 104_ds5_condition_stratified_phenotype.ipynb
