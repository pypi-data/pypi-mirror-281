from __future__ import annotations
from abc import ABC, abstractmethod
from attrs import define
from typing import Optional
from griptape.artifacts import TextArtifact, ListArtifact
from griptape.rules import Ruleset


@define
class BaseQueryEngine(ABC):
    @abstractmethod
    def query(
        self,
        query: str,
        namespace: Optional[str] = None,
        *,
        rulesets: Optional[list[Ruleset]] = None,
        top_n: Optional[int] = None,
        filter: Optional[dict] = None,
    ) -> TextArtifact: ...

    @abstractmethod
    def load_artifacts(self, namespace: str) -> ListArtifact: ...

    @abstractmethod
    def upsert_text_artifact(self, artifact: TextArtifact, namespace: Optional[str] = None) -> str: ...

    @abstractmethod
    def upsert_text_artifacts(self, artifacts: list[TextArtifact], namespace: str) -> None: ...
