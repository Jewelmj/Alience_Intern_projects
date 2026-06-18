from agents.embedding.agent import (
    EmbeddingAgent
)

from database.vector_repository import (
    save_embeddings,
    search_similar
)


def test_similarity_search():

    embedding_agent = (
        EmbeddingAgent()
    )

    chunks = [
        {
            "chunk_id": 0,
            "session_id": "test-session",
            "source_file": "test.pdf",
            "chunk_length": 10,
            "text": "FastAPI is a Python framework"
        },
        {
            "chunk_id": 1,
            "session_id": "test-session",
            "source_file": "test.pdf",
            "chunk_length": 10,
            "text": "MongoDB is a NoSQL database"
        }
    ]

    embeddings = (
        embedding_agent.generate_embeddings(
            chunks
        )
    )

    save_embeddings(
        embeddings
    )

    query_embedding = (
        embedding_agent.model
        .encode(
            "What is FastAPI?"
        )
        .tolist()
    )

    results = search_similar(
        query_embedding,
        top_k=1
    )

    assert len(
        results["documents"][0]
    ) > 0