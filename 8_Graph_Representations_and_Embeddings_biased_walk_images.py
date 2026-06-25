"""Pregenerate the homophily / structural-similarity / BFS-vs-DFS figures for
8_Graph_Representations_and_Embeddings.md. Only needs networkx + matplotlib.
Run from the repo root:  python 8_..._biased_walk_images.py"""

import os
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle

os.makedirs("figures", exist_ok=True)
RED, BLUE, GREEN, ORANGE, GREY = "#d62728", "#1f77b4", "#2ca02c", "#fdae6b", "#dddddd"


def ring(G, pos, nodes, ax, color=GREEN, size=1300):
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color="none",
                           edgecolors=color, linewidths=3.5, node_size=size, ax=ax)


# ----------------------------------------------------------- homophily
def homophily():
    G = nx.Graph()
    A = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
    B = [(5, 6), (5, 7), (6, 7), (6, 8), (7, 8), (7, 9), (8, 9)]
    G.add_edges_from(A + B + [(4, 5)])
    commA = {0, 1, 2, 3, 4}
    pos = nx.spring_layout(G, seed=7)
    fig, ax = plt.subplots(figsize=(7, 5.5))
    colors = ["#9ecae1" if n in commA else ORANGE for n in G.nodes()]
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#bbbbbb")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=620)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10)
    ring(G, pos, [1, 3], ax)
    ax.set_title("Homophily — “same crowd”\nthe two ringed nodes share a community",
                 fontsize=13, fontweight="bold")
    ax.axis("off")
    fig.savefig("figures/sim_homophily.png", dpi=150, bbox_inches="tight"); plt.close(fig)


# ----------------------------------------------------------- structural
def structural():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4)])         # star 1, hub 0
    G.add_edges_from([(4, 5), (5, 6)])                          # bridge path
    G.add_edges_from([(7, 6), (7, 8), (7, 9), (7, 10)])         # star 2, hub 7
    pos = nx.spring_layout(G, seed=9)
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#bbbbbb")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=GREY, node_size=520)
    nx.draw_networkx_nodes(G, pos, nodelist=[0, 7], node_color=ORANGE, node_size=760, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=9)
    ring(G, pos, [0, 7], ax)
    ax.set_title("Structural similarity — “same job”\nboth ringed nodes are hubs, yet far apart",
                 fontsize=13, fontweight="bold")
    ax.axis("off")
    fig.savefig("figures/sim_structural.png", dpi=150, bbox_inches="tight"); plt.close(fig)


# ----------------------------------------------------------- BFS vs DFS
def bfs_dfs():
    G = nx.Graph()
    G.add_edges_from([(0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6), (6, 7), (7, 8), (8, 9)])
    pos = nx.spring_layout(G, seed=3)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax in axes:
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#cccccc")
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=GREY, node_size=430)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9)
        nx.draw_networkx_nodes(G, pos, nodelist=[0], node_color=RED, node_size=560, ax=ax)

    # BFS — immediate neighbours of the source
    nx.draw_networkx_nodes(G, pos, nodelist=[1, 2, 3], node_color=BLUE, node_size=480, ax=axes[0])
    nx.draw_networkx_edges(G, pos, edgelist=[(0, 1), (0, 2), (0, 3)], edge_color=BLUE, width=3, ax=axes[0])
    axes[0].set_title("BFS — stay local\n→ structural role", fontsize=13, fontweight="bold")

    # DFS — a path wandering outward
    path = [0, 3, 6, 7, 8, 9]
    nx.draw_networkx_nodes(G, pos, nodelist=path[1:], node_color=GREEN, node_size=480, ax=axes[1])
    nx.draw_networkx_edges(G, pos, edgelist=list(zip(path[:-1], path[1:])),
                           edge_color=GREEN, width=3, ax=axes[1])
    axes[1].set_title("DFS — wander outward\n→ community (homophily)", fontsize=13, fontweight="bold")

    for ax in axes:
        ax.axis("off")
    fig.savefig("figures/sim_bfs_dfs.png", dpi=150, bbox_inches="tight"); plt.close(fig)


# ----------------------------------------------------------- transition bias
def transition():
    """Why each candidate next-step gets its weight: it depends ONLY on the
    distance back to t (the node we just left). Every move follows a real edge —
    nothing teleports."""
    pos = {"t": (0, 1.0), "v": (2.4, 1.0),
           "x1": (4.8, 2.5), "x2": (5.3, 1.0), "x3": (4.8, -0.5)}
    NODE_R = 0.22

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.axis("off"); ax.set_xlim(-1.1, 8.8); ax.set_ylim(-1.9, 3.5)

    # ---- real graph edges (solid grey) — the structure that actually exists ----
    graph_edges = [("t", "v"), ("v", "x1"), ("v", "x2"), ("v", "x3")]
    for a, b in graph_edges:
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]],
                color="#bbbbbb", lw=2.2, zorder=1)
    # the t–x1 edge is THE point: x1 is a neighbour of t as well as of v.
    ax.plot([pos["t"][0], pos["x1"][0]], [pos["t"][1], pos["x1"][1]],
            color=BLUE, lw=2.2, alpha=0.45, zorder=1)
    ax.text(2.05, 2.18, "t–x1 edge\n(x1 is a neighbour of t too)",
            fontsize=10, color=BLUE, ha="center", va="center", style="italic")

    # the step just taken, t -> v
    ax.add_patch(FancyArrowPatch(pos["t"], pos["v"], arrowstyle="-|>", mutation_scale=22,
                                 color="#333333", lw=3.2, zorder=2,
                                 shrinkA=15, shrinkB=15))
    ax.text(1.2, 1.16, "just walked", fontsize=10.5, color="#333333", ha="center", style="italic")

    # candidate next steps from v: (weight label, colour, arc, distance-to-t tag)
    cand = {"t":  ("1/p", RED,   0.45, "d=0  back to t"),
            "x1": ("1",   BLUE,  0.0,  "d=1  same distance as v"),
            "x2": ("1/q", GREEN, 0.0,  "d=2  one step farther"),
            "x3": ("1/q", GREEN, 0.0,  "d=2  one step farther")}
    for n, (w, c, rad, tag) in cand.items():
        ax.add_patch(FancyArrowPatch(pos["v"], pos[n], arrowstyle="-|>", mutation_scale=17,
                                     color=c, lw=2.4, ls="--", shrinkA=15, shrinkB=15,
                                     connectionstyle=f"arc3,rad={rad}", zorder=2))
        mx, my = (pos["v"][0] + pos[n][0]) / 2, (pos["v"][1] + pos[n][1]) / 2
        off = 0.42 if n == "t" else 0.18
        ax.text(mx, my + off, w, fontsize=16, color=c, fontweight="bold", ha="center")
        # distance-to-t tag next to each target node (skip t itself; it carries its own)
        if n != "t":
            ax.text(pos[n][0] + 0.34, pos[n][1], tag, fontsize=9.5, color=c,
                    ha="left", va="center")
    ax.text(pos["t"][0], pos["t"][1] - 0.55, "d=0  back to t", fontsize=9.5, color=RED, ha="center")

    # nodes on top
    for n, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), NODE_R, facecolor="white", edgecolor="#333333", lw=1.8, zorder=3))
        ax.text(x, y, n, ha="center", va="center", fontsize=13, fontweight="bold", zorder=4)
    ax.text(0, 1.0 + 0.42, "previous", fontsize=9.5, color="#888888", ha="center")
    ax.text(2.4, 1.0 + 0.42, "current", fontsize=9.5, color="#888888", ha="center")

    # ---- legend / the rule, in a boxed note ----
    rule = ("The weight depends only on the distance back to t (where we just came from):\n"
            "   • d = 0  → 1/p   step back to t\n"
            "   • d = 1  → 1      x1 is a neighbour of t too — stay equally close\n"
            "   • d = 2  → 1/q   x2, x3 are farther from t — wander outward\n"
            "Every move follows a real edge from v — nothing teleports.")
    ax.text(-0.95, -1.55, rule, fontsize=10.5, ha="left", va="bottom", family="monospace",
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#f7f7f7", edgecolor="#cccccc"))

    ax.set_title("node2vec: a candidate's weight = how far it is from where you just were (t)",
                 fontsize=13.5, fontweight="bold")
    fig.savefig("figures/node2vec_transition.png", dpi=150, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    homophily(); structural(); bfs_dfs(); transition()
    print("Wrote figures/sim_homophily.png, sim_structural.png, sim_bfs_dfs.png, "
          "node2vec_transition.png")
