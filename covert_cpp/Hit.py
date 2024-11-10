# Hit.py
from Vector import Vector

class Hit:
    def __init__(self, source=Vector(), d=Vector(), t=-1.0, object=None):
        self.source = source
        self.d = d
        self.t = t
        self.object = object

    def hit_point(self):
        return self.source + self.d * self.t
