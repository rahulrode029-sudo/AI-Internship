from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentRetriever:

    def __init__(self, documents: list[str]):
        self.documents = documents

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        if documents:
            self.matrix = self.vectorizer.fit_transform(
                documents
            )
        else:
            self.matrix = None

    def search(
        self,
        query: str,
        top_k: int = 3
    ) -> list[tuple[str, float]]:

        if not self.documents:
            return []

        if self.matrix is None:
            return []

        query_vector = self.vectorizer.transform(
            [query]
        )

        scores = cosine_similarity(
            query_vector,
            self.matrix
        )[0]

        ranked_indices = scores.argsort()[::-1]

        results = []

        for index in ranked_indices[:top_k]:

            score = float(scores[index])

            if score > 0:
                results.append(
                    (
                        self.documents[index],
                        score
                    )
                )

        return results