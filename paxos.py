import random
import time
import threading

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.state = "follower"
        self.votes = 0
        self.leader = None
        self.active = True

    def start_election(self, cluster):
        self.state = "candidate"
        self.votes = 1
        for node in cluster:
            if node != self and node.active:
                if random.choice([True, False]):
                    self.votes += 1
        if self.votes > len(cluster) // 2:
            self.state = "leader"
            self.leader = self
            print(f"Node {self.node_id} became leader with {self.votes} votes.")

    def replicate_value(self, value, cluster):
        if self.state != "leader":
            return
        for node in cluster:
            if node != self and node.active:
                print(f"Leader {self.node_id} replicated value {value} to Node {node.node_id}.")
        print(f"Value {value} committed by Leader {self.node_id}.")

def simulate_raft():
    cluster = [Node(i) for i in range(3)]
    random.choice(cluster).start_election(cluster)
    leader = [n for n in cluster if n.state == "leader"][0]
    leader.replicate_value("A=1", cluster)

    # Simulate leader failure
    leader.active = False
    print(f"Leader {leader.node_id} has failed.")
    time.sleep(1)
    # Start new election
    for node in cluster:
        if node.active:
            node.start_election(cluster)
            break

simulate_raft()
