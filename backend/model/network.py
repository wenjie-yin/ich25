"""Network Class
"""

import numpy as np
from collections import deque


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
    def __init__(self, N):
        """Initialise Network
        Args:
            N : Number of nodes in network
        """
        self.N = N
        self.feed = deque(maxlength=N*4) #TODO: should we reset this every tick?

        # Initialise nodes
        inital_beliefs = np.random.randint(2, size=N)
        nodes = [Node(b) for b in inital_beliefs]

        # Initialise connectivity
        adjacency_matrix = np.random.uniform(0, 1, size=(N, N))


    def filter_feed(self, agent):
        agents =
        return filter(lambda x: x.agent in agents, self.feed)
    
    def update_with_user_input(self, message: str):
        """Update agent beliefs from user's message
        """
        user = self.get_user()


    def update_with_agent_crosstalk(self):
        """Update beliefs through exchange of information
        across agent graph
        """
        raise NotImplementedError
    
    def serialise(self):
        raise NotImplementedError
 

class Node:
    def __init__(self, initial_belief, agent):
        self._belief = initial_belief
        self.agent = agent

    @property
    def belief():
        return
    
    def set_belief(value):
        self._belief = value
    

