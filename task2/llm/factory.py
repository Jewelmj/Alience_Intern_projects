from config.settings import LLM_PROVIDER

from llm.ollama_provider import OllamaProvider


def get_provider():

    if LLM_PROVIDER == "ollama":
        return OllamaProvider()

    raise ValueError(
        f"Unsupported LLM provider: {LLM_PROVIDER}"
    )