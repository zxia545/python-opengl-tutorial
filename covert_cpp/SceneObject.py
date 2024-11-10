# SceneObject.py
from Color import Color
from Vector import Vector

class SceneObject:
    def __init__(self):
        self.ambient = Color()
        self.diffuse = Color()
        self.specular = Color()
        self.shininess = 0
        self.reflectivity = 0.0

    def intersect(self, source, d):
        raise NotImplementedError

    def normal(self, p):
        raise NotImplementedError
