import unittest
from calculator import Calculator, ScientificCalculator

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(self.calc.divide(6, 3), 2)
        with self.assertRaises(ValueError):
            self.calc.divide(1, 0)

class TestScientificCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = ScientificCalculator()

    def test_sin(self):
        self.assertAlmostEqual(self.calc.sin(0), 0)

    def test_cos(self):
        self.assertAlmostEqual(self.calc.cos(0), 1)

    def test_tan(self):
        self.assertAlmostEqual(self.calc.tan(0), 0)

    def test_log(self):
        self.assertAlmostEqual(self.calc.log(1), 0)
        with self.assertRaises(ValueError):
            self.calc.log(0)

    def test_sqrt(self):
        self.assertAlmostEqual(self.calc.sqrt(4), 2)
        with self.assertRaises(ValueError):
            self.calc.sqrt(-1)

if __name__ == '__main__':
    unittest.main()
