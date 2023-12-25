# coding=utf-8
import csv

from financial.date_utils import str_to_date
from financial.models import Account, Client

costs_business_traffic = 0
accounts = []
creditors = []
debtors = []
total_in = 0
total_out = 0


def get_client_by_account(account):
    for client in creditors + debtors:
        if client.has_account_number(account.account_number):
            return client


def order_by_out(_accounts, reverse=True):
    return sorted(_accounts, key=lambda a: a.total_out, reverse=reverse)


def order_by_in(_accounts, reverse=True):
    return sorted(_accounts, key=lambda a: a.total_in, reverse=reverse)


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
            # import pdb; pdb.set_trace()
            if start_date <= date <= end_date:
                amount = float(amount.replace(',', '.'))
                if code == 'DV':
                    costs_business_traffic += amount
                account_name = from_account or code
                account = next((a for a in accounts if a.account_number == account_name),
                               next((c.get_account(account_name) for c in (creditors+debtors) if c.has_account_number(account_name)), None)
                               )
                if not account:
                    account = Account(account_name, desc)
                    client = get_client_by_account(account)
                    if client:
                        client.add_account(account)
                    else:
                        accounts.append(account)

                if in_out in ["Bij", 'Credit']:
                    total_in += amount
                if in_out in ["Af", "Debit"]:
                    total_out += amount
                account.add_transaction(date, code, in_out, amount, mutation, notes)


def init_clients():
    creditors.append(Client('JESLEE', 'NL51INGB0657750476'))
    # creditors.append(Client('Groendaktotaal', 'NL73ABNA0627226078'))
    # creditors.append(Client('Kingbee BV', 'NL79INGB0004309860'))
    # creditors.append(Client('Tooltrac LTD',
    #                         ['NL03BUNQ2291341480', 'NL40ASNB0942657403', 'NL52SNSB0858861860', 'NL94INGB0005717933']))
    # creditors.append(Client('ULRIC BEHEER BV', 'NL44INGB0670476323'))
    # creditors.append(Client('Make-A-Wish Nederland', ['NL48RABO0366021222', 'NL48RABO0366004344']))
    # creditors.append(Client('The Online Media Company', 'NL11INGB0006559738'))
    # creditors.append(Client('Karper-Camping', 'NL86RABO0304490237'))
    #
    # debtors.append(Client('Belastingdienst', 'NL86INGB0002445588'))
    # debtors.append(Client('Prive rekening yasmine', 'NL49INGB0752540173'))
    # debtors.append(Client('Aflossing hypotheek', 'NL37INGB0007726083'))
    # # debtors.append(Client('', ''))
    # debtors.append(Client('CAROLINE VAN STAVEREN', 'NL74INGB0004523059'))
    # debtors.append(Client('Sara', 'NL04ABNA0442858353'))
    # debtors.append(Client('PPRO Financial Ltd', 'DE42700111104107387000'))
    # debtors.append(Client('A Elamine', 'NL22INGB0002893134'))
    # debtors.append(Client('VODAFONE LIBERTEL B.V.', 'NL83DEUT0265121817'))
    # debtors.append(Client('PayPal (Europe) S.a.r.l. et Cie., S.C.A.)', 'DE88500700100175526303'))
    debtors.append(Client('GEEN TEGEN NUMMER', ''))


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


def analyse(ing_csv_file, context):
    init_clients()
    analyse_csv_file(ing_csv_file, context['start_date'], context['end_date'])
    print_result(context)
