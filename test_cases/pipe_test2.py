import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from pipe import Pipe
# main
"""enter flow, diameter, length, us invert, ds invert, Ks, kinematic viscocity"""
# channel1 = channel.Channel(0.5, 1.0, 2.0, 100, 0.1, 0.0, 0.003, 1.141e-06, 0.4)
print("Pipe Test Run 3")
pipe1 = Pipe()
pipe1.setValues(0.5, 1.0, 100.0, 1.0, 0.0, 0.003, 1.141e-06)
# print(channel1.critical_depth())
# print(channel1.normal_depth())
# crit_depth = channel1.critical_depth()
pipe1.calculate()
print(pipe1.crit_depth)
print(pipe1.norm_depth)
# print(channel1.chainage[0], channel1.energy[0], channel1.water[0], channel1.head[0])
x = 0
for i in pipe1.chainage:
    print("Length %.1f" % i, "Energy %.3f" % pipe1.energy[x], "Water %.3f" % pipe1.water[x], "Head %.3f" % pipe1.head[x])
    x += 1

print("Test Run 4")
pipe1.setValues(0.5, 1.0, 100.0, 1.0, 1.0, 0.003, 1.141e-06, 0.4, False, "DWCW", 0, 0)
# print(channel1.critical_depth())
# print(channel1.normal_depth())
# crit_depth = channel1.critical_depth()
pipe1.calculate()
print(pipe1.crit_depth)
print(pipe1.norm_depth)
# print(channel1.chainage[0], channel1.energy[0], channel1.water[0], channel1.head[0])
x = 0
for i in pipe1.chainage:
    print("Length %.1f" % i, "Energy %.3f" % pipe1.energy[x], "Water %.3f" % pipe1.water[x], "Head %.3f" % pipe1.head[x])
    x += 1
