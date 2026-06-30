from config.settings import LLM_PROVIDER

from llm.ollama_provider import OllamaProvider
from llm.openrouter_provider import OpenRouterProvider


def get_provider():

    if LLM_PROVIDER == "ollama":
        return OllamaProvider()
    elif LLM_PROVIDER == "openrouter":
        return OpenRouterProvider()

    raise ValueError(
        f"Unsupported LLM provider: {LLM_PROVIDER}"
    )