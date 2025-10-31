class DummyChemical:
    def __init__(self, chemical_id: int, name: str, formula: str):
        self.chemical_id = chemical_id
        self.name = name
        self.formula = formula
        self.reactions = []

    def add_reaction(self, reaction):
        if reaction not in self.reactions:
            self.reactions.append(reaction)
import pytest
from datetime import datetime, timedelta
from experiments_and_equipments.Reaction import Reaction

@pytest.fixture
def reaction():
    return Reaction(
        reaction_id=1,
        description="Гидратация",
        conditions="Температура 25°C",
        recorded_at=datetime.now()
    )
def test_initial_state(reaction):
    assert reaction.reaction_id == 1
    assert reaction.description == "Гидратация"
    assert reaction.conditions == "Температура 25°C"
    assert reaction.reactants == []
    assert reaction.products == []

def test_add_reactant(reaction):
    chem = DummyChemical(101, "Вода", "H2O")
    reaction.add_reactant(chem)
    assert chem in reaction.reactants
    assert reaction in chem.reactions

def test_add_product(reaction):
    chem = DummyChemical(102, "Этанол", "C2H5OH")
    reaction.add_product(chem)
    assert chem in reaction.products
    assert reaction in chem.reactions

def test_remove_chemical(reaction):
    chem = DummyChemical(103, "Кислота", "HCl")
    reaction.add_reactant(chem)
    reaction.add_product(chem)
    reaction.remove_chemical(chem)
    assert chem not in reaction.reactants
    assert chem not in reaction.products
    assert reaction not in chem.reactions

def test_involves_chemical_true(reaction):
    chem = DummyChemical(104, "Бензол", "C6H6")
    reaction.add_reactant(chem)
    assert reaction.involves_chemical(chem) is True

def test_involves_chemical_false(reaction):
    chem = DummyChemical(105, "Метан", "CH4")
    assert reaction.involves_chemical(chem) is False

def test_get_all_chemicals(reaction):
    c1 = DummyChemical(106, "NaOH", "NaOH")
    c2 = DummyChemical(107, "CO2", "CO2")
    reaction.add_reactant(c1)
    reaction.add_product(c2)
    all_chems = reaction.get_all_chemicals()
    assert set(all_chems) == {c1, c2}

def test_summarize_output(reaction):
    c1 = DummyChemical(108, "NH3", "NH3")
    c2 = DummyChemical(109, "H2O", "H2O")
    reaction.add_reactant(c1)
    reaction.add_product(c2)
    summary = reaction.summarize()
    assert "🧪 Reaction #1" in summary
    assert "Реагенты: NH3" in summary
    assert "Продукты: H2O" in summary
    assert "Условия: Температура 25°C" in summary

def test_to_dict(reaction):
    c1 = DummyChemical(110, "H2", "H2")
    c2 = DummyChemical(111, "O2", "O2")
    reaction.add_reactant(c1)
    reaction.add_product(c2)
    data = reaction.to_dict()
    assert data["reaction_id"] == 1
    assert data["description"] == "Гидратация"
    assert data["reactants"] == [110]
    assert data["products"] == [111]
    assert data["conditions"] == "Температура 25°C"
    assert isinstance(data["recorded_at"], str)

def test_is_recent_true(reaction):
    assert reaction.is_recent(days=30) is True

def test_is_recent_false():
    old_date = datetime.now() - timedelta(days=90)
    r = Reaction(2, "Старая реакция", recorded_at=old_date)
    assert r.is_recent(days=30) is False

def test_contains_formula_true(reaction):
    chem = DummyChemical(112, "Ацетон", "C3H6O")
    reaction.add_reactant(chem)
    assert reaction.contains_formula("C3H6O") is True

def test_contains_formula_false(reaction):
    chem = DummyChemical(113, "Этан", "C2H6")
    reaction.add_product(chem)
    assert reaction.contains_formula("CH4") is False
