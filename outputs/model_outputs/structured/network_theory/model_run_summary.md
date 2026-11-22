# Structured NeT — Model Run Summary

**Run date:** 2026-08-03
**Notebook:** notebooks/64_structured_network_theory.ipynb
**Blueprint:** outputs/reports/structured/structured_net_blueprint.md

## Eligibility
- Participants: 61
- NeT-eligible (M>=20 transitions): 45 (73.8%)
- Stationary-eligible (M>=50, ergodic): 8 (13.1%)

## Key results (eligible participants, N=45)
- HHI_net: mean=0.534, median=0.512
- rho_self: mean=0.373, median=0.400
- H_trans: mean=1.284 bits (max possible log2(7)=2.807)
- top1_share_net: mean=0.670

## Entry-state distribution (non-censored tasks only, FLAG W1)
entry_state
timed      0.9335
all_day    0.0526
inbox      0.0139

## Subscription group comparison (FLAG W5 -- observational only)
                       HHI_net              rho_self              H_trans              top1_share_net             
                          mean median count     mean median count    mean median count           mean median count
subscription_type_last                                                                                            
free                     0.576  0.540    16    0.333  0.371    16   1.249  1.271    16          0.708  0.681    16
pro                      0.510  0.509    29    0.395  0.425    29   1.303  1.362    29          0.648  0.667    29

## Flags applied
See outputs/reports/structured/structured_net_blueprint.md Part 2-4 for full FLAG rationale:
NET-S1 (state priority order), NET-S2 (cosmetic edits = self-loop), NET-S3 (self-loops included),
NET-G1 (task-then-participant pooling), NET-T1 (MIN_TRANSITIONS=20/50), W1-W6 (weakness flags).
