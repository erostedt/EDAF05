import sys
from collections import deque, defaultdict
from itertools import islice


class Node:
    """
    Node class. A node holds its name, set of index of neighbours and parent node.
    """
    def __init__(self, name):
        """
        Initializes node object.
        :param name: node name
        """
        self.name = name
        self.neighbours = set()
        self.parent = None

    def __eq__(self, other):
        """
        Checks if two nodes have the same name. Since we have unique nodes, if the names are the same, then it must be the same node.
        """
        return True if self.name == other.name else False

class ResidualGraph:
    """
    Residual Graph class. Contains the edges with remaining capacities as dict with edge as key and capacity as value.
    Dict of nodes.
    Edges to add to the (possibly) incomplete network.
    number of nodes in the full network.
    Source and sink node
    """
    def __init__(self):
        """
        Initializes residual graph
        """
        self.remaining_capacities = defaultdict(int)
        self.nodes = defaultdict(Node)
        self.edges_to_add = []
        self.source = None
        self.sink = None

    def insert_edge(self, edge, val):
        """
        Adds an edge to the graph. Creates new nodes if node is missing, if so also checks if the node is source or sink.
        :param edge: edge to be added.
        :param val: capacity of the added edge
        """
        rev_edge = (edge[1], edge[0])
        self.remaining_capacities[edge] = val
        self.remaining_capacities[rev_edge] = val
        self.nodes[edge[0]].neighbours.add(edge[1])
        self.nodes[edge[1]].neighbours.add(edge[0])

    def reset_parents(self):
        """
        Resets the parents.
        """
        for node in self.nodes.itervalues():
            node.parent = None
    

def parse():
    """
    Parses the input and constructs an residual graph.
    :return graph: Residual graph.
    :return min_flow: Minimum tolerated flow.
    """
    lines = sys.stdin.readlines()

    lines = deque([tuple(map(int, line.strip().split())) for line in lines])
    num_nodes, num_edges, min_flow, _ = lines.popleft()

    _edges = deque(islice(lines, 0, num_edges))
    _edges_to_add = set(route[0] for route in islice(lines, num_edges, None))
    
    idx_to_edge = defaultdict(tuple)
    graph = ResidualGraph()

    for i, edge in enumerate(_edges):
        u, v, c = edge

        # Add nodes if they are missing
        if u not in graph.nodes:
            graph.nodes[u] = Node(u)
            if u == 0:
                graph.source = graph.nodes[u]
            if u == num_nodes - 1:
                graph.sink = graph.nodes[u]
            
        if v not in graph.nodes:
            graph.nodes[v] = Node(v)
            if v == 0:
                graph.source = graph.nodes[v]
            if v == num_nodes - 1:
                graph.sink = graph.nodes[v]

        if i not in _edges_to_add:
            graph.insert_edge((u, v), c)

        else:
            idx_to_edge[i] = (u, v, c)

    graph.edges_to_add = [idx_to_edge[i] for i in _edges_to_add]
    return graph, min_flow

def BFS(graph):
    """
    Bredth first search through the graph, from source to sink.
    :param graph: Residual graph.
    :return: True if there is a path from source to sink, else False.
    """
    graph.reset_parents()
    q = deque([graph.source])

    while q:
        node = q.popleft()
        for _neighbour in node.neighbours:
            neighbour = graph.nodes[_neighbour]
            edge = (node.name, _neighbour)
            if not neighbour.parent and graph.remaining_capacities[edge] > 0:
                neighbour.parent = node
                q.append(neighbour) 
                if neighbour == graph.sink:
                    return True      
    
    return False

def ford_fulkerson(graph):
    """
    Finds the max flow in graph.
    :param graph: Residual graph.
    :return: max flow
    """
    max_flow = 0
    while BFS(graph): 
        pflow = float('Inf')
        node = graph.sink
        while node != graph.source:
            edge = (node.parent.name, node.name)
            delta = graph.remaining_capacities[edge]
            pflow = min(pflow, delta)              
            node = node.parent

        node = graph.sink
        while node != graph.source:
            edge = (node.parent.name, node.name)
            rev_edge = (node.name, node.parent.name)
            graph.remaining_capacities[edge] -= pflow
            graph.remaining_capacities[rev_edge] += pflow
            node = node.parent

        max_flow += pflow
    return max_flow

if __name__ == "__main__":
    """
    Finds the number routes that we can remove and all the flow.
    """
    graph, min_flow = parse()
    while not graph.source or not graph.sink:
        u, v, c = graph.edges_to_add.pop()
        graph.insert_edge((u, v), c)

    flow = ford_fulkerson(graph)

    while flow < min_flow:
        u, v, c = graph.edges_to_add.pop()
        graph.insert_edge((u, v), c)
        flow += ford_fulkerson(graph)

    print(str(len(graph.edges_to_add)) + ' ' + str(flow))
