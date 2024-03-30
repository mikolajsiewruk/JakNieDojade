t1=[[0,3,0,5,10,0,0,0,0,0],
    [3,0,2,1,3,0,4,0,0,0],
    [0,2,0,0,3,2,0,4,0,0],
    [5,1,0,0,0,5,7,1,0,0],
    [10,3,3,0,0,1,2,2,0,1],
    [0,0,2,5,1,0,3,3,0,0],
    [0,4,0,7,2,3,0,2,1,0],
    [0,0,4,1,2,3,2,0,1,4],
    [0,0,0,0,0,0,1,1,0,1],
    [0,0,0,0,1,0,0,4,1,0]]

h = [[1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,1,1,1,1,1,1]]


def pathfinding(start:int, finish:int) ->list:
    path = [start]
    neighbours = []
    distances = []
    q = 0
    while path[-1] != finish:
        for k in path:
            for i in range(len(t1)):
                if t1[i][k] != 0 and i not in neighbours and i not in path:
                    neighbours.append(i)
                    f = q + t1[i][k] + h[i][k]
                    distances.append(f)
        q += min(distances)
        closest = neighbours[distances.index(min(distances))]
        if t1[path[-1]][closest] != 0:
            path.append(closest)
        else:
            continue
        neighbours.clear()
        distances.clear()
    return path

print(pathfinding(1, 9))