from collections import Counter
import re
import config


def get_word_frequency_table(df, threshold=5):
    all_words = []
    for tag in df["TAG"].dropna():
        words = re.findall(r"\b\w+\b", tag.lower())
        all_words.extend([w for w in words if w not in config.STOP_WORDS and len(w) > 2])

    counts = Counter(all_words)
    table_data = [(word, count) for word, count in counts.items() if count >= threshold]
    table_data.sort(key=lambda x: x[1], reverse=True)
    return table_data
