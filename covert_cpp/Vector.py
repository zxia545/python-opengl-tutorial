# Vector.py
import numpy as np

class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.coords = np.array([x, y, z], dtype=float)

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def z(self):
        return self.coords[2]

    def dot(self, other):
        return np.dot(self.coords, other.coords)

    def __add__(self, other):
        return Vector(*(self.coords + other.coords))

    def __sub__(self, other):
        return Vector(*(self.coords - other.coords))

    def __mul__(self, scalar):
        return Vector(*(self.coords * scalar))

    def normalize(self):
        norm = np.linalg.norm(self.coords)
        if norm == 0:
            return Vector(*self.coords)
        return Vector(*(self.coords / norm))

    def __eq__(self, other):
        return np.allclose(self.coords, other.coords, atol=1e-4)
