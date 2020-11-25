import math


class Particle(object):

    def __init__(self, position, mass, velocity):
        self.position = position
        self.mass = mass
        self.velocity = velocity

        self.speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        self.momentum = self.mass * self.speed

        self.points = None
