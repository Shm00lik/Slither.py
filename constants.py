import vpython as vp

class Player:
    STARTING_RADIUS = 0.5
    DEFAULT_COLOR = vp.color.red
    STARTING_DIRECTION = vp.vector(0, 0, 0)
    STARTING_VELOCITY = 0.5 # Units per second

class Food:
    SMALL_RADIUS = 0.5
    LARGE_RADIUS = 1
    STARTING_COLOR = vp.color.green


class Game:
    CANVAS_WIDTH = 1800
    CANVAS_HEIGHT = 900
    CANVAS_CENTER = vp.vector(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, 0)
    CANVAS_BACKGROUND_COLOR = vp.color.black

    PLATFORM_WIDTH = 20_000
    PLATFORM_HEIGHT = 20_000