import random

class Acceptor:
    def __init__(self, node_id):
        self.node_id = node_id
        self.promised_id = None
        self.accepted_value = None

    def prepare(self, proposal_id):
        if not self.promised_id or proposal_id > self.promised_id:
            self.promised_id = proposal_id
            return True
        return False

    def accept(self, proposal_id, value):
        if proposal_id >= self.promised_id:
            self.accepted_value = value
            return True
        return False

def simulate_paxos():
    acceptors = [Acceptor(i) for i in range(3)]
    proposal_id = random.randint(1, 100)
    value = "X=5"
    promises = 0

    for a in acceptors:
        if a.prepare(proposal_id):
            promises += 1

    if promises > len(acceptors) // 2:
        accepts = 0
        for a in acceptors:
            if random.choice([True, True, False]):  # simulate one failure
                if a.accept(proposal_id, value):
                    accepts += 1
        if accepts > len(acceptors) // 2:
            print(f"Consensus reached on value: {value}")
        else:
            print("Consensus failed in accept phase.")
    else:
        print("Consensus failed in prepare phase.")

simulate_paxos()
