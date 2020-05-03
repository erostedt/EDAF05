import sys

class Node:
    """
    Class which constructs a Node. This kind of node has 4 attributes. Its own name/which node it is (node),
    Its neighbours and the weights of the roads there (possible nodes to transition to), if the node has been visited before and its predecessor.
    """

    def __init__(self, node, neighbourweights):
        self.node = node
        self.neighbourweights = neighbourweights
        self.parent = None
        self.size = 0


def construct_graph():
    #lines = sys.stdin.readlines()
    lines=['3 2','3 2 3']
    num_nodes, num_roads = lines.pop(0).split(' ')
    print('2')
    for line in range(len(lines)):
        node1, node2, weight = lines[line].split(' ')
        lines[line]=[node1,node2,weight]

    nodes = []
    for num in range(int(num_nodes)):
        nodes.append(Node(int(num),[]))
    print(lines)
    lines[1][1]
    for connections in lines:
        nodes[int(connections[1])].neighbourweights.append[int(connections[2]), int(connections[3])]
        nodes[int(connections[2])].neighbourweights.append[int(connections[1]), int(connections[3])]

    return nodes

construct_graph()


def kruskal(nodes):
    """
    Constructs a minimal spanning tree utilizing Kruskal's algorithm.
    :param nodes: List of node objects.
    :return MST: Returns list of nodes which represents minimal spanning tree.
    """
    MST = []
    edges = set()
    for node in nodes:
        for neighbour, weight in node.neighbourweight:
            edges.add((node, neighbour, weight))

    edges = sorted(edges, key=lambda w: w[2])

    for edge in edges:
        node, neighbour, weight = edge

        if not cycle(node, neighbour):
            union(node, neighbour)
            MST.append(edge)

    return MST


def find(node):
    """
    Finds canonical member for the node.
    :param node: Node object.
    :return member: Canonical member.
    """
    member = node
    while member.parent:
        member = member.parent
    while node.parent:
        w = node.parent
        node.parent = member
        node = w
    return member


def union(node, neighbour):
    """
    Merges the set node belongs to with the set neighbour belongs to.
    :param node: Node object.
    :param neighbour: Neighbour node object.
    """
    node = find(node)
    neighbour = find(neighbour)
    if node.size < neighbour.size:
        node.parent = neighbour
        neighbour.size = node.parents + neighbour.parents
    else:
        neighbour.parent = node
        node.size = node.parents + neighbour.parents


def cycle(node, neighbour):
    """
    Checks if a node and a neighbour belongs to the same root, i.e creates a cycle.
    :param node: Node object.
    :param neighbour: Neighbour node object.
    :return: True if they have the same root. False else.
    """
    return find(node) is find(neighbour)













