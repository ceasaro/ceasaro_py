#!/usr/bin/python3
# coding=utf-8
import argparse
import csv
import json
import sys
from datetime import datetime


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    return parser


def parse_csv(csv_file):
    with open(csv_file, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csv_reader:
            for col in row:
                if '@' in col:
                    for email in col.split(','):
                        print(email.strip())


def main():
    parser = get_arg_parser()
    args = parser.parse_args()
    json_file = args.file
    with open(json_file) as json_data:
        data = json.load(json_data)
        meta = [m['key'] for m in data.get('meta')]

        print(f"date time, timestamp, {','.join(meta)}")
        for measurement in data.get('measurements'):
            timestamp = int(measurement.get('timestamp'))
            print(f"{timestamp}, {datetime.utcfromtimestamp(timestamp)}, {','.join(map(str, measurement.get('values')))}")

if __name__ == '__main__':
    sys.exit(main())
