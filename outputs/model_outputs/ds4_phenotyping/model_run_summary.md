# DS4 Phenotyping -- Model Run Summary

**Notebook:** `59_ds4_phenotype_exploration.ipynb`  
**Blueprint:** `outputs/reports/stage4/step2_phenotyping/ds4_phenotyping_blueprint.md`  
**Run date:** 2026-08-11

## Complete-case N: 641

## K-selection -- silhouette AND bootstrap stability for every candidate

```
k=2: silhouette=0.2267, bootstrap_jaccard=0.8822 (STABLE), sizes=[382, 259]
k=3: silhouette=0.2608, bootstrap_jaccard=0.8486 (STABLE), sizes=[200, 363, 78]
k=4: silhouette=0.2747, bootstrap_jaccard=0.6651 (not stable), sizes=[355, 68, 186, 32]
k=5: silhouette=0.2321, bootstrap_jaccard=0.7567 (STABLE), sizes=[226, 61, 232, 92, 30]
k=6: silhouette=0.2215, bootstrap_jaccard=0.7085 (not stable), sizes=[26, 179, 46, 58, 159, 173]
```

Chosen k=3 -- highest silhouette among STABLE candidates (not the raw silhouette-argmax, which was unstable here). See blueprint SS1 for this project's established stability-first selection practice.

## Stability

Bootstrap Jaccard (100 resamples): mean=0.8486 -- STABLE

## Cluster profiles (feature means)

```
   cluster   tau_hat     H_emp  fixed_point_deviation     chi_OU  rho_self    n
0        0  0.688742  1.992545               0.005185  13.884339  0.543261  200
1        1  0.631762  2.561270               0.008028   5.770066  0.752856  363
2        2  1.698516  2.645855               0.038046   5.473163  0.739653   78
```

## PCA

PC1+PC2 explained variance: 60.4%

## Demographic overlay (exploratory)

N=149; ANOVA age by cluster: F=1.564, p=0.2128

## Hierarchical clustering triangulation

ARI(k-means, hierarchical/ward, k=3) = 0.5971

## PCA loadings

```
                       PC1_loading  PC2_loading
tau_hat                      0.265        0.745
H_emp                        0.549       -0.126
fixed_point_deviation        0.425        0.444
chi_OU                      -0.544        0.334
rho_self                     0.389       -0.347
```
