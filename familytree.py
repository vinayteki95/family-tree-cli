import networkx as nx
import json
import atexit
import os
from enum import Enum

import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

class RelationType(str, Enum):
    prevgen = "prevgen"
    nextgen = "nextgen"
    samegem = "samegen"
    partner = "partner"

class FamilyTree:

    def __init__(self):
        self.graph = nx.DiGraph()
        self.all_relations = {}
        self._count_relation_cyclic_break = {}
        self._read_cached_graph()

        def cleanup():
            self._write_cached_graph()
            self.create_family_tree_image()
        
        atexit.register(cleanup)
    
    def _read_cached_graph(self):
        try:
            self.graph = nx.read_graphml("cache.graphml")
            with open("cache.json", "r") as filebuf:
                self.all_relations = json.load(filebuf)
        except:
            pass

    def _write_cached_graph(self):
        temp = self.graph
        nx.write_graphml(temp, "cache.graphml")
        with open("cache.json", "w") as filebuf:
            json.dump(self.all_relations, filebuf)

    def add_relationship(self, relation: str, relation_type: RelationType):
        self.all_relations[relation] = relation_type

    def add_person(self, person: str):
        self.graph.add_node(person)

    def connect_people(self, person1, person2, relation):
        if self.all_relations.get(relation, None):
            self.graph.add_edge(person1, person2, relation=relation)
        else:
            raise Exception("Mentioned relation: {} doesn't exist - you can create one with 'add relationship command'")

    def count_relation(self, person, relation, all =False):
        relation_type = self.all_relations[relation]
        neighbors = list([(v,e["relation"]) for u,v,e in self.graph.edges(person, True) if self.all_relations[e["relation"]]==relation_type])
        neighbors += list([(u,e["relation"]) for u,v,e in self.graph.in_edges(person, True) if self.all_relations[e["relation"]]==RelationType.prevgen])

        # If we are counting next generation people, we might as well add partner (wife/husband's children)
        if relation_type == RelationType.nextgen:
            partners = [(v,e["relation"]) for u,v,e in self.graph.edges(person, True) if self.all_relations[e["relation"]]==RelationType.partner]
            partners += [(u,e["relation"]) for u,v,e in self.graph.in_edges(person, True) if self.all_relations[e["relation"]]==RelationType.partner]
            for p in partners:
                p = p[0]
                neighbors += [(v,e["relation"]) for u,v,e in self.graph.edges(p, True) if self.all_relations[e["relation"]]==relation_type]
                neighbors += [(u,e["relation"]) for u,v,e in self.graph.in_edges(p, True) if self.all_relations[e["relation"]]==relation_type]
                neighbors = list(set(neighbors)) # eliminate duplicates
        else:
            partners = []
        
        count = len([x for x in neighbors if x[1] == relation])
        # print(count)

        print(neighbors)

        if len(neighbors) > 0 and all:
            for n in neighbors:
                if self._count_relation_cyclic_break.get(n,None) is None:
                    self._count_relation_cyclic_break[n] = 1
                    count += self.count_relation(n[0], relation, all=all)
        return count


    
    def create_family_tree_image(self):
        pos =graphviz_layout(self.graph, prog='dot')
        nx.draw(self.graph , pos, with_labels=True, font_weight='bold')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels={k:v.get("relation") for k,v in dict(self.graph.edges()).items()})
        plt.savefig("cache.png")
    
    def clear(self):
        self.graph = nx.DiGraph()
        self.all_relations = {}
        current_path = os.path.dirname(os.path.abspath(__name__))

        paths_of_interest = [os.path.join(current_path,x) for x in ["cache.graphml", "cache.png", "cache.json"]]

        for clear_path in paths_of_interest:
            if os.path.exists(clear_path):
                print(clear_path)
                os.remove(clear_path)