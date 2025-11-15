from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar, Tuple

TKey = TypeVar("TKey")
TEdgeData = TypeVar("TEdgeData")

@dataclass(frozen=True)
class EdgeHandle(Generic[TEdgeData, TKey]):
    id: int
    u: TKey
    v: TKey
    def endpoints(self) -> Tuple[TKey, TKey]:
        return (self.u, self.v)
    def __repr__(self):
        return f"EdgeHandle(id={self.id}, {self.u!r}, {self.v!r})"