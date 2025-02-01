"""Inter-agent communication dynamics
"""

import numpy as np


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
        self.adjacency_matrix = np.random.randint(2, size=(n, n))
    
    def update(self, state):
        """Update state of the network given beliefs
        Args:
            state : An n-dimensional array of beliefs
        Returns:
            new_state: Updated beliefs
        """
        state_freeze = np.copy(state)
        updates = np.zeros(self.n_neurons)
        for i in range(self.n_neurons):
            for j in range(self.n_neurons):
                p_exchange = self.adjacency_matrix[i,j]
                comm = np.random.uniform(0, 1)
                if p_exchange > comm:
                    print(i, j, 'YANK', p_exchange)
                    updates[i] = (state_freeze[i] + state_freeze[j])/2
        
        return updates


# Test
state_0 = [1, 0]
matrix = np.array([[0, 1], [0, 0]])

S = Stochastic(2)
S.adjacency_matrix = matrix

print(S.adjacency_matrix)
print('S0:', state_0)
print('S1:', S.update(state_0))
