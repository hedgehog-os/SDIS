import pytest
from models.infrastructure.retail_shop import RetailShop

class DummyTerminal:
    def __init__(self, name):
        self.name = name

@pytest.fixture
def terminal():
    return DummyTerminal("T1")

def test_valid_initialization(terminal):
    shop = RetailShop("TechZone", "electronics", terminal)
    assert shop.name == "TechZone"
    assert shop.category == "electronics"
    assert shop.terminal == terminal
    assert shop.is_open is True
    assert shop.maintenance_required is False
    assert shop.customer_log == []
    assert shop.inventory == []

def test_invalid_category(terminal):
    with pytest.raises(ValueError, match="Invalid category: furniture"):
        RetailShop("HomeStuff", "furniture", terminal)

@pytest.fixture
def shop(terminal):
    return RetailShop("BookNest", "books", terminal)

def test_open_and_close(shop):
    shop.close()
    assert shop.is_open is False
    shop.open()
    assert shop.is_open is True

def test_mark_and_clear_maintenance(shop):
    shop.mark_for_maintenance()
    assert shop.maintenance_required is True
    shop.clear_maintenance()
    assert shop.maintenance_required is False

def test_is_operational(shop):
    assert shop.is_operational() is True
    shop.mark_for_maintenance()
    assert shop.is_operational() is False
    shop.clear_maintenance()
    shop.close()
    assert shop.is_operational() is False

def test_log_customer_and_count(shop):
    shop.log_customer("Alice")
    shop.log_customer("Bob")
    assert shop.customer_log == ["Alice", "Bob"]
    assert shop.get_customer_count() == 2

def test_add_item(shop):
    shop.add_item("Notebook")
    shop.add_item("Pen")
    assert shop.inventory == ["Notebook", "Pen"]

def test_remove_item_success(shop):
    shop.add_item("Map")
    assert shop.remove_item("Map") is True
    assert "Map" not in shop.inventory

def test_remove_item_failure(shop):
    assert shop.remove_item("Nonexistent") is False

def test_has_item(shop):
    shop.add_item("Guidebook")
    assert shop.has_item("Guidebook") is True
    assert shop.has_item("Camera") is False

def test_get_inventory_returns_copy(shop):
    shop.add_item("Postcard")
    inv = shop.get_inventory()
    assert inv == ["Postcard"]
    assert inv is not shop.inventory

def test_reset(shop):
    shop.log_customer("X")
    shop.add_item("Y")
    shop.mark_for_maintenance()
    shop.close()
    shop.reset()
    assert shop.is_open is True
    assert shop.maintenance_required is False
    assert shop.customer_log == []
    assert shop.inventory == []

def test_summary(shop):
    shop.terminal_name = shop.terminal.name  # simulate terminal_name property
    assert shop.summary() == "BookNest (books) in Terminal T1"
