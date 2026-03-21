import pyxel
import random

from particle import Particle

class Enemy:
    def __init__(self):
        self._x = 0 # enemies are loaded at startup so location doesn't matter
        self._y = 0 # enemies are loaded at startup so location doesn't matter
        self._sprite = 0 # image bank
        self._u = 112
        self._v = 0
        self._w = 16
        self._h = 16
        self._y_speed = 0.2
        self._transparent_color = 1
        self._explosion_particles = []
        self._alive = False # enemies are loaded at startup so start "dead"
        self._spawn_location = None

    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def get_h(self):
        return self._h
    
    def get_w(self):
        return self._w
    
    def get_spawn_location(self):
        return self._spawn_location

    def handle_movement(self, level, screen_width, screen_height):
        if self.is_exploding():
            self._update_explosion()

        if self._alive:
            if level >= 1:
                self.handle_movement_lvl_1(screen_width, screen_height)

    # Simple downward drift, no side to side
    def handle_movement_lvl_1(self, screen_width, screen_height):
        if self._y < 20:
            self._y += self._y_speed
        elif self._y + self._h > screen_height - 20:
            self._y -= self._y_speed

    def hit(self):
        self._alive = False
        for i in range(150):
            self._explosion_particles.append(Particle(
                    x=self._x + 8, # expolosion at middle of plane body
                    y=self._y + 8, # expolosion at middle of plane body
                    x_speed=(random.random() * 4) * (random.random() - 0.5), # Random horizontal speed for spread
                    y_speed=random.uniform(-1, 1) * 2, # Upwards speed with some variation
                    color=random.choice([3, 11, 0]), # enemy colors
                    life=random.randint(80, 120) # frames
            ))

    def is_exploding(self):
        if len(self._explosion_particles) > 0:
            return True
        else:
            return False

    def is_alive(self):
        return self._alive
    
    def spawn(self, direction, screen_width, screen_height):
        self._alive = True
        self._spawn_location = direction
        self._x = random.randint(0, screen_width - self._w)

        # We want the plan to start out of view and drift into view
        if direction == "top":
            self._y = -self._h
        else:
            self._y = screen_height

    def _update_explosion(self):
        # Update existing particles
        for particle in self._explosion_particles:
            particle.update()

        # Remove particles that have expired
        self._explosion_particles = [p for p in self._explosion_particles if p.get_life() > 0]

    def get_explosion_particles(self):
        return self._explosion_particles

    def blt(self):
        return self._x, self._y, self._sprite, self._u, self._v, self._w, self._h, self._transparent_color