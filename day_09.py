from pathlib import Path

INPUTS = Path('inputs')

DAY = 9

f = INPUTS / f'day_{DAY:02d}.txt'

L_PREAMBLE = 25


def main():
    buffer = []

    with f.open() as f_o:
        numbers = [int(s) for s in f_o.readlines()]

    critical_n = -1
    for n in numbers:
        found = False
        if len(buffer) < L_PREAMBLE:
            buffer.append(n)
            continue

        for s1 in buffer:
            for s2 in buffer:
                if s1 == s2:
                    continue

                if s1 + s2 == n:
                    del buffer[0]
                    buffer.append(n)
                    found = True
                    break

            if found:
                break

        if found:
            continue

        print(f'No values were found to sum {n}')
        critical_n = n
        break

    print('Searching for Critical N')
    if critical_n >= 0:
        for win_size in range(2, len(numbers)):

            print(f'{win_size = }')

            for i0 in range(win_size, len(numbers)):
                subset = numbers[i0:i0+win_size]
                print(subset)

                if sum(subset) == critical_n:
                    print(f'Identified sums for critical N {win_size = }')
                    print(f'{max(subset) + min(subset) = }')
                    return

    print('DONE')


if __name__ == '__main__':
    main()
