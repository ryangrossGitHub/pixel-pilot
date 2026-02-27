class Fighter:
    def __init__(self, x, y):
        self._sprite = 0 # image bank index
        self._transparent_color = 1 # dark blue
        self.img_default() # set initial image
        self._x = x
        self._y = y
        self._speed = 0.3
        self._x_acceleration = 0 # positive means move right, negative means move left

    def left(self):
        if self._x_acceleration > 0:
            self.img_bank_left_hard()
        else:
            self.img_bank_left()

        if self._x_acceleration > -4:
            self._x_acceleration -= self._speed

    def right(self):
        if self._x_acceleration < 0:
            self.img_bank_right_hard()
        else:
            self.img_bank_right()

        if self._x_acceleration < 4:
            self._x_acceleration += self._speed

    def handle_movement(self):
        if self._x_acceleration < 2.5 and self._x_acceleration > -2.5:
            self.img_default()
        elif self._x_acceleration > 2.5 and self._x_acceleration < 3:
            self.img_bank_right()
        elif self._x_acceleration < -2.5 and self._x_acceleration > -3:
            self.img_bank_left()

        if self._x_acceleration > 1.1 or self._x_acceleration < -1.1:
            self._x += self._x_acceleration

    def apply_friction(self):
        # Apply friction to slow down the plane when not accelerating
        if self._x_acceleration < 0.05 and self._x_acceleration > -0.05:
            self._x_acceleration = 0
        elif self._x_acceleration > 0:
            self._x_acceleration -= 0.01
        elif self._x_acceleration < 0:
            self._x_acceleration += 0.01

        self.handle_movement()

    def img_default(self):
        self._u = 0
        self._v = 0
        self._w = 11
        self._h = 14

    def img_bank_left(self):
        self._u = 16
        self._v = 0
        self._w = 9
        self._h = 14

    def img_bank_left_hard(self):
        self._u = 44
        self._v = 0
        self._w = 10
        self._h = 24

    def img_bank_right(self):
        self._u = 32
        self._v = 0
        self._w = 9
        self._h = 14

    def img_bank_right_hard(self):
        self._u = 56
        self._v = 0
        self._w = 10
        self._h = 24

    def blt(self):
        return self._x, self._y, self._sprite, self._u, self._v, self._w, self._h, self._transparent_color