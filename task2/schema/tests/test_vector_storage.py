from agents.embedding.agent import (
    EmbeddingAgent
)

from schema.utils.vector_storage import (
    save_vectors
)

from pathlib import Path


def test_vector_file_created():

    agent = EmbeddingAgent()

    chunks = [
        {
            "chunk_id": 0,
            "session_id": "test-session",
            "source_file": "sample.pdf",
            "chunk_length": 100,
            "text": "FastAPI is a web framework"
        }
    ]

    embeddings = (
        agent.generate_embeddings(
            chunks
        )
    )

    filename = save_vectors(
        "sample.pdf",
        embeddings
    )

    file_path = (
        Path("storage/vectors")
        / filename
    )

    assert file_path.exists()