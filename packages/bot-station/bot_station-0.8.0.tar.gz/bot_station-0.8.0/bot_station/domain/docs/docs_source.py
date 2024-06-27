from abc import ABC, abstractmethod

from bot_station.domain.docs.model.documents_search_result import DocumentsSearchResult


class DocsSource(ABC):

    @abstractmethod
    async def load(self):
        pass

    @abstractmethod
    async def get_relevant_docs(
            self,
            query: str,
            min_score: float = 0.8,
            limit: int = 10
    ) -> DocumentsSearchResult:
        pass

    @abstractmethod
    async def close(self):
        pass
