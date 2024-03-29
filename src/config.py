# Global variables
# Target color
YELLOW = (226, 255, 33)
GRAY = (200, 200, 200)
MAUVE = (236, 174, 249)

# Restart button colors
SHADOW_COLOR = (150, 150, 150)
RESTART_BUTTON_COLOR = (10, 150, 200)
HOVER_BUTTON_COLOR = (12, 170, 220)
TEXT_COLOR = (255, 255, 255)
# Particule colors
POSSIBLE_COLORS = [
    (253, 86, 86), # RED
    (98, 156, 255), # BLUE
    (247, 0, 255), # ROSE

]

INITIAL_VELOCITY = (2, 4)
INITIAL_FORCE = (0, 0)

MAX_SPEED = 8
MAX_FORCE = 10

# Pygame setting
FPS = 20
RESTART_BUTTON_COLOR = (0, 128, 255)
TEXT_COLOR = (0, 0, 0)
FLEE_RADIUS = 50

WIDTH = 700
HEIGHT = 700
CIRCUIT_COORDS = (
    (100, 100),
    (100, 300),
    (300, 600),
    (600, 400)
)
POINT_REACHED_THRESHOLD = 3 # In circuit.py
COLLISION_THRESHOLD = 1 # In environment.py
OBSTACLE_THRESHOLD = 10 # In environment.py
OBSTACLE_RADIUS = 20 # In environment.py
OBSTACLE_AVOIDANCE_RADIUS = 30
AVOIDANCE_STRENGTH = 5
SEPARATION_DISTANCE = 35 # In flock.py behavior
NEIGHBOR_RADIUS = 100 # In environment.py for flock