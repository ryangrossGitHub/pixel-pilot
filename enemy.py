import pyxel
import random

from particle import Particle

class Enemy:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._sprite = 0 # image bank
        self._u = 112
        self._v = 0
        self._w = 16
        self._h = 16
        self._transparent_color = 1
        self._explosion_particles = []
        self._alive = True

    def hit(self):
        for i in range(200):
            self._explosion_particles.append(Particle(
                    x=self._x + 8, # expolosion at middle of plane body
                    y=self._y + 8, # expolosion at middle of plane body
                    x_speed=(random.random() * 4) * (random.random() - 0.5), # Random horizontal speed for spread
                    y_speed=random.uniform(-1, 1) * 2, # Upwards speed with some variation
                    color=random.choice([3, 11, 0]), # enemy colors
                    life=random.randint(80, 120) # frames
            ))

    def update_explosion(self):
        # Update existing particles
        for particle in self._explosion_particles:
            particle.update()

        # Remove particles that have expired
        self._explosion_particles = [p for p in self._explosion_particles if p.get_life() > 0]

    def get_explosion_particles(self):
        return self._explosion_particles

    def blt(self):
        return self._x, self._y, self._sprite, self._u, self._v, self._w, self._h, self._transparent_color