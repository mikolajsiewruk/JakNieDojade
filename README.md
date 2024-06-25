
# JakNieDojade

Public transportation investment analysis based on graph algorithms using Python, SQL and GIS technologies. Current subject of analysis is MPK Wroclaw transportation system.

## Abstract
The research project was aimed to measure the impact of new investments on Wrocław's transportation system. All public transportation lines were collected in a graph structure which was later analised with graph algorithms solvind known graph problems such as Dijkstra's, Bellman-Ford and A* algorithms for shortest path problem, Held-Karp and nearest neighbor algorithm for Travelling Salesman problem and Kruskal's and Prim's algorithm for minimal spanning tree problem. The graph was subjected to testing before and after all investments were added. The calculations were made using Monte Carlo simulations. The presented results might serve as valuable insight to which investments are the most important for the city's community.

### Skills and Technology
* Data structures and algorithms
* Python
* SQL
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

### Simulations
The sumulations conducted included analysis of public transportation network with all planned investments as well as separate analysis for each one of the proposed lines. The main method of simulation was Monte Carlo fashion repeated random sampling. The randomization took into consideration the importance of end stops which was measured as the amount of key facilities located near the stop, the possibility of a random person going to the particular stop - measured as the percentage of population living in the area of the end stop, and the most popular travel destinations for residents of each area.

### Results
#### All lines simulation
The simulation compared travel times between random stops in the current public transportation network and the network with proposed changes. 
1. Dijkstra's algorithm

The test subject was the travel time between two random stops before and after applying changes to the public transportation network. Sample differences are shown on the plots 1. and 2.
Path in the current graph
![cur 17](https://github.com/mikolajsiewruk/JakNieDojade/assets/152521027/5258a8ef-4e45-4d52-9002-f662ccff3208)
Path in the updated graph
![new 17](https://github.com/mikolajsiewruk/JakNieDojade/assets/152521027/c81312a0-fc18-498e-9626-8de78ea17d88)
