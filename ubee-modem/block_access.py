#!/usr/bin/python
import argparse
import sys

import requests


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help="Username to login on ubee.")
    parser.add_argument('-p', '--password', help="Password to login on ubee.")
    parser.add_argument('--url', help="ip address of ubee modem.", default='http://192.168.178.1/')
    return parser


class UbeeModem():
    LOGIN_PATH = 'goform/loginMR4'

    def __init__(self, url, username, password):
        self.session = requests.Session()
        self.url = url
        self.username = username
        self.password = password

    def login(self):
        print ('loging into ubee at {}'.format(self.url))
        resp = self.session.post(UbeeModem.LOGIN_PATH,
                                 {
                                     'loginUsername': self.username,
                                     'loginPassword': self.password,
                                     # 'isTogglePasswordAction': 0,
                                     # 'MR4LoginApply': 'Doorgaan,
                                 })
        import pdb; pdb.set_trace()


def main(prog_args):
    parser = get_arg_parser()
    args = parser.parse_args(prog_args[1:])
    ubee = UbeeModem(args.url, args.username, args.password)
    ubee.login()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
