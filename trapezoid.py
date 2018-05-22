import conduit
import math

class Trapezoid(conduit.Conduit):

    def __init__(self):
        self.width = None
        self.depth = None
        self.side_slope = None
        super().__init__()

    def setValues(self, flow, width, depth, side_slope, length, us_il, ds_il,
        Ks, kinvisc, ds_depth=0, open_chan=False, friction_formula="DWCW"):
        self.width = self.checkValues(width, True)
        self.depth = self.checkValues(depth, True)
        self.side_slope = self.checkValues(side_slope, True)
        super().setValues(flow, length, us_il, ds_il, Ks, kinvisc,
        ds_depth, open_chan, friction_formula)

    def critical_depth(self):
        """Calculate critical depth for trapezoid"""
        upper = self.maxdepth
        lower = 0.0
        solution = False
        while not solution:
            Hcrit = (upper + lower) / 2.0
            area = self.getFlowArea(Hcrit)
            top_width = self.getFlowTopWidth(Hcrit)
            froude = self.flow**2 * top_width / (Trapezoid.g * area**3)
            if math.fabs(froude - 1.0) < Trapezoid.precision:
                solution = True
            elif froude > 1.0:
                lower = Hcrit
            else:
                upper = Hcrit
        return Hcrit

    def max_depth(self):
        return self.depth

    def getFlowArea(self, depth):
        area = depth * (self.width + self.side_slope * depth)
        return area

    def getFlowPerimeter(self, depth=0):
        perimeter = self.width + (2.0 * depth *
        math.sqrt(1.0 + self.side_slope**2))
        return perimeter

    def getFlowTopWidth(self, depth=0):
        topWidth = self.width + 2.0 * self.side_slope * depth
        return topWidth

    def getConduitArea(self):
        return self.depth * (self.width + self.side_slope * self.depth)

    def getConduitPerimeter(self):
        return self.width + (2.0 * self.depth *
        math.sqrt(1.0 + self.side_slope**2))
