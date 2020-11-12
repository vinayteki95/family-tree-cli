import gc
import typer
from familytree import FamilyTree
from familytree import RelationType

# Command line Interface requirements
app = typer.Typer()
add_app = typer.Typer()
app.add_typer(add_app, name = "add")

# Instantiating familytree
ft = FamilyTree()

@add_app.command("person")
def add_person(person: str):
    ft.add_person(person)

@add_app.command("relationship")
def add_relationship(relation: str, relation_type: RelationType):
    ft.add_relationship(relation, relation_type)

@app.command("connect")
def connect_people(person: str , relation: str = typer.Option(...), of: str = typer.Option(...)):
    ft.connect_people(of, person, relation)

@app.command("count")
def count_relation(person: str, relation: str = typer.Option(...), all: bool = typer.Option(False)):
    print("No of {}s of {}: {}".format(relation, person, ft.count_relation(person, relation, all=all)))

@app.command("clear")
def clear():
    ft.clear()


if __name__ == "__main__":
    app()