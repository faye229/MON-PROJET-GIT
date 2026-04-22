# models.py
import time
from collections import deque


class Packet:
    def __init__(self, source, destination, size=1):
        self.source = source
        self.destination = destination
        self.size = size
        self.timestamp = time.time()
        self.path = []

    def __repr__(self):
        return f"Packet({self.source.id} -> {self.destination.id}, size={self.size})"


class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.buffer = deque()
        self.connections = []

    def connect(self, node):
        if node not in self.connections:
            self.connections.append(node)
            node.connections.append(self)

    def receive_packet(self, packet):
        self.buffer.append(packet)

    def send_packet(self):
        if self.buffer:
            return self.buffer.popleft()
        return None

    def process(self):
        packet = self.send_packet()
        return packet

    def __repr__(self):
        return f"Node({self.id})"


class Link:
    def __init__(self, node_a, node_b, bandwidth=100, latency=1):
        self.node_a = node_a
        self.node_b = node_b
        self.bandwidth = bandwidth
        self.latency = latency

    def transmit(self, packet):
        if packet.destination in [self.node_a, self.node_b]:
            packet.destination.receive_packet(packet)
        else:
            # simple routing (random pass)
            next_node = self.node_b if packet.source == self.node_a else self.node_a
            next_node.receive_packet(packet)


class Network:
    def __init__(self):
        self.nodes = {}
        self.links = []
        self.time = 0

    def add_node(self, node):
        self.nodes[node.id] = node

    def add_link(self, node_a_id, node_b_id, bandwidth=100, latency=1):
        node_a = self.nodes[node_a_id]
        node_b = self.nodes[node_b_id]

        link = Link(node_a, node_b, bandwidth, latency)
        self.links.append(link)
        node_a.connect(node_b)

    def send_packet(self, packet):
        packet.source.receive_packet(packet)

    def step(self):
        self.time += 1

        for node in self.nodes.values():
            packet = node.process()
            if packet:
                for link in self.links:
                    if node in [link.node_a, link.node_b]:
                        link.transmit(packet)
                        break