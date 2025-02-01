"""Network Class
"""

import numpy as np
import backend.llm_agent as llm_agent
from collections import deque
from backend.app.main import WorldState
from backend.model.dynamics import Stochastic


class FeedEntry:
    def __init__(self, message, node_idx):
        self.message = message
        self.node_index = node_index

class Network:
    """Graph representation
    - Nodes are represented by a length N vector b, with
    entries b_i between 0 and 1.
    - The graph is a matrix... that's it.
    """
    def __init__(self, N, belief="The earth is flat"):
        """Initialise Network
        Args:
            N : Number of nodes in network
            belief : belief of interest for the entire network
        """
        self.N = N
        self.belief = belief 
        self.feed = deque(maxlen=N*4) #TODO: should we reset this every tick?

        # Initialise nodes
        inital_certaintys = np.random.randint(2, size=N)
        self.nodes = [Node(b) for b in inital_certaintys]

        # Initialise connectivity
        self.stochastic_network = Stochastic(self.N)
        self.adjacency_matrix = self.stochastic_network.adjacency_matrix
        self.llm_agent = llm_agent.Agent()

    def get_certainties(self):
        return [ node.certainty for node in self.nodes ]

    def filter_feed(self, node_index) -> deque:
        adjacent = self.get_adjacent(node_index)
        return list(filter(lambda x: x.node_index == node_index, self.feed))
    
    def get_adjacent(self, node_index):
        idxs = np.arange(0, self.N)
        idxs = idxs[idxs != i]
        adjacencies = self.adjacency_matrix[node_index]
        return [ i for i, w in zip(np.arange(0, self.N), adjacencies) if i != node_index and w == 1 ]
    
    def update_with_user_input(self, message: str):
        """Update agent certaintys from user's message
        """
        self.feed.append(FeedEntry(message, None))

        for i, node in enumerate(self.nodes):
            node_feed = self.filter_feed(i)
            node._certainty = self.llm_agent.update_certainty(self.belief, node._certainty, self.feed)

    def update_with_agent_crosstalk(self):
        """Update certaintys through exchange of information
        across agent graph
        """
        # Put belief state into vector
        network_state = np.array([node.get_certainty() for node in self.nodes])

        # Update beliefs with stochastic network
        new_network_state = self.stochastic_network.update(network_state)

        # Update belief states in node objects
        for i, new_certainty in enumerate(new_network_state):
            self.nodes[i].set_certainty(new_certainty)
    
    def update_feed(self):
        for node in self.nodes:
            post = self.llm_agent.write(self.belief, node._certainty, self.feed)
            self.feed.append(FeedEntry(post, node))

    def serialise(self):
        matrix = self.adjacency_matrix.astype(int).tolist()
        beliefs = [ node.get_certainty() for node in self.nodes ]
        return matrix, beliefs
 

class Node:
    def __init__(self, initial_certainty):
        self._certainty = initial_certainty

    def get_agent(self):
        return self.agent

    def get_certainty(self):
        return self._certainty
    
    def set_certainty(value):
        self._certainty = value

