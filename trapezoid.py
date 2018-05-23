import conduit
import math

class Trapezoid(conduit.Conduit):

    def __init__(self):
        self.width = None
        self.depth = None
        self.side_slope = None
        super().__init__()

    def setValues(self, flow, width, depth, side_slope, length, us_il, ds_il,
        Ks, kinvisc, ds_depth=0, open_chan=False, friction_formula="DWCW",
        us_K=0, ds_K=0):
        self.width = self.checkValues(width, True)
        self.depth = self.checkValues(depth, True)
        self.side_slope = self.checkValues(side_slope, True)
        super().setValues(flow, length, us_il, ds_il, Ks, kinvisc,
        ds_depth, open_chan, friction_formula, us_K, ds_K)

    def max_depth(self):
        return self.depth

    def getFlowArea(self, depth):
        area = depth * (self.width + self.side_slope * depth)
        return area

    def getFlowPerimeter(self, depth):
        perimeter = self.width + (2.0 * depth *
        math.sqrt(1.0 + self.side_slope**2))
        return perimeter

    def getFlowTopWidth(self, depth):
        topWidth = self.width + 2.0 * self.side_slope * depth
        return topWidth

    def getConduitArea(self):
        return self.depth * (self.width + self.side_slope * self.depth)

    def getConduitPerimeter(self):
        return self.width + (2.0 * self.depth *
        math.sqrt(1.0 + self.side_slope**2))
