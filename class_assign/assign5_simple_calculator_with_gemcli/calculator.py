import math

class Calculator:
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y

class ScientificCalculator(Calculator):
    def sin(self, x):
        return math.sin(x)

    def cos(self, x):
        return math.cos(x)

    def tan(self, x):
        return math.tan(x)

    def log(self, x):
        if x <= 0:
            raise ValueError("Cannot take the logarithm of a non-positive number")
        return math.log(x)

    def sqrt(self, x):
        if x < 0:
            raise ValueError("Cannot take the square root of a negative number")
        return math.sqrt(x)
