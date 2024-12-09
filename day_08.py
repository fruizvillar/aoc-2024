from pathlib import Path

INPUTS = Path('inputs')

DAY = 8

f = INPUTS / f'day_{DAY:02d}.txt'


class Instruction:
    Count = 0

    def __init__(self, line):
        self.operation = line.split(' ')[0]
        self.argument = int(line.split(' ')[1])
        self.n = self.Count

        self.__class__.Count += 1

    def __repr__(self):
        return f'Instr. [{self.n:03}] {self.operation.upper()} {self.argument:4}'


def main():

    acc = 0
    try:

        for replacing_int in range(1000):

            with f.open() as f_o:
                instructions = [Instruction(s) for s in f_o.readlines()]

            replacing = instructions[replacing_int]
            if replacing.operation == 'jmp':
                replacing_operation = 'nop'
            elif replacing.operation == 'nop':
                replacing_operation = 'jmp'
            else:
                continue
            print(f'Replacing #{replacing.n}')

            replacing.operation = replacing_operation

            acc = 0
            n = 0
            visited = set()

            inf_loop = False
            while not inf_loop:
                if n in visited:
                    print(f'Inf loop detected. {n = } {acc = }')
                    break
                else:
                    visited.add(n)

                instr = instructions[n]
                if instr.operation == 'acc':
                    acc += instr.argument
                elif instr.operation == 'jmp':
                    n += instr.argument
                    continue

                n += 1

    except IndexError:
        print(f'BOOTED !!!!. {acc = }')

    print('DONE')


if __name__ == '__main__':
    main()
