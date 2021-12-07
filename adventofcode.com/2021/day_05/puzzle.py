#!/usr/bin/python3
import sys

lines = []


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return f"({self.x1}, {self.y1}) -> ({self.x2}, {self.y2})"


class Grid:
    def __init__(self, max_x, max_y):
        self.grid = [[0]*max_x for i in range(max_y)]

    @property
    def dangerous_areas(self):
        dangerous_count = 0
        for row in self.grid:
            for count in row:
                if count > 1:
                    dangerous_count += 1
        return dangerous_count

    def add_line(self, line):
        min_x = min(line.x1, line.x2)
        max_x = max(line.x1, line.x2)
        min_y = min(line.y1, line.y2)
        max_y = max(line.y1, line.y2)
        x_range = [x for x in range(min_x, max_x+1)]
        y_range = [y for y in range(min_y, max_y+1)]

        if line.x1 > min_x:
            x_range.reverse()
        if line.y1 > min_y:
            y_range.reverse()
        for xi, x in enumerate(x_range):
            for yi, y in enumerate(y_range):
                if xi == yi or min_x == max_x or min_y == max_y:
                    self.grid[y][x] += 1

    def __str__(self):
        to_str = ""
        for row in self.grid:
            for cell_count in row:
                to_str += str(cell_count) if cell_count else '.'
            to_str += "\n"
        return to_str


def run(input_file):
    max_x = 0
    max_y = 0

    with open(input_file) as fp:
        for line in fp.readlines():
            coord1_str, coord2_str = line.rstrip('\n').split(' -> ')
            x1, y1 = [int(x) for x in coord1_str.split(',')]
            x2, y2 = [int(x) for x in coord2_str.split(',')]
            max_x = max(max_x, x1, x2)
            max_y = max(max_y, y1, y2)
            lines.append(Line(x1, y1, x2, y2))

    grid = Grid(max_x+1, max_y+1)
    for line in lines:
        # uncomment next line to sole first puzzle.
        # if line.x1 == line.x2 or line.y1 == line.y2:
        grid.add_line(line)
    # print(grid)
    print(grid.dangerous_areas)
    # print('CORRECT ANSWER = 6283')


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
