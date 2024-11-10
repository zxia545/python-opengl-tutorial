# Color.py

class Color:
    def __init__(self, r=0.0, g=0.0, b=0.0):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def __mul__(self, other):
        if isinstance(other, Color):
            return Color(self.r * other.r, self.g * other.g, self.b * other.b)
        elif isinstance(other, (int, float)):
            return Color(self.r * other, self.g * other, self.b * other)
        else:
            raise NotImplementedError("Unsupported multiplication")

    __rmul__ = __mul__

    def clamp(self):
        self.r = min(max(self.r, 0.0), 1.0)
        self.g = min(max(self.g, 0.0), 1.0)
        self.b = min(max(self.b, 0.0), 1.0)
        return self

    def to_tuple(self):
        return (self.r, self.g, self.b)
