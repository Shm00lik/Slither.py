import pywebio.input as pwinput
import vpython as vp

import constants
from player import Player


class Game:
    def __init__(self):
        self.me = None
        self.players = []
        self.scene = vp.canvas(
            width=constants.Game.CANVAS_WIDTH, 
            height=constants.Game.CANVAS_HEIGHT, 
            background=constants.Game.CANVAS_BACKGROUND_COLOR
        )

        self.setup()

    def setup(self):
        self.scene.userpan = False
        self.scene.userspin = False
        self.scene.userzoom = False
        self.scene.autoscale = False
        self.me = Player(self.scene, pwinput.input("Enter your name: ", type="text"))

        vp.sphere(pos=vp.vector(0, 0, 0), color=vp.color.white)
        vp.sphere(pos=vp.vector(1, 0, 0), color=vp.color.green)
        vp.sphere(pos=vp.vector(0, 1, 0), color=vp.color.red)
        vp.sphere(pos=vp.vector(0, 0, 1), color=vp.color.blue)


Game()