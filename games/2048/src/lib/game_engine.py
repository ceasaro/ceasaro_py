import random
from lib.helper import quit_game, remove_empty_cells, accumulate_neighbours
from lib.models import Cell, Game

running_game = Game()


def start_new_game():
    global running_game
    running_game = Game()


def add_random_number():
    """
    Add a random number to an empty place in the game
    """
    empty_cells = []
    for row in running_game.game_matrix:
        for cell in row:
            if cell.empty:
                empty_cells.append(cell)

    count = len(empty_cells)
    if count == 0:
        quit_game("No more valid places!")
    random_cell = empty_cells[random.randint(0, count - 1)]
    choices = [2, 2, 4]
    random_cell.value = choices[random.randint(0, len(choices)-1)]


def move_cells(row):
    """
    Move cells
    """
    cells = remove_empty_cells(row)
    cells = accumulate_neighbours(cells)
    empty_count = len(row) - len(cells)
    j = 0
    while j < empty_count:
        cells.append(Cell())
        j += 1
    return cells


def move_left():
    """
    Move numbers to the left
    """
    moved = False
    for i, row in enumerate(running_game.game_matrix):
        cells = move_cells(row)
        moved |= row != cells
        running_game.game_matrix[i] = cells
    if moved:
        add_random_number()


def move_right():
    """
    Move numbers to the right
    """
    moved = False
    for i, row in enumerate(running_game.game_matrix):
        print "row = {0}".format(row)
        row.reverse()
        cells = move_cells(row)
        moved |= row != cells
        cells.reverse()
        running_game.game_matrix[i] = cells
    if moved:
        add_random_number()


def move_up():
    """
    Move numbers up
    """
    moved = False
    matrix_transposed = zip(*running_game.game_matrix)
    for i, column in enumerate(matrix_transposed):
        column = list(column)
        cells = move_cells(column)
        moved |= column != cells
        matrix_transposed[i] = cells
    if moved:
        running_game.game_matrix = map(list, zip(*matrix_transposed))
        add_random_number()


def move_down():
    """
    Move numbers down
    """
    moved = False
    matrix_transposed = zip(*running_game.game_matrix)
    for i, column in enumerate(matrix_transposed):
        column = list(column)
        column.reverse()
        cells = move_cells(column)
        moved |= column != cells
        cells.reverse()
        matrix_transposed[i] = cells
    if moved:
        running_game.game_matrix = map(list, zip(*matrix_transposed))
        add_random_number()
