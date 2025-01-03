import datetime

import create_file
import lib


def main():
    print("Hello, advent adventurer!")

    now = datetime.datetime.now()

    if now < datetime.datetime(2025, 12, 1):
        print(f"Let's solve 2024's AoC ({lib.URL})!")

    started = []
    pending = []
    for i in range(1, 26):
        day_aoc = datetime.datetime(2024, 12, i)
        print(f"Day {i:2}", end=" ")

        if day_aoc > now:
            print("... Locked")
            continue

        if (lib.SOLUTIONS / f"day_{i:02}.py").exists():
            started.append(i)

        n_pending = 0
        for part in range(1, 3):
            if (lib.RESULTS / f"day_{i:02}_{part}.txt").exists():
                print("★", end=" ")
            else:
                print("☆", end=" ")
                n_pending += 1

        if n_pending == 0:
            print()
            continue

        if n_pending == 2:
            print(" (pending)", end="")
            pending.append(i)
        elif n_pending == 1:
            print(" (pending part 2)", end="")
            pending.append(i)

        print()

    print("Let's start adventuring! Choose a day to solve (1-25): ", end=" ")
    while True:
        try:
            day = int(input())
        except ValueError:
            print("Invalid day. Choose a day to solve (1-25): ", end=" ")
            continue
        except KeyboardInterrupt:
            print("Oh, ok.\nGoodbye, advent adventurer!")
            return

        if 1 <= day <= 25 and day in pending:
            break

        print("Invalid day. Choose a day to solve (1-25): ", end=" ")

    print(f"Let's solve day {day}!")

    create_file.create_files(day)

    print("Goodbye, advent adventurer!")


if __name__ == "__main__":
    main()
