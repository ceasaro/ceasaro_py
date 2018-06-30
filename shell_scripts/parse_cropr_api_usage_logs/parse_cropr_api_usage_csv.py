#!/usr/bin/python
import os
import sys

write = sys.stdout.write

IP = 0
DATE_TIME = 1
METHOD = 2
PATH = 3
PROTOCOL = 4
STATUS_CODE = 5
RESPONSE_MS = 6
REFERER = 7



def quit(msg=None):
    print (msg)
    exit(0)


def main(prog_args):
    if len(prog_args) < 2:
        quit("Please specify a file name: {} [FILE_NAME]".format(__name__))
    fname = prog_args[1]
    if not os.path.isfile(fname):
        quit("{} is not a file".format(fname))

    path_dict = {}
    with open(fname) as infile:
        for line in infile:
            try:
                ip, date_time, method, path, protocol, status_code, response_ms, referer = line.split(',')
                try:
                    path_dict[path] += 1
                except KeyError:
                    path_dict[path] = 1
            except Exception as e:
                print("error handling line:\n {}\n\n cause:\n{}".format(line, e.message))

        for key, value in path_dict.iteritems():
            print("{} = {}".format(key, value))

if __name__ == '__main__':
    sys.exit(main(sys.argv))