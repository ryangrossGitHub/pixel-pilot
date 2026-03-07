class Particle:
    def __init__(self, x, y, x_speed, y_speed, color, life):
        self._x = x
        self._y = y
        self._x_speed = x_speed
        self._y_speed = y_speed
        self._color = color
        self._life = life

    def update(self):
        self._x += self._x_speed
        self._y += self._y_speed
        self._life -= 1

    def get_life(self):
        return self._life
    
    def get_position_and_color(self):
        return (self._x, self._y, self._color)