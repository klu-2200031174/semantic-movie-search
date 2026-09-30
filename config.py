"""
Shared settings for the whole project.

Keeping these in one file means that if we change something (like the model
name or a file path), we change it in ONE place and every script picks it up.
"""

from pathlib import Path

# Folder that this file lives in = the project folder.
PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = PROJECT_DIR / "results"

# Where the original dataset is downloaded from (Wikipedia Movie Plots,
# originally published on Kaggle by JustinR, license CC BY-SA 4.0).
RAW_DATA_URL = (
    "https://raw.githubusercontent.com/kiq005/movie-recommendation/"
    "master/src/dataset/wiki_movie_plots_deduped.csv"
)
RAW_DATA_FILE = DATA_DIR / "wiki_movie_plots_raw.csv"

# Our cleaned 10,000-movie subset, and the saved embeddings.
MOVIES_FILE = DATA_DIR / "movies.csv.gz"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.npz"

# The embedding model: BGE-small (about 130 MB), runs fine on a laptop CPU.
# It was trained specifically for search (short question -> long passage).
# We first tried "all-MiniLM-L6-v2"; BGE-small found the right movie more often
# (see the README), so we switched.
MODEL_NAME = "BAAI/bge-small-en-v1.5"

# BGE was trained with this sentence in front of every search query (NOT in
# front of the documents). Adding it tells the model "this is a question".
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# How many movies to keep.
NUM_MOVIES = 10_000

# Movie plots are long (often 500+ words), and one embedding for a whole plot
# blurs everything together. So we cut each plot into overlapping chunks of
# CHUNK_WORDS words and embed each chunk separately.
CHUNK_WORDS = 150
CHUNK_OVERLAP = 30
