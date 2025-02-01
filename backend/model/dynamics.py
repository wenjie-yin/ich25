"""Inter-agent communication dynamics
"""

import numpy as np
import matplotlib.pyplot as plt


class Stochastic:
    """Stochastic updates
    Agents i takes on the belief of agent j with
    probabiltiy p_ij. The matrix P describes all the
    exchange probabilities between agents. At each
    step, an agent can also randomly take on the
    belief with probability f and forget the belief
    with probability (1-f).
    """

    def __init__(self, n: int):
        self.n_neurons = n
        self.adjacency_matrix = np.random.uniform(0, 1, size=(n, n))
        self.adjacency_matrix *= (1 - np.identity(n))
    
    def update(self, state):
        """Update state of the network given beliefs
        Args:
            state : An n-dimensional array of beliefs
        Returns:
            new_state: Updated beliefs
        """
        state_freeze = np.copy(state)
        new_state = np.zeros(self.n_neurons)
        for i in range(self.n_neurons):
            for j in range(self.n_neurons):
                p_exchange = self.adjacency_matrix[i,j]
                comm = np.random.binomial(1, p_exchange, size=1)
                if comm:
                    new_state[i] = state_freeze[j]
        
        return np.round(new_state)

