# %%

import networkx as nx
import matplotlib.pyplot as plt
import random

random.seed(145)

fig, ax = plt.subplots(figsize=(8, 6))
G = nx.erdos_renyi_graph(10, 0.3, seed=42)
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color="lightblue", ax=ax)
ax.set_title("Graph before the walk")
plt.tight_layout()
fig.savefig("figures/uniform_walk_0.png")

# %%
plt.clf()
walk = [0]
N_STEPS = 5
for step in range(N_STEPS):
    fig, ax = plt.subplots(figsize=(8, 6))
    neighbors = list(G.neighbors(walk[-1]))
    if neighbors:
        walk.append(random.choice(neighbors))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=walk, node_color="red", ax=ax)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=list(zip(walk[:-1], walk[1:])),
        edge_color="red",
        width=2,
        ax=ax,
    )
    ax.set_title(f"Graph after {step+1} steps")
    plt.tight_layout()
    fig.savefig(f"figures/uniform_walk_{step+1}.png")
    print(f"Saved figure {step+1}")

# %%

from node2vec import Node2Vec

node2vec = Node2Vec(G, dimensions=64, walk_length=5, num_walks=1, p=0.5, q=2, seed=42)
walks = node2vec.walks
walk = [int(n) for n in walks[0]]
fig, ax = plt.subplots(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color="lightblue", ax=ax)
nx.draw_networkx_nodes(G, pos, nodelist=walk, node_color="red", ax=ax)
nx.draw_networkx_edges(
    G, pos, edgelist=list(zip(walk[:-1], walk[1:])), edge_color="red", width=2, ax=ax
)
ax.set_title("Node2Vec Walk")
plt.tight_layout()
fig.savefig("figures/node2vec_walk.png")

# %%

walk

# %%
[n for n in G.nodes()]
# %%
