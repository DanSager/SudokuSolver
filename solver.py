""" solve sudoku """
from array import *

puzzle_directory = 'puzzles'


def complete(arr):
    return not any('X' in x for x in arr)


def print_puzzle(arr):
    """ Print the puzzle to console """
    for row in arr:
        print(row)


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
        if char == '\n':
            i += 1
            j = 0
    return puzzle


def solve(puzzle):
    """ Solve """
    i, j = 0, 0
    while not complete(puzzle):
        print("a")


def main():
    """ Main """
    puzzle = load_puzzle("easy1.txt")
    print_puzzle(puzzle)
    solve(puzzle)
    print("Done: " + str(complete(puzzle)))


if __name__ == "__main__":
    main()
