from __future__ import annotations
from typing import Dict, Set, Tuple, Iterator, Generic, TypeVar, Optional
from EdgeData import EdgeData
from EdgeHandle import EdgeHandle
from VertexData import VertexData
from VertexHandle import VertexHandle

TKey = TypeVar("TKey")
TData = TypeVar("TData")
TEdgeData = TypeVar("TEdgeData")

class UndirectedAdjListMultiGraph(Generic[TKey, TData, TEdgeData]):
    """
    Неориентированный мультиграф (список смежности), вершины хранят данные.
    - Вершины индексируются ключом (hashable) TKey.
    - Каждое ребро имеет уникальный целочисленный id и может хранить data.
    """
    def __init__(self):
        self._vertices: Dict[TKey, VertexData] = {}
        self._adj: Dict[TKey, Dict[TKey, Set[int]]] = {}
        self._edges: Dict[int, EdgeData] = {}
        self._next_edge_id: int = 1

    # Vertex methods
    def add_vertex(self, key: TKey, data: Optional[TData] = None) -> VertexHandle[TKey]:
        """Добавляет вершину (если уже есть — обновляет data)."""
        if key in self._vertices:
    
            if data is not None:
                self._vertices[key].data = data
        else:
            self._vertices[key] = VertexData(key=key, data=data)
            self._adj[key] = {}
        return VertexHandle(key)

    def has_vertex(self, key: TKey) -> bool:
        return key in self._vertices

    def get_vertex_data(self, key: TKey) -> Optional[TData]:
        if key not in self._vertices:
            raise KeyError(f"Vertex {key!r} not in graph")
        return self._vertices[key].data

    def set_vertex_data(self, key: TKey, data: TData) -> None:
        if key not in self._vertices:
            raise KeyError(f"Vertex {key!r} not in graph")
        self._vertices[key].data = data

    def num_vertices(self) -> int:
        return len(self._vertices)

    def remove_vertex(self, key: TKey) -> bool:
        """Удаляет вершину и все инцидентные рёбра."""
        if key not in self._vertices:
            return False
        
        incident_ids = set()
        for edge_set in self._adj[key].items():
            incident_ids.update(edge_set)
        
        for eid in list(incident_ids):
            self.remove_edge_by_id(eid)
        
        del self._adj[key]
        del self._vertices[key]
        
        return True

    def remove_vertex_by_handle(self, h: VertexHandle[TKey]) -> bool:
        return self.remove_vertex(h.key)

    def degree_vertex(self, key: TKey) -> int:
        """Степень вершины — число инцидентных рёбер (с учётом кратности)."""
        if key not in self._adj:
            raise KeyError(f"Vertex {key!r} not in graph")
        total = 0
        for edge_set in self._adj[key].values():
            total += len(edge_set)

        loop_set = self._adj[key].get(key, set())
        loop_count = len(loop_set)

        return total + loop_count

    # Edge methods
    def _alloc_edge_id(self) -> int:
        eid = self._next_edge_id
        self._next_edge_id += 1
        return eid

    def add_edge(self, u: TKey, v: TKey, data: Optional[TEdgeData] = None) -> EdgeHandle:
        """Добавляет ребро (включая параллельные). Создаёт вершины, если их нет."""
        self.add_vertex(u)
        self.add_vertex(v)
        eid = self._alloc_edge_id()
        e = EdgeData(id=eid, u=u, v=v, data=data)
        self._edges[eid] = e
        self._adj[u].setdefault(v, set()).add(eid)
        if u != v:
            self._adj[v].setdefault(u, set()).add(eid)
        else:
            pass
        return EdgeHandle(id=eid, u=u, v=v)

    def has_edge(self, u: TKey, v: TKey) -> bool:
        if u not in self._adj:
            return False
        return v in self._adj[u] and len(self._adj[u][v]) > 0

    def num_edges(self) -> int:
        return len(self._edges)

    def get_edge_data(self, edge_id: int) -> Optional[TEdgeData]:
        if edge_id not in self._edges:
            raise KeyError(f"Edge id {edge_id} not in graph")
        return self._edges[edge_id].data

    def set_edge_data(self, edge_id: int, data: TEdgeData) -> None:
        if edge_id not in self._edges:
            raise KeyError(f"Edge id {edge_id} not in graph")
        self._edges[edge_id].data = data

    def remove_edge_by_id(self, edge_id: int) -> bool:
        """Удаляет конкретное ребро по его id."""
        if edge_id not in self._edges:
            return False
        e = self._edges.pop(edge_id)
        u, v = e.u, e.v
        # убрать из adjacency
        if u in self._adj and v in self._adj[u]:
            self._adj[u][v].discard(edge_id)
            if len(self._adj[u][v]) == 0:
                del self._adj[u][v]
        if u != v:
            if v in self._adj and u in self._adj[v]:
                self._adj[v][u].discard(edge_id)
                if len(self._adj[v][u]) == 0:
                    del self._adj[v][u]
        return True

    def remove_all_edges_between(self, u: TKey, v: TKey) -> int:
        """Удаляет все рёбра между u и v, возвращает число удалённых рёбер."""
        if u not in self._adj or v not in self._adj[u]:
            return 0
        ids = list(self._adj[u][v])
        for eid in ids:
            self.remove_edge_by_id(eid)
        return len(ids)

    def remove_edge_by_handle(self, h: EdgeHandle) -> bool:
        return self.remove_edge_by_id(h.id)

    def incident_edges(self, key: TKey) -> Iterator[EdgeHandle]:
        """Итератор по всем инцидентным рёбрам (включая петли), возвращает EdgeHandle."""
        if key not in self._adj:
            raise KeyError(f"Vertex {key!r} not in graph")
        seen: Set[int] = set()
        for nb, eids in self._adj[key].items():
            for eid in eids:
                if eid in seen:
                    continue
                seen.add(eid)
                e = self._edges[eid]
                yield EdgeHandle(id=eid, u=e.u, v=e.v)

    def incident_edges_reversed(self, key: TKey) -> Iterator[EdgeHandle]:
        for e in reversed(list(self.incident_edges(key))):
            yield e

    def neighbors(self, key: TKey) -> Iterator[VertexHandle]:
        if key not in self._adj:
            raise KeyError(f"Vertex {key!r} not in graph")
        for nb in self._adj[key].keys():
            yield VertexHandle(nb)

    def neighbors_reversed(self, key: TKey) -> Iterator[VertexHandle]:
        for nb in reversed(list(self._adj[key].keys())):
            yield VertexHandle(nb)

    def edges(self) -> Iterator[EdgeHandle]:
        """Итератор по всем рёбрам (порядок по id)."""
        for eid in sorted(self._edges.keys()):
            e = self._edges[eid]
            yield EdgeHandle(id=eid, u=e.u, v=e.v)

    def edges_reversed(self) -> Iterator[EdgeHandle]:
        for eid in sorted(self._edges.keys(), reverse=True):
            e = self._edges[eid]
            yield EdgeHandle(id=eid, u=e.u, v=e.v)

    def vertices(self) -> Iterator[VertexHandle]:
        for k in self._vertices.keys():
            yield VertexHandle(k)

    def vertices_reversed(self) -> Iterator[VertexHandle]:
        for k in reversed(list(self._vertices.keys())):
            yield VertexHandle(k)

    # degree of edge
    def degree_edge(self, edge_id: int) -> int:
        """
        Степень ребра (в мультиграфе): число других рёбер, инцидентных этому ребру,
        то есть имеющих общую вершину с данным ребром. Само ребро не считается.
        """
        if edge_id not in self._edges:
            raise KeyError(f"Edge id {edge_id} not in graph")
        e = self._edges[edge_id]
        u, v = e.u, e.v
        incident_ids = set()
        if u in self._adj:
            for s in self._adj[u].values():
                incident_ids.update(s)
        if v in self._adj:
            for s in self._adj[v].values():
                incident_ids.update(s)

        incident_ids.discard(edge_id)
        return len(incident_ids)

    # views / utils
    def vertices_view(self) -> Tuple[Tuple[TKey, Optional[TData]], ...]:
        """Константный просмотр: кортеж (key, data)"""
        return tuple((k, self._vertices[k].data) for k in self._vertices.keys())

    def edges_view(self) -> Tuple[Tuple[int, TKey, TKey, Optional[TEdgeData]], ...]:
        """Константный просмотр ребер: (id, u, v, data)"""
        return tuple((eid, e.u, e.v, e.data) for eid, e in sorted(self._edges.items(), key=lambda x: x[0]))

    def neighbors_view(self, key: TKey) -> Tuple[TKey, ...]:
        return tuple(self._adj[key].keys())

    def clear(self) -> None:
        self._vertices.clear()
        self._adj.clear()
        self._edges.clear()
        self._next_edge_id = 1

    def __repr__(self):
        return f"UndirectedAdjListMultiGraph(V={self.num_vertices()}, E={self.num_edges()})"