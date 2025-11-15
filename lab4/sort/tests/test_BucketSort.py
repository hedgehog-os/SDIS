import pytest
from sort.BucketSort import BucketSort

class Dummy:
    def __init__(self, value):
        self.value = value
    def __lt__(self, other):
        return self.value < other.value
    def __repr__(self):
        return f"Dummy({self.value})"

@pytest.mark.parametrize("data,expected", [
    ([], []),
    ([42], [42]),
    ([1, 2, 3], [1, 2, 3]),
    ([3, 2, 1], [1, 2, 3]),
    ([5, 5, 5], [5, 5, 5]),
])
def test_basic_cases(data, expected):
    assert BucketSort.sort(data) == expected

def test_inplace_true():
    data = [4, 2, 5, 1]
    BucketSort.sort(data, inplace=True)
    assert data == [1, 2, 4, 5]

def test_inplace_false():
    data = [4, 2, 5, 1]
    result = BucketSort.sort(data, inplace=False)
    assert result == [1, 2, 4, 5]
    assert data == [4, 2, 5, 1]

def test_key_function():
    data = ["apple", "banana", "pear", "kiwi"]
    result = BucketSort.sort(data, key=len)
    assert [len(x) for x in result] == sorted([len(x) for x in data])

def test_custom_bucket_count():
    data = [0.1, 0.2, 0.3, 0.4, 0.5]
    result = BucketSort.sort(data, bucket_count=3)
    assert result == sorted(data)

def test_bucket_count_one():
    data = [9, 3, 5, 1]
    result = BucketSort.sort(data, bucket_count=1)
    assert result == sorted(data)

def test_bucket_count_exceeds_data():
    data = [3, 1]
    result = BucketSort.sort(data, bucket_count=10)
    assert result == sorted(data)

def test_repr_output():
    class CustomSort(BucketSort):
        def sort(data, **kwargs):
            return [1, 2, 3]
    assert CustomSort().__repr__() == "[1, 2, 3]"

def test_custom_objects():
    items = [Dummy(3), Dummy(1), Dummy(2)]
    sorted_items = BucketSort.sort(items, key=lambda x: x.value)
    assert [x.value for x in sorted_items] == [1, 2, 3]

