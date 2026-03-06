class Fighter:
    def __init__(self, x, y):
        self._sprite = 0 # image bank index
        self._transparent_color = 1 # dark blue (ocean)
        self.img_default() # set initial image
        self._x = x
        self._y = y
        self._x_speed = 0.4
        self._y_speed = 0.4
        self.background_scroll_speed = 1
        self._roll_speed = 7 # higher is slower
        self._flip_speed = 10 # higher is slower
        self._boot_animation_speed = 10 # higher is slower
        self._x_acceleration = 0 # positive means move right, negative means move left
        self._x_friction = 0.01 # how quickly the plane slows down when not accelerating
        self._y_acceleration = 0 # positive means move down, negative means move up
        self._y_friction = 0.02 # how quickly the plane slows down when not accelerating
        self._animation_in_progress = None # used to prevent input during certain animations (e.g. boost)
        self._animation_sequence = 0 # used to track which frame of an animation sequence we're on

    def left(self):
        if self._animation_in_progress is None:
            if self._x_acceleration > 0:
                self.img_bank_left_hard()
            else:
                self.img_bank_left()

            if self._x_acceleration > -5:
                self._x_acceleration -= self._x_speed

    def roll_left(self):
        if self._animation_in_progress is None:
            self._animation_in_progress = "ROLL_LEFT"
            self._animation_sequence = 0
        elif self._animation_in_progress == "ROLL_LEFT":
            if self._animation_sequence == self._roll_speed:
                self.img_bank_left()
            elif self._animation_sequence == self._roll_speed*2:
                self._x += 4 # compensate for center position of image
                self.img_barrel_roll_left_side()
            elif self._animation_sequence == self._roll_speed*3:
                self._x -= 4 # return to original x position
                self.img_barrel_roll_upside_down_left()
            elif self._animation_sequence == self._roll_speed*4:
                self.img_barrel_roll_upside_down()
            elif self._animation_sequence == self._roll_speed*5:
                self.img_barrel_roll_updside_down_right()
            elif self._animation_sequence == self._roll_speed*6:
                self._x += 4 # compensate for center position of image
                self.img_barrel_roll_right_side()
            elif self._animation_sequence == self._roll_speed*7:
                self._x -= 4 # return to original x position
                self.img_bank_right()
            elif self._animation_sequence == self._roll_speed*8:
                self.img_default()
                self._animation_in_progress = None

        self._animation_sequence += 1
        self._x -= 1

    def right(self):
        if self._animation_in_progress is None:
            if self._x_acceleration < 0:
                self.img_bank_right_hard()
            else:
                self.img_bank_right()

            if self._x_acceleration < 5:
                self._x_acceleration += self._x_speed

    def roll_right(self):
        if self._animation_in_progress is None:
            self._animation_in_progress = "ROLL_RIGHT"
            self._animation_sequence = 0
        elif self._animation_in_progress == "ROLL_RIGHT":
            if self._animation_sequence == self._roll_speed:
                self.img_bank_right()
            elif self._animation_sequence == self._roll_speed*2:
                self._x += 4 # compensate for center position of image
                self.img_barrel_roll_right_side()
            elif self._animation_sequence == self._roll_speed*3:
                self._x -= 4 # return to original x position
                self.img_barrel_roll_updside_down_right()
            elif self._animation_sequence == self._roll_speed*4:
                self.img_barrel_roll_upside_down()
            elif self._animation_sequence == self._roll_speed*5:
                self.img_barrel_roll_upside_down_left()
            elif self._animation_sequence == self._roll_speed*6:
                self._x += 4 # compensate for center position of image
                self.img_barrel_roll_left_side()
            elif self._animation_sequence == self._roll_speed*7:
                self._x -= 4 # return to original x position
                self.img_bank_left()
            elif self._animation_sequence == self._roll_speed*8:
                self.img_default()
                self._animation_in_progress = None

        self._animation_sequence += 1
        self._x += 1

    def up(self):
        if self._animation_in_progress is None:
            self.img_boost()

            if self._y_acceleration > -5:
                self._y_acceleration -= self._y_speed/2

    def boost(self):
        if self._animation_in_progress is None:
            self._animation_in_progress = "BOOST"
            self._animation_sequence = 0
            self.background_scroll_speed = 2
        elif self._animation_in_progress == "BOOST":
            if self._animation_sequence < self._boot_animation_speed:
                self.img_boost()
            elif self._animation_sequence == self._boot_animation_speed*2:
                self.img_boost_hard1()
            elif self._animation_sequence == self._boot_animation_speed*3:
                self.img_boost_hard2()
            elif self._animation_sequence == self._boot_animation_speed*4:
                self._x -= 8 # image is wider than default, so move it left to keep it centered on the plane
                self.img_boost_hard3()
            elif self._animation_sequence == self._boot_animation_speed*5:
                self._x += 8 # move back to original x position
                self.img_boost_hard4()
            elif self._animation_sequence == self._boot_animation_speed*7:
                self._animation_in_progress = None
                self.background_scroll_speed = 1
                self.img_default()

        self._animation_sequence += 1
        self._y -= 2

    def down(self):
        if self._animation_in_progress is None:
            if self._y_acceleration < 5:
                self._y_acceleration += self._y_speed

    def backflip(self):
        if self._animation_in_progress is None:
            self._animation_in_progress = "BACKFLIP"
            self._animation_sequence = 0
            self.background_scroll_speed = 0.5
        elif self._animation_in_progress == "BACKFLIP":
            if self._animation_sequence < self._flip_speed:
                self.img_backflip1()
            elif self._animation_sequence < self._flip_speed*2:
                self.img_backflip2()
            elif self._animation_sequence < self._flip_speed*3:
                self.img_backflip3()
            elif self._animation_sequence < self._flip_speed*4:
                self.img_backflip4()
            elif self._animation_sequence < self._flip_speed*5:
                self.img_backflip5()
            elif self._animation_sequence < self._flip_speed*6:
                self.img_backflip6()
            elif self._animation_sequence < self._flip_speed*7:
                self.img_backflip7()
            else:
                self._animation_in_progress = None
                self.background_scroll_speed = 1
                self.img_default()

        self._animation_sequence += 1
        self._y += 2

    def handle_movement(self, screen_width, screen_height):
        self._apply_friction()

        if self._animation_in_progress == "BOOST":
            self.boost()
        elif self._animation_in_progress == "BACKFLIP":
            self.backflip()
        elif self._animation_in_progress == "ROLL_LEFT":
            self.roll_left()
        elif self._animation_in_progress == "ROLL_RIGHT":
            self.roll_right()
        elif self._x_acceleration < 2.5 and self._x_acceleration > -2.5:
            self.img_default()
        elif self._x_acceleration > 2.5 and self._x_acceleration < 3:
            self.img_bank_right()
        elif self._x_acceleration < -2.5 and self._x_acceleration > -3:
            self.img_bank_left()

        if self._x_acceleration > 1.1 or self._x_acceleration < -1.1:
            self._x += self._x_acceleration

        if self._y_acceleration > 1.1 or self._y_acceleration < -1.1:
            self._y += self._y_acceleration

        # Keep the plane within the screen bounds
        if self._x < 0:
            self._x = 0
            self._x_acceleration = 0
        elif self._x > screen_width - self._w:
            self._x = screen_width - self._w
            self._x_acceleration = 0

        if self._y < 0:
            self._y = 0
        elif self._y > screen_height - self._h:
            self._y = screen_height - self._h

    def _apply_friction(self):
        # Apply friction to slow down the plane when not accelerating
        if self._x_acceleration < 0.05 and self._x_acceleration > -0.05:
            self._x_acceleration = 0
        elif self._x_acceleration > 0:
            self._x_acceleration -= self._x_friction
        elif self._x_acceleration < 0:
            self._x_acceleration += self._x_friction

        if self._y_acceleration < 0.05 and self._y_acceleration > -0.05:
            self._y_acceleration = 0
        elif self._y_acceleration > 0:
            self._y_acceleration -= self._y_friction
        elif self._y_acceleration < 0:
            self._y_acceleration += self._y_friction

    def img_default(self):
        self._u = 0
        self._v = 0
        self._w = 16
        self._h = 14

    def img_bank_left(self):
        self._u = 16
        self._v = 0
        self._w = 16
        self._h = 14

    def img_bank_left_hard(self):
        self._u = 44
        self._v = 0
        self._w = 10
        self._h = 24

    def img_bank_right(self):
        self._u = 32
        self._v = 0
        self._w = 16
        self._h = 14

    def img_bank_right_hard(self):
        self._u = 56
        self._v = 0
        self._w = 10
        self._h = 24

    def img_barrel_roll_left_side(self):
        self._u = 0
        self._v = 24
        self._w = 7
        self._h = 14

    def img_barrel_roll_right_side(self):
        self._u = 9
        self._v = 24
        self._w = 7
        self._h = 14

    def img_barrel_roll_upside_down_left(self):
        self._u = 16
        self._v = 24
        self._w = 16
        self._h = 14

    def img_barrel_roll_updside_down_right(self):
        self._u = 32
        self._v = 24
        self._w = 16
        self._h = 14

    def img_barrel_roll_upside_down(self):
        self._u = 48
        self._v = 24
        self._w = 16
        self._h = 14

    def img_boost(self):
        self._u = 0
        self._v = 40
        self._w = 16
        self._h = 20

    def img_boost_hard1(self):
        self._u = 16
        self._v = 40
        self._w = 16
        self._h = 24

    def img_boost_hard2(self):
        self._u = 32
        self._v = 40
        self._w = 16
        self._h = 24

    def img_boost_hard3(self):
        self._u = 8
        self._v = 64
        self._w = 32
        self._h = 24

    def img_boost_hard4(self):
        self._u = 48
        self._v = 40
        self._w = 16
        self._h = 24

    def img_backflip1(self):
        self._u = 48
        self._v = 72
        self._w = 16
        self._h = 10

    def img_backflip2(self):
        self._u = 0
        self._v = 88
        self._w = 16
        self._h = 6

    def img_backflip3(self):
        self._u = 0
        self._v = 94
        self._w = 16
        self._h = 10

    def img_backflip4(self):
        self._u = 16
        self._v = 88
        self._w = 16
        self._h = 14

    def img_backflip5(self):
        self._u = 32
        self._v = 88
        self._w = 16
        self._h = 10

    def img_backflip6(self):
        self._u = 32
        self._v = 98
        self._w = 16
        self._h = 6

    def img_backflip7(self):
        self._u = 48
        self._v = 88
        self._w = 11
        self._h = 10

    def blt(self):
        return self._x, self._y, self._sprite, self._u, self._v, self._w, self._h, self._transparent_color