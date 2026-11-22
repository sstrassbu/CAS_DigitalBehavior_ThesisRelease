# path_f_joint_crosstab.csv

**Unit of observation:** 4×3 contingency table — rows = Path A′ behavior cluster
(0–3), columns = Path C′ network cluster (0–2), cells = participant counts.

---

## Actual run results (2026-08-06)

```
path_c_cluster    0    1   2
path_a_cluster
0                39  122  13
1                25   36  11
2               123  173  72
3                10   10   7
```

Expected counts under independence:

```
path_c_cluster      0      1     2
path_a_cluster
0                53.5   92.6  28.0
1                22.1   38.3  11.6
2               113.1  195.8  59.1
3                 8.3   14.4   4.3
```

Standardized residuals (|value|>2 flags a cell driving the departure from
independence):

```
path_c_cluster     0     1     2
path_a_cluster
0              -1.98  3.06 -2.83
1               0.61 -0.37 -0.17
2               0.93 -1.63  1.67
3               0.59 -1.15  1.28
```

**Behavior cluster 0** (highest-susceptibility, per Path A′'s profile) is
disproportionately over-represented in **network cluster 1** (residual +3.06) and
under-represented in **network cluster 2** (residual −2.83) — the main driver of the
significant chi-square (p<0.0001).

## How this file was produced

- **Producing notebook:** `notebooks/133_ds4_hierarchical_phenotype.ipynb`, cell 7
- **Plan:** `outputs/reports/stage4/step2_phenotyping/ds4_step2_exploration_plan.md`

## Known limitations

Same as `path_f_joint_assignments.md` — one cell has expected count 4.3 (<5).

## How to load

```python
import pandas as pd

ct = pd.read_csv("outputs/model_outputs/ds4_phenotyping/path_f_joint_crosstab.csv", index_col=0)
```
