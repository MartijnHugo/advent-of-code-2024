from dataclasses import dataclass
from enum import auto, Enum, StrEnum
from itertools import product
import operator


class Operator(StrEnum):
    ADD = "+"
    MULTIPLY = "*"


ALL_OPERATORS = [op for op in Operator]

class Operator2(Enum):
    ADD = operator.add
    MULTIPLY = operator.mul
    CONCAT = auto()

ALL_OPERATORS_2 = [op for op in Operator2]


@dataclass
class Equation:
    test_value: int
    numbers: list[int]

    def whatever(self) -> bool:
        for operators in product(*[ALL_OPERATORS for _ in range(len(self.numbers) - 1)]):
            expression = f"value = {'('*(len(self.numbers) - 1)}{self.numbers[0]}"
            for i in range(len(operators)):
                expression += f"{operators[i]}{self.numbers[i+1]})"

            loc = {}
            exec(expression, globals(), loc)
            if loc["value"] == self.test_value:
                return True

        return False
    
    def whatever2(self) -> bool:
        for operators in product(*[ALL_OPERATORS_2 for _ in range(len(self.numbers) - 1)]):
            value = self.numbers[0]
            for i in range(len(operators)):
                op = operators[i]
                num = self.numbers[i+1]
                
                if op == Operator2.CONCAT:
                    value = int(f"{value}{num}")
                else:
                    value = op.value(value, num)
            
            if value == self.test_value:
                return True
            
        return False



equations: list[Equation] = []
with open("src/day_7.txt", "r") as f:
    for l in f.readlines():
        a, b = l.split(": ")
        nums = b.rstrip().split(" ")
        equations.append(Equation(int(a), [int(x) for x in nums]))


total_calibration_result = 0
total_calibration_result_2 = 0
for eq in equations:
    if eq.whatever():
        total_calibration_result += eq.test_value

    if eq.whatever2():
        total_calibration_result_2 += eq.test_value

print(total_calibration_result)
print(total_calibration_result_2)