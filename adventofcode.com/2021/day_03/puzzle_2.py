#!/usr/bin/python3
import sys


def log_binary(number):
    print(f"{number:16b}: {number}")


def bit_not(n, numbits=8):
    return (1 << numbits) - 1 - n


def run(input_file):
    gamma_list = []
    code_list = []
    with open(input_file) as fp:
        for line in fp.readlines():
            code = line.rstrip('\n')
            code_list.append(int(code, base=2))
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

        oxygen_codes = code_list[:]
        c02_codes = code_list[:]

        digit_count = len(gamma_rate)
        one_mask = 2 ** digit_count - 1
        for i, c in enumerate(gamma_rate):
            pos = digit_count - i
            mask = int(2) ** (pos - 1)
            zero_mask = bit_not(mask, digit_count)
            if len(oxygen_codes) > 1:
                oxygen_codes_with_ones = [c for c in oxygen_codes if c & mask]
                oxygen_codes_with_zeros = [c for c in oxygen_codes if (c | zero_mask) ^ one_mask]
                oxygen_codes = oxygen_codes_with_ones if len(oxygen_codes_with_ones) >= len(
                    oxygen_codes_with_zeros) else oxygen_codes_with_zeros

            if len(c02_codes) > 1:
                c02_codes_with_ones = [c for c in c02_codes if c & mask]
                c02_codes_with_zeros = [c for c in c02_codes if (c | zero_mask) ^ one_mask]
                c02_codes = c02_codes_with_zeros if len(c02_codes_with_zeros) <= len(c02_codes_with_ones) else c02_codes_with_ones

        print(oxygen_codes[0] * c02_codes[0])


def log_codes(code_list, msg="codes"):
    print(msg)
    for code in code_list:
        log_binary(code)


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
