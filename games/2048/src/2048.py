#!/usr/bin/env python
import sys
import lib.game_engine as engine
from lib.getch import getch
from lib.helper import quit_game
from lib.test import test_all


def print_help():
    """
    Prints this help message
    """
    for key in key_map:
        value = key_map[key]
        if type(value) == list:
            func_names_list = [func.__name__ for func in value if func is not None]
            func_names = ", ".join(func_names_list)
            print "{key}: {func_names}".format(key=key, func_names=func_names)
        else:
            print "{key}: {doc}".format(key=key, doc=value.__doc__)


def _key_mapper():
    return {
        'a': engine.add_random_number,
        'q': quit_game,
        'h': print_help,
        'p': engine.running_game.print_matrix,
        't': test_all,
        '[': engine.move_up,
        '\\': engine.move_right,
        "'": engine.move_down,
        ';': engine.move_left,
        '{': [engine.move_up, engine.running_game.print_matrix],
        '|': [engine.move_right, engine.running_game.print_matrix],
        '"': [engine.move_down, engine.running_game.print_matrix],
        ':': [engine.move_left, engine.running_game.print_matrix],
    }
key_map = _key_mapper()


def main(argv):
    print_help()
    # engine.add_random_number()
    engine.running_game.game_matrix[2][2].value = 2
    engine.running_game.print_matrix()
    key = ''
    while key != 'q':
        key = getch()

        if key in key_map.keys():
            value = key_map[key]
            if type(value) == list:
                for func in value:
                    func()
            else:
                value()
        else:
            print "unknown command '{0}', press 'q' to quit!".format(key)



if __name__ == '__main__':
    sys.exit(main(sys.argv))
