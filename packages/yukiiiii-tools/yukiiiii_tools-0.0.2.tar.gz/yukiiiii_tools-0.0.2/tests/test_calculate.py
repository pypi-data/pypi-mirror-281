# tests/test_calculate.py
import unittest
from yukiiiii_tools.calculate import add, subtract, multiply, divide

class TestCalculate(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(subtract(3, 1), 2)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(divide(3, 3), 1)
