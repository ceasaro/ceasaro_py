#!/usr/bin/python
# coding=utf-8
import argparse
import calendar
import csv
import os
import sys
from datetime import datetime

__version__ = '0.1'

costs_business_traffic = 0
accounts = []
creditors = []
debtors = []
total_in = 0
total_out = 0



class Client(object):

    def __init__(self, name, account_numbers):
        super(Client, self).__init__()
        self.name = name
        self.account_numbers = account_numbers if isinstance(account_numbers, list) else [account_numbers]
        self.accounts = []

    def has_account_number(self, account_number):
        return account_number in self.account_numbers

    def get_account(self, account_number):
        return next((a for a in self.accounts if a.account_number == account_number), None)

    def add_account(self, account):
        self.accounts.append(account)

    @property
    def total_in(self):
        return sum(a.total_in for a in self.accounts)

    @property
    def total_out(self):
        return sum(a.total_out for a in self.accounts)

    def __str__(self):
        return "Client({})".format(self.name)

    def __repr__(self):
        return "Client({})".format(self.name)


class Account(object):

    def __init__(self, account_number, desc):
        super(Account, self).__init__()
        self.account_number = account_number
        self.desc = desc
        self.total_in = 0
        self.total_out = 0

    def add_transaction(self, date, code, in_out, amount, mutation, notes):
        if in_out == 'Bij':
            self.total_in += amount
        if in_out == 'Af':
            self.total_out += amount

    def __eq__(self, other):
        return self.account_number == other.account_number

    def __str__(self):
        return "Account({}, {})".format(self.account_number, self.desc)

    def __repr__(self):
        return "Account({})".format(self.account_number)


def get_client_by_account(account):
    for client in creditors + debtors:
        if client.has_account_number(account.account_number):
            return client


def order_by_out(_accounts, reverse=True):
    return sorted(_accounts, key=lambda a: a.total_out, reverse=reverse)


def order_by_in(_accounts, reverse=True):
    return sorted(_accounts, key=lambda a: a.total_in, reverse=reverse)


def str_to_date(start_date_str):
    try:
        return datetime.strptime(start_date_str, '%d-%m-%Y')
    except ValueError:
        return datetime.strptime(start_date_str, '%Y%m%d')


def analyse_csv_file(ing_csv_file, start_date=None, end_date=None):
    global total_in
    global total_out
    global costs_business_traffic
    with open(ing_csv_file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(csv_reader, None)  # skip the headers

        for row in csv_reader:
            date, desc, account_number, from_account, code, in_out, amount, mutation, notes = row
            date = str_to_date(date)
            if start_date <= date <= end_date:
                amount = float(amount.replace(',', '.'))
                if code == 'DV':
                    costs_business_traffic += amount
                account = next((a for a in accounts if a.account_number == from_account),
                               next((c.get_account(from_account) for c in (creditors+debtors) if c.has_account_number(from_account)), None)
                               )
                if not account:
                    account = Account(from_account, desc)
                    client = get_client_by_account(account)
                    if client:
                        client.add_account(account)
                    else:
                        accounts.append(account)

                if in_out == "Bij":
                    total_in += amount
                if in_out == "Af":
                    total_out += amount
                account.add_transaction(date, code, in_out, amount, mutation, notes)


def init_clients():
    creditors.append(Client('Groendaktotaal', 'NL73ABNA0627226078'))
    creditors.append(Client('Kingbee BV', 'NL79INGB0004309860'))
    creditors.append(Client('Tooltrac LTD',
                            ['NL03BUNQ2291341480', 'NL40ASNB0942657403', 'NL52SNSB0858861860', 'NL94INGB0005717933']))
    creditors.append(Client('ULRIC BEHEER BV', 'NL44INGB0670476323'))
    creditors.append(Client('Make-A-Wish Nederland', ['NL48RABO0366021222', 'NL48RABO0366004344']))
    creditors.append(Client('The Online Media Company', 'NL11INGB0006559738'))
    creditors.append(Client('Karper-Camping', 'NL86RABO0304490237'))

    debtors.append(Client('Belastingdienst', 'NL86INGB0002445588'))
    debtors.append(Client('Prive rekening yasmine', 'NL49INGB0752540173'))
    debtors.append(Client('Aflossing hypotheek', 'NL37INGB0007726083'))
    # debtors.append(Client('', ''))
    debtors.append(Client('CAROLINE VAN STAVEREN', 'NL74INGB0004523059'))
    debtors.append(Client('Sara', 'NL04ABNA0442858353'))
    debtors.append(Client('PPRO Financial Ltd', 'DE42700111104107387000'))
    debtors.append(Client('A Elamine', 'NL22INGB0002893134'))
    debtors.append(Client('VODAFONE LIBERTEL B.V.', 'NL83DEUT0265121817'))
    debtors.append(Client('PayPal (Europe) S.a.r.l. et Cie., S.C.A.)', 'DE88500700100175526303'))
    debtors.append(Client('GEEN TEGEN NUMMER', ''))


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    parser.add_argument('-m', '--month_year',
                        help="Only use transaction within this month year. eg -m 08-2018")
    parser.add_argument('-a', '--accounts_out', default=0,
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
    init_clients()
    analyse_csv_file(ing_csv_file, start_date, end_date)
    print_result(context)


def print_result(context):
    print("\n\n\n")
    print("Account: {}".format(context['own_account_number']))
    start_date = context['start_date'].strftime("%d %B %Y")
    end_date = context['end_date'].strftime("%d %B %Y")
    print("From {} to {}".format(start_date, end_date))
    print("\n")
    print("Total")
    print(u"in:  € {:.2f}".format(total_in))
    print(u"out: € {:.2f}".format(total_out))
    print("\n")
    print("Creditors:")
    print("==============")
    creditor_total_in = 0
    for creditor in order_by_in(creditors):
        print(u"{:<50} € {:.2f}".format(creditor.name, creditor.total_in))
        creditor_total_in += creditor.total_in
    print("--------------")
    print("{:<50} € {:.2f}".format("TOTAAL", creditor_total_in))
    print("")
    print("Debtors:")
    print("==============")
    debtor_total_out = costs_business_traffic
    print(u"{:<50} € {:.2f}".format('Kosten zakelijk betalingsverkeer', costs_business_traffic))

    for debtor in order_by_out(debtors):
        print(u"{:<50} € {:.2f}".format(debtor.name, debtor.total_out))
        debtor_total_out += debtor.total_out
    print("--------------")
    print("{:<50} € {:.2f}".format("TOTAAL", debtor_total_out))
    if context['accounts_to_print'] > 0:
        print("\n")
        print("{} highest creditor accounts".format(context['accounts_to_print']))
        print("==============")
        for account in order_by_in(accounts)[:context['accounts_to_print']]:
            print("{:<60} € {:.2f}".format(account.account_number + " " + account.desc, account.total_in))

    if context['accounts_to_print'] > 0:
        print("\n")
        print("{} highest debtor accounts".format(context['accounts_to_print']))
        print("==============")
        for account in order_by_out(accounts)[:context['accounts_to_print']]:
            print("{:<60} € {:.2f}".format(account.account_number + " " + account.desc, account.total_out))


if __name__ == '__main__':
    sys.exit(main())
