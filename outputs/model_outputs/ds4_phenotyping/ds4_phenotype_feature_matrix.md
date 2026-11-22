# ds4_phenotype_feature_matrix.csv

**Unit of observation:** one row per complete-case DS4 participant (641 of 1,039 —
valid across StoP, InT, DyS, StM, and NeT-eligible simultaneously).

**Model:** DS4 Stage 4 Step 2, Phase 1 — a single curated-feature clustering pass.

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `participant_id_canonical` | string | Participant identifier |
| `tau_hat` | float | StoP relaxation time (days) — raw, not standardized |
| `H_emp` | float | InT empirical binned entropy of daily X_t |
| `fixed_point_deviation` | float | DyS all-days-vs-fitted-pair-days mean gap (\|x_mean_raw − mu_hat_OU\|) — a coverage/estimation-noise diagnostic, NOT model-fit quality (r=−0.569 with pair-day coverage) |
| `chi_OU` | float | StM susceptibility |
| `rho_self` | float | NeT self-transition rate (attempts-only, top-20+'other' encoded — includes 'other'->'other' pairs; inflated by >0.05 for 57/950 eligible participants) |
| `cluster` | int | Cluster label, 0/1/2 (k=3, chosen via stability-first selection — see below) |

Note: values in this file are the **raw** (unstandardized) feature values joined to the
final cluster label. Clustering itself was performed on z-scored versions of these 5
columns (`StandardScaler`) — not exported separately, since they're a deterministic
transform of this file's own columns.

---

## How this file was produced

- **Sources:** all 5 DS4 Step 1 model outputs (`ds4_stochastic_processes`,
  `ds4_information_theory`, `ds4_dynamical_systems`, `ds4_statistical_mechanics`,
  `ds4_network_models`)
- **Producing notebook:** `notebooks/59_ds4_phenotype_exploration.ipynb`
- **Generator script:** `notebooks/make_59_ds4_phenotype.py`
- **Blueprint:** `outputs/reports/stage4/step2_phenotyping/ds4_phenotyping_blueprint.md`

## K-selection — real methodological correction made during implementation

The blueprint's FLAG 3 said "silhouette-based k selection." Running it literally would
have picked **k=4** (highest silhouette, 0.2747) — but k=4's bootstrap Jaccard stability
was **0.665, NOT STABLE** (below this project's established 0.75 threshold). Rather than
ship an unstable "best-silhouette" solution, every candidate k (2–6) was checked for
**both** silhouette and bootstrap stability:

```
k=2: silhouette=0.2267, bootstrap_jaccard=0.8822 (STABLE), sizes=[382, 259]
k=3: silhouette=0.2608, bootstrap_jaccard=0.8486 (STABLE), sizes=[200, 363, 78]
k=4: silhouette=0.2747, bootstrap_jaccard=0.6651 (not stable), sizes=[355, 68, 186, 32]
k=5: silhouette=0.2321, bootstrap_jaccard=0.7567 (STABLE), sizes=[226, 61, 232, 92, 30]
k=6: silhouette=0.2215, bootstrap_jaccard=0.7085 (not stable), sizes=[26, 179, 46, 58, 159, 173]
```

**k=3 chosen** — highest silhouette (0.2608) among the STABLE candidates (2, 3, 5), not
the raw silhouette-argmax. This matches this project's established practice (DS5,
Structured) of preferring a bootstrap-stable solution over a marginally-higher-silhouette
unstable one.

**Scope of the stability claim — preprocessing sensitivity not covered by the bootstrap.**
The bootstrap Jaccard establishes stability under *resampling only*. Three of the five
features are heavy-tailed (skew/excess-kurtosis: `tau_hat` 2.83/15.25,
`fixed_point_deviation` 3.60/16.93, `chi_OU` 1.91/5.23) and are z-scored without any
transform, winsorization or outlier screen, so k-means' squared-Euclidean objective
remains tail-sensitive. Refitting the identical k=3 pipeline with only the preprocessing
changed gives ARI against the shipped labels of **0.903** (1st/99th-percentile
winsorization), **0.689** (log1p on the three skewed features) and **0.272** (rank-to-
normal quantile transform). Cluster 2 (n=78) is the least robust component: it is defined
by the two most extreme-tailed features (highest `tau_hat` 1.699, highest
`fixed_point_deviation` 0.038) and contains 11 of the 17 participants with any |z|>4.
Read the k=3 solution as resampling-stable but preprocessing-dependent, and treat the
third phenotype in particular as provisional. Path A′ inherits the same dependence
(ARI vs. its own shipped k=4 labels: 0.242 quantile, 0.593 log1p), and every downstream
number keyed to these labels (Path A′ ARI=0.664, Path C′ ARI=0.047, Path F′ chi2=31.44)
inherits it too.

## Actual run results (2026-08-06)

| Cluster | N | tau_hat (mean) | H_emp (mean) | fixed_point_deviation (mean) | chi_OU (mean) | rho_self (mean) |
|---|---|---|---|---|---|---|
| 0 | 200 | 0.689 | 1.993 | 0.005 | 13.884 | 0.543 |
| 1 | 363 | 0.632 | 2.561 | 0.008 | 5.770 | 0.753 |
| 2 | 78 | 1.699 | 2.646 | 0.038 | 5.473 | 0.740 |

PCA: PC1+PC2 = 60.4% of variance (5 genuinely contributing dimensions, not 1–2 dominant
axes hiding behind 5 labels — consistent with the pre-registered redundancy check, which
found no feature pair correlated above \|r\|=0.483). PCA loadings: PC1 is mainly
`H_emp` (0.549) vs. `chi_OU` (−0.544) pulling opposite directions; PC2 is mainly
`tau_hat` (0.745) with `fixed_point_deviation` (0.444) — i.e. PC1 separates
high-entropy/low-susceptibility from low-entropy/high-susceptibility participants, PC2
separates slow-relaxation participants from the rest.

**Hierarchical clustering (ward) triangulation:** `ARI(k-means, hierarchical, k=3) =
0.597` — moderate agreement, real but not near-perfect; the k=3 structure is not purely
a k-means artifact, but the two methods don't fully coincide either.

**Radar chart:** `figures/fig5_ds4_phenotype_radar.png` — 3-panel radar (one per
cluster) across the same 5 features, model-family-colored axis arcs and conceptual-layer
bands. Plotting machinery adapted directly from
`notebooks/108_ds5_balanced_profile_radar.ipynb` (structural reuse only — the
normalization/arc-drawing/IQR-band code is generic; DS4's own 5 features and 3 clusters
are supplied, not DS5's content). Rendered cleanly on the first pass, no legend
collisions (DS5's and Structured's own versions of this chart needed layout iteration
before reaching this point — DS4's reused the already-fixed machinery).

## Known limitations

- **Complete-case N=641/1,039 (61.7%)** — inherits the same attrition-confound caveat as
  every DS4 Step 1 notebook (long-window survivors vs. short-window dropouts).
- No experimental condition — clusters describe naturalistic heterogeneity, not a
  friction-response typology (unlike DS5's condition-stratified Step 2 paths).
- `tau_hat` and `chi_OU` inherit StoP's daily/weekly timescale ambiguity — these
  clusters describe daily-timescale dynamics specifically.
- This is a Phase 1 pass only. Whether further exploration paths are warranted is an
  open decision, not resolved by this file alone.

## How to load

```python
import pandas as pd

phenotypes = pd.read_csv("outputs/model_outputs/ds4_phenotyping/ds4_phenotype_feature_matrix.csv")
```
