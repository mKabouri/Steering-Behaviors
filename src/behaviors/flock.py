from behaviors.base_particule import Particule

class FlockingBehavior(Particule):
    def __init__(self, coordinate, velocity, acceleration, targets):
        super().__init__(coordinate, velocity, acceleration, targets)

    def particule_behavior(self):
        pass
