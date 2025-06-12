import utils
import networkx as nx
import numpy as np
from tqdm.auto import tqdm
import os


def combine_nodes(grph, node1, node2) -> nx.Graph:
    """
    Combine the two nodes into a new node.

    The new node is a combination of the two nodes: it gets all the edges of the two nodes
    (incoming and outgoing). The `label` of the new node is 1.
    The ID of the new node is the concatenation of the IDs of the two nodes.
    """
    G_new = grph.copy()
    G_new.add_node(f"{node1}_{node2}", label=1)
    G_new.add_edges_from([(f"{node1}_{node2}", n) for n in grph.neighbors(node1)])
    G_new.add_edges_from([(f"{node1}_{node2}", n) for n in grph.neighbors(node2)])
    G_new.remove_node(node1)
    G_new.remove_node(node2)
    return G_new


def get_synthetic_graph_file_path() -> str:

    url = "https://snap.stanford.edu/data/ca-AstroPh.txt.gz"
    file_path = utils.download_and_extract_data(zip_url=url, filetype="csv.gz")
    file_path_out = os.path.splitext(file_path)[0] + "_sample.graphml"
    if os.path.exists(file_path_out):
        print(f"File {file_path_out} already exists")
        return file_path_out

    # Load the Astro Physics collaboration network dataset as an undirected graph.
    G = nx.read_edgelist(file_path, create_using=nx.Graph(), nodetype=int, comments="#")
    utils.print_graph_info(G)

    # For faster execution, use a subgraph with the first K nodes.
    K = 5_000
    subset_nodes = list(G.nodes())[:K]
    G_sub = G.subgraph(subset_nodes).copy()
    G_sub = utils.get_giant_component(G_sub)
    utils.print_graph_info(G_sub)

    # set the ids of each nodes to string
    G_sub = nx.relabel_nodes(G_sub, {node: str(node) for node in G_sub.nodes()})

    # add 'label' attribute to the nodes and set it to 0 for all nodes
    for node in G_sub.nodes():
        G_sub.nodes[node]["label"] = 0

    n_pairs_to_combine = int(G_sub.number_of_nodes() * 0.05)
    print(f"Will combine {n_pairs_to_combine} pairs of nodes")
    np.random.seed(111)
    nodes = list(G_sub.nodes())
    d = (np.array([G_sub.degree(node) for node in nodes])) ** 2
    probs = d / d.sum()
    for i in tqdm(range(n_pairs_to_combine)):
        node1, node2 = np.random.choice(nodes, 2, replace=False, p=probs)
        try:
            G_sub = combine_nodes(G_sub, node1, node2)
        except:
            continue

    # replace the labels: 1 -> "ambiguous"; 0 -> "not ambiguous"
    for node, data in G_sub.nodes(data=True):
        data["label"] = "ambiguous" if data["label"] == 1 else "not ambiguous"

    nx.write_graphml(G_sub, file_path_out)
    print(f"Synthetic graph saved to {file_path_out}")
    return file_path_out


if __name__ == "__main__":
    get_synthetic_graph_file_path()
