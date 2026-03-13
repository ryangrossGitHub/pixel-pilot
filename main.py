import pyxel

from fighter import Fighter

class App:
    def __init__(self):
        self.player = Fighter(64, 64)
        self.screen_width = 480
        self.screen_height = 270
        self.background_y = 0
        self.background_scroll_speed = 1

        pyxel.init(self.screen_width, self.screen_height, title="Pixel Pilot", fps=60)
        pyxel.load("sprites.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.background_y = (self.background_y + self.background_scroll_speed) % self.screen_height # Loop background every 16 pixels for seamless scrolling
        self.player.handle_movement(self.screen_width, self.screen_height)
        
        if (pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A)):
            self.player.shoot_gun(self.screen_height)
        
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
        pyxel.cls(0)
        
        self.background_scroll_speed = 15 + -1 *self.player.get_y_acceleration()*2 # Sync background scroll speed with player state
        if self.background_scroll_speed < 0.5:
            self.background_scroll_speed = 0.5
        
        self.draw_background()
        pyxel.blt(*self.player.blt()) # * to unpack the tuple returned by blt()

        for particle in self.player.get_boost_particles():
            pyxel.pset(*particle.get_position_and_color())

        for particle in self.player.get_gun_particles():
            pyxel.pset(*particle.get_position_and_color())

    def draw_background(self):
        pyxel.bltm(0, self.background_y, 0, 0, 0, self.screen_width, self.screen_height)

        # Second bltm to create seamless scrolling effect when background_y > 0
        pyxel.bltm(0, self.background_y-self.screen_height+2, 0, 0, 0, self.screen_width, self.screen_height)
App()

