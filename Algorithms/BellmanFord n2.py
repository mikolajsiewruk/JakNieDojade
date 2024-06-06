import json
def bellman_ford(graph: list, start: int, end: int):
    """
    Finds the shortest path between two stops using the Bellman-Ford algorithm.

    Args:
        - graph (list[list[int]]): Adjacency matrix representation of the graph.
        - start (int): Index of the starting stop.
        - end (int): Index of the ending stop.

    Returns:
        - tuple: A tuple containing the shortest path from the starting stop to the ending stop and the total travel time.
    """

    num_stops = len(graph)  # Get the number of stops (vertices) in the graph

    # Convert the adjacency matrix to a list of edges (tuples representing [start, end, weight])
    edge_list = []
    for i in range(num_stops):
        for j in range(num_stops):
            if graph[i][j] != 0:
                edge_list.append([i, j, graph[i][j]])  # Create an edge tuple

    # Initialize distances from the starting stop to all other stops as infinity
    distances = [float("inf")] * num_stops
    distances[start] = 0  # Set the distance to the starting stop as 0

    # Update distances by considering each edge in the graph
    for _ in range(num_stops - 1):  # Repeat the relaxation process n - 1 times
        for edge in edge_list:  # Iterate over each edge in the graph
            start_stop, end_stop, weight = edge  # Extract start, end, and weight from the edge
            if distances[start_stop] != float("inf") and distances[start_stop] + weight < distances[end_stop]:
                distances[end_stop] = distances[start_stop] + weight  # Update the distance if it's shorter

    # Check for negative cycles in the graph
    for edge in edge_list:
        start_stop, end_stop, weight = edge
        if distances[start_stop] != float("inf") and distances[start_stop] + weight < distances[end_stop]:
            print("The transportation network contains a negative cycle")
            return [], float("inf")  # Return an empty path and infinity if a negative cycle is found

    # Reconstruct the shortest path from the ending stop to the starting stop
    path = [end]
    current_stop = end
    length = 0
    while current_stop != start:
        for edge in edge_list:
            next_stop, prev_stop, weight = edge
            if prev_stop == current_stop and distances[next_stop] == distances[current_stop] - weight:
                path.insert(0, next_stop)  # Prepend the next stop to the path
                length += weight  # Update the total travel time
                current_stop = next_stop  # Move to the next stop
                break

    return path, length  # Return the shortest path and total travel time
file_path = "C:\\Users\\paula\\PycharmProjects\\JakNieDojade\\Dane\\graph.json"
with open(file_path, "r") as file:
    graph_data = json.load(file)

start_stop = 13
end_stop = 527
shortest_path, total_time = bellman_ford(graph_data, start_stop, end_stop)
print("Shortest Path:", shortest_path)
print("Total Travel Time:", total_time)