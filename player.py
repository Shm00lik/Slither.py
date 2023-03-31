import vpython as vp
import pywebio.input as pwinput
import pywebio.output as pwoutput

import constants
import utils
from networking import client

class Player():
    def __init__(self, scene: vp.canvas, name: str, pos: vp.vector = None):
        self.canvas = scene
        self.name = name
        self.radius = constants.Player.STARTING_RADIUS
        self.color = constants.Player.DEFAULT_COLOR
        self.direction = constants.Player.STARTING_DIRECTION
        self.velocity = constants.Player.STARTING_VELOCITY

        self.client = None
        
        self.setup_client()

        if pos is None:
            self.position = vp.vector.random()

        self.curve = vp.curve(pos=[self.position], radius=self.radius, color=self.color)
        self.curve.append(pos=[self.position + vp.vector(0, 0, 1)], radius=self.radius, color=self.color)

    def setup_client(self, host: str = None, port: int = None):
        if (host is None) or (port is None):
            host = pwinput.input("Enter the host: ", type=pwinput.TEXT)
            port = pwinput.input("Enter the port: ", type=pwinput.NUMBER, validate=utils.check_port)

        with pwoutput.toast("Connecting to server..."):
            try:
                self.client = client.TCPClient(host, port)
                self.client.connect()
            except:
                pwoutput.error("Failed to connect to server")
                return
            
    def update(self):
        self.position += self.direction * self.velocity
        self.curve.append(pos=[self.position], radius=self.radius, color=self.color)