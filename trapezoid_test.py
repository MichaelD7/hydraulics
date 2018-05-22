import trapezoid
# main
"""enter flow, width, depth, side_slope, length, us invert, ds invert, Ks, kinematic viscocity"""
print("Test Run 1")
trapezoid1 = trapezoid.Trapezoid()
trapezoid1.setValues(0.3, 0.5, 1.0, 0.3, 100, 1.0, 0.9, 0.003, 1.141e-06)
trapezoid1.calculate()
print(trapezoid1.crit_depth)
print(trapezoid1.norm_depth)
x = 0
for i in trapezoid1.chainage:
    print("Length %.1f" % i, "Energy %.3f" % trapezoid1.energy[x],
     "Water %.3f" % trapezoid1.water[x], "Head %.3f" % trapezoid1.head[x])
    x += 1
