from Graph import Graph
from Vertex import Vertex
import numpy as np


class ShortestPathCalculator:
    """
    Class which can use multiple different algorithms to calculate shortest paths in a graph

    Attributes
    ----------
    visited : set
        The set of currently visited vertices in a search
    unvisited : set
        The set of currently unvisited vertices in a search
    prev : dict
        A mapping of each vertex to the previous vertex in a search
    distances : dict
        (Dijkstra) A mapping of each vertex to the distance from it to the source node in a search

    Methods
    -------
    dijkstra(graph, source, dest)
        Find the shortest path between source and dest in the given graph using Dijkstra's algorithm
    """

    def __init__(self):
        # Algorithm agnostic attributes
        # The set of currently visited vertices
        self.visited = set()

        # The set of unvisited vertices (reset each time we do a new calculation)
        self.unvisited = set()

        # A map of each vertex in the graph to the previous vertex in the search
        self.prev = {}

        # Dijkstra specific attributes
        # A map of each vertex to the distance from it to the source vertex
        self.distances = {}

    def __reset(self):
        """Resets all of the attributes to empty"""
        # Reset the algorithm agnostic attributes
        self.visited = set()
        self.unvisited = set()
        self.prev = {}

        # Reset the Dijkstra specific attributes
        self.distances = {}

    # -------------------------------- #
    #                                  #
    #            Dijkstra              #
    #                                  #
    # -------------------------------- #

    def dijkstra(self, graph, source, dest):
        """Uses Dijkstra's shortest path algorithm to calculate the shortest path from source to dest

        Parameters
        ----------
        graph : Graph
            The graph that we will be using in the search
        source : Vertex
            The starting vertex in our search
        dest : Vertex
            The destination vertex in our search

        Returns
        -------
        list
            A list of the vertices to traverse to follow the shortest path from source to dest
        """

        # If either the source or the destination vertices are not in the graph, just return
        if not graph.contains_vertex(source) or not graph.contains_vertex(dest):
            return

        # Reset all of the sets and maps to empty
        self.__reset()

        # Set of all unvisited nodes
        self.unvisited = set(v.id for v in graph.vertices)

        # The distances of each node from the source node, all are initialized the infinity
        # except the distance from the source node to itself, which is zero
        for v in graph.vertices:
            self.distances.update({v.id: np.inf})
            self.prev.update({v.id: None})
        self.distances.update({source.id: 0})

        while len(self.unvisited) != 0:
            # The current vertex: the unvisited vertex with the shortest distance
            current = self.__min_distance()
            current_v = graph.find_vertex(current)

            # Remove the current vertex from the set of unvisited vertices
            self.visited.add(current)
            self.unvisited.remove(current)

            if current == dest.id:
                break

            # Update all the distances from the source to the unvisited neighbors of current_v
            self.__update_distances(current_v)

        # Lastly, we find the exact path of vertices to follow and return it
        path = []
        current = dest.id
        if self.prev[current] is not None or current == source.id:
            while current is not None:
                path.append(current)
                current = self.prev[current]

        path.reverse()
        return path

    def __min_distance(self):
        """Returns the unvisited vertex with the smallest current distance from the source vertex

        Returns
        -------
        int
            The id number of the vertex with the current smallest distance from the start
        """

        # Set the initial minimum distance to infinity
        min_dist = np.inf

        # Set the initial closest unvisited vertex to None
        closest = None

        for u in self.unvisited:
            if self.distances[u] < min_dist:
                min_dist = self.distances[u]
                closest = u

        return closest

    def __update_distances(self, current):
        """Updates the distances to all unvisited vertices adjacent to the current one

        Parameters
        ----------
        current : int
            The id number of the vertex currently being searched from
        """

        # If there are no unvisited vertices left, then we just return
        if len(self.unvisited) == 0:
            return

        # Otherwise, go through all of the unvisited adjacent vertices and update their distances
        for adj in current.weights.keys():
            if adj in self.unvisited:
                if self.distances[current.id] + current.weights[adj] < self.distances[adj]:
                    self.distances[adj] = self.distances[current.id] + current.weights[adj]
                    self.prev.update({adj: current.id})






















