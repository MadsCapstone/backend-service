from backend_api.models.species import ImpactRelationship
from backend_api import create_app
import networkx as nx



class Network:
    """
    This class is designed to re-read species edges from the database and create another set of
    data that is able to be used for the 3D network visualization.
    """
    def __init__(self):
        self.database = ImpactRelationship()
        self.graph = None
        # neighbors equal adjacent nodes
        self.neighbors_by_node = None
        # links are edge definitions for a node
        self.links_by_node = None

    def create_graph(self):
        edges = [(entry.impacter_id, entry.impacted_id) for entry in self.database.get_all_records()]
        print(edges)
        pass



if __name__ == "__main__":
    app = create_app('localprod')
    network = Network()
    network.create_graph()