#!/usr/bin/python
# coding=utf-8
import os
import sys
# add the parent dir of this script to the python path
from financial import debtors_creditors, filter_jeslee_transactions

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import argparse

__version__ = '0.1'


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    return parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    ing_csv_file = args.csv_file
    filter_jeslee_transactions.analyse_and_save(ing_csv_file)


if __name__ == '__main__':
    sys.exit(main())

