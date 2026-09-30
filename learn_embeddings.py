"""
STEP 3: A tiny playground to SEE what embeddings do, before using them for real.

Run:  python learn_embeddings.py
Nothing is saved. This file is only for learning (and for explaining in interviews).
"""

import numpy as np

from semantic_search import load_model

model = load_model()

sentences = [
    "A man keeps reliving the same day over and over.",    # 0
    "He wakes up every morning and it is always Tuesday.",  # 1  same meaning, no shared words
    "A shark attacks swimmers at a beach resort.",           # 2  different meaning
]

# Each sentence becomes a list of 384 numbers.
embeddings = model.encode(sentences, normalize_embeddings=True)
print("Shape:", embeddings.shape)  # (3 sentences, 384 numbers each)
print("First 5 numbers of sentence 0:", np.round(embeddings[0][:5], 3))

# Cosine similarity: 1.0 = identical meaning, lower = less related.
# (With this model even unrelated sentences score around 0.3, so what matters
# is which score is HIGHER, not the exact number.)
# Because every vector has length 1, the dot product equals the cosine similarity.
similarity = embeddings @ embeddings.T
print("\nSimilarity table (rows and columns are sentences 0, 1, 2):")
print(np.round(similarity, 2))
