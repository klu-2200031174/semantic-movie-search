"""
STEP 6: Measure keyword vs semantic vs hybrid search on test queries.

For each query in eval_queries.csv we know the "right answer" (one movie).
We check WHERE that movie lands in each engine's results.

Metrics (explained simply):
  - Hit@5: was the right movie in the top 5? (Would a user see it without scrolling?)
  - MRR (Mean Reciprocal Rank): 1/rank, averaged. Rank 1 -> 1.0, rank 2 -> 0.5,
    rank 10 -> 0.1, not found -> 0. Rewards putting the answer near the top.

Run:  python evaluate.py
Output: results/evaluation.md
"""

import pandas as pd

import config
from hybrid_search import reciprocal_rank_fusion
from keyword_search import KeywordSearch
from semantic_search import SemanticSearch

DEPTH = 100  # we look this far down each result list for the right answer
ENGINES = ["keyword", "semantic", "hybrid"]


def find_rank(result_ids, target_id):
    """Position of target_id in the results (1 = first), or None if missing."""
    return result_ids.index(target_id) + 1 if target_id in result_ids else None


def summarize(ranks):
    hit5 = sum(r is not None and r <= 5 for r in ranks) / len(ranks)
    mrr = sum(1 / r for r in ranks if r is not None) / len(ranks)
    return hit5, mrr


def main():
    movies = pd.read_csv(config.MOVIES_FILE)
    queries = pd.read_csv(config.PROJECT_DIR / "eval_queries.csv")

    print("Loading search engines...")
    keyword_engine = KeywordSearch(movies)
    semantic_engine = SemanticSearch(movies)

    rows = []
    for q in queries.itertuples():
        match = movies[(movies["title"] == q.expected_title) & (movies["year"] == q.expected_year)]
        target_id = int(match["movie_id"].iloc[0])
        kw_ids = [m for m, _ in keyword_engine.search(q.query, top_k=DEPTH)]
        sem_ids = [m for m, _, _ in semantic_engine.search(q.query, top_k=DEPTH)]
        hyb_ids = [m for m, _ in reciprocal_rank_fusion(kw_ids, sem_ids, top_k=DEPTH)]
        rows.append({"query": q.query, "expected": q.expected_title, "type": q.query_type,
                     "keyword": find_rank(kw_ids, target_id),
                     "semantic": find_rank(sem_ids, target_id),
                     "hybrid": find_rank(hyb_ids, target_id)})

    lines = ["# Evaluation: keyword vs semantic vs hybrid search", "",
             f"{len(movies):,} movies, {len(rows)} test queries, model `{config.MODEL_NAME}`.", "",
             "| Query type | Queries | " + " | ".join(f"{e} Hit@5" for e in ENGINES)
             + " | " + " | ".join(f"{e} MRR" for e in ENGINES) + " |",
             "|---" * 8 + "|"]
    for qtype in ["ALL"] + list(queries["query_type"].unique()):
        group = [r for r in rows if qtype == "ALL" or r["type"] == qtype]
        stats = [summarize([r[e] for r in group]) for e in ENGINES]
        lines.append(f"| {qtype} | {len(group)} | "
                     + " | ".join(f"{hit:.0%}" for hit, _ in stats) + " | "
                     + " | ".join(f"{mrr:.2f}" for _, mrr in stats) + " |")

    def show(rank):
        return str(rank) if rank is not None else f">{DEPTH}"

    lines += ["", "## Every query (rank of the correct movie, 1 is best)", "",
              "| Query | Correct movie | Keyword | Semantic | Hybrid |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['query']} | {r['expected']} | "
                     + " | ".join(show(r[e]) for e in ENGINES) + " |")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    report = "\n".join(lines) + "\n"
    (config.RESULTS_DIR / "evaluation.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
