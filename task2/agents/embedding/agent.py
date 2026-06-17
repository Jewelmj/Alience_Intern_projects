from sentence_transformers import (
    SentenceTransformer
)

from config.settings import (
    EMBEDDING_MODEL
)

from config.logger import logger


class EmbeddingAgent:

    def __init__(self):

        logger.info(
            f"Loading embedding model: {EMBEDDING_MODEL}"
        )

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    def generate_embeddings(
        self,
        chunk_metadata
    ):

        logger.info(
            f"Generating embeddings for {len(chunk_metadata)} chunks"
        )

        texts = [
            chunk["text"]
            for chunk in chunk_metadata
        ]

        vectors = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        embedding_records = []

        for chunk, vector in zip(
            chunk_metadata,
            vectors
        ):

            embedding_records.append(
            {
                "chunk_id": chunk["chunk_id"],
                "source_file": chunk["source_file"],
                "chunk_length": chunk["chunk_length"],
                "text": chunk["text"],
                "vector_dimension": len(vector),
                "embedding": vector.tolist()
            }
        )

        logger.info(
            f"Generated {len(embedding_records)} embeddings"
        )

        return embedding_records