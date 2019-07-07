#!/usr/bin/python
import argparse
import sys
import re
import os


def search(mask, has_chars=None, has_word=None, regex=False, ij_as_y=False):
    matching_words = []
    match_letter_count = '.' in mask
    mask_chars = len(mask)
    local_path = os.path.dirname(os.path.realpath(__file__))
    files = [
        os.path.join(local_path, 'opentaal-210G-woordenlijsten/OpenTaal-210G-basis-gekeurd.txt'),
        # os.path.join(local_path, 'opentaal-210G-woordenlijsten/OpenTaal-210G-basis-ongekeurd.txt'),
    ]
    for file_with_words in files:
        for word in open(file_with_words):
            original_word = word.rstrip('\n')
            word = original_word.replace('ij', 'y') if ij_as_y else original_word
            matches = True
            for char in has_chars or []:
                matches &= char in word
            if has_word:
                matches &= has_word in word
            if matches:
                if regex and re.match(mask, word):
                    matching_words.append(original_word)
                if match_letter_count and len(word) == mask_chars and re.match(mask, word):
                    matching_words.append(original_word)
                elif not match_letter_count and mask in word:
                    matching_words.append(original_word)

    return matching_words


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('mask', help="The mask to search words with. (eg. 'wor..' results in 'words', 'worth', etc. ")
    parser.add_argument('-c', '--chars', help="word must include these characters")
    parser.add_argument('-w', '--word', help="word must include this word")
    parser.add_argument('-i', '--ij_as_y', help="treat the characters 'ij' as one letter", action='store_true')
    parser.add_argument('-r', '--regex', help="word must match the specified regular expression", action='store_true',)
    return parser


def main(prog_args):
    parser = get_arg_parser()
    args = parser.parse_args(prog_args[1:])
    mask = args.mask
    print ('looking for {} {} {}'.format(mask,
                                         ', with {}'.format(args.chars) if args.chars else '',
                                         ', contains {}'.format(args.word) if args.word else ''
                                         ))
    matches = search(mask, args.chars, args.word, args.regex, args.ij_as_y)
    print ('found words:')
    for w in matches:
        print(w)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
