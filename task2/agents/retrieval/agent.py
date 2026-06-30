import time
import uuid
from datetime import datetime, UTC

from database.vector_repository import (
    search_similar
)
from schema.prompts.rag_prompt import (
    build_rag_messages
)
from llm.factory import get_provider
from llm.base import LLMProviderError
from schema.session.conversation_manager import (
    ConversationManager
)
from dependencies.repositories import (
    analytics_repository
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

    def retrieve(self, query, session_id, top_k=None):
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

        retrieval_start = time.time()

        results = search_similar(query_embedding, session_id, top_k)

        retrieval_latency_ms = int((time.time()- retrieval_start)* 1000)

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

        for chunk in chunks:

            logger.info(
                f"Retrieved chunk "
                f"{chunk['chunk_id']} "
                f"from {chunk['source_file']} "
                f"(similarity={chunk['similarity_score']:.4f}) "
                f"Preview: {chunk['text'][:100]}"
            )

        return {
            "chunks": chunks,
            "retrieval_latency_ms": retrieval_latency_ms,
            "top_k_used": top_k,
            "raw_chunk_count": len(documents),
            "filtered_chunk_count": len(chunks),
        }

    def chat(self, query, session_id):
        query = query.strip()

        if not query:
            raise ValueError(
                "Query cannot be empty"
            )
        
        start_time = time.time()

        interaction_id = (
            str(uuid.uuid4())
        )
        
        retrieval_data  = self.retrieve(query, session_id)
        chunks = retrieval_data["chunks"]

        similarity_scores = [
            chunk.get(
                "similarity_score",
                0.0
            )
            for chunk in chunks
        ]

        if not chunks:
            analytics_repository.save(
            {
                "interaction_id": interaction_id,
                "session_id": session_id,
                "query": query,

                "response_time_ms": int(
                    (time.time() - start_time) * 1000
                ),

                "retrieved_sources": 0,

                "similarity_scores": [],

                "retrieval_latency_ms":
                    retrieval_data["retrieval_latency_ms"],

                "top_k_used":
                    retrieval_data["top_k_used"],

                "raw_chunk_count":
                    retrieval_data["raw_chunk_count"],

                "filtered_chunk_count": 0,

                "retrieval_success": False,

                "created_at": datetime.now(UTC),

                "feedback": None
            }
            )

            return {
                "status": "not_found",
                "answer": NOT_FOUND_MESSAGE,
                "interaction_id": interaction_id,
                "sources": []
            }
        
        history = (ConversationManager.get_history(session_id))

        history_text = "\n".join(
            f"{item['role']}: {item['message']}"
            for item in history
        )

        messages = build_rag_messages(
            query,
            chunks,
            history_text
        )

        try:
            provider = get_provider()
            answer = provider.generate(messages)
            response_time_ms = int(
                (
                    time.time()
                    - start_time
                )
                * 1000
            )

            ConversationManager.add_turn(
                session_id,
                "user",
                query
            )

            ConversationManager.add_turn(
                session_id,
                "assistant",
                answer
            )

            analytics_repository.save(
                {
                    "interaction_id":
                    interaction_id,

                    "session_id":
                    session_id,

                    "query":
                    query,

                    "response_time_ms":
                    response_time_ms,

                    "retrieved_sources":
                    len(chunks),

                    "similarity_scores":
                    similarity_scores,

                    "retrieval_latency_ms":
                    retrieval_data["retrieval_latency_ms"],

                    "top_k_used":
                    retrieval_data["top_k_used"],

                    "raw_chunk_count":
                    retrieval_data["raw_chunk_count"],

                    "filtered_chunk_count":
                    retrieval_data["filtered_chunk_count"],

                    "retrieval_success":
                    len(chunks) > 0,

                    "created_at":
                    datetime.now(UTC),

                    "feedback":
                    None
                }
            )

        except LLMProviderError as exc:

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
            "interaction_id": interaction_id,
            "sources": sources
        }
