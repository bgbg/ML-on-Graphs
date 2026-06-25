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
    pos = {"t": (0, 1), "v": (2, 1), "x1": (3.5, 2.1), "x2": (4.0, 1.0), "x3": (3.5, -0.1)}
    base = [("t", "v"), ("t", "x1"), ("v", "x1"), ("v", "x2"), ("v", "x3")]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.axis("off"); ax.set_xlim(-0.7, 6.2); ax.set_ylim(-0.9, 2.8)
    for a, b in base:
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color="#cccccc", lw=1.5, zorder=1)
    # the step just taken, t -> v
    ax.add_patch(FancyArrowPatch(pos["t"], pos["v"], arrowstyle="-|>", mutation_scale=20,
                                 color="#333333", lw=3, zorder=2,
                                 shrinkA=14, shrinkB=14))
    ax.text(1.0, 1.22, "just walked", fontsize=10, color="#333333", ha="center")
    # candidate next steps from v, each with its bias weight
    cand = {"t": ("1/p", RED, 0.42), "x1": ("1", BLUE, 0.0),
            "x2": ("1/q", GREEN, 0.0), "x3": ("1/q", GREEN, 0.0)}
    for n, (w, c, rad) in cand.items():
        ax.add_patch(FancyArrowPatch(pos["v"], pos[n], arrowstyle="-|>", mutation_scale=15,
                                     color=c, lw=2, ls="--", shrinkA=14, shrinkB=14,
                                     connectionstyle=f"arc3,rad={rad}", zorder=2))
        mx, my = (pos["v"][0] + pos[n][0]) / 2, (pos["v"][1] + pos[n][1]) / 2
        off = 0.42 if n == "t" else 0.16
        ax.text(mx, my + off, w, fontsize=14, color=c, fontweight="bold", ha="center")
    for n, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 0.2, facecolor="white", edgecolor="#333333", lw=1.8, zorder=3))
        ax.text(x, y, n, ha="center", va="center", fontsize=12, fontweight="bold", zorder=4)
    ax.text(0, 0.55, "previous", fontsize=9, color="#888888", ha="center")
    ax.text(2, 0.55, "current", fontsize=9, color="#888888", ha="center")
    ax.set_title("From v, each candidate gets a bias weight", fontsize=14, fontweight="bold")
    fig.savefig("figures/node2vec_transition.png", dpi=150, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    homophily(); structural(); bfs_dfs(); transition()
    print("Wrote figures/sim_homophily.png, sim_structural.png, sim_bfs_dfs.png, "
          "node2vec_transition.png")
