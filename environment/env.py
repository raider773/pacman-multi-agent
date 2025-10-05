import pygame as pg


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
        self.walkable = False
        
        
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
    
        Parameters
        ----------
        layout : list[list[int]]
            A 2D list representing the environment layout.
            Each element should be a string indicating the type of tile:
            - "0" or 0 : walkable tile
            - "1" or 1 : unwalkable tile (wall)
    
        Returns
        -------
        None
    
        Notes
        -----
        Updates the `self.grid` attribute. Each cell's `walkable` property is set
        to True if the corresponding layout element is "0".
        """
        
        for y, row in enumerate(layout):
            for x, char in enumerate(row):
                if char == "0":  # walkable
                    self.grid[y][x].walkable = True