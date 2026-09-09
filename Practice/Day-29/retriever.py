from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from document_processor import DocumentChunk


class DocumentRetriever:

    def __init__(
        self,
        documents: list[DocumentChunk]
    ):

        self.documents = documents

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
        )

        if documents:

            self.matrix = (
                self.vectorizer.fit_transform(
                    [
                        document.text
                        for document in documents
                    ]
                )
            )

        else:

            self.matrix = None

    def search(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.12
    ):

        if (
            not self.documents
            or self.matrix is None
        ):

            return []

        query_vector = (
            self.vectorizer.transform(
                [query]
            )
        )

        scores = cosine_similarity(
            query_vector,
            self.matrix
        )[0]

        # Highest score first
        ranked_indices = scores.argsort()[::-1]

        results = []

        for index in ranked_indices[:top_k]:

            score = float(
                scores[index]
            )

            if score < min_score:
                continue

            document = self.documents[
                index
            ]

            results.append(
                {
                    "text": document.text,
                    "score": score,
                    "metadata": document.metadata,
                }
            )

        return results