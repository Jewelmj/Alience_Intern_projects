from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from main import app
from agents.embedding.agent import (
    EmbeddingAgent
)
from database.vector_repository import (
    save_embeddings
)
from llm.base import LLMProviderError

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
            "text": text
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


def test_chat_empty_query():

    response = client.post(
        "/chat",
        json={
            "query": "   ",
            "session_id": "test-session"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "error"
    assert "empty" in data["message"].lower()


def test_chat_not_found_without_relevant_documents():
    response = client.post(
        "/chat",
        json={
            "query": "quantum teleportation in uploaded files",
            "session_id": "test-session"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "not_found"
    assert data["sources"] == []
    assert "could not find" in data["answer"].lower()


@patch("agents.retrieval.agent.get_provider")
def test_chat_with_relevant_context(mock_provider):
    mock_llm = Mock()

    mock_llm.generate.return_value = (
        "FastAPI is a Python web framework."
    )

    mock_provider.return_value = mock_llm

    _seed_embeddings(
        "ZyxUniqueToken98765 describes a specialized widget processor.",
        source_file="unique_widget_doc.pdf"
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

    assert data["status"] == "success"
    assert data["answer"] == "FastAPI is a Python web framework."
    assert len(data["sources"]) >= 1
    assert data["sources"][0]["source_file"] == "unique_widget_doc.pdf"
    assert data["sources"][0]["similarity_score"] > 0

    mock_provider.assert_called_once()


@patch("agents.retrieval.agent.get_provider",)
def test_chat_ollama_failure_returns_error(mock_provider):
    mock_llm = Mock()

    mock_llm.generate.side_effect = (
        LLMProviderError(
            "Failed to reach the language model."
        )
    )

    mock_provider.return_value = mock_llm

    _seed_embeddings(
        "Some indexed document text about databases."
    )

    response = client.post(
        "/chat",
        json={
            "query": "Tell me about databases",
            "session_id": "test-session"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "error"

    mock_provider.assert_called_once()


@patch("agents.retrieval.agent.get_provider",)
def test_session_isolation(mock_provider):
    mock_llm = Mock()

    mock_llm.generate.side_effect = (
        LLMProviderError(
            "Failed to reach the language model."
        )
    )

    mock_provider.return_value = mock_llm

    _seed_embeddings(
        "FastAPI is a modern Python web framework.",
        source_file="fastapi.pdf",
        session_id="session-a"
    )

    response = client.post(
        "/chat",
        json={
            "query": "What is FastAPI?",
            "session_id": "session-b"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "not_found"
    assert data["sources"] == []

    mock_provider.assert_not_called()