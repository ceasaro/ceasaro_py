#!/usr/bin/python3
import sys


def run(input_file):
    with open(input_file) as fp:
        horizontal = 0
        depth = 0
        for line in fp.readlines():
            move, positions = line.rstrip('\n').split(' ')
            positions = int(positions)
            if move == 'forward':
                horizontal += positions
            elif move == 'down':
                depth += positions
            elif move == 'up':
                depth -= positions
        print(f"{horizontal} * {depth} = {horizontal * depth}")


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
