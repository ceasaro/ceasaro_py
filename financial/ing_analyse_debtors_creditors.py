#!/usr/bin/python
# coding=utf-8
import os
import sys
# add the parent dir of this script to the python path
from financial import debtors_creditors
from financial.date_utils import str_to_date

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import argparse
import calendar
from datetime import datetime

__version__ = '0.1'


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    parser.add_argument('-m', '--month_year',
                        help="Only use transaction within this month year. eg -m 08-2018")
    parser.add_argument('-a', '--accounts_out', default=20,
                        help="A number how many accounts should be printed. defaults to 20")
    return parser


def parse_filename(ing_csv_file):
    filename, file_extension = os.path.splitext(ing_csv_file)
    account_number, start_date_str, end_date_str = filename.split("_")
    return account_number, str_to_date(start_date_str), str_to_date(end_date_str)


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    accounts_to_print = int(args.accounts_out)
    ing_csv_file = args.csv_file
    own_account_number, transactions_start_date, transactions_end_date = parse_filename(ing_csv_file)
    if args.month_year:
        start_date = str_to_date("01-{}".format(args.month_year))
        end_date = datetime(day=calendar.monthrange(start_date.year, start_date.month)[1], month=start_date.month, year=start_date.year)
    else:
        start_date = transactions_start_date
        end_date = transactions_end_date
    context = {
        'own_account_number': own_account_number,
        'start_date': start_date,
        'end_date': end_date,
        'accounts_to_print': accounts_to_print,
    }
    debtors_creditors.analyse(ing_csv_file, context)


if __name__ == '__main__':
    sys.exit(main())

