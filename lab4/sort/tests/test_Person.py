from sort.Person import Person

def test_person_initialization():
    p = Person("Alice", 30, 170)
    assert p.name == "Alice"
    assert p.age == 30
    assert p.height == 170

def test_person_repr():
    p = Person("Bob", 25, 180)
    assert repr(p) == "Person('Bob', 25, 180)"

def test_person_lt_true():
    p1 = Person("Alice", 30, 170)
    p2 = Person("Bob", 25, 180)
    assert p2 < p1  # 25 < 30

def test_person_lt_false():
    p1 = Person("Alice", 30, 170)
    p2 = Person("Bob", 35, 180)
    assert not p2 < p1

