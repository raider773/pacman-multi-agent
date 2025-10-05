##assert tamaño grid
##assert que las walls sean walkable
## cant walkables vs la cantidad que tiene que ser en cada mapa


#agente tienen algo que sea ver siguiente bloque. ese ver bloque llamo al grid walkable

#fijate igual por que algunos algoritmos son de grafos

#agregar atributo extra de teleport o de puerta. si es peurta y esta en true o algo asi lo 
#pones como walkable

#https://itnext.io/how-to-create-pac-man-in-python-in-300-lines-of-code-or-less-part-1-288d54baf939
#aca arriba esta el mapa que estas usando

# Import Modules
import sys
import pygame as pg
import yaml
from environment.env import Environment

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")
    

# Initialize Pygame
pg.init()

with open("conf/env.yaml") as f:
    config = yaml.safe_load(f)

                    
env = Environment()
env.fill_matrix(config["height"], config["width"], config["tile_size"])
env.load_layout(config["original_layout"])
    

# --- Setup display ---
screen = pg.display.set_mode((config["width"] * config["tile_size"], config["height"] * config["tile_size"]))
pg.display.set_caption("Grid with Walls")

clock = pg.time.Clock()


# --- Game loop ---
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
            if env.grid[y][x].walkable == False:
                pg.draw.rect(screen, tuple(config["unwalkable_tile_color"]), env.grid[y][x].rect)
            else:
                pg.draw.rect(screen, tuple(config["walkable_tile_color"]), env.grid[y][x].rect)

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()

