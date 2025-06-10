from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import os


model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_thesis(sentences: List[str]) -> List[str]:
    embeddings = model.encode(sentences)
    centroid = np.mean(embeddings, axis=0)
    
    sims = [
        (s, np.dot(e, centroid) / (np.linalg.norm(e) * np.linalg.norm(centroid)))
        for s, e in zip(sentences, embeddings)
    ]
    sorted_sims = sorted(sims, key=lambda x: x[1], reverse=True)

    # Load and validate TOP_THEMES from environment
    top_n_raw = os.environ.get("TOP_THEMES", "2")
    try:
        top_n = int(top_n_raw)
        if top_n < -1 or (top_n == 0):
            raise ValueError
    except ValueError:
        raise ValueError(
            f"Invalid value for TOP_THEMES: {top_n_raw}. Must be -1 or a positive integer."
        )

    if top_n == -1:
        return [s for s, _ in sorted_sims]
    return [s for s, _ in sorted_sims[:top_n]]