"""Network Class
"""

import numpy as np
from backend.model.dynamics import Stochastic

class Network:
    """Graph representation
    - Nodes are represented by a length N vector b, with
    entries b_i between 0 and 1.
    - The graph is a matrix... that's it.
    """
    def __init__(self, n_nodes):
        """Initialise Network
        Args:
            N : Number of nodes in network
        """
        self.n_nodes = n_nodes

        # Initialise nodes
        self.inital_beliefs = np.random.randint(2, size=n_nodes)
        self.nodes = [ Node(b) for b in inital_beliefs ]

        # Initialise stochastic belief propagation network
        self.stochastic_network = Stochastic(self.n_nodes)

    def update_with_user_input(self, message: str):
        """Update agent beliefs from user's message
        """
        raise NotImplementedError

    def update_with_agent_crosstalk(self):
        """Update beliefs through exchange of information
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
        raise NotImplementedError
 

class Node:
    def __init__(self, initial_belief):
        self._belief = initial_belief

    @property
    def certainty():
        return
    
    def set_certainty(value):
        self._belief = value
    

