""" Solver for AoC 2024 Day 7"""

import collections
import dataclasses
import datetime
import itertools
from typing import override

import lib

DAY = int("7")


@dataclasses.dataclass
class CalibrationEquation:
    test_value: int
    operands: list[int]


class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/7"""

    @override
    def solve(self) -> None:

        equations = self.load_equations()

        sum_test_values = 0
        sum_test_values_with_concat = 0

        for equation in equations:
            if self.DEBUG or True:
                print(datetime.datetime.now(), "Equation:", equation)

            if self.equation_can_be_resolved(equation):
                sum_test_values += equation.test_value
                sum_test_values_with_concat += equation.test_value

                if self.DEBUG:
                    print("Equation resolved:", equation)

            elif self.equation_can_be_resolved(equation, allow_concat=True):
                sum_test_values_with_concat += equation.test_value

                if self.DEBUG:
                    print("Equation resolved (concat):", equation)

        self.resolved(result_1=sum_test_values, result_2=sum_test_values_with_concat)

    def load_equations(self) -> list[CalibrationEquation]:
        equations = []

        for line in self.read_lines_re(r"[ :]+", int, split=True):
            equations.append(CalibrationEquation(line[0], line[1:]))

        return equations

    def equation_can_be_resolved(
        self, equation: CalibrationEquation, allow_concat=False
    ) -> bool:

        q = (
            collections.deque()
        )  # type: collections.deque[tuple[int, int, collections.deque[int]]]

        q_operands = collections.deque(equation.operands)

        q.append((0, equation.test_value, q_operands.popleft(), q_operands))

        while q:
            it, test_value, acc, q_operands = q.popleft()

            if self.DEBUG:
                print(
                    "It",
                    it,
                    "Test value:",
                    test_value,
                    "Acc",
                    acc,
                    "Operands:",
                    q_operands,
                )
                print("Queue:", len(q))
            if not q_operands:
                if acc == test_value:
                    return True
                else:
                    continue

            next_operand = q_operands.popleft()
            it += 1
            q.appendleft((it, test_value, acc + next_operand, q_operands.copy()))
            q.appendleft((it, test_value, acc * next_operand, q_operands.copy()))
            if allow_concat:
                q.appendleft(
                    (
                        it,
                        test_value,
                        int(str(acc) + str(next_operand)),
                        q_operands.copy(),
                    )
                )


solver = Solver(DAY)
solver()
