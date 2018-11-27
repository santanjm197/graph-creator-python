#--------------------------------------------------------------------#
# Author: Joseph Santantasio       				     			     #
# Project: Graph Creator         				                     #
# Class: Graph_GUI					   		                         #
# Created On: 9/4/2018             				                     #
#--------------------------------------------------------------------#

from time import sleep, time
from Vertex import Vertex
from Graph import Graph
from ShortestPathCalculator import ShortestPathCalculator
from tkinter import *
import tkinter as tk
import math

class Graph_GUI(Frame):
    """Class which will display the graph gui

    Attributes
    ----------
    graph_canvas : Canvas
        The canvas in the window that displays the graph
    options_canvas : Canvas
        The canvas in the window that holds the buttons
    info_canvas : Canvas
        The canvas in the window that displays information about the graph
    basic_info_txt : Text
        Text widget that displays up-to-date info about the basics of the graph
    new_vertex_button : Button
        Button that when clicked allows the user to create new vertices in the graph
    del_vertex_button : Button
        Button that when clicked allows the user to delete vertices from the graph
    new_edge_button : Button
        Button that when clicked allows the user to create new edges in the graph
    del_edge_button : button
        Button that when clicked allows the user to delete edges from the graph
    gt_button : Button
        Button that when clicked allows the user to give and take in the graph
    sp_button : Button
        Button that when clicked allows the user to calculate a shortest path in the graph
    cancel_button : Button
        Button that when clicked cancels the currently active command
    value_prompt_window : TopLevel
        Window in which the user is prompted to enter a value for a new vertex
    value_entry : Entry
        The text entry box in which the user enters the value of a new vertex
    entered_value : int
        The value entered by the user when creating a new vertex
    weight_prompt_window : TopLevel
        Window in which the user is prompted to enter a weight for a new edge
    weight_entry : Entry
        The text entry box in which the user enters the weight of a new edge
    entered_weight : int
        The weight entered by the user when creating a new edge
    context_text : Text
        Text that displays instructions to the user about the currently active command
    graph : Graph
        The underlying graph object being manipulated
    ovals : list
        A list of the ids of the ovals in the graph canvas that correspond to a vertex
    lines : dict
        A map taking the id of each line (edge) in the graph canvas to info about it
    sel_vertex_ids : list
        A list of the ids of the currently selected vertices (ovals)
    cancel_commands : dict
        A map taking each two-letter command to the cancel function for that command
    active_command : str
        A two-letter string representing the currently active command
    hv_funcid : str
        The id of the hover vertex command
    draw_funcid : str
        The id of the draw vertex command
    dv_funcid : str
        The id of the delete vertex command
    sv_funcid : str
        The id of the select vertex command
    g_funcid : str
        The id of the give command
    t_funcid : str
        The id of the take command

    Methods
    -------
    draw_vertex(event)
        Draw a vertex at the coordinates of the event
    draw_edge()
        Draw an edge between the two currently selected vertices
    give(event)
        The selected vertex gives one to each of its neighbors
    take(event)
        The selected vertex takes one from each of its neighbors
    shortest_path()
        Calculate the shortest path between the two currently selected vertices using Dijkstra's algorithm
    cancel()
        Cancel the currently active command
    """

    def __init__(self, master=None):
        Frame.__init__(self, master)

        # The canvas which will display the actual graph
        self.graph_canvas = Canvas(self, bg='#908b8b', height=800, width=1000)
        self.graph_canvas.grid(row=0, column=0)

        # The canvas which will contain the buttons
        self.options_canvas = Canvas(self, bg='blue', height=800, width=300)
        self.options_canvas.grid(row=0, column=1)

        # The canvas which will contain the text information about the current graph
        self.info_canvas = Canvas(self, bg='black', height=175, width=1300)
        self.info_canvas.grid(row=1, column=0, columnspan=2)

        # The window for the value prompt when creating a new Vertex in the graph
        self.value_prompt_window = None

        # The window for the edge weight prompt when creating a new edge in the graph
        self.weight_prompt_window = None

        # Create the various text widgets in the info canvas
        self.__create_info_texts()

        # Create the various buttons
        self.__create_buttons()

        # Context-sensitive text which will be displayed when a button is pressed
        self.context_text = None

        # Creates a new Graph object which will hold the information about the vertices and whatnot
        self.graph = Graph()

        # A list of the ovals in the graph canvas: used in part to ensure vertices do not overlap
        self.ovals = []

        # A dictionary of the ids of the lines (edges) in the graph mapped to the ids of
        # the weight text of the line
        self.lines = {}

        # A list of the currently selected Vertices
        self.sel_vertex_ids = []

        # Dictionary mapping command strings to their respective cancellation functions
        #   nv - new vertex
        #   dv - delete vertex
        #   ne - new edge
        #   de - delete edge
        #   gt - give/take
        #   sp - shortest path
        self.cancel_commands = {'nv': self.__cancel_nv,
                                'dv': self.__cancel_dv,
                                'ne': self.__cancel_sv,
                                'de': self.__cancel_sv,
                                'gt': self.__cancel_gt,
                                'sp': self.__cancel_sp}
        self.active_command = None

        self.grid()

    def __create_info_texts(self):
        """Creates the various text widgets for displaying info about the graph"""

        # The following information is shown about the graph in this widget:
        # n(G)     - number of vertices
        # e(G)     - number of edges
        # delta(G) - minimum degree
        # DELTA(G) - maximum degree
        starting_info = 'Vertices: 0\n' + \
                        'Edges: 0\n' + \
                        'Min Degree: 0\n' + \
                        'Max Degree: 0'

        self.basic_info_txt = self.info_canvas.create_text(72, 40, text=starting_info, fill='white',
                                                           font=('Courier', 12, 'bold'))

        # The following information is shown about the vertex being hovered over in this widget:
        # tk_id - the id number of the vertex that tkinter uses to identify it
        # value - the current value of the vertex
        # d(v)  - the degree of the vertex
        # (x,y) - the coordinates of the vertex on the canvas
        self.hover_info_txt = self.info_canvas.create_text(300, 40, text='', fill='white',
                                                           font=('Courier', 12, 'bold'))

    def __create_buttons(self):
        """Creates the various buttons for the options canvas"""

        # New Vertex Button
        self.__create_new_vertex_button()

        # Delete Vertex Button
        self.__create_delete_vertex_button()

        # New Edge Button
        self.__create_new_edge_button()

        # Delete Edge Button
        self.__create_delete_edge_button()

        # Give/Take Button
        self.__create_gt_button()

        # Shortest Path Button
        self.__create_shortest_path_button()

        # Cancel Button
        self.__create_cancel_button()

        # Create the hover vertex event
        self.__set_hover_vertex()

    def __activate_all(self):
        """Activates all buttons that should be active based on the current state of the graph"""
        # Activate the new vertex button
        self.new_vertex_button.config(state=tk.ACTIVE)

        # If at least 1 vertex exists, activate the delete vertex button
        if len(self.ovals) >= 1:
            self.del_vertex_button.config(state=tk.ACTIVE)

        # If at least 2 vertices exist, activate the new edge button
        if len(self.ovals) >= 2:
            self.new_edge_button.config(state=tk.ACTIVE)

        # If at least 1 edge exists, activate the delete edge, give/take and shortest path buttons
        if len(self.lines.keys()) >= 1:
            self.del_edge_button.config(state=tk.ACTIVE)
            self.gt_button.config(state=tk.ACTIVE)
            self.sp_button.config(state=tk.ACTIVE)

    def __deactivate_all(self):
        """Deactivates all but the cancel button"""
        self.new_vertex_button.config(state=tk.DISABLED)
        self.del_vertex_button.config(state=tk.DISABLED)
        self.new_edge_button.config(state=tk.DISABLED)
        self.del_edge_button.config(state=tk.DISABLED)
        self.gt_button.config(state=tk.DISABLED)
        self.sp_button.config(state=tk.DISABLED)

    # -------------------------------- #
    #                                  #
    #        Vertex Hover Event        #
    #                                  #
    # -------------------------------- #

    def __set_hover_vertex(self):
        """Sets up the ability to hover over a Vertex and highlight it and its edges"""
        self.hv_funcid = self.graph_canvas.bind('<Motion>', self.__hover_vertex)

    def __hover_vertex(self, event):
        """Highlights a Vertex and all of its connected edges when the mouse hovers over it

        Parameters
        ----------
        event : Event
            The event that is triggered when the mouse hovers over a vertex (oval)
        """

        # The objects that overlap with the current mouse position
        overlaps = self.graph_canvas.find_overlapping(event.x-3, event.y-3,
                                                      event.x+3, event.y+3)

        # The vertex being hovered over
        vertex_id = None

        for i in range(len(overlaps)):
            if self.graph_canvas.type(overlaps[i]) == 'oval':
                vertex_id = overlaps[i]

        if vertex_id:
            # Change the color of the vertex to red if it is not currently selected
            if vertex_id not in self.sel_vertex_ids:
                self.graph_canvas.itemconfigure(vertex_id, fill='red')

            # The coordinates of the vertex being hovered over
            x, y = self.graph.get_coordinates(vertex_id)

            # Get a list of all overlapping objects
            overlaps = self.graph_canvas.find_overlapping(x-3, y-3,
                                                          x+3, y+3)

            # Change the edges connected to this vertex and its weight text to red
            for i in range(len(overlaps)):
                if self.graph_canvas.type(overlaps[i]) == 'line':
                    self.graph_canvas.itemconfigure(overlaps[i], fill='red')
                    self.graph_canvas.itemconfigure(self.lines[overlaps[i]][1], fill='red')

            # Display the vertex information in the info canvas
            self.__display_hover_info(vertex_id)
        else:
            self.__reset_colors()
            self.info_canvas.itemconfigure(self.hover_info_txt, text='')

    # -------------------------------- #
    #                                  #
    #  New Vertex Button Construction  #
    #                                  #
    # -------------------------------- #

    def __create_new_vertex_button(self):
        """Creates the New Vertex Button"""

        # Create the window in the options canvas to contain the New Vertex button
        self.nv_id = self.options_canvas.create_window(150, 100)

        # Construct the New Vertex button
        self.new_vertex_button = Button(self.options_canvas, text="New Vertex",
                                        command=self.__set_draw_vertex, height=2, width=100)

        # Add the New Vertex button to the nv_id window
        self.options_canvas.itemconfigure(self.nv_id, window=self.new_vertex_button)

    def __set_draw_vertex(self):
        """Command for the new vertex button"""

        # Set the active command to new vertex
        self.active_command = 'nv'

        # Disable all buttons except for the cancel button
        self.__deactivate_all()

        # The tutorial text for the command
        help_txt = 'Click anywhere on the graph canvas to add a new vertex to the graph\n' + \
                   'Click Cancel to return'

        # Create the instructional text
        self.context_text = self.graph_canvas.create_text(450, 20, text=help_txt, fill='black',
                                                          font=("Courier", 12), justify=tk.CENTER)
        sleep(0.2)

        # Bind the draw vertex event to the left mouse button
        self.draw_funcid = self.graph_canvas.bind('<Button-1>', self.draw_vertex)

    # --------------------------------- #
    #                                   #
    # Delete Vertex Button Construction #
    #                                   #
    # --------------------------------- #

    def __create_delete_vertex_button(self):
        """Creates the delete vertex button"""

        # Create the window in the options canvas to contain the Delete Vertex button
        self.dv_id = self.options_canvas.create_window(150, 200)

        # Create the delete vertex button
        self.del_vertex_button = Button(self.options_canvas, text="Delete Vertex",
                                        command=self.__set_delete_vertex, height=2, width=100,
                                        state=tk.DISABLED)

        # Add the delete vertex button to the window
        self.options_canvas.itemconfigure(self.dv_id, window=self.del_vertex_button)

    def __set_delete_vertex(self):
        """Command for the delete vertex button"""

        # Set the active command to delete vertex
        self.active_command = 'dv'

        # Deactivate all buttons except for cancel
        self.__deactivate_all()

        # The tutorial text for the command
        help_txt = 'Left click on a vertex to remove it from the graph\n' + \
                   'Click Cancel to return'

        # Create the instructional text
        self.context_text = self.graph_canvas.create_text(450, 20, text=help_txt, fill='black',
                                                          font=("Courier", 12), justify=tk.CENTER)
        sleep(0.2)

        # Bind the delete vertex event to the left mouse button
        self.dv_funcid = self.graph_canvas.tag_bind('vertex', '<Button-1>', self.__delete_vertex)

    # -------------------------------- #
    #                                  #
    #   New Edge Button Construction   #
    #                                  #
    # -------------------------------- #

    def __create_new_edge_button(self):
        """Creates the New Edge Button"""

        # Create the window in the options canvas to contain the create edge button
        self.ne_id = self.options_canvas.create_window(150, 300)

        # Create the create edge button
        self.new_edge_button = Button(self.options_canvas, text='New Edge',
                                      command=self.__set_select_vertex, state=tk.DISABLED,
                                      height=2, width=100)

        # Add the create edge button to the window
        self.options_canvas.itemconfigure(self.ne_id, window=self.new_edge_button)

    def __set_select_vertex(self):
        """Command for selecting a vertex"""

        # Set the active command to new edge
        self.active_command = 'ne'

        # Disable all buttons except for the cancel button
        self.__deactivate_all()

        # The tutorial text for the command
        help_txt = 'Click on two different non-adjacent vertices to create an edge between them\n' + \
                   'Click Cancel to return'

        # Create the instructional text
        self.context_text = self.graph_canvas.create_text(450, 20, text=help_txt, fill='black',
                                                          font=("Courier", 12), justify=tk.CENTER)
        sleep(0.2)

        # Bind the select vertex event to all vertices via the left mouse button
        self.sv_funcid = self.graph_canvas.tag_bind('vertex', '<Button-1>', self.select_vertex)

    # -------------------------------- #
    #                                  #
    #  Delete Edge Button Construction #
    #                                  #
    # -------------------------------- #

    def __create_delete_edge_button(self):
        """Creates the Delete Edge Button"""

        # Create the window in the options canvas to contain the delete edge button
        self.de_id = self.options_canvas.create_window(150, 400)

        # Create the delete edge button
        self.del_edge_button = Button(self.options_canvas, text='Delete Edge',
                                      command=self.__set_select_delete, state=tk.DISABLED,
                                      height=2, width=100, )

        # Add the delete edge button to the window
        self.options_canvas.itemconfigure(self.de_id, window=self.del_edge_button)

    def __set_select_delete(self):
        """Command for selecting vertices to delete the edge between them"""

        # Set the active command to delete edge
        self.active_command = 'de'

        # Disable all buttons except for the cancel button
        self.__deactivate_all()

        # The tutorial text for the command
        help_txt = 'Select two adjacent vertices to delete the edge between them\n' + \
                   'Click Cancel to return'

        # Create the instructional text
        self.context_text = self.graph_canvas.create_text(450, 20, text=help_txt, fill='black',
                                                          font=("Courier", 12), justify=tk.CENTER)
        sleep(0.2)

        # Bind the select vertex event to all vertices via the left mouse button
        self.sv_funcid = self.graph_canvas.tag_bind('vertex', '<Button-1>', self.select_vertex)

    # -------------------------------- #
    #                                  #
    #   Give/Take Button Construction  #
    #                                  #
    # -------------------------------- #

    def __create_gt_button(self):
        """Creates the Give/Take Button"""

        # Create the window in the options canvas to contain the give/take button
        self.gt_id = self.options_canvas.create_window(150, 500)

        # Create the give/take button
        self.gt_button = Button(self.options_canvas, text='Give/Take',
                                command=self.__set_gt, height=2, width=100, state=tk.DISABLED)

        # Add the give/take button to the window
        self.options_canvas.itemconfigure(self.gt_id, window=self.gt_button)

    def __set_gt(self):
        """Sets up the give and take events"""

        # Set the active command to give/take
        self.active_command = 'gt'

        # Disable all buttons except for the cancel button
        self.__deactivate_all()

        # The tutorial text for the command
        help_txt = 'Left click on a vertex give to each of its adjacent vertices, ' + \
                   'right click to take from its adjacent vertices\n' + \
                   'Click Cancel to return'

        # Create the instructional text
        self.context_text = self.graph_canvas.create_text(450, 20, text=help_txt, fill='black',
                                                          font=("Courier", 10), justify=tk.CENTER)
        sleep(0.2)

        # Bind the give and take events to the left and right mouse buttons respectively
        self.g_funcid = self.graph_canvas.tag_bind('vertex', '<Button-1>', self.give)
        self.t_funcid = self.graph_canvas.tag_bind('vertex', '<Button-3>', self.take)

    # --------------------------------- #
    #                                   #
    # Shortest Path Button Construction #
    #                                   #
    # --------------------------------- #

    def __create_shortest_path_button(self):
        """Creates the shortest path button"""

        # Create the window in the options canvas to contain the shortest path button
        self.sp_id = self.options_canvas.create_window(150, 600)

        # Create the shortest path button
        self.sp_button = Button(self.options_canvas, text='Shortest Path',
                                command=self.__set_select_sp, height=2, width=100, state=tk.DISABLED)

        # Add the give/take button to the window
        self.options_canvas.itemconfigure(self.sp_id, window=self.sp_button)

    def __set_select_sp(self):
        """Command for selecting two vertices to calculate the shortest path between them"""

        # If the active command is ALREADY shortest path, then we can safely delete the context text
        # before we re-create it to avoid stacking multiple copies of it
        if self.active_command == 'sp':
            self.graph_canvas.delete(self.context_text)

        # Set the active command to shortest path
        self.active_command = 'sp'

        # Disable all buttons except for the cancel button
        self.__deactivate_all()

        # The tutorial text for the command
        help_txt = 'Select two vertices to calculate the shortest path between them\n' + \
                   'Click Cancel to return'

        # Create the instructional text
        self.context_text = self.graph_canvas.create_text(450, 20, text=help_txt, fill='black',
                                                          font=("Courier", 12), justify=tk.CENTER)
        sleep(0.2)

        # Bind the select vertex event to all vertices via the left mouse button
        self.sv_funcid = self.graph_canvas.tag_bind('vertex', '<Button-1>', self.select_vertex)

        # Bind the hover vertex event to mouse motion (in case it was unbound previously)
        self.__set_hover_vertex()

        # Also we reset all of the colors of the graph back to their defaults
        self.__reset_colors()

    # -------------------------------- #
    #                                  #
    #   Cancel Button Construction     #
    #                                  #
    # -------------------------------- #

    def __create_cancel_button(self):
        """Creates the Cancel Button"""

        # Create the window in the options canvas to contain the cancel button
        self.cancel_id = self.options_canvas.create_window(150, 700)

        # Create the cancel button
        self.cancel_button = Button(self.options_canvas, text='Cancel',
                                    command=self.cancel, height=2, width=100)

        # Add the cancel button to the window
        self.options_canvas.itemconfigure(self.cancel_id, window=self.cancel_button)

    # -------------------------------- #
    #                                  #
    #          Draw Vertex             #
    #                                  #
    # -------------------------------- #

    def draw_vertex(self, event):
        """Draws a new Vertex on the graph canvas wherever the mouse is clicked

        Parameters
        ----------
        event : Event
            The event triggered when the user left-clicks on the graph canvas
        """

        # Radius of the circle
        r = 25

        # First ensure that the circle will not be drawn outside the canvas
        if event.x < 38 or event.x > 962 or event.y < 38 or event.y > 762:
            print("Too close to edge of canvas")
            return

        # Check to make sure that the selected location will be a certain distance from other ovals
        if len(self.graph_canvas.find_overlapping(event.x-r-25, event.y-r-25,
                                                  event.x+r+25, event.y+r+25)) != 0:
            print("Too close to another circle")
            return

        # Draws a green circle at the mouse's location
        self.ovals.append(self.graph_canvas.create_oval(event.x-r, event.y-r,
                            event.x+r, event.y+r, outline='black', width=2, fill='green',
                            tags='vertex'))

        # Prompt the user for a value for the Vertex
        self.__prompt_vertex_value()
        sleep(0.2)

        # Adds the circle as a new Vertex to the Graph
        # NOTE: If the user closes the value entry window using the close button,
        # then we must prevent an AttributeError by choosing a default vertex value
        try:
            self.graph.add_vertices(Vertex(self.entered_value, event.x, event.y, self.ovals[-1]))
        except AttributeError:
            self.graph.add_vertices(Vertex(0, event.x, event.y, self.ovals[-1]))

        # Displays the associated vertex's value at the circle's center
        self.graph_canvas.create_text(event.x, event.y-34, text=str(self.graph.vertices[-1].value),
                                      font=('Courier', 14, 'bold'), tags='vertexvalue')

        # Update the graph info text
        self.__update_graph_info()

    def __prompt_vertex_value(self):
        """"Method which creates a dialog box for the user to enter the value of a new Vertex,
            evaluates whether their entry was legal and then returns it
        """

        # Get the root window's location on the screen
        x = self.winfo_rootx() + 450
        y = self.winfo_rooty() + 300

        # Creates a text popup dialog asking the user to enter an integer value for the Vertex
        self.value_prompt_window = Toplevel(master=self, takefocus=True)
        self.value_prompt_window.geometry(newGeometry=f'300x100+{x}+{y}')

        # Have the value prompt window take focus and all interaction until it is destroyed
        self.value_prompt_window.wait_visibility()
        self.value_prompt_window.grab_set()
        self.value_prompt_window.focus_set()

        # Creates a canvas in the new window to house the widgets
        value_prompt_canvas = Canvas(self.value_prompt_window, height=100, width=300)
        value_prompt_canvas.grid(row=0, column=0)

        # Create a text entry widget in the toplevel window
        value_entry_window = value_prompt_canvas.create_window(150, 45)
        self.value_entry = Entry(value_prompt_canvas)
        value_prompt_canvas.itemconfigure(value_entry_window, window=self.value_entry)

        # Create the label for the entry prompt
        value_label_window = value_prompt_canvas.create_window(150, 20)
        value_label = Label(value_prompt_canvas, text='Please enter an integer value for the Vertex')
        value_prompt_canvas.itemconfigure(value_label_window, window=value_label)

        # Create the accept button for the entry prompt
        value_accept_window = value_prompt_canvas.create_window(150, 80)
        value_accept = Button(value_prompt_canvas, text='Accept', command=self.__get_value)
        value_prompt_canvas.itemconfigure(value_accept_window, window=value_accept)

        # Bind the enter key to the accept command as well
        self.value_prompt_window.bind('<Key-Return>', self.__get_value)

        # Make the entry take immediate focus so the user can enter a value immediately
        self.value_entry.focus()

        self.wait_window(window=self.value_prompt_window)

    def __get_value(self, event=None):
        """Command for the value prompt accept button

        Parameters
        ----------
        event : Event, optional
            The event triggered by either pressing <enter> or left clicking the accept button
        """
        try:
            self.entered_value = int(self.value_entry.get())
        except ValueError:
            print("Entered is not an integer, please enter an integer")
            self.value_entry.select_range(0, tk.END)
            return

        self.value_prompt_window.grab_release()
        self.value_prompt_window.destroy()

    # -------------------------------- #
    #                                  #
    #        Deleting Vertices         #
    #                                  #
    # -------------------------------- #

    def __delete_vertex(self, event):
        """Deletes the vertex that was clicked on by the user

        Parameters
        ----------
        event : Event
            The event triggered by left clicking a vertex (oval) in the graph canvas
        """

        # All objects which overlap with where the user clicked
        overlap = self.graph_canvas.find_overlapping(event.x - 3, event.y - 3,
                                                     event.x + 3, event.y + 3)

        # The selected vertex
        sel_vertex_id = None

        # Set the selected vertex to whichever of the overlapping objects is an oval
        for i in range(0, len(overlap)):
            if self.graph_canvas.type(overlap[i]) == 'oval':
                sel_vertex_id = overlap[i]

        # If none of the overlapping objects are somehow an oval, just return
        if not sel_vertex_id:
            return

        x, y = self.graph.get_coordinates(sel_vertex_id)

        # Get the list of all edges connected to the selected vertex
        connected_edges = self.__get_edges(sel_vertex_id)

        # Delete all of the lines from the screen
        for i in range(len(connected_edges)):
            self.graph_canvas.delete(self.lines[connected_edges[i]][0])
            self.graph_canvas.delete(self.lines[connected_edges[i]][1])
            self.graph_canvas.delete(connected_edges[i])

            # Before removing the edge (and its weight text) from the line dictionary,
            # we need to ensure that we remove the edge from the underlying graph
            v1_id, v2_id = self.lines[connected_edges[i]][2]
            self.graph.remove_edge(v1_id, v2_id)

            # Now we can completely delete the edge's entry from the dictionary
            del self.lines[connected_edges[i]]

        # Delete the oval and its value text from the screen
        self.graph_canvas.delete(sel_vertex_id)
        self.graph_canvas.delete(self.graph_canvas.find_closest(x, y-34))
        self.ovals.remove(sel_vertex_id)

        # Now delete the vertex from the underlying graph
        self.graph.remove_vertex(sel_vertex_id)

        # Update the graph info text
        self.__update_graph_info()

    # -------------------------------- #
    #                                  #
    #        Vertex Selection          #
    #                                  #
    # -------------------------------- #

    def select_vertex(self, event):
        """Lets the user select a Vertex by left clicking it

        Parameters
        ----------
        event : Event
            The event triggered by left clicking a vertex (oval) in the graph canvas
        """

        # All objects which overlap with where the user clicked
        overlap = self.graph_canvas.find_overlapping(event.x-3, event.y-3,
                                                     event.x+3, event.y+3)

        # The selected vertex
        sel_vertex_id = None

        # Set the selected vertex to whichever of the overlapping objects is an oval
        for i in range(len(overlap)):
            if self.graph_canvas.type(overlap[i]) == 'oval':
                sel_vertex_id = overlap[i]

        # If none of the overlapping objects are somehow an oval, just return
        if not sel_vertex_id:
            return

        # Make the selected vertex stay blue
        self.graph_canvas.itemconfigure(sel_vertex_id, fill='blue')

        # If the same Vertex is selected twice, cancel the choice
        if self.sel_vertex_ids and self.sel_vertex_ids[0] == sel_vertex_id:
            self.graph_canvas.itemconfigure(sel_vertex_id, fill='green')
            self.sel_vertex_ids = []
            return

        # Add this vertex to the list of currently selected vertices
        self.sel_vertex_ids.append(sel_vertex_id)

        # If we now have selected 2 vertices, we may draw an edge between them
        if len(self.sel_vertex_ids) == 2:
            if self.active_command == 'ne':
                self.draw_edge()
            elif self.active_command == 'de':
                self.__delete_edge()
            elif self.active_command == 'sp':
                self.shortest_path()
            self.sel_vertex_ids = []

    # -------------------------------- #
    #                                  #
    #          Edge Drawing            #
    #                                  #
    # -------------------------------- #

    def draw_edge(self):
        """Draws an edge between the two currently selected vertices"""

        # The ids of the selected vertices
        v1_id, v2_id = self.sel_vertex_ids

        # If the two selected vertices are already adjacent, just return
        if self.graph.are_adjacent(v1_id, v2_id):
            print("Already adjacent!")
            return

        # Get the x and y coordinates of both vertices
        x1, y1 = self.graph.get_coordinates(v1_id)
        x2, y2 = self.graph.get_coordinates(v2_id)

        # Draw the actual edge and place it below the vertices in the display list
        new_edge = self.graph_canvas.create_line(x1, y1, x2, y2, fill='blue', tag='edge', width=3)
        self.graph_canvas.tag_lower('edge', 'vertex')

        # Check to see if the new line intersects more than its ending vertices
        vertex_overlaps = self.__check_for_overlap(new_edge)
        if vertex_overlaps:
            print("This edge would intersect another vertex")
            self.graph_canvas.delete(new_edge)
            return

        # Prompt the user to enter a weight for their new edge
        self.__prompt_edge_weight()
        sleep(0.2)

        # Find the midpoint of the new line
        midx, midy = ((x1 + x2) / 2, (y1 + y2) / 2)

        # Make the two vertices adjacent in the Graph
        # NOTE: If the user closes the weight prompt window with the close button we need to catch
        # the possible AttributeError that can occur and give a default weight
        try:
            self.graph.create_edge(v1_id, v2_id, self.entered_weight)
            # Create text of the new edge's weight slightly off from the midpoint
            weight_text = self.graph_canvas.create_text(midx, midy, text=str(self.entered_weight),
                                                        font=('Courier', 14, 'bold'), tag='weight')
        except AttributeError:
            self.graph.create_edge(v1_id, v2_id, 0)
            # Create text of the new edge's weight slightly off from the midpoint
            weight_text = self.graph_canvas.create_text(midx, midy, text=str(0),
                                                        font=('Courier', 14, 'bold'), tag='weight')
        print("New edge created")

        # We will create a small opaque rectangle at the point where the text will be
        # displayed to cover up the line
        width = (len(self.graph_canvas.itemcget(weight_text, 'text'))*10)/2 + 3
        weight_box = self.graph_canvas.create_rectangle(midx-width, midy-10, midx+width, midy+9,
                                           outline='#908b8b', fill='#908b8b', tag='weightbox')
        self.graph_canvas.tag_lower('weightbox', 'weight')

        # Add the new edge with its weight to the dictionary of lines and weight texts
        self.lines.update({new_edge: [weight_box, weight_text, [v1_id, v2_id]]})

        # Update the graph info text
        self.__update_graph_info()

    def __check_for_overlap(self, new_edge):
        """Returns a list of the vertices which the edge will intersect, if the only
            vertices it intersects are its endpoints, the method will return False

        Parameters
        ----------
        new_edge : int
            The id of the new edge being created

        Returns
        -------
        list/bool
            Either a list of the ovals that the new edge will intersect or False
        """

        # The number of vertices this edge would overlap with as a straight line
        # if it is greater than 2 the line must be curved
        vertex_overlaps = []

        for i in range(len(self.ovals)):
            # The x and y coordinates of self.ovals[i]
            x, y = self.graph.get_coordinates(self.ovals[i])

            # Search for overlaps between the center of the circle and the line
            overlap = self.graph_canvas.find_overlapping(x-30, y-30, x+30, y+30)

            # Check to see if the new edge is in the overlap
            for j in range(0, len(overlap)):
                if overlap[j] == new_edge:
                    vertex_overlaps.append(self.ovals[i])

        # If the number of vertices overlapping with the line is more than 2, return True
        if len(vertex_overlaps) > 2:
            return vertex_overlaps
        return False

    def __prompt_edge_weight(self):
        """Creates window which prompts the user to enter a weight for the edge they are creating"""

        # Get the root window's location on the screen
        x = self.winfo_rootx() + 450
        y = self.winfo_rooty() + 300

        # Creates a text popup dialog asking the user to enter an integer value for the Vertex
        self.weight_prompt_window = Toplevel(master=self, takefocus=True)
        self.weight_prompt_window.geometry(newGeometry=f'300x100+{x}+{y}')

        # Have the weight prompt window take focus and all interaction until it is destroyed
        self.weight_prompt_window.wait_visibility()
        self.weight_prompt_window.grab_set()
        self.weight_prompt_window.focus_set()

        # Creates a canvas in the new window to house the widgets
        weight_prompt_canvas = Canvas(self.weight_prompt_window, height=100, width=300)
        weight_prompt_canvas.grid(row=0, column=0)

        # Create a text entry widget in the toplevel window
        weight_entry_window = weight_prompt_canvas.create_window(150, 45)
        self.weight_entry = Entry(weight_prompt_canvas)
        weight_prompt_canvas.itemconfigure(weight_entry_window, window=self.weight_entry)

        # Create the label for the entry prompt
        weight_label_window = weight_prompt_canvas.create_window(150, 20)
        weight_label = Label(weight_prompt_canvas, text='Please enter an integer value for the edge weight')
        weight_prompt_canvas.itemconfigure(weight_label_window, window=weight_label)

        # Create the accept button for the entry prompt
        weight_accept_window = weight_prompt_canvas.create_window(150, 80)
        weight_accept = Button(weight_prompt_canvas, text='Accept', command=self.__get_weight)
        weight_prompt_canvas.itemconfigure(weight_accept_window, window=weight_accept)

        # Bind the enter key to the accept command as well
        self.weight_prompt_window.bind('<Key-Return>', self.__get_weight)

        # Make the entry take immediate focus so the user can enter a value immediately
        self.weight_entry.focus()

        self.wait_window(window=self.weight_prompt_window)

    def __get_weight(self, event=None):
        """Command for the weight prompt accept button

        Parameters
        ----------
        event : Event, optional
            The event triggered by either pressing <enter> or left clicking the accept button
        """
        try:
            self.entered_weight = int(self.weight_entry.get())
        except ValueError:
            print("Entered is not an integer, please enter an integer")
            self.weight_entry.select_range(0, tk.END)
            return

        if self.entered_weight < 0:
            print("Entered weight must be a non-negative integer")
            self.weight_entry.select_range(0, tk.END)
            return

        self.weight_prompt_window.grab_release()
        self.weight_prompt_window.destroy()

    # -------------------------------- #
    #                                  #
    #         Edge Deletion            #
    #                                  #
    # -------------------------------- #

    def __delete_edge(self):
        """Deletes the edge between adjacent vertices"""

        # The ids of the selected vertices
        v1_id, v2_id = self.sel_vertex_ids

        # First we need to make sure that the selected vertices are adjacent in the first place
        if not self.graph.are_adjacent(v1_id, v2_id):
            print('The selected vertices are not adjacent!')
            return

        # Since the selected vertices are adjacent, we find the id of the edge between them
        for k in self.lines.keys():
            if v1_id in self.lines[k][2] and v2_id in self.lines[k][2]:
                # Remove the edge, the weight text box and its weight text from the graph canvas
                self.graph_canvas.delete(k)
                self.graph_canvas.delete(self.lines[k][0])
                self.graph_canvas.delete(self.lines[k][1])

                # Remove the edge from the underlying graph
                self.graph.remove_edge(v1_id, v2_id)

                # Now finally, remove the edge from the lines dictionary
                del self.lines[k]

                # Update the graph info text
                self.__update_graph_info()

                return

    # -------------------------------- #
    #                                  #
    #        Giving and Taking         #
    #                                  #
    # -------------------------------- #

    def give(self, event):
        """The action of giving a value from the selected vertex to all adjacent vertices

        Parameters
        ----------
        event : Event
            The event triggered when the user left-clicks on the graph canvas
        """

        # Get all objects overlapping with the current mouse location
        overlaps = self.graph_canvas.find_overlapping(event.x-3, event.y-3,
                                                      event.x+3, event.y+3)

        # The vertex that was clicked on
        vertex = 0

        for i in range(len(overlaps)):
            if self.graph_canvas.type(overlaps[i]) == 'oval':
                self.sel_vertex_ids.append(overlaps[i])
                vertex = self.graph.find_vertex(overlaps[i])

        # A list of the ids of the vertices adjacent to the selected vertex
        adj_vertices = vertex.get_adjacent_vertices()

        # The value texts of all the adjacent vertices
        adj_value_texts = []

        # Get a list of the value texts of the adjacent vertices
        for i in range(len(adj_vertices)):
            x, y = adj_vertices[i].get_coordinates()
            adj_value_texts.append(self.graph_canvas.find_closest(x, y-34))

        # The coordinates of the selected vertex
        x, y = vertex.get_coordinates()

        # Find the value text for the selected vertex
        value_text = self.graph_canvas.find_closest(x, y-34)

        # Have the vertex give to all of its adjacent vertices
        vertex.give()

        # Change the value text of the vertex to reflect its new value
        self.graph_canvas.itemconfigure(value_text, text=str(vertex.get_value()))

        # Change the value text of all of the vertices adjacent to the selected vertex
        for i in range(len(adj_value_texts)):
            self.graph_canvas.itemconfigure(adj_value_texts[i], text=str(adj_vertices[i].get_value()))

        self.sel_vertex_ids = []

    def take(self, event):
        """The action of taking a value from each of the selected vertex's adjacent vertices

        Parameters
        ----------
        event : Event
            The event triggered when the user left-clicks on the graph canvas
        """

        # Get all objects overlapping with the current mouse location
        overlaps = self.graph_canvas.find_overlapping(event.x - 3, event.y - 3,
                                                      event.x + 3, event.y + 3)

        # The vertex that was clicked on
        sel_vertex = None

        for i in range(len(overlaps)):
            if self.graph_canvas.type(overlaps[i]) == 'oval':
                self.sel_vertex_ids.append(overlaps[i])
                sel_vertex = self.graph.find_vertex(overlaps[i])

        # A list of the ids of the vertices adjacent to the selected vertex
        adj_vertex_ids = sel_vertex.get_adjacent_vertices()

        # The value texts of all the adjacent vertices
        adj_value_texts = []

        # Get a list of the value texts of the adjacent vertices
        for i in range(len(adj_vertex_ids)):
            x, y = adj_vertex_ids[i].get_coordinates()
            adj_value_texts.append(self.graph_canvas.find_closest(x, y - 34))

        # The coordinates of the selected vertex
        x, y = sel_vertex.get_coordinates()

        # Find the value text for the selected vertex
        value_text = self.graph_canvas.find_closest(x, y - 34)

        # Have the vertex from each of its adjacent vertices
        sel_vertex.take()

        # Change the value text of the vertex to reflect its new value
        self.graph_canvas.itemconfigure(value_text, text=str(sel_vertex.get_value()))

        # Change the value text of all of the vertices adjacent to the selected vertex
        for i in range(len(adj_value_texts)):
            self.graph_canvas.itemconfigure(adj_value_texts[i], text=str(adj_vertex_ids[i].get_value()))

        self.sel_vertex_ids = []

    # -------------------------------- #
    #                                  #
    #    Calculating Shortest Path     #
    #                                  #
    # -------------------------------- #

    def shortest_path(self):
        """Calculates the shortest path between the two selected vertices"""
        v1_id, v2_id = self.sel_vertex_ids

        sp = ShortestPathCalculator()

        source, dest = self.graph.find_vertex(v1_id), self.graph.find_vertex(v2_id)

        path = sp.dijkstra(self.graph, source, dest)

        # Unbind the hover vertex command so the user can see the shortest path
        self.graph_canvas.unbind('<Motion>', self.hv_funcid)

        # Unbind the select vertex command so the user cannot select more vertices
        self.graph_canvas.tag_unbind('vertex', '<Button-1>', self.sv_funcid)

        # Lastly, reset all of the graph colors so that we can color the path properly
        self.__reset_colors()

        # The source vertex will be cyan and the destination vertex will be yellow
        self.graph_canvas.itemconfigure(path[0], fill='Cyan')
        self.graph_canvas.itemconfigure(path[-1], fill='Yellow')

        for i in range(len(path)):
            if 0 < i < len(path)-1:
                self.graph_canvas.itemconfigure(path[i], fill='Purple')
            if i != len(path)-1:
                self.graph_canvas.itemconfigure(self.__get_edge(path[i], path[i+1]), fill='Purple')

        # Reactivate the shortest path button
        self.sp_button.config(state=tk.ACTIVE)

    # -------------------------------- #
    #                                  #
    #            Canceling             #
    #                                  #
    # -------------------------------- #

    def cancel(self):
        """Cancels the currently active command so a new one may be selected"""

        # If no command is currently active then do nothing
        if self.active_command is None:
            return

        # First remove the context text
        self.graph_canvas.delete(self.context_text)

        # Execute the cancellation of whatever the currently active command is
        self.cancel_commands.get(self.active_command)()

        # Change the active command to None
        self.active_command = None

        # Reactivate all buttons
        self.__activate_all()

    def __cancel_nv(self):
        """Cancels the new vertex command"""

        # Unbind the draw vertex event from the left mouse button
        self.graph_canvas.unbind('<Button-1>', self.draw_funcid)

    def __cancel_dv(self):
        """Cancels the delete Vertex command"""

        # Unbind the delete vertex event from all ovals
        self.graph_canvas.tag_unbind('vertex', '<Button-1>', self.dv_funcid)

    def __cancel_sv(self):
        """Cancels any command that involves selecting multiple vertices"""

        # Unbind the select vertex event from all ovals
        try:
            self.graph_canvas.tag_unbind('vertex', '<Button-1>', self.sv_funcid)
        except TclError:
            pass

        # Set selected vertices back to empty and change the selected vertices back to green
        if self.sel_vertex_ids:
            for i in range(len(self.sel_vertex_ids)):
                self.graph_canvas.itemconfigure(self.sel_vertex_ids[i], fill='green')
            self.sel_vertex_ids = []

    def __cancel_gt(self):
        """Cancels the give/take command"""

        # Unbind the give/take events for all ovals
        self.graph_canvas.tag_unbind('vertex', '<Button-1>', self.g_funcid)
        self.graph_canvas.tag_unbind('vertex', '<Button-3>', self.t_funcid)

    def __cancel_sp(self):
        """Cancels the shortest path command entirely"""

        # First we cancel the select vertex command
        self.__cancel_sv()

        # Next, we re-bind the hover vertex event to mouse movement
        self.hv_funcid = self.graph_canvas.bind('<Motion>', self.__hover_vertex)

        # Lastly we reset the colors of the graph
        self.__reset_colors()

    # -------------------------------- #
    #                                  #
    #           Info Canvas            #
    #                                  #
    # -------------------------------- #

    def __update_graph_info(self):
        """Display information about the graph in its current state"""

        # First we update the information with the graph's current form
        graph_info = f'Vertices: {len(self.graph.vertices)}\n' + \
                     f'Edges: {len(self.graph.weights.keys())}\n' + \
                     f'Min Degree: {self.graph.find_min_degree()}\n' + \
                     f'Max Degree: {self.graph.find_max_degree()}'

        # Then we update the text widget to display this new text
        self.info_canvas.itemconfigure(self.basic_info_txt, text=graph_info)

    def __display_hover_info(self, v_id):
        """Displays info about the given vertex in the info canvas

        Parameters
        ----------
        v_id : int
            The id of a vertex (oval)
        """
        x, y = self.graph.get_coordinates(v_id)

        # First we create the string that we will display for the vertex
        vertex_info = f'ID: {v_id}\n' + \
                      f'Value: {self.graph.find_vertex(v_id).get_value()}\n' + \
                      f'Degree: {len(self.graph.find_vertex(v_id).get_adjacent_vertices())}\n' + \
                      f'Coordinates: ({x}, {y})'

        # Then we update the text widget to display this new text
        self.info_canvas.itemconfigure(self.hover_info_txt, text=vertex_info)

    # -------------------------------- #
    #                                  #
    #          Helper Functions        #
    #                                  #
    # -------------------------------- #

    def __get_edges(self, vertex):
        """Returns a list of the edges (lines) that are connected to the supplied vertex

        Parameters
        ----------
        vertex : Vertex/int
            Either a Vertex object or the id of one in the graph

        Returns
        -------
        list
            A list of the ids of the lines (edges) that extend from the given vertex
        """

        if isinstance(vertex, Vertex):
            vertex = vertex.id

        connected_edges = []

        for k in self.lines.keys():
            if vertex in self.lines[k][2]:
                connected_edges.append(k)

        return connected_edges

    def __get_edge(self, vertex1, vertex2):
        """Returns the edge (if there is one) between the given vertices

        Parameters
        ----------
        vertex1 : Vertex/int
            Either a Vertex object or the id of one in the graph
        vertex2 : Vertex/int
            Either a Vertex object or the id of one in the graph

        Returns
        -------
        int
            The id of the line (edge) between the given vertices in the graph, or None
        """

        if isinstance(vertex1, Vertex):
            vertex1 = vertex1.id
        if isinstance(vertex2, Vertex):
            vertex2 = vertex2.id

        for k in self.lines.keys():
            if vertex1 in self.lines[k][2] and vertex2 in self.lines[k][2]:
                return k

        return None

    def __reset_colors(self):
        """Resets the colors of all of the text, ovals and lines on the graph canvas to their defaults"""
        for i in range(len(self.ovals)):
            if not self.ovals[i] in self.sel_vertex_ids:
                self.graph_canvas.itemconfigure(self.ovals[i], fill='green')
        for k, v in self.lines.items():
            self.graph_canvas.itemconfigure(k, fill='blue')
            self.graph_canvas.itemconfigure(v[1], fill='black')
















