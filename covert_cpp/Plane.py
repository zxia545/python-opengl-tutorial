# Plane.py
from SceneObject import SceneObject
from Vector import Vector

class Plane(SceneObject):
    def __init__(self, n=Vector(0,1,0), a=0.0):
        super().__init__()
        self.n = n.normalize()
        self.a = a

    def intersect(self, source, d):
        dn = d.dot(self.n)
        if abs(dn) < 1e-6:
            return -1.0  # Parallel, no intersection
        t = (self.a - source.dot(self.n)) / dn
        return t if t > 1e-5 else -1.0

    def normal(self, p):
        return self.n
