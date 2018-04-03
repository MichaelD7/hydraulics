import math

from abc import ABCMeta, abstractmethod

class FrictionLoss:
    __metaclass__ = ABCMeta
    g = 9.806   #gravitational constant
    precision = 0.0001
    MAX_ITER = 29

    @abstractmethod
    def frictionSlope(self, hydraulic_radius, velocity):
        pass

class DarcyWeisbach(FrictionLoss):
    def __init__(self, roughness, kinvisc):
        self.roughness = roughness
        self.kinvisc = kinvisc

    def colebrook_white(self, hydraulic_radius, velocity):
        """calculate colebrook-white friction factor.
        Start with guess value."""
        guess = 0.02  # change to approximation to c-w to reduce iteration
        dia = 4.0 * hydraulic_radius
        # Re = dia * vel_norm / self.kinvisc
        solution = False
        while not solution:
            friction = 0.25 * math.pow(math.log10(self.roughness / (3.7 * dia) +
                2.51 / (velocity * dia / self.kinvisc * math.sqrt(guess))),-2)
            if math.fabs(friction - guess) < FrictionLoss.precision:
                solution = True
            else:
                guess += (friction - guess) / 2.0
        return friction

    def frictionSlope(self, hydraulic_radius, velocity):
        friction_factor = self.colebrook_white(hydraulic_radius, velocity)
        friction_slope = friction_factor * velocity * velocity / (
            8.0 * FrictionLoss.g * hydraulic_radius)
        return friction_slope
