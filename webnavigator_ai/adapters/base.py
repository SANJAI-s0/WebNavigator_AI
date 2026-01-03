# webnavigator_ai/adapters/base.py
from abc import ABC, abstractmethod
from typing import List
from webnavigator_ai.utils.schema import NormalizedSearchResult

class BaseSearchAdapter(ABC):
    @abstractmethod
    def search(self, query: str) -> List[NormalizedSearchResult]:
        ...
