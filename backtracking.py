""" solve sudoku """
from array import *
import time
from copy import copy, deepcopy

PUZZLES_DIRECTORY = 'puzzles/'
NUMS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
DEBUG = True


class box:
    """ Box Class """

    def determine_block(self):
        if self.x_coord < 3 and self.y_coord < 3:
            return 0
        elif self.x_coord < 3 and self.y_coord > 5:
            return 2
        elif self.x_coord < 3:
            return 1
        elif self.x_coord > 5 and self.y_coord < 3:
            return 6
        elif self.x_coord > 5 and self.y_coord > 5:
            return 8
        elif self.x_coord > 5:
            return 7
        elif self.y_coord < 3:
            return 3
        elif self.y_coord > 5:
            return 5
        else:
            return 4

    def __init__(self, x_coord, y_coord, original, value):
        self.x_coord = x_coord  # x_coord of this box
        self.y_coord = y_coord  # y_coord of this box
        self.original = original  # True = part of the board, # False = placed subsequently
        self.value = value  # Default = 0, value on the board
        self.block = self.determine_block()

    def set_value(self, value):
        self.value = value

    def get_x_coord(self):
        return self.x_coord

    def get_y_coord(self):
        return self.y_coord

    def get_original(self):
        return self.original

    def get_value(self):
        return self.value

    def get_block(self):
        return self.block


def load_puzzle(name):
    """ Read puzzle from text file """
    f = open(PUZZLES_DIRECTORY + name, "r")
    r = f.read()

    rows, cols = 9, 9
    puzzle = [[box for x in range(rows)] for y in range(cols)]

    x, y = 0, 0

    for char in r:
        if char != '\n':
            if char == '0':
                puzzle[x][y] = box(x, y, False, char)
            else:
                puzzle[x][y] = box(x, y, True, char)
            y += 1
        if char == '\n':
            x += 1
            y = 0

    return puzzle


def print_puzzle(puz):
    """ Print the puzzle to console """
    if not DEBUG:
        return
    for row in puz:
        for b in row:
            print(b.get_value(), end='')
        print('')
    print('\n')
    return


def insert(puz, x, y, value):
    b = puz[x][y]
    b.set_value(value)
    puz[x][y] = b
    if DEBUG:
        print("inserted: " + value + " at: " + str(x) + " " + str(y))
    return puz


def extract_row_values(puzzle, b):
    row = puzzle[b.get_x_coord()]
    arr = []
    for bo in row:
        arr.append(bo.get_value())
    return arr


def extract_column_values(puzzle, b):
    i = b.get_y_coord()
    arr = []
    for row in puzzle:
        arr.append(row[i].get_value())
    return arr


def extract_block_values(puzzle, b):
    block_num = b.get_block()
    arr = []
    for row in puzzle:
        for bo in row:
            if bo.get_block() == block_num:
                arr.append(bo.get_value())
    return arr


def missing_nearby(row, column, block):
    return sorted(set(NUMS + ['0']) ^ (set().union(row, column, block)))


def complete(puzzle):
    for row in puzzle:
        for obj in row:
            if obj.get_value() == '0':
                return False
    return True


def solve(puzzle, x, y):
    i = x
    j = y + 1
    if j == 9:
        j = 0
        i = x + 1
    if i == 9:
        i = 0

    print_puzzle(puzzle)

    if puzzle[x][y].get_original():
        return solve(puzzle, i, j)

    row_values = extract_row_values(puzzle, puzzle[x][y])
    column_values = extract_column_values(puzzle, puzzle[x][y])
    block_values = extract_block_values(puzzle, puzzle[x][y])
    possible_values = missing_nearby(row_values, column_values, block_values)
    while True:
        if complete(puzzle):
            break

        if len(possible_values) == 0:
            return puzzle
        else:
            if DEBUG:
                print(possible_values)
            out = solve(insert(deepcopy(puzzle), x, y, possible_values.pop()), i, j)
            if complete(out):
                puzzle = out


    return puzzle


def test(iterations, selection):
    arr = []
    for difficulty in selection:
        start_time = time.time()

        correctly_solved = 0
        title = ""
        if difficulty == 1:
            title = "very-easy"
        elif difficulty == 2:
            title = "easy"
        elif difficulty == 3:
            title = "medium"
        elif difficulty == 4:
            title = "hard"
        elif difficulty == 5:
            title = "very-hard"

        for i in range(0, iterations):

            filename = title + str(i)
            print("Attemping " + filename)
            puzzle = load_puzzle(filename)
            solve(puzzle, 0, 0)

        print("--- %s seconds to execute ---" % (time.time() - start_time))
    for val in arr:
        print("- Correct solved: " + str(val) + " out of: " + str(iterations))
    return


def main():
    """ Main """
    puzzle = load_puzzle("medium1")
    puzzle.reverse()
    # print_puzzle(puzzle)

    start_time = time.time()
    completed = solve(puzzle, 0, 0)
    #test(50, [3])
    print("COMPLETED")
    print_puzzle(completed)
    print("--- %s seconds ---" % (time.time() - start_time))
    # print("Done: " + str(complete(puzzle)))
    return


if __name__ == "__main__":
    main()
