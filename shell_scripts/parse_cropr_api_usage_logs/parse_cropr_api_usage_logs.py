#!/usr/bin/python
import operator
import os
import sys

import requests

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

    parse_django_log(fname)


def parse_django_log(fname):
    user_dict = {}
    path_dict = {}
    view_dict = {}
    remote_addr_dict = {}
    with open(fname) as infile:
        line_nr = 0
        for line in infile:
            line_nr += 1
            if line.startswith('INFO '):
                csv_line = line[5:]
                remote_addr, view, view_method, path, host, method, query_params, user, response_ms, status_code = \
                    csv_line.split(',')
                user_dict[user] = user_dict[user] + 1 if user in user_dict else 1
                path_dict[path] = path_dict[path] + 1 if path in path_dict else 1
                view_dict[view] = view_dict[view] + 1 if view in view_dict else 1
                remote_addr_stats(remote_addr_dict, remote_addr, user, view)
            else:
                print("unknown line in log file: {} at line {}".format(line, line_nr))

        # print_user_stats(user_dict)
        # print_path_stats(path_dict)
        # print_view_stats(view_dict)
        print_remote_addr_stats(remote_addr_dict)


def print_view_stats(view_dict, prefill=0):
    views = sorted(view_dict.items(), key=operator.itemgetter(1), reverse=True)
    prefill = ' ' * prefill
    print("\n{}Views".format(prefill))
    for view, count in views:
        print("{prefill}{count:<10}: {view}".format(prefill=prefill, count=count, view=view))


def print_path_stats(path_dict):
    paths = sorted(path_dict.items(), key=operator.itemgetter(1), reverse=True)
    print("\n paths")
    for path, count in paths:
        print("{} = {}".format(path, count))


def print_user_stats(user_dict, prefill=0):
    users = sorted(user_dict.items(), key=operator.itemgetter(1), reverse=True)
    prefill = ' ' * prefill
    print("\n{}Users".format(prefill))
    for user, count in users:
        print("{prefill}{count:<10}: {user}".format(prefill=prefill, count=count, user=user))


def remote_addr_stats(remote_addr_dict, remote_addr, user, view):
    if remote_addr not in remote_addr_dict:
        remote_addr_dict[remote_addr] = {
            'count': 0,
            'user_dict': {},
            'view_dict': {},
        }
    remote_addr_dict[remote_addr]['count'] += 1
    r_user_dict = remote_addr_dict[remote_addr]['user_dict']
    r_view_dict = remote_addr_dict[remote_addr]['view_dict']
    r_user_dict[user] = r_user_dict[user] + 1 if user in r_user_dict else 1
    r_view_dict[view] = r_view_dict[view] + 1 if view in r_view_dict else 1


def print_remote_addr_stats(remote_addr_dict):
    ips = sorted(remote_addr_dict.items(), key=lambda x: x[1].get('count'), reverse=True)
    # print("\n remote addresses")
    for remote_addr, stats in ips:
        location_resp = requests.get('http://ip-api.com/json/{}'.format(remote_addr))
        location = location_resp.json()
        """
        location example
        {
          "status": "success",
          "country": "United States",
          "countryCode": "US",
          "region": "CA",
          "regionName": "California",
          "city": "San Francisco",
          "zip": "94105",
          "lat": "37.7898",
          "lon": "-122.3942",
          "timezone": "America\/Los_Angeles",
          "isp": "Wikimedia Foundation",
          "org": "Wikimedia Foundation",
          "as": "AS14907 Wikimedia US network",
          "query": "208.80.152.201"
        }
        """
        print(''.rjust(80, '-'))
        location_str = "{org}, {city} - {country} ({ip})".format(ip=remote_addr, **location)
        print("{count:>10}: {location:<40}".format(count=stats.get('count'), location=location_str))
        print_user_stats(stats.get('user_dict'), prefill=10)
        print_view_stats(stats.get('view_dict'), prefill=10)
        print("\n\n")


def parse_curropt_psql_export(fname):
    with open(fname) as infile:
        write('IP,DATE_TIME,METHOD,PATH,PROTOCOL,STATUS_CODE,RESPONSE_MS,REFERER\n')
        for line in infile:
            # for char in line:
            line = line.strip()
            if line:
                split_quotes = line.split('"')
                ls = split_quotes[0].split('[')
                # sys.stdout.write(ls[0])
                write(ls[0].split(' ')[0])  # IP
                write(',')
                write(ls[1].split(' ')[0])  # DATE_TIME
                method_path_protocol = split_quotes[1].split(' ')
                write(',')
                write(method_path_protocol[0])  # METHOD
                write(',')
                write(method_path_protocol[1])  # PATH
                write(',')
                write(method_path_protocol[2])
                code_and_ms = split_quotes[2].strip().split(' ')
                write(',')
                write(code_and_ms[0])  # STATUS_CODE
                write(',')
                write(code_and_ms[1])  # RESPONSE_MS
                write(',')
                write(split_quotes[3])  # REFERER
                write('\n')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
