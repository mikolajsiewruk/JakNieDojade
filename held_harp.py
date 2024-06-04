from Algorithms.ShortestPath import ShortestPath


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

s = ShortestPath

def graph_creation(graph, start, to_visit):
    stops = [start] + to_visit
    new_graph = [[0]*len(stops) for _ in range(len(stops))]
    indexes = []
    for i in range(len(stops)):
        indexes.append([i, stops[i]])  # Each sublist contains [current_index, IdP]
        for j in range (len(stops)):
            new_graph[i][j] = s.dijkstra(graph, stops[i], stops[j])[1]
    return new_graph


def held_karp(graph: list, start: int, to_go: list, reach: int, lista = []):
    if len(to_go) == 0:
        return [graph[start][reach]]
    else:
        lista.append(reach)
        x = []
        for stop in to_go:
            new_to_go = to_go.copy()
            new_to_go.remove(stop)
            new_to_reach = stop
            x.append(held_karp(graph, start, new_to_go, new_to_reach)[0]+graph[new_to_reach][reach])
        return [min(x), lista]
# no tak to wygląda aktualnie, lista się zwraca ale on przekazuje wartości do listy przy każdym przejściu rekurencji
# przez co ta lista nie działa tak jak powinna :((



# krótki opis jak to ma działać
# zaczynamy w 0
# szukamy C({1,2,3}, 0)
# nie wiemy jaka jest min(C({1,2},3)+graph[3][0], C({1,3}, 2)+graph[2][0], C({2,3},1)+graph[1][0])
# ale teraz nie wiemy jaka jest min(C({1},2)+graph[2][3], C({2},1)+graph[1][3]) ... tak samo dla pozostałych przypadków
# a potem nie wiemy jaka jest min(C{},1)+graph[1][2]
# i to już można policzyć, bo to jest graph[0][1]


new_graph = graph_creation(t1, 2, [4,6,7])
print(held_karp(new_graph, 0, [1,2,3], 0))
