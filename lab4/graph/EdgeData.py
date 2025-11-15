from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

TKey = TypeVar("TKey")
TEdgeData = TypeVar("TEdgeData")

@dataclass
class EdgeData(Generic[TEdgeData, TKey]):
    id: int
    u: TKey
    v: TKey
    data: Optional[TEdgeData] = None