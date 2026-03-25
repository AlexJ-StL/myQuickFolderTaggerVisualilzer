import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import re
import config


def generate_3d_node_topology(df, output_image="codebase_node_graph_3d.png"):
    # Ensure any missing tags/techs are dropped (the rest was handled by utils.py)
    df = df.dropna(subset=["TAG", "TECH"])

    # 1. Identify Key Hubs (Top Techs and Tag Keywords)
    all_techs = []
    for t_str in df["TECH"]:
        all_techs.extend([t.strip() for t in t_str.split(",")])
    top_techs = [t for t, count in Counter(all_techs).most_common(12)]

    all_keywords = []
    for tag in df["TAG"]:
        words = re.findall(r"\b\w+\b", tag.lower())
        all_keywords.extend([w for w in words if w not in config.STOP_WORDS and len(w) > 2])
    top_keywords = [w for w, count in Counter(all_keywords).most_common(15)]

    # 2. Construct the Graph
    G = nx.Graph()

    # Add Tech nodes (Skyblue)
    for tech in top_techs:
        G.add_node(tech, type="tech", color="skyblue", size=150)

    # Add Keyword nodes (Orange)
    for kw in top_keywords:
        G.add_node(kw, type="keyword", color="orange", size=120)

    # Add edges: Weight increases based on co-occurrence in repositories
    for _, row in df.iterrows():
        row_techs = [t.strip() for t in row["TECH"].split(",") if t.strip() in top_techs]
        words = re.findall(r"\b\w+\b", row["TAG"].lower())
        row_keywords = [w for w in words if w in top_keywords]

        for t in row_techs:
            for k in row_keywords:
                if G.has_edge(t, k):
                    G[t][k]["weight"] += 1
                else:
                    G.add_edge(t, k, weight=1)

    # 3. Create Force-Directed 3D Layout
    pos_3d = nx.spring_layout(G, dim=3, seed=42, k=0.5)

    # 4. Render the Visualization
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Draw Weighted Edges
    for edge in G.edges(data=True):
        x_coords = [pos_3d[edge[0]][0], pos_3d[edge[1]][0]]
        y_coords = [pos_3d[edge[0]][1], pos_3d[edge[1]][1]]
        z_coords = [pos_3d[edge[0]][2], pos_3d[edge[1]][2]]
        weight = edge[2]["weight"]
        ax.plot(x_coords, y_coords, z_coords, color="gray", alpha=min(weight * 0.1, 0.5), linewidth=weight * 0.5)

    # Draw Nodes and Labels
    for node, data in G.nodes(data=True):
        ax.scatter(
            pos_3d[node][0],
            pos_3d[node][1],
            pos_3d[node][2],
            c=data["color"],
            s=data["size"],
            edgecolors="k",
            alpha=0.9,
            depthshade=True,
        )
        ax.text(pos_3d[node][0], pos_3d[node][1], pos_3d[node][2], node, fontsize=10, fontweight="bold")

    ax.set_title("3D Tech-Tag Topology: The Connective Tissue of the Codebase", fontsize=16)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(output_image, dpi=150)
    print(f"Topology saved as {output_image}")
