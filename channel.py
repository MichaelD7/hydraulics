import conduit
import math

class Channel(conduit.Conduit):

    def __init__(self):
        super().__init__()
        self.width = None
        self.depth = None


    def setValues(self, flow, width, depth,length, us_il,
        ds_il, Ks, kinvisc, ds_depth=0, open_chan=True,
        friction_formula="DWCW"):
        self.width = self.checkValues(width, True)
        self.depth = self.checkValues(depth, True)
        super().setValues(flow, length, us_il, ds_il, Ks, kinvisc,
        ds_depth, open_chan, friction_formula)

#override base class, but not needed
    def critical_depth(self):
        """calculate critical depth for channel"""
        crit_depth = math.pow((self.flow**2 /
            (self.width **2 * Channel.g)), (1/3))
        return crit_depth

    def max_depth(self):
        return self.depth

    def getFlowArea(self, depth):
        return self.width * depth

    def getFlowPerimeter(self, depth):
        return self.width + 2.0 * depth

    def getFlowTopWidth(self, depth):
        return self.width

    def getConduitArea(self):
        return self.width * self.depth

    def getConduitPerimeter(self):
        return 2.0 * (self.width + self.depth)
