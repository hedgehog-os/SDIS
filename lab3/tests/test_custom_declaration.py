import pytest
from models.operations.customs_declaration import CustomsDeclaration

class DummyPassenger:
    def __init__(self, full_name):
        self.full_name = full_name

def test_valid_initialization():
    p = DummyPassenger("Alice")
    decl = CustomsDeclaration(p, ["documents"], 500.0)
    assert decl.passenger == p
    assert decl.declared_items == ["documents"]
    assert decl.total_value_usd == 500.0
    assert decl.flagged_items == []
    assert decl.reviewed is False

def test_negative_total_value():
    p = DummyPassenger("Bob")
    with pytest.raises(ValueError, match="Total value cannot be negative."):
        CustomsDeclaration(p, [], -10.0)

@pytest.fixture
def declaration():
    return CustomsDeclaration(DummyPassenger("Charlie"), [], 0.0)

def test_is_required_by_value(declaration):
    declaration.total_value_usd = 1500.0
    assert declaration.is_required() is True

def test_is_required_by_items(declaration):
    declaration.declared_items.append("books")
    assert declaration.is_required() is True

def test_is_required_false(declaration):
    assert declaration.is_required() is False

def test_add_item_valid(declaration):
    declaration.add_item("food", 200.0)
    assert "food" in declaration.declared_items
    assert declaration.total_value_usd == 200.0
    assert declaration.flagged_items == []

def test_add_item_prohibited(declaration):
    declaration.add_item("narcotics", 100.0)
    assert "narcotics" in declaration.flagged_items

def test_add_item_invalid_value(declaration):
    with pytest.raises(ValueError, match="Item value must be positive."):
        declaration.add_item("mail", 0.0)

def test_remove_item_success(declaration):
    declaration.add_item("tools", 300.0)
    assert declaration.remove_item("tools", 300.0) is True
    assert "tools" not in declaration.declared_items
    assert declaration.total_value_usd == 0.0

def test_remove_item_prohibited(declaration):
    declaration.add_item("explosives", 500.0)
    assert "explosives" in declaration.flagged_items
    declaration.remove_item("explosives", 500.0)
    assert "explosives" not in declaration.flagged_items

def test_remove_item_not_found(declaration):
    assert declaration.remove_item("unknown", 100.0) is False

def test_has_prohibited_items(declaration):
    declaration.add_item("radioactive", 100.0)
    assert declaration.has_prohibited_items() is True

def test_has_prohibited_items_false(declaration):
    declaration.add_item("books", 100.0)
    assert declaration.has_prohibited_items() is False

def test_mark_reviewed(declaration):
    declaration.mark_reviewed()
    assert declaration.reviewed is True

def test_reset(declaration):
    declaration.add_item("mail", 100.0)
    declaration.add_item("firearms", 200.0)
    declaration.mark_reviewed()
    declaration.reset()
    assert declaration.declared_items == []
    assert declaration.total_value_usd == 0.0
    assert declaration.flagged_items == []
    assert declaration.reviewed is False

def test_summary_pending(declaration):
    declaration.add_item("books", 100.0)
    assert declaration.summary() == "Customs for Charlie: 1 items, $100.00, PENDING"

def test_summary_reviewed(declaration):
    declaration.add_item("books", 100.0)
    declaration.mark_reviewed()
    assert declaration.summary() == "Customs for Charlie: 1 items, $100.00, REVIEWED"
