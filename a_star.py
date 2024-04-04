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
        path.append(closest)
        neighbours.clear()
        distances.clear()
    return path

def xd(s,f):
    closed=set()
    opened=set()
    opened.add(s)
    q=0
    path=[s]
    x=s
    neighbors=[]
    while opened:
        if x == f:
            path.append(x)
            return path
        opened.remove(x)
        closed.add(x)
        for nodes in path:
            for i in range(len(t1)):
                if t1[i][nodes]!=0:
                    neighbors.append(i)
        for y in neighbors:
            if y in opened:

            m=min
            ten=q+min(t1[y])




print(pathfinding(1, 9))


# niedziałający gdyż nieraz znajdowany node nie jest w ciągu, lecz jest rozgałęzieniem
# wciąż brak opcji rozpatrywania kilku rozgałęzień jednocześnie - oddzielnie