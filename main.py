import pyxel

from fighter import Fighter

class App:
    def __init__(self):
        self.player = Fighter(64, 64)

        pyxel.init(256, 256, title="Pixel Pilot", fps=60)
        pyxel.load("sprites.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.apply_friction()
        
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player.left()
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player.right()
            
        # if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
        #     self.player.y -= self.player.speed
        # elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
        #     self.player.y += self.player.speed

    def draw(self):
        pyxel.cls(0)
        self.draw_background()
        pyxel.blt(*self.player.blt()) # * to unpack the tuple returned by blt()

    def draw_background(self):
        pyxel.bltm(0, 0, 0, 0, 0, 256, 256)
App()

