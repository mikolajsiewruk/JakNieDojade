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

# NOTE TO MY FUTURE SELF

# Zrobione według barcelońskiego pseudokodu
# idk co tu się odpierdala, nie mam na to aktualnie siły pozdro
# kod nie działa bo nie ma rekonstrukcji ścieżki btw
# a no i brakuje heurystyki ale to najmniejszy problem
# pls kill me

# ogl potrzebuje jakoś mądrzej zapisywać wartości g i h każdego node'a w open i w closed
# bo aktualnie to jest tak że elementowi open[2] przypada g_of_open[2] i h_of_open[2]
# idiotyzm
# a no i idk jak z tym, który node jest rodzicem którego, niby jest lista parenthood
# ale aktualnie nieprzydatna
# powodzenia
def a_star(start, goal):
    open = []
    closed = []
    open.append(start)
    g_of_open = []
    h_of_open = []
    f_of_open = []
    g_of_open.append(0)
    h_of_open.append(1)
    f_of_open.append(h_of_open[0])
    g_of_closed = []
    neighbours =[]
    parenthood = []
    while open:
        index = f_of_open.index(min(f_of_open))
        current = open[index]
        if current == goal:
            break
        for i in range(len(t1)):
            if t1[i][current] != 0:
                neighbours.append(i)
        for neighbour in neighbours:
            neighbour_cost = []
            neighbour_cost.append(g_of_open[index] + t1[current][neighbour])
            if neighbour in open:
                index_neigh_in_open = open.index(neighbour)
                index_neigh_in_neigh = neighbours.index(neighbour)
                if g_of_open[index_neigh_in_open] <= neighbour_cost[index_neigh_in_neigh]:
                    continue
            elif neighbour in closed:
                index_neigh_in_open = closed.index(neighbour)
                index_neigh_in_neigh = neighbours.index(neighbour)
                if g_of_closed[index_neigh_in_open] <= neighbour_cost[index_neigh_in_neigh]:
                    continue
                closed.remove(neighbour)
                open.append(neighbour)
            else:
                open.append(neighbour)
                h_of_open.append(3) #### do heuristic to append
            g_of_open.append(neighbour_cost)

            fuckthis = True
            for family in parenthood:
                if family[1] == neighbour:
                    family[0] = current
                    fuckthis = False
            if fuckthis:
                parenthood.append([current, neighbour])
        closed.append(current)
    if current != goal:
        return False
