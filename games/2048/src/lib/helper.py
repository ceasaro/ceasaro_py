import sys
from lib.models import Cell


def remove_empty_cells(list_of_cells):
    return [c for c in list_of_cells if not c.empty]


def accumulate_neighbours(list_of_cells):
    new_list = []
    if len(list_of_cells) <= 1:
        return list_of_cells
    elif list_of_cells[0].value == list_of_cells[1].value:
        c = Cell()
        c.value = list_of_cells[0].value + list_of_cells[1].value
        return [c] + accumulate_neighbours(list_of_cells[2:])
    else:
        return [list_of_cells[0]] + accumulate_neighbours(list_of_cells[1:])


def quit_game(msg=None):
    """
    Quits the game
    """
    if msg:
        print "---------------------------"
        print "> {0}".format(msg)
    print "ByeBye ... "
    sys.exit()
