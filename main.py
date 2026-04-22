# main.py
from models import Network, Node, Packet
from serializer import NetworkSerializer
from logger import NetworkLogger

# création réseau
network = Network()

# nodes
A = Node("A")
B = Node("B")
C = Node("C")

network.add_node(A)
network.add_node(B)
network.add_node(C)

# links
network.add_link("A", "B")
network.add_link("B", "C")

# logger
logger = NetworkLogger()

# création paquet
p1 = Packet(A, C, size=10)
network.send_packet(p1)

# simulation
for _ in range(5):
    network.step()

# sauvegarde
NetworkSerializer.save_json(network, "network.json")

# logs
logger.log_packet(p1, "delivered")
logger.export_csv()

print("Simulation terminée")