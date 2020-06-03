""" solve sudoku """
from array import *

puzzle_directory = 'puzzles'
nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
boxes = 0


class block:
    """ Block class """

    # init method or constructor
    def __init__(self, rows):
        self.rows = rows

    def set_rows(self, arr):
        self.rows = arr

    def get_rows(self):
        return self.rows

    def get_row(self, i):
        return self.rows[i]

    def get_cols(self):
        size = len(self.rows)
        arr = [[]]
        i = 0
        for row in self.rows:
            for j in range(0, size):
                arr[i].append(row[j])
            i += 1
        return arr

    def get_col(self, i):
        arr = []
        for row in self.rows:
            arr.append(row[i])
        return arr


def complete(arr):
    """ Does the sudoku contain any Xs """
    return not any('X' in x for x in arr)


def print_puzzle(arr):
    """ Print the puzzle to console """
    for row in arr:
        print(row)
    print('\n')


def get_col(arr2d, i):
    """ Returns column as a single array """
    arr = []
    for row in arr2d:
        arr.append(row[i])
    return arr


def get_block(arr2d, i, j):
    """ Returns block as a single array """
    x = i - int(i % 3)
    y = j - int(j % 3)
    b = block([[(arr2d[x][y]), (arr2d[x][y + 1]), (arr2d[x][y + 2])],
           [(arr2d[x + 1][y]), (arr2d[x + 1][y + 1]), (arr2d[x + 1][y + 2])],
           [(arr2d[x + 2][y]), (arr2d[x + 2][y + 1]), (arr2d[x + 2][y + 2])]])
    return b


def get_block_contents(arr2d, i, j):
    """ Returns block as a single array """
    x = i - int(i % 3)
    y = j - int(j % 3)
    arr = [(arr2d[x][y]), (arr2d[x][y + 1]), (arr2d[x][y + 2]),
           (arr2d[x + 1][y]), (arr2d[x + 1][y + 1]), (arr2d[x + 1][y + 2]),
           (arr2d[x + 2][y]), (arr2d[x + 2][y + 1]), (arr2d[x + 2][y + 2])]
    return arr


def load_puzzle(name):
    """ Read puzzle from text file """
    f = open("puzzles" + "/" + name, "r")
    r = f.read()

    rows, cols = 9, 9
    puzzle = [['X' for x in range(rows)] for y in range(cols)]
    i, j = 0, 0
    for char in r:
        if char != '\n':
            puzzle[i][j] = char
            j += 1
            if char != 'X':
                global boxes
                boxes += 1
        if char == '\n':
            i += 1
            j = 0

    return puzzle


def contain(input_array):
    """ Finds what numbers are in the current row """
    arr = []
    for num in nums:
        if any(num in x for x in input_array):
            arr.append(num)
    return arr


def missing(input_array):
    """ Finds what numbers arent in the current row """
    arr = []
    for num in nums:
        if not any(num in x for x in input_array):
            arr.append(num)
    return arr


def common(row, col, block):
    return set(row) & set(col) & set(block)


def found(puzzle, i, j, elem):
    puzzle[i][j] = elem
    print("Added " + elem + " at i:" + str(i) + " j:" + str(j))
    global boxes
    boxes += 1
    print(str(boxes) + "/81")
    print_puzzle(puzzle)
    return puzzle


def solve(puzzle):
    """ Solve """
    i, j = 3, 4
    while not complete(puzzle):
        if puzzle[i][j] == 'X':
            # try to solve
            relative_row = int(i % 3)
            row = []
            row_neighbor1 = []
            row_neighbor2 = []

            b = get_block(puzzle, i, j)

            row = contain(puzzle[i])
            if relative_row == 0:
                row_neighbor1 = contain((puzzle[i + 1]))
                row_neighbor2 = contain((puzzle[i + 2]))
            elif relative_row == 1:
                row_neighbor1 = contain((puzzle[i - 1]))
                row_neighbor2 = contain((puzzle[i + 1]))
            elif relative_row == 2:
                row_neighbor1 = contain((puzzle[i - 1]))
                row_neighbor2 = contain((puzzle[i - 2]))



            missing_row = missing(puzzle[i])
            missing_col = missing(get_col(puzzle, j))
            missing_block = missing(get_block_contents(puzzle, i, j))
            missing_elem = common(missing_row, missing_col, missing_block)

            if len(missing_elem) == 1:
                puzzle = found(puzzle, i, j, missing_elem.pop())
        j += 1
        if j == 9:
            j = 0
            i += 1
        if i == 9:
            i = 0


def main():
    """ Main """
    puzzle = load_puzzle("easy1.txt")
    print_puzzle(puzzle)
    solve(puzzle)
    print("Done: " + str(complete(puzzle)))


if __name__ == "__main__":
    main()
