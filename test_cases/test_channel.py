import sys
import unittest
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from channel import Channel


class TestChannel(unittest.TestCase):
    def setUp(self):
        self.channel1 = Channel()

    # Mild slope, critical depth at downstream end
    def test_run1(self):
        self.channel1.setValues(0.5, 0.8, 2, 100.0, 1.0, 0.9, 0.003, 1.141e-06)
        self.channel1.calculate()
        self.assertAlmostEqual(self.channel1.crit_depth, 0.342, 3)
        self.assertAlmostEqual(self.channel1.norm_depth, 0.713, 3)
        self.assertAlmostEqual(self.channel1.energy[0], 1.412, 3)
        self.assertAlmostEqual(self.channel1.energy[-1], 1.645, 3)

    # Mild slope, downstream water depth 0.4m
    def test_run2(self):
        self.channel1.setValues(0.5, 0.8, 2, 100.0, 1.0, 0.9, 0.003, 1.141e-06, 0.4, True, "DWCW", 0, 0)
        self.channel1.calculate()
        self.assertAlmostEqual(self.channel1.crit_depth, 0.342, 3)
        self.assertAlmostEqual(self.channel1.norm_depth, 0.713, 3)
        self.assertAlmostEqual(self.channel1.energy[0], 1.424, 3)
        self.assertAlmostEqual(self.channel1.energy[-1], 1.647, 3)

    # Mild slope, downstream water depth 0.4m, Manning friction
    def test_run2a(self):
        self.channel1.setValues(0.5, 0.8, 2, 100.0, 1.0, 0.9, 0.015, 1.141e-06, 0.4, True, "MANNING", 0, 0)
        self.channel1.calculate()
        self.assertAlmostEqual(self.channel1.crit_depth, 0.342, 3)
        self.assertAlmostEqual(self.channel1.norm_depth, 0.731, 3)
        self.assertAlmostEqual(self.channel1.energy[0], 1.424, 3)
        self.assertAlmostEqual(self.channel1.energy[-1], 1.655, 3)

    # Check steep slope, supercritical flow or calc critical depth full length
    def test_run3(self):
        self.channel1.setValues(0.5, 0.8, 2, 100.0, 1.0, 0.0, 0.003, 1.141e-06)
        self.channel1.calculate()
        self.assertAlmostEqual(self.channel1.crit_depth, 0.342, 3)
        self.assertAlmostEqual(self.channel1.norm_depth, 0.294, 3)
        # self.assertAlmostEqual(self.channel1.energy[0], 1.512, 3)
        # self.assertAlmostEqual(self.channel1.energy[-1], 0.512, 3)

    # Check level slope calculation
    def test_run4(self):
        self.channel1.setValues(0.5, 0.8, 2, 100.0, 1.0, 1.0, 0.003, 1.141e-06)
        self.channel1.calculate()
        self.assertAlmostEqual(self.channel1.crit_depth, 0.342, 3)
        self.assertEqual(self.channel1.norm_depth, None)
        self.assertAlmostEqual(self.channel1.energy[0], 1.709, 3, "fail level slope")
        self.assertAlmostEqual(self.channel1.energy[-1], 1.512, 3, "fail level slope")


if __name__ == '__main__':
    unittest.main()
