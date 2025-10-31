import pytest
from Multiset import Multiset

def test_atomic_elements():
    m = Multiset('{a, b, a}')
    assert m.cardinality() == 3
    assert m.multiset == {'a': 2, 'b': 1}
    assert 'a' in m
    assert 'b' in m
    assert 'c' not in m

def test_nested_multisets():
    m = Multiset('{a, {b, b}, a}')
    nested = Multiset('{b, b}')
    assert m.cardinality() == 3
    assert m.multiset == {'a': 2, nested: 1}
    assert nested in m
    assert 'a' in m
    assert Multiset('{b}') not in m

def test_empty_multiset():
    m = Multiset('{}')
    assert m.is_empty()
    assert m.cardinality() == 0
    assert repr(m) == "Multiset({})"

def test_delete_and_ndelete():
    m = Multiset('{x, x, y}')
    m.ndelete('x', 1)
    assert m.multiset == {'x': 1, 'y': 1}
    m.ndelete('x', 1)
    assert 'x' not in m
    m.delete('y')
    assert m.is_empty()

def test_union_and_addition():
    m1 = Multiset('{a, b}')
    m2 = Multiset('{b, c}')
    expected = Multiset('{a, b, b, c}')
    m1 += m2
    assert m1 == expected

def test_subtraction():
    m1 = Multiset('{a, b, b}')
    m2 = Multiset('{b}')
    result = m1 - m2
    expected = Multiset('{a, b}')
    assert result == expected
    m1 -= m2
    assert m1 == expected

def test_intersection():
    m1 = Multiset('{a, b, b}')
    m2 = Multiset('{b, b, c}')
    inter = m1 * m2
    expected = Multiset('{b, b}')
    assert inter == expected
    m1 *= m2
    assert m1 == expected

def test_bolean():
    m = Multiset('{x, x}')
    bolean = m.bolean()
    expected = [
        Multiset('{}'),
        Multiset('{x}'),
        Multiset('{x, x}')
    ]
    for subset in expected:
        assert subset in bolean
    assert len(bolean) == 3
    assert all(isinstance(sub, Multiset) for sub in bolean)

def test_repr_and_eq_and_hash():
    m1 = Multiset('{a, b}')
    m2 = Multiset('{a, b}')
    assert repr(m1) == repr(m2)
    assert m1 == m2
    assert hash(m1) == hash(m2)
    assert m1 != Multiset('{a, b, b}')

def test_empty_nested_multiset():
    m = Multiset('{{}}')
    inner = Multiset('{}')
    assert m.cardinality() == 1
    assert inner in m
    assert not m.is_empty()

def test_mixed_nested_and_atomic():
    m = Multiset('{a, {b}, a, {}}')
    assert m.cardinality() == 4
    assert 'a' in m
    assert Multiset('{b}') in m
    assert Multiset('{}') in m

def test_redundant_nesting():
    m = Multiset('{{a}}')
    inner = Multiset('{a}')
    assert inner in m
    assert m.cardinality() == 1
    assert 'a' not in m

def test_multiple_empty_sets():
    m = Multiset('{{}, {}, {}}')
    empty = Multiset('{}')
    assert m.cardinality() == 3
    assert m.multiset[empty] == 3
    assert not m.is_empty()

def test_whitespace_and_commas():
    m = Multiset('{  a ,   b , {  c ,  } , }')
    assert 'a' in m
    assert 'b' in m
    assert Multiset('{c}') in m
    assert m.cardinality() == 3

def test_invalid_but_tolerated_structure():
    m = Multiset('{a, {b, {}}}')
    assert 'a' in m
    assert Multiset('{b, {}}') in m
    assert m.cardinality() == 2

def test_hash_and_repr():
    ms = Multiset('{a, b, a}')
    assert isinstance(hash(ms), int)
    assert repr(ms) == f"Multiset({ms.multiset})"

def test_contains_and_eq():
    ms1 = Multiset('{x, y}')
    ms2 = Multiset('{x, y}')
    assert 'x' in ms1
    assert ms1 == ms2

def test_iadd_isub_imul():
    ms1 = Multiset('{a, b, b}')
    ms2 = Multiset('{b, b, c}')
    ms1 += ms2
    assert ms1.cardinality() == 6
    ms1 -= Multiset('{b, b}')
    assert ms1.multiset['b'] == 2
    ms1 *= Multiset('{b, b, b}')
    assert ms1.multiset['b'] == 2

def test_delete_ndelete():
    ms = Multiset('{a, a, b}')
    ms.ndelete('a', 1)
    assert ms.multiset['a'] == 1
    ms.delete('a')
    assert 'a' not in ms.multiset

def test_is_empty_and_bolean():
    ms = Multiset('{}')
    assert ms.is_empty()
    ms2 = Multiset('{x, x}')
    subsets = ms2.bolean()
    assert any(isinstance(sub, Multiset) for sub in subsets)

def test_init_from_dict():
    m = Multiset({'x': 2, 'y': 1})
    assert m.cardinality() == 3
    assert m.multiset['x'] == 2
    assert 'y' in m

def test_repr_contains_hash_with_nested():
    inner = Multiset('{a}')
    outer = Multiset('{b, {a}}')
    assert repr(outer).startswith("Multiset(")
    assert inner in outer
    assert isinstance(hash(inner), int)

def test_eq_with_different_nested_structure():
    m1 = Multiset('{a, {b}}')
    m2 = Multiset('{a, {b, b}}')
    assert m1 != m2

def test_contains_with_none_and_int():
    m = Multiset('{a, b}')
    m.to_multiset(None)
    m.to_multiset(42)
    assert None in m
    assert 42 in m
    assert m.cardinality() == 4

def test_delete_nonexistent_element():
    m = Multiset('{x, y}')
    m.delete('z')  # Should not raise
    assert m.cardinality() == 2

def test_ndelete_more_than_exists():
    m = Multiset('{x}')
    m.ndelete('x', 5)
    assert m.is_empty()

def test_bolean_with_three_elements():
    m = Multiset('{a, b, c}')
    result = m.bolean()
    assert len(result) == 8  # 2^3 subsets
    assert Multiset('{a, b, c}') in result
    assert Multiset('{}') in result

def test_nested_multiset_equality_and_hash():
    m1 = Multiset('{{a, b}}')
    m2 = Multiset('{{a, b}}')
    assert m1 == m2
    assert hash(m1) == hash(m2)

def test_cardinality_with_mixed_types():
    m = Multiset('{}')
    m.to_multiset('x')
    m.to_multiset(1)
    m.to_multiset(Multiset('{y}'))
    assert m.cardinality() == 3

def test_repr_with_mixed_elements():
    m = Multiset('{}')
    m.to_multiset('x')
    m.to_multiset(Multiset('{y}'))
    r = repr(m)
    assert "Multiset(" in r
    assert "'x'" in r or "x" in r 

def test_hash_consistency_with_order():
    m1 = Multiset('{a, b, a}')
    m2 = Multiset('{b, a, a}')
    assert hash(m1) == hash(m2)

def test_eq_with_non_multiset_type():
    m = Multiset('{x}')
    assert m != {'x': 1}
    assert m != "Multiset({x})"
    assert m != 42

def test_repr_nested_structure():
    m = Multiset('{a, {b, c}}')
    r = repr(m)
    assert "Multiset(" in r
    assert "b" in r and "c" in r

def test_subtraction_full_removal():
    m1 = Multiset('{x, x}')
    m2 = Multiset('{x, x}')
    result = m1 - m2
    assert result.is_empty()
    m1 -= m2
    assert m1.is_empty()

def test_intersection_no_common_elements():
    m1 = Multiset('{a, b}')
    m2 = Multiset('{c, d}')
    result = m1 * m2
    assert result.is_empty()
    m1 *= m2
    assert m1.is_empty()

def test_is_empty_with_nested_empty_sets():
    m = Multiset('{{}, {}, {}}')
    assert not m.is_empty()

def test_ndelete_nonexistent_element():
    m = Multiset('{a, b}')
    m.ndelete('z', 3)
    assert m.cardinality() == 2

def test_delete_nonexistent_element_safe():
    m = Multiset('{x}')
    m.delete('y')
    assert 'x' in m

def test_cardinality_with_nested_sets():
    m = Multiset('{a, {b, b}, {c}}')
    assert m.cardinality() == 3

def test_bolean_empty():
    m = Multiset('{}')
    result = m.bolean()
    assert len(result) == 1
    assert result[0].is_empty()
