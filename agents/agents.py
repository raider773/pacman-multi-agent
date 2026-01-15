import pygame as pg
import heapq 
from random import randint

pg.init()



#agregar velocidades en algun momento (no mas casillas, sino mas movimientos mientras lkos otros estan quietos sria creo)


#finite state machine (FSM):
    #- Pacman [eat]
    #- chasers [idle, chase, patrol]
    
    
#Add small randomness or “hesitation” to humanize them.

    
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
       self.states = ["eat"]
       self.current_state = "eat" 
       
    def move(self, graph):         
        if self.current_state == "eat":
            next_position = self._eat_pellets(graph)     
        if self._check_valid_movement(next_position):
            self.current_position = next_position        
        
    def _eat_pellets(self, graph):
        starting_position = self.current_position
        open_list = []
        path = {}
        cost_values = {starting_position: 0}
        heapq.heappush(open_list, (0,starting_position))       
        
        
        nodes_with_pellets = []
        for node in graph.keys():
            if graph[node].has_pellet :
                nodes_with_pellets.append(node)
        
        while open_list:
            current_priority, current_node = heapq.heappop(open_list)
            if graph[current_node].has_pellet:
                break
            for adjacent_tile in graph[current_node].adjacent_tiles:
                new_cost = cost_values[current_node] + 1
                if adjacent_tile not in cost_values or new_cost < cost_values[current_node]:
                    cost_values[adjacent_tile] = new_cost
                    path[adjacent_tile] = current_node                     
                    
                    h = min(abs(adjacent_tile[0] - pellet[0]) + abs(adjacent_tile[1] - pellet[1]) for pellet in nodes_with_pellets)                          
                    priority = new_cost + h + graph[adjacent_tile].threat_level   
                    
                    heapq.heappush(open_list, (priority, adjacent_tile))            
        
        target = current_node      
        
        if target == starting_position:
                return starting_position
            
        if target != starting_position:
            next_move = target
            while path[next_move] != starting_position:
                next_move = path[next_move]            
        return next_move          
        
        
class Seeker(Agent):
    def __init__(self, row, column, enviroment):
       super().__init__(row, column, enviroment)  
       self.color = (0, 100, 100)      
       
    def move(self, graph):
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
        