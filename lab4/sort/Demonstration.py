from __future__ import annotations
from SelectionSort import SelectionSort
from BucketSort import BucketSort
from Person import Person

class Demonstration:
    
    def integers():
        values = [5, 873, 1, 90, 43, 15, 111]
        selectionsort = SelectionSort.sort(data=values)
        bucketsort = BucketSort.sort(data=values, bucket_count=4)
        print('Исходный список: ', values)
        print('SelectionSort: ', selectionsort)
        print('BucketSort: ', bucketsort)
        print()

    def floats():
        values = [2.3, 10.8, 0.1, 4.9, 36.7, 0.2]
        selectionsort = SelectionSort.sort(data=values)
        bucketsort = BucketSort.sort(data=values, bucket_count=4)
        print('Исходный список: ', values)
        print('SelectionSort: ', selectionsort)
        print('BucketSort: ', bucketsort)
        print()

    def persons():
        persons = [
            Person('Bob', 15, 167),
            Person('Alice', 27, 177),
            Person('Jhon', 21, 181),
            Person('Kate', 25, 170)
        ]
        selectionsort = SelectionSort.sort(data=persons, key=lambda p: p.age)
        bucketsort = BucketSort.sort(data=persons, key=lambda p: p.age, bucket_count=4)
        print('Sort by age: ', persons)
        print('SelectionSort: ', selectionsort)
        print('BucketSort: ', bucketsort)
        print()

        selectionsort = SelectionSort.sort(data=persons, key=lambda p: p.height)
        bucketsort = BucketSort.sort(data=persons, key=lambda p: p.height, bucket_count=4)
        print('Sort by height: ', persons)
        print('SelectionSort: ', selectionsort)
        print('BucketSort: ', bucketsort)
        print()

        selectionsort = SelectionSort.sort(data=persons, key=lambda p: p.name)
        print('Sort by name: ', persons)
        print('SelectionSort: ', selectionsort)
        print()

    def run():
        Demonstration.integers()
        Demonstration.floats()
        Demonstration.persons()