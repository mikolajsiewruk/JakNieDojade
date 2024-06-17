# JakNieDojade

Public transportation investment analysis based on graph algorithms using Python, SQL and GIS technologies. Current subject of analysis is MPK Wroclaw transportation system.

## Abstract
The research project was aimed to measure the impact of new investments on Wrocław's transportation system. All public transportation lines were collected in a graph structure which was later analised with graph algorithms solvind known graph problems such as Dijkstra's, Bellman-Ford and A* algorithms for shortest path problem, Held-Karp and nearest neighbor algorithm for Travelling Salesman problem and Kruskal's and Prim's algorithm for minimal spanning tree problem. The graph was subjected to testing before and after all investments were added. The calculations were made using Monte Carlo simulations. The presented results might serve as valuable insight to which investments are the most important for the city's community.

### Skills and Technology
* Data structures and algorithms
* Python
* SQL databases
* Data collection and formatting
* Data visualisation
* Object Oriented Programming
* Monte Carlo simulations
* Optimization
### Methodology
1. Information about stops and travel distance between them was collected from MPK Wroclaw's website with  BeautifulSoup library and then put into a SQL database.
2. The public transportation lines were presented as dictionaries in JSON format with lists representing route and travel time.
3. The graph used for testing was presented in adjacency matrix form, where the weight of (i,j) was travel time between stops of index i and j.
4. The subject of calculations was travel time on short, medium and long distance in graphs with and without tested investment.
5. Information about travel destinations for each neighborhood was collected in a survey.
6. The simulations took into account where the majority of residents of each neighborhood were going by public transportation. 
