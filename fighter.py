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

        if self._x_acceleration > -5:
            self._x_acceleration -= self._speed

    def right(self):
        if self._x_acceleration < 0:
            self.img_bank_right_hard()
        else:
            self.img_bank_right()

        if self._x_acceleration < 5:
            self._x_acceleration += self._speed

    def up(self):
        self.img_boost()
        self._y -= self._speed * 8

    def down(self):
        self._y += self._speed * 10

    def handle_movement(self, screen_width, screen_height):
        self._apply_friction()

        if self._x_acceleration < 2.5 and self._x_acceleration > -2.5:
            self.img_default()
        elif self._x_acceleration > 2.5 and self._x_acceleration < 3:
            self.img_bank_right()
        elif self._x_acceleration < -2.5 and self._x_acceleration > -3:
            self.img_bank_left()

        if self._x_acceleration > 1.1 or self._x_acceleration < -1.1:
            self._x += self._x_acceleration

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
            self._x_acceleration -= 0.01
        elif self._x_acceleration < 0:
            self._x_acceleration += 0.01

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

    def img_boost(self):
        self._u = 0
        self._v = 40
        self._w = 11
        self._h = 19

    def blt(self):
        return self._x, self._y, self._sprite, self._u, self._v, self._w, self._h, self._transparent_color