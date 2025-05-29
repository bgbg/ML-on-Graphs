# cora_export.py

import os
import torch
import random
from collections import deque
from torch_geometric.datasets import CoraFull
from torch_geometric.utils import subgraph, to_networkx
from torch_geometric.data import Data
import networkx as nx


def get_neighbors_within_radius(
    edge_index: torch.Tensor, node: int, radius: int
) -> set:
    visited = set([node])
    queue = deque([(node, 0)])
    while queue:
        current, dist = queue.popleft()
        if dist == radius:
            continue
        neighbors = set(edge_index[1][edge_index[0] == current].tolist())
        neighbors.update(edge_index[0][edge_index[1] == current].tolist())
        for n in neighbors:
            if n not in visited:
                visited.add(n)
                queue.append((n, dist + 1))
    return visited


def download_sample(initial_sample=10, radius=3, out_name="cora_graph_subset.graphml"):
    dataset = CoraFull(root="/tmp/CoraFull")
    data = dataset[0]
    num_nodes = data.num_nodes
    edge_index = data.edge_index

    # set seed for reproducibility
    random.seed(42)
    random_nodes = random.sample(
        range(num_nodes),
        initial_sample,
    )

    neighbors = set()
    for node in random_nodes:
        neighbors.update(get_neighbors_within_radius(edge_index, node, radius))
    neighbors = torch.tensor(list(neighbors), dtype=torch.long)

    sub_edge_index, _ = subgraph(neighbors, edge_index, relabel_nodes=True)
    sub_x = data.x[neighbors]
    sub_y = data.y[neighbors]
    sub_data = Data(x=sub_x, edge_index=sub_edge_index, y=sub_y)

    nx_graph = to_networkx(sub_data, to_undirected=True, node_attrs=["y"])

    dir_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(dir_out, exist_ok=True)
    fn_out = os.path.join(dir_out, out_name)
    nx.write_graphml(nx_graph, fn_out)
    print(f"Sample graph saved to {fn_out}")
    return fn_out


def download_full(out_name="cora_graph_full.graphml"):
    dataset = CoraFull(root="/tmp/CoraFull")
    data = dataset[0]

    nx_graph = to_networkx(data, to_undirected=True, node_attrs=["y"])

    dir_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(dir_out, exist_ok=True)
    fn_out = os.path.join(dir_out, out_name)
    nx.write_graphml(nx_graph, fn_out)
    print(f"Full graph saved to {fn_out}")
    return fn_out


if __name__ == "__main__":
    download_full()
    download_sample()
