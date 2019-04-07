import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from channel import Channel
# main
"""enter flow, width, depth, length, us invert, ds invert, Ks, kinematic viscocity"""
# channel1 = channel.Channel(0.5, 1.0, 2.0, 100, 0.1, 0.0, 0.003, 1.141e-06, 0.4)
print("Test Run 3")
channel1 = Channel()
channel1.setValues(0.5, 0.8, 2, 100.0, 1.0, 0.0, 0.003, 1.141e-06)
# print(channel1.critical_depth())
# print(channel1.normal_depth())
# crit_depth = channel1.critical_depth()
channel1.calculate()
print(channel1.crit_depth)
print(channel1.norm_depth)
# print(channel1.chainage[0], channel1.energy[0], channel1.water[0], channel1.head[0])
x = 0
for i in channel1.chainage:
    print("Length %.1f" % i, "Energy %.3f" % channel1.energy[x], "Water %.3f" % channel1.water[x], "Head %.3f" % channel1.head[x])
    x += 1

print("Test Run 4")
channel1.setValues(0.5, 0.8, 2, 100.0, 1.0, 1.0, 0.003, 1.141e-06)
# print(channel1.critical_depth())
# print(channel1.normal_depth())
# crit_depth = channel1.critical_depth()
channel1.calculate()
print(channel1.crit_depth)
print(channel1.norm_depth)
# print(channel1.chainage[0], channel1.energy[0], channel1.water[0], channel1.head[0])
x = 0
for i in channel1.chainage:
    print("Length %.1f" % i, "Energy %.3f" % channel1.energy[x], "Water %.3f" % channel1.water[x], "Head %.3f" % channel1.head[x])
    x += 1
