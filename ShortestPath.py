
t2=[[0,2,0,5,0],
    [2,0,3,0,7],
    [0,3,0,1,0],
    [5,0,1,0,4],
    [0,7,0,4,0]]
class ShortestPath:

# wyszukuje na razie tylko najkrótszą trasę od 1go do ostatniego, nie między dowolnymi
# dodać klasy na graf, kolejkę, drzewo itd
    def dijkstra(self,graph:list,start:int,end:int)-> list:
        """
        Dijkstras algorithm for finding the shortest path in a graph.
        :param graph: a graph of nodes in matrix form
        :param start: source
        :param end: target
        :return: list of shortest distances from node 0 to the last node
        """
        unvisited=set()
        for j in range(len(graph)):
            unvisited.add(j)
        distances=[]
        for i in range(len(graph)):
            distances.append("inf")
        distances[start]=0

        for j in range(len(graph)):
            current=graph[start+j]
            print(current)
            cur_ind=start+j
            print(cur_ind)

            for i in range(len(current)):
                if current[i]!=0 and i in unvisited:
                    if distances[i]=="inf":
                        print(distances[i],current[i],distances[cur_ind])
                        distances[i]=current[i]+distances[cur_ind]
                    elif distances[i]>current[i]+distances[cur_ind]:
                        print(distances[i], current[i], distances[cur_ind])
                        distances[i]=current[i]+distances[cur_ind]

        return distances
s=ShortestPath()

print(s.dijkstra(t2,0,4))


