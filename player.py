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
        self.num_of_segments = 30

        self.a = None
        self.b = None

        self.is_sprinting = False

        self.canvas.bind("keydown", self.on_key_down)

    def on_key_down(self, event):
        if event.key == "w":
            self.num_of_segments += 10
        elif event.key == "s":
            self.num_of_segments -= 10
        elif event.key == "e":
            self.sprint()
        elif event.key == "q":
            self.stop_sprinting()


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

        if self.is_sprinting:
            self.verify_sprint()

        self.position += self.direction * self.velocity
        self.position.z = 0

        self.segments.insert(0, self.position)

        self.update_length()

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

    def update_length(self):
        while len(self.segments) > self.num_of_segments:
            self.segments.pop()

    def is_able_to_sprint(self):
        return self.num_of_segments >= constants.Player.MIN_NUM_OF_SEGMENTS
    
    def sprint(self):
        if self.is_able_to_sprint() and not self.is_sprinting:
            self.velocity = constants.Player.SPRINT_VELOCITY_FACTOR * self.velocity
            self.is_sprinting = True

    def verify_sprint(self):
        if not self.is_able_to_sprint():
            self.stop_sprinting()
        else:
            self.num_of_segments -= constants.Player.SPRINT_COST

    def stop_sprinting(self):
        if self.is_sprinting:
            self.is_sprinting = False
            self.velocity = self.velocity / constants.Player.SPRINT_VELOCITY_FACTOR