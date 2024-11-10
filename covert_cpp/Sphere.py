# Sphere.py
from SceneObject import SceneObject
from Vector import Vector
from Hit import Hit
from math import sqrt

class Sphere(SceneObject):
    def __init__(self, center=Vector(0,0,0), radius=1.0):
        super().__init__()
        self.center = center
        self.radius = radius

    def intersect(self, source, d):
        oc = source - self.center
        A = d.dot(d)
        B = 2.0 * oc.dot(d)
        C = oc.dot(oc) - self.radius ** 2

        discriminant = B * B - 4 * A * C
        if discriminant < 0:
            return -1.0

        sqrt_disc = sqrt(discriminant)
        if B > 0:
            t1 = (-B - sqrt_disc) / (2 * A)
        else:
            t1 = (-B + sqrt_disc) / (2 * A)

        t2 = C / (A * t1) if t1 != 0 else -1.0

        t = t1 if t1 < t2 else t2
        return t if t > 1e-5 else -1.0

    def normal(self, p):
        return (p - self.center).normalize()
