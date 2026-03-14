import random
import pyxel

from particle import Particle

class Fighter:
    def __init__(self, x, y):
        self._sprite = 0 # image bank index
        self._transparent_color = 1 # dark blue (ocean)
        self.img_default() # set initial image
        self._x = x
        self._y = y
        self._w = 16
        self._h = 16
        self._y_margin = 20 # buffer space between plane and screen edges on y axis
        self._x_speed = 0.4
        self._y_speed = 0.4
        self._roll_speed = 10 # higher is slower
        self._boot_animation_speed = 10 # higher is slower
        self._x_acceleration = 0 # positive means move right, negative means move left
        self._y_acceleration = 0 # positive means move down, negative means move up
        self._y_friction = 0.1 # how quickly the plane slows down when not accelerating
        self._animation_in_progress = None # used to prevent input during certain animations (e.g. boost)
        self._animation_sequence = 0 # used to track which frame of an animation sequence we're on
        self._boost_particles = []
        self._gun_particles = []
        self._gun_burst_max = 10
        self._gun_burst_count = 0 # Track how many shots have been fired in the current burst
        self._missile_particles = []

    def get_animation_in_progress(self):
        return self._animation_in_progress

    def get_y_acceleration(self):
        return self._y_acceleration

    def left(self):
        if self._animation_in_progress is None:
            if self._x_acceleration < -4:
                self.roll_left()
            else:
                self.img_roll_left()

        if self._x_acceleration > -5:
            self._x_acceleration -= self._x_speed

    def roll_left(self):
        if self._animation_in_progress is None:
            self._animation_in_progress = "ROLL_LEFT"
            self._animation_sequence = 0
        elif self._animation_in_progress == "ROLL_LEFT":
            if self._animation_sequence == self._roll_speed:
                self.img_roll_left()
            elif self._animation_sequence == self._roll_speed*2:
                self.img_roll_upside_down()
            elif self._animation_sequence == self._roll_speed*3:
                self.img_roll_right()
            elif self._animation_sequence >= self._roll_speed*4:
                self.img_default()
                self._animation_in_progress = None

        self._animation_sequence += 1
        self._x -= 0.5

    def right(self):
        if self._animation_in_progress is None:
            if self._x_acceleration > 4:
                self.roll_right()
            else:
                self.img_roll_right()

        if self._x_acceleration < 5:
            self._x_acceleration += self._x_speed

    def roll_right(self):
        if self._animation_in_progress is None:
            self._animation_in_progress = "ROLL_RIGHT"
            self._animation_sequence = 0
        elif self._animation_in_progress == "ROLL_RIGHT":
            if self._animation_sequence == self._roll_speed:
                self.img_roll_right()
            elif self._animation_sequence == self._roll_speed*2:
                self.img_roll_upside_down()
            elif self._animation_sequence == self._roll_speed*3:
                self.img_roll_left()
            elif self._animation_sequence >= self._roll_speed*4:
                self.img_default()
                self._animation_in_progress = None

        self._animation_sequence += 1
        self._x += 0.5

    def up(self):
        if self._y_acceleration > -5:
            self._y_acceleration -= self._y_speed/1.5 # slower vert accel to sim air friction

    def down(self):
        if self._y_acceleration < 5:
            self._y_acceleration += self._y_speed

    def handle_movement(self, screen_width, screen_height):
        self._apply_friction()

        if self._animation_in_progress == "ROLL_LEFT":
            self.roll_left()
        elif self._animation_in_progress == "ROLL_RIGHT":
            self.roll_right()
        else:
            self.img_default()

        if self._x_acceleration > 1.1 or self._x_acceleration < -1.1:
            self._x += self._x_acceleration

        self._y += self._y_acceleration

        # Keep the plane within the screen bounds
        if self._x < 0:
            self._x = 0
            self._x_acceleration = 0
        elif self._x > screen_width - self._w:
            self._x = screen_width - self._w
            self._x_acceleration = 0

        # Add margin for y
        if self._y < self._y_margin:
            self._y = self._y_margin
        elif self._y > screen_height - self._h - self._y_margin:
            self._y = screen_height - self._h - self._y_margin

        self._update_boost_particles()
        self._update_gun_particles()
        self._update_missile_particles()

    def _apply_friction(self):
        if self._y_acceleration < -0.2:
            self._y_acceleration += self._y_friction

    def _update_boost_particles(self):
        # Update existing particles
        for particle in self._boost_particles:
            particle.update()

        # Remove particles that have expired
        self._boost_particles = [p for p in self._boost_particles if p.get_life() > 0]

        # Add new particles based on current acceleration
        if self._y_acceleration <= 0: # Only show boost particles when accelerating upwards
            for i in range(3 + int(self._y_acceleration*-1)): # More particles for higher acceleration
                self._boost_particles.append(Particle(
                    x=self._x + self._w/2 - 1,
                    y=self._y + self._h,
                    x_speed=(0.3+self._y_acceleration/5) * (random.random() - 0.5), # Random horizontal speed for spread
                    y_speed=-self._y_acceleration/4 + 0.5, # Base speed plus some variation based on acceleration
                    color=random.choice([9,10]), # yellow and orange
                    life=random.randint(10, 35) # frames
                ))

    def get_boost_particles(self):
        return self._boost_particles
    
    def shoot_gun(self, screen_height):
        if self._gun_burst_count < self._gun_burst_max:
            pyxel.play(0, 0)
            self._gun_particles.append(Particle(
                x=self._x + self._w/2 - 1,
                y=self._y,
                x_speed=0,
                y_speed=-5, # Upwards speed with some variation
                color=7, # white
                life=screen_height # frames
            ))

            self._gun_burst_count += 1

    def reset_gun_burst(self):
        self._gun_burst_count = 0

    def _update_gun_particles(self):
        # Update existing particles
        for particle in self._gun_particles:
            particle.update()

        # Remove particles that have expired
        self._gun_particles = [p for p in self._gun_particles if p.get_life() > 0]

    def get_gun_particles(self):
        return self._gun_particles
    
    def shoot_missile(self, screen_height):
        pyxel.play(0, 1)
        self._missile_particles.append(Particle(
            x=self._x + self._w/2 - 1,
            y=self._y,
            x_speed=0,
            y_speed=-5, 
            color=0, # doesn't matter because will be drawn from sprite
            life=screen_height
        ))

    def _update_missile_particles(self):
        # Update existing particles
        for particle in self._missile_particles:
            particle.update()

        # Remove particles that have expired
        self._missile_particles = [p for p in self._missile_particles if p.get_life() > 0]

    def get_missile_particles(self):
        return self._missile_particles

    def img_default(self):
        self._u = 0
        self._v = 0

    def img_roll_left(self):
        self._u = 16
        self._v = 0

    def img_roll_upside_down(self):
        self._u = 32
        self._v = 0

    def img_roll_right(self):
        self._u = 48
        self._v = 0
        
    def blt(self):
        return self._x, self._y, self._sprite, self._u, self._v, self._w, self._h, self._transparent_color