"""
STEP 7: The web app. Type a query and compare three search engines side by side.

Run locally:  python app.py   then open http://127.0.0.1:7860 in your browser.
On Hugging Face Spaces this file is started automatically.
"""

import re

import gradio as gr
import pandas as pd

import config
from hybrid_search import reciprocal_rank_fusion
from keyword_search import KeywordSearch, tokenize
from semantic_search import SemanticSearch

# Load everything ONCE when the app starts (not on every search).
print("Loading movies and building search engines...")
movies = pd.read_csv(config.MOVIES_FILE)
keyword_engine = KeywordSearch(movies)
semantic_engine = SemanticSearch(movies)
print("Ready!")

EXAMPLES = [
    "a man is stuck reliving the same day again and again",
    "a girl's feelings are little characters living inside her head",
    "a child who can't read properly is called lazy until a teacher realises he has a learning disorder",
    "a woman goes on her honeymoon trip alone after her fiance calls off the wedding",
    "Hannibal Lecter Clarice Starling",
]


def shorten(text, max_words=45):
    words = text.split()
    return " ".join(words[:max_words]) + (" ..." if len(words) > max_words else "")


def keyword_snippet(plot, query):
    """Show the part of the plot where query words appear, with them in bold."""
    query_words = set(tokenize(query))
    words = plot.split()
    is_match = [re.sub(r"[^a-z0-9]", "", w.lower()) in query_words for w in words]
    first = is_match.index(True) if True in is_match else 0
    start = max(0, first - 10)
    window = [f"**{w}**" if m else w for w, m in zip(words[start:], is_match[start:])]
    return ("... " if start > 0 else "") + shorten(" ".join(window))


def format_results(results):
    """results = list of (movie_id, score, snippet) -> one Markdown string."""
    if not results:
        return "*No results.*"
    blocks = []
    for rank, (movie_id, score, snippet) in enumerate(results, start=1):
        row = movies.loc[movie_id]
        blocks.append(f"**{rank}. [{row['title']}]({row['wiki_url']})** ({row['year']}, "
                      f"{row['origin']}) <small>score {score:.3f}</small>\n\n> {snippet}\n")
    return "\n".join(blocks)


def search(query):
    if not query.strip():
        return "Type a query first.", "", ""
    keyword = keyword_engine.search(query, top_k=100)
    semantic = semantic_engine.search(query, top_k=100)
    passages = {movie_id: passage for movie_id, _, passage in semantic}
    hybrid = reciprocal_rank_fusion([m for m, _ in keyword], [m for m, _, _ in semantic])

    keyword_md = format_results(
        [(m, s, keyword_snippet(movies.loc[m, "plot"], query)) for m, s in keyword[:5]])
    semantic_md = format_results([(m, s, shorten(p)) for m, s, p in semantic[:5]])
    hybrid_md = format_results(
        [(m, s, shorten(passages[m]) if m in passages else keyword_snippet(movies.loc[m, "plot"], query))
         for m, s in hybrid])
    return keyword_md, semantic_md, hybrid_md


with gr.Blocks(title="Semantic Movie Search") as demo:
    gr.Markdown(
        "# 🎬 Movie Search: Keyword vs Semantic vs Hybrid\n"
        "Describe a movie in your own words and compare three search engines over "
        "10,000 Wikipedia movie plots. **Keyword** (BM25) matches your exact words. "
        "**Semantic** (BGE-small embeddings) matches meaning. **Hybrid** combines both."
    )
    with gr.Row():
        query_box = gr.Textbox(label="Describe a movie", scale=4,
                               placeholder="e.g. a man keeps reliving the same day")
        search_button = gr.Button("Search", variant="primary", scale=1)
    gr.Examples(EXAMPLES, inputs=query_box)
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 🔤 Keyword (BM25)")
            keyword_output = gr.Markdown()
        with gr.Column():
            gr.Markdown("### 🧠 Semantic (embeddings)")
            semantic_output = gr.Markdown()
        with gr.Column():
            gr.Markdown("### 🤝 Hybrid (both)")
            hybrid_output = gr.Markdown()

    outputs = [keyword_output, semantic_output, hybrid_output]
    search_button.click(search, inputs=query_box, outputs=outputs)
    query_box.submit(search, inputs=query_box, outputs=outputs)

if __name__ == "__main__":
    demo.launch()
