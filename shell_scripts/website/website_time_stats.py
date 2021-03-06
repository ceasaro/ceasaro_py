#!/usr/bin/python
import argparse
import atexit
import getpass
import os
import sys
from datetime import datetime
from time import sleep
from lib.google import create_line_chart
from lib.utils import parse_time

__version__ = '0.1'

import subprocess
from lib import console, stats

# get file name './website_time_stats.py' --> website_time_stats
from lib.exceptions import ScriptAlreadyRunningException, WebsiteException

SYSTEM_USER = getpass.getuser()
SCRIPT_NAME = os.path.split(__file__)[1].split('.')[0]
PID_FILE = os.path.expanduser('/run/{0}.pid'.format(SCRIPT_NAME)) \
    if SYSTEM_USER == 'root'\
    else os.path.expanduser('~/.{0}.pid'.format(SCRIPT_NAME))


def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="The url to measure.")
    parser.add_argument('-i', '--interval', default='10s',
                        help="Time interval between polling e.g. 5s, 1m, 1h10m30s. Default: 10s")
    parser.add_argument('-t', '--time',
                        help="The time to run this script e.g. 1h10m30s, 2m, 5s")
    parser.add_argument('-g', '--graph', action='store_true',
                        help="Create a html file with a google graph of the recorded data")
    parser.add_argument('--graph-file', default='google-line-chart.html',
                        help="name of the google graph html file "
                        )
    # parser.add_argument('-t', '--test', nargs='?',
    #                     help="run the units tests, a python test path can be added as value. "
    #                          "e.g. -t TestDebianSysInfo.test_get_disk_info")
    return parser


def pid_running(pid):
    # grep -v grep --> to filter out the grep process
    p = subprocess.Popen('ps auxww | grep {0} | grep -v grep'.format(pid),
                         shell=True, stdout=subprocess.PIPE)
    return str(pid) in p.stdout.read()


def create_pid():
    if os.path.exists(PID_FILE):
        pid = open(PID_FILE).read()
        if pid_running(pid):
            raise ScriptAlreadyRunningException("A {0} script is already running, "
                                                "can only run one instance a time".format(SCRIPT_NAME))
    p_file = open(PID_FILE, 'w')
    p_file.write(str(os.getpid()))
    os.chmod(PID_FILE, 0600)


def remove_pid():
    os.remove(PID_FILE)


def cleanup():
    console.log("\n\n{0} stopped, cleaning up\n".format(SCRIPT_NAME))
    remove_pid()


def main(prog_args):
    atexit.register(cleanup)
    try:
        create_pid()
        parser = get_arg_parser()
        args = parser.parse_args(prog_args[1:])
        if args.time:
            all_data = []
            iteration_interval = parse_time(args.interval)
            time_delta = parse_time(args.time)
            stop_loop_at_time = datetime.now() + time_delta
            while datetime.now() < stop_loop_at_time:
                start_iteration = datetime.now()
                iteration_time_left = iteration_interval - (datetime.now() - start_iteration)
                time_stats = stats.load_time(args.url)
                all_data.append(time_stats)
                sleep_time = iteration_time_left if iteration_time_left.seconds > 0 else 0
                sleep(sleep_time.seconds)

            if args.graph:
                create_line_chart(all_data, html_output_file=args.graph_file)
                console.log(all_data)
            else:
                console.log(all_data)

        else:
            time_stats = stats.load_time(args.url)
            console.log(time_stats)

    except ScriptAlreadyRunningException, e:
        console.error(e)
        os._exit(0)  # exit the script without cleaning up,
                     # cause the script that's already running should do his own cleaning.
    except WebsiteException, e:
        console.error(e)
    except KeyboardInterrupt, e:
        pass


if __name__ == '__main__':
    sys.exit(main(sys.argv))