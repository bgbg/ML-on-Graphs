---
marp: true
theme: default
paginate: true
---

<!-- Title Slide -->
# Network Formation Models

---

<!-- Agenda Slide -->
# Network Formation Models
- **Why Models Matter** 👈🌟 **Coming Up**
- Erdos-Renyi Model
- Watts-Strogatz Model
- Scale-Free Networks
- Summary / Key Takeaways

---

# Why Models Matter

## Why Models Matter – Importance of Network Models
- Simplify complex systems
- Reveal underlying structural principles
- Predict and simulate behaviors
- Assist in designing efficient, robust networks

---

# Network Formation Models
- **Why Models Matter**
- **Erdos-Renyi Model** 👈🌟 **Coming Up**
- Watts-Strogatz Model
- Scale-Free Networks
- Summary / Key Takeaways

---

# Erdos-Renyi Model

> **Main intuition:** "Everybody has roughly the same chance to connect to everybody else."

---

## Erdos-Renyi Model – Definition
- Developed in 1959 by Paul Erdős and Alfréd Rényi
- Denoted as G(n, p): n nodes, each pair connected with probability p
- Often used as null models in network science to compare against real networks and detect non-random structure

---

## Erdos-Renyi Model – Manual Python Example
```python
import random
import networkx as nx
G = nx.Graph()
n, p = 100, 0.05
G.add_nodes_from(range(n))
for i in range(n):
    for j in range(i+1, n):
        if random.random() < p:
            G.add_edge(i, j)
```

---

## Erdos-Renyi Model – Using `nx` Function
```python
import networkx as nx
G = nx.erdos_renyi_graph(n=100, p=0.05)
```

---

## Erdos-Renyi Model – Properties
- Binomial (or Poisson-like) degree distribution
- Phase transition: sudden emergence of giant component
- Low clustering

---

## When Does ER Fit? – Real-Life-ish Examples
Best approximation when edges form roughly **independently** and **uniformly at random**.

| Example | Why it can fit |
| --- | --- |
| Random assignment of students to project groups | Pairs equally likely to end up together |
| Randomized clinical trial contact networks | Participants randomly assigned to groups |
| Synthetic benchmark networks | Null model: "what if there were no structure?" |
| Some infrastructure failure graphs | Failures/links independent and sparse |
| Gene/protein interaction null models | ER as a useful baseline, not because biology is random |

---

## ER – When It Fails
**Usually bad for** social networks, citation networks, web graphs, collaboration networks, and biological networks — these have clustering, hubs, communities, or heavy-tailed degree distributions.

---

### Erdos-Renyi Model – Real-Life Examples
- **Random gene regulatory networks under specific constraints**
- **Neural connectivity in simple organisms (e.g., C. elegans)**
- **Used as null models in biological and social networks**

---

# Network Formation Models
- **Why Models Matter**
- **Erdos-Renyi Model**
- **Watts-Strogatz Model** 👈🌟 **Coming Up**
- Scale-Free Networks
- Summary / Key Takeaways

---

# Watts-Strogatz Model

> **Main intuition:** "Most connections are local, but a few shortcuts make the world small."

---

## Watts-Strogatz Model – Motivation
- Developed in 1998 by Duncan Watts and Steven Strogatz
- Real-world networks show both high clustering and short path lengths

---

## Watts-Strogatz Model – Manual Python Example
```python
import networkx as nx
import random

# Initialize parameters
n, k, beta = 100, 4, 0.1  # n nodes, k neighbors, beta rewiring probability
G = nx.Graph()

# Create a ring lattice with k neighbors
for i in range(n):
    for j in range(1, k//2 + 1):
        G.add_edge(i, (i + j) % n)
        G.add_edge(i, (i - j) % n)

# Rewire edges with probability beta
edges = list(G.edges())
for i, j in edges:
    if random.random() < beta:
        # Remove the current edge
        G.remove_edge(i, j)

        # Find a valid new target that's not i or already connected to i
        possible_targets = [node for node in range(n) if node != i and not G.has_edge(i, node)]

        # If there are valid targets available
        if possible_targets:
            new_target = random.choice(possible_targets)
            G.add_edge(i, new_target)
        else:
            # If no valid targets, keep the original edge
            G.add_edge(i, j)
```

---

## Watts-Strogatz Model – Using `nx` Function
```python
import networkx as nx
G = nx.watts_strogatz_graph(n=100, k=4, p=0.1)
```

---

## Watts-Strogatz Model – Properties
- High clustering
- Short average path length
- Intermediate randomness

---

## When Does Watts–Strogatz Fit? – Real-Life Examples
Best approximation for networks with **high clustering** and **short average path lengths**.

| Example | Why it can fit |
| --- | --- |
| Friendship networks in small communities | Friends know each other; few long-range links bridge groups |
| Scientific collaboration networks | Local collaboration within fields; cross-field links shorten paths |
| Actor co-appearance networks | Clusters by genre/country, with bridging actors |
| Neural / simplified brain connectivity | Local clustering plus some long-distance connections |
| Power grids | Mostly local links with some long-distance transmission |
| Organizational communication networks | Dense teams; managers/connectors create shortcuts |
| Social media follower networks (partial) | Better than ER for clustering, but misses hubs |

---

### Watts-Strogatz Model – Real-Life Examples
- **Power grid networks**
- **Neural networks in mammals**
- **Collaboration networks among actors or scientists**

---

# Network Formation Models
- **Why Models Matter**
- **Erdos-Renyi Model**
- **Watts-Strogatz Model**
- **Scale-Free Networks** 👈🌟 **Coming Up**
- Summary / Key Takeaways

---

# Scale-Free Networks

> **Main intuition:** "A few hubs hold the whole network together; most nodes have very few links."

---

## Scale-Free Networks – Definition
- Term popularized in the late 1990s
- Degree distribution follows a power law: P(k) ~ k^-γ
- Few hubs, many low-degree nodes

---

## Scale-Free Networks – Real-World Examples
- Internet (router and AS levels)
- Social media networks (e.g., Facebook, Twitter)
- Citation networks

---

## Scale-Free Network Models – Overview
- **Copying model**: 2000s, simulates replication of links
- **Fitness model**: 2002, includes node-specific attractiveness
- **Barabasi-Albert model**: Introduced in 1999

---

### Scale-Free Networks – Real-Life Examples
- **World Wide Web (link structure)**
- **Scientific citation networks**
- **Airport networks (with hub airports)**

---

# Network Formation Models
- **Why Models Matter**
- **Erdos-Renyi Model**
- **Watts-Strogatz Model**
- **Scale-Free Networks**
- **Barabasi-Albert Model** 👈🌟 **Coming Up**
- Summary / Key Takeaways

---

# Barabasi-Albert Model

> **Main intuition:** "The rich get richer — new nodes prefer to attach to already-popular nodes."

---

## Barabasi-Albert Model – Generation Principle
- Introduced in 1999 by Albert-László Barabási and Réka Albert
- New nodes prefer to attach to high-degree nodes
- "Rich-get-richer" mechanism

---

## Barabasi-Albert Model – Manual Python Example
```python
import networkx as nx
import random
import numpy as np

# Start with a small complete graph
G = nx.complete_graph(2)

# Add nodes one at a time with preferential attachment
while len(G) < 100:
    new_node = len(G)  # ID of the new node
    G.add_node(new_node)
    # Calculate probabilities proportional to node degrees
    degrees = [G.degree(node) for node in G.nodes]
    probabilities = np.array(degrees) / sum(degrees)
    # Select m=2 targets with probability proportional to node degree
    targets = np.random.choice(list(G.nodes), size=2, replace=False, p=probabilities)

    # Add edges from new node to targets
    for target in targets:
        G.add_edge(new_node, target)
```

---

## Barabasi-Albert Model – Using `nx` Function
```python
import networkx as nx
G = nx.barabasi_albert_graph(n=100, m=2)
```

---

## Barabasi-Albert Model – Properties
- Power-law degree distribution
- Emergence of hubs
- Robust to random failure but vulnerable to targeted attacks

---

### Barabasi-Albert Model – Real-Life Examples
- **Internet backbone connectivity**
- **Online social networks (e.g., LinkedIn)**
- **Protein interaction networks**

---

# Summary / Key Takeaways

- **Erdos-Renyi (1959)**: Randomness, simple model, phase transitions
- **Watts-Strogatz (1998)**: Clustering + short paths, small-world
- **Scale-Free (1999+)**: Power-law distribution, robustness, real-world relevance
- **Barabasi-Albert (1999)**: Preferential attachment, hub formation
- **Real-world relevance**: Each model reflects different types of observed networks
