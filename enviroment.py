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

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")
    

# Initialize Pygame
pg.init()

# --- Grid settings ---
tile_size = 25
width = 28
height = 31

# --- Colors ---
background_color = (255, 255, 255)
walkable_tile_color = (0, 0, 0)
unwalkable_tile_color = (50, 50, 255)

class tile ():
    def __init__(self,x,y,tile_size):
        self.rect = pg.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        self.walkable = False

grid = []
for y in range(height):
    row = []
    for x in range(width):
        current_tile = tile(x,y,tile_size)
        row.append(current_tile)
    grid.append(row)
    

pacman_map = [
    "1111111111111111111111111111", #1
    "1000000000000110000000000001", #2
    "1011110111110110111110111101", #3
    "1011110111110110111110111101", #4
    "1011110111110110111110111101", #5
    "1000000000000000000000000001", #6
    "1011110110111111110110111101", #7
    "1011110110111111110110111101", #8
    "1000000110000110000110000001", #9
    "1111110111110110111110111111", #10
    "1111110111110110111110111111", #11
    "1111110110000000000110111111", #12
    "1111110110111111110110111111", #13
    "1111110110100000010110111111", #14
    "0000000000100000010000000000", #15
    "1111110110100000010110111111", #16
    "1111110110111111110110111111", #17
    "1111110110000000000110111111", #17
    "1111110110111111110110111111", #18
    "1111110110111111110110111111", #19
    "1000000000000110000000000001", #20
    "1011110111110110111110111101", #21
    "1011110111110110111110111101", #22
    "1000110000000000000000110001", #23
    "1110110110111111110110110111", #24
    "1110110110111111110110110111", #25
    "1000000110000110000110000001", #26
    "1011111111110110111111111101", #27
    "1011111111110110111111111101", #28
    "1000000000000000000000000001", #29
    "1111111111111111111111111111", #30
]

# Now apply this map to your existing grid
for y, row in enumerate(pacman_map):
    for x, char in enumerate(row):
        if char == "0":  # walkable
            grid[y][x].walkable = True


# --- Setup display ---
screen = pg.display.set_mode((width * tile_size, height * tile_size))
pg.display.set_caption("Grid with Walls")

clock = pg.time.Clock()


# --- Game loop ---
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Draw background
    screen.fill(background_color)

    # Draw grid
    for y in range(height):
        for x in range(width):
            if grid[y][x].walkable == False:
                pg.draw.rect(screen, unwalkable_tile_color, grid[y][x].rect)
            else:
                pg.draw.rect(screen, walkable_tile_color, grid[y][x].rect)

    pg.display.flip()
    clock.tick(60)

pg.quit()
sys.exit()

