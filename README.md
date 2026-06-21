# Movie-Recommendation-System-
### `recommendation(title, n=7)` Function: A Comprehensive Overview

This function is designed to provide content-based movie recommendations. Given a movie title, it identifies and suggests other movies that are most similar in terms of their content attributes.

**How it Works:**

1.  **Input Movie Identification:**
    *   It first checks if the provided `title` exists in the `Indices` Series, which maps movie titles to their corresponding numerical indices in the DataFrame. If the movie is not found, it immediately returns a 'Movie not found' message.

2.  **TF-IDF Vectorization:**
    *   The core of the similarity calculation relies on `Tfidf_metrix`, which is a Term Frequency-Inverse Document Frequency (TF-IDF) representation of each movie's `combined_features`. The `combined_features` for each movie were created by concatenating and preprocessing its `title`, `genres`, and `tagline`.
    *   TF-IDF is a numerical statistic that reflects how important a word is to a document in a collection or corpus. It increases proportionally to the number of times a word appears in the document but is offset by the frequency of the word in the corpus, which helps to adjust for the fact that some words appear more frequently in general.

3.  **Cosine Similarity Calculation:**
    *   Once the input movie's index (`idx`) is identified, the function retrieves its TF-IDF vector from `Tfidf_metrix[idx]`.
    *   It then computes the `cosine_similarity` between this vector and all other movie vectors in `Tfidf_metrix`. Cosine similarity measures the cosine of the angle between two non-zero vectors in a multi-dimensional space. A higher cosine similarity (closer to 1) indicates greater similarity between the movie contents.
    *   The `.flatten()` method is used to convert the 2D similarity matrix (which would be 1xN for a single input movie) into a 1D array of similarity scores.

4.  **Ranking and Selection:**
    *   The `argsort()` method is applied to these similarity `score`s to get the indices that would sort the scores in ascending order. By using `[::-1]`, these indices are reversed to get the sorting order for descending similarity (most similar first).
    *   The `[0:n+1]` slicing selects the top `n+1` indices. This includes the input movie itself (which will have a similarity of 1 with itself), plus `n` other most similar movies.

5.  **Output:**
    *   Finally, it returns the `title`s from the `df` DataFrame corresponding to these top `n` similar movie indices (excluding the input movie itself if `n` refers to the number of *other* movies).

**Parameters:**

*   `title` (str): The exact title of the movie for which recommendations are desired. This title must exist in the `useFull_df['title']` column.
*   `n` (int, optional): The number of similar movies to return. The default value is 7.

**Returns:**

*   A Pandas Series containing the titles of the `n` most recommended movies.
*   If the `title` is not found in the dataset, it returns a list containing the string `"Movie not found"`.
