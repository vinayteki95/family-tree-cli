import pytest
from familytree import FamilyTree
from familytree import RelationType

@pytest.fixture
def ft_clean():
    ft = FamilyTree()
    ft.clear()
    yield ft

@pytest.fixture
def ft_base_family():
    ft = FamilyTree()
    ft.clear()
    # people
    ft.add_person("john shakespeare")
    ft.add_person("mary arden")
    ft.add_person("joan")
    ft.add_person("margaret")
    ft.add_person("gilbert")
    ft.add_person("joan2")
    ft.add_person("anne")
    ft.add_person("richard")
    ft.add_person("edmund")
    ft.add_person("william")
    ft.add_person("anne hathaway")
    ft.add_person("susanna")
    ft.add_person("john hall")
    ft.add_person("hamnet")
    ft.add_person("judith")
    ft.add_person("thomas quiney")
    ft.add_person("elizabeth")
    ft.add_person("shakespeare")
    ft.add_person("richard2")
    ft.add_person("thomas")

    # relations
    ft.add_relationship("father", RelationType.prevgen)
    ft.add_relationship("mother", RelationType.prevgen)
    ft.add_relationship("wife", RelationType.partner)
    ft.add_relationship("son", RelationType.nextgen)
    ft.add_relationship("daughter", RelationType.nextgen)
    ft.add_relationship("brother", RelationType.samegen)

    # sparse shuffled relations
    ft.connect_people("john shakespeare", "mary arden", "wife")
    ft.connect_people("john shakespeare", "joan", "daughter")
    ft.connect_people("john shakespeare", "margaret", "daughter")
    ft.connect_people("john shakespeare", "joan2", "daughter")
    ft.connect_people("mary arden", "anne", "daughter")
    ft.connect_people("mary arden", "gilbert", "son")
    ft.connect_people("mary arden", "richard", "son")
    ft.connect_people("mary arden", "edmund", "son")
    ft.connect_people("mary arden", "william", "son")
    ft.connect_people("william", "anne hathaway", "wife")
    ft.connect_people("william", "hamnet", "son")
    ft.connect_people("william", "susanna", "daughter")
    ft.connect_people("william", "judith", "daughter")
    ft.connect_people("john hall", "susanna", "wife")
    ft.connect_people("thomas quiney", "judith", "wife")
    ft.connect_people("susanna", "elizabeth", "daughter")
    ft.connect_people("judith", "shakespeare", "son")
    ft.connect_people("judith", "richard2", "son")
    ft.connect_people("judith", "thomas", "son")

    yield ft

def test_add_relationship(ft_clean):
    ft_clean.add_relationship("mother", "prevgen")
    assert ft_clean.all_relations == {
        "mother": "prevgen"
    }

def test_add_person(ft_clean):
    ft_clean.add_person("person1")
    assert list(ft_clean.graph.nodes()) == ["person1"]

def test_connect_people(ft_clean):
    person_1 = "john shakespeare"
    person_2 = "mary arden"
    relation = "wife"
    relation_type = RelationType.partner

    ft_clean.add_person(person_1)
    ft_clean.add_person(person_2)
    ft_clean.add_relationship(relation, relation_type)

    ft_clean.connect_people(person_1, person_2, relation)

    assert list(ft_clean.graph.edges(person_1, True)) == [(person_1, person_2, {"relation": relation})]

def test_count_relation(ft_base_family):

    assert ft_base_family.count_relation("william", "son") == 1
    assert ft_base_family.count_relation("john shakespeare", "son") == 4
    assert ft_base_family.count_relation("mary arden", "daughter", all=True) == 7
    assert ft_base_family.count_relation("anne hathaway", "daughter", all=True) == 3