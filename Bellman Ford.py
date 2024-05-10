class ShortestPathFinder:
    """
    A class to find the shortest path between two stops using the Bellman-Ford algorithm.
    """

    def __init__(self, connections):
        """
        Initializes the ShortestPathFinder with connections between stops.

        Args:
        - connections (list): A list of tuples representing connections between stops. Each tuple contains three elements:
                              (start_stop, end_stop, travel_time).
        """
        self.connections = connections

    def bellman_ford(self, start, end):
        """
        Finds the shortest path between two stops using the Bellman-Ford algorithm.

        Args:
        - start (int): Index of the starting stop.
        - end (int): Index of the ending stop.

        Returns:
        - list: The shortest path from the starting stop to the ending stop.
        """
        # Initialize distances from the starting stop to all other stops as infinity
        distances = [float('inf')] * len(self.connections)
        distances[start] = 0

        # Relaxation loop
        for _ in range(len(self.connections) - 1):
            for start_stop, end_stop, travel_time in self.connections: # tu powinno być odwoływanie do adjacency matrix a nie połączeń w formie tuple (1,2,3)
                if distances[start_stop] != float('inf') and distances[start_stop] + travel_time < distances[end_stop]:
                    distances[end_stop] = distances[start_stop] + travel_time

        # Check for negative cycles
        for start_stop, end_stop, travel_time in self.connections:
            if distances[start_stop] != float('inf') and distances[start_stop] + travel_time < distances[end_stop]:
                print("The transportation network contains a negative cycle")
                return []

        # Constructing the path
        path = [end]
        current_stop = end
        while current_stop != start:
            for start_stop, end_stop, travel_time in self.connections:
                if start_stop == current_stop and distances[end_stop] == distances[current_stop] - travel_time:
                    path.insert(0, end_stop)
                    current_stop = end_stop
                    break

        return path


# Example connections between stops
connections = [
    (0, 1, 3), (1, 0, 3), (1, 2, 2), (1, 3, 1), (1, 4, 3), (1, 6, 4), (2, 1, 2), (2, 4, 3), (3, 0, 5),
    (3, 1, 1), (3, 5, 5), (3, 6, 7), (3, 7, 1), (4, 0, 10), (4, 1, 3), (4, 2, 3), (4, 5, 1), (4, 6, 2),
    (4, 7, 2), (4, 9, 1), (5, 2, 2), (5, 3, 5), (5, 4, 1), (5, 6, 3), (5, 7, 3), (6, 1, 4), (6, 3, 7),
    (6, 4, 2), (6, 7, 2), (6, 8, 1), (7, 2, 4), (7, 3, 1), (7, 4, 2), (7, 5, 3), (7, 6, 2), (7, 8, 1),
    (7, 9, 4), (8, 6, 1), (8, 7, 1), (8, 9, 4), (9, 6, 1), (9, 7, 4), (9, 8, 4)
]

# Create an instance of ShortestPathFinder
path_finder = ShortestPathFinder(connections)

# Example function call
start = int(input("Enter the starting stop: "))
end = int(input("Enter the ending stop: "))
print("Shortest path:", path_finder.bellman_ford(start, end))
