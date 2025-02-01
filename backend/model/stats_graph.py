"""Belief Network
"""

import numpy as np
import matplotlib.pyplot as plt
from backend.model.network import Network


class StatMechProp(Network):
    def __init__(self):
        self.beliefs = self._initalise_beliefs(N)
        self.adjacency_matrix = self._initialise_adjacency_matrix(N)
        self.N = N
        self.comm_threshold = 1
        self.threshold = self.comm_threshold / N
    
    def get_adjacent(self, node):
        raise NotImplementedError

    def get_belief(self, node):
        """Get belief state of node
        Args:
            node : Node object
        """
        raise NotImplementedError
    
    def set_belief(self, node, belief):
        """Set belief state of node
        Args:
            node: Node object
            belief (float): Belief level
        """
        pass

    
    def spread_belief(self):
        state_accum = self.adjacency_matrix @ self.beliefs
        self.beliefs = np.round(state_accum)
    
    # Helper functions
    def _transfer(self, x):
        return 1 / (1 + np.exp(-x))

    def _initalise_beliefs(self, N):
        return np.random.randint(2, size=N)
    
    def _initialise_adjacency_matrix(self, N):
        M = np.random.randint(2, size=(N, N))
        M = M * (1 - np.identity(N))
        return M


