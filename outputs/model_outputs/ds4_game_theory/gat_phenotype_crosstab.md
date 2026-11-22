# gat_phenotype_crosstab.csv

**Unit of observation:** 4×3 contingency table — rows = GaT phenotype, columns =
Step 2 Phase 1 cluster (0/1/2).

---

## How this file was produced

- **Sources:** `participant_gat_phenotypes.csv`, `ds4_cluster_assignments.csv`
- **Producing notebook:** `notebooks/56_ds4_game_theory.ipynb`, cell 8
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_gat_blueprint.md`

## Actual run results (2026-08-07)

```
cluster              0    1   2
gat_phenotype
adaptive_switcher    26   50  21
chronic_overrider   131   90  11
commitment_oriented  24  158  42
reward_oriented      19   65   4
```

**Chi-square: chi2=136.4, dof=6, p<0.0001** — strong, real association. Chronic
overrider is heavily concentrated in Phase 1 cluster 0 (131/232 = 56%) — the same
cluster Step 2 independently identified as highest-susceptibility (χ_OU mean 13.9 vs
~5.5 elsewhere). Two independently-built model families (GaT's rule-based phenotypes,
Step 2's feature-based clustering) converge on the same high-risk group.

## Known limitations

Correlational, not causal — this shows convergent structure, not that one phenotyping
approach "explains" the other.

## How to load

```python
import pandas as pd

ct = pd.read_csv("outputs/model_outputs/ds4_game_theory/gat_phenotype_crosstab.csv", index_col=0)
```
