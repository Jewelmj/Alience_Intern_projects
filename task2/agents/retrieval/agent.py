import time
import uuid
from datetime import datetime

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

        results = search_similar(query_embedding, session_id, top_k)

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
        
        chunks = self.retrieve(
            query, 
            session_id
        )

        similarity_scores = [
            chunk.get(
                "similarity_score",
                0.0
            )
            for chunk in chunks
        ]

        if not chunks:

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
            answer = generate_chat_response(messages)
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

                    "created_at":
                    datetime.utcnow(),

                    "feedback":
                    None
                }
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
            "interaction_id": interaction_id,
            "sources": sources
        }
