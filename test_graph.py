import pygame as pg
import yaml
from environment.env import Environment
import matplotlib.pyplot as plt


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
env.load_layout(config["default_layout"])


env.create_graph(threat_agents_positions = [(5,5),(20,6),(26,24),(14,18)], max_threat_level = 50, decay_rate = 0.15)


def graph_to_threat_matrix(graph, width, height): 
    matrix = [[0 for _ in range(width)] for _ in range(height)]
    
    for (y, x), node in graph.items():
        matrix[y][x] = node.threat_level
    
    return matrix


threat_matrix = graph_to_threat_matrix(env.current_graph, config["width"], config["height"])
# threat_matrix is your 2D list of threat levels
plt.imshow(threat_matrix, cmap='hot', interpolation='nearest')
plt.colorbar(label='Threat Level')
plt.title("Threat Level Heatmap")
plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Parameters
max_threat = 50
distances = np.arange(0, 15, 1)  # distances from 0 to 14
k_values = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]       # different decay rates

plt.figure(figsize=(8,5))

for k in k_values:
    threat = max_threat * np.exp(-k * distances)
    plt.plot(distances, threat, label=f'k={k}')

plt.xlabel("Distance from source")
plt.ylabel("Threat level")
plt.title("Exponential Decay of Threat")
plt.legend()
plt.grid(True)
plt.show()
