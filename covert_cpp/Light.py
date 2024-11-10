# Light.py
from Vector import Vector
from Color import Color

class Light:
    def __init__(self, position=Vector(), ambient=Color(), diffuse=Color(), specular=Color()):
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
