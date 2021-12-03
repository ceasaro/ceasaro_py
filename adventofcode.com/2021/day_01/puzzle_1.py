#!/usr/bin/python3
import argparse
import sys


def run(input_file):
    previous = None
    increases = 0
    with open(input_file) as fp:
        for line in fp.readlines():
            value = int(line)
            if previous is not None and value > previous:
                increases += 1
            previous = value
    print(increases)


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
