import pygame as pg
import math
from concurrent.futures import ThreadPoolExecutor

class Tile ():
    """
    Represents an individual tile.
    
    Attributes
    ----------
    x : int
        The starting x-coordinate of the tile.
    y : int
        The starting y-coordinate of the tile.
    tile_size : int
        The size of each tile in pixels.
    """
    
    def __init__(self, x:int, y:int, tile_size:int):
        self.rect = pg.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        self.x = x
        self.y = y
        self.walkable = False
        self.has_pellet = False        
        
class Environment():
    """
    Environment where agents will interact between each other.
    
    Methods
    ---------
    fill_matrix(height:int, width:int, tile_size:int) -> list[list[int]]
        Fills environment with empty tiles.
        
    load_layout(layout:list[list[int]]) -> None
        Loads layout into environment, making wakable tiles.
        
    """
    
    def __init__(self):
        self.grid = []
        self.current_graph = []
        
    def fill_matrix (self, height:int, width:int, tile_size:int) -> list[list[int]]:
        """
        Fills environment with empty tiles.
    
        Parameters
        ----------
        height : int
            Number of rows in the grid.
        width : int
            Number of columns in the grid.
        tile_size : int
            Size of each tile in pixels.
    
        Returns
        -------
        list[list[int]]
            A 2D list filled with zeros representing empty tiles.
        """
    
        for y in range(height):
            row = []
            for x in range(width):
                current_tile = Tile(x, y, tile_size)
                row.append(current_tile)
            self.grid.append(row)
    
    def load_layout(self, layout:list[list[int]]) -> None:
        """        
        Updates the `self.grid` attribute. Each cell's `walkable` property is set
        to True if the corresponding layout element is "0". `has_pellet` property is also set to True
    
        Parameters
        ----------
        layout : list[list[string]]
            A 2D list representing the environment layout.
            Each element should be a string indicating the type of tile:
            - "0" : walkable tile 
            - "1" : unwalkable tile             
    
        Returns
        -------
        None  
        """
        
        for y, row in enumerate(layout):
            for x, char in enumerate(row):
                if char == "0":  # walkable and pellet
                    self.grid[y][x].walkable = True
                    self.grid[y][x].has_pellet = True        
                  
    def create_graph(self, threat_agents:list, max_threat_level:float, decay_rate:float) -> None:   
        """
        Creates a graph representation of the environment and propagates threat levels from agents.
    
        Each walkable tile becomes a node in the graph. Nodes store their coordinates, 
        whether they contain a pellet, their current threat level, and a list of adjacent walkable tiles.
    
        Threat levels are propagated from specified agent positions using exponential decay, 
        decreasing as distance from the agent increases.
    
        Parameters
        ----------
        threat_agents_positions : list of tuple
            List of (y, x) coordinates representing positions of agents (e.g., ghosts) 
            that generate threat.
        max_threat_level : float
            The maximum threat level assigned at the agent's position.
        decay_rate : float
            Rate for exponential function, represented as k in the formula.
    
        Returns
        -------
        None            
    
        Notes
        -----
        The resulting graph is stored in `self.current_graph`. Each node contains:
            - coord : tuple of (y, x)
            - has_pellet : bool
            - threat_level : float
            - adjacent_tiles : list of neighboring node coordinates
        - The graph is represented as a dictionary: keys are (y, x) coordinates, 
          values are node objects.
        - Threat propagation uses BFS and exponential decay:
            threat = max_threat_level * exp(-k * distance)
        - Distance is measured as steps along walkable tiles.
        - ThreadPoolExecutor is used to parallelize row processing for faster graph creation.
        """
        
        class node():
            def __init__(self):
                self.coord = None
                self.has_pellet = None
                self.threat_level = 1
                self.adjacent_tiles = []                
       
        def process_row(row:list[int], y:int, grid:list[list[int]]) -> None:
            row_nodes = {}
            for element in row:
                if element.walkable: # Only add nodes that are walkable
                    new_node = node()
                    new_node.coord = (element.y,element.x)
                    new_node.has_pellet = element.has_pellet
                    new_node.threat_level = 1
                    new_node.adjacent_tiles = []     
                    
                    # Create adjacnecy list
        
                    # Down
                    if grid[element.y + 1][element.x].walkable:
                        new_node.adjacent_tiles.append((element.y + 1, element.x))
                    # Up
                    if grid[element.y - 1][element.x].walkable:
                        new_node.adjacent_tiles.append((element.y - 1, element.x))
                    # Right
                    if grid[element.y][element.x + 1].walkable:
                        new_node.adjacent_tiles.append((element.y, element.x + 1))
                    # Left
                    if grid[element.y][element.x - 1].walkable:
                        new_node.adjacent_tiles.append((element.y, element.x - 1))
        
                    row_nodes[(element.y, element.x)] = new_node
            return row_nodes
    
        def add_threat_levels(graph:dict[tuple:list[tuple[int]]], threat_agents:list, max_threat_level:int) -> None:            
            for agent in threat_agents:
                queue = []
                queue.append((agent.current_position, 0))
                
                while len(queue) > 0: 
                    current_pos, distance = queue.pop(0)         
                    node = graph[current_pos]
                    new_threat = max_threat_level * math.exp(-decay_rate * distance)  
                    
                    if new_threat <= node.threat_level:    
                        continue
                    
                    node.threat_level = new_threat 
                    
                    for neighbor_coord in node.adjacent_tiles:
                        queue.append((neighbor_coord, distance + 1))  
        
        
        graph = {}
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_row, row, y, self.grid) for y, row in enumerate(self.grid)]            
            for future in futures:
                graph.update(future.result())    
                                                                       
        self.current_graph = graph        
        add_threat_levels(self.current_graph, threat_agents = threat_agents, max_threat_level = max_threat_level)
        
        

        
        
        
        
        
        
        
        
        

                      
                