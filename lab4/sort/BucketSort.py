# BucketSort_inherit.py
from __future__ import annotations
from math import floor
from typing import Optional, List, Callable, TypeVar
from SelectionSort import SelectionSort

T = TypeVar("T")

class BucketSort(SelectionSort):

    """Implementation of Bucket Sort using Selection Sort for intra-bucket ordering.

        This algorithm distributes elements into buckets based on their key values,
        assuming a roughly uniform distribution. Each bucket is then sorted individually
        using Selection Sort, making the overall process efficient for well-distributed data.

        Bucket Sort is particularly effective for numeric data with known range and
        approximate uniformity. It supports custom key functions and optional in-place sorting.
    """

    def sort(data: List[T], key: Optional[Callable[[T], object]] = None,
             bucket_count: int = 10, inplace: bool = False) -> List[T]:
        """Return a sorted list built using the Bucket Sort algorithm.

            Args:
                data: List of elements to sort.
                key: Optional function that extracts a comparison key from each element,
                    similar to the built-in `sorted`.
                bucket_count: Number of buckets to use for distribution. Higher values
                    may improve performance for uniformly distributed data.
                inplace: If True, the input list is sorted in place and returned.
                    If False, a new sorted list is returned.

            Returns:
                A list containing the sorted elements from `data`, either as a new list
                or the modified original, depending on `inplace`.
        """

        if not data:
            return []

        key_func = (key if key is not None else (lambda x: x))

        keys = [key_func(x) for x in data]
        min_k, max_k = min(keys), max(keys)

        if min_k == max_k:
            return data.copy() if not inplace else data[:]

        buckets: List[List[T]] = [[] for _ in range(bucket_count)]

        for item in data:
            k = key_func(item)
            index = int(floor((k - min_k) / (max_k - min_k) * (bucket_count - 1)))
            buckets[index].append(item)

        result: List[T] = []
        for b in buckets:
            if b:
                sorted_b = SelectionSort.sort(b, key=key)
                result.extend(sorted_b)

        if inplace:
            data[:] = result
            return data
        else:
            return result

    def __repr__(self):
        return str(self.sort())