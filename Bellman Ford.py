import json
import time as tm
class ShortestPath:
    """
    A class to find the shortest path between two stops using the Bellman-Ford algorithm.
    """

    def __init__(self, adjacency_matrix):
        """
        Initializes the ShortestPathFinder with an adjacency matrix representing connections between stops.

        Args:
        - adjacency_matrix (list): A 2D list representing the adjacency matrix of the graph.
        """
        self.adjacency_matrix = adjacency_matrix

    def bellman_ford(self, start, end):
        """
        Finds the shortest path between two stops using the Bellman-Ford algorithm.

        Args:
        - start (int): Index of the starting stop.
        - end (int): Index of the ending stop.

        Returns:
        - tuple: A tuple containing the shortest path from the starting stop to the ending stop and the total travel time.
        """
        num_stops = len(self.adjacency_matrix)
        # Initialize distances from the starting stop to all other stops as infinity
        distances = [float('inf')] * num_stops
        distances[start] = 0

        # Relaxation loop
        for _ in range(num_stops - 1):
            for current_stop in range(num_stops):
                for next_stop in range(num_stops):
                    if self.adjacency_matrix[current_stop][next_stop] != 0 and distances[current_stop] != float('inf'):
                        if distances[current_stop] + self.adjacency_matrix[current_stop][next_stop] < distances[next_stop]:
                            distances[next_stop] = distances[current_stop] + self.adjacency_matrix[current_stop][next_stop]

        # Check for negative cycles
        for current_stop in range(num_stops):
            for next_stop in range(num_stops):
                if self.adjacency_matrix[current_stop][next_stop] != 0 and distances[current_stop] + self.adjacency_matrix[current_stop][next_stop] < distances[next_stop]:
                    print("The transportation network contains a negative cycle")
                    return [], float('inf')

        # Constructing the path and calculating total travel time
        path = [end]
        current_stop = end
        total_time = 0
        while current_stop != start:
            for next_stop in range(num_stops):
                if self.adjacency_matrix[next_stop][current_stop] != 0 and distances[next_stop] == distances[current_stop] - self.adjacency_matrix[next_stop][current_stop]:
                    path.insert(0, next_stop)
                    total_time += self.adjacency_matrix[next_stop][current_stop]
                    current_stop = next_stop
                    break

        return path, total_time

# Load graph from JSON
with open("Dane/graph.json", "r") as file:
    graph_data = json.load(file)

# Extract adjacency matrix from JSON data
adjacency_matrix = graph_data[0]['graph']
# Create an instance of ShortestPathFinder
path_finder = ShortestPath(adjacency_matrix)

# Example function call
start = int(input("Enter the starting stop: "))
end = int(input("Enter the ending stop: "))
shortest_path, total_time = path_finder.bellman_ford(start, end)
print("Shortest path:", shortest_path)
print("Total travel time:", total_time)
