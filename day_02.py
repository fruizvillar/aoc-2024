from pathlib import Path

INPUTS = Path('inputs')

DAY = 2

f = INPUTS / f'day_{DAY:02d}.txt'


def main():
    count_ok_1 = 0
    count_ok_2 = 0

    for line in f.open().readlines():
        n_0, n_1, letter, passwd = parse_line_info(line)

        if check_pass_valid_rule1(n_0, n_1, letter, passwd):
            count_ok_1 += 1
        if check_pass_valid_rule2(n_0, n_1, letter, passwd):
            count_ok_2 += 1

    print(f'{count_ok_1} passwords were valid according to rule 1')
    print(f'{count_ok_2} passwords were valid according to rule 2')


def parse_line_info(line: str):
    interval, letter_colon, passwd = line.split(' ')
    i_i, i_f = interval.split('-')
    return int(i_i), int(i_f), letter_colon[0], passwd[:-1]


def check_pass_valid_rule1(n_min, n_max, letter, passwd):
    n = passwd.count(letter)
    ok = n_min <= n <= n_max
    # print(f"N of '{letter}' in {passwd:>20s} = {n:2}. || {n_min:2} <= {n:2} <= {n_max:2} ?? -> {ok}")
    return ok


def check_pass_valid_rule2(n0, n1, letter, passwd):
    ok = (passwd[n0 - 1] == letter) ^ (passwd[n1 - 1] == letter)
    # print(f" Chars {n0:2} ^ {n1:2} of {passwd:>20s} is '{letter}' ?? -> {ok}")

    return ok


if __name__ == '__main__':
    main()
