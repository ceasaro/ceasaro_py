#!/home/cees/.virtualenvs/ceasaro_py/bin/python
import argparse
import json
import os
import sys
from factory import TranslatorFactory


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', help="file or directory to translate", )
    parser.add_argument('-l', '--target_lang', help="language to translate to", )
    parser.add_argument('-s', '--source_lang', help="language of text to translate", )
    return parser

def write(msg=''):
    print(msg)

def parse_page(page_json):
    def key_write(json_data, json_key):
        write(json_data.get(json_key) or '')

    key_write(page_json, 'title')
    write("HEADER")
    write("----------------------------------------------------------------")
    write("TITLE:")
    key_write(page_json, 'field_header_title')
    write("SUBTITLE:")
    key_write(page_json, 'field_subtitle')
    write()
    write("META")
    write("TITLE:")
    key_write(page_json.get('field_metatags', {}), 'title')
    write("DESCRIPTION:")
    key_write(page_json.get('field_metatags', {}), 'description')
    write()
    write()
    write("FIELD WIDGETS")
    for widget in page_json.get('field_widgets', []):
        write('TITLE:')
        key_write(widget, "field_title")
        write('TEXT:')
        key_write(widget, "field_text")
        write('-------------------------------------')
        write()
        for block in widget.get('field_blocks', []):
            write("FIELD BLOCKS")
            write('TITLE:')
            key_write(block, "field_title")
            write('TEXT:')
            key_write(block, "field_text")
            write('-------------------------------------')
            write()


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
                if file_path.endswith('.json'):
                    print(os.path.basename(file_path))
                    with open(file_path) as f:
                        parse_page(json.loads(f.read()))

    elif os.path.isfile(file_path):
        print(f"{file_path} is a normal file")
    else:
        print(f"{file_path} is a special file (socket, FIFO, device file)")
    print()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
