#!/usr/bin/python3
import sys


def run(input_file):
    gamma_list = []
    code_list = []
    with open(input_file) as fp:
        for line in fp.readlines():
            code = line.rstrip('\n')
            for i, bit in enumerate(code):
                count = 1 if bit == '1' else -1
                if len(gamma_list) != len(code):
                    gamma_list.append(count)
                else:
                    gamma_list[i] += count
        gamma_rate = ''
        epsilon_rate = ''
        for one_count in gamma_list:
            if one_count > 0:
                gamma_rate += '1'
                epsilon_rate += '0'
            else:
                gamma_rate += '0'
                epsilon_rate += '1'
        gamma_rate_value = int(gamma_rate, base=2)
        epsilon_rate_value = int(epsilon_rate, base=2)
        print(f" {gamma_rate_value} * {epsilon_rate_value} = {gamma_rate_value * epsilon_rate_value}")


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
