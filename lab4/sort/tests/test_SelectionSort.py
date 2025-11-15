from sort.SelectionSort import SelectionSort

def test_selection_sort_basic():
    assert SelectionSort.sort([3, 1, 2]) == [1, 2, 3]

def test_selection_sort_inplace():
    data = [5, 4, 3]
    SelectionSort.sort(data, inplace=True)
    assert data == [3, 4, 5]

def test_selection_sort_key():
    items = ["pear", "kiwi", "banana"]
    result = SelectionSort.sort(items, key=len)
    assert [len(x) for x in result] == sorted([len(x) for x in items])

def test_selection_repr():
    class S(SelectionSort):
        def sort(data): return [1, 2, 3]
    assert S().__repr__() == "[1, 2, 3]"
