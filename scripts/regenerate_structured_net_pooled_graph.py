"""Regenerate the Structured pooled task-state network graph (thesis Figure 4.9)
with larger node circles, node-label text, and title.

Loads the already-aggregated transition edge list
(notebooks/64_structured_network_theory.ipynb, cell 22/26) -- the pooling here is
a plain groupby sum over that frozen per-participant edge list, not a re-derivation
from raw event data, so nothing about the network can change, only its size on the
page.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
EDGE_LIST = ROOT / "outputs" / "model_outputs" / "structured" / "network_theory" / "transition_edge_list.csv"
OUTPUT_PATH = ROOT / "outputs" / "model_outputs" / "structured" / "network_theory" / "figures" / "fig2_net_pooled_state_graph.png"
THESIS_PATH = ROOT / "latex_master_thesis" / "figure" / "structured" / "fig2_net_pooled_state_graph.png"

STATES = ["inbox", "timed", "all_day", "moved", "completed", "reopened", "deleted"]


def main():
    edges_df = pd.read_csv(EDGE_LIST)
    n_participants = edges_df["participant_id"].nunique()

    pooled_W = (
        edges_df.groupby(["state_from", "state_to"])["count"].sum()
        .unstack(fill_value=0)
        .reindex(index=STATES, columns=STATES, fill_value=0)
    )

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

    fig, ax = plt.subplots(figsize=(9, 9))
    nx.draw_networkx_nodes(G, pos, node_color="#4C72B0", node_size=5200, ax=ax)
    nx.draw_networkx_labels(G, pos, font_color="white", font_size=13, font_weight="bold", ax=ax)
    for (u, v), w in zip(G.edges(), weights):
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=1 + 4 * w / max_w,
                                alpha=0.6, connectionstyle="arc3,rad=0.15",
                                arrowsize=18, ax=ax)
    ax.set_title(
        f"Pooled task-state transition network (all {n_participants} participants, "
        "edge width ~ log flow)",
        fontsize=17, pad=16,
    )
    ax.axis("off")
    plt.tight_layout()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=200, bbox_inches="tight")
    plt.close(fig)

    THESIS_PATH.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copyfile(OUTPUT_PATH, THESIS_PATH)
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Copied: {THESIS_PATH}")


if __name__ == "__main__":
    main()
