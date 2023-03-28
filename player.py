from vpython import *

class Player:
    def __init__(self, pos, color):
        self.segments = []
        self.head = sphere(pos=pos, radius=0.5, color=color)
        self.segments.append(self.head)
        self.direction = vector(1, 0, 0)

        # Bind the keydown event to the scene object
        scene.bind('keydown', self.handle_keydown)

    def handle_keydown(self, evt):
        """Handle the keydown event."""
        if evt.key == 'up':
            self.set_direction(vector(0, 1, 0))
        elif evt.key == 'down':
            self.set_direction(vector(0, -1, 0))
        elif evt.key == 'left':
            self.set_direction(vector(-1, 0, 0))
        elif evt.key == 'right':
            self.set_direction(vector(1, 0, 0))

    def move(self):
        """Move the player in the current direction."""
        head_pos = self.head.pos + self.direction
        new_head = sphere(pos=head_pos, radius=0.5, color=self.head.color)
        self.segments.insert(0, new_head)
        self.head = new_head
        self.segments[-1].visible = False
        self.segments.pop()

    def set_direction(self, direction):
        """Set the current direction of the player."""
        self.direction = direction

    def grow(self):
        """Add a new segment to the player."""
        pos = self.segments[-1].pos
        new_segment = sphere(pos=pos, radius=0.5, color=self.head.color)
        self.segments.append(new_segment)

    def die(self):
        """Handle the player's death."""
        for segment in self.segments:
            segment.visible = False
        self.segments = []
        self.head = None
