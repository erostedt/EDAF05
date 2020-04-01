import sys


class Node:

    def __init__(self, node, neighbours):
        self.node = node
        self.neighbours = neighbours
        self.visited = False
        self.pred = None


def parse():
    lines = sys.stdin.readlines()
    num_words, num_queries = lines.pop(0).split(' ')
    num_words, num_queries = int(num_words), int(num_queries)

    lines = [line.rstrip() for line in lines]

    words = lines[:num_words]
    _queries = lines[num_words+1:]
    _queries = [query.split() for query in _queries]

    nodes = []
    for word in words:
        nodes.append(Node(word, None))


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


def BFS(tree, s, t):
    q = []
    nmbr_of_moves = 0

    for v in tree:
        v.visited = False

    s.visited = True
    q.append(s)

    while q:
        v = q.pop(0)
        for neighbour in v.neighbours:
            if not neighbour.visited:
                neighbour.visited = True
                q.append(neighbour)
                neighbour.pred = v
                if neighbour == t:
                    print('found path s-t')
                    while neighbour.pred:
                        nmbr_of_moves = nmbr_of_moves+1
                        neighbour = neighbour.pred
                    return nmbr_of_moves
    print('found no path s-t')


if __name__ == '__main__':
    nodes, queries = parse()
    for query in queries:
        nbr_moves = BFS(nodes, query[0], query[1])


