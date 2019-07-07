#!/usr/bin/python
# coding=utf-8
import argparse
import csv
import sys


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    return parser


def parse_csv(csv_file):
    with open(csv_file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            for col in row:
                if '@' in col:
                    for email in col.split(','):
                        print(email.strip())


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    csv_file = args.csv_file
    parse_csv(csv_file)


if __name__ == '__main__':
    sys.exit(main())
