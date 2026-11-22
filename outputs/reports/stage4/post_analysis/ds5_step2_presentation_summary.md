# DS5 Step 2 — Presentation-Oriented Summary

**Written:** 2026-04-20  
**Purpose:** Early-stage research presentation reference — central storyline, key results, figures to show, caveats, next steps  
**Audience:** Academic research presentation (thesis committee, seminar)
 
---

## Overview of the full implementation journey

### The three-step logic of Stage 4

The Stage 4 implementation follows a deliberate three-step logic aligned with the paper's research levels:

| Step | Name | Scope | DS5 Status |
|---|---|---|---|
| **Step 1** | Theoretical and Conceptual Modeling | One CAS model family per notebook; parameter estimation; cross-condition comparison; no phenotyping | **COMPLETE** (5 model families: StoP, InT, DyS, StM, NeT) |
| **Step 2** | Phenotyping | Use Step 1 parameters as features for behavioral subgroup discovery | **COMPLETE** (Phase 1 + 6 paths: C, A, F, E, B, D) |
| **Step 3** | Personalization | Intervention matching based on phenotype profiles | Deferred |

Step 1 established what participants' behavioral processes look like through each theoretical lens. Step 2 asked whether participants differ from each other in structured ways. Step 3 will ask what those differences imply for intervention design — not yet implemented.

---

## The five Step 1 model families — what each contributed to DS5

### StoP — Stochastic Processes (notebook 43)

**Theory:** Each participant's daily app-opening behavior is modeled as a random walk: X_t+1 = X_t + μ + σ·ε, where X_t = daily override rate, μ = behavioral drift, σ = behavioral noise (diffusion).

**What DS5 showed:**
- 414/573 participants eligible (minimum 7 days of data)
- Drift μ̂ is near-zero for virtually all participants (~0.007 across conditions) — behavior is not systematically drifting within the 6-week window
- **Noise σ̂ varies by condition:** default (0.245) > reintervention (0.200) > control (0.172) — but this ordering matches each arm's binomial sampling-noise floor (0.251 / 0.212 / 0.179) and vanishes once the floor is controlled (F=0.80, p=0.450), so it is not evidence that friction disrupts behavioral regularity
- Exploratory: FoMO correlates weakly with μ̂ (r=-0.12, p=0.047) — higher FoMO slightly associated with downward behavioral drift

**Potential for project:** StoP provides the fundamental state variable X_t and its variability parameters. It is the theoretical backbone for all other model families. Most directly applicable to DS4 where long observation windows (~900 days) would allow drift detection and OU mean-reversion estimation.

**DS5 suitability:** High for behavioral baseline, moderate for drift detection (windows too short for drift accumulation).

### InT — Information Theory (notebook 45)

**Theory:** Behavioral uncertainty is characterized via Shannon entropy across multiple dimensions: H_emp (entropy of daily override rate), H_out (outcome diversity across friction events), H_app (app diversity), H_hour (temporal spread).

**What DS5 showed:**
- H_out varies strongly by condition (control=0.686, default=0.940, reintervention=0.902) — condition-confounded
- H_SDE (Gaussian entropy from σ̂) correlates with H_emp at r=0.650 — moderate support for Gaussian increment assumption
- Psychosocial (exploratory): FoMO ~ H_SDE r=-0.13; social media wellbeing ~ H_app r=0.10

**Potential for project:** InT provides a condition-free characterization of behavioral diversity (H_emp, H_hour) and a condition-sensitive one (H_out). Important for phenotyping because it measures diversity in types not captured by StoP's single-parameter noise. Critical for DS6 where session structure allows richer entropy profiling.

**DS5 suitability:** High for behavioral entropy dimensions; H_out interpretation requires careful condition control.

### DyS — Dynamical Systems (notebook 42)

**Theory:** In the σ→0 limit of the StoP model, behavior becomes deterministic. Participants with low σ̂ are "DyS-eligible" — their behavior approximates a 1D map with a stable behavioral attractor (fixed point).

**What DS5 showed:**
- σ threshold = 0.1812 (median σ̂); 207/414 (50%) DyS-eligible by construction
- **Control: 64% DyS-eligible; default: only 29%** — the default friction condition dramatically reduces deterministic behavior
- 154 participants (37.2%) are "behaviorally deterministic" (DyS-eligible AND H_emp < median)
- DyS-deterministic participants: H_emp=1.75; StoP-stochastic: H_emp=2.32 — InT confirms model selection

**Potential for project:** DyS provides vocabulary for distinguishing habit-locked (near-attractor) participants from noise-dominated participants. Most powerful for DS4 where long windows allow actual convergence to fixed points.

**DS5 suitability:** Moderate — windows may be too short for true attractor convergence, but the regime partition (deterministic vs. stochastic) is useful for phenotyping.

### StM — Statistical Mechanics (notebook 41)

**Theory:** Behavioral "temperature" T_behav = σ̂²/2 (inverse of ordering tendency); susceptibility χ_behav = β·p·(1−p) quantifies distance from a behavioral tipping point (near x_mean=0.5 + low noise = near phase transition).

**What DS5 showed:**
- β_behav ordering: control (154.8) > reintervention (123.8) > default (66.8) — friction raises behavioral temperature
- **Four-model convergence: 154 participants (37.2%)** — same as DyS behavioral determinism; closes the theoretical quadrangle
- χ_behav: reintervention (23.2) > control (18.0) > default (12.8) — reintervention participants near tipping point
- Exploratory: behavioral temperature correlates with social media wellbeing (r=0.13)

**Most counterintuitive finding:** C1 (low-noise, low-override) has chi_behav=56.8 — the HIGHEST among the three behavioral types. Low-noise participants near x_mean=0.5 are closest to a phase transition. High-noise C3 participants (chi_behav=7.7) are noise-dominated and far from a deterministic tipping point.

**Potential for project:** StM provides vocabulary for "intervention-readiness" — the chi_behav tipping-point concept identifies who might be most susceptible to a well-targeted friction nudge. Very relevant for personalization (Step 3).

**DS5 suitability:** High conceptually; the β=2/σ̂² approximation is flagged throughout (constant-drift SDE is not identical to a potential-well SDE; this is a behavioral analog, not rigorous thermodynamics).

### NeT — Network Theory (notebook 44)

**Theory:** Each participant's app-switching behavior defines a directed weighted network. HHI_net (network concentration), rho_self (self-loop rate), H_trans (transition entropy) characterize the topology.

**What DS5 showed:**
- 463/569 NeT-eligible (81.4%)
- **HHI_net is extremely high across all conditions** (0.837–0.864) — networks are heavily hub-concentrated; most participants use predominantly one app
- rho_self very high (0.922–0.924) — same-app repetition dominates
- **Bridge verified:** I_consec = H_app − H_trans (r=0.945) — mutual information between consecutive apps equals app entropy minus transition entropy
- Control has lower H_trans (0.243) than default (0.266) — friction slightly increases transition diversity

**Potential for project:** NeT is the dimension most strongly differentiating participants in DS5. It provides structural context for intervention design: hub-locked users have a different "decision landscape" than distributed-network users. Critical for DS4 (long windows allow stable network characterization). Most theoretically important for ABM (agent network types) and GaT (strategic behavior in networks).

**DS5 suitability:** Very high for network-topology phenotyping; limited by short windows for dynamic network evolution.

---

## Step 2 phenotyping — what DS5 found

### The central storyline

> DS5 behavioral heterogeneity is organized along two orthogonal dimensions. One is structural — how a participant organizes their app use across a network of apps. The other is dynamic — how variable, predictable, and compliance-oriented their behavioral process is. These two dimensions are nearly independent of each other (ARI=0.020). But only one of them survives the test of experimental condition: the structural dimension is condition-stable, while the dynamic dimension is suppressed by the default friction condition. This means that different friction designs "activate" different aspects of individual heterogeneity.

### The two-layer phenotype framework

**Layer 1 — Network topology (stable):**
- 70% of DS5 participants are hub-dominated (Profile B: HHI_net≈1, rho_self≈1)
- 30% are network-distributed (Profile A: HHI_net≈0.55)
- This split is condition-independent and entirely network-driven
- Sub-structure within Profile B: 90% pure single-app lockers (B1), 10% multi-hub anchored (B2)

**Layer 2 — Behavioral dynamics (condition-modulated):**
- Three types: C1 (stable, susceptible), C2 (stable, override-locked), C3 (noisy, variable)
- These types are completely orthogonal to network type
- They are NOT condition-invariant: default condition collapses them
- Reintervention preserves the strongest within-condition heterogeneity

---

## The strongest results for a presentation

### Result 1: Network topology dominates the feature space (Phase 1 + Path C)
- k=2 global clustering; Jaccard=0.995; ARI(NeT-only vs Phase 1)=0.990
- NeT features explain 99% of the cluster assignment variance
- **Presentation interpretation:** "The biggest individual difference in DS5 is structural — how concentrated a participant's app use is, not how variable or compliant their behavior is."

### Result 2: Behavioral dynamics are orthogonal to network type (Path A + Path F)
- Behavior-only clustering: k=3, ARI vs Phase 1 = 0.020 (near-zero)
- Within hub-locked group: behavioral sub-types have ARI=1.000 with full-sample result
- **Presentation interpretation:** "Knowing someone's network structure tells you nothing about how variable or compliant their behavioral process is, and vice versa. The two axes are genuinely independent."

### Result 3: The default friction condition collapses behavioral heterogeneity (Path E)
- Default: no stable clustering possible (all k solutions rejected)
- Control: marginal structure; Reintervention: stable structure
- DyS regime: 64% deterministic in control vs 29% in default
- **Presentation interpretation:** "Not all friction designs allow individual differences to be observed. The default friction design effectively homogenizes behavior, making behavioral phenotyping infeasible within that condition."

### Result 4: The counterintuitive chi_behav finding (Path B + Path D)
- C1 (low-noise, low-override) has chi_behav=56.8 — the highest susceptibility
- **Presentation interpretation:** "The most 'stable' behavioral type is paradoxically the most susceptible to change: low noise near x_mean=0.5 means near a tipping point, not safely away from it."

### Result 5: Friction response diversity is not an independent dimension (Path B)
- ARI(Path B vs Path A) = 0.725; r(H_out_resid, x_mean) = -0.707
- **Presentation interpretation:** "How diversely someone responds to friction is largely the same information as how often they override it — there is no separate 'response style' dimension in DS5."

---

## Most important figures to show

| Figure | What it shows | Source |
|---|---|---|
| Phase 1 cluster profiles (radar/bar) | Hub-locked vs distributed split + feature profiles | outputs/model_outputs/phenotyping/figures/fig4_cluster_profiles_radar.png |
| Path A: sig_hat × H_emp × x_mean scatter by cluster | 3 behavioral types in feature space | fig_a5_cluster_profiles.png |
| Path A: cluster assignment by condition (stacked bar) | C2=65% control, C3=72% default | fig in path A outputs |
| Path E: feature distributions by condition (violin) | Default collapses sig_hat and H_emp distributions | fig_e1_feature_distributions_by_condition.png |
| Path F: hierarchy structure (schematic) | 4-cell taxonomy with N counts and Jaccard at each node | fig_f1_hierarchy_structure.png |
| Path D: sig_hat × H_emp scatter with chi_behav contours | Counterintuitive susceptibility finding | fig_d9_stochastic_landscape.png |
| Path B: chi_behav by Path B cluster | B_fr3 chi_behav=45.8 standout | fig_b4_fullsample_cluster_profiles.png |
| Path C: B1/B2 profiles | Within-B network sub-structure | fig_c4_profileB_subcluster_profiles.png |

---

## What DS4 could mean for the models

DS4 (N=1039; naturalistic, non-experimental; observation windows up to 897 days) is fundamentally different from DS5 in three ways that matter for each model:

**StoP:** DS4's 897-day windows allow actual drift estimation. In DS5, μ̂ ≈ 0 for everyone because 6 weeks is too short. DS4 is where adaptation curves, habit formation trajectories, and OU mean-reversion can be meaningfully estimated.

**DyS:** DS4's long windows allow testing whether fixed points are truly stable over time. The DyS regime (deterministic vs stochastic) may show different proportions in naturalistic vs experimental settings.

**StM:** DS4 has no experimental condition — β_behav variation will reflect individual differences in habitual behavior, not condition assignment. The potential-well SDE (V(x)) reconstruction may be more defensible with longer time series.

**NeT:** DS4 networks will be far more stable and richer (longer windows = more transitions). Network topology findings from DS4 may replicate DS5 Layer 1 but with higher confidence in HHI estimates.

**InT:** DS4 H_hour patterns will capture real circadian structure. DS5 windows are too short for stable circadian patterns.

**Phenotyping:** DS4 is the critical replication dataset. If the two-layer structure (network topology × behavioral dynamics) replicates in DS4's naturalistic, non-RCT setting, the claim that these are stable individual-difference phenotypes becomes much stronger. If it does not replicate, DS5's structure is partly experimental.

---

## The key caveats to address in a presentation

1. **Short observation windows in DS5:** 7–45 days. Behavioral profiles may reflect within-study responses, not stable life-time traits.

2. **The condition-dependence problem:** Behavioral types (C1/C2/C3) are not condition-invariant. The default condition collapses them. Any claim about "stable behavioral phenotypes" must acknowledge this.

3. **Proxy limitation:** X_t = n_opened/n_events is a behavioral ratio, not a direct measure of urge, self-control, or psychological state. All model parameters inherit this.

4. **Psychosocial null results:** No psychosocial measure significantly distinguished behavioral phenotypes after correction. The behavioral taxonomy is not yet validated against psychological scales.

5. **DS5 is German adolescents in a controlled RCT:** Generalizability to other populations and contexts is not established.

6. **Two layers, not more:** Despite six phenotyping paths, only two genuinely independent dimensions were found. The feature-space richness of the model outputs does not translate to high-dimensional phenotypic diversity.

---

## What is completed

- Stage 0 (audit and cleaning): all 4 datasets
- Stage 1 (feature extraction): all 4 datasets
- Stage 2 (cross-dataset harmonization): complete
- Stage 3 (dataset strengths and modeling readiness): complete
- Stage 4, Step 1 (DS5 model implementations): StoP, InT, DyS, StM, NeT — complete
- Stage 4, Step 2 (DS5 phenotyping): Phase 1 + Paths C, A, F, E, B, D — complete

---

## The logical next steps after this waypoint

1. **DS4 Step 1 — StoP first** (notebook naming: 53_ds4_stochastic_processes.ipynb)
   - DS4 StoP must precede all other DS4 models (OU parameters are the dependency backbone)
   - This is the direct replication test for DS5's behavioral findings

2. **DS4 Phenotyping (Step 2)** — will test whether the two-layer structure replicates

3. **DS6** — substitution dynamics, session structure, repeated psychosocial waves — different theoretical strengths

4. **Interpretation and writing** — the DS5 Step 2 findings are rich enough to draft the behavioral phenotyping chapter now

5. **GaT / ABM on DS5** — now that phenotype types are established, agent initialization vocabulary is available for theoretical model extensions

---

*Written 2026-04-20 as presentation synthesis note for the DS5 Step 2 waypoint.*
