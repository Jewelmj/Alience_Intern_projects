from database.vector_repository import (
    search_similar
)
from schema.prompts.rag_prompt import (
    build_rag_messages
)
from schema.utils.ollama_client import (
    generate_chat_response,
    OllamaError
)
from config.settings import (
    RETRIEVAL_TOP_K,
    RELEVANCE_MAX_DISTANCE,
    NOT_FOUND_MESSAGE
)
from config.logger import logger


class RetrievalAgent:

    def __init__(
        self,
        embedding_agent
    ):
        self.embedding_agent = embedding_agent

    def _distance_to_similarity(
        self,
        distance
    ):

        return max(
            0.0,
            1.0 - (distance / 2.0)
        )

    def retrieve(
        self,
        query,
        top_k=None
    ):

        if top_k is None:
            top_k = RETRIEVAL_TOP_K

        logger.info(
            f"Searching for query: {query}"
        )

        query_embedding = (
            self.embedding_agent
            .model
            .encode(query)
            .tolist()
        )

        results = search_similar(
            query_embedding,
            top_k
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        logger.info(
            f"Retrieved {len(documents)} raw result(s)"
        )

        chunks = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            if distance > RELEVANCE_MAX_DISTANCE:
                continue

            chunks.append(
                {
                    "text": document,
                    "source_file": metadata["source_file"],
                    "chunk_id": metadata["chunk_id"],
                    "similarity_score": (
                        self._distance_to_similarity(
                            distance
                        )
                    ),
                    "distance": distance
                }
            )

        logger.info(
            f"Kept {len(chunks)} chunk(s) after relevance filtering"
        )

        return chunks

    def chat(
        self,
        query
    ):

        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty"
            )

        chunks = self.retrieve(
            query
        )

        if not chunks:

            return {
                "status": "not_found",
                "answer": NOT_FOUND_MESSAGE,
                "sources": []
            }

        messages = build_rag_messages(
            query,
            chunks
        )

        try:

            answer = generate_chat_response(
                messages
            )

        except OllamaError as exc:

            raise ValueError(
                str(exc)
            ) from exc

        sources = [
            {
                "source_file": chunk["source_file"],
                "chunk_id": chunk["chunk_id"],
                "similarity_score": round(
                    chunk["similarity_score"],
                    4
                ),
                "text_preview": chunk["text"][:200]
            }
            for chunk in chunks
        ]

        return {
            "status": "success",
            "answer": answer,
            "sources": sources
        }
