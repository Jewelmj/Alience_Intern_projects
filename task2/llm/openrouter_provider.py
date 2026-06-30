from openai import OpenAI

from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_BASE_URL,
)

from llm.base import (
    BaseLLMProvider,
    LLMProviderError,
)

class OpenRouterProvider(BaseLLMProvider):

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
        )

    def generate(
        self,
        messages: list[dict],
    ) -> str:

        try:

            response = (
                self.client.chat.completions.create(
                    model=OPENROUTER_MODEL,
                    messages=messages,
                )
            )

            return (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

        except Exception as exc:
            raise LLMProviderError(
                "Failed to reach OpenRouter."
            ) from exc