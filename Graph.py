#--------------------------------------------------------------------#
# Author: Joseph Santantasio       				     			     #
# Project: Graph Creator         				                     #
# Class: Graph					   		                             #
# Created On: 9/1/2018             				                     #
#--------------------------------------------------------------------#


from Vertex import Vertex
from tkinter import *
import numpy as np


class Graph:
    """
    Class which represents a mathematical graph object

    Attributes
    ----------
    vertices : list
        a list of the vertices which make up the graph
    weights : dict
        a dictionary which maps lists of adjacent vertices to the weight of the edge between them

    Methods
    -------
    add_vertices(*args)
        Adds a collection of vertices to the graph all at once
    remove_vertex(vertex)
        Removes an existing vertex from the graph
    create_edge(vertex1, vertex2, weight=0)
        Adds a new edge to the graph with a given weight between two vertices
    remove_edge(vertex1, vertex2)
        If an edge exists between the given vertices in the graph, it is removed
    get_weight(vertex1, vertex2)
        Returns the weight of the edge (if there is one) between two vertices
    are_adjacent(vertex1, vertex2)
        Returns True if the given vertices are adjacent in the graph and False otherwise
    find_vertex(id)
        Returns the vertex in the graph with the given id number
    contains_vertex(vertex)
        Returns True if the graph contains the vertex and False if not
    get_coordinates(vertex)
        Returns an ordered pair of the coordinates of a vertex in the graph
    """

    def __init__(self):
        # The list of vertices which make up this graph
        self.vertices = []

        # Dictionary mapping a tuple of vertex id's to the weight of the edge
        # between the vertices with the corresponding id's
        self.weights = {}

    def __repr__(self):
        rep = ""
        for i in range(len(self.vertices)):
            rep = rep + 'Vertex ' + str(self.vertices[i].id) + ': (' + str(self.vertices[i].x) \
                  + ', ' + str(self.vertices[i].y) + ')\n'
        for k in self.weights.keys():
            rep = rep + 'Edge (' + str(k[0]) + ' - ' + str(k[1]) + ') weight = ' \
                  + str(self.weights[k]) + '\n'
        return rep

    def add_vertices(self, *args):
        """Adds a number of new vertices to this graph

        Parameters
        ----------
        *args : Vertex
            Any number of Vertex objects

        Returns
        -------
        bool
            True if the vertices were successfully added to the graph

        Raises
        ------
        TypeError
            If any of the supplied arguments is not a Vertex instance
        RuntimeError
            If one of the vertices has the same id number as a vertex already in the graph
        """

        # We must ensure that every argument given is a Vertex
        for i in range(len(args)):
            if not isinstance(args[i], Vertex):
                raise TypeError(f'{args[i]} is not a Vertex object, it is type {type(args[i])}')
            else:
                for vertex in self.vertices:
                    # We do not allow multiple vertices with the same id number
                    if vertex.id == args[i].id:
                        raise RuntimeError(f'A vertex already exists in the graph with the id: {args[i].id}')

        self.vertices.extend(args)
        return True

    def remove_vertex(self, vertex):
        """Removes an existing vertex from this graph if it is in the graph

        Parameters
        ----------
        vertex : Vertex/int
            Either a Vertex instance or the id of a Vertex instance

        Returns
        -------
        bool
            True if the vertex was removed successfully and False if it was not in the graph
        """

        # First we make sure that the vertex we are trying to remove is in the graph
        if not self.contains_vertex(vertex):
            return False

        # If vertex was given as an integer id number, then we must find the vertex in
        # this graph that has that id number
        if isinstance(vertex, int):
            vertex = self.find_vertex(vertex)

        for v in self.vertices:
            if v is vertex:
                # Before removing the vertex from the graph, the first thing we do
                # is make sure that every vertex it was adjacent to deletes it
                for i in range(len(self.vertices)):
                    self.vertices[i].delete_adjacent(v)
                self.vertices.remove(v)
                return True
        return False

    def create_edge(self, vertex1, vertex2, weight=0):
        """Creates an edge between 2 vertices in the graph with the supplied weight

        Parameters
        ----------
        vertex1 : Vertex/int
            Either a Vertex instance or the id number of a Vertex
        vertex2 : Vertex/int
            Either a Vertex instance or the id number of a Vertex
        weight : int, optional
            The weight of the edge to create, default value is 0

        Returns
        -------
        bool
            True if the edge was successfully created and False if it was not
        """

        # First we check whether or not the vertices are even in the graph to begin with
        if not self.contains_vertex(vertex1) or not self.contains_vertex(vertex2):
            return False

        # NOTE: At this point we KNOW that both vertex1 AND vertex2 are in the graph
        if isinstance(vertex1, int):
            vertex1 = self.find_vertex(vertex1)

        if isinstance(vertex2, int):
            vertex2 = self.find_vertex(vertex2)

        vertex1.add_adjacent(vertex2, weight)
        self.weights.update({(vertex1.id, vertex2.id): weight})
        return True

    def remove_edge(self, vertex1, vertex2):
        """Deletes the edge between two vertices in the graph

        Parameters
        ----------
        vertex1 : Vertex/int
            Either a Vertex instance or the id number of a Vertex
        vertex2 : Vertex/int
            Either a Vertex instance or the id number of a Vertex

        Returns
        -------
        bool
            True if the edge was successfully removed and False if it was not
        """

        if not self.contains_vertex(vertex1) or not self.contains_vertex(vertex2):
            return False

        if isinstance(vertex1, int):
            vertex1 = self.find_vertex(vertex1)

        if isinstance(vertex2, int):
            vertex2 = self.find_vertex(vertex2)

        if not self.are_adjacent(vertex1, vertex2):
            return False

        vertex1.delete_adjacent(vertex2)
        for k in self.weights.keys():
            if vertex1.id in k and vertex2.id in k:
                del self.weights[k]
                return True

    def get_weight(self, vertex1, vertex2):
        """Returns the weight of the edge between two vertices in the graph if they are adjacent

        Parameters
        ----------
        vertex1 : Vertex/int
            Either a Vertex instance or the id number of a Vertex
        vertex2 : Vertex/int
            Either a Vertex instance or the id number of a Vertex

        Returns
        -------
        int
            The weight of the edge between the given vertices in the graph

        Raises
        ------
        RuntimeError
            If one or both of the given vertices are not in the graph
        KeyError
            If the given vertices are not adjacent in the graph
        """

        if not self.contains_vertex(vertex1) or not self.contains_vertex(vertex2):
            raise RuntimeError(f'Both vertices must be present in the graph')

        if isinstance(vertex1, int):
            vertex1 = self.find_vertex(vertex1)

        if isinstance(vertex2, int):
            vertex2 = self.find_vertex(vertex2)

        if self.are_adjacent(vertex1, vertex2):
            for k in self.weights.keys():
                if vertex1.id in k and vertex2.id in k:
                    return self.weights[k]
        else:
            raise KeyError("The vertices given are not adjacent")

    def are_adjacent(self, vertex1, vertex2):
        """Return True if the two vertices are adjacent and False otherwise

        Parameters
        ----------
        vertex1 : Vertex/int
            Either a Vertex instance or the id number of a Vertex
        vertex2 : Vertex/int
            Either a Vertex instance or the id number of a Vertex

        Returns
        -------
        bool
            True if the given vertices are adjacent in the graph and false if they are not
        """

        if not self.contains_vertex(vertex1) or not self.contains_vertex(vertex2):
            return False

        if isinstance(vertex1, int):
            vertex1 = self.find_vertex(vertex1)

        if isinstance(vertex2, int):
            vertex2 = self.find_vertex(vertex2)

        return vertex1.is_adjacent(vertex2)

    def find_vertex(self, id):
        """Returns the Vertex in this Graph with the requested id, and None if it doesn't exist

        Parameters
        ----------
        id : int
            The id number of a vertex which may or may not be in the graph

        Returns
        -------
        Vertex
            The Vertex in the graph with the given id number, or None if there is not one
        """
        vertex = None
        for i in range(0, len(self.vertices)):
            if self.vertices[i].id == id:
                vertex = self.vertices[i]

        return vertex

    def contains_vertex(self, vertex):
        """Function that returns whether or not a given Vertex is in this graph

        Parameters
        ----------
        vertex : Vertex/id
            Either a Vertex instance or the id number of a Vertex

        Returns
        -------
        bool
            True if this graph contains the vertex or False if it does not
        """

        # If the argument was given as a Vertex, then check if it is in the list of vertices
        if isinstance(vertex, Vertex):
            return vertex in self.vertices

        # If instead the argument was given as an int, check to see if there is a vertex
        # in the graph that has that id number
        if isinstance(vertex, int):
            for v in self.vertices:
                if v.id == vertex:
                    return True
            return False

    def get_coordinates(self, vertex):
        """Returns a 2-tuple of the coordinates of a vertex

        Parameters
        ----------
        vertex : Vertex/int
            Either a Vertex instance or the id number of a Vertex

        Returns
        -------
        tuple
            A 2-tuple containing the x and y coordinates of the given vertex

        Raises
        ------
        RuntimeError
            If the given vertex is not in this graph
        """
        if not self.contains_vertex(vertex):
            raise RuntimeError(f'The vertex given: {vertex} is not in the graph')

        if isinstance(vertex, int):
            vertex = self.find_vertex(vertex)

        return vertex.get_coordinates()

    def find_min_degree(self):
        """Calculates and returns the minimum degree of the graph

        Returns
        -------
        int
            The minimum degree of all vertices in the graph
        """

        # The minimum degree of the graph
        min_degree = np.inf

        for vertex in self.vertices:
            if len(vertex.get_adjacent_vertices()) < min_degree:
                min_degree = len(vertex.get_adjacent_vertices())

        return min_degree

    def find_max_degree(self):
        """Calculates and returns the maximum degree of the graph

        Returns
        -------
        int
            The maximum degree of all vertices in the graph
        """

        # The maximum degree of the graph
        max_degree = 0

        for vertex in self.vertices:
            if len(vertex.get_adjacent_vertices()) > max_degree:
                max_degree = len(vertex.get_adjacent_vertices())

        return max_degree




























