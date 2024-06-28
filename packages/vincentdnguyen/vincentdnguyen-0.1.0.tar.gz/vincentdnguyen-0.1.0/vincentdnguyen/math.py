class MyMath:
    def __init__(self, value:int):
        self.value = value
    def factorial(self) -> int:
        if self.value == 0:
            return 1
        else:
            return self.value * MyMath(self.value - 1).factorial()

n = 4
fact_n = MyMath(n) * factorial()
print(f"Factorial of {n} is {fact_n}")
