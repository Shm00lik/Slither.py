from vpython import *
import random
from player import Player
import utils


class GameManager:
    def __init__(self):
        self.players = []
        self.food = []
        self.score = 0
        self.create_food()

    def create_food(self):
        """Create a new piece of food at a random position."""
        pos = vector(random.randint(-5, 5), random.randint(-5, 5), 0)
        food = sphere(pos=pos, radius=0.5, color=color.green)
        self.food.append(food)

    def add_player(self, player):
        """Add a player to the game."""
        self.players.append(player)

    def update(self):
        """Update the game state."""
        for player in self.players:
            # Check for collision with food
            for food in self.food:
                if utils.distance(player.head.pos, food.pos) < player.head.radius:
                    self.food.remove(food)
                    food.visible = False
                    self.score += 1
                    player.grow()

            player.move()

            # Check for collision with other players
            for other in self.players:
                if player != other and utils.distance(player.head.pos, other.head.pos) < player.head.radius + other.head.radius:
                    player.die()

        # Create new food if there are less than 10 pieces remaining
        if len(self.food) < 10:
            self.create_food()


gm = GameManager()
gm.add_player(Player(vector.random(), color.red))
gm.add_player(Player(vector.random(), color.red))
gm.add_player(Player(vector.random(), color.red))


while True:
    rate(8)
    gm.update()