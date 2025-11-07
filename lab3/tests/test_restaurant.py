import pytest
from models.infrastructure.restaurant import Restaurant

class DummyTerminal:
    def __init__(self, name):
        self.name = name

def test_valid_initialization():
    terminal = DummyTerminal("T1")
    r = Restaurant("Pasta Place", "italian", terminal)
    assert r.name == "Pasta Place"
    assert r.cuisine_type == "italian"
    assert r.terminal == terminal
    assert r.is_open is True
    assert r.maintenance_required is False
    assert r.customer_log == []
    assert r.menu_items == []

def test_invalid_cuisine_type():
    terminal = DummyTerminal("T1")
    with pytest.raises(ValueError, match="Invalid cuisine type: nordic"):
        Restaurant("Viking Dine", "nordic", terminal)

@pytest.fixture
def restaurant():
    return Restaurant("Sushi Spot", "japanese", DummyTerminal("T2"))

def test_close_and_open(restaurant):
    restaurant.close()
    assert restaurant.is_open is False
    restaurant.open()
    assert restaurant.is_open is True

def test_mark_and_clear_maintenance(restaurant):
    restaurant.mark_for_maintenance()
    assert restaurant.maintenance_required is True
    restaurant.clear_maintenance()
    assert restaurant.maintenance_required is False

def test_is_operational(restaurant):
    assert restaurant.is_operational() is True
    restaurant.mark_for_maintenance()
    assert restaurant.is_operational() is False
    restaurant.clear_maintenance()
    restaurant.close()
    assert restaurant.is_operational() is False

def test_log_customer_and_count(restaurant):
    restaurant.log_customer("Alice")
    restaurant.log_customer("Bob")
    assert restaurant.customer_log == ["Alice", "Bob"]
    assert restaurant.get_customer_count() == 2

def test_add_menu_item(restaurant):
    restaurant.add_menu_item("Sushi Roll")
    restaurant.add_menu_item("Miso Soup")
    assert restaurant.menu_items == ["Sushi Roll", "Miso Soup"]

def test_remove_menu_item_success(restaurant):
    restaurant.add_menu_item("Tempura")
    assert restaurant.remove_menu_item("Tempura") is True
    assert "Tempura" not in restaurant.menu_items

def test_remove_menu_item_failure(restaurant):
    assert restaurant.remove_menu_item("Nonexistent") is False

def test_has_menu_item(restaurant):
    restaurant.add_menu_item("Ramen")
    assert restaurant.has_menu_item("Ramen") is True
    assert restaurant.has_menu_item("Burger") is False

def test_get_menu_copy(restaurant):
    restaurant.add_menu_item("Sashimi")
    menu = restaurant.get_menu()
    assert menu == ["Sashimi"]
    assert menu is not restaurant.menu_items

def test_reset(restaurant):
    restaurant.log_customer("X")
    restaurant.add_menu_item("Y")
    restaurant.mark_for_maintenance()
    restaurant.close()
    restaurant.reset()
    assert restaurant.is_open is True
    assert restaurant.maintenance_required is False
    assert restaurant.customer_log == []
    assert restaurant.menu_items == []
