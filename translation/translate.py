#!/home/cees/.virtualenvs/ceasaro_py/bin/python
import argparse
import sys

import deepl_api
import csv_handler


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help="file to translate",)
    parser.add_argument('-l', '--target_lang', help="language to translate to",)
    return parser


def main(prog_args):
    parser = get_arg_parser()
    args = parser.parse_args(prog_args[1:])
    file = args.file
    target_lang = args.target_lang
    print(f"translating {file} to {target_lang}")
    if file.endswith('.csv'):
        csv_handler.translate(file, columns_to_translate=[1, ])
    # resp = deepl_api.translate('Werkt het nu?', target_lang=target_lang)
    # print(resp)
    # print(resp.json())


if __name__ == '__main__':
    sys.exit(main(sys.argv))
