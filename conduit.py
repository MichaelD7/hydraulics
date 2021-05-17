import math
import friction
from abc import ABCMeta, abstractmethod


class Conduit:
    __metaclass__ = ABCMeta

    """set step lengths, define defaults"""
    step = (0, 0.625, 0.625, 1.25, 2.5, 2.5, 5, 5, 10,
            10, 10, 10, 10, 10, 10, 10, 2.5)
    g = 9.806   # gravitational constant
    precision = 0.0001
    MAX_ITER = 29

    def __init__(self):
        self.__flow = None
    #    self.width = None
    #    self.depth = None
        self.__length = None
        self.__us_invert = None
        self.__ds_invert = None
        self.__slope = None
        self.__Ks = None
        self.__kinvisc = None
        self.ds_depth = None
        self.maxdepth = None
        self.chainage = []
        self.energy = []
        self.water = []
        self.head = []
        self.crit_depth = 0.0
        self.norm_depth = 0.0
        self.open_chan = None
        self.friction_formula = None
        self.us_K = None
        self.ds_K = None
        self.us_discont = None
        self.ds_discont = None
        self.us_velocity = None
        self.ds_velocity = None

    @property
    def flow(self):
        return self.__flow

    def setValues(self, flow, length, us_il, ds_il, Ks, kinvisc,
                  ds_depth=0, open_chan=True, friction_formula="DWCW",
                  us_K=0, ds_K=0):
        self.__flow = self.checkValues(flow, True)
    #    self.width = self.checkValues(width, True)
    #    self.depth = self.checkValues(depth, True)
        self.__length = self.checkValues(length, True)
        self.__us_invert = self.checkValues(us_il)
        self.__ds_invert = self.checkValues(ds_il)
        self.__slope = (self.__us_invert - self.__ds_invert) / self.__length
        self.__Ks = self.checkValues(Ks, True)
        self.__kinvisc = self.checkValues(kinvisc, True)
        self.ds_depth = self.checkValues(ds_depth, True)
        self.open_chan = open_chan
        self.friction_formula = self.setFrictionModel(friction_formula)
        self.maxdepth = self.max_depth()
        # allow negatives?
        self.us_K = self.checkValues(us_K)
        self.ds_K = self.checkValues(ds_K)

    def setFrictionModel(self, friction_formula):
        if friction_formula == "DWCW":
            friction_model = friction.DarcyWeisbach(self.__Ks, self.__kinvisc)
        elif friction_formula == "MANNING":
            friction_model = friction.Manning(self.__Ks)

        return friction_model

    def checkValues(self, checkValue, non_negative=False):
        # change to static method
        try:
            checkValue = float(checkValue)
            if non_negative:
                if checkValue < 0:
                    raise ValueError("Can't be negative")
        except ValueError as e:
            print("can't be negative", e)
            pass
        return checkValue

    def critical_depth(self):
        """Calculate critical depth"""
        upper = self.maxdepth
        lower = 0.0
        solution = False
        while not solution:
            Hcrit = (upper + lower) / 2.0
            area = self.getFlowArea(Hcrit)
            top_width = self.getFlowTopWidth(Hcrit)
            froude = self.__flow**2 * top_width / (Conduit.g * area**3)
            if math.fabs(froude - 1.0) < Conduit.precision:
                solution = True
            elif froude > 1.0:
                lower = Hcrit
            else:
                upper = Hcrit
        return Hcrit

    @abstractmethod
    def max_depth(self):
        pass

    @abstractmethod
    def getFlowArea(self, depth):
        pass

    @abstractmethod
    def getFlowPerimeter(self, depth):
        pass

    @abstractmethod
    def getFlowTopWidth(self, depth):
        pass

    @abstractmethod
    def getConduitArea(self):
        pass

    @abstractmethod
    def getConduitPerimeter(self):
        pass

    def normal_depth(self):
        """calculate normal depth for conduit"""
        # check for flat slope
        if self.__slope <= 0.0001:
            # raise ValueError("check slope")
            return None
        # include loop counter, need better way than 2 x max depth. not good
        if self.open_chan:
            upper = 2 * self.maxdepth
        else:
            upper = self.maxdepth
        # upper = self.maxdepth
        lower = 0.0
        solution = False
        count = 0
        while not solution:
            normal_depth = (upper + lower) / 2.0
            area = self.getFlowArea(normal_depth)
            perimeter = self.getFlowPerimeter(normal_depth)
            vel_norm = self.__flow / area
        #    hydraulic_radius = area / perimeter
        #    friction_factor = self.friction_formula.friction_factor(
        #        hydraulic_radius, vel_norm)
            # calc_flow = math.pow((self.__slope * 4.0 * hydraulic_radius *
            #        area * area * 2.0 * Conduit.g / friction_factor), 0.5)
            calc_flow = self.friction_formula.flowRate(self.__slope, area,
                                                       perimeter, vel_norm)
            if math.fabs(self.__flow - calc_flow) < Conduit.precision:
                solution = True
            elif calc_flow > self.__flow:
                upper = normal_depth
            else:
                lower = normal_depth
            count += 1
            if count > Conduit.MAX_ITER:
                return None
        return normal_depth

    def backwater(self):
        """calculate back water profile. Calculate zero distance values,
         then distances as per step length."""
        water_depth = max(self.ds_depth, self.crit_depth)
        E_previous = 0
        Sf_previous = 0
        delta_chain = 0
        previous_depth = water_depth
        for i in Conduit.step:
            if i == 0:
                # check for conduit full
                if water_depth > self.maxdepth:
                    if self.open_chan:
                        raise ValueError("over tops past ch. " +
                                         str(delta_chain))
                    wet_perimeter = self.getConduitPerimeter()
                    area = self.getConduitArea()
                else:
                    wet_perimeter = self.getFlowPerimeter(water_depth)
                    area = self.getFlowArea(water_depth)
                hyd_radius = area / wet_perimeter
                velocity = self.__flow / area
                self.ds_velocity = velocity
                #  set downstream K to 0 for crit depth
                if water_depth == self.crit_depth:
                    self.ds_discont = 0
                else:
                    self.ds_discont = self.ds_K * (self.ds_velocity**2 /
                                                   (2 * Conduit.g))
                E0 = water_depth + (velocity**2 /
                                    (2 * Conduit.g)) + self.ds_discont
                # TODO update water_depth based on updated energy level??
                # Sf = slope of hydraulic gradient
                Sf = self.friction_formula.frictionSlope(area, wet_perimeter,
                                                         velocity)
                # print("E0: %.3f" % E0, " Sf: %.3f" % Sf)
                E_previous = E0
                Sf_previous = Sf
                self.updateResults(0, E0, water_depth)
            elif water_depth >= self.maxdepth:
                if self.open_chan:
                    raise ValueError("over tops past ch. " + str(delta_chain))
                delta_L = i * (self.__length / 100.0)
                # print(delta_L, water_depth)
                wet_perimeter = self.getConduitPerimeter()
                area = self.getConduitArea()
            #    hyd_radius = area / wet_perimeter
                velocity = self.__flow / area
                # E0 = water_depth + (velocity**2 / (2 * Conduit.g))
                # print(E0)
                Sf = self.friction_formula.frictionSlope(area, wet_perimeter,
                                                         velocity)
                E_upstream = E_previous + delta_L * Sf
                water_depth = E_upstream - velocity**2 / (2 * Conduit.g)
                if water_depth > self.maxdepth and self.open_chan:
                    raise ValueError("over tops past ch. " + str(delta_chain))
                # print(water_depth)
                delta_chain += delta_L
                self.updateResults(delta_chain, (E_upstream - E_previous),
                                   (water_depth - previous_depth), False)
                E_previous = E_upstream
                # E2 = E_previous
                Sf_previous = Sf
                previous_depth = water_depth

            else:
                delta_L = i * (self.__length / 100.0)
                upper = self.maxdepth
                lower = previous_depth

                solution = False
                count = 0
                while not solution:
                    water_depth = (upper + lower) / 2.0
                    area = self.getFlowArea(water_depth)
                    wet_perimeter = self.getFlowPerimeter(water_depth)
                #    hyd_radius = area / wet_perimeter
                    velocity = self.__flow / area
                    E_upstream = water_depth + (velocity**2 / (2 * Conduit.g))
                    Sf = self.friction_formula.frictionSlope(area,
                                                             wet_perimeter,
                                                             velocity)
                    Sf_mean = (Sf + Sf_previous) / 2.0
                    E2 = E_previous - delta_L * (self.__slope - Sf_mean)
                    # print("check", E_upstream, E2)
                    if math.fabs(E_upstream - E2) < Conduit.precision:
                        solution = True
                    elif E_upstream > E2:
                        upper = water_depth
                        count += 1
                        if count == Conduit.MAX_ITER:
                            solution = True
                    else:
                        lower = water_depth
                        count += 1
                        if count == Conduit.MAX_ITER:
                            solution = True
                E_previous = E2
                Sf_previous = Sf
                previous_depth = water_depth
                delta_chain += delta_L
                self.updateResults(delta_chain, E2, water_depth)
                # print("Friction: %.4f" % friction_factor)
                # print("Length %.1f" % delta_chain, "E2: %.3f" % E_previous,
                # " Sf: %.3f" % Sf_previous)
        self.us_velocity = velocity
        if self.us_K:
            self.us_discont = self.us_K * (self.us_velocity**2 /
                                           (2 * Conduit.g))
            E_previous += self.us_discont
            self.chainage.append(delta_chain)
            self.energy.append(self.energy[-1] + self.us_discont)
            self.water.append(self.water[-1])
            self.head.append(self.head[-1])
        #    self.updateResults(delta_chain, E_previous, water_depth)
        return 0

    def updateResults(self, delta_chain, energy, water_depth,
                      include_gradient=True):
        self.chainage.append(delta_chain)
        if delta_chain == 0:
            self.energy.append(self.__ds_invert + energy)
            self.water.append(water_depth)
            self.head.append(self.__ds_invert + water_depth)
        elif include_gradient:
            self.energy.append(self.__ds_invert + delta_chain *
                               self.__slope + energy)
            self.water.append(water_depth)
            self.head.append(self.__ds_invert +
                             delta_chain * self.__slope + water_depth)
        else:
            self.energy.append(self.energy[-1] + energy)
            self.water.append(self.water[-1] + water_depth -
                              (self.chainage[-1] - self.chainage[-2]) *
                              self.__slope)
            self.head.append(self.head[-1] + water_depth)

    def clearResults(self):
        del self.chainage[:]
        del self.energy[:]
        del self.water[:]
        del self.head[:]

    def calculate(self):
        try:
            # TODO validate data
            # calculate critical depth
            self.crit_depth = self.critical_depth()
            # calculate normal depth
            self.norm_depth = self.normal_depth()
            # print(self.__slope)
            # TODO figure out how to handle downstream depth greater
            # than normal depth
    #        if self.ds_depth > self.norm_depth:
    #            return
            if self.norm_depth is None:
                self.clearResults()
                self.backwater()
            elif self.norm_depth > self.crit_depth:
                self.clearResults()
                self.backwater()
            else:
                print("supercritical calc to be added")
        except ValueError as e:
            print(e)
            pass
        except:
            print("error")
            pass
