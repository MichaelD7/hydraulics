import sys
import unittest
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from pipe import Pipe


class TestPipe(unittest.TestCase):
    def setUp(self):
        self.pipe1 = Pipe()

    # Mild slope, critical depth at downstream end
    def test_run1(self):
        self.pipe1.setValues(0.5, 1.0, 100.0, 1.0, 0.9, 0.003, 1.141e-06)
        self.pipe1.calculate()
        self.assertAlmostEqual(self.pipe1.crit_depth, 0.399, 3)
        self.assertAlmostEqual(self.pipe1.norm_depth, 0.640, 3)
        self.assertAlmostEqual(self.pipe1.energy[0], 1.448, 3)
        self.assertAlmostEqual(self.pipe1.energy[-1], 1.634, 3)

    # Mild slope, downstream water depth 1.3m
    def test_run2(self):
        self.pipe1.setValues(0.5, 1.0, 100.0, 1.0, 0.9, 0.003, 1.141e-06, 0.4,
                             False, "DWCW", 0, 0)
        self.pipe1.calculate()
        self.assertAlmostEqual(self.pipe1.crit_depth, 0.399, 3)
        self.assertAlmostEqual(self.pipe1.norm_depth, 0.640, 3)
        self.assertAlmostEqual(self.pipe1.energy[0], 1.448, 3)
        self.assertAlmostEqual(self.pipe1.energy[-1], 1.634, 3)

    # Critical depth full length
    def test_run3(self):
        self.pipe1.setValues(0.5, 1.0, 100.0, 1.0, 0.0, 0.003, 1.141e-06, 0.0,
                             False, "DWCW", 0, 0)
        self.pipe1.calculate()
        self.assertAlmostEqual(self.pipe1.crit_depth, 0.399, 3)
        self.assertAlmostEqual(self.pipe1.norm_depth, 0.327, 3)
        self.assertAlmostEqual(self.pipe1.energy[0], 0.548, 3)
        self.assertAlmostEqual(self.pipe1.energy[-1], 1.548, 3)


if __name__ == '__main__':
    unittest.main()
