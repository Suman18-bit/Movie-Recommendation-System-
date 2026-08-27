"""
logic.py — the projection room.
Loads the pickled TF-IDF model once, then serves cosine-similarity
recommendations.
"""
import ast
import os
import pickle

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = "movie_data.pkl"
MATRIX_FILE = "tfidf_matrix.pkl"
_CACHE = {}


def _read(path):
    with open(path, "rb") as fh:
        return pickle.load(fh)


def load_data():
    """Loads the prepared movie dataframe and TF-IDF matrix (cached in memory)."""
    if _CACHE:
        return _CACHE["df"], _CACHE["indices"], _CACHE["matrix"]

    df = indices = matrix = None

    if os.path.exists(DATA_FILE):
        blob = _read(DATA_FILE)
        if isinstance(blob, dict):
            df = blob.get("df")

            # Explicit 'is None' checks to prevent pandas truthiness errors
            indices = blob.get("Indices")
            if indices is None:
                indices = blob.get("indices")

            matrix = blob.get("Tfidf_metrix")
            if matrix is None:
                matrix = blob.get("Tfidf_matrix")
            if matrix is None:
                matrix = blob.get("tfidf_matrix")
        else:  # bare dataframe pickle
            df = blob

    for name in ("movies.pkl", "df.pkl", "data.pkl"):
        if df is None and os.path.exists(name):
            df = _read(name)
            break

    if matrix is None and os.path.exists(MATRIX_FILE):
        matrix = _read(MATRIX_FILE)

    if df is None or matrix is None:
        raise FileNotFoundError(
            "Model files not found. Place 'movie_data.pkl' "
            "(and/or 'tfidf_matrix.pkl') next to logic.py."
        )

    if indices is None:
        indices = pd.Series(df.index, index=df["title"])
    if isinstance(indices, pd.Series):
        indices = indices.to_dict()
    indices = {str(k): int(v) for k, v in indices.items()}

    _CACHE.update(df=df, indices=indices, matrix=matrix)
    return df, indices, matrix


def _row(df, i):
    try:
        return df.loc[i]
    except KeyError:
        return df.iloc[i]


def _parse_genres(raw):
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return []
    if not isinstance(raw, list):
        try:
            raw = ast.literal_eval(str(raw))
        except Exception:
            return [g.strip() for g in str(raw).split(",") if g.strip()][:4]
    out = []
    for g in raw if isinstance(raw, list) else []:
        out.append(g.get("name", "") if isinstance(g, dict) else str(g))
    return [g for g in out if g][:4]


def _meta(row):
    """Extracts optional rating/year/genres for the front-end cards."""
    meta = {}
    if "vote_average" in row:
        try: meta["rating"] = round(float(row["vote_average"]), 1)
        except Exception: pass
        
    year = None
    for col in ("release_year", "year"):
        if col in row:
            try:
                year = int(float(row[col]))
                break
            except Exception: pass
    if year is None and "release_date" in row:
        try: year = pd.to_datetime(row["release_date"]).year
        except Exception: pass
        
    if year: meta["year"] = year
    if "genres" in row:
        genres = _parse_genres(row["genres"])
        if genres: meta["genres"] = genres
    return meta


def get_recommendations(title, n=7):
    """Finds the top n most similar movies based on cosine similarity."""
    df, indices, matrix = load_data()

    if title not in indices:
        lowered = {t.lower(): t for t in indices}
        if title.lower() in lowered:
            title = lowered[title.lower()]
        else:
            return [{"error": "Movie not found", "title": title}]

    idx = indices[title]
    # Similarity of the chosen film against the entire TF-IDF matrix
    scores = cosine_similarity(matrix[idx], matrix).flatten()

    # Rank everything, drop the film itself, keep the top n
    picked = [i for i in scores.argsort()[::-1] if i != idx][:n]

    return [
        {"title": str(_row(df, i)["title"]),
         "score": round(float(scores[i]), 4),
         **_meta(_row(df, i))}
        for i in picked
    ]


def all_titles():
    """Returns a sorted list of all unique movie titles for the Streamlit dropdown."""
    df, _, _ = load_data()
    return sorted(df["title"].astype(str).unique().tolist(), key=str.lower)


def engine_stats():
    """Returns model dimensions for the UI metrics."""
    df, _, matrix = load_data()
    return {"movies": int(df.shape[0]), "features": int(matrix.shape[1])}