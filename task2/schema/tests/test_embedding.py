from agents.embedding.agent import (
    EmbeddingAgent
)


def test_embedding_generation():

    agent = EmbeddingAgent()

    chunks = [
        {
            "chunk_id": 0,
            "source_file": "sample.pdf",
            "chunk_length": 100,
            "text": "FastAPI is a web framework"
        },
        {
            "chunk_id": 1,
            "source_file": "sample.pdf",
            "chunk_length": 120,
            "text": "LangChain helps build RAG systems"
        }
    ]

    embeddings = (
        agent.generate_embeddings(
            chunks
        )
    )

    assert len(embeddings) == 2