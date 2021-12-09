#!/usr/bin/python3
import sys


def includes_digit_segments(digit_segments, includes_digit):
    return all(x in digit_segments for x in includes_digit)


def get_digit_mapping(input_digits):
    ordered = sorted(input_digits, key=lambda x: len(x))
    ordered = [''.join(sorted(o)) for o in ordered]
    zero = None  # 6 segments
    one = ordered[0]  # 2 segments, only one has 2 segments
    two = None  # 5 segments
    three = None  # 5 segments
    four = ordered[2]  # 4 segments, only four has 2 segments
    five = None  # 5 segments
    six = None  # 6 segments
    seven = ordered[1]  # 3 segments, only seven has 3 segments
    eight = ordered[9]  # 7 segments, only eight has 8 segments
    nine = None  # 6 segments, nine is the only digit that includes all 4 segments

    five_segment_digits = ordered[3:6]
    six_segment_digits = ordered[6:9]

    for six_seg_digit in six_segment_digits:
        if includes_digit_segments(six_seg_digit, four):
            nine = six_seg_digit
            six_segment_digits.remove(nine)
    if includes_digit_segments(six_segment_digits[0], one):
        zero = six_segment_digits[0]
        six = six_segment_digits[1]
    else:
        zero = six_segment_digits[1]
        six = six_segment_digits[0]

    for five_seg_digit in five_segment_digits:
        if includes_digit_segments(five_seg_digit, one):
            three = five_seg_digit
            five_segment_digits.remove(three)
    if includes_digit_segments(six, five_segment_digits[0]):
        five = five_segment_digits[0]
        two = five_segment_digits[1]
    else:
        five = five_segment_digits[1]
        two = five_segment_digits[0]

    return {
        zero: 0,
        one: 1,
        two: 2,
        three: 3,
        four: 4,
        five: 5,
        six: 6,
        seven: 7,
        eight: 8,
        nine: 9
    }


def run(input_file):
    puzzle_1_count = 0
    puzzle_2_count = 0
    with open(input_file) as fp:
        for line in fp.readlines():
            input_digits, ouput_digits = line.rstrip('\n').split('|')
            mapping = get_digit_mapping(input_digits.strip(' ').split(' '))
            digits = [mapping.get(''.join(sorted(digit))) for digit in ouput_digits.strip(' ').split(' ')]
            puzzle_1_count += len([d for d in digits if d in [1, 4, 7, 8]])
            puzzle_2_count += int(''.join([str(d) for d in digits]))

    print(f"puzzle 1: {puzzle_1_count}")
    print(f"puzzle 2: {puzzle_2_count}")


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
