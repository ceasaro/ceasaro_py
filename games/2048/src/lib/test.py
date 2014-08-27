from lib.models import Cell


def test_all():
    test_cell()


def test_cell():
    print Cell() == Cell()
    print Cell(5) == Cell(5)
    print Cell(2) == Cell(5)

    lc1 = [Cell(1), Cell(2), Cell(3)]
    lc2 = [Cell(1), Cell(2), Cell(3)]
    lc3 = [Cell(2), Cell(2), Cell(3)]
    print lc1 == lc2
    print lc3 == lc1



