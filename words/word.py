#!/usr/bin/python
import argparse
import sys
import re
import os


def search(mask, has_chars=None, has_word=None):
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
            word = word.rstrip('\n')
            matches = True

            for char in has_chars or []:
                matches &= char in word
            if has_word:
                matches &= has_word in word
            if matches:
                if match_letter_count and len(word) == mask_chars and re.match(mask, word):
                    matching_words.append(word)
                elif not match_letter_count and mask in word:
                    matching_words.append(word)

    return matching_words


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('mask', help="The mask to search words with. (eg. 'wor..' results in 'words', 'worth', etc. ")
    parser.add_argument('-c', '--chars', help="word must include these characters")
    parser.add_argument('-w', '--word', help="word must include this word")
    return parser


def main(prog_args):
    parser = get_arg_parser()
    args = parser.parse_args(prog_args[1:])
    mask = args.mask
    print ('looking for {} {} {}'.format(mask,
                                         ', with {}'.format(args.chars) if args.chars else '',
                                         ', contains {}'.format(args.word) if args.word else ''
                                         ))
    matches = search(mask, args.chars, args.word)
    print ('found words:')
    for w in matches:
        print(w)

if __name__ == '__main__':
    sys.exit(main(sys.argv))