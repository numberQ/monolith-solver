class Node:

    def __init__(self, score, coords):
        self.score = score
        self.coords = coords

        self.children = []

    def insert(self, node):
        self.children.append(node)

    def __str__(self):
        return str(self.coords) + " -> " + ''.join([str(child) for child in self.children])
