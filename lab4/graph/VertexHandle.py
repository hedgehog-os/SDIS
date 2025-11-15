from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, TypeVar

TKey = TypeVar("TKey")

@dataclass(frozen=True)
class VertexHandle(Generic[TKey]):
    key: TKey
    def __repr__(self):
        return f"VertexHandle({self.key!r})"