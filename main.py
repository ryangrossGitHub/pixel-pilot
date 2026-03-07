import pyxel

from fighter import Fighter

class App:
    def __init__(self):
        self.player = Fighter(64, 64)
        self.screen_width = 256
        self.screen_height = 240
        self.background_y = 0
        self.background_scroll_speed = 1

        pyxel.init(self.screen_width, self.screen_height, title="Pixel Pilot", fps=60)
        pyxel.load("sprites.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.background_y = (self.background_y + self.background_scroll_speed) % 8 # Loop background every 16 pixels for seamless scrolling
        self.player.handle_movement(self.screen_width, self.screen_height)
               
        # Prevent concurrent animation/special movements
        if ((pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)) and 
            (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP))):
            self.player.boost()
        elif ((pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)) and 
            (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN))):
            self.player.backflip()
        
        if ((pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)) and 
            (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT))):
            self.player.roll_left()
        elif ((pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)) and 
            (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT))):
            self.player.roll_right()
        
        # Prevent opposite inputs on x or y axis
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player.left()
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player.right()
        
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.player.up()
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.player.down()

    def draw(self):
        pyxel.cls(0)
        
        self.background_scroll_speed = 1.5 + -1 *self.player._y_acceleration/5 # Sync background scroll speed with player state
        if self.background_scroll_speed < 1.5:
            self.background_scroll_speed = 1.5
        
        self.draw_background()
        pyxel.blt(*self.player.blt()) # * to unpack the tuple returned by blt()

    def draw_background(self):
        pyxel.bltm(0, self.background_y, 0, 0, 0, self.screen_width, self.screen_height)

        # Second bltm to create seamless scrolling effect when background_y > 0
        pyxel.bltm(0, self.background_y-16, 0, 0, 0, self.screen_width, self.screen_height)
App()

