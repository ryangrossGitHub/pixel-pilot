import pyxel

from fighter import Fighter

class App:
    def __init__(self):
        self.screen_width = 480
        self.screen_height = 270
        self.player = Fighter(self.screen_width//2, self.screen_height-40, -2)
        self.background_y = 0
        self.background_scroll_speed = 1
        self.game_started = False
        self.game_paused = False
        self.runway_position_y = self.screen_height - 80

        pyxel.init(self.screen_width, self.screen_height, title="Pixel Pilot", fps=60)
        pyxel.load("sprites.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.game_started:
            self.update_start_screen()
            return
        
        if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            self.game_paused = not self.game_paused

        if self.game_paused:
            return
        
        self.update_background()
        self.player.handle_movement(self.screen_width, self.screen_height)

        if (pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER):
            self.player.shoot_gun(self.screen_height)
        elif (pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_B)) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER):
            self.player.reset_gun_burst()
        
        if (pyxel.btnp(pyxel.KEY_SHIFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER):
            # self.player.shoot_missile(self.screen_height)
            self.player.fire_flares()

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
        if not self.game_started:
            self.draw_start_screen()
            return
        
        if self.game_paused:
            return
        
        pyxel.cls(0)

        self.background_scroll_speed = 17 + -1 *self.player.get_y_acceleration()*1.5 # Sync background scroll speed with player state
        if self.background_scroll_speed < 0.5:
            self.background_scroll_speed = 0.5
        
        self.draw_background()

        if self.runway_position_y < self.screen_height:
            self.runway_position_y = self.runway_position_y * 1.01
            self.draw_carrier(self.runway_position_y)

        pyxel.blt(*self.player.blt()) # * to unpack the tuple returned by blt()

        for particle in self.player.get_boost_particles():
            pyxel.pset(*particle.get_position_and_color())

        for particle in self.player.get_flare_particles():
            pyxel.pset(*particle.get_position_and_color())

        for particle in self.player.get_gun_particles():
            pyxel.pset(*particle.get_position_and_color())

        for particle in self.player.get_missile_particles():
            pyxel.blt(particle.get_x(), particle.get_y(), 0, 0, 16, 1, 3)

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
        pyxel.text(self.screen_width//2 - 50, self.screen_height//2 - 30, "CONTROLS: MOVE|FIRE|FLARES|PAUSE", 7)
        pyxel.text(self.screen_width//2 - 50, self.screen_height//2 - 20, "KEYBOARD: ARROW KEYS|SPACE|SHIFT|P", 7)
        pyxel.text(self.screen_width//2 - 50, self.screen_height//2 - 10, "CONTROLLER: DPAD|A|B|START", 7)
        pyxel.text(self.screen_width//2 - 25, self.screen_height//2 + 10, "PRESS UP TO FLY!!!", 8)
        pyxel.blt(*self.player.blt()) # * to unpack the tuple returned by blt()

    def update_start_screen(self):
        if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
            self.game_started = True

    def draw_carrier(self, y):
        pyxel.blt(self.screen_width//2-24, y, 0, 0, 16, 56, 80, 1)

App()