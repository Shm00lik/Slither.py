import vpython as vp
import pywebio.input as pwinput
import pywebio.output as pwoutput
import constants
import utils
import math
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

        self.segments.append(self.position)

        self.curve = vp.curve(pos=self.segments, radius=self.radius, color=self.color)

        self.last_mouse_pos = vp.vector(0, 0, 0)
        self.in_transition = False

        self.a = None
        self.b = None

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
        self.position.z = 0

        self.segments.insert(0, self.position)

        if len(self.segments) > 100:
            self.segments.pop()

        # print(self.segments)

        self.curve.clear()
        self.curve.append(pos=self.segments, radius=self.radius, color=self.color)
        
        self.update_camera()

    def update_camera(self):
        self.canvas.camera.pos = vp.vector(self.position.x, self.position.y, self.segments[1].z + 10)

    def update_direction(self):
        mp = self.canvas.mouse.pos
        
        if mp == self.last_mouse_pos and not self.in_transition:
            return
            

        last_direction = self.direction

        # Calculate the angle between the current direction and the mouse direction
        current_angle = math.atan2(self.direction.y, self.direction.x)
        mouse_angle = math.atan2(mp.y - self.position.y, mp.x - self.position.x)
        angle_diff = mouse_angle - current_angle

        # Wrap the angle difference between -pi and pi to find the shortest angle
        if angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        elif angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        # Gradually adjust the direction of the snake towards the mouse direction
        if abs(angle_diff) < constants.Player.MAX_ANGLE_CHANGE:
            # If the angle difference is less than the turning threshold, no need to turn
            self.direction = vp.vector(math.cos(mouse_angle), math.sin(mouse_angle), 0).norm()
            self.in_transition = False
        else:
            # Otherwise, turn by a small fraction of the turning angle
            turn_direction = math.copysign(1, angle_diff)
            turn_amount = constants.Player.MAX_ANGLE_CHANGE * turn_direction
            new_angle = current_angle + turn_amount
            target_direction = vp.vector(math.cos(new_angle), math.sin(new_angle), 0)
            self.direction = utils.lerp(self.direction, target_direction, constants.Player.TURN_SPEED)

            self.in_transition = True

        # Update the direction arrows for debugging purposes
        if self.a is not None:
            self.a.stop()
            self.b.stop()

        self.a = vp.arrow(pos=self.position, axis=self.direction, color=vp.color.green)
        self.b = vp.arrow(pos=self.position, axis=last_direction, color=vp.color.blue)

        self.last_mouse_pos = mp
