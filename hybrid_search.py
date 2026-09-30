"""
STEP 6b: Hybrid search: combine keyword AND semantic results.

Each engine is good at different things:
  - keyword search nails exact names and rare words ("Hannibal Lecter"),
  - semantic search understands descriptions ("a man relives the same day").
So we merge their rankings with Reciprocal Rank Fusion (RRF):

    score(movie) = 1 / (60 + rank in keyword list) + 1 / (60 + rank in semantic list)

A movie ranked high by BOTH engines wins. We use ranks, not raw scores,
because BM25 scores (like 20.7) and cosine scores (like 0.62) aren't comparable.
The 60 is a standard constant that stops the #1 spot from dominating everything.
"""

RRF_K = 60


def reciprocal_rank_fusion(keyword_ids, semantic_ids, top_k=5):
    """Merge two ranked lists of movie ids. Returns [(movie_id, rrf_score), ...]."""
    scores = {}
    for ranked_list in (keyword_ids, semantic_ids):
        for rank, movie_id in enumerate(ranked_list, start=1):
            scores[movie_id] = scores.get(movie_id, 0) + 1 / (RRF_K + rank)

    best = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return best[:top_k]


if __name__ == "__main__":
    # Tiny example you can check by hand:  python hybrid_search.py
    keyword = ["A", "B", "C"]   # keyword engine thinks A is best
    semantic = ["C", "A", "D"]  # semantic engine thinks C is best
    for movie, score in reciprocal_rank_fusion(keyword, semantic):
        print(movie, round(score, 4))
    # A is 1st and 2nd -> wins. C is 3rd and 1st -> close second.
