
class Node:
    """
    A* Node class for Path Finding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost to end
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position