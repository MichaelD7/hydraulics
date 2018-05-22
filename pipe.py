import conduit
import math

class Pipe(conduit.Conduit):

    def __init__(self):
        self.diameter = None
        self.theta = None
        super().__init__()

    def setValues(self, flow, diameter, length, us_il, ds_il,
        Ks, kinvisc, ds_depth=0, open_chan=False, friction_formula="DWCW"):
        self.diameter = self.checkValues(diameter, True)
        super().setValues(flow, length, us_il, ds_il, Ks, kinvisc,
        ds_depth, open_chan, friction_formula)

    def critical_depth(self):
        """Calculate critical depth for pipe"""
        upper = self.maxdepth
        lower = 0.0
        solution = False
        while not solution:
            Hcrit = (upper + lower) / 2.0
            area = self.getFlowArea(Hcrit)
            top_width = self.getFlowTopWidth(Hcrit)
            froude = self.flow**2 * top_width / (Pipe.g * area**3)
            if math.fabs(froude - 1.0) < Pipe.precision:
                solution = True
            elif froude > 1.0:
                lower = Hcrit
            else:
                upper = Hcrit
        return Hcrit

    def partPipe(self, guess_depth):
        """calculate angle based on guessed depth of flow"""
        radius = self.diameter / 2.0
        if guess_depth < radius:
            z = radius - guess_depth
            theta = 2.0 * math.acos(2.0 * z / self.diameter)
        elif guess_depth == radius:
            theta = math.pi
        else:
            z = guess_depth - radius
            theta = 2.0 * math.pi - 2.0 * (math.acos(2.0 * z / self.diameter))
        return theta

    def max_depth(self):
        return self.diameter

    def getFlowArea(self, depth):
        self.theta = self.partPipe(depth)
        area = (self.diameter**2 / 8.0) * (self.theta - math.sin(self.theta))
        return area

    def getFlowPerimeter(self, depth=0):
        if not self.theta:
            self.theta = self.partPipe(depth)
        perimeter = self.diameter * self.theta / 2.0
        return perimeter

    def getFlowTopWidth(self, depth=0):
        if not self.theta:
            self.theta = self.partPipe(depth)
        topWidth = self.diameter * math.sin(self.theta / 2.0)
        return topWidth

    def getConduitArea(self):
        return math.pi * self.diameter**2 / 4.0

    def getConduitPerimeter(self):
        return math.pi * self.diameter
