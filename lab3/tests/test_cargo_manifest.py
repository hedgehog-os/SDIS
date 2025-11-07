import pytest
from models.operations.cargo_manifest import CargoManifest

def test_valid_initialization():
    manifest = CargoManifest("M001", ["luggage", "mail"], 1000.0)
    assert manifest.manifest_id == "M001"
    assert manifest.items == ["luggage", "mail"]
    assert manifest.total_weight_kg == 1000.0
    assert manifest.weight_log == []

def test_invalid_weight_negative():
    with pytest.raises(ValueError, match="Invalid total weight: -10.0 kg"):
        CargoManifest("M002", ["food"], -10.0)

def test_invalid_weight_exceeds_limit():
    with pytest.raises(ValueError, match="Invalid total weight: 60000.0 kg"):
        CargoManifest("M003", ["tools"], 60000.0)

def test_invalid_item_type():
    with pytest.raises(ValueError, match="Invalid item type: furniture"):
        CargoManifest("M004", ["furniture"], 100.0)

@pytest.fixture
def manifest():
    return CargoManifest("M005", ["equipment", "food"], 2000.0)

def test_add_item_success(manifest):
    manifest.add_item("medical", 500.0)
    assert "medical" in manifest.items
    assert manifest.total_weight_kg == 2500.0
    assert manifest.weight_log == [500.0]

def test_add_item_invalid_type(manifest):
    with pytest.raises(ValueError, match="Invalid item type: gold"):
        manifest.add_item("gold", 100.0)

def test_add_item_negative_weight(manifest):
    with pytest.raises(ValueError, match="Weight must be positive."):
        manifest.add_item("mail", -50.0)

def test_add_item_exceeds_limit(manifest):
    with pytest.raises(ValueError, match="Exceeds maximum cargo weight limit."):
        manifest.add_item("mail", 49000.0)

def test_remove_item_success(manifest):
    assert manifest.remove_item("food") is True
    assert "food" not in manifest.items

def test_remove_item_not_found(manifest):
    assert manifest.remove_item("hazardous") is False

def test_reset(manifest):
    manifest.add_item("documents", 100.0)
    manifest.reset()
    assert manifest.items == []
    assert manifest.total_weight_kg == 0.0
    assert manifest.weight_log == []

def test_get_item_count(manifest):
    assert manifest.get_item_count() == 2

def test_get_weight_log_copy(manifest):
    manifest.add_item("mail", 300.0)
    log = manifest.get_weight_log()
    assert log == [300.0]
    assert log is not manifest.weight_log

def test_is_overloaded_false(manifest):
    assert manifest.is_overloaded() is False


def test_summary(manifest):
    manifest.add_item("electronics", 100.0)
    assert manifest.summary() == f"Manifest M005: 3 items, {manifest.total_weight_kg:.2f} kg"
