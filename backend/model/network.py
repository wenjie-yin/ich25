"""Abstract network class
"""

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
        self.nodes = [Node() for _ in range(N)]
    
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
        raise NotImplementedError

