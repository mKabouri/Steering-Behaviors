# Global variables
# Target color
YELLOW = (226, 255, 33)
GRAY = (200, 200, 200)
MAUVE = (236, 174, 249)

# Particule colors
POSSIBLE_COLORS = [
    (253, 86, 86), # RED
    (98, 156, 255) # BLUE
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
POINT_REACHED_THRESHOLD = 4 # used in circuit.py