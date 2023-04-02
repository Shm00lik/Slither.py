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
        
        self.setup_client(constants.Networking.DEFAULT_HOST, constants.Networking.DEFAULT_PORT)

        if pos is None:
            self.position = vp.vector.random()

        self.segments = [] 

        self.curve = vp.curve(pos=[self.position], radius=self.radius, color=self.color)
        self.curve.append(pos=[self.position + vp.vector(0, 0, 0)], radius=self.radius, color=self.color)
        self.curve.append(pos=[self.position + vp.vector(1, 0, 0)], radius=self.radius, color=self.color)
        self.curve.append(pos=[self.position + vp.vector(2, 0, 0)], radius=self.radius, color=self.color)

        self.last_mouse_pos = vp.vector(0, 0, 0)

    def setup_client(self, host: str = None, port: int = None):
        if (host is None) or (port is None):
            host = pwinput.input("Enter the host: ", type=pwinput.TEXT)
            port = pwinput.input("Enter the port: ", type=pwinput.NUMBER, validate=utils.check_port)

        # with pwoutput.put_loading():
        #     try:
        #         self.client = client.TCPClient(host, port)
        #         self.client.connect()
        #     except:
        #         pwoutput.error("Failed to connect to server")
        #         return
            
    def update(self):
        self.update_direction()

        self.position += self.direction * self.velocity
        self.curve.append(pos=[self.position], radius=self.radius, color=self.color)
        
        self.update_camera()

    def update_camera(self):
        self.canvas.camera.pos = vp.vector(self.position.x, self.position.y, 10)

    def update_direction(self):
        ml = self.canvas.mouse.pos

        if ml == self.last_mouse_pos:
            return
        
        self.direction = vp.vector(ml.x, ml.y, 0) - self.position
        self.direction = self.direction.norm()

        self.last_mouse_pos = ml