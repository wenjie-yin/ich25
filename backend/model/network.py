"""Network Class
"""

import numpy as np
import agent
from collections import deque
from backend.app.main import WorldState

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
    def filter_feed(self, node):
        agents = {i for i in self.get_adjacent(node)}
        return filter(lambda x: x.agent in agents, self.feed)
    
    def update_with_user_input(self, message: str):
        """Update agent certaintys from user's message
        """
        user = self.get_user()
        for node in graph.get_adjacent(node):
            agent.



    def update_with_agent_crosstalk(self):
        """Update certaintys through exchange of information
        across agent graph
        """
        raise NotImplementedError
    
    def serialise(self) -> WorldState:
        return WorldState(
            matrix=self.adjacency_matrix.tolist(),
            current_message=""
        )
 

class Node:
    def __init__(self, initial_certainty, agent):
        self._certainty = initial_certainty
        self.agent = agent

    def get_agent(self):
        return self.agent

    @property
    def certainty():
        return
    
    def set_certainty(value):
        self._certainty = value
