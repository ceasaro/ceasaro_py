#!/usr/bin/python
__author__ = 'cvw'
"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells, each
of which is in one of two possible states, alive or dead. Every cell interacts with its eight neighbours,
 which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time,
 the following transitions occur:

 1) Any live cell with fewer than two live neighbours dies, as if caused by under-population.
 2) Any live cell with two or three live neighbours lives on to the next generation.
 3) Any live cell with more than three live neighbours dies, as if by overcrowding.
 4) Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

The initial pattern constitutes the seed of the system. The first generation is created by applying the above
rules simultaneously to every cell in the seed-births and deaths occur simultaneously, and the discrete
moment at which this happens is sometimes called a tick (in other words, each generation is a pure function
of the preceding one). The rules continue to be applied repeatedly to create further generations.
"""
LIVE_CELL = 'o'
DEAD_CELL = '.'
MAX_ROWS = 5
MAX_COLUMNS = 5
CYCLES = 15

life_matrix = [[DEAD_CELL for x in range(MAX_ROWS)] for y in range(MAX_COLUMNS)]
#Block still lives
# life_matrix[0][0] = LIVE_CELL
# life_matrix[0][1] = LIVE_CELL
# life_matrix[1][0] = LIVE_CELL
# life_matrix[1][1] = LIVE_CELL

# Blinker (period 2)
# life_matrix[1][1] = LIVE_CELL
# life_matrix[1][2] = LIVE_CELL
# life_matrix[1][3] = LIVE_CELL


# Glider
life_matrix[0][1] = LIVE_CELL
life_matrix[1][2] = LIVE_CELL
life_matrix[2][0] = LIVE_CELL
life_matrix[2][1] = LIVE_CELL
life_matrix[2][2] = LIVE_CELL


def main():
    global life_matrix
    cycle = 1
    while cycle <= CYCLES:
        print_matrix(cycle)
        life_matrix = get_next_generation()
        cycle += 1


def get_next_generation():
    next_generation_matrix = [[DEAD_CELL for x_n in range(MAX_ROWS)] for y_n in range(MAX_COLUMNS)]
    for r_i, row in enumerate(life_matrix):
        for c_i, column in enumerate(row):
            # print "row={}".format(r_i)
            # print "column={}".format(c_i)
            next_generation_matrix[r_i][c_i] = evolve(r_i, c_i)
    return next_generation_matrix


def evolve(row, column):
    next_generation = life_matrix[row][column]
    living_neighbours = count_living_neighbours(row, column)
    if (life_matrix[row][column]) == LIVE_CELL:
        # rule 1 and rule 3
        if living_neighbours < 2 or living_neighbours > 3:
            next_generation = DEAD_CELL
        # rule 2 is implicit
    elif living_neighbours == 3:
        next_generation = LIVE_CELL
    return next_generation


def count_living_neighbours(row, column):
    living_neighbours = 0
    # top left neighbour
    if row > 0 and column > 0 and life_matrix[row-1][column-1] == LIVE_CELL:
        living_neighbours += 1
    # top neighbour
    if row > 0 and life_matrix[row-1][column] == LIVE_CELL:
        living_neighbours += 1
    # top right neighbour
    if row > 0 and column < (MAX_COLUMNS-1) and life_matrix[row-1][column+1] == LIVE_CELL:
        living_neighbours += 1
    # left neighbour
    if column > 0 and life_matrix[row][column-1] == LIVE_CELL:
        living_neighbours += 1
    # right neighbour
    if column < (MAX_COLUMNS-1) and life_matrix[row][column+1] == LIVE_CELL:
        living_neighbours += 1
    # bottom left neighbour
    if row < (MAX_ROWS-1) and column > 0 and life_matrix[row+1][column-1] == LIVE_CELL:
        living_neighbours += 1
    # bottom neighbour
    if row < (MAX_ROWS-1) and life_matrix[row+1][column] == LIVE_CELL:
        living_neighbours += 1
    # bottom right neighbour
    if row < (MAX_ROWS-1) and column < (MAX_COLUMNS-1) and life_matrix[row+1][column+1  ] == LIVE_CELL:
        living_neighbours += 1
    return living_neighbours


def print_matrix(cycle):
    print "cycle: {}".format(cycle)
    for row in life_matrix:
        print ''.join(row)


main()