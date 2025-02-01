"""Network Class
"""

import numpy as np

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

        # Initialise nodes
        inital_beliefs = np.random.randint(2, size=N)
        nodes = [Node(b) for b in inital_beliefs]

        # Initialise connectivity
        adjacency_matrix = np.random.uniform(0, 1, size=(N, N))

    
    def update_with_user_input(self, message: str):
        """Update agent beliefs from user's message
        """
        raise NotImplementedError

    def update_with_agent_crosstalk(self):
        """Update beliefs through exchange of information
        across agent graph
        """
        raise NotImplementedError
    
    def serialise(self):
        raise NotImplementedError
 

class Node:
    def __init__(self, initial_belief):
        self._belief = initial_belief

    @property
    def belief():
        return
    
    def set_belief(value):
        self._belief = value
    

