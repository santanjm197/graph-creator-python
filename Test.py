from Vertex import Vertex
from Graph import Graph
from ShortestPathCalculator import ShortestPathCalculator

g = Graph()
g.add_vertices(Vertex(0, 1, 1, 1), Vertex(0, 2, 2, 2), Vertex(0, 3, 3, 3), Vertex(0, 4, 4, 4), Vertex(0, 5, 5, 5))
g.create_edge(1,2,6)
g.create_edge(1,3,300)
g.create_edge(1,4,150)
g.create_edge(2,3,30)
g.create_edge(3,5,40)
g.create_edge(4,5,10)

source = g.find_vertex(1)
dest = g.find_vertex(5)

sp = ShortestPathCalculator()
sp.dijkstra(g, source, dest)
