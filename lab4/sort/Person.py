class Person:
    def __init__(self, name: str, age: int, height: int):
        self.name = name
        self.height = height
        self.age = age

    def __repr__(self):
        return f"Person({self.name!r}, {self.age}, {self.height})"

    def __lt__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age