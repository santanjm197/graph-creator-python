#--------------------------------------------------------------------#
# Author: Joseph Santantasio       				     			     #
# Project: Graph Creator         				                     #
# Class: Vertex					   		                             #
# Created On: 9/1/2018             				                     #
#--------------------------------------------------------------------#


class Vertex():
    """A class for a vertex in a graph, keeps track of its value,
        x and y coordinates and adjacent vertices"""

    def __init__(self, value=0, x=0, y=0, id=0):
        """Constructs a new Vertex with a value and coordinates

        Attributes
        ----------
        value : int
            The integer value held by the vertex (default 0)
        x : int
            The x-coordinate of this vertex on the screen (default 0)
        y : int
            The y-coordinate of this vertex on the screen (default 0)
        id : int
            The unique identifier of this vertex
        adjacent : list
            A list containing every vertex that is adjacent to this vertex
        weights : dict
            A dictionary mapping the id's of adjacent vertices to the weight of the edge

        Methods
        -------
        add_adjacent(vertex)
            Creates an edge between this vertex and another
        delete_adjacent(vertex)
            Deletes the edge between this vertex and another (if there is one)
        is_adjacent(vertex)
            Checks whether or not this vertex is adjacent to another
        give()
            Adds one to the value of every adjacent vertex and subtracts from this vertex
        take()
            Subtracts one from every adjacent vertex and adds the total to this vertex
        get_coordinates()
            Gets the x and y coordinates of this vertex
        get_adjacent()
            Gets the list of vertices currently adjacent to this vertex
        get_adjacent_ids()
            Gets a list of the id numbers of the vertices currently adjacent to this vertex
        get_value()
            Gets the current value of this vertex
        """

        # The value first held by this Vertex
        self.value = value

        # The x and y coordinates of this Vertex, used solely for graphical purposes
        self.x = x
        self.y = y

        # The unique integer id number of this Vertex, same as the oval which
        # represents it in the canvas
        self.id = id

        # The list of this Vertex's adjacent vertices (those it is connected to via an edge)
        self.adjacent = []

        # Dictionary of the ids of the vertices adjacent to this vertex to the weight of their edge
        self.weights = {}

    def __repr__(self):
        """Returns a representation of this Vertex"""
        s = f'Coordinates: ({self.x}, {self.y})\nValue: {self.value}\n'

        for k in self.weights.keys():
            s = s + f'Adjacent: {str(k)} - {self.weights[k]}\n'

        return s

    def __eq__(self, other):
        """Returns True if other is a Vertex with the same id number as self and False otherwise"""
        if isinstance(other, Vertex):
            return self.id == other.id
        return False

    def add_adjacent(self, vertex, weight=0):
        """Adds a new Vertex adjacent to this Vertex, essentially creating an edge

        Parameters
        ----------
        vertex : Vertex
            A Vertex instance with a different id number
        weight : int, optional
            The weight of the new edge

        Returns
        -------
        bool
            True if a new edge was successfully created and False otherwise
        """

        # If the given vertex has the same id number as this vertex, or has the same
        # id as an already adjacent vertex, do not create the edge
        if self == vertex or vertex.id in self.weights.keys():
            return False

        # First add the new vertex to the list of adjacent vertices and map its id to the weight
        self.adjacent.append(vertex)
        self.weights.update({vertex.id: weight})

        # Now do the same for the other vertex
        vertex.adjacent.append(self)
        vertex.weights.update({self.id: weight})
        return True

    def delete_adjacent(self, vertex):
        """Removes the vertex from the list of this vertex's neighbors: deletes an edge

        Parameters
        ----------
        vertex : Vertex
            A Vertex instance that may or may not be adjacent to this Vertex

        Returns
        -------
        bool
            True if the edge was successfully removed and False otherwise
        """
        if self.is_adjacent(vertex):
            # Now remove the vertex from the weights dictionary and the list of adjacent vertices
            del self.weights[vertex.id]
            self.adjacent.remove(vertex)

            # Do the same for the removed vertex
            del vertex.weights[self.id]
            vertex.adjacent.remove(self)
            return True
        return False

    def is_adjacent(self, vertex):
        """Returns True if given Vertex v is adjacent to this Vertex, False otherwise

        Parameters
        ----------
        vertex : Vertex/int
            A Vertex instance or the id number of a Vertex

        Returns
        -------
        bool
            True if the given vertex is adjacent to this vertex and False if not
        """
        if isinstance(vertex, Vertex):
            return vertex in self.adjacent

        if isinstance(vertex, int):
            return vertex in self.weights.keys()

    def give(self):
        """Gives a dollar to each of this Vertex's neighboring Vertices"""
        for i in range(len(self.adjacent)):
            self.value = self.value - 1
            self.adjacent[i].value = self.adjacent[i].value + 1

    def take(self):
        """Takes a dollar from each of this Vertex's neighboring Vertices"""
        for i in range(len(self.adjacent)):
            self.value = self.value + 1
            self.adjacent[i].value = self.adjacent[i].value - 1

    def get_coordinates(self):
        """Returns a tuple of this Vertex's x and y coordinates

        Returns
        -------
        tuple
            A two-tuple containing the x and y coordinates of this vertex
        """
        return self.x, self.y

    def get_id(self):
        """Returns the id number of this Vertex

        Returns
        -------
        int
            The id number of this vertex
        """
        return self.id

    def get_adjacent_vertices(self):
        """Returns the list of the vertices adjacent to self

        Returns
        -------
        list
            List of the vertices currently adjacent to this vertex
        """
        return self.adjacent

    def get_adjacent_ids(self):
        """Returns the list of ids of this Vertex's adjacent vertices

        Returns
        -------
        list
            List of the id numbers of the vertices adjacent to this vertex
        """
        return self.weights.keys()

    def get_value(self):
        """Returns the value of this vertex

        Returns
        -------
        int
            This vertex's current value
        """
        return self.value

    def weight(self, vertex):
        """Gets the weight of the edge between this vertex and the given one (if there is an edge)

        Parameters
        ----------
        vertex : Vertex/int
            Either a Vertex instance or the id number of a Vertex

        Returns
        -------
        int
            The weight of the edge between the vertices or None if there is no edge
        """

        # If the given vertex is not adjacent at all, then return None
        if not self.is_adjacent(vertex):
            return None

        # If the given argument was a Vertex instance, set it to its id number
        # NOTE: At this point we have a guarantee that the passed vertex IS adjacent,
        # thus is must follow that vertex.id is a key in the self.weights dictionary
        if isinstance(vertex, Vertex):
            vertex = vertex.id

        return self.weights[vertex]













