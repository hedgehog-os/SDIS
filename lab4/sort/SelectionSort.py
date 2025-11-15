from __future__ import annotations
from typing import List, Callable, TypeVar, Optional

T = TypeVar("T")

class SelectionSort:
    """Implementation of Selection Sort for arbitrary comparable objects.

    This algorithm performs in-place or out-of-place sorting by repeatedly selecting
    the minimum element from the unsorted portion and placing it at the beginning.
    It supports custom comparison logic via a key function, allowing flexible sorting
    of complex data structures.

    Selection Sort is simple and predictable, making it suitable for small datasets
    or educational purposes. However, its quadratic time complexity limits its use
    for large-scale sorting tasks.
    """

    def sort(data: List[T], key: Optional[Callable[[T], object]] = None, inplace: bool = False) -> List[T]:
        """Return a sorted list built using the Selection Sort algorithm.

        Args:
            data: List of elements to sort.
            key: Optional function that extracts a comparison key from each element,
                similar to the built-in `sorted`.
            inplace: If True, the input list is sorted in place and returned.
                If False, a new sorted list is returned.

        Returns:
            A list containing the sorted elements from `data`, either as a new list
            or the modified original, depending on `inplace`.
        """

        arr = data if inplace else data.copy()
        n = len(arr)

        def less(a: T, b: T) -> bool:
            if key is not None:
                return key(a) < key(b)
            else:
                return a < b

        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                if less(arr[j], arr[min_idx]):
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
            
        return arr
    
    def __repr__(self):
        return str(self.sort())