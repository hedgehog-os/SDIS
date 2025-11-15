from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

TKey = TypeVar("TKey")
TData = TypeVar("TData")
TEdgeData = TypeVar("TEdgeData") 

@dataclass
class VertexData(Generic[TData]):
    key: TKey
    data: Optional[TData] = None