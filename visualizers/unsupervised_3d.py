import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import config

def generate_3d_semantic_plot(df, output_image="semantic_3d_plot.png"):
    # Clean data - remove missing values
    df = df.dropna(subset=["TAG", "TECH"])

    # Combine custom STOP_WORDS with english
    combined_stops = list(ENGLISH_STOP_WORDS.union(config.STOP_WORDS))

    # 1. Vectorize the Tags
    vectorizer = TfidfVectorizer(stop_words=combined_stops)
    tfidf_matrix = vectorizer.fit_transform(df["TAG"])

    # 2. Scale the TF-IDF matrix before PCA
    scaler = StandardScaler(with_mean=False)
    scaled_tfidf = scaler.fit_transform(tfidf_matrix)

    # 3. Reduce dimensions to 3 (X, Y, Z) using PCA
    pca = PCA(n_components=3)
    coords = pca.fit_transform(scaled_tfidf.toarray())

    df["x"] = coords[:, 0]
    df["y"] = coords[:, 1]
    df["z"] = coords[:, 2]

    # 4. Categorize by Primary Technology for coloring
    df["primary_tech"] = df["TECH"].apply(lambda x: x.split(",")[0].strip())
    top_techs = df["primary_tech"].value_counts().nlargest(8).index
    df["color_group"] = df["primary_tech"].apply(lambda x: x if x in top_techs else "Other")

    # 5. Create the 3D Visualization
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")

    unique_groups = df["color_group"].unique()

    for i, group in enumerate(unique_groups):
        mask = df["color_group"] == group
        ax.scatter(
            df.loc[mask, "x"], df.loc[mask, "y"], df.loc[mask, "z"], label=group, s=50, alpha=0.7, edgecolors="w"
        )

    ax.set_title("3D Semantic Galaxy: Repository Tag Relationships", fontsize=16, pad=20)
    ax.set_xlabel("Semantic Component 1")
    ax.set_ylabel("Semantic Component 2")
    ax.set_zlabel("Semantic Component 3")

    # Position the legend
    ax.legend(title="Primary Technology", loc="center left", bbox_to_anchor=(1.07, 0.5))

    plt.tight_layout()
    plt.savefig(output_image, dpi=150)
    print(f"✅ 3D Plot saved to {output_image}")
