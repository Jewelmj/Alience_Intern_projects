import httpx

from config.settings import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT
)
from config.logger import logger

from llm.base import BaseLLMProvider, LLMProviderError

class OllamaProvider(BaseLLMProvider):
    def generate(self,messages: list[dict],) -> str:
        url = (
            f"{OLLAMA_BASE_URL.rstrip('/')}"
            f"/api/chat"
        )

        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False
        }

        logger.info(
            f"Calling Ollama model: {OLLAMA_MODEL}"
        )

        try:

            response = httpx.post(
                url,
                json=payload,
                timeout=OLLAMA_TIMEOUT
            )

            response.raise_for_status()

        except httpx.HTTPError as exc:

            logger.exception(
                f"Ollama request failed: {exc}"
            )

            raise LLMProviderError(
                "Failed to reach the language model. "
                "Ensure Ollama is running and the model is installed."
            ) from exc

        data = response.json()

        message = data.get(
            "message",
            {}
        )

        content = message.get(
            "content",
            ""
        ).strip()

        if not content:

            raise LLMProviderError(
                "The language model returned an empty response."
            )

        return content
