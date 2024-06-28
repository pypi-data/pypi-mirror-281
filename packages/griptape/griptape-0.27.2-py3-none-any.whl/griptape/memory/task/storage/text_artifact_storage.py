from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional
from attrs import define, field
from griptape.artifacts import TextArtifact, BaseArtifact, ListArtifact
from griptape.memory.task.storage import BaseArtifactStorage

if TYPE_CHECKING:
    from griptape.engines import BaseSummaryEngine, CsvExtractionEngine, JsonExtractionEngine, VectorQueryEngine


@define
class TextArtifactStorage(BaseArtifactStorage):
    query_engine: VectorQueryEngine = field(kw_only=True)
    summary_engine: Optional[BaseSummaryEngine] = field(kw_only=True, default=None)
    csv_extraction_engine: Optional[CsvExtractionEngine] = field(kw_only=True, default=None)
    json_extraction_engine: Optional[JsonExtractionEngine] = field(kw_only=True, default=None)

    def can_store(self, artifact: BaseArtifact) -> bool:
        return isinstance(artifact, TextArtifact)

    def store_artifact(self, namespace: str, artifact: BaseArtifact) -> None:
        if isinstance(artifact, TextArtifact):
            self.query_engine.upsert_text_artifact(artifact, namespace)
        else:
            raise ValueError("Artifact must be of instance TextArtifact")

    def load_artifacts(self, namespace: str) -> ListArtifact:
        return self.query_engine.load_artifacts(namespace)

    def summarize(self, namespace: str) -> TextArtifact:
        if self.summary_engine is None:
            raise ValueError("Summary engine is not set.")
        return self.summary_engine.summarize_artifacts(self.load_artifacts(namespace))

    def query(self, namespace: str, query: str, metadata: Any = None) -> TextArtifact:
        return self.query_engine.query(namespace=namespace, query=query, metadata=str(metadata) if metadata else None)
