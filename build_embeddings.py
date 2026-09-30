"""
STEP 4: Turn every plot chunk into an embedding and save them to disk.

Run:  python build_embeddings.py
Output: data/embeddings.npz
This is the slow step: about 60,000 chunks, which takes roughly 30-60 minutes
on a laptop CPU (or a few minutes on a free Google Colab GPU). We only do it
ONCE; the app loads the saved file instead of recomputing.
"""

import time

import numpy as np
import pandas as pd

import config
from semantic_search import chunk_text, load_model


def main():
    movies = pd.read_csv(config.MOVIES_FILE)

    # Cut every plot into chunks and remember which movie each chunk belongs to.
    chunks, movie_ids = [], []
    for movie_id, plot in zip(movies["movie_id"], movies["plot"]):
        for chunk in chunk_text(plot):
            chunks.append(chunk)
            movie_ids.append(movie_id)
    print(f"{len(movies):,} movies -> {len(chunks):,} chunks")

    model = load_model()
    start = time.time()
    embeddings = model.encode(
        chunks,
        batch_size=64,  # how many chunks to process at once
        show_progress_bar=True,
        normalize_embeddings=True,  # make every vector length 1 (needed for cosine)
    )
    print(f"Done in {time.time() - start:.0f} seconds. Shape: {embeddings.shape}")

    np.savez(
        config.EMBEDDINGS_FILE,
        embeddings=embeddings.astype(np.float16),  # half the size, same results
        movie_ids=np.array(movie_ids, dtype=np.int32),
    )
    print(f"Saved to {config.EMBEDDINGS_FILE}")


if __name__ == "__main__":
    main()
