import sys


class Node:
    """
    Class which constructs a Node. This kind of node has 4 attributes. Its own name/which node it is (node),
    Its neighbours and the weights of the roads there (possible nodes to transition to), its parent and the number
    of children.
    """
    def __init__(self, node, neighbourweights):
        self.node = node
        self.neighbourweights = neighbourweights
        self.parent = None
        self.size = 0


def construct_graph():
    """
    Reads the data from the input file (from stdin) and constructs a graph of nodes(vertices),
    where every node has some neighbour node(s) which can be directly reached by the current node
    by going a certain distance. Constructs all edges of the tree.
    :return edges: List of edges.
    """
    lines = sys.stdin.readlines()
    num_nodes, num_roads = lines.pop(0).split(' ')
    for line in range(len(lines)):
        node1, node2, weight = lines[line].split(' ')
        lines[line] = [node1, node2, weight]

    nodes = []
    for num in range(int(num_nodes) + 1):
        nodes.append(Node(int(num), []))

    for connections in lines:
        nodes[int(connections[0])].neighbourweights.append([nodes[int(connections[1])], int(connections[2])])
        nodes[int(connections[1])].neighbourweights.append([nodes[int(connections[0])], int(connections[2])])

    edges = set()
    for node in nodes:
        for neighbour, weight in node.neighbourweights:
            if (neighbour, node, weight) not in edges:
                edges.add((node, neighbour, weight))

    return edges


def kruskal(edges):
    """
    Construct the minimal spanning tree, represented by a list of edges (tuples of node, neighbour node and weight)
    :param edges: List of edged, i.e list of tuples with node, neighbour node and weight.
    :return MST: Minimal spanning tree.
    """
    MST = []
    edges = sorted(edges, key=lambda w: w[2])

    for edge in edges:
        node, neighbour, weight = edge
        if union(node, neighbour):
            MST.append(edge)

    return MST


def find(node):
    """
    Finds canonical member of node.
    :param node: Node object
    :return root: Canonical member.
    """
    root = node
    while root.parent:
        root = root.parent
    while node.parent:
        node.parent, node = root, node.parent
    return root


def union(node, neighbour):
    """
    Merges the set node belongs to with the set that neighbour belongs to.
    :param node: Node object.
    :param neighbour: Neighbouring node object.
    """
    node = find(node)
    neighbour = find(neighbour)

    if node is neighbour:
        return False

    new_size = node.size + neighbour.size
    if node.size < neighbour.size:
        node.parent = neighbour
        neighbour.size = new_size
    else:
        neighbour.parent = node
        node.size = new_size

    return True


if __name__ == '__main__':
    edges = construct_graph()
    MST = kruskal(edges)
    sum_weights = 0
    for edge in MST:
        sum_weights += edge[2]
    print(sum_weights)
