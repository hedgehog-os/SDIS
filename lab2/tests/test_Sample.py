class DummyChemical:
    def __init__(self, chemical_id: int, name: str, formula: str, concentration_molar: float = None):
        self.chemical_id = chemical_id
        self.name = name
        self.formula = formula
        self.concentration_molar = concentration_molar
import pytest
from experiments_and_equipments.Sample import Sample

@pytest.fixture
def chemical():
    return DummyChemical(chemical_id=1, name="NaCl", formula="NaCl", concentration_molar=0.5)

@pytest.fixture
def sample(chemical):
    return Sample(sample_id=101, chemical=chemical, volume_ml=250.0)
def test_initial_state(sample, chemical):
    assert sample.sample_id == 101
    assert sample.chemical == chemical
    assert sample.volume_ml == 250.0

def test_get_concentration(sample):
    assert sample.get_concentration() == 0.5

def test_get_moles(sample):
    expected_moles = 0.5 * (250.0 / 1000)  # 0.125
    assert sample.get_moles() == expected_moles

def test_get_moles_none():
    chem = DummyChemical(2, "H2O", "H2O", concentration_molar=None)
    s = Sample(sample_id=102, chemical=chem, volume_ml=100.0)
    assert s.get_moles() is None

def test_describe_with_concentration(sample):
    description = sample.describe()
    assert "Образец #101" in description
    assert "Вещество: NaCl (NaCl)" in description
    assert "Объём: 250.00 мл" in description
    assert "Концентрация: 0.5 M" in description
    assert "Количество вещества: 0.1250 моль" in description

def test_describe_without_concentration():
    chem = DummyChemical(3, "H2O", "H2O", concentration_molar=None)
    s = Sample(sample_id=103, chemical=chem, volume_ml=100.0)
    description = s.describe()
    assert "Концентрация: — M" in description
    assert "Количество вещества: —" in description

def test_to_dict(sample):
    data = sample.to_dict()
    assert data["sample_id"] == 101
    assert data["chemical_id"] == 1
    assert data["chemical_name"] == "NaCl"
    assert data["formula"] == "NaCl"
    assert data["volume_ml"] == 250.0
    assert data["concentration_molar"] == 0.5
    assert data["moles"] == 0.125

def test_is_same_chemical_true(sample):
    other = Sample(sample_id=104, chemical=sample.chemical, volume_ml=50.0)
    assert sample.is_same_chemical(other) is True

def test_is_same_chemical_false(sample):
    other_chem = DummyChemical(2, "KCl", "KCl", concentration_molar=0.5)
    other = Sample(sample_id=105, chemical=other_chem, volume_ml=50.0)
    assert sample.is_same_chemical(other) is False
