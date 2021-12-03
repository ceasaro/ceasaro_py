#!/usr/bin/python3
import argparse
import sys


def run(input_file):
    increases = 0
    values = []

    with open(input_file) as fp:
        for position, line in enumerate(fp.readlines()):
            value = int(line)
            if len(values) == 3:
                previous_sum = sum(values)
                values = values[1:]
                values.append(value)
                current_sum = sum(values)
                if current_sum > previous_sum:
                    increases += 1
            else:
                values.append(value)
    print(increases)


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
