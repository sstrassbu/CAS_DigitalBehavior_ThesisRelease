# DS5 — Network Theory (NeT) Step 1 Blueprint
# Notebook: `44_ds5_network_models.ipynb`

**Written:** 2026-04-17  
**Confirmed:** 2026-04-17 — implementation approved by user  
**Stage:** Stage 4, Step 1 — Theoretical and Conceptual Modeling
**Position in sequence:** Final DS5 Step 1 notebook (notebooks 41–43, 45 complete; 44 is last active Step 1 notebook)
**Depends on:** Outputs from notebooks 41, 42, 43, 45 (model parameters available in `outputs/model_outputs/`)

---

## Part 0 — DS5 Recommendation for NeT

### Is DS5 the right dataset for the first NeT implementation?

**Recommendation: Yes, with explicit limitations documented throughout.**

**Reasons for yes:**

1. **Only RCT in the project.** DS5 is the only dataset with randomized condition assignment. Network structure differences across control / default / reintervention conditions can be compared against a true experimental reference. No other dataset provides this. This means the central NeT question — "does friction rewire the app-transition network?" — can be asked with experimental validity only in DS5.

2. **Consistency with completed models.** Four Step 1 models (StM, DyS, StoP, InT) are already complete on DS5. NeT must be implemented on the same dataset to complete the Step 1 model-family quadrangle on DS5 and make inter-model comparison (the net_stop_int_dys_stm_comparison file) fully populated.

3. **Rich behavioral event log.** DS5 has 288,688 events across 573 participants with UTC timestamps and app names. This is enough to engineer participant-level transition sequences, even if network structures will be sparse for short-window participants.

4. **Psychosocial moderators available.** FoMO, belonging, ostracism, and digital_wellbeing scales (the richest psychosocial layer in the project) allow network centralization to be correlated against meaningful individual-difference measures. This is unique to DS5.

5. **Agreement with paper.** §4.2.4 explicitly develops the NeT application for DS5-type data (app-transition networks, centralized users, bridge users, friction as "rewiring"). Implementing NeT on DS5 directly tests the paper's own illustrative framing.

**Reasons for explicit limitation flags (do not suppress these — they belong in the notebook):**

1. **No pre-computed sequence structure.** DS6 has pre-engineered `app_next`/`app_prev` fields and `group_id` session boundaries. DS5 does not. Transitions must be engineered by sorting events within participant by timestamp and constructing consecutive pairs. The absence of session-boundary information means some consecutive pairs may span hours or days and do not reflect behavioral coupling — they are temporal adjacency, not true behavioral transitions.

2. **Short observation windows.** DS5 observation windows range from 7 to ~45 days (MIN_DAYS=7 → ~414 eligible). Compared to DS4 (up to 897 days), DS5 networks will be based on far fewer transition observations. Networks for short-window participants will be sparse and noisy. Network structural metrics (especially stationary distribution) should be treated with low confidence for participants with fewer than 50 observed transitions.

3. **No causal edge interpretation.** A directed edge app_i → app_j means participant used app_j after app_i. It does not mean app_i caused app_j. All inter-app coupling is inferred from temporal ordering, not from any logged interaction. This limits all network claims to descriptive structure.

4. **Fraction of participants with stable network estimates will be lower than StoP/InT.** StoP/InT required MIN_DAYS=7 → 414 eligible (72%). Network stability requires not just days but enough repeated transitions. A participant with 10 unique apps and only 30 transitions will produce a highly sparse matrix. Expect fewer than 414 participants to yield structurally interpretable networks.

5. **Friction events only.** DS5 only logs friction-intervention events (the OneSec trigger). It does NOT log all phone use. Networks therefore represent the participant's app-use structure as observed through OneSec triggers — not their total digital app ecology. This is a major interpretation constraint.

**Bottom line:** DS5 is the right first NeT dataset because of its experimental design and completed model-family context. But the analysis must flag DS5 NeT as the most proxy-dependent of the five Step 1 implementations, with explicit documentation that DS4 will later provide more structurally stable networks (longer windows, more events), and DS6 will provide the most interpretable sequence structure (pre-computed next/prev, session boundaries).

---

## Part 1 — Equations and Network Quantities

### 1.1 What is already in the paper (§4.1.4)

The following are present in the paper and can be cited directly without addition:

| Equation/Concept | Paper location | Formula |
|---|---|---|
| Graph definition | §4.1.4 text | G = (V, E), V = vertices, E = edges |
| Adjacency matrix | Eq. 20 | A_{ij} = 1 if edge between i and j, else 0 |
| Degree | Eq. 21 | k_i = Σ_{j=1}^{n} A_{ij} |
| Graph Laplacian | Eq. 22 | L = D − A |
| Clustering coefficient | Eq. 23 | C = (number of triangles × 3) / number of connected triples |
| Degree distribution | Eq. 24 | p_k ~ k^{-α} |
| App-transition network framing | §4.1.4 core example; §4.2.4 | Apps as nodes; transitions as edges |
| Centrality concepts | Fig. 1 + §4.1.4 text | Degree, betweenness, closeness, eigenvector, PageRank, participation coefficient |
| Behavioral framing | §4.2.4 | "How apps are interconnected in sequences and transitions" |
| Intervention role | §4.2.4 | Friction "rewires" the network, fragments a loop, or blocks a single transition |
| Phenotype framing | §4.2.4 | Centralized (hub-dependent), bridge, tightly clustered, fragmented users |

### 1.2 What is needed for implementation but NOT in the paper

These must be added to the paper (§4.1.4 or §4.2.4) before submission. Flag each in the notebook with: `⚠ NOT IN PAPER — must add to §4.1.4`.

| Quantity | Formula | Why needed | Where to add in paper |
|---|---|---|---|
| Weighted adjacency matrix | W_{ij} = count(i→j) | Core of any empirical network — unweighted A is too sparse | §4.1.4 key quantities |
| Weighted out-degree (strength) | s_i^{out} = Σ_j W_{ij} | Node-level importance measure for directed weighted graphs | §4.1.4 key quantities |
| Row-normalized transition matrix | T_{ij} = W_{ij} / s_i^{out} | Probability of going to app j given currently at app i; Markov chain formulation | §4.1.4 implementation / §4.2.4 |
| Transition entropy (network-level) | H_trans = −Σ_i (s_i^{out}/M) Σ_j T_{ij} log₂(T_{ij}) | Behavioral uncertainty over transition structure; connects NeT to InT | §4.1.5 forward or §4.2.4 |
| Stationary distribution | π T = π, Σ π_i = 1 | Long-run behavioral attractor over apps; connects NeT to DyS | §4.1.4 implementation |
| Network Herfindahl index | HHI_net = Σ_i (s_i^{out}/M)² | Concentration of transition flow; degree of hub-dependence | §4.2.4 |
| Self-transition share | ρ_self = Σ_i W_{ii} / M | How often a participant repeatedly opens the same app | §4.2.4 |

Where M = total number of transitions for participant p.

### 1.3 Optional quantities — defer to Step 2 or DS4

Do not implement these in the first pass. Document as forward flags only.

| Quantity | Why deferred |
|---|---|
| Betweenness / closeness centrality | Requires connected graph; DS5 networks too sparse for most participants |
| Community detection (modularity) | Meaningful only with ≥20 nodes and sufficient density; DS5 scope too limited |
| Temporal network (time-ordered edge sequence) | Step 2 / DS6 |
| Mutual information I(app_t; app_{t+1}) | Bridges InT↔NeT; possible in Step 2 |
| Cross-condition transition matrix comparison (KL divergence) | Possible but adds complexity; Step 2 or paper extension |
| Persistence / relaxation of stationary distribution | Requires DS4 length |
| Network of outcome sequences (opened→dismissed chains) | More appropriate for DS4 or DS6 |

---

## Part 2 — Theory-to-Data Translation Table

| Theoretical Quantity | Original Scientific Meaning | DS5 Variable / Engineered Quantity | Mapping Type | Confidence | Justification |
|---|---|---|---|---|---|
| Graph G = (V, E) | Abstract network of entities and their relations | Per-participant directed weighted app-transition graph | Direct | High | The mapping is explicit in paper §4.1.4 core example |
| Node v ∈ V | An entity in the system | `app_name` — each unique app seen by participant p | Direct | High | Apps are the natural behavioral entities; paper explicitly names this |
| Directed edge (i → j) | Directed relation from entity i to entity j | Consecutive event pair: app_name[t] → app_name[t+1] within participant, sorted by `event_timestamp_utc` | Derived | Medium | Temporal adjacency is not behavioral coupling; but it is the only available signal |
| Edge weight w_{ij} | Strength of relation between i and j | Count of transitions from app i to app j for participant p | Derived | Medium-High | Higher count = stronger behavioral coupling; reasonable proxy |
| Transition matrix T | Markov chain transition probabilities | Row-normalized W_{ij}: T_{ij} = W_{ij} / s_i^{out} | Derived | Medium | Assumes Markov property (next app depends only on current) — not verified; appropriate for Step 1 |
| Weighted out-degree s_i^{out} | Total flow out of node i | Count of all transitions from app_name == i for participant p | Derived | High | Well-defined from event log |
| Network concentration / hub-dependence | Degree to which flow is dominated by few nodes | HHI_net = Σ_i (s_i^{out}/M)² | Derived | Medium-High | Standard measure; directly computable; overlap with `app_herfindahl` from Stage 1 (but NeT uses transition flow, not event count) |
| Transition entropy H_trans | Uncertainty over transition structure | H_trans = −Σ_i (s_i^{out}/M) Σ_j T_{ij} log₂(T_{ij}); omit i where s_i^{out}=0 | Derived | Medium | Related to but distinct from H_app (InT); H_trans conditions on source app; H_app does not |
| Stationary distribution π | Long-run equilibrium visitation frequency | Left eigenvector of T: π T = π, normalized | Derived | Low-Medium | Requires ergodicity and sufficient observations; low confidence for short-window DS5 participants |
| Stationary entropy H_π | Uncertainty of stationary occupancy | H_π = −Σ_i π_i log₂(π_i) | Derived | Low-Medium | Inherits stationary distribution limitations |
| Clustering coefficient C | Local transitivity (triangles) | Same formula applied to binarized A | Derived | Low | DS5 networks too sparse for reliable triangle counts; flag as unreliable |
| Degree distribution p_k | Distribution of connectivity across nodes | Empirical degree distribution of participant network | Derived | Low | Too few nodes per participant for power-law estimation; flag as exploratory only |
| Network centralization | How hub-like the overall network is | Top-1 and top-3 app share of total transition flow | Derived | Medium | Coarse but robust measure of hub-dependence |
| Self-transition share | Tendency to stay on the same app | ρ_self = Σ_i W_{ii} / M | Derived | Medium-High | Directly observable from consecutive events |
| Friction as "rewiring" | Network structure changes under intervention | Condition-level comparison of HHI_net, H_trans, top-app share across control / default / reintervention | Proxy | Medium | Cannot directly observe rewiring; compare condition distributions as proxy |

---

## Part 3 — Sequence Engineering — Explicit Specification

This is the most important pre-implementation decision in the NeT notebook. Every engineering choice must be documented explicitly.

### 3.1 What counts as a node

**A node is an app_name value** for a given participant's network.

- Only apps that appear at least once for participant p are nodes in that participant's network.
- App names are kept as-is from `app_name` in `ds5_behavioral_clean.csv`.
- The number of nodes per participant will vary widely (5–50+ apps).
- There is no cross-participant node alignment: each participant has their own network vocabulary.
- For condition-level analysis, a pooled cross-participant transition matrix is computed separately.

### 3.2 What counts as an edge

**A directed edge (app_i → app_j) is a consecutive event pair** for the same participant.

Formally: for participant p, sort all events by `event_timestamp_utc`. For each consecutive pair (event_t, event_{t+1}) where both events have non-missing `app_name`:
- source node = `app_name[t]`
- target node = `app_name[t+1]`
- this is one transition observation

### 3.3 Handling of event outcomes

**FLAG 2A (default):** Use ALL valid events (event_outcome_simple ∈ {opened, dismissed, closed}) regardless of outcome. This maximizes the transition count and produces the largest, most stable networks.

**Rationale:** The question "which app follows this app in the behavioral sequence?" is independent of whether the participant opened or dismissed. Even a dismissed event represents a moment in the behavioral sequence.

**Alternative (FLAG 2B, deferred):** Use only friction-triggered transitions (is_intervention_event == 1). This produces sparser but more intervention-specific networks. Defer to Step 2.

**Filter:** Exclude events with `event_outcome_simple == 'missing'` (NaN app_name rows). This is already handled by the `app_name` non-null requirement above.

### 3.4 How consecutive events are paired

```python
# Within participant, sort by event_timestamp_utc
# Create app_next = shift(-1) within participant groups

beh_sorted = beh_clean.sort_values(['participant_id_canonical', 'event_timestamp_utc'])
beh_sorted['app_next'] = beh_sorted.groupby('participant_id_canonical')['app_name'].shift(-1)

# Drop last event per participant (no app_next) and drop missing app_name
transitions = beh_sorted.dropna(subset=['app_name', 'app_next']).copy()
```

### 3.5 How time ordering is defined

**Ordering criterion:** `event_timestamp_utc` ascending within participant.

This is the only available ordering. There are no session boundaries in DS5.

### 3.6 How large time gaps are handled

**FLAG G1 (default, Step 1):** No time-gap filtering. All consecutive pairs are included.

**Rationale:** Defining a "behavioral session window" requires an arbitrary threshold (e.g., 2 hours, 12 hours). Without session boundaries from DS5 data, any threshold is a modeling choice that can be deferred. Step 1 uses all consecutive pairs for maximum coverage.

**FLAG G1 deferred alternative (Step 2):** Apply a time-gap filter (e.g., exclude transitions where `time_to_next_event_sec > 7200` seconds / 2 hours). This would make edges more representative of within-session behavioral coupling.

**Document clearly:** Because no gap filter is applied, some edges will span overnight breaks, weekends, or long idle periods. These are temporal adjacencies, not behavioral coupling. This is a known limitation of Step 1.

### 3.7 How same-app (self-loop) transitions are handled

**Include self-loops in the transition matrix** but track them separately.

- W_{ii} > 0 is valid: it means the participant repeatedly opened the same app consecutively.
- Self-loop share ρ_self = Σ_i W_{ii} / M is computed as a separate network metric.
- When computing HHI_net and H_trans, include self-loops in the transition flow.
- For visualizations (if any), self-loops can be drawn separately or suppressed for clarity.

**Do NOT remove self-loops** — they carry signal about habitual single-app focus, which is directly relevant to the phenotype dimension "habitual stability."

### 3.8 Network granularity — participant-level, condition-level, or pooled?

**Primary analysis: participant-level networks.**

Each participant gets their own G^{(p)} = (V^{(p)}, E^{(p)}, W^{(p)}). Network metrics are extracted per participant and stored in `participant_network_metrics.csv`.

**Secondary analysis: condition-level pooled networks.**

For condition-level comparisons, a pooled transition matrix is computed by summing counts across all participants within a condition:

W^{(cond)}_{ij} = Σ_{p ∈ cond} W^{(p)}_{ij}

This is used for visualization and narrative comparison only, not for individual-level analysis. Report it in `condition_network_summary.csv`.

**No global pooled network** — mixing conditions would destroy the experimental structure.

### 3.9 Minimum transition threshold for network eligibility

**FLAG NET1 (default):** Minimum 20 valid transitions to compute network metrics. Below this threshold, set all network metrics to NaN.

**Rationale:** A participant with 5–10 transitions produces a degenerate network with 1–2 edges. HHI_net and H_trans are meaningless at this scale.

**Expected impact:** The eligible fraction will be lower than StoP's 72% (MIN_DAYS=7). Estimate 60–70% of participants will have ≥20 transitions. This should be reported explicitly as a limitation.

---

## Part 4 — Core Network Metrics — First Pass

These are the Step 1 metrics. They are the most theoretically justified and most computationally stable.

### 4.1 Per-participant metrics

| Metric | Symbol | Formula | Notes |
|---|---|---|---|
| Number of nodes | N_nodes | len(V^{(p)}) | n unique apps for participant p |
| Number of unique transitions | N_edges | len(E^{(p)}) | n unique (app_i, app_j) pairs |
| Total transition observations | M | Σ_{ij} W_{ij} | n consecutive event pairs (= total transitions) |
| Network Herfindahl (flow concentration) | HHI_net | Σ_i (s_i^{out}/M)² | In [0,1]; 1 = single hub; lower = more distributed |
| Top-1 app transition share | top1_share_net | max_i(s_i^{out}) / M | Share of all outgoing flow from dominant app |
| Top-3 app transition share | top3_share_net | Σ_{top 3} s_i^{out} / M | Robustness check of hub concentration |
| Self-transition share | rho_self | Σ_i W_{ii} / M | In [0,1]; same-app consecutive rate |
| Transition entropy | H_trans | −Σ_i (s_i^{out}/M) Σ_j T_{ij} log₂(T_{ij}) | Source-weighted transition uncertainty |
| Stationary entropy | H_pi | −Σ_i π_i log₂(π_i) | Only for participants with ergodic T |
| Is stationary distribution computable? | is_stationary_eligible | bool | True if T has unique stationary dist. |

### 4.2 Stationary distribution eligibility

Compute the stationary distribution π only for participants where:
- M ≥ 50 (minimum transitions for convergence)
- The transition matrix T is strongly connected (or has a single dominant communicating class)

For participants where T is reducible or has absorbing states, set `is_stationary_eligible = False` and H_pi = NaN.

Use power iteration or `numpy.linalg.eig` to compute π. Verify: π T ≈ π (check residual).

---

## Part 5 — NeT ↔ StoP / InT / DyS / StM — What NeT Adds

### 5.1 What each prior model captures

| Model | Core object | Core claim | Unit |
|---|---|---|---|
| StoP | Daily X_t time series | Behavioral trajectory has drift μ̂ and variability σ̂ | Per-participant |
| InT | Distributions of outcomes, apps, hours | Behavioral uncertainty in marginal distributions | Per-participant |
| DyS | Same X_t, σ→0 regime | Deterministic vs stochastic behavioral regime | Per-participant |
| StM | Same X_t, Boltzmann bridge | Effective thermodynamic "inverse temperature" β_behav; free energy cost | Per-participant |
| **NeT** | **App-transition graph** | **Relational structure of behavioral sequences** | **Per-participant** |

### 5.2 What NeT adds that is genuinely new

**1. Relational structure.** StoP/InT/DyS/StM all model X_t = n_opened/n_events, which collapses app identity. NeT keeps app identity explicitly — it asks "which apps connect to which apps?" rather than "what fraction of events are opened?". This is the key new dimension.

**2. Hub-dependence.** HHI_net and top-app share measure whether a participant's behavioral flow concentrates through one or a few apps, or spreads evenly. This is orthogonal to σ̂ (StoP) and H_app (InT). A low-σ̂ participant (highly regular) could be either centralized (one-hub) or distributed (habitual multi-app routine). NeT distinguishes these.

**3. Transition uncertainty vs. marginal uncertainty.** H_trans conditions on the source app: "given that I just opened Instagram, how uncertain is my next app?" H_app (InT) is a marginal measure: "how diverse is the overall app distribution?" These are different quantities. A participant who always goes Instagram→WhatsApp→Safari (low H_trans) could still show high H_app if they use many apps. NeT's conditional structure is new.

**4. Stationary distribution.** π gives the long-run expected fraction of time at each app node, derived from the Markov chain implied by T. This is interpretable as a behavioral attractor in app space — the apps that "capture" behavioral flow. DyS found fixed-point attractors in X_t space; π finds attractors in app space. These are related but genuinely different quantities.

**5. Network centralization phenotype dimension.** The paper's §4.3 integration section explicitly lists "network centralization / hub-dependence" as a distinct phenotype dimension (separate from friction sensitivity, impulsivity, etc.). Only NeT produces this.

### 5.3 Overlap with InT

**H_trans is related to but distinct from H_app:**

- H_app = −Σ_a p(app=a) log₂(p(app=a)) — marginal entropy of the app distribution
- H_trans = −Σ_i (s_i^{out}/M) Σ_j T_{ij} log₂(T_{ij}) — weighted average conditional entropy of transitions

H_app measures "how diverse is the overall app distribution?"
H_trans measures "given where I am, how predictable is where I go next?"

These are related by: H_app = H_trans + I(app_t; app_{t+1}) [mutual information between consecutive apps]

This means H_app ≥ H_trans always (inequality: conditional entropy ≤ marginal entropy).
The gap I(app_t; app_{t+1}) = H_app − H_trans measures how much sequential structure reduces uncertainty.

**This is a new bridge between InT and NeT** that should be documented in the paper (§5 integration section) and tested empirically in the notebook:

```
r(H_app, H_trans) expected to be positive but < 1.0
I(app_t; app_{t+1}) = H_app − H_trans gives the mutual information between consecutive apps
```

**Note:** This bridge equation I(X;Y) = H(X) + H(Y) - H(X,Y) is already in the paper (Eq. 28), but its application to the NeT-InT bridge is NOT in the paper. Must add.

### 5.4 Overlap with StoP (σ̂)

H_trans and σ̂ operate on different levels:
- σ̂ is day-level variability in the override rate X_t
- H_trans is event-level uncertainty in app transitions

Expected: moderate positive correlation (high σ̂ participants tend to have higher H_trans, both capturing behavioral disorder), but not redundant. Verify empirically.

### 5.5 Overlap with Stage 1 features

`app_herfindahl` from Stage 1 features is:
- HHI_stage1 = Σ_a (n_events_a / N_total)²

`HHI_net` from NeT is:
- HHI_net = Σ_i (s_i^{out} / M)²

These use different denominators (event count vs. outgoing transition count) and different numerators (events from app a vs. outgoing transitions from app a), but the difference is only the participant's final event. **Check run (post-hoc, 2026-08-08): r(HHI_net, app_herfindahl) = 0.99997, max absolute difference 0.011 across the 463 eligible participants. HHI_net is numerically the same feature as Stage 1's `app_herfindahl`, not a new one.** It is also r=0.985 with `top_app_share` and r=-0.980 with `app_entropy`.

### 5.6 NeT's contribution to later phenotype extraction (Step 2)

NeT adds two phenotype dimensions to the Step 2 feature space that are not covered by the completed models:

1. **Network centralization / hub-dependence:** HHI_net, top1_share_net — **NOT new.** HHI_net is r=0.99997 with Stage 1's `app_herfindahl` and top1_share_net is r=0.985 with HHI_net; both are app-concentration features that NeT re-derives from the transition flow rather than new network dimensions. The genuinely relational NeT quantities are H_trans, I_consec, H_pi and (from nb61) the self-loop-free HHI_net_v2, none of which is reproducible from the app marginal alone.
2. **Transition uncertainty:** H_trans (related to H_app but conditional; adds independent signal)
3. **Self-transition pattern:** rho_self (new; no equivalent in other models)
4. **Stationary distribution entropy:** H_pi (connects to DyS attractor concept; new in app space)

These complete the behavioral profile for Step 2 phenotyping alongside: σ̂, μ̂, H_emp, H_out, H_app, H_hour, β_behav, χ_behav, F_behav, is_dys_eligible.

### 5.7 Unification path in the paper

| Connection | Mechanism | Paper section | Status |
|---|---|---|---|
| NeT → InT | H_trans = H_app − I(app_t; app_{t+1}); sequential mutual information | §5 integration or §4.2.4 ↔ §4.2.5 | NOT in paper — must add |
| NeT → DyS | π (stationary distribution) is the network attractor; DyS found temporal attractor in X_t space | §5 integration | NOT in paper — must add |
| NeT → StoP | H_trans ~correlated with~ σ̂ (both capture behavioral disorder, different levels) | §5 integration | NOT in paper — must add |
| NeT → StM | HHI_net provides network-structural view of the concentration that β_behav captures thermodynamically | §5 integration | NOT in paper — must add |

---

## Part 6 — Explicit DS5 Weakness Flags for NeT

These must appear as explicit warning cells in the notebook, not buried in footnotes.

### FLAG W1 — Short windows → sparse networks

DS5 observation windows are 7–45 days. Most participants have 50–500 friction events (from Stage 1: median events ~100-300 range estimated from 288,688 / 573 ≈ 504 mean events per participant). However, the number of *unique transitions* is typically much smaller — many of those events are self-transitions or repeats of a small number of (app_i → app_j) pairs.

**Consequence:** Network metrics computed from < 20-50 transitions are unreliable. Stationary distribution is only interpretable with ≥ 50 transitions and a well-connected graph.

**What to report:** Distribution of M (total transitions) across participants; fraction eligible for each metric tier.

### FLAG W2 — No session boundaries

DS5 has no `group_id` or explicit session delimiters. Consecutive events may span overnight breaks or multi-day gaps. A transition "Instagram → WhatsApp" at 11pm one night followed by "WhatsApp → YouTube" at 8am the next morning would be treated as two consecutive transitions in the Step 1 implementation.

**Consequence:** Some edges in the network represent temporal adjacency across long gaps, not behavioral coupling. This inflates apparent network connectivity.

**What to do:** Report mean time between consecutive events (time gap distribution). Note that a later Step 2 analysis could apply a session window filter.

### FLAG W3 — Temporal adjacency ≠ causal interaction

The fact that app_j follows app_i in the event log does NOT mean app_i caused or triggered app_j. The participant may have simply finished their task, put the phone down, and returned to a different app later. All network claims must be framed as "observed temporal-succession structure" not "app interaction," "behavioral coupling," or "causal coupling."

**Required language in notebook:** "Edges represent temporal succession in the observed behavioral log, not causal influence between apps. All relational structure is inferred from event ordering, not from any recorded interaction between apps."

### FLAG W4 — Markov assumption not verified

The transition matrix T assumes the Markov property: the next app depends only on the current app, not on the history. This is a strong assumption. In reality, app-switching may depend on time of day, mood state, or earlier in the same session. The Markov assumption is an approximation appropriate for Step 1.

**What to do:** Note that a second-order Markov (T_{ijk}: app_k depends on app_i, app_j) is deferred to Step 2. Compute T_{ij} as Step 1 default.

### FLAG W5 — OneSec-triggered events only

The DS5 behavioral log captures only events where the OneSec friction screen was triggered. It does NOT capture all app use. A participant who uses many apps without triggering OneSec (because those apps are not in their OneSec list) will appear to have fewer apps and a more centralized network than their true digital ecology.

**Consequence:** HHI_net reflects the structure of friction-exposed app use, not the full app ecology. This is a fundamental data boundary that cannot be resolved within DS5.

### FLAG W6 — Stationary distribution is an approximation, not a long-run claim

The stationary distribution π represents where the Markov chain would spend its time *in the long run* under stationarity. DS5 has at most 45-day windows — too short to claim stationarity. π should be treated as a descriptive summary of the empirical transition structure only: the apps toward which the observed transition flow would converge if the behavioral pattern were sustained indefinitely. It is not a claim about true long-run behavioral equilibrium.

**Required language in notebook:** "π is reported as an approximate stationary distribution derived from the observed transition matrix. It describes the implied long-run occupancy under the first-order Markov assumption, not a behaviorally verified equilibrium."

---

## Part 7 — FLAG Decisions Table

| Flag | Default (Step 1) | Alternative (deferred) | Why deferred |
|---|---|---|---|
| FLAG 1 | Participant-level networks (separate G^{(p)} per participant) | Condition-pooled single network per condition | Step 1 focuses on individual variation; condition comparison is secondary |
| FLAG 2A | All valid events define transitions (opened, dismissed, closed) | Friction-only transitions (is_intervention_event == 1) | More events → more stable networks; friction-only subset is Step 2 option |
| FLAG G1 | No time-gap filter on consecutive pairs | 2-hour session window filter | Threshold is arbitrary; defer to Step 2 |
| FLAG M1 | First-order Markov chain (T_{ij}) | Second-order Markov (T_{ijk}) | Complexity; Step 2 |
| FLAG NET1 | MIN_TRANSITIONS = 20 for network metrics | MIN_TRANSITIONS = 50 for stationary distribution | Different quality thresholds for different metrics |
| FLAG S1 | Self-loops included in transition matrix | Self-loops excluded | Self-loops carry signal about habitual same-app use |

---

## Part 8 — Proposed Notebook Structure

Follow the same disciplined format as notebooks 41–43, 45. Copy `notebooks/00_model_notebook_template.ipynb` as starting point.

### Cell 0 — Notebook Header (markdown)
```
# 44 — DS5 Network Theory (NeT) — Step 1
Stage 4, Step 1: Theoretical and Conceptual Modeling
Model family: Network Theory (NeT)
Dataset: DS5 (German adolescents, N=573, RCT)
Paper section: §4.1.4, §4.2.4
```

### Cell 1 — Scope statement (markdown)

Goal: Build per-participant directed weighted app-transition networks from DS5 behavioral event sequences. Estimate network structure metrics. Compare across experimental conditions. Correlate with psychosocial measures.

Not goal: Causal inference about app interactions. Session-boundary analysis. Community detection. Temporal network analysis. These are Step 2 or DS4/DS6.

Output root: `outputs/model_outputs/network_models/`

### Cell 2 — FLAG decisions table (markdown)

Reproduce FLAG table from Part 7 above. All FLAGS must be set before any code cell.

### Cell 3 — Proxy warning cell (markdown)

**Universal proxy warning** (same as notebooks 41–43, 45):

> The behavioral event log in DS5 logs only OneSec-triggered friction events. It does not represent total phone use. All network structures derived from this data reflect the participant's app-transition patterns within the OneSec-triggered subset only, not their complete digital ecology.

Plus NeT-specific proxy warnings:
- Edges represent temporal succession, not causal interaction.
- Transition matrix T assumes Markov property — not verified.
- Networks from < 20 transitions are excluded; stationary distribution requires ≥ 50 transitions.
- No session boundaries: some consecutive pairs span long time gaps.

### Cell 4 — Pure theory (markdown)

**Section 1: Network Theory — Theoretical Foundations**

Present the core NeT formalism in the context of this project. Include:
- G = (V, E, W) definition
- Equations 20–24 from paper (cite)
- Equation additions needed: weighted T_{ij}, s_i^{out}, H_trans, π (flag each as ⚠ NOT IN PAPER)
- Figure: schematic of app-transition network (hand-drawn or conceptual, not data-based)

### Cell 5 — Theory-to-data mapping table (markdown)

Reproduce theory-to-data table from Part 2 above.

### Cell 6 — Equation gaps table (markdown)

| Equation | Status | Action required |
|---|---|---|
| Eq. 20 A_{ij} | In paper | Use directly |
| Eq. 21 k_i | In paper | Use directly |
| Eq. 22 L = D − A | In paper | Reference only; not core for Step 1 |
| Eq. 23 C | In paper | Reference only; too sparse for DS5 Step 1 |
| Eq. 24 p_k ~ k^{-α} | In paper | Reference only; too few nodes for power-law |
| W_{ij} weighted adjacency | NOT in paper | Add to §4.1.4 before submission |
| T_{ij} = W_{ij}/s_i^{out} | NOT in paper | Add to §4.1.4 / §4.2.4 |
| s_i^{out} | NOT in paper | Add to §4.1.4 |
| H_trans | NOT in paper | Add to §4.1.4 or §4.2.4 or §5 |
| π T = π | NOT in paper | Add to §4.1.4 or §4.2.4 |
| HHI_net | NOT in paper | Add to §4.2.4 |
| I(app_t; app_{t+1}) = H_app − H_trans | NOT in paper | Add to §5 integration section |

### Cell 7 — Imports and data loading (code)

Load `ds5_behavioral_clean.csv`. Join `study_condition` from `ds5_pre_survey_clean.csv`. Filter to valid outcomes. Load existing model outputs (StoP participant_parameters, StM participant_stm_parameters, etc.) for later cross-model join.

### Section 1 cells — Sequence Engineering

Cell: sort events within participant by `event_timestamp_utc`. 

Cell: create `app_next` by shifting within participant groups.

Cell: report transition count distribution (M distribution across participants). Report fraction with M ≥ 20. Report mean/median time gap between consecutive events. Flag large-gap transitions.

### Section 2 cells — Transition matrices

Cell: compute W^{(p)} as a dictionary or sparse matrix per eligible participant.

Cell: compute T^{(p)} (row-normalize W^{(p)}).

Cell: sanity checks — T rows sum to 1.0; W symmetric vs asymmetric (expected: asymmetric).

Cell: report distribution of N_nodes, N_edges, M across eligible participants.

### Section 3 cells — Per-participant network metrics

Cell: compute HHI_net, top1_share_net, top3_share_net, rho_self, H_trans per eligible participant.

Cell: sanity check — H_trans should be ≤ H_app (verify empirically; report correlation).

Cell: compute I(app_t; app_{t+1}) = H_app − H_trans bridge metric. Report distribution.

Cell: distribution plots of all metrics.

### Section 4 cells — Stationary distribution

Cell: for eligible participants (M ≥ 50 and ergodic T), compute π via power iteration.

Cell: compute H_pi = −Σ π_i log₂(π_i).

Cell: report fraction of participants eligible for stationary distribution; compare to full eligible set.

Cell: sanity check — verify π T ≈ π (check max absolute residual).

### Section 5 cells — Condition-level comparisons

Cell: compute condition-level pooled networks W^{(cond)}.

Cell: group-level statistics of network metrics by condition (mean, median, std).

Cell: condition comparison — are default/reintervention networks more or less centralized than control?

Cell: Figure 1 — violin plots of HHI_net and H_trans by condition. Mirror style of StoP fig1_stop_params_by_condition.

Cell: Figure 2 — network visualization of condition-level pooled transition matrix (top N apps only; use networkx spring layout or circular layout).

Expected direction: Friction conditions → lower self-transition share (friction interrupts same-app habit loops) + possibly higher H_trans (more diverse transitions after friction interruption). But treat as exploratory.

### Section 6 cells — Psychosocial correlations

Cell: join FoMO, belonging, ostracism, digital_wellbeing, social_media_wellbeing from `ds5_prepost_features.csv`.

Cell: compute Pearson r between network metrics and psychosocial scales (friction-exposed only; N ≈ 250–280).

Hypotheses (exploratory):
- FoMO ~ HHI_net: positive? (high FoMO → hub-dependent, Instagram-dominated network)
- Belonging ~ H_trans: positive? (social motivation → more diverse app transitions)
- digital_wellbeing ~ rho_self: negative? (worse wellbeing → more habitual single-app loops)

Cell: Figure 3 — scatter plots of top 2–3 significant correlations.

Cell: Multi-comparison caveat — report Bonferroni-adjusted p-values alongside uncorrected; flag all as exploratory.

### Section 7 cells — NeT ↔ StoP/InT/DyS/StM unification

Cell: load existing model output files and join to participant_network_metrics.

Cell: compute pairwise correlations:
- r(HHI_net, sigma_hat) — network concentration vs behavioral variability
- r(H_trans, H_emp) — transition entropy vs state-space entropy
- r(H_trans, H_app) — verify InT-NeT bridge (expect H_trans ≤ H_app)
- r(H_pi, F_behav) — stationary entropy vs free energy
- r(rho_self, is_dys_eligible) — self-transition share vs DyS eligibility

Cell: Figure 4 — NeT four-model cross-model comparison scatter (mirror stm_stop_int_dys_comparison pattern).

Cell: Cross-model summary table (condition means for all NeT metrics, matching the style of stm_stop_int_dys_comparison.csv).

### Section 8 cells — Interpretation and limits (markdown)

Step 1 interpretation limits. What can be claimed. What cannot.

### Section 9 cells — Forward connections (markdown)

- Step 2: HHI_net, H_trans, rho_self, H_pi as phenotype features.
- Step 2 extension: time-gap filter on transitions (FLAG G1); friction-only transitions (FLAG 2B).
- DS4: longer windows → more stable networks; rigorous stationary distribution estimation.
- DS6: pre-computed app_next / session boundaries → cleaner network engineering; I(app_t; app_{t+1}) more reliable.
- InT-NeT bridge: mutual information I(app_t; app_{t+1}) = H_app − H_trans (add to §5 integration section of paper).

### Section 10 cells — Save outputs (code)

Save all output files (see Part 9).

---

## Part 9 — Output File Structure

```
outputs/model_outputs/network_models/
  participant_network_metrics.csv         # Per-participant: see column spec below
  transition_edge_list.csv                # Long format: all (participant, app_from, app_to, count, weight)
  condition_network_summary.csv           # Condition-level: mean/median all metrics per condition
  net_stop_int_dys_stm_comparison.csv     # Joined file: participant-level across all 5 model families
  psychosocial_net_correlations.csv       # Pearson r, p, n for each network metric ~ psychosocial scale
  figures/
    fig1_net_hhi_h_trans_by_condition.png
    fig2_net_condition_pooled_graph.png   # NOTE (2026-08-07): shipped as a scatter plot
                                           # (Hub Concentration vs. Transition Entropy by
                                           # condition), not the graph-layout visualization
                                           # this filename implies. Content is correct and
                                           # well-labeled; kept the original planned filename
                                           # rather than renaming the delivered output file.
    fig3_net_psychosocial_scatter.png
    fig4_net_cross_model_comparison.png
  model_run_summary.md
```

### participant_network_metrics.csv — Column specification

| Column | Type | Description |
|---|---|---|
| participant_id_canonical | string | Participant ID |
| study_condition | string | control / default / reintervention |
| n_nodes | int | Number of unique apps (nodes) |
| n_edges | int | Number of unique (app_from, app_to) pairs |
| M_transitions | int | Total transition observations |
| is_net_eligible | bool | M_transitions ≥ 20 |
| is_stationary_eligible | bool | M_transitions ≥ 50 and ergodic T |
| HHI_net | float | Network Herfindahl index of outgoing flow |
| top1_share_net | float | Share of outgoing flow from top-1 app |
| top3_share_net | float | Share of outgoing flow from top-3 apps |
| rho_self | float | Self-transition share (same-app consecutive) |
| H_trans | float | Weighted transition entropy (bits) |
| H_pi | float | Stationary distribution entropy (bits; NaN if not eligible) |
| I_consec | float | I(app_t; app_{t+1}) = H_app − H_trans; NaN if H_app not available |
| H_app | float | H_app from InT outputs (join from information_theory outputs) |

### model_run_summary.md — Required contents

- Date and time of run
- Eligible participant counts (by tier: all, net_eligible, stationary_eligible)
- Condition-level mean HHI_net, H_trans, rho_self
- Top correlation findings (FoMO, belonging, etc.)
- Key limitation flags
- Reference to comparison CSV

---

## Part 10 — Summary of Paper Gaps to Resolve Before Submission

The following must be added to the paper. They can be added during or after notebook implementation.

| Gap | Priority | Where in paper |
|---|---|---|
| Weighted adjacency W_{ij} and strength s_i^{out} (formal definition) | High | §4.1.4 key quantities |
| Transition matrix T_{ij} = W_{ij}/s_i^{out} (formal definition) | High | §4.1.4 key quantities or §4.2.4 |
| Transition entropy H_trans (formula + interpretation) | High | §4.1.4 or §4.2.4 |
| Stationary distribution π T = π (formula + behavioral interpretation) | High | §4.1.4 or §4.2.4 |
| HHI_net as network concentration measure | Medium | §4.2.4 |
| InT–NeT bridge: I(app_t; app_{t+1}) = H_app − H_trans | High | §5 integration section |
| NeT–DyS connection: π as app-space attractor | Medium | §5 integration section |
| NeT–StoP connection: H_trans ~ σ̂ (empirical bridge) | Medium | §5 integration section |
| NeT–StM connection: HHI_net ~ β_behav (structural vs thermodynamic concentration) | Low-Medium | §5 integration section |

---

## Part 11 — Implementation Readiness Checklist

Before writing any code in notebook 44, confirm:

- [x] Read `data_docs/modeling_cautions.md` — done
- [x] Read `data_docs/stage1_feature_qc_notes.md` — done
- [x] Read `outputs/reports/stage4/stage4_implementation_plan.md` — done
- [x] Confirm DS5 structural notes (condition join, is_intervention_event, MIN_DAYS) — done
- [x] Confirm notebooks 41–43, 45 outputs are present in `outputs/model_outputs/` — confirmed
- [x] Blueprint reviewed and approved by user — **CONFIRMED 2026-04-17**
- [x] Copy `notebooks/00_model_notebook_template.ipynb` to `44_ds5_network_models.ipynb` before coding — done (notebook implemented and run 2026-04-17)
- [x] Set all FLAGs in notebook header before first code cell — done
- [x] Write proxy warning cell before Section 1 — done

---

## Appendix — Minimum Working Example (sequence engineering)

```python
import pandas as pd
from pathlib import Path

OUT_CLEAN = Path("outputs/cleaned")
OUT_NET = Path("outputs/model_outputs/network_models")
OUT_NET.mkdir(parents=True, exist_ok=True)

# Load behavioral
beh = pd.read_csv(OUT_CLEAN / "ds5_behavioral_clean.csv",
                  parse_dates=["event_timestamp_utc"])
beh["event_timestamp_utc"] = pd.to_datetime(beh["event_timestamp_utc"], utc=True)

# Join condition
pre = pd.read_csv(OUT_CLEAN / "ds5_pre_survey_clean.csv")
cond_map = pre.set_index("participant_id_canonical")["cond"]
beh["study_condition"] = beh["participant_id_canonical"].map(cond_map)

# Filter to valid events
beh_clean = beh[beh["event_outcome_simple"].isin(["opened","dismissed","closed"])
                & beh["app_name"].notna()].copy()

# Sort and engineer app_next
beh_sorted = beh_clean.sort_values(["participant_id_canonical","event_timestamp_utc"])
beh_sorted["app_next"] = (beh_sorted
    .groupby("participant_id_canonical")["app_name"]
    .shift(-1))

# Valid transitions only
transitions = beh_sorted.dropna(subset=["app_next"]).copy()
print(f"Total transitions: {len(transitions):,}")
print(f"Participants with transitions: {transitions['participant_id_canonical'].nunique()}")

# Per-participant transition counts
edge_counts = (transitions
    .groupby(["participant_id_canonical","app_name","app_next"])
    .size()
    .reset_index(name="count"))
edge_counts.rename(columns={"app_name":"app_from"}, inplace=True)
```
