# DS5 Step 2 — Systematic Phenotype Exploration Plan

**Written:** 2026-04-19
**Stage:** Stage 4, Step 2 — Phenotyping and Behavioral Subgroup Discovery
**Status:** Planning document — execution not yet started at time of writing.
**Update:** All six paths (C, A, F, E, B, D) are now complete (2026-04-18/2026-08-05). See
`outputs/reports/stage4/post_analysis/ds5_step2_master_synthesis.md` for the completed
cross-path synthesis, and the "DS5 (German Adolescents RCT)" section of `CLAUDE.md` for the
headline results of each path.

---

## 0. Why a systematic exploration plan

The initial Step 2 clustering (notebook `100_phenotype_exploration.ipynb`) produced a stable
k=2 solution dominated almost entirely by NeT features (HHI_net, rho_self). The behavioral
variability and entropy features (sig_hat, H_emp, x_mean) barely differed between profiles.

This is a finding worth taking seriously — but it is not the end of phenotyping. A single
global k-means pass answers one specific question: "what is the dominant axis of individual
difference in the joint feature space?" It does not answer:

- What is the phenotype structure if network topology is held aside?
- Are there sub-types within the dominant hub-locked profile?
- What does the phenotype structure look like separately within each experimental condition?
- Do behavioral dynamics (drift, noise, temporal spread) reveal a different grouping?
- Is the network-behavioral split better captured hierarchically?

Each path below is a distinct, theoretically motivated question. Running all of them and
comparing the resulting structures is itself the thesis contribution — not any single
clustering solution.

---

## 1. Six phenotype-analysis paths

---

### Path A — Core behavior-only phenotypes

**Central question:** What is the behavioral heterogeneity structure when network topology
is excluded?

**Features to USE:**
- `sig_hat` — noise / diffusion (StoP backbone)
- `H_emp` — behavioral entropy (InT backbone)
- `x_mean` — mean override rate
- `H_hour` — temporal spread (secondary, independent)
- `mu_hat` — behavioral drift (secondary; near-zero for most DS5, use with caution)

**Features to EXCLUDE:**
- All NeT features (HHI_net, rho_self, H_trans, H_app) — this is the entire point of Path A
- H_out — condition-confounded
- All monotone transforms (beta_behav, H_SDE, T_behav)
- All composites (F_behav, four_model_convergent)

**Analysis population:** N ≈ 414 (same StoP-eligible population as Phase 1)

**What it is likely to reveal:**
The variability (sig_hat) and behavioral entropy (H_emp) axes together define a 2D behavioral
space. If there is genuine behavioral subgroup structure beyond network topology, Path A will
find it. Expected outcomes:
- A stochastic-high vs. stochastic-low split (dominated by sig_hat / H_emp)
- Possible x_mean gradient within each group (low override vs. high override)
- Possibly weak clustering structure (Phase 1 showed sig_hat/H_emp barely differ across
  existing clusters — the subgroup signal here may be low)

**Main risks:**
- Weak or absent cluster structure (silhouette may be low after removing NeT features)
- If k=2 still emerges, it may be driven by x_mean alone
- mu_hat is near-zero for virtually all DS5 participants — likely a noise feature here

**Theoretical model families:** StoP (OU process), InT (entropy), StM (behavioral temperature)

**Value for thesis:**
- **Interpretation:** HIGH — establishes what the variability/entropy axes alone say
- **Robustness:** HIGH — confirms whether NeT features were driving or amplifying structure
- **Step 3 relevance:** MODERATE — behavior-only profiles are less specific about friction response

**Execution priority: 2nd**

---

### Path B — Intervention-sensitive phenotypes

**Central question:** Who shows variable friction outcomes, and does that variability cluster
into interpretable types?

**Features to USE (within-condition only):**
- `H_out` — friction outcome entropy (the key feature here; measures how unpredictably the
  participant responds to friction events across opened/dismissed/closed)
- `x_mean` — mean override rate (friction compliance level)
- `chi_behav` — behavioral susceptibility (StM; independent of sig_hat/H_emp via p_use)
- `sig_hat` — retain as context anchor

**Critical constraint:**
`H_out` is confounded by condition — the outcome set available to a participant depends on
whether they are in control, default, or reintervention. Path B MUST be run separately within
each condition, or using a condition-residualized version of H_out.

**Analysis structure:**
- Option B1: Run k-means within each condition (N per condition ≈ 100–140)
  - Risk: small N; unstable clusters
- Option B2: Residualize H_out on condition (OLS residuals), then run global clustering
  - More powerful; N ≈ 414; less theoretically pure

**Features to EXCLUDE:**
- All NeT features — this path is about friction response diversity, not network structure
- H_app, H_hour — secondary; not friction-response-specific

**What it is likely to reveal:**
- Participants whose friction response is highly variable (H_out high) vs. participants with
  a consistent behavioral pattern (open always, or dismiss always)
- Whether susceptibility (chi_behav) clusters with outcome variability or is orthogonal to it
- This is the path most directly relevant to "who can be influenced by friction"

**Main risks:**
- Condition confound in H_out — must handle explicitly; document choice
- chi_behav shares x_mean via p_use (partial overlap); check correlation before using together
- Small within-condition N for B1 approach

**Theoretical model families:** InT (outcome entropy), StM (susceptibility), StoP (drift as
baseline friction response direction)

**Value for thesis:**
- **Interpretation:** MODERATE — reveals response variability structure
- **Robustness:** MODERATE
- **Step 3 relevance:** HIGHEST — directly connects to personalization question; identifies
  "who can be moved"

**Execution priority: 5th** (requires careful condition handling; high Step 3 value but
premature before other paths establish the landscape)

---

### Path C — Network-structural phenotypes

**Central question:** Within the dominant hub-locked profile (Profile B, N=289), is there
meaningful sub-structure? Are there different types of hub-dominated users?

**Features to USE:**
- `HHI_net` — network flow concentration
- `rho_self` — self-loop rate (same-app repetition)
- `H_trans` — conditional transition entropy
- `H_app` — app diversity (WARNING: I_consec = H_app − H_trans; use either H_app or
  H_trans + I_consec, not all three)
- `H_pi` — stationary distribution entropy (only N=378 eligible; use where available)
- `top1_share_net` — share of dominant app (partially redundant with HHI_net; secondary)

**Features to EXCLUDE:**
- All StoP/InT/StM/DyS behavior features — this path is about network topology alone
- I_consec if H_app and H_trans are both included (it is their difference)

**Analysis population:**
- Primary: Profile B sub-clustering (N=289)
- Secondary: Profile A sub-clustering (N=125) — check for internal structure
- Full sample NeT-only clustering: N ≈ 463 (NeT-eligible) as a robustness check

**What it is likely to reveal:**
Profile B (HHI_net ≈ 0.978, rho_self ≈ 0.992) occupies the near-ceiling region of both
features. However, H_trans varies (Profile B mean H_trans = 0.032 vs. Profile A mean H_trans
= 0.789). Within Profile B, there may be sub-groups defined by:
- Single-app lockers: only one app, always the same (rho_self = 1.0, H_pi low)
- Multi-hub lock-ins: two or three apps share dominance but no diversity
- Occasional branchers: primarily hub-locked but with episodic diversification

Profile A has genuine network diversity (H_app ≈ 1.05, H_trans ≈ 0.79). Within Profile A,
sub-groups might differentiate by level of network diversity.

**Main risks:**
- Profile B features are near-ceiling — effective variance is very low; sub-clusters may be
  driven by noise
- H_pi has limited coverage (N=378 of 569); sub-analysis reduces N further
- NeT features are heavily correlated with each other (HHI_net, rho_self, top1_share_net
  all measure hub-concentration); effective dimensionality is low

**Theoretical model families:** NeT (network structure, centralization), ABM (agent topology
types), GaT (strategic network positions)

**Value for thesis:**
- **Interpretation:** PRIMARY — directly extends the dominant Phase 1 finding
- **Robustness:** HIGH — tests whether the binary hub-split is the right level of resolution
- **Step 3 relevance:** MODERATE — network type informs intervention channel but not
  urgency or susceptibility directly

**Execution priority: 1st** (most natural follow-on; high N; directly extends existing finding)

---

### Path D — Dynamic / stochastic phenotypes

**Central question:** Do participants separate into meaningful groups based on their
drift-noise structure — specifically, are there participants with systematic directional
behavioral change vs. pure noise processes?

**Features to USE:**
- `sig_hat` — noise / diffusion (OU)
- `mu_hat` — drift (OU); CAUTION: near-zero for most DS5 participants
- `sigma_mu_ratio` — impulsivity ratio; CAUTION: 31.2% NaN
- `H_emp` — empirical behavioral entropy
- `H_hour` — temporal diversity (independent; may capture circadian variability structure)
- `deviation_from_predicted_fixed_point` — DyS; how far participant is from their
  predicted OU attractor

**Features to EXCLUDE:**
- All NeT features
- x_mean — not trajectory-dynamic; use as overlay post-hoc
- chi_behav — partially derived from x_mean

**Analysis population:** N ≈ 285 (participants with both sig_hat and non-NaN sigma_mu_ratio;
reduces sample substantially)

**What it is likely to reveal:**
- High-noise vs. low-noise behavioral styles (expected; essentially splits on sig_hat)
- Possibly: a "drifter" group (participants with mu_hat ≠ 0) vs. "stable-noise" group
  (participants with mu_hat ≈ 0 and moderate sigma_mu_ratio)
- H_hour may add a temporal regularity dimension: some participants use their phone apps
  uniformly across hours; others concentrate in specific time windows

**Main risks:**
- mu_hat is near-zero for virtually all DS5 participants (study window too short for drift
  to accumulate) — this dramatically limits the discriminative power of this path
- sigma_mu_ratio NaN loss reduces sample to N ≈ 285; cluster stability will be lower
- H_hour had very small variance in Phase 1 (Profile A = 4.031, Profile B = 4.049) —
  may not be discriminative

**Theoretical model families:** StoP (OU process), DyS (deterministic vs. stochastic
regime boundary), StM (behavioral temperature as inverse diffusion)

**Value for thesis:**
- **Interpretation:** MODERATE — theoretically motivated but DS5 may lack the window length
  to reveal true drift structure; DS4 will be more informative for DyS phenotyping
- **Robustness:** LOW — expected to confirm sig_hat is the main axis again
- **Step 3 relevance:** LOW

**Execution priority: 6th** (last; lowest expected discriminative yield; save for completeness)

---

### Path E — Condition-stratified phenotypes

**Central question:** Does the phenotype structure differ across experimental conditions?
Are the behavioral profiles condition-invariant, or does friction assignment reshape the
subgroup structure?

**Features to USE:** Same as Phase 1 core (sig_hat, H_emp, x_mean, HHI_net, rho_self)
— but run separately within each condition.

**Analysis structure:**
- Control condition: N ≈ 100–140 (exact N to be confirmed from condition frequencies)
- Default friction condition: N ≈ 100–140
- Reintervention condition: N ≈ 100–140

Run k=2 and k=3 within each condition. Compare:
- Silhouette scores across conditions (does friction make subgroup structure sharper?)
- Profile means across conditions (do the same features drive separation in each condition?)
- Cross-condition ARI (are the same participants assigned together regardless of condition?)

**Key comparison:** Take full-sample Phase 1 cluster assignments. Within each condition,
how well do the Phase 1 cluster labels reproduce within-condition cluster labels? If
ARI(condition-k vs. full-sample k) is high, phenotypes are condition-invariant. If ARI
is low within the reintervention condition specifically, that would suggest friction
*creates* behavioral differentiation.

**Features to EXCLUDE:**
- H_out (condition-confounded)
- All monotone transforms and composites

**Main risks:**
- N per condition ≈ 100–140; may be too small for stable k-means
  → Use hierarchical clustering or GMM as supplementary; bootstrap stability is critical
- Small N per condition means confidence intervals on cluster profiles will be wide
- Condition assignment in DS5 is at the participant level (not within-participant) —
  so no pre/post comparison is possible; this is purely between-condition

**Theoretical model families:** Connects to the RCT experimental design; relevant to all
model families as a moderator test

**Value for thesis:**
- **Interpretation:** HIGH — directly tests whether phenotypes are trait-like or
  condition-shaped; important for the thesis claim about behavioral heterogeneity stability
- **Robustness:** HIGH — validates that Phase 1 clusters are not condition artifacts
  (Phase 1 χ² = 1.22, p = 0.545 already suggests this, but within-condition clustering
  is a deeper test)
- **Step 3 relevance:** HIGH — if phenotypes differ by condition, then condition × phenotype
  interaction is the correct Step 3 framework

**Execution priority: 4th**

---

### Path F — Hierarchical / two-stage phenotype extraction

**Central question:** Can a two-level phenotype taxonomy — first split by network structure,
then sub-typed by behavioral dynamics — reveal richer profile structure than any single
flat clustering?

**Stage 1 split:** Use HHI_net threshold (or Phase 1 cluster assignments) to divide sample
into:
- Group 1: Distributed network users (Phase 1 Profile A, N=125) — HHI_net < ~0.75
- Group 2: Hub-dominated users (Phase 1 Profile B, N=289) — HHI_net ≥ ~0.75

**Stage 2 sub-clustering within each group:**
- Use behavior-only features: sig_hat, H_emp, x_mean (+ H_hour optionally)
- Run k=2 within Group 1 and k=2,3 within Group 2
- Group 2 sub-types may reveal: noisy hub-lockers vs. quiet hub-lockers; high override
  vs. low override within hub structure

**Resulting taxonomy:** Up to 4–6 phenotype cells (2 × 2 or 2 × 3), each with a specific
behavioral signature across both network structure and behavioral dynamics.

**Features:**
- Stage 1: HHI_net, rho_self
- Stage 2 (Group 1): sig_hat, H_emp, x_mean
- Stage 2 (Group 2): sig_hat, H_emp, x_mean

**Main risks:**
- Group 1 (N=125) is small for sub-clustering; k=2 may be fragile
- Stage 1 threshold is arbitrary if not using Phase 1 cluster assignments directly
  → Safer to use Phase 1 assignments as Stage 1 split rather than a raw threshold
- Two-stage taxonomy is more complex to present; requires careful interpretation of
  whether Stage 2 splits are real or just splitting noise within small groups

**Theoretical model families:** Hierarchical structure maps onto the theory's distinction
between network-topological and dynamical-behavioral phenotype dimensions; directly relevant
to ABM (agent types defined by two orthogonal attributes) and GaT (strategies differ by
network position AND noise level)

**Value for thesis:**
- **Interpretation:** HIGH — produces the richest theoretical profile taxonomy
- **Robustness:** MODERATE — depends on stability of Stage 2 splits; bootstrap required
- **Step 3 relevance:** HIGH — the most specific initialization point for GaT and ABM

**Execution priority: 3rd** (after C and A establish the building blocks for Stage 1 and 2)

---

## 2. Execution order and rationale

| Order | Path | Rationale |
|---|---|---|
| **1st** | **C — Network-structural sub-phenotyping** | Directly extends dominant Phase 1 finding; large N within Profile B; answers the most pressing open question (is the hub-locked group homogeneous?) |
| **2nd** | **A — Core behavior-only** | Establishes what sig_hat/H_emp/x_mean structure looks like without NeT; necessary for Path F Stage 2 and as robustness baseline |
| **3rd** | **F — Hierarchical two-stage** | Builds on C and A results; produces richest taxonomy; requires both prior paths to be complete |
| **4th** | **E — Condition-stratified** | Tests whether phenotypes are condition-invariant; requires full-sample structure to be established first |
| **5th** | **B — Intervention-sensitive** | Requires condition stratification insight from E; most relevant for Step 3 but premature before landscape is established |
| **6th** | **D — Dynamic/stochastic** | Expected lowest yield in DS5 given mu_hat ≈ 0; complete for thoroughness |

---

## 3. Cross-path comparison framework

After all paths are run, compare the resulting cluster solutions using:

- **ARI (Adjusted Rand Index):** How similar are the cluster assignments across paths?
  - If ARI(Path A vs. Path C) is high, network and behavior structure are not independent
  - If ARI is low, the two feature groups are revealing orthogonal phenotype dimensions
- **Feature importance per path:** Which features drive the within-path separation?
- **Theoretical coherence:** Do the profiles from each path correspond to recognizable
  theoretical types from the paper (§4.2 and §4.3)?
- **Profile stability:** Bootstrap Jaccard ≥ 0.75 as threshold for publication-worthy claims

The primary thesis contribution is not "we found k groups" but rather:
"Behavioral phenotype structure in DS5 depends on which feature space is prioritized,
and the network-structural and behavioral-dynamics axes are partially orthogonal."

---

## 4. Output file plan

| Path | Notebook | Output cluster file | Profile file |
|---|---|---|---|
| C | `101_ds5_network_subphenotype.ipynb` | `ds5_net_subcluster_assignments.csv` | `ds5_net_subcluster_profiles.csv` |
| A | `102_ds5_behavior_only_phenotype.ipynb` | `ds5_behav_only_cluster_assignments.csv` | `ds5_behav_only_cluster_profiles.csv` |
| F | `103_ds5_hierarchical_phenotype.ipynb` | `ds5_hierarchical_assignments.csv` | `ds5_hierarchical_profiles.csv` |
| E | `104_ds5_condition_stratified_phenotype.ipynb` | `ds5_condition_cluster_assignments.csv` | `ds5_condition_cluster_profiles.csv` |
| B | `105_ds5_intervention_sensitive_phenotype.ipynb` | `ds5_intervention_cluster_assignments.csv` | `ds5_intervention_cluster_profiles.csv` |
| D | `106_ds5_dynamic_stochastic_phenotype.ipynb` | `ds5_dynamic_cluster_assignments.csv` | `ds5_dynamic_cluster_profiles.csv` |

All outputs → `outputs/model_outputs/phenotyping/`
All companion `.md` files required per output file documentation rule.

---

## 5. What success looks like for Step 2

Step 2 is complete when the thesis can make the following claims with evidence:

1. The dominant axis of individual difference in DS5 is network structure (hub-dominated vs.
   distributed) — established by Phase 1.

2. Within the hub-dominated majority, behavioral variability (sig_hat/H_emp) creates
   meaningful sub-profiles — established by Path C.

3. When network topology is held aside, behavioral dynamics reveal their own phenotype
   structure — established by Path A.

4. A two-level taxonomy (network structure × behavioral dynamics) captures the full
   heterogeneity more completely than any single-level solution — established by Path F.

5. The core phenotype structure is condition-invariant (not a friction artifact) —
   established by Path E.

6. Participants differ in their friction response variability in ways that map onto
   the behavioral phenotypes — suggested by Path B.

These six claims together constitute a substantial, methodologically grounded phenotyping
chapter.
