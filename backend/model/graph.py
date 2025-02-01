"""Belief Network
"""

import numpy as np
import matplotlib.pyplot as plt


class Node:
    """Node"""
    def __init__(self):
        self._id_num = hex(id(self))

    @property
    def id_num(self):
        return self._id_num

    def get_agent():
        raise NotImplementedError



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
        self.beliefs = self._initalise_beliefs(N)
        self.adjacency_matrix = self._initialise_adjacency_matrix(N)
        self.N = N
    
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
        raise NotImplementedError
    
    def serialise(self):
        raise NotImplementedError
    
    def spread_belief(self):
        belief_updates = {i: [] for i in range(self.N)}
        for i in range(self.N):
            for j in range(i, self.N):
                p = self.adjacency_matrix[i,j]
                if p != 0:
                    #updates_i.append(self.beliefs[j])
                    belief_updates[i].append(self.beliefs[j])
            
            #if len(updates_i) > 0:
            #    belief_updates[i] = np.mean(updates_i)


        # Threshold beliefs
        print(belief_updates)
        new_beliefs = np.array([ np.mean(v) if len(v) > 0 else 0 for v in belief_updates.values() ])
        self.beliefs = (self.beliefs + new_beliefs)/2
        self.beliefs = np.round(self.beliefs)

    def spread_belief_v2(self):
        #A = self.adjacency_matrix / 
        state_accum = (self.adjacency_matrix @ self.beliefs) / normalisation
        print(state_accum)
        self.beliefs = np.round(state_accum)

    def _initalise_beliefs(self, N):
        return np.random.randint(2, size=N)
    
    def _initialise_adjacency_matrix(self, N):
        M = np.random.randint(2, size=(N, N))
        M = M * (1 - np.identity(N))
        return M
    

