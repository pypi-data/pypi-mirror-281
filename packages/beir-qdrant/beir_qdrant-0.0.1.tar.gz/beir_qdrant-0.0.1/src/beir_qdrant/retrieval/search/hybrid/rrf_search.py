from typing import List

from qdrant_client import models

from beir_qdrant.retrieval.search.hybrid import HybridQdrantSearch


class RRFHybridQdrantSearch(HybridQdrantSearch):
    """
    Hybrid search using Qdrant and FastEmbed models and Rank Reciprocal Fusion (RRF) strategy.
    """

    def handle_query(self, query: str, limit: int) -> List[models.ScoredPoint]:
        dense_embedding = next(self.dense_model.query_embed(query)).tolist()
        sparse_embedding = next(self.sparse_model.embed(query)).as_object()
        results = self.qdrant_client.query_points(
            self.collection_name,
            prefetch=[
                models.Prefetch(
                    query=sparse_embedding, using=self.sparse_vector_name, limit=limit
                ),
                models.Prefetch(
                    query=dense_embedding, using=self.vector_name, limit=limit
                ),
            ],
            query=models.Fusion.RRF,
            limit=limit,
        )
        return results.points
