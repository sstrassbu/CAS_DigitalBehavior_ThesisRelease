# ds5_condition_cluster_stability.csv

## What this file contains
K-selection results and bootstrap Jaccard stability for all within-condition clustering
attempts (Path E). One row per condition x scope x k combination.

## Column reference
| Column | Type | Description |
|---|---|---|
| scope | str | full_sample (all N~137-142) or profile_B (N~94-99) |
| condition | str | Experimental condition |
| k | int | Number of clusters attempted |
| silhouette | float | Mean silhouette score; NaN if rejected |
| min_cell | int | Minimum cluster size |
| jaccard_mean | float | Bootstrap Jaccard mean (100 bootstraps, 80% sample) |
| jaccard_std | float | Bootstrap Jaccard std |
| feasible | bool | True if Jaccard >= 0.60 and min_cell >= 30 |
| selected | bool | True if this k was selected as the best for this condition/scope |

## Stability thresholds
- Jaccard >= 0.75: STABLE
- 0.60-0.75: MARGINAL
- < 0.60: UNSTABLE
- min_cell < 30: REJECTED regardless of Jaccard
