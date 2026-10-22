class Calculator:
    def __init__(self, value: float):
        self.result = float(value)

    def add(self, value: float) -> 'Calculator':
        self.result += value
        return self

    def subtract(self, value: float) -> 'Calculator':
        self.result -= value
        return self

    def multiply(self, value: float) -> 'Calculator':
        self.result *= value
        return self

    def divide(self, value: float) -> 'Calculator':
        if value == 0:
            raise ValueError("Division by zero is not allowed")
        self.result /= value
        return self

    def power(self, value: float) -> 'Calculator':
        self.result **= value
        return self

    def getResult(self) -> float:
        return self.result

class Solution:
    pass
