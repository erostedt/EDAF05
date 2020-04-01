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
    queries = lines[num_words+1:]

    nodes = []
    for word in words:
        neighbours = get_neighbours(word, words)
        nodes.append(Node(word, neighbours))

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


if __name__ == '__main__':
    parse()
















