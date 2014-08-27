class Cell(object):
    def __init__(self, value=0):
        self.value = value
        super(Cell, self).__init__()

    @property
    def empty(self):
        return self.value == 0

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Game(object):

    def __init__(self):
        self.game_matrix = [[Cell() for x in xrange(4)] for y in xrange(4)]

    def print_matrix(self):
        """
        Prints the game matrix
        """
        print "-------------------------------"
        print
        for row in self.game_matrix:
            for cell in row:
                if cell.value:
                    print "{0: 5d}".format(cell.value),
                else:
                    print "     ",
            print
        print
        print "-------------------------------"
