#!/usr/bin/python
import sys
import urllib2

from bs4 import BeautifulSoup

STUDIO_EVENAAR_URL = 'http://www.studio-evenaar.nl/parken/register.php'


def main(prog_args):
    page = urllib2.urlopen(STUDIO_EVENAAR_URL).read()
    soup = BeautifulSoup(page, 'html.parser')
    register_table = soup.find_all('table')[3]
    for tr in register_table.find_all('tr'):
        print (tr.find('a').text)


if __name__ == '__main__':
    sys.exit(main(sys.argv))