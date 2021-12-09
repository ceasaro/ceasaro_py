#!/usr/bin/python3
import sys


def offspring(fish_per_age, days):
    # print(f"start {fish_per_age}")

    for day in range(days):
        new_fish = fish_per_age[0]
        for age in range(len(fish_per_age)):
            if age == 6:
                fish_per_age[age] = fish_per_age[age + 1] + new_fish
            elif age == 8:
                fish_per_age[age] = new_fish
            else:
                fish_per_age[age] = fish_per_age[age+1]
    print(sum(fish_per_age))


def run(input_file):
    fish_per_age = [0] * 9
    with open(input_file) as fp:
        for line in fp.readlines():
            for fish_age_str in line.rstrip('\n').split(','):
                fish_per_age[int(fish_age_str)] += 1
    print("puzzle 1")
    offspring(fish_per_age.copy(), 80)  # puzzle 1
    print("puzzle 2")
    offspring(fish_per_age.copy(), 256)  # puzzle 2


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
