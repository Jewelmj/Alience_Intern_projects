from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate(self,messages: list[dict],) -> str:
        pass

class LLMProviderError(Exception):
    pass