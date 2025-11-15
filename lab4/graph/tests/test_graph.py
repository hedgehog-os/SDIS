# test_graph.py
import pytest
from UndirecteddAdjListMultiGraph import UndirectedAdjListMultiGraph
from VertexHandle import VertexHandle
from EdgeHandle import EdgeHandle


@pytest.fixture
def graph():
    """Фикстура: чистый граф для каждого теста."""
    return UndirectedAdjListMultiGraph[str, str, str]()


# === VertexHandle tests ===
def test_vertex_handle_repr():
    h = VertexHandle("A")
    assert repr(h) == "VertexHandle('A')"
    assert h.key == "A"


# === EdgeHandle tests ===
def test_edge_handle_repr():
    h = EdgeHandle(id=1, u="A", v="B")
    assert repr(h) == "EdgeHandle(id=1, 'A', 'B')"
    assert h.endpoints() == ("A", "B")


# === UndirectedAdjListMultiGraph tests ===
class TestVertexOperations:
    def test_add_vertex_new(self, graph):
        h = graph.add_vertex("A", "dataA")
        assert h.key == "A"
        assert graph.has_vertex("A")
        assert graph.get_vertex_data("A") == "dataA"
        assert graph.num_vertices() == 1

    def test_add_vertex_update_data(self, graph):
        graph.add_vertex("A", "old")
        graph.add_vertex("A", "new")
        assert graph.get_vertex_data("A") == "new"

    def test_add_vertex_no_data(self, graph):
        h = graph.add_vertex("B")
        assert graph.get_vertex_data("B") is None

    def test_set_vertex_data(self, graph):
        graph.add_vertex("A")
        graph.set_vertex_data("A", "updated")
        assert graph.get_vertex_data("A") == "updated"

    def test_set_vertex_data_missing(self, graph):
        with pytest.raises(KeyError, match="Vertex 'X' not in graph"):
            graph.set_vertex_data("X", "data")

    def test_get_vertex_data_missing(self, graph):
        with pytest.raises(KeyError, match="Vertex 'X' not in graph"):
            graph.get_vertex_data("X")

    def test_remove_vertex(self, graph):
        graph.add_vertex("A")
        assert graph.remove_vertex("A") is True
        assert not graph.has_vertex("A")
        assert graph.num_vertices() == 0

    def test_remove_vertex_missing(self, graph):
        assert graph.remove_vertex("X") is False

    def test_remove_vertex_by_handle(self, graph):
        h = graph.add_vertex("A")
        assert graph.remove_vertex_by_handle(h) is True
        assert not graph.has_vertex("A")


class TestEdgeOperations:
    def test_add_edge_creates_vertices(self, graph):
        h = graph.add_edge("A", "B", "edge_data")
        assert graph.has_vertex("A")
        assert graph.has_vertex("B")
        assert h.id == 1
        assert h.u == "A"
        assert h.v == "B"

    def test_add_parallel_edges(self, graph):
        e1 = graph.add_edge("A", "B")
        e2 = graph.add_edge("A", "B", "data2")
        assert e1.id != e2.id
        assert graph.has_edge("A", "B")
        assert graph.num_edges() == 2

    def test_add_loop(self, graph):
        e = graph.add_edge("A", "A", "loop")
        assert graph.has_edge("A", "A")
        assert graph.num_edges() == 1

    def test_edge_id_allocation(self, graph):
        ids = [graph.add_edge(f"{i}", f"{i+1}").id for i in range(5)]
        assert ids == [1, 2, 3, 4, 5]

    def test_has_edge(self, graph):
        graph.add_edge("A", "B")
        assert graph.has_edge("A", "B")
        assert graph.has_edge("B", "A")
        assert not graph.has_edge("A", "C")

    def test_get_set_edge_data(self, graph):
        e = graph.add_edge("A", "B")
        graph.set_edge_data(e.id, "new_data")
        assert graph.get_edge_data(e.id) == "new_data"

    def test_get_edge_data_missing(self, graph):
        with pytest.raises(KeyError, match="Edge id 999 not in graph"):
            graph.get_edge_data(999)

    def test_set_edge_data_missing(self, graph):
        with pytest.raises(KeyError, match="Edge id 999 not in graph"):
            graph.set_edge_data(999, "data")

    def test_remove_edge_by_id(self, graph):
        e = graph.add_edge("A", "B")
        assert graph.remove_edge_by_id(e.id) is True
        assert graph.num_edges() == 0
        assert not graph.has_edge("A", "B")

    def test_remove_edge_by_id_missing(self, graph):
        assert graph.remove_edge_by_id(999) is False

    def test_remove_edge_by_handle(self, graph):
        e = graph.add_edge("A", "B")
        assert graph.remove_edge_by_handle(e) is True
        assert graph.num_edges() == 0

    def test_remove_all_edges_between(self, graph):
        graph.add_edge("A", "B")
        graph.add_edge("A", "B", "second")
        assert graph.remove_all_edges_between("A", "B") == 2
        assert graph.num_edges() == 0

    def test_remove_all_edges_between_no_edges(self, graph):
        assert graph.remove_all_edges_between("A", "B") == 0


class TestIteratorsAndViews:
    def test_vertices_iterator(self, graph):
        graph.add_vertex("C")
        graph.add_vertex("A")
        graph.add_vertex("B")
        keys = [h.key for h in graph.vertices()]
        assert sorted(keys) == ["A", "B", "C"]

    def test_vertices_reversed(self, graph):
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        keys = [h.key for h in graph.vertices_reversed()]
        assert keys == ["C", "B", "A"]

    def test_edges_iterator(self, graph):
        e1 = graph.add_edge("A", "B")
        e2 = graph.add_edge("B", "C")
        edges = list(graph.edges())
        assert len(edges) == 2
        assert edges[0].id < edges[1].id

    def test_edges_reversed(self, graph):
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        ids = [e.id for e in graph.edges_reversed()]
        assert ids == [2, 1]

    def test_neighbors(self, graph):
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("A", "A")
        nb = sorted([h.key for h in graph.neighbors("A")])
        assert nb == ["A", "B", "C"]

    def test_neighbors_reversed(self, graph):
        graph.add_edge("A", "X")
        graph.add_edge("A", "Y")
        graph.add_edge("A", "Z")
        nb = [h.key for h in graph.neighbors_reversed("A")]
        assert nb == ["Z", "Y", "X"]

    def test_incident_edges(self, graph):
        e1 = graph.add_edge("A", "B")
        e2 = graph.add_edge("A", "C")
        e3 = graph.add_edge("A", "A")
        inc = {(e.u, e.v) for e in graph.incident_edges("A")}
        assert inc == {("A", "B"), ("A", "C"), ("A", "A")}

    def test_incident_edges_reversed(self, graph):
        graph.add_edge("A", "X")
        graph.add_edge("A", "Y")
        graph.add_edge("A", "Z")
        ids = [e.id for e in graph.incident_edges_reversed("A")]
        assert ids == [3, 2, 1]

    def test_vertices_view(self, graph):
        graph.add_vertex("A", "dataA")
        graph.add_vertex("B")
        view = graph.vertices_view()
        assert view == (("A", "dataA"), ("B", None))

    def test_edges_view(self, graph):
        graph.add_edge("A", "B", "e1")
        graph.add_edge("B", "C")
        view = graph.edges_view()
        assert view == ((1, "A", "B", "e1"), (2, "B", "C", None))

    def test_neighbors_view(self, graph):
        graph.add_edge("A", "X")
        graph.add_edge("A", "Y")
        view = graph.neighbors_view("A")
        assert view == ("X", "Y") or view == ("Y", "X")


class TestDegreeCalculations:
    def test_degree_vertex_simple(self, graph):
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        assert graph.degree_vertex("A") == 2
        assert graph.degree_vertex("B") == 1

    def test_degree_vertex_with_parallel(self, graph):
        graph.add_edge("A", "B")
        graph.add_edge("A", "B")
        assert graph.degree_vertex("A") == 2
        assert graph.degree_vertex("B") == 2

    def test_degree_edge(self, graph):
        e1 = graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        graph.add_edge("A", "B")  # parallel
        assert graph.degree_edge(e1.id) == 3  # edges to C, D, and parallel

    def test_degree_edge_loop(self, graph):
        e_loop = graph.add_edge("A", "A")
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        assert graph.degree_edge(e_loop.id) == 2  # edges to B and C


class TestClear:
    def test_clear(self, graph):
        graph.add_vertex("A")
        graph.add_edge("A", "B")
        graph.clear()
        assert graph.num_vertices() == 0
        assert graph.num_edges() == 0
        assert graph._next_edge_id == 1


class TestRepr:
    def test_graph_repr(self, graph):
        graph.add_vertex("A")
        graph.add_edge("A", "B")
        assert repr(graph) == "UndirectedAdjListMultiGraph(V=2, E=1)"


class TestErrorHandling:
    def test_degree_vertex_missing(self, graph):
        with pytest.raises(KeyError):
            graph.degree_vertex("X")

    def test_neighbors_missing(self, graph):
        with pytest.raises(KeyError):
            list(graph.neighbors("X"))

    def test_incident_edges_missing(self, graph):
        with pytest.raises(KeyError):
            list(graph.incident_edges("X"))

    def test_degree_edge_missing(self, graph):
        with pytest.raises(KeyError):
            graph.degree_edge(999)