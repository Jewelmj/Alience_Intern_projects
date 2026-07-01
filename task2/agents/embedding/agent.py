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

        self._model = None

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

            record = chunk.copy()

            record["vector_dimension"] = len(vector)
            record["embedding"] = vector.tolist()

            embedding_records.append(record)

        logger.info(
            f"Generated {len(embedding_records)} embeddings"
        )

        return embedding_records
    
    @property
    def model(self):

        if self._model is None:

            logger.info(
                f"Loading embedding model: {EMBEDDING_MODEL}"
            )

            self._model = SentenceTransformer(
                EMBEDDING_MODEL
            )

        return self._model