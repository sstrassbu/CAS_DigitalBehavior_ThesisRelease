# DS5 Step 2 — Thesis Chapter/Section Outline

**Written:** 2026-04-20  
**Purpose:** Guide for writing up the DS5 Step 2 phenotyping findings in the thesis  
**Assumption:** This section follows Step 1 (model implementations) and precedes Step 3 (personalization)

---

## Proposed chapter structure

The DS5 phenotyping chapter should be organized around the two main findings (the two-layer structure and the condition modulation finding), with the six paths serving as evidence, not as separate equal chapters.

---
 
### Suggested section order

#### Section 1 — Purpose and scope of the phenotyping analysis

**What to include:**
- Define what "phenotyping" means in this context: using Step 1 model parameters as features for behavioral subgroup discovery
- Distinguish from confirmatory hypothesis-testing: this is exploratory discovery, not validation
- State the key questions this analysis addresses (from the Step 2 exploration plan)
- Brief mention of the dataset: DS5 (N=573 German adolescents, RCT)
- Clarify the Step 2 / Step 3 boundary: no intervention prescriptions here

**Keep concise:** 1 short paragraph or a bullet list. The reader needs orientation, not a literature review.

---

#### Section 2 — Feature space and methodology

**What to include:**
- The five model families and what feature each contributed (brief table: sig_hat, H_emp, x_mean, HHI_net, rho_self + secondary features)
- Feature independence structure: only two genuinely independent axes in StoP/InT/DyS/StM (sig_hat and H_emp); NeT adds a third axis (HHI_net, rho_self); H_out is condition-confounded
- Key redundancies to acknowledge: beta_behav = f(sig_hat); H_SDE = f(sig_hat); F_behav ≈ x_mean; I_consec = H_app − H_trans
- Analysis population: N=414 (StoP-eligible; complete on all core features)
- Algorithm choice: k-means (k-means++); silhouette + Calinski-Harabasz + Davies-Bouldin for k selection; bootstrap Jaccard stability (threshold 0.75)

**What to emphasize:** The feature independence analysis — the apparent richness of 20+ features reduces to ~3 genuinely independent dimensions before clustering begins. This should be stated clearly because it sets the right expectations.

**What to keep concise:** Skip detailed descriptions of each algorithm variant. Focus on what was actually used and why.

---

#### Section 3 — Phase 1: The dominant axis (network topology)

**What to include:**
- Global k=2 solution; Jaccard=0.995 STABLE
- Profile A (N=125, 30%): distributed network; Profile B (N=289, 70%): hub-locked
- Feature profiles: HHI_net (0.545 vs 0.978); rho_self (0.761 vs 0.992); behavioral features barely differ
- Condition distribution: χ²=1.22, p=0.545 → network phenotype cuts across conditions
- Full-sample NeT-only confirmation (Path C): ARI=0.990 → NeT features alone reproduce the split
- Within-B sub-structure (Path C): B1 pure single-app (N=260, 90%) and B2 hub-anchored (N=29, 10%)

**What to emphasize:** The dominant axis is structural (network topology), not dynamical. Most participants (70%) are hub-locked. This is the most important single finding from Phase 1.

**Where to discuss limitations:** Here — briefly note (a) short windows may compress NeT features, (b) B2 (N=29) is a small subgroup, (c) A1/A2 sub-structure is tentative.

---

#### Section 4 — Path A: The orthogonal behavioral-dynamic axis

**What to include:**
- Behavior-only clustering (no NeT features): k=3, Jaccard=0.991 STABLE
- Three behavioral types: C1 (low-noise, low-override); C2 (low-noise, high-override); C3 (high-noise, variable)
- Feature profiles table for C1/C2/C3 (sig_hat, H_emp, x_mean)
- **The central independence result: ARI(Path A vs Phase 1) = 0.020** — behavioral dynamics are nearly orthogonal to network topology
- Path F confirmation: the behavioral sub-types within Profile B match the full-sample types exactly (ARI=1.000 within B)
- Condition dependence: χ²=91.885, p<0.0001 → requires Path E treatment

**What to emphasize:** The near-zero ARI (0.020) between network structure and behavioral dynamics is the central finding. A participant's network type tells you virtually nothing about their behavioral process type.

**How to connect to Step 1:** Name each type using the theoretical vocabulary:
- C1 = "DyS-deterministic, near-tipping (StM susceptibility peak)"
- C2 = "DyS-deterministic, override-locked"
- C3 = "StoP-stochastic, noise-dominated"

**What to keep concise:** The sensitivity analysis (H_hour inclusion) can be a footnote.

---

#### Section 5 — Path F: The hierarchical joint taxonomy

**What to include:**
- Two-stage hierarchy: Stage 1 = NeT split (Phase 1); Stage 2 = behavioral sub-clustering within each profile
- Final 4-cell taxonomy: B_behav1, B_behav2, B_behav3, A_all
- Profile A reported as A_all (no stable sub-split; Jaccard=0.744 marginal)
- The critical cross-path result: ARI(Stage2-B vs Path A within B) = 1.000 — exact correspondence
- What the 4-cell taxonomy means: a joint characterization of structural context × behavioral dynamic
- Figure: hierarchy schematic with N counts and Jaccard at each node

**What to emphasize:** The ARI=1.000 within Profile B is the key result. It confirms that the behavioral phenotype structure is NeT-type-invariant not only globally but locally. The two axes are genuinely orthogonal at every level.

**What to keep concise:** The cross-path ARI comparisons table can be condensed. Report ARI(Phase F vs Path A) = 0.520 and ARI(Path F vs Path C) = 0.343 without extensive discussion.

---

#### Section 6 — Path E: Condition modulation of behavioral phenotypes

**What to include:**
- Within-condition k-means results: control (marginal), default (infeasible), reintervention (stable)
- The default condition result in detail: no stable k; all k rejected by min_cell<30
- ARI comparison: reintervention recovers Path A most closely (0.697); default = 0.000
- DyS regime finding: control 64% deterministic vs default 28.9% vs reintervention 57.8%
- Interpretation: Outcome D — default is qualitatively different, not merely distributionally shifted

**What to emphasize:** The default friction condition is the main finding here. It does not merely shift proportions — it eliminates the behavioral heterogeneity that drives the taxonomy. This is a strong finding about friction design, not just a methodological limitation.

**Critical interpretive statement to include:**
> "The behavioral phenotype taxonomy derived from Path A describes DS5 behavioral heterogeneity as it appears in a mixed-condition sample. Within the default friction condition, this heterogeneity disappears. This means the taxonomy partially captures condition-mediated behavioral states, not only stable individual differences. Any claim about stable behavioral phenotypes must acknowledge the condition qualification."

**How to connect to Step 3:** State that personalization analysis (Step 3) will need to account for condition-phenotype interactions, and that the default condition may be the least suitable design context for observing or exploiting behavioral heterogeneity.

---

#### Section 7 — Paths B and D: Complementary dimensions

**Approach:** These two paths are supporting evidence, not separate central claims. Present them as a combined "additional characterization" section.

**Path B — Friction-response diversity:**
- H_out_resid is highly correlated with x_mean (r=-0.707) → not an independent dimension
- ARI(Path B vs Path A) = 0.725 → largely recovers the behavioral taxonomy
- Key finding: B_fr3 (diverse responder) has chi_behav=45.8 — highest susceptibility, connecting friction-response diversity to the StM tipping-point concept
- Important robustness finding: even within the default condition (where clustering is infeasible), Path F cells significantly predict H_out_resid direction

**Path D — Dynamic/stochastic characterization:**
- D1 [sig_hat, H_emp, chi_behav]: k=2 forced (k=3 rejected min_cell=11)
- ARI(D1 vs Path A) = 0.560 → partial reorganization; C1+C2 collapsed into D_sde1
- The counterintuitive chi_behav ordering: C1 has highest chi_behav (56.8), C3 lowest (7.7) — low-noise near-threshold participants are closest to a phase transition
- Regime flags extend Path E: default reduces deterministic proportions by >50%
- sigma_mu_ratio confirms noise-dominance: all types have ratio>10; DS5 dynamics are diffusion-driven

**What to keep concise:** Skip the k-selection tables for Path B and D. Report the key numbers only. Use the chi_behav finding as the main narrative hook.

---

#### Section 8 — The complete phenotype framework

**What to include:**
- Present the final two-layer framework as the synthesis
- Layer 1: NeT type (condition-stable; structural context)
- Layer 2: Behavioral type (condition-modulated; dynamic response)
- Clear statement that no genuinely independent third layer was found
- Table: two-layer taxonomy with N, key feature profiles, theoretical interpretation
- Robustness summary table (Jaccard, N, condition status for each structure)

**What to emphasize:** The framework's practical meaning — a person who is hub-locked and C1-type differs from one who is hub-locked and C3-type in interpretable and potentially intervention-relevant ways. The taxonomy is not a theoretical claim — it is a data-derived description of DS5 heterogeneity.

**What to include as a limitation callout box or footnote:**
- Profile A taxonomy is tentative (N=125; Stage 2 reported as A_all)
- Psychosocial null findings across all paths
- Condition qualification on Layer 2
- All findings are DS5-specific and require DS4 replication

---

#### Section 9 — Limitations (dedicated section)

**Keep this section, do not fold into each subsection.** Consolidate the limitations here:

1. Short observation windows (7–45 days) — behavioral profiles may reflect within-study states
2. Proxy variable — X_t is not a direct measure of urge or self-control
3. Condition qualification — behavioral types are condition-mediated
4. Profile A stability — k=2 within Profile A is marginal (Jaccard=0.744)
5. Psychosocial null results — behavior clusters do not predict psychosocial outcomes in this sample
6. Cross-dataset replication not yet done
7. Sample population — German adolescents in a controlled RCT

---

## What to emphasize vs keep concise (overall guidance)

**Emphasize (spend space):**
- The independence of the two layers (ARI=0.020)
- The default condition's homogenization effect
- The chi_behav counterintuitive finding
- The ARI=1.000 confirmation (Stage 2-B vs Path A within B)
- The final four-cell taxonomy as a synthesis

**Keep concise:**
- Technical algorithm details (k-means++, bootstrap protocol) — put in appendix or methods note
- Sensitivity analyses (H_hour, 4-feature vs 3-feature runs, within-group vs full-sample scaler) — mention in footnotes only
- Path B and Path D results tables — summarize in 1–2 paragraphs each
- Cross-path ARI comparison tables — provide in supplementary; narrate the key number only in text

---

## How to connect Step 1 model families to Step 2 phenotype results

| Model family | Connection to phenotype |
|---|---|
| StoP | sig_hat backbone of Layer 2; C1/C2 = low-σ̂; C3 = high-σ̂; sigma_mu_ratio confirms noise dominance |
| InT | H_emp backbone of Layer 2 (r=0.538 with sig_hat); H_out = condition-confounded; H_hour secondary |
| DyS | is_dys_eligible = Layer 2 C1/C2 group; regime labels as narrative for behavioral type |
| StM | chi_behav = key finding (C1 has highest susceptibility despite lowest noise); F_behav framing |
| NeT | HHI_net + rho_self = entire Layer 1 taxonomy; H_trans/H_app for sub-structure within Profile B |

---

## How to describe the final phenotype framework without overclaiming

**Appropriate framing:**
> "The analysis identified two behavioral phenotype dimensions in DS5. The first is network-topological: most participants (70%) predominantly use a single app, while 30% maintain a more distributed app repertoire. The second is behavioral-dynamic: within the study period, participants varied along a noise-vs-compliance axis (three types: stable-susceptible, stable-override-locked, and noisy-variable). These two dimensions were nearly statistically independent (ARI=0.020). However, the behavioral types were substantially influenced by experimental condition assignment — a finding that limits their interpretation as stable individual traits."

**Inappropriate framing (avoid):**
- "We identified four distinct behavioral phenotypes" (overclaims stability and independence of A_all)
- "Participants belong to one of three behavioral types" (implies exclusivity and permanence)
- "These phenotypes predict intervention outcomes" (Step 3 territory; not established)
- "The hub-locked type is inherently less susceptible to friction" (causal claim not supported)

---

## Where to discuss the condition-phenotype interaction as the central interpretive tension

The most intellectually important moment in the chapter is the transition from Path A to Path E:

1. Path A finds a clean 3-type structure (good)
2. But the condition χ² is enormous (91.885, p<0.0001) — bad signal
3. Path E resolves this: the default condition *eliminates* the structure, while reintervention *preserves* it
4. **Interpretive resolution:** The behavioral types are not artifacts of the analysis, but their degree of stability depends on friction design. This is a finding about intervention design, not a methodological limitation.

Place this resolution after the Path E section. End it with the theoretical takeaway: different friction designs activate different aspects of individual heterogeneity.

---

*Written 2026-04-20 as thesis chapter planning document for the DS5 Step 2 phenotyping analysis.*
