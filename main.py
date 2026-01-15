import sys
import pygame as pg
import yaml
from environment.env import Environment
from agents.agents import Eater, Seeker, Hunter, Pursuer, Catcher

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")
    
pg.init()

with open("conf/conf.yaml") as f:
    config = yaml.safe_load(f)

                    
env = Environment()
env.fill_matrix(config["height"], config["width"], config["tile_size"])
env.load_layout(config["default_layout"])   
      
        
eater = Eater(5,5,env)
seeker = Seeker(20,6,env)
hunter = Seeker(20,6,env)
pursuer = Seeker(20,6,env)
catcher = Seeker(20,6,env)

eater_list = [eater]
#chasers_list = [seeker]
chasers_list = [seeker, hunter, pursuer, catcher]

# --- Setup display ---
screen = pg.display.set_mode((config["width"] * config["tile_size"], config["height"] * config["tile_size"]))
pg.display.set_caption("Grid with Walls")

clock = pg.time.Clock()
last_move_time = 0 
move_delay = 100    


DEBUG = True  
font = pg.font.SysFont(None, 25)

running = True
game_over = False

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
    if not game_over:
      
        # Draw Grid
        screen.fill(tuple(config["background_color"]))           
        for y in range(config["height"]):
            for x in range(config["width"]):
                tile = env.grid[y][x]
    
                # Draw walkable/unwalkable tiles
                if not tile.walkable:
                    pg.draw.rect(screen, tuple(config["unwalkable_tile_color"]), tile.rect)
                else:
                    pg.draw.rect(screen, tuple(config["walkable_tile_color"]), tile.rect)
    
                # Draw pellets
                if tile.has_pellet:
                    center_x = tile.rect.x + tile.rect.width // 2
                    center_y = tile.rect.y + tile.rect.height // 2
                    radius = tile.rect.width // 6
                    pg.draw.circle(screen, tuple(config["pellet_color"]), (center_x, center_y), radius)
    
                # DEBUG: overlay threat heatmap
                if DEBUG and tile.walkable and env.current_graph:
                    node = env.current_graph.get((y, x))
                    if node:
                        intensity = int((node.threat_level / config["max_threat_level"]) * 255)
                        intensity = max(0, min(intensity, 255))
                        heat_surface = pg.Surface((tile.rect.width, tile.rect.height), pg.SRCALPHA)
                        heat_surface.fill((intensity, 0, 0, 255))
                        screen.blit(heat_surface, (tile.rect.x, tile.rect.y))      
                        text = font.render(f"{int(node.threat_level)}", True, (255, 255, 255))
                        screen.blit(text, (tile.rect.x + 2, tile.rect.y + 2))
    
        # Update graph with current ghost positions and threat levels
        env.create_graph(threat_agents = chasers_list, max_threat_level = config["max_threat_level"], decay_rate = config["decay_rate"])
    
        # Move agents with time delay        
        current_time = pg.time.get_ticks()
        if current_time - last_move_time >= move_delay:
            for agent in eater_list + chasers_list:
                agent.move(env.current_graph)
    
    
            # Pacman consumes pellet
            env.grid[eater.current_position[0]][eater.current_position[1]].has_pellet = False
    
            last_move_time = current_time
    
        # Draw agents
        for agent in eater_list + chasers_list:
            agent.draw(screen)
            
        # Count pellets. If no pelles then eater wins
        nodes_with_pellets = []
        for node in env.current_graph.keys():
            if env.current_graph[node].has_pellet :
                nodes_with_pellets.append(node)
        if len(nodes_with_pellets) == 0:
            game_over = True
            winner = "eater"
            
        # Check if eater and chaser share position. If they do eater losses
        for eater in eater_list:
            for chaser in chasers_list:
                if eater.current_position == chaser.current_position:
                    game_over = True
                    winner = "chaser"
        
    if game_over:   
        if winner == "eater":     
            game_over_message = "Eater Won"
        elif winner == "chaser":     
            game_over_message = "chaser Won"        
        text = font.render(game_over_message, True, (255, 0, 0))
        text_rect = text.get_rect(center=(320, 240))
        screen.blit(text, text_rect)        

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()






