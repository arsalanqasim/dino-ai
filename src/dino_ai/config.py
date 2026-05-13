"""Project-wide game and training configuration."""

WIDTH = 800
HEIGHT = 300
FPS = 60
GROUND_Y = HEIGHT - 40

GRAVITY = 0.6
JUMP_POWER = -11.5
BASE_GAME_SPEED = 6
MAX_GAME_SPEED = 20
GAME_SPEED_STEP = 0.002

POPULATION_SIZE = 200
MUTATION_RATE = 0.1
ELITISM_RATE = 0.05

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_COLOR = (247, 247, 247)

SPRITE_SHEET_URL = (
    "https://raw.githubusercontent.com/chromium/chromium/main/components/"
    "neterror/resources/images/default_100_percent/offline/100-offline-sprite.png"
)
SPRITE_SHEET_FILENAME = "sprite.png"
