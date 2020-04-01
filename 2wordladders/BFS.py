def BFS(tree, s, t):
    q = []
    nmbr_of_moves =0

    for v in tree:
        v.visited = False

    s.visited = True
    q.append(s)

    while q:
        v=q.pop(0)
        for neighbour in v.neighbour:
            if not neighbour.visited:
                neighbour.visited=True
                q.append(neighbour)
                neighbour.pred=v
                if neighbour==t:
                    print('found path s-t')
                    while neighbour.pred:
                        nmbr_of_moves=nmbr_of_moves+1
                        neighbour=neighbour.pred
                    return nmbr_of_moves
    print('found no path s-t')