import os


EPSILON = 1e-12

PLAYER_COLOR = (255, 100, 100)
CAMERA_XBORDER = 250
CAMERA_YBORDER = 160


RADIUS_OIL_SCALE = 1.5

SAVE_FILE = "max_level.dat"


TILE_COLOR = (255, 255, 255)
DATA_WORLD = os.path.join("data", "level_0.txt")
DATA_DIR = "data"
PLAYER_ANIMATION_DATA = os.path.join("data", "miner")
TILE_SIZE = 64

SCALE_FACTOR = TILE_SIZE // 32

FONT_LOCATION = os.path.join("data", "prstartk.ttf")#os.path.join(DATA_DIR, "PressStart2P-Regular.ttf")
FONT_SIZE_TITLE = 40
FONT_LETTER_B = 50
FONT_LETTER = 40
FONT_SIZE_SMALL = 16
FONT_SIZE_MENU = 22
FONT_SIZE_MENU_B = 32


GRAVITY = 0.3
MAX_VERTICAL_SPEED = 5
AIR_FRICTION = 0.05



GROUND_DIR = os.path.join("data", "ground")
GROUND_TOP = os.path.join(GROUND_DIR, "ground_1.png")
GROUND_TOPLEFT = os.path.join(GROUND_DIR, "ground_2.png")
GROUND_LEFT = os.path.join(GROUND_DIR, "ground_3.png")
GROUND_BULK = os.path.join(GROUND_DIR, "ground_4.png")
GROUND_TOPLEFTRIGHT = os.path.join(GROUND_DIR, "ground_5.png")
GROUND_LEFTRIGHT = os.path.join(GROUND_DIR, "ground_6.png")


WINDOW_SIZE = (800, 600)