#!/home/cees/.virtualenvs/ceasaro_py/bin/python
import argparse
import csv
import os
import re
import sys


def search_plaatsnamen_NL(mask, has_chars=None, has_word=None, regex=False, ij_as_y=False, province_code=None):
    PROVINCES = {
        'DR': 'Drenthe',
        'FL': 'Flevoland',
        'FR': 'Fryslân',
        # 'FR': 'Friesland',
        'GD': 'Gelderland',
        'GR': 'Groningen',
        'LB': 'Limburg',
        'NB': 'Noord - Brabant',
        'NH': 'Noord - Holland',
        'OV': 'Overijssel',
        'UT': 'Utrecht',
        'ZH': 'Zuid - Holland',
        'ZL': 'Zeeland',
    }
    matching_words = []
    local_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(local_path, 'geografie/plaatsnamen_NL.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            city_code, city, len_city_name, zip_code, township, province = row
            if line_count == 0:
                # skip first row, contains only column names
                line_count += 1
            else:
                if not province_code or PROVINCES[province_code] == province:
                    for city_name in [city.split('/')[0]]:
                    # for city_name in city.split('/'):
                        city_name = city_name.strip().lower()
                        if word_matches(city_name, has_chars, has_word, ij_as_y, mask, regex):
                            matching_words.append(city_name)
                line_count += 1

    return matching_words


def search_open_taal(mask, has_chars=None, has_word=None, regex=False, ij_as_y=False):
    matching_words = []
    local_path = os.path.dirname(os.path.realpath(__file__))
    files = [
        os.path.join(local_path, 'opentaal-210G-woordenlijsten/OpenTaal-210G-basis-gekeurd.txt'),
        # os.path.join(local_path, 'opentaal-210G-woordenlijsten/OpenTaal-210G-basis-ongekeurd.txt'),
    ]
    for file_with_words in files:
        for word in open(file_with_words):
            original_word = word.rstrip('\n')
            if word_matches(original_word, has_chars, has_word, ij_as_y, mask, regex):
                matching_words.append(original_word)

    return matching_words


def word_matches(word, has_chars, has_word, ij_as_y, mask, regex):
    match_letter_count = '.' in mask
    mask_chars = len(mask)
    if ij_as_y:
        word = word.replace('ij', 'y')
    matches = True
    for char in has_chars or []:
        matches &= char in word
    if has_word:
        matches &= has_word in word
    if matches:
        if regex and re.match(mask, word):
            return True
        if match_letter_count and len(word) == mask_chars and re.match(mask, word):
            return True
        elif not match_letter_count and mask in word:
            return True
    return False


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('mask', help="The mask to search words with. (eg. 'wor..' results in 'words', 'worth', etc. ")
    parser.add_argument('-c', '--chars', help="word must include these characters")
    parser.add_argument('-w', '--word', help="word must include this word")
    parser.add_argument('-i', '--ij_as_y', help="treat the characters 'ij' as one letter", action='store_true')
    parser.add_argument('-r', '--regex', help="word must match the specified regular expression", action='store_true', )
    parser.add_argument('-p', '--province', help="Province code e.g. 'GR', 'LB', 'NH' (Only for city names)",)
    return parser


def main(prog_args):
    parser = get_arg_parser()
    args = parser.parse_args(prog_args[1:])
    mask = args.mask
    try:
        length = int(mask)
        mask = '.' * length
    except ValueError:
        pass
    print('looking for {} {} {}'.format(mask,
                                        ', with {}'.format(args.chars) if args.chars else '',
                                        ', contains {}'.format(args.word) if args.word else ''
                                        ))
    matches = search_open_taal(mask, args.chars, args.word, args.regex, args.ij_as_y)
    print('found words:')
    for w in matches:
        print("{w}    - https://www.google.com/search?q={w}".format(w=w))
    matched_cities = search_plaatsnamen_NL(mask, args.chars, args.word, args.regex, args.ij_as_y, args.province)
    print('found cities:')
    for w in matched_cities:
        print("{w}    - https://www.google.com/search?q={w}".format(w=w))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
