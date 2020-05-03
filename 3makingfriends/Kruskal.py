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


def kruskal(nodes):
    """
    Construct the minimal spanning tree, represented by a list of edges (tuples of node, neighbour node and weight)
    :param nodes: List of nodes.
    :return MST: Minimal spanning tree.
    """
    MST = []
    edges = set()
    for node in nodes:
        for neighbour, weight in node.neighbours:
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
    Finds canonical member of node.
    :param node: Node object
    :return member: Canonical member.
    """
    member = node
    while member.parent:
        member = member.parent
    while node.parent:
        node, node.parent = node.parent, member
    return member


def union(node, neighbour):
    """
    Merges the set node belongs to with the set that neighbour belongs to.
    :param node: Node object.
    :param neighbour: Neighbouring node object.
    """
    node = find(node)
    neighbour = find(neighbour)
    new_size = node.size + neighbour.size
    if node.size < neighbour.size:
        node.parent = neighbour
        neighbour.size = new_size
    else:
        neighbour.parent = node
        node.size = new_size


def cycle(node, neighbour):
    """
    Checks if a node and its neighbour has the same root, used to determine if nodes makes a cycle.
    :param node: Node object.
    :param neighbour: Neighbouring node object.
    :return: True if nodes have the same root, false else.
    """
    return find(node) is find(neighbour)


if __name__ == '__main__':
    nodes = construct_graph()
    MST = kruskal(nodes)
