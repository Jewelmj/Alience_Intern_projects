from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from main import app
from agents.embedding.agent import EmbeddingAgent
from database.vector_repository import save_embeddings
from database.analytics_repository import AnalyticsRepository

analytics_repository = AnalyticsRepository()
client = TestClient(app)


def _seed_embeddings(
    text,
    source_file="test_chat.pdf",
    session_id="test-session",
    chunk_id=0
):

    embedding_agent = EmbeddingAgent()

    chunks = [
        {
            "chunk_id": chunk_id,
            "session_id": session_id,
            "source_file": source_file,
            "chunk_length": len(text),
            "text": text,
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


@patch("agents.retrieval.agent.get_provider")
def test_retrieval_metrics_saved(mock_provider):
    mock_llm = Mock()

    mock_llm.generate.return_value = "Mock response"

    mock_provider.return_value = mock_llm

    _seed_embeddings(
        "ZyxUniqueToken98765 describes a specialized widget processor."
    )

    response = client.post(
        "/chat",
        json={
            "query": "What is ZyxUniqueToken98765?",
            "session_id": "test-session"
        }
    )

    assert response.status_code == 200

    data = response.json()

    interaction_id = data["interaction_id"]

    record = analytics_repository.get_by_id(interaction_id)

    assert record is not None

    assert "retrieval_latency_ms" in record
    assert "top_k_used" in record
    assert "raw_chunk_count" in record
    assert "filtered_chunk_count" in record
    assert "retrieval_success" in record


@patch("agents.retrieval.agent.get_provider")
def test_similarity_scores_saved(mock_provider):
    _seed_embeddings(
        "Unique analytics testing document."
    )

    mock_llm = Mock()

    mock_llm.generate.return_value = "Mock response"

    mock_provider.return_value = mock_llm

    response = client.post(
        "/chat",
        json={
            "query": "analytics",
            "session_id": "test-session"
        }
    )

    interaction_id = response.json()["interaction_id"]

    record = analytics_repository.get_by_id(interaction_id)

    assert isinstance(
        record["similarity_scores"],
        list
    )

    assert len(
        record["similarity_scores"]
    ) > 0

    assert all(
        isinstance(score, float)
        for score in record["similarity_scores"]
    )


@patch("agents.retrieval.agent.get_provider")
def test_successful_retrieval_sets_success_flag(mock_provider):
    mock_llm = Mock()

    mock_llm.generate.return_value = "Mock response"

    mock_provider.return_value = mock_llm

    _seed_embeddings(
        "FastAPI retrieval metrics testing."
    )

    response = client.post(
        "/chat",
        json={
            "query": "FastAPI",
            "session_id": "test-session"
        }
    )

    interaction_id = response.json()["interaction_id"]

    record = analytics_repository.get_by_id(interaction_id)

    assert record["retrieval_success"] is True

    assert (
        record["filtered_chunk_count"]
        > 0
    )


def test_failed_retrieval_sets_failure_flag():

    response = client.post(
        "/chat",
        json={
            "query": "ThisQueryShouldNeverMatchAnything123456",
            "session_id": "test-session"
        }
    )

    data = response.json()

    interaction_id = data["interaction_id"]

    record = analytics_repository.get_by_id(interaction_id)

    assert record["retrieval_success"] is False

    assert (
        record["filtered_chunk_count"]
        == 0
    )