#!/usr/bin/python3
import sys
import statistics


def run(input_file):
    positions = []
    with open(input_file) as fp:
        for line in fp.readlines():
            positions = [int(p) for p in line.rstrip('\n').split(',')]
    positions.sort()
    print(f" fuel_costs puzzle 1: {least_fuel_puzzle_1(positions)}")
    print(f" fuel_costs puzzle 2: {least_fuel_puzzle_2(positions)}")


def least_fuel_puzzle_1(crabs):
    median = statistics.median(crabs)
    fuel_costs = 0
    for crab in crabs:
        fuel_costs += abs(crab - median)
    return fuel_costs


def least_fuel_puzzle_2(crabs):
    least_fuel = None
    for x in range(0, len(crabs)):
        fuel_costs = fuel_costs_puzzle_2(crabs, x)
        if least_fuel is None:
            least_fuel = fuel_costs
        else:
            if fuel_costs < least_fuel:
                least_fuel = fuel_costs
            else:
                break
    return least_fuel


def triangular_number(n):
    return n * (n + 1) / 2


def fuel_costs_puzzle_2(crabs, position):
    fuel_costs = 0
    for crab in crabs:
        moves = abs(crab - position)
        fuel_costs += triangular_number(moves)
    return fuel_costs


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
