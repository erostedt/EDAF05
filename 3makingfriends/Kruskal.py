import sys

class Node:
    """
    Class which constructs a Node. This kind of node has 3 attributes. Its own name/which node it is (node),
    Its neighbours and the weights of the roads there (possible nodes to transition to), and its predecessor.
    """

    def __init__(self, node, neighbourweights):
        self.node = node
        self.neighbourweights = neighbourweights
        self.pred = None


def construct_graph():
    """
    Reads the data from the input file (from stdin) and constructs a graph of nodes(vertices),
    where every node has some neighbour node(s) which can be directly reached by the current node
    by going a certain distance.
    :return nodes: List of nodes.
    """
    lines = sys.stdin.readlines()
    num_nodes, num_roads = lines.pop(0).split(' ')

    for line in range(len(lines)):
        node1, node2, weight = lines[line].split(' ')
        lines[line]=[node1,node2,weight]

    nodes = []
    for num in range(int(num_nodes)+1):
        nodes.append(Node(int(num),[]))

    for connections in lines:
        nodes[int(connections[0])].neighbourweights.append([nodes[int(connections[1])],int(connections[2])])#,int(connections[2])])
        nodes[int(connections[1])].neighbourweights.append([nodes[int(connections[0])], int(connections[2])])


    return nodes