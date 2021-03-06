import sys


class Node:
    """
    Class which constructs a Node. This kind of node has 4 attributes. Its own name/which node it is (node),
    Its neighbours (possible nodes to transition to), if the node has been visited before and its predecessor.
    """
    def __init__(self, node, neighbours):
        self.node = node
        self.neighbours = neighbours
        self.visited = False
        self.pred = None


def construct_graph():
    """
    Reads the data from the input file (from stdin) and constructs a graph of nodes(vertices),
    where every node has some neighbour nodes which can be directly reached by the current node
     (which represent the arcs/edges in a graph).
    :return nodes, queries: List of nodes, List of start nodes and end nodes (used for testing).
    """
    lines = sys.stdin.readlines()
    num_words, num_queries = lines.pop(0).split(' ')
    num_words, num_queries = int(num_words), int(num_queries)

    lines = [line.rstrip() for line in lines]

    words = lines[:num_words]
    _queries = lines[num_words:]
    _queries = [query.split() for query in _queries]

    nodes = []
    for word in words:
        nodes.append(Node(word, []))

    for node in nodes:
        neighbours = get_neighbours(node.node, words)
        for neighbour in neighbours:
            node.neighbours.append(get_node(neighbour, nodes))

    queries = []
    for start, end in _queries:
        for node in nodes:
            if start == node.node:
                start_node = node
            if end == node.node:
                end_node = node

        queries.append([start_node, end_node])

    return nodes, queries


def get_neighbours(word, words):
    """
    Takes a word and list of all words and finds, for the word, all other words which contains the four last
    characters in it.
    :param word: Current word
    :param words: All words
    :return: Names of all neighbours corresponding to the node with name word.
    """
    ending = word[1:]
    len_ending = len(ending)
    neighbours = []
    for other in words:
        overlap = 0
        other_temp = [char for char in other]
        if other != word:
            for char in ending:
                if char in other_temp:
                    overlap += 1
                    other_temp.remove(char)
            if overlap == len_ending:
                neighbour = ''.join(other)
                neighbours.append(neighbour)
    return neighbours


def get_node(word, nodes):
    """
    Finds the node object which has the name 'word'.
    :param word: Current word.
    :param nodes: List of all nodes.
    :return: Node with name 'word'
    """
    for node in nodes:
        if word == node.node:
            return node


def BFS(graph, s, t):
    """
    Implements a BFS in order to find the shortest path from one node to another. If the target node
    is found, it backtracks through the traversed nodes using the .pred attribute of the node class.
    :param graph: tree to be traversed.
    :param s: start node.
    :param t: target node.
    :return: the number of nodes it had to traverse in order to find the target node.
    """

    q = []
    nmbr_of_moves = 0

    for v in graph:
        v.visited = False

    s.visited = True
    q.append(s)
    if s.node == t.node: return 0
    while q:
        v = q.pop(0)
        for neighbour in v.neighbours:
            if not neighbour.visited:
                neighbour.visited = True
                q.append(neighbour)
                neighbour.pred = v
                if neighbour == t:
                    while neighbour.pred.node != s.node:
                        nmbr_of_moves = nmbr_of_moves + 1
                        neighbour = neighbour.pred
                    return nmbr_of_moves + 1


if __name__ == '__main__':
    nodes, queries = construct_graph()
    for query in queries:
        nbr_moves = BFS(nodes, query[0], query[1])
        if nbr_moves is None:
            print('Impossible')
        else:
            print(nbr_moves)

