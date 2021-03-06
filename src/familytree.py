import json
import atexit
import os
from enum import Enum
from src import config_management

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

class RelationType(str, Enum):
    """
        RelationType Enum
        prevgen -> one step above in family tree hierarchy (mother, father)
        nextgen -> one step below in family tree hierarchy (son, daughter)
        samegen -> same level in family tree hierarchy (brother, sister)
        partner -> same level in family tree but common children (wife / step wife / husband / step husband)
    """
    prevgen = "prevgen"
    nextgen = "nextgen"
    samegen = "samegen"
    partner = "partner"


class FamilyTree:

    def __init__(self):
        
        self.config = config_management.read_config() # Maintains persistent configuration files 
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
            self.graph = nx.read_graphml(self.config['DEFAULT']['familytree_graph_path'])
            with open(self.config['DEFAULT']['relationships_list_path'], "r") as filebuf:
                self.all_relations = json.load(filebuf)
        except:
            pass


    def _write_cached_graph(self):
        temp = self.graph
        nx.write_graphml(temp, self.config['DEFAULT']['familytree_graph_path'])
        with open(self.config['DEFAULT']['relationships_list_path'], "w") as filebuf:
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
        # this section of code can be moved to a different function when adding more rules for different types of relations
        if relation_type == RelationType.nextgen:
            partners = [(v,e["relation"]) for u,v,e in self.graph.edges(person, True) if self.all_relations[e["relation"]]==RelationType.partner]
            partners += [(u,e["relation"]) for u,v,e in self.graph.in_edges(person, True) if self.all_relations[e["relation"]]==RelationType.partner]
            for p in partners:
                p = p[0]
                neighbors += [(v,e["relation"]) for u,v,e in self.graph.edges(p, True) if self.all_relations[e["relation"]]==relation_type]
                neighbors += [(u,e["relation"]) for u,v,e in self.graph.in_edges(p, True) if self.all_relations[e["relation"]]==RelationType.prevgen]
                neighbors = list(set(neighbors)) # eliminate duplicates
        else:
            partners = []
        
        count = len([x for x in neighbors if x[1] == relation])
        # print(count)

        # print(neighbors)

        if len(neighbors) > 0 and all:
            for n in neighbors:
                if self._count_relation_cyclic_break.get(n,None) is None:
                    self._count_relation_cyclic_break[n] = 1
                    count += self.count_relation(n[0], relation, all=all)
        self._count_relation_cyclic_break = {}  # breaks cycles at only depth one - need to figure out a better way to do this
        return count


    def create_family_tree_image(self):
        pos =graphviz_layout(self.graph, prog='dot')
        nx.draw(self.graph , pos, with_labels=True, font_weight='bold')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels={k:v.get("relation") for k,v in dict(self.graph.edges()).items()})
        try:
            plt.savefig(self.config['DEFAULT']['familytree_image_path'])
        except:
            pass


    def clear(self):
        self.graph = nx.DiGraph()
        self.all_relations = {}
        current_path = os.path.dirname(os.path.abspath(__name__))

        list_of_paths = list(self.config['DEFAULT'].values())
        paths_of_interest = [os.path.join(current_path,x) for x in list_of_paths]

        for clear_path in paths_of_interest:
            if os.path.exists(clear_path):
                print(clear_path)
                os.remove(clear_path)