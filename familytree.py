import networkx as nx
import json
import atexit
import os

import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

class FamilyTree:

    def __init__(self):
        self.graph = nx.DiGraph()
        self.all_relations = {}
        self._read_pickled_graph()

        def cleanup():
            self._write_pickled_graph()
            self.create_family_tree_image()
        
        atexit.register(cleanup)
    
    def _read_pickled_graph(self):
        try:
            self.graph = nx.read_graphml("cache.graphml")
            with open("cache.json", "r") as filebuf:
                self.all_relations = json.load(filebuf)
        except:
            pass

    def _write_pickled_graph(self):
        temp = self.graph
        nx.write_graphml(temp, "cache.graphml")
        with open("cache.json", "w") as filebuf:
            json.dump(self.all_relations, filebuf)

    def add_relationship(self, relation: str):
        self.all_relations[relation] = 1

    def add_person(self, person: str):
        self.graph.add_node(person)

    def connect_people(self, person1, person2, relation):
        if self.all_relations.get(relation, None):
            self.graph.add_edge(person1, person2, relation=relation)
        else:
            raise Exception("Mentioned relation: {} doesn't exist - you can create one with 'add relationship command'")
    
    def count_relation(self, person, relation, all=False):
        # change this into dynamic programing algo for gain in space complexity
        neighbors = [ v for u,v,e in self.graph.edges(person, True) if e["relation"] == relation]

        count = len(neighbors)

        if count > 0 and all:
            for n in neighbors:
                count += self.count_relation(n, relation, all=all)
        
        return count
    
    def create_family_tree_image(self):
        pos =graphviz_layout(self.graph, prog='dot')
        nx.draw(self.graph , pos, with_labels=True, font_weight='bold')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels={k:v.get("relation") for k,v in dict(self.graph.edges()).items()})
        plt.savefig("cache.png")
    
    def clear(self):
        current_path = os.path.dirname(os.path.abspath(__name__))

        paths_of_interest = [os.path.join(current_path,x) for x in ["cache.graphml", "cache.png", "cache.json"]]

        for clear_path in paths_of_interest:
            print(clear_path)
            if os.path.exists(clear_path):
                os.remove(clear_path)