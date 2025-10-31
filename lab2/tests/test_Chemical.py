from datetime import datetime

class DummyReaction:
    def __init__(self, reaction_id, recorded_at=None, conditions=None):
        self.reaction_id = reaction_id
        self.reactants = []
        self.products = []
        self.recorded_at = recorded_at or datetime.now()
        self.conditions = conditions
import pytest
from experiments_and_equipments.Chemical import Chemical

@pytest.fixture
def chemical():
    return Chemical(
        chemical_id=1,
        name="Вода",
        formula="H2O",
        concentration_molar=0.5
    )
def test_initial_state(chemical):
    assert chemical.name == "Вода"
    assert chemical.formula == "H2O"
    assert chemical.concentration_molar == 0.5
    assert chemical.reactions == []

def test_add_reaction_as_reactant(chemical):
    r = DummyReaction(101)
    chemical.add_reaction(r)
    assert r in chemical.reactions
    assert chemical in r.reactants
    assert chemical not in r.products

def test_add_reaction_no_duplicate(chemical):
    r = DummyReaction(102)
    chemical.add_reaction(r)
    chemical.add_reaction(r)
    assert chemical.reactions.count(r) == 1

def test_remove_reaction(chemical):
    r = DummyReaction(103)
    chemical.add_reaction(r)
    chemical.remove_reaction(r)
    assert r not in chemical.reactions
    assert chemical not in r.reactants
    assert chemical not in r.products

def test_is_reactant_in(chemical):
    r = DummyReaction(104)
    r.reactants.append(chemical)
    assert chemical.is_reactant_in(r) is True

def test_is_product_in(chemical):
    r = DummyReaction(105)
    r.products.append(chemical)
    assert chemical.is_product_in(r) is True

def test_get_reaction_ids(chemical):
    r1 = DummyReaction(201)
    r2 = DummyReaction(202)
    chemical.add_reaction(r1)
    chemical.add_reaction(r2)
    ids = chemical.get_reaction_ids()
    assert ids == [201, 202]

def test_get_reactions_as_reactant(chemical):
    r1 = DummyReaction(301)
    r2 = DummyReaction(302)
    r1.reactants.append(chemical)
    r2.products.append(chemical)
    chemical.reactions = [r1, r2]
    result = chemical.get_reactions_as("reactant")
    assert result == [r1]

def test_get_reactions_as_product(chemical):
    r1 = DummyReaction(303)
    r2 = DummyReaction(304)
    r1.products.append(chemical)
    r2.reactants.append(chemical)
    chemical.reactions = [r1, r2]
    result = chemical.get_reactions_as("product")
    assert result == [r1]

def test_get_reactions_as_invalid_role(chemical):
    with pytest.raises(ValueError):
        chemical.get_reactions_as("catalyst")

def test_summarize(chemical):
    r = DummyReaction(401)
    chemical.add_reaction(r)
    summary = chemical.summarize()
    assert "Chemical #1: Вода (H2O)" in summary
    assert "Связанные реакции: 401" in summary

def test_to_dict(chemical):
    r = DummyReaction(501)
    chemical.add_reaction(r)
    data = chemical.to_dict()
    assert data["chemical_id"] == 1
    assert data["reaction_ids"] == [501]

def test_get_recent_reactions(chemical):
    from datetime import timedelta
    recent = DummyReaction(601, recorded_at=datetime.now())
    old = DummyReaction(602, recorded_at=datetime.now() - timedelta(days=60))
    chemical.reactions = [recent, old]
    result = chemical.get_recent_reactions(days=30)
    assert recent in result
    assert old not in result

def test_get_reactions_by_condition(chemical):
    r1 = DummyReaction(701, conditions="Температура: 100C")
    r2 = DummyReaction(702, conditions="pH: 7")
    chemical.reactions = [r1, r2]
    result = chemical.get_reactions_by_condition("температура")
    assert result == [r1]

def test_visualize_reaction_roles(chemical):
    r1 = DummyReaction(801)
    r2 = DummyReaction(802)
    r1.reactants.append(chemical)
    r2.products.append(chemical)
    chemical.reactions = [r1, r2]
    diagram = chemical.visualize_reaction_roles()
    assert "Реагент: | (1)" in diagram
    assert "Продукт: | (1)" in diagram

def test_get_co_reactants(chemical):
    c2 = Chemical(2, "Кислород", "O2")
    r = DummyReaction(901)
    r.reactants = [chemical, c2]
    chemical.reactions = [r]
    result = chemical.get_co_reactants()
    assert result == [c2]
