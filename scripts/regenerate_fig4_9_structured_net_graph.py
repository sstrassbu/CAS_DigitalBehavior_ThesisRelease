"""Regenerate Fig 4.9 (pooled Structured task-state network) at thesis width, no title.

Restyle only: redraws from the already-computed pooled transition edge list; no re-fitting.
Data: PRE-RERUN (61-participant) edge list via structured_old_data.read_old_csv (the thesis
caption reports 61 participants / 26,957 transitions).
Source notebook: notebooks/64_structured_network_theory.ipynb (cell 22).
LaTeX placement: drawn at ts.W_075 and meant for width=0.75\\textwidth (was 0.5\\textwidth,
which cannot hold 7 readable node labels; 04_network_theory.tex must be updated).
Self-transitions are drawn as compact outer loops (previously hidden behind the nodes).
Edge width formula unchanged: width = (1 + 4*w/max_w) * EDGE_SCALE (linear in flow; the
caption wording "proportional to log flow" does not match this -- see report).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import Circle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import thesis_style as ts  # noqa: E402
from structured_old_data import read_old_csv  # noqa: E402

OUT_DIR = ts.ROOT / "outputs" / "model_outputs" / "structured" / "network_theory" / "figures"
STATES = ["inbox", "all_day", "timed", "moved", "completed", "reopened", "deleted"]
EDGE_SCALE = 0.6
NODE_SIZE = 2900
LABEL_FS = 7.5


def main() -> None:
    ts.apply()
    edges_df = read_old_csv("network_theory/transition_edge_list.csv")
    pooled_W = edges_df.groupby(["state_from", "state_to"])["count"].sum().unstack(fill_value=0).reindex(
        index=STATES, columns=STATES, fill_value=0)
    print(f"participants={edges_df['participant_id'].nunique()}, total transitions={int(pooled_W.values.sum())}")

    G = nx.DiGraph()
    for s in STATES:
        G.add_node(s)
    for s_from in STATES:
        for s_to in STATES:
            w = pooled_W.loc[s_from, s_to]
            if w > 0:
                G.add_edge(s_from, s_to, weight=w)

    pos = nx.circular_layout(G)
    weights = [G[u][v]["weight"] for u, v in G.edges()]
    max_w = max(weights)

    fig, ax = plt.subplots(figsize=(ts.W_075, ts.W_075))
    # Node circle must be wide enough for "completed" (bold white text) -- otherwise the
    # outer letters land on the white page and vanish.
    nx.draw_networkx_nodes(G, pos, node_color="#4C72B0", node_size=NODE_SIZE, ax=ax)
    nx.draw_networkx_labels(G, pos, font_color="white", font_size=LABEL_FS, font_weight="bold", ax=ax)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    LOOP_R, LOOP_OFFSET = 0.15, 0.34  # offset = node centre -> loop centre (touches node edge)
    for (u, v), w in zip(G.edges(), weights):
        lw = (1 + 4 * w / max_w) * EDGE_SCALE
        if u == v:
            # compact self-loop outside the node (networkx's own loop scales with node
            # size and is huge/clipped at this node size); same weight->width rule.
            unit = np.asarray(pos[u]) / np.linalg.norm(pos[u])
            centre = np.asarray(pos[u]) + unit * LOOP_OFFSET
            ax.add_patch(Circle(centre, LOOP_R, fill=False, lw=lw, ec="#333333", alpha=0.6, zorder=0.5))
            continue
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=lw,
                               alpha=0.6, connectionstyle="arc3,rad=0.15",
                               arrowsize=8, node_size=NODE_SIZE, ax=ax)
    ax.axis("off")
    fig.tight_layout(pad=0.1)

    for path in ts.save(fig, "structured", "fig2_net_pooled_state_graph.png", OUT_DIR):
        print(f"Saved: {path}")


if __name__ == "__main__":
    main()
