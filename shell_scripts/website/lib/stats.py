# curl -o /dev/null -s -w  hq.getlogic.nl
import ast
import subprocess
import time
from lib.exceptions import WebsiteException
from lib.utils import convert_string

TIME_CONNECT_KEY = 'time_connect'
TIME_START_TRANSFER_KEY = 'time_start_transfer'
TIME_TOTAL_KEY = 'time_total'


def load_time(url, raw=False):
    """
    :param url: the url to measure
    :param raw: if True returns the raw string, otherwise a python dict is returned. default=False
    :return:
    """
    curl_output_format = \
        "{{'{tc}':'%{{time_connect}}','{ts}':'%{{time_starttransfer}}','{tt}':'%{{time_total}}'}}".\
            format(tc=TIME_CONNECT_KEY, ts=TIME_START_TRANSFER_KEY, tt=TIME_TOTAL_KEY)
    curl_process = subprocess.Popen('curl -o /dev/null -s -w "{output_format}" {url}'.
                                    format(output_format=curl_output_format, url=url),
                                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # check for errors
    curl_err = curl_process.stderr.read()
    if curl_err:
        raise WebsiteException(curl_err)

    curl_output = curl_process.stdout.read()
    if raw:
        return curl_output
    else:
        time_data = ast.literal_eval(curl_output)
        time_data[TIME_CONNECT_KEY] = convert_string(time_data[TIME_CONNECT_KEY].replace(',', '.'))
        time_data[TIME_START_TRANSFER_KEY] = convert_string(time_data[TIME_START_TRANSFER_KEY].replace(',', '.'))
        time_data[TIME_TOTAL_KEY] = convert_string(time_data[TIME_TOTAL_KEY].replace(',', '.'))
        time_data['timestamp'] = int(time.time() * 1000)
        return time_data

    # lines = curl_output.splitlines()