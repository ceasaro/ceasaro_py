#!/usr/bin/python3
import sys

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


class BingoCard:

    def __init__(self, lines=None):
        self.grid = []
        self.row_count = len(lines)
        self.col_count = self.row_count
        self.had_first_bingo = False
        for line in lines or []:
            self.grid.append([[int(n), False] for n in line.rstrip('\n').split(' ') if n])

    def mark_number(self, number):
        for row in self.grid:
            for cell in row:
                cell[1] = cell[1] or cell[0] == number

    def has_bingo(self):
        cols = []
        # check if a row has bingo
        for row in self.grid:
            if all([c[1] for c in row]):
                return True

        # check if a column has bingo
        for col in range(self.col_count):
            col_cells = [self.grid[row][col] for row in range(self.row_count)]
            if all([c[1] for c in col_cells]):
                return True

    def has_first_bingo(self):
        if not self.had_first_bingo:
            self.had_first_bingo = self.has_bingo()
            return self.had_first_bingo
        return False

    def sum_unmarked(self):
        total_sum = 0
        for row in self.grid:
            for cell in row:
                if not cell[1]:
                    total_sum += cell[0]
        return total_sum

    def __str__(self) -> str:
        to_str = ""
        for row in self.grid:
            for cell in row:
                cell_str = f"{cell[0]:3}"
                if cell[1]:
                    cell_str = color_str(OKGREEN, cell_str)
                to_str += cell_str
            to_str += "\n"
        return to_str


def run(input_file):
    cards = []
    with open(input_file) as fp:
        numbers = [int(n) for n in fp.readline().rstrip('\n').split(',')]

        card_lines = []
        for line in fp.readlines():
            line = line.rstrip('\n')
            if not line:
                if card_lines:
                    cards.append(BingoCard(lines=card_lines))
                card_lines = []
            else:
                card_lines.append(line)
        if card_lines:
            cards.append(BingoCard(lines=card_lines))

    print(numbers)
    print_cards(cards)

    cards_with_no_bingo_count = len(cards)
    for number in numbers:
        for card in cards:
            card.mark_number(number)
            if card.has_first_bingo():
                print(card)
                if cards_with_no_bingo_count == 1:
                    found_last_bingo(card, cards, number)
                cards_with_no_bingo_count -= 1


def first_bingo_card(cards, number):
    for card_index, card in enumerate(cards):
        card.mark_number(number)
        if card.has_bingo():
            print(card)
            return card, card_index
    return None, None


def print_cards(cards):
    for card in cards:
        print(card)


def found_last_bingo(card, cards, last_number):
    # print_cards(cards)
    print('-----------')
    print(card)
    sum_unmarked = card.sum_unmarked()
    print(f"{sum_unmarked} * {last_number} = {sum_unmarked * last_number}")
    sys.exit()


def color_str(color, msg):
    return f"{color}{msg}{ENDC}"


def main(prog_args):
    run(prog_args[1])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
