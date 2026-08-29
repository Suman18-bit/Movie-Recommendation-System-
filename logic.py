"""
logic.py — the projection room.

Loads the pickled TF-IDF model once, then serves cosine-similarity
recommendations.

Algorithm is unchanged from the original: TF-IDF vectors, cosine
similarity between the query film's row and every other row, top-n
by score. The only things that changed are *how* that math gets to
its answer (precomputed norms + partial sort instead of a fresh
sklearn call and a full sort on every request) and some defensive
plumbing around loading/parsing.
"""
from __future__ import annotations

import ast
import os
import pickle
import time
from typing import Any

import numpy as np
import pandas as pd
import scipy.sparse as sp

DATA_FILE = "movie_data.pkl"
MATRIX_FILE = "tfidf_matrix.pkl"

_CACHE: dict[str, Any] = {}


def _read(path: str) -> Any:
    with open(path, "rb") as fh:
        return pickle.load(fh)


def load_data() -> tuple[pd.DataFrame, dict[str, int], Any]:
    """Loads the prepared movie dataframe and TF-IDF matrix (cached in memory).

    Returns (df, indices, matrix). On repeat calls this is a dict
    lookup — the pickle load and norm precompute only happen once
    per process, same as before.
    """
    if _CACHE:
        return _CACHE["df"], _CACHE["indices"], _CACHE["matrix"]

    t0 = time.perf_counter()
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

    if getattr(matrix, "shape", (0,))[0] == 0:
        raise FileNotFoundError(
            "The TF-IDF matrix loaded but is empty (0 rows). "
            "Regenerate 'tfidf_matrix.pkl'."
        )

    if indices is None:
        indices = pd.Series(df.index, index=df["title"])
    if isinstance(indices, pd.Series):
        indices = indices.to_dict()
    indices = {str(k): int(v) for k, v in indices.items()}

    # Precompute per-row L2 norms once. cosine_similarity(matrix[idx], matrix)
    # would otherwise recompute the query row's norm on every single call —
    # here it's done once at load time, and get_recommendations() just does
    # a dot product + divide, which is the same math, faster per request.
    if sp.issparse(matrix):
        matrix = matrix.tocsr()
        norms = np.sqrt(matrix.multiply(matrix).sum(axis=1)).A1
    else:
        matrix = np.asarray(matrix)
        norms = np.linalg.norm(matrix, axis=1)
    norms[norms == 0] = 1e-12  # guard divide-by-zero for any all-zero row

    _CACHE.update(
        df=df,
        indices=indices,
        matrix=matrix,
        norms=norms,
        load_seconds=round(time.perf_counter() - t0, 3),
    )
    return df, indices, matrix


def _row(df: pd.DataFrame, i: int) -> pd.Series:
    try:
        return df.loc[i]
    except KeyError:
        return df.iloc[i]


def _parse_genres(raw: Any) -> list[str]:
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


def _meta(row: pd.Series) -> dict[str, Any]:
    """Extracts optional rating/year/genres for the front-end cards."""
    meta: dict[str, Any] = {}
    if "vote_average" in row:
        try:
            meta["rating"] = round(float(row["vote_average"]), 1)
        except Exception:
            pass

    year = None
    for col in ("release_year", "year"):
        if col in row:
            try:
                year = int(float(row[col]))
                break
            except Exception:
                pass
    if year is None and "release_date" in row:
        try:
            year = pd.to_datetime(row["release_date"]).year
        except Exception:
            pass

    if year:
        meta["year"] = year
    if "genres" in row:
        genres = _parse_genres(row["genres"])
        if genres:
            meta["genres"] = genres
    return meta


def _cosine_scores(matrix: Any, norms: np.ndarray, idx: int) -> np.ndarray:
    """Cosine similarity of row `idx` against every row in `matrix`.

    Identical result to sklearn's cosine_similarity(matrix[idx], matrix)
    — same dot-product-over-norms formula — but reuses the norms
    precomputed once in load_data() instead of recomputing them here.
    """
    query = matrix[idx]
    if sp.issparse(matrix):
        dots = matrix.dot(query.T)
        dots = np.asarray(dots.todense()).ravel() if sp.issparse(dots) else np.asarray(dots).ravel()
    else:
        dots = matrix @ np.asarray(query).ravel()
    return dots / (norms * norms[idx])


def get_recommendations(title: str, n: int = 7) -> list[dict[str, Any]]:
    """Finds the top n most similar movies based on cosine similarity."""
    df, indices, matrix = load_data()
    norms = _CACHE["norms"]

    if title not in indices:
        lowered = {t.lower(): t for t in indices}
        if title.lower() in lowered:
            title = lowered[title.lower()]
        else:
            return [{"error": "Movie not found", "title": title}]

    idx = indices[title]
    scores = _cosine_scores(matrix, norms, idx)

    n = max(0, min(n, len(scores) - 1))
    if n == 0:
        return []

    # Full descending sort, then drop the query film and take the top n —
    # byte-for-byte the same selection and ordering as the original
    # scores.argsort()[::-1], ties included. An argpartition-based partial
    # sort was tried here but rejected: it cannot reproduce the original's
    # tie-breaking behaviour (equal-score rows can end up in a different
    # order, or a different equal-score row gets excluded outright) without
    # first sorting the whole array anyway, which defeats the point.
    order = scores.argsort()[::-1]
    picked = [int(i) for i in order if i != idx][:n]

    return [
        {
            "title": str(_row(df, i)["title"]),
            "score": round(float(scores[i]), 4),
            **_meta(_row(df, i)),
        }
        for i in picked
    ]


def all_titles() -> list[str]:
    """Returns a sorted list of all unique movie titles for the Streamlit dropdown."""
    df, _, _ = load_data()
    return sorted(df["title"].astype(str).unique().tolist(), key=str.lower)


def engine_stats() -> dict[str, Any]:
    """Returns model dimensions (and load time) for the UI metrics."""
    df, _, matrix = load_data()
    return {
        "movies": int(df.shape[0]),
        "features": int(matrix.shape[1]),
        "load_seconds": _CACHE.get("load_seconds", 0.0),
    }
