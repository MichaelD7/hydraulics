import pipe
# main
"""enter flow, diameter, length, us invert, ds invert, Ks, kinematic viscocity"""
print("Test Run 1")
pipe1 = pipe.Pipe()
pipe1.setValues(0.375, 0.9, 87.385, 15.456, 15.338, 0.006, 1.141e-06)
pipe1.calculate()
print(pipe1.crit_depth)
print(pipe1.norm_depth)
x = 0
for i in pipe1.chainage:
    print("Length %.1f" % i, "Energy %.3f" % pipe1.energy[x],
     "Water %.3f" % pipe1.water[x], "Head %.3f" % pipe1.head[x])
    x += 1
