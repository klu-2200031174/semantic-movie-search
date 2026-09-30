"""
STEP 1: Download the movie dataset, clean it, and keep 10,000 movies.

Run:  python prepare_data.py
Output: data/movies.csv.gz
"""

import re
import urllib.request

import pandas as pd

import config


def download_raw_data():
    """Download the original CSV once. Skip if we already have it."""
    config.DATA_DIR.mkdir(exist_ok=True)
    if config.RAW_DATA_FILE.exists():
        print("Raw data already downloaded, skipping download.")
        return
    print("Downloading dataset (about 80 MB, this can take a minute)...")
    # Download to a temporary ".part" file first, and only rename it when the
    # download is complete. That way a half-finished download never gets
    # mistaken for the real file next time.
    temp_file = config.RAW_DATA_FILE.with_suffix(".part")
    urllib.request.urlretrieve(config.RAW_DATA_URL, temp_file)
    temp_file.rename(config.RAW_DATA_FILE)
    print("Download finished.")


def clean_plot(text):
    """Tidy up one plot summary."""
    text = re.sub(r"\[\d+\]", "", text)  # remove Wikipedia citations like [3]
    text = re.sub(r"\s+", " ", text)  # squash newlines / double spaces into one space
    return text.strip()


def main():
    download_raw_data()
    df = pd.read_csv(config.RAW_DATA_FILE)
    print(f"Loaded {len(df):,} movies.")

    # Give the columns short, simple names.
    df = df.rename(columns={
        "Release Year": "year", "Title": "title", "Origin/Ethnicity": "origin",
        "Director": "director", "Cast": "cast", "Genre": "genre",
        "Wiki Page": "wiki_url", "Plot": "plot",
    })

    # Clean the text columns. Some titles have hidden spaces (" Cast Away").
    df["title"] = df["title"].str.strip()
    df["plot"] = df["plot"].apply(clean_plot)
    df["word_count"] = df["plot"].str.split().str.len()

    # Keep modern films (1980+) that have a real plot (80+ words).
    df = df[(df["year"] >= 1980) & (df["word_count"] >= 80)]
    # Some films appear twice (e.g. listed as both American and British, or
    # under a UK and a US title). Identical plot text = same film, keep one.
    df = df.drop_duplicates(subset=["plot"])
    df = df.drop_duplicates(subset=["title", "year"])
    print(f"After filtering: {len(df):,} movies.")

    # Keep the 10,000 movies with the LONGEST plots. Well-known films tend to
    # have longer Wikipedia plot sections, so this keeps the famous ones.
    df = df.sort_values("word_count", ascending=False).head(config.NUM_MOVIES)
    df = df.reset_index(drop=True)
    df["movie_id"] = df.index  # a simple 0..9999 id for each movie

    columns = ["movie_id", "title", "year", "origin", "genre",
               "director", "cast", "wiki_url", "plot"]
    df[columns].to_csv(config.MOVIES_FILE, index=False, compression="gzip")

    print(f"Saved {len(df):,} movies to {config.MOVIES_FILE}")
    print("Movies per origin:")
    print(df["origin"].value_counts().head(8).to_string())


if __name__ == "__main__":
    main()
