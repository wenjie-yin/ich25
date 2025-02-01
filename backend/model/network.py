"""Network Class
"""

import numpy as np
import backend.llm_agent as llm_agent
from collections import deque
from backend.app.main import WorldState
from backend.model.dynamics import Stochastic


class FeedEntry:
    def __init__(self, message, agent):
        self.message = message
        self.agent = agent

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
        self.feed = deque(maxlength=N*4) #TODO: should we reset this every tick?

        # Initialise nodes
        inital_certaintys = np.random.randint(2, size=N)
        self.nodes = [Node(b) for b in inital_certaintys]

        # Initialise connectivity
        self.adjacency_matrix = np.random.uniform(0, 1, size=(N, N))
        self.llm_agent = llm_agent.Agent()
        
        # Initialise stochastic belief propagation network
        self.stochastic_network = Stochastic(self.n_nodes)

    def filter_feed(self, node):
        agents = {i for i in self.get_adjacent(node)}
        return filter(lambda x: x.agent in agents, self.feed)
    

    def update_with_user_input(self, message: str):
        """Update agent certaintys from user's message
        """
        self.feed.append(FeedEntry(message, None))

        for node in self.nodes:
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

    def serialise(self):
        matrix = self.adjacency_matrix.tolist()
        beliefs = [ node.get_certainty() for node in self.nodes ]
        return matrix, beliefs
 

class Node:
    def __init__(self, initial_certainty):
        self._certainty = initial_certainty


    def get_agent(self):
        return self.agent

    @property
    def certainty():
        return
    
    def set_certainty(value):
        self._certainty = value
