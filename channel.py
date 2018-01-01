import math


class Channel:
    """set step lengths, define defaults"""
    step = (0, 0.625, 0.625, 1.25, 2.5, 2.5, 5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 2.5)
    g = 9.806   # gravitational constant
    precision = 0.0001
    MAX_ITER = 29

    def __init__(self, flow, width, depth, length, us_il, ds_il, Ks, kinvisc, ds_depth=0, open_chan=True):
        self.flow = flow
        self.width = width
        self.depth = depth
        self.length = length
        self.us_invert = us_il
        self.ds_invert = ds_il
        self.slope = (self.us_invert - self.ds_invert) / self.length
        self.Ks = Ks
        self.kinvisc = kinvisc
        self.ds_depth = ds_depth
        self.chainage = []
        self.energy = []
        self.water = []
        self.head = []
        self.crit_depth = 0.0
        self.norm_depth = 0.0
        self.open_chan = open_chan

    def critical_depth(self):
        """calculate critical depth for channel"""
        crit_depth = math.pow((self.flow**2 / (self.width **2 * Channel.g)), (1/3))
        return crit_depth

    def normal_depth(self):
        """calculate normal depth for channel"""
        # check for flat slope
        if self.slope <= 0.0001:
            raise ValueError("flat slope")
        upper = self.depth
        lower = 0.0
        solution = False
        while not solution:
            normal_depth = (upper + lower) / 2.0
            area = normal_depth * self.width
            perimeter = self.width + 2.0 * normal_depth
            vel_norm = self.flow / (self.width * normal_depth)
            hydraulic_radius = area / perimeter
            friction_factor = self.colebrook_white(hydraulic_radius, vel_norm)
            calc_flow = math.pow((self.slope * 4.0 * hydraulic_radius * area * area * 2.0 * Channel.g / friction_factor), 0.5)
            if math.fabs(self.flow - calc_flow) < Channel.precision:
                solution = True
            elif calc_flow > self.flow:
                upper = normal_depth
            else:
                lower = normal_depth
        return normal_depth

    def colebrook_white(self, hydraulic_radius, vel_norm):
        """calculate colebrook-white friction factor.
        Start with guess value."""
        guess = 0.02  # change to approximation to colebrook-white to reduce iteration
        dia = 4.0 * hydraulic_radius
        Re = dia * vel_norm / self.kinvisc
        solution = False
        while not solution:
            friction = 0.25 * math.pow(math.log10(self.Ks / (3.7 * dia) + 2.51 / (vel_norm * dia / self.kinvisc * math.sqrt(guess))),-2)
            if math.fabs(friction - guess) < Channel.precision:
                solution = True
            else:
                guess += (friction - guess) / 2.0
        return friction

    def backwater(self):
        """calculate back water profile. Calculate zero distance values,
         then distances as per step length."""
        water_depth = max(self.ds_depth, self.crit_depth)
        E_previous = 0
        Sf_previous = 0
        delta_chain = 0
        previous_depth = water_depth
        for i in Channel.step:
            if i == 0:
                # check for conduit full
                if water_depth > self.depth:
                    wet_perimeter = 2 * (self.width + self.depth)
                    area = self.width * self.depth
                else:
                    wet_perimeter = self.width + 2 * water_depth
                    area = self.width * water_depth
                hyd_radius = area / wet_perimeter
                velocity = self.flow / area
                E0 = water_depth + (velocity**2 / (2 * Channel.g))
                friction_factor = self.colebrook_white(hyd_radius, velocity)
                Sf = friction_factor * velocity**2 / (8.0 * Channel.g * hyd_radius)
                # print("E0: %.3f" % E0, " Sf: %.3f" % Sf)
                E_previous = E0
                Sf_previous = Sf
                self.chainage.append(0)
                self.energy.append(self.ds_invert + E0)
                self.water.append(water_depth)
                self.head.append(self.ds_invert + water_depth)
            elif water_depth > self.depth:
                delta_L = i * (self.length / 100.0)
                print(delta_L, water_depth)
                wet_perimeter = 2 * (self.width + self.depth)
                area = self.width * self.depth
                hyd_radius = area / wet_perimeter
                velocity = self.flow / area
                E0 = water_depth + (velocity**2 / (2 * Channel.g))
                print(E0)
                friction_factor = self.colebrook_white(hyd_radius, velocity)
                Sf = friction_factor * velocity**2 / (8.0 * Channel.g * hyd_radius)
                E_upstream = E0 + delta_L * Sf
                water_depth = E_upstream - velocity**2 / (2 * Channel.g)
                print(water_depth)
                E_previous = E_upstream
                E2 = E_previous
                Sf_previous = Sf
                previous_depth = water_depth
                delta_chain += delta_L
                self.chainage.append(delta_chain)
                self.energy.append(self.ds_invert + E_previous)
                self.water.append(water_depth - delta_chain * self.slope)
                self.head.append(self.ds_invert + water_depth)
            else:
                delta_L = i * (self.length / 100.0)
                upper = self.depth
                lower = previous_depth
                # changed as depth could decrease preventing solution
                # lower = 0
                # print("loop")

                solution = False
                count = 0
                while not solution:
                    water_depth = (upper + lower) / 2.0
                    area = self.width * water_depth
                    wet_perimeter = self.width + 2 * water_depth
                    hyd_radius = area / wet_perimeter
                    velocity = self.flow / area
                    E_upstream = water_depth + (velocity**2 / (2 * Channel.g))
                    friction_factor = self.colebrook_white(hyd_radius, velocity)
                    Sf = friction_factor * velocity**2 / (8.0 * Channel.g * hyd_radius)
                    Sf_mean = (Sf + Sf_previous) / 2.0
                    E2 = E_previous - delta_L * (self.slope - Sf_mean)
                    # print("check", E_upstream, E2)
                    if math.fabs(E_upstream - E2) < Channel.precision:
                        solution = True
                    elif E_upstream > E2:
                        upper = water_depth
                        count += 1
                        if count == Channel.MAX_ITER:
                            solution = True
                    else:
                        lower = water_depth
                        count += 1
                        if count == Channel.MAX_ITER:
                            solution = True
                E_previous = E2
                Sf_previous = Sf
                previous_depth = water_depth
                delta_chain += delta_L
                self.chainage.append(delta_chain)
                self.energy.append(self.ds_invert + delta_chain * self.slope + E2)
                self.water.append(water_depth)
                self.head.append(self.ds_invert + delta_chain * self.slope + water_depth)
                print("Friction: %.4f" % friction_factor)
                print("Length %.1f" % delta_chain, "E2: %.3f" % E_previous, " Sf: %.3f" % Sf_previous)
        return E2

    def calculate(self):
        try:
            # TODO validate data
            # calculate critical depth
            self.crit_depth = self.critical_depth()
            # calculate normal depth
            self.norm_depth = self.normal_depth()
            print(self.slope)
            # TODO figure out how to handle downstream depth greater than normal depth
    #        if self.ds_depth > self.norm_depth:
    #            return
            if self.norm_depth > self.crit_depth:
                self.backwater()
        except ValueError as e:
            print(e)
            pass
        except:
            pass


#main
#"""enter flow, width, depth, length, us invert, ds invert, Ks, kinematic viscocity"""
#channel1 = Channel(0.5, 0.8, 2.0, 100, 1.0, 0.9, 0.003, 1.141e-06)
#print(channel1.critical_depth())
#print(channel1.normal_depth())
#crit_depth = channel1.critical_depth()
#channel1.backwater(crit_depth)
#print(channel1.chainage[0], channel1.energy[0], channel1.water[0], channel1.head[0])
#x = 0
#for i in channel1.chainage:
#    print("Length %.1f" % i, "Energy %.3f" % channel1.energy[x], "Water %.3f" % channel1.water[x], "Head %.3f" % channel1.head[x])
#    x += 1
