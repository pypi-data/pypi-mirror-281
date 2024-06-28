import abc
import uuid
from typing import Dict

from beir.retrieval.search import BaseSearch
from fastembed import TextEmbedding, SparseTextEmbedding
from qdrant_client import QdrantClient, models

from beir_qdrant.retrieval.search.qdrant import QdrantBase


class HybridQdrantSearch(QdrantBase, BaseSearch, abc.ABC):
    """
    Hybrid search using Qdrant and FastEmbed models. By default, it uses all-miniLM-L6-v2 model for dense text
    embeddings and SPLADE model for sparse text embeddings. Both results are combined using a rank fusion algorithm.
    """

    def __init__(
        self,
        qdrant_client: QdrantClient,
        collection_name: str,
        initialize: bool = True,
        vector_name: str = "dense",
        sparse_vector_name: str = "sparse",
        dense_model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        sparse_model_name: str = "prithvida/Splade_PP_en_v1",
    ):
        super().__init__(qdrant_client, collection_name, vector_name, initialize)
        self.sparse_vector_name = sparse_vector_name
        self.dense_model = TextEmbedding(model_name=dense_model_name)
        self.sparse_model = SparseTextEmbedding(model_name=sparse_model_name)

    def recreate_collection(self):
        test_dense_embedding = next(self.dense_model.query_embed("test"))
        dense_embedding_size = len(test_dense_embedding)

        self.qdrant_client.delete_collection(self.collection_name)
        self.qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config={
                self.vector_name: models.VectorParams(
                    size=dense_embedding_size,
                    distance=models.Distance.COSINE,
                )
            },
            sparse_vectors_config={
                self.sparse_vector_name: models.SparseVectorParams(
                    modifier=models.Modifier.IDF,
                )
            },
        )

    def doc_to_point(self, doc_id: str, doc: Dict[str, str]) -> models.PointStruct:
        dense_embedding = next(self.dense_model.passage_embed([doc["text"]])).tolist()
        sparse_embedding = next(self.sparse_model.embed(doc["text"])).as_object()
        return models.PointStruct(
            id=uuid.uuid4().hex,
            vector={
                self.vector_name: dense_embedding,
                self.sparse_vector_name: models.SparseVector(**sparse_embedding),
            },
            payload={"doc_id": doc_id, **doc},
        )
