from backend_api.models.species import ImpactRelationship, InvasiveSpecies, Species
from backend_api import create_app
import networkx as nx
import pandas as pd
import json
import pprint

pp = pprint.PrettyPrinter(indent=1)


class NodeSchema:
    def __init__(self):
        self.id = None
        self.name = None
        self.color = "f00000"
        self.order = 0
        self.size = 0
        self.neighbors_out = []
        self.neighbors_in = []
        self.neighbor_type = dict()
        self.links = []


class LinkSchema:
    def __init__(self):
        self.source = ""
        self.target = ""


class NetworkStore:
    def __init__(self):
        self.seen_nodes = dict()
        self.nodes = []
        self.links = []

impact_rel_table = ImpactRelationship()
species_table = Species()

class Network:
    """
    This class is designed to re-read species edges from the database and create another set of
    data that is able to be used for the 3D network visualization.
    """

    def __init__(self):

        self.impact_rel_df = impact_rel_table.get_all_records()
        self.species_df = species_table.get_all_records()

        # name the species
        self.named_species_df = self.__name_species_edges()

        # graph object
        self.G = self.__create_graph()

        # where the network details are stored
        self.networkStore = NetworkStore()

        self.networkStore_2 = NetworkStore()

        # get a node details
        self.node_details = dict()

    def __name_species_edges(self):
        rename_dict = dict(zip(self.species_df.id.values, self.species_df.name.values))
        df = self.impact_rel_df.replace(rename_dict)
        return df

    def __create_graph(self):
        edges = zip(self.named_species_df.impacter_id.values, self.named_species_df.impacted_id.values)
        G = nx.DiGraph()
        G.add_edges_from(edges)
        return G

    def __create_child_NodeSchema(self):
        pass

    def fill_nodes_store(self, name=None):
        for node in list(self.G.nodes):
            n = NodeSchema()
            n.name = node
            n.id = int(self.species_df[self.species_df.name == node].id.values[0])
            self.networkStore.seen_nodes[node] = ""

            # building links for current node adding neighbors as well
            in_edges = self.G.in_edges(node)
            out_edges = self.G.out_edges(node)
            for n1, n2 in list(in_edges):
                n.neighbor_type[n1] = 'in'
                n.neighbors_in.append(n1)
                l = LinkSchema()
                l.source = n1
                l.target = n2
                n.links.append(l.__dict__)
            for n1, n2 in list(out_edges):
                n.neighbor_type[n2] = 'out'
                n.neighbors_out.append(n2)
                l = LinkSchema()
                l.source = n1
                l.target = n2
                n.links.append(l.__dict__)

            self.node_details[n.name] = n.__dict__
            self.networkStore.nodes.append(n.__dict__)

    def map_nodes_in_network_store(self):
        for node in self.networkStore.nodes:
            neighbors_out = []
            for node_out in node['neighbors_out']:
                try:
                    new_node = self.node_details[node_out].copy()
                    new_node['order'] += 1
                    neighbors_out.append(new_node)
                except KeyError:
                    print(f'no key found for {node_out}')
                    pass
            node['neighbors_out'] = neighbors_out

            # node['neighbors_out'] = neighbors_out  #this shit might not work
            # self.networkStore_2.nodes.append(node)

    def write_node_store_to_file(self):
        with open('output/test.json', 'w') as f:
            json.dump(self.networkStore.__dict__, f)

        # pp.pprint(self.networkStore.__dict__)

        # building child nodes for current node (direction?)
        # for node_neighbor in list(self.G.neighbors(node)):
        #     n_child = NodeSchema()
        #     n_child.id = self.species_df[self.species_df.name == node_neighbor].id.values[0]
        #     n_child.name = node_neighbor

        # self.networkStore

    def __create_color(self):
        pass

    def color_nodes(self):
        pass


if __name__ == "__main__":
    network = Network()
    network.fill_nodes_store()

    # network.map_nodes_in_network_store()
    # network.write_node_store_to_file()
    # print(network.networkStore.nodes)
    # print(network.networkStore_2.nodes)
    # network.write_node_store_to_file()
