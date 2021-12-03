#!/usr/bin/python3
import sys


def run(input_file):
    with open(input_file) as fp:
        for line in fp.readlines():
            print(line)


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
