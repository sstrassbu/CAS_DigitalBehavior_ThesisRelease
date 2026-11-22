# transition_edge_list.csv

**Unit of observation:** one row per `(app_prev, app_current)` pair — the **pooled**
transition matrix across all eligible participants' attempt-row sequences (top-20 apps +
`'other'`, 21×21 = 441 rows).

---

## Column reference

| Column | Type | Description |
|---|---|---|
| `app_prev` | string | Previous app (one of the top-20 by attempt-row frequency, or `'other'`) |
| `app_current` | string | Current app |
| `count` | int | Pooled count of this transition across all 950 eligible participants |
| `probability` | float | `count` / (row total for `app_prev`) — row-normalized, each `app_prev`'s row sums to 1.0 (verified) |

---

## How this file was produced

- **Producing notebook:** `notebooks/54_ds4_network_models.ipynb`, cell 12
- **Blueprint:** `outputs/reports/stage4/step1_modeling/ds4_net_blueprint.md`

Built from attempt rows only (`intervention_event`+`no_intervention`, excluding
`app_close_event`) — see `participant_network_metrics.md` for why.

## Known limitations

- This is a **pooled** matrix (summed counts across participants before normalizing),
  not an average of per-participant matrices — high-volume participants contribute more
  to the pooled structure than low-volume ones.
- Same event-class-exclusion caveat as `participant_network_metrics.md`.

## How to load

```python
import pandas as pd

edges = pd.read_csv("outputs/model_outputs/ds4_network_models/transition_edge_list.csv")
pivot = edges.pivot(index="app_prev", columns="app_current", values="probability")
```
