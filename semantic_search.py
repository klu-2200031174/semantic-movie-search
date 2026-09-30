"""
STEP 5: Semantic search: search by MEANING using embeddings.

An embedding is a list of 384 numbers that describes what a piece of text is
about. Texts with similar meaning get similar numbers, even if they share no words.
To search, we turn the query into an embedding and find the plot chunks whose
embeddings point in the most similar direction (cosine similarity).
"""

import numpy as np

import config


def chunk_text(text, chunk_words=config.CHUNK_WORDS, overlap=config.CHUNK_OVERLAP):
    """Split a long text into overlapping pieces of `chunk_words` words each.

    Example with chunk_words=4, overlap=1:
    "a b c d e f g"  ->  ["a b c d", "d e f g"]
    """
    words = text.split()
    step = chunk_words - overlap
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + chunk_words]))
        if start + chunk_words >= len(words):
            break  # this chunk reached the end of the text
    return chunks


def load_model():
    """Load the embedding model (downloads about 130 MB the first time)."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(config.MODEL_NAME)


class SemanticSearch:
    def __init__(self, movies, model=None):
        self.movies = movies
        self.model = model or load_model()

        saved = np.load(config.EMBEDDINGS_FILE)
        # Stored as float16 to halve the file size; convert back for math.
        self.chunk_embeddings = saved["embeddings"].astype(np.float32)
        self.chunk_movie_ids = saved["movie_ids"]  # which movie each chunk came from

        # Re-create the chunk texts (same order as when we built the embeddings)
        # so we can show the user WHICH passage matched.
        self.chunk_texts = [c for plot in movies["plot"] for c in chunk_text(plot)]
        assert len(self.chunk_texts) == len(self.chunk_embeddings), (
            "Chunks don't match the saved embeddings. Re-run build_embeddings.py")

    def search(self, query, top_k=5):
        """Return the top_k movies as a list of (movie_id, score, best_passage)."""
        query_embedding = self.model.encode(config.QUERY_PREFIX + query,
                                            normalize_embeddings=True)

        # All vectors have length 1, so a dot product IS the cosine similarity.
        # One matrix multiply scores every chunk at once.
        chunk_scores = self.chunk_embeddings @ query_embedding

        # A movie's score = the score of its BEST matching chunk.
        movie_scores = np.full(len(self.movies), -1.0)
        np.maximum.at(movie_scores, self.chunk_movie_ids, chunk_scores)

        results = []
        for movie_id in movie_scores.argsort()[::-1][:top_k]:
            chunks_of_movie = np.where(self.chunk_movie_ids == movie_id)[0]
            best_chunk = chunks_of_movie[chunk_scores[chunks_of_movie].argmax()]
            results.append((int(movie_id), float(movie_scores[movie_id]),
                            self.chunk_texts[best_chunk]))
        return results
