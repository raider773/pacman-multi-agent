##assert tamaño grid
##assert que las walls sean walkable
## cant walkables vs la cantidad que tiene que ser en cada mapa





#agrega a los walkable que tienen pellet. tamb algunos que tengan el pellet grande

#agregar atributo extra de puerta. si es peurta y esta en true o algo asi lo 
#pones como walkable



#finite state machine (FSM) para estado scatrter, chase, idle, running away, eaten

"""
 Pac-Man (AI version)
Goal:

Navigate the maze collecting pellets while avoiding ghosts.

Algorithms:
Purpose	Algorithm	Why
Navigation toward pellets	A*	Finds shortest path to the nearest pellet efficiently.
Ghost avoidance	Dijkstra with “threat cost”	Add extra cost for tiles near ghosts → Pac-Man detours around them.
Frightened chasing (optional)	Greedy BFS toward nearest ghost	When ghosts are frightened, Pac-Man hunts them.

This lets Pac-Man use weighted pathfinding and heuristics to feel “intelligent.”

Blinky (Red Ghost)
Classic Role: The direct chaser.
Behavior & Algorithms:
State	Algorithm	Target / Logic
Chase	A*	Target Pac-Man’s current position (straight pursuit).
Scatter	Breadth-First Search (BFS)	Go to assigned corner tile. BFS guarantees shortest path in uniform grid.
Frightened	Random walk (uniform random valid move)	Emulates panic; no pathfinding.
Eaten	Dijkstra	Fast route back to ghost house (home), supports weighted speeds if you add them later.

→ Blinky is your reference A* ghost — deterministic, efficient, always finds Pac-Man.
 Pinky (Pink Ghost)
Classic Role: The ambusher.
Behavior & Algorithms:
State	Algorithm	Target / Logic
Chase	A* (with look-ahead target)	Target 4 tiles ahead of Pac-Man’s direction.
Scatter	BFS	Corner.
Frightened	Randomized DFS	DFS creates unpredictable wandering (fewer reversals).
Eaten	A*	Return to home directly.

→ Pinky still uses A*, but you’ll adjust the target position heuristic. This teaches how different heuristics affect pursuit.

 Inky (Blue Ghost)
Classic Role: The “tricky” one — uses vector math with Blinky.
Behavior & Algorithms:
State	Algorithm	Target / Logic
Chase	Hybrid: BFS for pathfinding + computed vector target	Target = 2×(Pac-Man ahead position) – (Blinky position). Path found via BFS.
Scatter	Greedy Best-First Search	Head toward its corner, but only greedily (not guaranteed shortest path).
Frightened	Random weighted movement	Weighted by distance from Pac-Man (moves away if close).
Eaten	Dijkstra	Home route.

→ Inky gives you practice combining target prediction + BFS, and best-first search, which uses only the heuristic, not full A*.

 Clyde (Orange Ghost)
Classic Role: Shy / unpredictable.
Behavior & Algorithms:
State	Algorithm	Target / Logic
Chase	Conditional BFS or Random BFS	If far from Pac-Man (>8 tiles), chase him via BFS; if close, head to corner randomly.
Scatter	DFS	Wanders toward corner without optimal path (looks more hesitant).
Frightened	Random movement	Simple, chaotic.
Eaten	BFS	Straight to home.

→ Clyde demonstrates behavioral switching and simpler pathfinding (BFS, DFS), showing how search depth and branching affect patterns.



"""

#https://itnext.io/how-to-create-pac-man-in-python-in-300-lines-of-code-or-less-part-1-288d54baf939
#aca arriba esta el mapa que estas usando

# Import Modules
import sys
import pygame as pg
import yaml
from environment.env import Environment
from agents.agents import Eater, Seeker, Hunter, Pursuer, Catcher

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")
    
# Initialize Pygame
pg.init()

with open("conf/conf.yaml") as f:
    config = yaml.safe_load(f)

                    
env = Environment()
env.fill_matrix(config["height"], config["width"], config["tile_size"])
env.load_layout(config["default_layout"])   
      
        
eater = Eater(5,5,env)
seeker = Seeker(5,6,env)
hunter = Hunter(20,6,env)
pursuer = Pursuer(26,24,env)
catcher = Catcher(14,18,env)

eater_list = [eater]
chasers_list = []
#chasers_list = [seeker, hunter, pursuer, catcher]

# --- Setup display ---
screen = pg.display.set_mode((config["width"] * config["tile_size"], config["height"] * config["tile_size"]))
pg.display.set_caption("Grid with Walls")

clock = pg.time.Clock()
last_move_time = 0 
move_delay = 1000    

DEBUG = False  # Set to False to hide threat heatmap overlay
font = pg.font.SysFont(None, 16)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Draw background
    screen.fill(tuple(config["background_color"]))

    # Draw grid
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

            # Draw hideout
            if tile.hideout:
                pg.draw.rect(screen, tuple(config["hideout_tile_color"]), tile.rect)

            # DEBUG: overlay threat heatmap
            if DEBUG and tile.walkable and env.current_graph:
                node = env.current_graph.get((y, x))
                if node:
                    intensity = int((node.threat_level / config["max_threat_level"]) * 255)
                    intensity = max(0, min(intensity, 255))
                    heat_surface = pg.Surface((tile.rect.width, tile.rect.height), pg.SRCALPHA)
                    heat_surface.fill((intensity, 0, 0, 255))
                    screen.blit(heat_surface, (tile.rect.x, tile.rect.y))
        
                    # draw number using pre-created font
                    text = font.render(f"{int(node.threat_level)}", True, (255, 255, 255))
                    screen.blit(text, (tile.rect.x + 2, tile.rect.y + 2))

    # Update graph with current ghost positions and threat levels
    env.create_graph(threat_agents= chasers_list, max_threat_level= config["max_threat_level"], decay_rate= config["decay_rate"])

    # Move agents with time delay
    current_time = pg.time.get_ticks()
    if current_time - last_move_time >= move_delay:
        for agent in eater_list + chasers_list:
            agent.move()


        # Pacman consumes pellet
        env.grid[eater.current_position[0]][eater.current_position[1]].has_pellet = False

        last_move_time = current_time

    # Draw agents
    for agent in eater_list + chasers_list:
        agent.draw(screen)

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()



# si pacman pasa por arriba, chau pellet


