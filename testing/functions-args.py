#!/usr/bin/python
import os


def main():
    # my_function(1)
    # my_function(1, 'a', 2, 'bdef')
    my_function(1, drie=2, twee='a', vier='bdef')


def my_function(een, drie, *args, **kwargs):
    print "args:"
    print(args)
    print "kwargs:"
    print(kwargs)


main()