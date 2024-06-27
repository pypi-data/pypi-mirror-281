from abc import ABC, abstractmethod


class LLM(ABC):

    @abstractmethod
    async def call(self, query: str, temperature: float = 0.6) -> str:
        pass
