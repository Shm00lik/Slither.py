import vpython as vp
import math

class Player:
    STARTING_RADIUS = 0.5
    DEFAULT_COLOR = vp.color.red
    STARTING_DIRECTION = vp.vector(1, 0, 0)
    STARTING_VELOCITY = 0.1 # Units per second
    MAX_ANGLE_CHANGE = math.radians(7) # Degrees to radians
    TURN_SPEED = 1 # Radians per second

class Food:
    SMALL_RADIUS = 0.5
    LARGE_RADIUS = 1
    STARTING_COLOR = vp.color.green


class Game:
    CANVAS_WIDTH = 1800
    CANVAS_HEIGHT = 900
    CANVAS_CENTER = vp.vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, 0)
    CANVAS_BACKGROUND_COLOR = vp.vector(51, 51, 57) * (1 / 255)

    PLATFORM_WIDTH = 20_000
    PLATFORM_HEIGHT = 20_000

class Networking:
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 3339
