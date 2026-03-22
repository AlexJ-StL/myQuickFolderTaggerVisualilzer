import pandas as pd
from collections import Counter
import re


def get_word_frequency_table(file_path, threshold=5):
    df = pd.read_csv(file_path)
    df.columns = [c.strip() for c in df.columns]

    all_words = []
    stop_words = {"a", "an", "the", "in", "on", "at", "to", "for", "with", "and", "or", "of"}
    for tag in df["TAG"].dropna():
        words = re.findall(r"\b\w+\b", tag.lower())
        all_words.extend([w for w in words if w not in stop_words and len(w) > 2])

    counts = Counter(all_words)
    table_data = [(word, count) for word, count in counts.items() if count >= threshold]
    table_data.sort(key=lambda x: x[1], reverse=True)
    return table_data


word_table = get_word_frequency_table("codebase_tags.csv", threshold=10)
print(word_table)
