import pygame as pg
from random import randint

pg.init()

class Agent():
    
    def __init__(self, row, column, enviroment):
        self.current_position = (row,column)
        self.enviroment = enviroment
        self.directions = {0:"up", 1:"right", 2:"down", 3:"left"}        
        self.states = []
        self.current_state = ""
        self.color = (0,0,0)
    
    def move(self):        
        raise NotImplementedError("Subclasses must implement move()")       
    
    def _check_valid_movement(self, next_position):
        row, col = next_position              
        try:
            return self.enviroment.grid[row][col].walkable
        except IndexError:
            return False    
        
    def draw(self, screen):       
        tile = self.enviroment.grid[self.current_position[0]][self.current_position[1]]  
        center_x = tile.rect.x + tile.rect.width // 2
        center_y = tile.rect.y + tile.rect.height // 2     
        radius = tile.rect.width // 2
        pg.draw.circle(screen, (self.color), (center_x, center_y), radius)
        
 
class Eater(Agent):
    def __init__(self, row, column, enviroment):
       super().__init__(row, column, enviroment)  
       self.color = (255, 255, 0)  
       
    def move(self):
        can_move = False               
        while can_move == False:
            direction = self.directions[randint(0,3)]            
            if direction == "up":
                next_position = (self.current_position[0] - 1, self.current_position[1])
            elif direction == "right":
                next_position = (self.current_position[0], self.current_position[1] + 1)
            elif direction == "down":
                next_position = (self.current_position[0] + 1, self.current_position[1])
            elif direction == "left":
                next_position = (self.current_position[0], self.current_position[1] - 1)           
            can_move = self._check_valid_movement(next_position)       
        self.current_position = next_position    
        
        
class Seeker(Agent):
    def __init__(self, row, column, enviroment):
       super().__init__(row, column, enviroment)  
       self.color = (0, 100, 100)
       
    def move(self):
        can_move = False               
        while can_move == False:
            direction = self.directions[randint(0,3)]            
            if direction == "up":
                next_position = (self.current_position[0] - 1, self.current_position[1])
            elif direction == "right":
                next_position = (self.current_position[0], self.current_position[1] + 1)
            elif direction == "down":
                next_position = (self.current_position[0] + 1, self.current_position[1])
            elif direction == "left":
                next_position = (self.current_position[0], self.current_position[1] - 1)           
            can_move = self._check_valid_movement(next_position)       
        self.current_position = next_position   

class Hunter(Agent):
    def __init__(self, row, column, enviroment):
       super().__init__(row, column, enviroment)  
       self.color = (200, 0, 200)  
       
    def move(self):
        can_move = False               
        while can_move == False:
            direction = self.directions[randint(0,3)]            
            if direction == "up":
                next_position = (self.current_position[0] - 1, self.current_position[1])
            elif direction == "right":
                next_position = (self.current_position[0], self.current_position[1] + 1)
            elif direction == "down":
                next_position = (self.current_position[0] + 1, self.current_position[1])
            elif direction == "left":
                next_position = (self.current_position[0], self.current_position[1] - 1)           
            can_move = self._check_valid_movement(next_position)       
        self.current_position = next_position  
        
        
class Pursuer(Agent):
    def __init__(self, row, column, enviroment):
       super().__init__(row, column, enviroment)  
       self.color = (70, 0, 150)  
       
    def move(self):
        can_move = False               
        while can_move == False:
            direction = self.directions[randint(0,3)]            
            if direction == "up":
                next_position = (self.current_position[0] - 1, self.current_position[1])
            elif direction == "right":
                next_position = (self.current_position[0], self.current_position[1] + 1)
            elif direction == "down":
                next_position = (self.current_position[0] + 1, self.current_position[1])
            elif direction == "left":
                next_position = (self.current_position[0], self.current_position[1] - 1)           
            can_move = self._check_valid_movement(next_position)       
        self.current_position = next_position  
        
        
class Catcher(Agent):
    def __init__(self, row, column, enviroment):
       super().__init__(row, column, enviroment)  
       self.color = (250, 120, 0)  
       
    def move(self):
        can_move = False               
        while can_move == False:
            direction = self.directions[randint(0,3)]            
            if direction == "up":
                next_position = (self.current_position[0] - 1, self.current_position[1])
            elif direction == "right":
                next_position = (self.current_position[0], self.current_position[1] + 1)
            elif direction == "down":
                next_position = (self.current_position[0] + 1, self.current_position[1])
            elif direction == "left":
                next_position = (self.current_position[0], self.current_position[1] - 1)           
            can_move = self._check_valid_movement(next_position)       
        self.current_position = next_position  