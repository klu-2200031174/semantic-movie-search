"""
STEP 2: Keyword search with BM25 (the "old-school" search engine).

BM25 scores a movie higher when:
  - it contains the query's words many times, and
  - those words are RARE across all movies ("heist" counts more than "the").
It only matches exact words. It has no idea "car" and "automobile" mean the same thing.
"""

import re

from rank_bm25 import BM25Okapi

# Very common words that carry no meaning for search.
STOPWORDS = set("""
a an the and or but if of to in on at by for with from as is are was were be been
being it its he she they them his her their him this that these those who whom which
what when where why how into out up down over under again then than so not no do does
did has have had i you we me my our your us about after before while
""".split())


def tokenize(text):
    """Lowercase the text, split it into words, and drop stopwords."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if w not in STOPWORDS]


class KeywordSearch:
    def __init__(self, movies):
        """Build the BM25 index. `movies` is the pandas table from movies.csv.gz."""
        self.movies = movies
        tokenized_plots = [tokenize(plot) for plot in movies["plot"]]
        self.bm25 = BM25Okapi(tokenized_plots)

    def search(self, query, top_k=5):
        """Return the top_k movies as a list of (movie_id, score)."""
        query_words = tokenize(query)
        if not query_words:
            return []
        scores = self.bm25.get_scores(query_words)  # one score per movie
        best_ids = scores.argsort()[::-1][:top_k]  # indexes of highest scores
        return [(int(i), float(scores[i])) for i in best_ids if scores[i] > 0]


if __name__ == "__main__":
    # Quick test:  python keyword_search.py
    import pandas as pd
    import config

    movies = pd.read_csv(config.MOVIES_FILE)
    print("Building keyword index (takes a few seconds)...")
    engine = KeywordSearch(movies)
    for query in ["dinosaur theme park", "a man keeps living the same day over and over"]:
        print(f"\nQuery: {query}")
        for movie_id, score in engine.search(query):
            row = movies.loc[movie_id]
            print(f"  {score:6.2f}  {row['title']} ({row['year']})")
