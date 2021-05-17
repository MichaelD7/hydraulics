import math

from abc import ABCMeta, abstractmethod


class FrictionLoss:
    __metaclass__ = ABCMeta
    g = 9.806   # gravitational constant
    precision = 0.0001
    MAX_ITER = 29

    @abstractmethod
    def frictionSlope(self, area, perimeter, velocity):
        pass

#    @abstractmethod
#    def friction_factor(self, hydraulic_radius, velocity):
#        pass

    @abstractmethod
    def flowRate(self, slope, area, perimeter, velocity):
        pass


class DarcyWeisbach(FrictionLoss):
    def __init__(self, roughness, kinvisc):
        self.roughness = roughness
        self.kinvisc = kinvisc

    def friction_factor(self, hydraulic_radius, velocity):
        """calculate colebrook-white friction factor.
        Start with guess value."""
        guess = 0.02  # change to approximation to c-w to reduce iteration
        dia = 4.0 * hydraulic_radius
        # Re = dia * vel_norm / self.kinvisc
        solution = False
        while not solution:
            friction = 0.25 * math.pow(math.log10(self.roughness /
                                       (3.7 * dia) + 2.51 /
                                       (velocity * dia / self.kinvisc *
                                        math.sqrt(guess))), -2)
            if math.fabs(friction - guess) < FrictionLoss.precision:
                solution = True
            else:
                guess += (friction - guess) / 2.0
        return friction

    def frictionSlope(self, area, perimeter, velocity):
        hydraulic_radius = area / perimeter
        frictionFactor = self.friction_factor(hydraulic_radius, velocity)
        friction_slope = frictionFactor * velocity * velocity / (
            8.0 * FrictionLoss.g * hydraulic_radius)
        return friction_slope

    def flowRate(self, slope, area, perimeter, velocity):
        hydraulic_radius = area / perimeter
        friction_factor = self.friction_factor(hydraulic_radius, velocity)
        flow = math.pow((slope * 4.0 * hydraulic_radius *
                        area * area * 2.0 * FrictionLoss.g /
                        friction_factor), 0.5)
        return flow


class Manning(FrictionLoss):
    def __init__(self, roughness):
        self.roughness = roughness

    def frictionSlope(self, area, perimeter, velocity):
        flow = area * velocity
        friction_slope = self.roughness**2 * flow**2 * math.pow(perimeter, (4.0/3.0)) / math.pow(area, (10.0 / 3.0))
        return friction_slope

    def flowRate(self, slope, area, perimeter, velocity):
        hydraulic_radius = area / perimeter
        flow = (1.0 / self.roughness) * area * math.pow(hydraulic_radius, (2.0 / 3.0)) * math.pow(slope, 0.5)
        return flow
