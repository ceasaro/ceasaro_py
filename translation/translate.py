#!/home/cees/.virtualenvs/ceasaro_py/bin/python
import argparse
import os
import sys
from factory import TranslatorFactory


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help="file or directory to translate", )
    parser.add_argument('-l', '--target_lang', help="language to translate to", )
    parser.add_argument('-s', '--source_lang', help="language of text to translate", )
    return parser


def main(prog_args):
    parser = get_arg_parser()
    args = parser.parse_args(prog_args[1:])
    file_path = args.file_path
    target_lang = args.target_lang
    source_lang = args.source_lang

    if os.path.isdir(file_path):
        for subdir, dirs, files in os.walk(file_path):
            for file in files:
                file_path = os.path.join(subdir, file)
                TranslatorFactory().translate_file(file_path, target_lang, source_lang=source_lang)
    elif os.path.isfile(file_path):
        print(f"{file_path} is a normal file")
    else:
        print(f"{file_path} is a special file (socket, FIFO, device file)")
    print()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
