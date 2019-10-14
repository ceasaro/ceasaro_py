import csv
import os

FILTER_OUT = {
    'desc': [
        'Jumbo', 'PRIMARK', 'Droppie', 'Coop', 'ARRIVA', 'Wes-Lee van Wieringen', 'Brave van Wieringen',
    ]
}


def desc_matches(desc, filter_words):
    for filter_word in filter_words:
        if filter_word in desc:
            return True


def analyse(ing_csv_file):
    filtered_transactions = []
    filtered_out_transactions = []
    with open(ing_csv_file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        filtered_transactions.append(next(csv_reader, None))  # skip the headers

        for row in csv_reader:
            date, desc, account_number, from_account, code, in_out, amount, mutation, notes = row
            if in_out == 'Bij' or desc_matches(desc, FILTER_OUT['desc']):
                filtered_out_transactions.append(row)
            else:
                filtered_transactions.append(row)

    return filtered_transactions, filtered_out_transactions


def write_csv_file(file_name, transactions):
    with open(file_name, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in transactions:
            csv_writer.writerow(row)

    print("csv file writen to {}".format(file_name))


def analyse_and_save(ing_csv_file):
    filtered, filtered_out = analyse(ing_csv_file)
    filename, file_extension = os.path.splitext(ing_csv_file)
    write_csv_file("{}-filtered{}".format(filename, file_extension), filtered)
    write_csv_file("{}-filtered_out{}".format(filename, file_extension), filtered_out)
