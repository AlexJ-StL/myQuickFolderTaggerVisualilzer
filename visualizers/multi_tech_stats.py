from collections import Counter
import itertools
import matplotlib.pyplot as plt
import seaborn as sns


def generate_multi_tech_stats(df, output_image="tech_synergy_pairs.png"):
    df = df.dropna(subset=["TECH"])

    # 1. Tech Combination Frequency
    # Get lists of techs for each repo
    tech_lists = [[t.strip() for t in str(row).split(",")] for row in df["TECH"]]

    # Tech count distribution
    tech_counts_per_repo = [len(tl) for tl in tech_lists]
    tech_count_dist = Counter(tech_counts_per_repo)

    # Most common pairs
    pairs = []
    for tl in tech_lists:
        if len(tl) >= 2:
            # Sort to ensure (Python, React) is same as (React, Python)
            for pair in itertools.combinations(sorted(tl), 2):
                pairs.append(pair)

    common_pairs = Counter(pairs).most_common(15)

    # 2. Tech per "Focus" (Keywords)
    focus_keywords = ["agent", "mcp", "template", "rust", "web"]
    focus_stats = {}

    for kw in focus_keywords:
        subset = df[df["TAG"].str.contains(kw, case=False, na=False)]
        all_techs_in_subset = []
        for t_str in subset["TECH"]:
            all_techs_in_subset.extend([t.strip() for t in t_str.split(",")])
        focus_stats[kw] = Counter(all_techs_in_subset).most_common(5)

    # 3. Visualization: Top Tech Pairs
    pair_labels = [f"{p[0]} & {p[1]}" for p, c in common_pairs]
    pair_values = [c for p, c in common_pairs]

    plt.figure(figsize=(12, 8))
    sns.barplot(x=pair_values, y=pair_labels, palette="magma")
    plt.title("Multi-Tech Synergy: Top Technology Pairings", fontsize=15)
    plt.xlabel("Number of Repositories", fontsize=12)
    plt.ylabel("Technology Pairs", fontsize=12)
    plt.tight_layout()
    plt.savefig(output_image)
    print(f"✅ Multi-tech synergy saved to {output_image}")

    return tech_count_dist, common_pairs, focus_stats
