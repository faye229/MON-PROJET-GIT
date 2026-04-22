# serializer.py
import json
from models import Network, Node, Link


class NetworkSerializer:

    @staticmethod
    def to_dict(network):
        return {
            "nodes": [{"id": n.id} for n in network.nodes.values()],
            "links": [
                {
                    "a": l.node_a.id,
                    "b": l.node_b.id,
                    "bandwidth": l.bandwidth,
                    "latency": l.latency
                }
                for l in network.links
            ]
        }

    @staticmethod
    def save_json(network, path):
        with open(path, "w") as f:
            json.dump(NetworkSerializer.to_dict(network), f, indent=4)

    @staticmethod
    def load_json(path):
        with open(path, "r") as f:
            data = json.load(f)

        network = Network()

        # recréer nodes
        for n in data["nodes"]:
            network.add_node(Node(n["id"]))

        # recréer links
        for l in data["links"]:
            network.add_link(l["a"], l["b"], l["bandwidth"], l["latency"])

        return network