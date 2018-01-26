#!/usr/bin/python
import argparse
import os
import sys
__version__ = '0.1'
import PIL.Image

import subprocess


EXIF_TAG_DATE_TIME = 306
EXIF_TAG_DATE_TIME_ORIGINAL = 36867


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default='.',
                        help="Directory with photos")
    # parser.add_argument('-t', '--test', nargs='?',
    #                     help="run the units tests, a python test path can be added as value. "
    #                          "e.g. -t TestDebianSysInfo.test_get_disk_info")
    return parser


def main(prog_args):
    parser = get_arg_parser()
    args = parser.parse_args(prog_args[1:])
    new_dir = os.path.join(args.dir, 'RENAMED')
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    for fn in os.listdir(args.dir):
        file_path = os.path.join(args.dir, fn)
        if os.path.isfile(file_path):
            img = PIL.Image.open(file_path)
            exif_data = img._getexif()
            if exif_data:
                dt = exif_data.get(EXIF_TAG_DATE_TIME) or exif_data.get(EXIF_TAG_DATE_TIME_ORIGINAL)
                if dt and len(dt) == 19:
                    new_file_name = dt[:4] + '-' + dt[5:7] + '-' + dt[8:10] + '_' + dt[11:]
                    try:
                        os.rename(file_path, os.path.join(new_dir, new_file_name))
                    except TypeError:
                        print ("ERROR {}: {}".format(fn, exif_data))
                else:
                    print ("UNKNOWN {}: {}".format(fn, exif_data))
            else:
                print ("UNKNOWN {}".format(fn))

if __name__ == '__main__':
    sys.exit(main(sys.argv))