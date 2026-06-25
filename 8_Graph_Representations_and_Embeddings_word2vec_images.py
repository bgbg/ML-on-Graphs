"""Pregenerate the Word2Vec explanatory figures used by
8_Graph_Representations_and_Embeddings.md (Marp doesn't render Mermaid, so we
ship images). Run from the repo root:  python 8_..._word2vec_images.py
Only needs matplotlib + numpy."""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

os.makedirs("figures", exist_ok=True)
RED, ORANGE, BLUE, GREEN, GOLD = "#d62728", "#ff7f0e", "#1f77b4", "#2ca02c", "#e0a800"


# ---------------------------------------------------------------- 1. window
def context_window():
    words = ["the", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]
    center, win = 3, 2
    fig, ax = plt.subplots(figsize=(12, 2.8))
    for i, w in enumerate(words):
        if i == center:
            fc, ec, tc = RED, RED, "white"
        elif 0 < abs(i - center) <= win:
            fc, ec, tc = "#ffe0c2", ORANGE, "black"
        else:
            fc, ec, tc = "#eeeeee", "#bbbbbb", "#999999"
        ax.add_patch(Rectangle((i, 0), 0.9, 1, facecolor=fc, edgecolor=ec, lw=2.5))
        ax.text(i + 0.45, 0.5, w, ha="center", va="center", color=tc,
                fontsize=15, fontweight="bold")
    ax.annotate("center word", (center + 0.45, 1.25), ha="center",
                color=RED, fontsize=13, fontweight="bold")
    ax.annotate("context  (window = 2 each side)", (center + 0.45, -0.45),
                ha="center", color=ORANGE, fontsize=13, fontweight="bold")
    ax.set_xlim(-0.2, len(words)); ax.set_ylim(-0.8, 1.6); ax.axis("off")
    fig.tight_layout(); fig.savefig("figures/w2v_context_window.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- 2. skip-gram
def skipgram():
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)

    vocab = ["cat", "dog", "fox", "run", "the", "…"]
    for j, w in enumerate(vocab):
        filled = w == "fox"
        ax.add_patch(Rectangle((0.7, 4.4 - 0.45 * j), 0.5, 0.4,
                               facecolor=RED if filled else "white", edgecolor="black"))
        ax.text(0.6, 4.6 - 0.45 * j, w, ha="right", va="center", fontsize=10,
                fontweight="bold" if filled else "normal")
    ax.text(0.95, 5.1, "center word\n(one-hot)", ha="center", fontsize=12, fontweight="bold")

    ax.add_patch(Rectangle((3.7, 2.4), 2.1, 1.4, facecolor="#fff3cd", edgecolor=GOLD, lw=3))
    ax.text(4.75, 3.1, "embedding\n(hidden layer)", ha="center", va="center",
            fontsize=13, fontweight="bold")
    ax.text(4.75, 2.0, "↑ the vector we keep", ha="center", color=GOLD,
            fontsize=12, fontweight="bold")

    ctx = [("quick", 0.75), ("brown", 0.85), ("jumps", 0.6), ("over", 0.5), ("democracy", 0.05)]
    for j, (w, p) in enumerate(ctx):
        y = 4.3 - 0.5 * j
        ax.add_patch(Rectangle((8.1, y), 1.7 * p, 0.36, facecolor=BLUE))
        ax.text(8.0, y + 0.18, w, ha="right", va="center", fontsize=10)
    ax.text(8.9, 5.1, "predicted\ncontext words", ha="center", fontsize=12, fontweight="bold")

    for x0, x1 in [(1.35, 3.6), (5.9, 8.0)]:
        ax.add_patch(FancyArrowPatch((x0, 3.1), (x1, 3.1), arrowstyle="-|>",
                                     mutation_scale=22, lw=2.2, color="#333"))
    fig.savefig("figures/w2v_skipgram.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- 3. space
def embedding_space():
    clusters = {
        "royalty": (["king", "queen", "prince", "throne"], (1.4, 4.2), RED),
        "animals": (["cat", "dog", "horse", "cow"], (4.4, 1.2), GREEN),
        "numbers": (["one", "two", "three", "four"], (6.2, 4.8), BLUE),
    }
    rng = np.random.default_rng(1)
    fig, ax = plt.subplots(figsize=(8, 6))
    for words, (cx, cy), color in clusters.values():
        for w in words:
            x, y = cx + rng.normal(0, 0.32), cy + rng.normal(0, 0.32)
            ax.scatter(x, y, s=70, color=color, zorder=3)
            ax.text(x + 0.1, y + 0.1, w, fontsize=12)
    ax.set_title("Similar words land close together", fontsize=14, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(0, 8); ax.set_ylim(0, 6.3)
    fig.savefig("figures/w2v_embedding_space.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- 4. analogy
def analogy():
    pts = {"man": (1, 1), "king": (1, 3.2), "woman": (3.6, 1), "queen": (3.6, 3.2)}
    fig, ax = plt.subplots(figsize=(7.5, 6))
    for w, (x, y) in pts.items():
        ax.scatter(x, y, s=90, color="#333", zorder=3)
        ax.text(x + 0.07, y + 0.1, w, fontsize=14, fontweight="bold")
    for a, b in [("man", "king"), ("woman", "queen")]:
        ax.add_patch(FancyArrowPatch(pts[a], pts[b], arrowstyle="-|>",
                                     mutation_scale=22, color=RED, lw=2.6, zorder=2))
    for a, b in [("man", "woman"), ("king", "queen")]:
        ax.add_patch(FancyArrowPatch(pts[a], pts[b], arrowstyle="-", color="#999",
                                     ls="--", lw=1.5))
    ax.text(0.55, 2.1, "+ royalty", color=RED, fontsize=12, fontweight="bold", rotation=90)
    ax.set_title("king − man + woman ≈ queen", fontsize=16, fontweight="bold")
    ax.set_xlim(0, 5); ax.set_ylim(0, 4.3); ax.set_xticks([]); ax.set_yticks([])
    fig.savefig("figures/w2v_analogy.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- 5. pairs
def training_pairs():
    words = ["the", "quick", "brown", "fox", "jumps", "over"]
    center, win = 3, 2
    fig, ax = plt.subplots(figsize=(11, 4.4))
    ax.axis("off"); ax.set_xlim(-0.3, len(words)); ax.set_ylim(-3.0, 1.4)
    for i, w in enumerate(words):
        if i == center:
            fc, ec, tc = RED, RED, "white"
        elif 0 < abs(i - center) <= win:
            fc, ec, tc = "#ffe0c2", ORANGE, "black"
        else:
            fc, ec, tc = "#eeeeee", "#bbbbbb", "#999999"
        ax.add_patch(Rectangle((i, 0.3), 0.9, 0.9, facecolor=fc, edgecolor=ec, lw=2.5))
        ax.text(i + 0.45, 0.75, w, ha="center", va="center", color=tc, fontsize=14, fontweight="bold")
    ax.text(center + 0.45, -0.35, "center word predicts each neighbour", ha="center", fontsize=12, color="#333")
    pairs = ["(fox, quick)", "(fox, brown)", "(fox, jumps)", "(fox, over)"]
    for k, p in enumerate(pairs):
        ax.text(0.6 + k * 1.5, -1.4, p, ha="center", fontsize=14, color=ORANGE, fontweight="bold")
    ax.text((len(words)) / 2 - 0.3, -2.4,
            "→ four (center, context) training pairs from one window",
            ha="center", fontsize=13, fontweight="bold")
    fig.savefig("figures/w2v_pairs.png", dpi=150, bbox_inches="tight"); plt.close(fig)


# ---------------------------------------------------------------- 6. one-hot
def onehot():
    vocab = ["aardvark", "…", "cat", "dog", "fox", "…", "zebra"]
    hot = 4
    fig, ax = plt.subplots(figsize=(5, 6.5))
    ax.axis("off"); ax.set_xlim(0, 4); ax.set_ylim(-1.7, len(vocab) + 0.6)
    for j, w in enumerate(vocab):
        y = len(vocab) - 1 - j
        v = 1 if j == hot else 0
        ax.add_patch(Rectangle((1.6, y), 0.8, 0.85, facecolor=RED if v else "white", edgecolor="black"))
        ax.text(2.0, y + 0.42, str(v), ha="center", va="center",
                color="white" if v else "#333", fontsize=13, fontweight="bold")
        ax.text(1.45, y + 0.42, w, ha="right", va="center", fontsize=12,
                fontweight="bold" if v else "normal")
    ax.set_title("“fox” as a one-hot vector", fontsize=14, fontweight="bold")
    ax.text(2.0, -1.05, "length = the whole vocabulary (100,000s)\nand it says nothing about meaning",
            ha="center", va="center", fontsize=11)
    fig.savefig("figures/w2v_onehot.png", dpi=150, bbox_inches="tight"); plt.close(fig)


# ---------------------------------------------------------------- 7. lookup
def lookup():
    words = ["cat", "dog", "fox", "run", "the"]
    rng = np.random.default_rng(3)
    E = np.round(rng.uniform(-0.9, 0.9, size=(len(words), 5)), 1)
    hot = 2
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis("off"); ax.set_xlim(-1.6, 9.5); ax.set_ylim(-0.6, len(words) + 1)
    for i, w in enumerate(words):
        y = len(words) - 1 - i
        for j in range(5):
            hl = i == hot
            ax.add_patch(Rectangle((j, y), 1, 1, facecolor="#fff3cd" if hl else "white",
                                   edgecolor=GOLD if hl else "#bbbbbb", lw=2.5 if hl else 1))
            ax.text(j + 0.5, y + 0.5, f"{E[i, j]:+.1f}", ha="center", va="center",
                    fontsize=11, fontweight="bold" if hl else "normal")
        ax.text(-0.2, y + 0.5, w, ha="right", va="center", fontsize=12,
                fontweight="bold" if i == hot else "normal")
    ax.text(2.5, len(words) + 0.35, "embedding matrix   (vocabulary × dimensions)",
            ha="center", fontsize=13, fontweight="bold")
    yfox = len(words) - 1 - hot + 0.5
    ax.add_patch(FancyArrowPatch((5.15, yfox), (6.3, yfox), arrowstyle="-|>",
                                 mutation_scale=20, color=GOLD, lw=2.4))
    ax.text(6.5, yfox, "“fox” vector\n(what we keep)", ha="left", va="center",
            fontsize=12, color=GOLD, fontweight="bold")
    fig.savefig("figures/w2v_lookup.png", dpi=150, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    context_window(); skipgram(); embedding_space(); analogy()
    training_pairs(); onehot(); lookup()
    print("Wrote 7 figures: w2v_context_window, w2v_pairs, w2v_onehot, w2v_lookup, "
          "w2v_skipgram, w2v_embedding_space, w2v_analogy (.png)")
