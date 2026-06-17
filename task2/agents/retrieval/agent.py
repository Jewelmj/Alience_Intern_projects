from database.vector_repository import (
    search_similar
)

from config.logger import logger


class RetrievalAgent:

    def __init__(
        self,
        embedding_agent
    ):
        self.embedding_agent = embedding_agent

    def retrieve(
            self,
            query,
            top_k=5
            ):

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

            logger.info(
                f"Retrieved {len(results['documents'][0])} results"
            )

            return results