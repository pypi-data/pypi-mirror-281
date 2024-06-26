from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from typing import Literal
from pydantic import Field

func = get_registry().get('sentence-transformers').create(name='nampham1106/bkcare-embedding')

class EmbeddedPassage(LanceModel):
    vector: Vector(dim=func.ndims()) == func.VectorField() # type: ignore
    chunk_id: str
    text: str = func.SourceField()

class EmbeddedPassageWithQA(LanceModel):
    vector: Vector(func.ndims()) = func.VectorField() # type: ignore
    chunk_id: str
    text: str = func.SourceField()
    source_text: str

class EmbeddedPassageWithMetadata(LanceModel):
    vector: Vector(func.ndims()) = func.VectorField() # type: ignore
    chunk_id: str
    text: str = func.SourceField()
    keywords: str
    search_queries: str

class QueryItem(LanceModel):
    query: str
    vector: list[str]