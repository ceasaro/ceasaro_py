#!/usr/bin/python3
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.color import yellow, light_red, color_str
from utils import color

color_mapping = {
    0: color.WHITE,
    1: color.RED,
    2: color.GREEN,
    3: color.YELLOW,
    4: color.BLUE,
    5: color.MAGENTA,
    6: color.CYAN,
    7: color.LIGHT_GRAY,
    8: color.LIGHT_RED,
    9: color.LIGHT_GREEN,
}


class Cell:

    def __init__(self, height):
        self.height = height
        self.is_low_point = False
        self.pool_id = None
        self.pool_group = None

    def get_pool_repr(self):
        # _str = str(self.pool_id) if self.pool_id else '9'
        _str = str(self.height)
        if self.pool_id:
            # return color_str(color_mapping.get(self.pool_id % 10), '.')
            return '.'
        else:
            return _str

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        _str = str(self.height)
        if self.is_low_point:
            return light_red(_str)
        elif self.height == 9:
            return yellow(_str)
        else:
            return _str


class Grid:

    def __init__(self) -> None:
        self.grid = []
        self.risk_level = 0
        super().__init__()

    def add_line(self, line):
        self.grid.append([Cell(int(x)) for x in line])

    def find_lowest_points(self):
        max_y = len(self.grid) - 1
        max_x = len(self.grid[0]) - 1
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                is_low_point = True
                if y > 0:  # north
                    is_low_point &= cell.height < self.grid[y - 1][x].height
                if y < max_y:  # south
                    is_low_point &= cell.height < self.grid[y + 1][x].height
                if x > 0:  # west
                    is_low_point &= cell.height < self.grid[y][x - 1].height
                if x < max_x:  # east
                    is_low_point &= cell.height < self.grid[y][x + 1].height

                if is_low_point:
                    self.risk_level += cell.height + 1
                    cell.is_low_point = is_low_point

    def find_pools(self):
        # max_y = len(self.grid) - 1
        # max_x = len(self.grid[0]) - 1
        next_pool_id = 1
        pools = {}
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell.height == 9:
                    continue  # no pool
                else:
                    pool_id_north = self.grid[y - 1][x].pool_id if y > 0 else None
                    # if y < max_y:  # south
                    #     height_south = self.grid[y+1][x].height
                    pool_id_west = self.grid[y][x - 1].pool_id if x > 0 else None
                    # if x < max_x:  # east
                    #     height_east = self.grid[y][x+1].height
                    if pool_id_north:
                        cell.pool_id = pool_id_north
                        for pool in pools.items():
                            if pool_id_north in pool[0]:
                                pools[pool[0]] += 1
                        if pool_id_west and pool_id_west != pool_id_north:
                            # merge pools
                            # print(f"merge {pool_id_west} and {pool_id_north}")
                            # print(pools)
                            new_pools = {}
                            pool_west_count = pool_north_count = 0
                            for pool, pool_count in pools.items():
                                if pool_id_west in pool:
                                    pool_with_west = pool
                                    pool_west_count = pool_count
                                elif pool_id_north in pool:
                                    pool_with_north = pool
                                    pool_north_count = pool_count
                                else:
                                    new_pools[pool] = pool_count
                            # print(f"west = {pool_with_west},  north={pool_with_north}")
                            new_pools[frozenset().union(*[pool_with_west, pool_with_north])] =\
                                pool_west_count + pool_north_count
                            pools = new_pools
                            # print(pools)
                            # print('------------')
                    elif pool_id_west:
                        cell.pool_id = pool_id_west
                        for pool in pools.items():
                            if pool_id_west in pool[0]:
                                pools[pool[0]] += 1
                    else:
                        cell.pool_id = next_pool_id
                        pools[frozenset({next_pool_id})] = 1
                        next_pool_id += 1
                    print(f"number of pools: {len(pools)}")
                    print(pools)
                    print(self.get_pool_repr())
                    print('----------------------------------')

        return pools

    def get_pool_repr(self):
        _str = ''
        for row in self.grid:
            for cell in row:
                _str += cell.get_pool_repr()
            _str += '\n'
        return _str

    def __str__(self):
        _str = ''
        for row in self.grid:
            for cell in row:
                _str += str(cell)
            _str += '\n'
        return _str


def run(input_file):
    grid = Grid()
    with open(input_file) as fp:
        for line in fp.readlines():
            grid.add_line(line.rstrip('\n'))
    # puzzle 1
    # grid.find_lowest_points()
    # print(f"puzzle 1: {grid.risk_level}")
    pools = grid.find_pools()
    print(grid)
    print(grid.get_pool_repr())
    sizes = [x for x in pools.values()]
    sizes.sort()
    print(sizes)
    print(len(sizes))
    print(sizes[-1] * sizes[-2] * sizes[-3])
    # for pool, count in pools.items():
    #     print(f"{pool} - {count}")
    # print(sizes[-1] * sizes[-2] * sizes[-3])


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
