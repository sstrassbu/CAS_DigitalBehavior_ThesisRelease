# DS4 NeT -- Model Run Summary

**Notebook:** `54_ds4_network_models.ipynb`  
**Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_net_blueprint.md`  
**Run date:** 2026-08-11

## Summary

```
                                                  0
n_total                                 1039.000000
n_eligible                               950.000000
median_rho_self                            0.679544
median_H_trans                             0.954493
median_HHI_net                             0.509072
n_stationary_eligible                    946.000000
median_H_pi                                1.084518
r_HHInet_appherfindahl                     0.968766
n_Iconsec_negative                         0.000000
n_Iconsec_negative_naive_buggy_version   138.000000
```

## Note

rho_self here excludes app_close_event (see blueprint SS1) -- do not compare directly to DS5's rho_self without that caveat.

## Bug caught and fixed during implementation

Initial I_consec = InT's all-events H_app minus H_trans produced 138/950 negative values (min -0.631 bits) -- mathematically impossible for a true H(Y)-H(Y|X). Root cause, verified concretely on participant <participant-id>: InT's H_app is computed over ALL events including app_close_event rows: 647 of this participant's events were app_close_event, 98% reddit, dragging their all-events H_app to 0.86 bits even though their 158 real attempt rows were much more diverse (H_trans=1.49 bits on that same diverse population). Fixed by computing H_app_attempts -- the current-app marginal within the exact same attempts-only, top-20-encoded population H_trans uses -- instead of reusing InT's differently-scoped H_app. Result: 0/950 negative after the fix.
