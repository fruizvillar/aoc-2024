""" Solver for AoC 2024 Day 2"""

from typing import override

import lib

DAY = 2


class Solver(lib.Solver):
    """https://adventofcode.com/2024/day/2"""

    @override
    def solve(self) -> None:
        reports = self.read_lines_typed(int)
        safe_reports = 0
        safe_with_1_supression = 0
        for report in reports:

            if self.report_is_safe(report):
                safe_reports += 1
                continue

            # Unsafe! Check if we can suppress one level
            for i in range(len(report)):
                suppressed = report[:i] + report[i + 1 :]
                if self.report_is_safe(suppressed):
                    safe_with_1_supression += 1
                    break

        self.resolved(result_1=safe_reports)
        self.resolved(result_2=safe_reports + safe_with_1_supression)

    def report_is_safe(self, report):
        sorting = None
        prev_level = report[0]

        for level in report[1:]:
            if not (diff := abs(level - prev_level)):
                return False

            if diff > 3:
                return False

            if sorting is None:
                if level > prev_level:
                    sorting = "asc"
                else:
                    sorting = "desc"

            if sorting == "asc" and level < prev_level:
                return False
            if sorting == "desc" and level > prev_level:
                return False

            prev_level = level

        return True


solver = Solver(DAY)
solver()
