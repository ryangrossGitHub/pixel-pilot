import pyxel
import random

from fighter import Fighter
from particle import Particle
from enemy import Enemy

class App:
    def __init__(self):
        self.screen_width = 480
        self.screen_height = 270
        self.player = Fighter(self.screen_width//2, self.screen_height-40, -2)
        self.background_y = 0
        self.background_scroll_speed = 1
        self.started = False
        self.paused = False
        self.runway_position_y = self.screen_height - 80
        self.level = 1
        self.enemies = []
        self.enemies_alive = 0

        pyxel.init(self.screen_width, self.screen_height, title="Pixel Pilot", fps=60)
        pyxel.load("sprites.pyxres")

        # Load enemies up front and recycle them for better performance
        for i in range(5):
            self.enemies.append(Enemy())

        pyxel.playm(1, 0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.started:
            self.update_start_screen()
            return
        
        if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            self.paused = not self.paused

        if self.paused:
            return
        
        if self.level == 1:
            desired_enemy_count = 1
            for enemy in self.enemies:
                needed_enemy_spawn_count = desired_enemy_count - self.enemies_alive
                if needed_enemy_spawn_count > 0: 
                    if not enemy.is_alive() and not enemy.is_exploding(): # find "dead" enemies that can be recycled
                        enemy.spawn("TOP", self.screen_width, self.screen_height)
                        self.enemies_alive += 1
                else:
                    break

        self.update_background()
        self.player.handle_movement(self.screen_width, self.screen_height)
        
        for enemy in self.enemies:
            enemy.handle_movement(self.level)

        self.update_missiles()

        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER):
            self.player.shoot(self.screen_height)
            # self.player.shoot_gun(self.screen_height)
        # elif (pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_B)) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER):
        #     self.player.reset_gun_burst()
        
        if (pyxel.btn(pyxel.KEY_SHIFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER):
            self.player.flares()
        elif (pyxel.btnr(pyxel.KEY_SHIFT) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A)) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER):
            self.player.reset_flares()

        # Allow simultaneous vertical and horizontal input without blocking each other
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player.left()
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player.right()
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.player.up()
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.player.down()

    def draw(self):
        if not self.started:
            self.draw_start_screen()
            return
        
        if self.paused:
            return
        
        pyxel.cls(0)

        self.background_scroll_speed = 17 + -1 *self.player.get_y_acceleration()*1.5 # Sync background scroll speed with player state
        if self.background_scroll_speed < 0.5:
            self.background_scroll_speed = 0.5
        
        self.draw_background()

        if self.runway_position_y < self.screen_height:
            self.runway_position_y = self.runway_position_y * 1.01
            self.draw_carrier(self.runway_position_y)

        for particle in self.player.get_boost_particles():
            pyxel.pset(*particle.get_position_and_color())

        for particle in self.player.get_flare_particles():
            pyxel.pset(*particle.get_position_and_color())

        for particle in self.player.get_gun_particles():
            pyxel.pset(*particle.get_position_and_color())

        for particle in self.player.get_missile_particles():
            self.draw_missile(particle.get_x(), particle.get_y())
        
        for enemy in self.enemies:
            if enemy.is_alive():
                self.draw_enemy(enemy)
            elif enemy.is_exploding():
                for particle in enemy.get_explosion_particles():
                    pyxel.pset(*particle.get_position_and_color())
        
        self.draw_player() # draw player last to ensure it is always on top

    def draw_player(self):
        pyxel.blt(*self.player.blt()) # * to unpack the tuple returned by blt()

    def draw_enemy(self, enemy):
        pyxel.blt(*enemy.blt())

    def draw_missile(self, x, y):
        pyxel.blt(x, y, 0, 96, 0, 3, 6)

    def update_missiles(self):
        for particle in self.player.get_missile_particles():
            mx = particle.get_x()
            my = particle.get_y()

            for enemy in self.enemies:
                if enemy.is_alive():
                    if ((mx > enemy.get_x() and mx < enemy.get_x() + enemy.get_w()) and
                        (my > enemy.get_y() and my < enemy.get_y() + enemy.get_h())):
                        pyxel.play(3, 4)
                        particle.end_life()
                        enemy.hit()
                        self.enemies_alive -= 1
                        break

    def update_background(self):
        self.background_y = (self.background_y + self.background_scroll_speed) % self.screen_height # Loop background every 16 pixels for seamless scrolling

    def draw_background(self):
        pyxel.bltm(0, self.background_y, 0, 0, 0, self.screen_width, self.screen_height)

        # Second bltm to create seamless scrolling effect when background_y > 0
        pyxel.bltm(0, self.background_y-self.screen_height+2, 0, 0, 0, self.screen_width, self.screen_height)

    def draw_start_screen(self):
        pyxel.cls(1)
        self.update_background()
        self.draw_background()
        self.draw_carrier(self.runway_position_y)
        pyxel.text(self.screen_width//2 - 15, self.screen_height//2 - 50, "PIXEL PILOT", 9)
        pyxel.text(self.screen_width//2 - 50, self.screen_height//2 - 30, "CONTROLS: MOVE|SHOOT|FLARES|PAUSE", 7)
        pyxel.text(self.screen_width//2 - 50, self.screen_height//2 - 20, "KEYBOARD: ARROW KEYS|SPACE|SHIFT|P", 7)
        pyxel.text(self.screen_width//2 - 50, self.screen_height//2 - 10, "CONTROLLER: DPAD|A|B|START", 7)
        pyxel.text(self.screen_width//2 - 25, self.screen_height//2 + 10, "PRESS UP TO FLY!!!", 8)
        pyxel.blt(*self.player.blt()) # * to unpack the tuple returned by blt()

    def update_start_screen(self):
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
            pyxel.stop()
            self.started = True

    def draw_carrier(self, y):
        pyxel.blt(self.screen_width//2-24, y, 0, 0, 16, 56, 80, 1)

App()