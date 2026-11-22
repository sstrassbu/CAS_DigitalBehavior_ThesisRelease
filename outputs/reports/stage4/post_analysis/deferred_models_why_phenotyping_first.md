# Deferred Models — Why Phenotyping Comes First

**Written:** 2026-04-18  
**Purpose:** Persistent reasoning record explaining why GaT, ABM, and SyD remain deferred
while phenotyping (Step 2) is the correct next move. Documents the reasoning for each model,
explains how phenotyping enables the deferred models, and reconstructs the learning curve
that led to this conclusion — including that this was not the original plan.

---

## 1. The three deferred models and their status

At the close of DS5 Step 1, three model families were formally deferred:

| Notebook | Model | Status | Deferred since |
|---|---|---|---|
| `46_ds5_game_theory.ipynb` | GaT — Game Theory | Deferred: awaiting behavioral profiles | 2026-04-17 |
| `47_ds5_agent_based.ipynb` | ABM — Agent-Based Modeling | Deferred: requires prior model characterization | 2026-04-17 |
| `48_ds5_system_dynamics.ipynb` | SyD — System Dynamics | Deferred to DS6: structural data requirement | 2026-04-17 |

These three models share only their deferred status. The reasons are entirely different and
must be understood separately.

---

## 2. SyD — System Dynamics: deferred for a structural data reason

### Why deferred

System Dynamics models behavior as a feedback loop structure connecting stocks and flows —
for example, the cycle: boredom → app opening → short-term relief → reduced concentration
→ increased boredom. This requires repeated within-person survey measurements to observe
how stocks (boredom, fatigue, self-control) change over time and whether flows (app openings)
respond to these changes.

DS5 has only **two survey measurement points**: pre-intervention and post-intervention
(approximately 4–6 weeks apart). This is insufficient to identify a feedback loop structure.
The SyD framework needs at least 3–4 measurement waves per person, preferably with high
temporal resolution (daily or weekly psychological state measures alongside behavioral logs).

**DS6 (Danish adolescents)** has a repeated survey structure across the study period
(`survey_nr` waves 1 and 2; `survey_nr_fact`). This makes DS6 the structurally correct
target for SyD — the feedback loop between psychosocial state (addiction_index, trivsel,
self_control_index) and behavioral response (event_rate_ratio) can be traced across waves.

### Does phenotyping help SyD?

Indirectly. Phenotyping on DS5 will establish the behavioral dimensions (e.g., noise-dominated
vs. habit-stable; hub-concentrated vs. distributed) that should be included as boundary
conditions in the SyD stock-flow model. When SyD is implemented on DS6, the question will be:
"do the feedback loops look different for high-sig_hat vs low-sig_hat participants (identified
in DS5 Step 2)?" Phenotype profiles become the entry point for SyD heterogeneity analysis.

### When SyD can proceed

After DS4 and DS5 Steps 2 and 3 are complete, and DS6 implementation begins. SyD's
position in the DS6 notebook queue is DS6 notebook 68 or 78 (to be determined when DS6
Step 1 planning begins). It cannot proceed before then.

---

## 3. GaT — Game Theory: deferred because it requires payoff heterogeneity

### Why deferred

Game Theory models smartphone use as a strategic conflict between two competing goals:
short-term reward (the immediate gratification of opening an app) and long-term self-regulation
(the goal of reducing problematic use). Friction shifts the payoff structure — it increases
the time cost of the "distraction" option.

A pure theoretical formulation can always be written without data. The conceptual case for GaT
is already made in the paper (§4.2.6). The problem is **operationalization**: to make GaT
empirically grounded rather than purely illustrative, you need to know what the payoff
structure looks like for different users. Specifically:

1. **Who are the stable self-regulators?** These users consistently refuse to open despite
   friction. Their "payoff" for the long-term goal is high. Without knowing who they are,
   the game cannot be parameterized.

2. **Who are the chronic over-riders?** These users open despite friction almost every time.
   Their "payoff" for immediate gratification dominates. Without knowing who they are, the
   equilibrium analysis cannot be made user-specific.

3. **Who are the adaptive learners?** These users change their strategy over repeated
   exposures to friction. Their game-theoretic equilibrium shifts over time. This is the
   most theoretically interesting case — and it is invisible without knowing individuals'
   behavioral trajectories.

**The payoff structure cannot be estimated without first characterizing behavioral types.**
If you apply a generic payoff function to all 573 DS5 participants, you get an average
equilibrium that says nothing about the heterogeneity the paper is specifically trying
to address. GaT is only scientifically valuable when it is applied to identified subgroups
with meaningfully different payoff structures.

### How phenotyping enables GaT

Step 2 will identify phenotype profiles — for example:

- Profile A: low sig_hat, high rho_self, low x_mean → likely stable self-regulators with
  a strong long-term goal orientation. GaT prediction: strong preference for cooperating
  with friction; equilibrium favors the long-term goal.

- Profile B: high sig_hat, high x_mean, high HHI_net → likely chronic over-riders with a
  hub-dependent app ecology. GaT prediction: payoff for distraction dominates; equilibrium
  favors repeated defection against self-regulation.

- Profile C: high chi_behav, moderate x_mean → participants near the behavioral tipping
  point. GaT prediction: unstable equilibrium; payoff is nearly indifferent; friction may
  flip equilibrium with small payoff changes (most responsive group).

With these profiles identified, GaT becomes a **within-phenotype equilibrium analysis**:
"given that Profile B participants have these behavioral characteristics, what friction-payoff
manipulation would shift their equilibrium toward cooperation?" This is a scientifically
precise and useful question. Without the profiles, GaT would only be able to answer the
average-treatment-effects question — which is precisely what the paper says existing research
already does and does insufficiently.

### When GaT can proceed

After DS5 Step 2 cluster assignments are complete and stable. GaT will use the cluster
labels as agent-type definitions. Notebook 46 will then implement payoff matrices and
equilibrium analysis for each cluster separately, rather than for all participants pooled.

---

## 4. ABM — Agent-Based Modeling: deferred because it requires characterized agent parameters

### Why deferred

Agent-Based Modeling simulates a population of heterogeneous agents, each with specific
behavioral rules, interacting in a shared environment. For this project, the primary ABM
formulation is user-level: each agent corresponds to one DS5 participant with specific
attributes — impulsivity, self-control, reward sensitivity, friction responsiveness.

The model then simulates repeated friction-interaction rounds and asks: "what population-level
response distribution emerges from these heterogeneous agents?" The key advantage of ABM
over simpler models is that it can show how average treatment effects mask distributional
effects — some agents may improve strongly while others worsen, producing moderate averages
with wide variance.

The problem: **ABM requires knowing what the agent parameter distributions look like.** You
cannot write an ABM without specifying:

- The range of impulsivity parameters across agents
- The distribution of self-control tendencies
- The types of friction-response rules agents follow
- How different rule-types are distributed in the population

None of these can be estimated from the behavioral data alone without first characterizing
individuals' behavioral profiles through a model family. Before Step 1, we had raw behavioral
counts. After Step 1, we have model-derived parameters (sig_hat, H_emp, chi_behav, HHI_net)
that begin to characterize agent-level attributes. But Step 1 produces continuous parameters,
not discrete agent types. ABM needs types.

**Step 2 phenotyping provides exactly the agent-type distributions ABM needs.** Once
Step 2 identifies, say, 3–4 behavioral profiles with their relative population frequencies
and characteristic parameter values, those profiles become the ABM agent types. For example:

- Agent Type 1 (Profile A — habit-stable, low-noise): sig_hat ≈ 0.13, H_emp ≈ 1.6, x_mean ≈ 0.6.
  Rule: high persistence; friction has minimal effect on short-term behavior; long-run
  stability high.

- Agent Type 2 (Profile B — noise-dominated, hub-dependent): sig_hat ≈ 0.27, H_emp ≈ 2.4,
  x_mean ≈ 0.75. Rule: high impulsivity; responds strongly to friction in the short term
  but reverts; high volatility.

- Agent Type 3 (Profile C — susceptible, near tipping point): sig_hat ≈ 0.20, H_emp ≈ 2.0,
  x_mean ≈ 0.55, chi_behav high. Rule: near-indifferent; small friction changes flip behavior;
  most responsive to payoff manipulation.

Without Step 2, ABM would need to invent these types ad hoc, which would make the
simulation a theoretical illustration rather than a data-grounded model.

### A further dependency: ABM benefits from StoP + NeT parameter calibration

Even after phenotype profiles are identified, the ABM agent rules should be calibrated against
observed behavioral dynamics. The StoP-derived drift and diffusion parameters (mu_hat, sig_hat)
can be used to set agent behavioral update rules. The NeT transition matrix T_{ij} can be used
to set agent app-switching rules. This calibration requires the full Step 1 parameter output,
not just phenotype labels — ABM is downstream of both Step 1 and Step 2.

### When ABM can proceed

After DS5 Step 2 is complete and cluster profiles are stable. Notebook 47 will define agent
types from Step 2 cluster profiles, calibrate agent parameters from Step 1 model outputs,
and simulate the population-level response distribution. This is the most complex DS5 notebook
and appropriately comes last.

---

## 5. Why phenotyping now is the correct next move

### 5.1 The logical prerequisite structure

The full DS5 Step 1 → Step 2 → Step 3 → GaT/ABM dependency chain is:

```
StoP → InT → DyS → StM → NeT     (Step 1: model parameters)
                              ↓
             100_phenotype_exploration.ipynb    (Step 2: behavioral profiles)
                              ↓
            200_personalization_exploration.ipynb    (Step 3: intervention fitting)
                              ↓
              46_ds5_game_theory.ipynb    (GaT: within-phenotype equilibria)
              47_ds5_agent_based.ipynb    (ABM: agent types from profiles)
```

GaT and ABM are the most theoretically ambitious model families in the paper — and they are
the ones that most directly address the paper's core research question: "Can CAS frameworks
model and predict the non-linear outcomes of behavioral change interventions and through that
help characterize users by digital behavior?"

Attempting GaT or ABM before Step 2 would mean applying them to an undifferentiated population.
The result would be an average treatment effect — exactly what the paper says existing research
already provides insufficiently.

### 5.2 What phenotyping unlocks that Step 1 alone cannot

Step 1 produces a rich but continuous parameter space: sig_hat, H_emp, x_mean, chi_behav,
HHI_net, rho_self. These are valuable but they describe individual positions on dimensions,
not behavioral archetypes. The paper's contribution relies on being able to say:

"We identified three (or four) behaviorally distinct profiles in DS5. Profile B (noise-dominated,
hub-dependent over-riders) does not benefit from mild friction but shows stronger response
to reintervention design. Profile A (habit-stable, low-entropy) shows minimal friction
sensitivity across all conditions. This differential responsiveness would be invisible in
average treatment effect analyses."

This statement requires Step 2 cluster labels. Step 1 alone cannot generate it.

### 5.3 The completeness argument

At the close of NeT, the DS5 Step 1 feature space is complete — all five active model
families have been implemented. GaT, ABM, and SyD have been formally deferred. This is
the moment the Stage 4 plan designated for Step 2. Proceeding now is not early — it is
on schedule.

---

## 6. The learning curve — how this sequence was discovered, not pre-planned

### 6.1 What the original plan said

The original Stage 4 planning document (`stage4_implementation_plan.md`, written 2026-04-16)
established the model family ordering but did not yet specify the full Step 2 dependency
structure for GaT and ABM. The original deferrals were:

- GaT: "Deferred — awaiting behavioral profiles from Step 2"
- ABM: "Deferred — requires prior model characterization"
- SyD: "Deferred to DS6 — requires repeated survey waves"

These notes were written before any Step 1 notebook was complete. They were *expected* to
be true based on prior theoretical reasoning — but they had not yet been tested against
actual Step 1 outputs.

### 6.2 What Step 1 revealed

As Step 1 progressed through five notebooks (StoP → InT → DyS → StM → NeT), three things
became increasingly clear:

**First:** The four-model cluster summary (`ds5_four_model_cluster_summary.md`) confirmed
that the StoP↔InT↔DyS↔StM models effectively describe the same two underlying behavioral
axes (sig_hat and H_emp). This was known theoretically but became vivid empirically when
the four-model convergence count (154 participants, 37.2%) matched the DyS behavioral
determinism count exactly. The feature space appeared rich but was less independent than it
looked. This immediately raised the question: "is a 5-dimensional clustering space actually
feasible here, or are we clustering noise?" The answer requires seeing the data — which means
Step 2 must come first to diagnose the actual dimensional structure before GaT or ABM can
reasonably specify their agent types.

**Second:** The NeT results showed that app-transition networks in DS5 are extremely
hub-concentrated (HHI_net ≈ 0.84–0.86) and dominated by self-loops (rho_self ≈ 0.92). This
is a structural finding, not just a nuisance. It means that the DS5 behavioral space is
narrower than the theoretical frameworks imply — users mostly repeat the same app and occasionally
switch. This constrains what GaT payoff matrices can look like (the effective choice set is
small) and what ABM transition rules should encode (high self-repetition dominates). Both
insights improve GaT and ABM design — but they only emerge from reading the NeT output
first.

**Third:** The psychosocial correlation results across all five Step 1 notebooks were
consistently small but non-zero (r = 0.10–0.15 range). This tells us that model parameters
individually are weak predictors of psychosocial outcomes — which is expected. The implicit
message is that combinations of parameters (i.e., profiles) may produce stronger and more
interpretable associations. Step 2's psychosocial overlay analysis is the direct test of
this hypothesis.

### 6.3 The emergent insight: the models form a feature space, not a typology

The most important learning from Step 1 was not any single result. It was the realization
that running five model families on the same participants produces a **multi-dimensional
feature space**, not a set of five independent model conclusions. This insight is explicit
in `ds5_four_model_cluster_summary.md` §5:

> "The theoretical value of the cluster is precisely that it shows how the same behavioral
> signal (daily override variance and entropy) can be framed productively in four different
> scientific languages."

Once you see the models as different theoretical lenses on shared behavioral data — rather
than as separate analyses — the next logical step is to characterize the structure of that
shared data. That is exactly what Step 2 does. Step 1 named the dimensions; Step 2 discovers
whether meaningful regions exist in that dimensional space.

This insight was not in the original plan. The original plan said "run five models, then
phenotype." What emerged from running the five models was a sharper understanding of *why*
phenotyping is the necessary next step, rather than jumping to GaT or ABM directly.

### 6.4 The learning this creates for the paper

This discovery has direct value for the paper. The paper's §4.4 (Conclusion on Conceptual
Application and Feasibility) states:

> "The reviewed models support phenotyping not because they directly produce one final
> typology, but because they provide recurring dimensions along which users may differ."

This is exactly right — and Step 1 confirms it empirically. The five models converge on
a small number of genuinely independent behavioral axes (primarily sig_hat, H_emp, and the
NeT metrics), and Step 2 is where the structure of those axes is explored.

The paper can therefore make a more precise claim than "we applied five models":
"The five CAS model families, when applied to DS5, reduce to approximately 4–5 independent
behavioral dimensions. These dimensions form the basis for phenotype discovery (Step 2) and
provide theoretically motivated feature inputs that generic machine-learning clustering would
lack. The multi-model characterization is not redundant — each model family contributes
distinct dimensional content while sharing a common behavioral substrate."

### 6.5 What was not anticipated — and what it teaches

The original Step 1 plan did not anticipate the extent of **mathematical redundancy** between
the four-model cluster. The discovery that β_behav = 2/σ̂² and H_SDE = f(σ̂) meant that
the four-model quadrangle's apparent richness reduces to two genuinely independent empirical
axes. This is documented as an honest finding, not hidden.

The lesson: **running all model families before phenotyping is the correct order, not because
it was planned that way, but because you cannot know which features are redundant until you
have computed all of them.** Starting Step 2 after only StoP and InT (which would have been
possible technically) would have produced a feature space that was either incomplete (missing
NeT's genuinely new dimensions) or one where the redundancy structure was not yet visible.

This is a methodological lesson for the paper: the multi-model framework's value lies not
only in its theoretical diversity but in the fact that running all models first makes the
feature selection for phenotyping principled rather than arbitrary.

---

## 7. Summary table — deferred model status and enablers

| Model | Why deferred | What phenotyping provides | When unblocked |
|---|---|---|---|
| **GaT** | Payoff heterogeneity not characterizable without behavioral types | Phenotype profiles define who are stable self-regulators, chronic over-riders, and adaptive learners — the three GaT player types | After DS5 Step 2 clusters are stable |
| **ABM** | Agent-type distributions require prior model characterization + phenotype profiles | Cluster profiles define agent types; Step 1 parameters calibrate agent rules (sig_hat → update rule volatility; T_{ij} → switching probabilities) | After DS5 Step 2; notebook 47 is last in DS5 sequence |
| **SyD** | Structural data requirement: repeated within-person survey waves not available in DS5 | Phenotyping establishes DS5 boundary conditions (profile distributions) that SyD models on DS6 will need as heterogeneity inputs | When DS6 implementation begins (after DS4 complete) |

---

## 8. Anticipated integration of deferred models with Step 2 output

### GaT (notebook 46) — post-Step 2

- Read `outputs/model_outputs/phenotyping/ds5_cluster_assignments.csv`
- Use cluster labels to stratify participants into GaT player types
- For each player type, estimate payoff parameter from behavioral data:
  - p(open | friction): x_mean within cluster ≈ p(defect against self-regulation)
  - Adaptation rate: mu_hat direction within cluster ≈ whether strategy shifts over time
- Define two-player game: user vs. friction tool (zero-sum framing) OR user vs. self (internal
  conflict framing, more appropriate to DS5)
- Compute Nash equilibrium per cluster
- Report: which clusters are in a stable defect-equilibrium? Which are near a cooperative
  equilibrium? Which are unstable (near the boundary)?

### ABM (notebook 47) — post-Step 2

- Read `outputs/model_outputs/phenotyping/ds5_cluster_profiles.csv`
- Use cluster means on (sig_hat, mu_hat, x_mean, HHI_net) as agent initialization parameters
- Use cluster frequencies as agent-type population weights
- Implement a simple daily behavioral update rule per agent type:
  - Noise-dominated agents: X_{n+1} ~ N(X_n + mu_hat, sig_hat²) with soft boundary handling
  - Habit-stable agents: X_{n+1} = clip(X_n + mu_hat, 0, 1) (DyS map for low-sigma types)
- Simulate under three conditions (no friction, default friction, reintervention)
- Compare simulated response distribution against observed DS5 condition-level distributions
- Report: does the ABM calibrated from Step 2 profiles reproduce the DS5 condition-level
  mean and variance? What is the agent-type distribution of responders vs non-responders?

---

*Written 2026-04-18. The two deferred notebooks (46 and 47) are blocked on Step 2 completion.
Notebook 48 (SyD) is blocked on DS6 implementation. This document is a persistent planning
record, not a commitment to specific implementation details for GaT or ABM — those will be
blueprinted separately once Step 2 is complete.*
