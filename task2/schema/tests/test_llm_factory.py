from unittest.mock import patch

import pytest

from llm.factory import get_provider
from llm.ollama_provider import OllamaProvider
from llm.openrouter_provider import OpenRouterProvider


@patch("llm.factory.LLM_PROVIDER", "ollama")
def test_factory_returns_ollama_provider():

    provider = get_provider()

    assert isinstance(
        provider,
        OllamaProvider
    )


@patch("llm.factory.LLM_PROVIDER", "openrouter")
def test_factory_returns_openrouter_provider():

    provider = get_provider()

    assert isinstance(
        provider,
        OpenRouterProvider
    )


@patch("llm.factory.LLM_PROVIDER", "invalid_provider")
def test_factory_rejects_invalid_provider():

    with pytest.raises(ValueError):

        get_provider()