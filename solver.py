""" solve sudoku """
from array import *
import time

puzzle_directory = 'puzzles/'

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
    return not any('0' in x for x in arr)


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


def block_to_array(input_block):
    """ Returns block as a single array """
    arr = []
    for row in input_block.get_rows():
        for box in row:
            arr.append(box)
    return arr


def load_puzzle(name):
    """ Read puzzle from text file """
    f = open(puzzle_directory + name, "r")
    r = f.read()

    rows, cols = 9, 9
    puzzle = [['0' for x in range(rows)] for y in range(cols)]
    i, j = 0, 0
    for char in r:
        if char != '\n':
            puzzle[i][j] = char
            j += 1
            if char != '0':
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


def find_row(local, elem):
    i = 0
    for row in local.get_rows():
        for box in row:
            if elem == box:
                return i
        i += 1
    return -1


def missing_in_local(local, arr1, arr2):
    return ((set(arr1) & set(arr2)) ^ set(local)) - set(local)


def common(row, col, local):
    return set(row) & set(col) & set(local)


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
    i, j = 0, 0
    iterations_since_last_found = 0
    while not complete(puzzle):
        if iterations_since_last_found > 81:
            # stuck
            print("Got stuck")
            print_puzzle(puzzle)
            break

        if puzzle[i][j] == '0':
            # try to solve
            relative_row = int(i % 3)  # Row position in block
            relative_col = int(j % 3)  # Column position in block
            relative_horizontal_block = int(j / 3)  # Horizonal block number in puzzle
            relative_vertical_block = int(i / 3)  # Vertical block number in puzzle

            row = contain(puzzle[i])  # Entire row
            col = contain(get_col(puzzle, j))  # Entire column

            con = False

            while True:
                if i == 1 and j == 6:
                    a = 1

                # BEGIN FILL ONE EMPTY SPOT BLOCK
                local_block = get_block(puzzle, i, j)  # Block that the active box is situated
                if len(missing(block_to_array(local_block))) == 1:
                    print("Added from fill one empty spot block")
                    puzzle = found(puzzle, i, j, missing(block_to_array(local_block)).pop())
                    iterations_since_last_found = 0
                    con = True

                if con:
                    break
                # END FILL ONE EMPTY SPOT BLOCK

                # BEGIN FILL ONE EMPTY SPOT ROW
                if len(missing(puzzle[i])) == 1:
                    print("Added from fill one empty spot row")
                    puzzle = found(puzzle, i, j, missing(puzzle[i]).pop())
                    iterations_since_last_found = 0
                    con = True

                if con:
                    break
                # END FILL ONE EMPTY SPOT ROW

                # BEGIN FILL ONE EMPTY SPOT COLUMN
                if len(missing(get_col(puzzle, j))) == 1:
                    print("Added from fill one empty spot column")
                    puzzle = found(puzzle, i, j, missing(get_col(puzzle, j)).pop())
                    iterations_since_last_found = 0
                    con = True

                if con:
                    break
                # END FILL ONE EMPTY SPOT COLUMN

                # BEGIN BASIC DIRECT ROW SPECULATION
                missing_row = missing(puzzle[i])
                missing_col = missing(get_col(puzzle, j))

                missing_block = missing(block_to_array(get_block(puzzle, i, j)))
                missing_elem = common(missing_row, missing_col, missing_block)

                if len(missing_elem) == 1:
                    print("Added from basic direct row speculation")
                    puzzle = found(puzzle, i, j, missing_elem.pop())
                    iterations_since_last_found = 0
                    con = True

                if con:
                    break
                # END BASIC DIRECT ROW SPECULATION

                # BEGIN STRAIGHT FORWARD BLOCK SPECULATION
                horizontal_block1, horizontal_block2 = block, block  # Blocks that are in the same row as the active box
                if relative_horizontal_block == 0:
                    horizontal_block1 = get_block(puzzle, i, j + 3)
                    horizontal_block2 = get_block(puzzle, i, j + 6)
                elif relative_horizontal_block == 1:
                    horizontal_block1 = get_block(puzzle, i, j - 3)
                    horizontal_block2 = get_block(puzzle, i, j + 3)
                elif relative_horizontal_block == 2:
                    horizontal_block1 = get_block(puzzle, i, j - 3)
                    horizontal_block2 = get_block(puzzle, i, j - 6)

                vertical_block1, vertical_block2 = block, block  # Blocks that are in the same coumn as the active box
                if relative_vertical_block == 0:
                    vertical_block1 = get_block(puzzle, i + 3, j)
                    vertical_block2 = get_block(puzzle, i + 6, j)
                elif relative_vertical_block == 1:
                    vertical_block1 = get_block(puzzle, i - 3, j)
                    vertical_block2 = get_block(puzzle, i + 3, j)
                elif relative_vertical_block == 2:
                    vertical_block1 = get_block(puzzle, i - 3, j)
                    vertical_block2 = get_block(puzzle, i - 6, j)

                # Find whats in both of the neighboring blocks but not in the local one
                miss_row = missing_in_local(block_to_array(local_block), block_to_array(horizontal_block1),
                                            block_to_array(horizontal_block2))
                miss_col = missing_in_local(block_to_array(local_block), block_to_array(vertical_block1),
                                            block_to_array(vertical_block2))

                local_row_simple = contain(local_block.get_row(relative_row))
                for row_element in miss_row:
                    if len(local_row_simple) == 2:
                        if row_element not in row and row_element not in col:
                            print("Added from rows missing")
                            puzzle = found(puzzle, i, j, row_element)
                            iterations_since_last_found = 0
                            con = True

                if con:
                    break

                local_col_simple = contain(local_block.get_col(relative_col))
                for column_element in miss_col:
                    if len(local_col_simple) == 2:
                        if column_element not in row and column_element not in col:
                            print("Added from cols missing")
                            puzzle = found(puzzle, i, j, column_element)
                            iterations_since_last_found = 0
                            con = True

                if con:
                    break
                # END STRAIGHT FORWARD BLOCK SPECULATION

                # BEGIN LACK OF SPACE
                for elem in missing_elem:
                    possible_locations = 9
                    for local_i in range(0, len(local_block.get_rows())):
                        for local_j in range(0, len(local_block.get_rows())):
                            if local_block.get_row(local_i)[local_j] == '0':
                                # elem can possbily go here
                                x = (relative_vertical_block * 3) + local_i
                                y = (relative_horizontal_block * 3) + local_j

                                missing_row2 = missing(puzzle[x])
                                missing_col2 = missing(get_col(puzzle, y))

                                missing_block2 = missing(block_to_array(vertical_block1))
                                missing_elem2 = common(missing_row2, missing_col2, missing_block2)
                                if elem not in missing_elem2:
                                    possible_locations -= 1
                            else:
                                possible_locations -= 1

                    if possible_locations == 1:
                        print("Added from lack of space")
                        puzzle = found(puzzle, i, j, elem)
                        iterations_since_last_found = 0
                        con = True
                        break

                if con:
                    break
                # END LACK OF SPACE

                # BEGIN ROWS PLUS COLUMNS
                local_row_raw = local_block.get_row(relative_row)

                other_row1, other_row2 = [], []
                if relative_row == 0:
                    other_row1 = contain(puzzle[i + 1])
                    other_row2 = contain(puzzle[i + 2])
                elif relative_row == 1:
                    other_row1 = contain(puzzle[i - 1])
                    other_row2 = contain(puzzle[i + 1])
                elif relative_row == 2:
                    other_row1 = contain(puzzle[i - 1])
                    other_row2 = contain(puzzle[i - 2])

                for elem in missing_elem:
                    if elem in other_row1 and elem in other_row2:
                        # Now see if it fits in the column
                        remaining = 3
                        for k in range(0, len(local_row_raw)):
                            if k == relative_col:
                                continue
                            elif local_row_raw[k] == '0':
                                # Check if this column has elem
                                if elem in contain(get_col(puzzle, (j + k - relative_col))):
                                    remaining -= 1
                            else:
                                remaining -= 1
                        if remaining == 0:
                            print("Added from rows plus columns")
                            puzzle = found(puzzle, i, j, elem)
                            iterations_since_last_found = 0
                            con = True

                if con:
                    break
                # END ROWS PLUS COLUMNS

                # BEGIN COLUMNS PLUS ROWS
                local_col_raw = local_block.get_col(relative_col)

                other_col1, other_col2 = [], []
                if relative_col == 0:
                    other_col1 = contain(get_col(puzzle, j + 1))
                    other_col2 = contain(get_col(puzzle, j + 2))
                elif relative_col == 1:
                    other_col1 = contain(get_col(puzzle, j - 1))
                    other_col2 = contain(get_col(puzzle, j + 1))
                elif relative_col == 2:
                    other_col1 = contain(get_col(puzzle, j - 1))
                    other_col2 = contain(get_col(puzzle, j - 2))

                for elem in missing_elem:
                    if elem in other_col1 and elem in other_col2:
                        # Now see if it fits in the column
                        remaining = 2
                        for k in range(0, len(local_col_raw)):
                            if k == relative_row:
                                continue
                            elif local_col_raw[k] == '0':
                                # Check if this column has elem
                                if elem in contain(puzzle[(i + k - relative_row)]):
                                    remaining -= 1
                            else:
                                remaining -= 1
                        if remaining == 0:
                            print("Added from columns plus rows")
                            puzzle = found(puzzle, i, j, elem)
                            iterations_since_last_found = 0
                            con = True

                if con:
                    break
                # END COLUMNS PLUS ROWS

                # BEGIN FORWARD THINKING ROW
                for elem in missing_elem:
                    if elem in other_row1 and elem in other_row2:
                        # Begin forward thinking
                        remaining = 2  # other spots it can goto. if zero, number must be here

                        for k in range(0, len(local_row_raw)):
                            if k == relative_col:
                                if (len(contain(vertical_block1.get_col(k))) == 3 or elem in block_to_array(
                                        vertical_block1)) and \
                                        (len(contain(vertical_block2.get_col(k))) == 3 or elem in block_to_array(
                                            vertical_block2)):
                                    remaining -= 1
                                    continue
                            if local_row_raw[k] == '0':
                                possible_local = 0
                                possible_block1 = 0
                                possible_block2 = 0
                                x = i
                                y = j + k - relative_col
                                if x == i and y == j:
                                    continue

                                elem_not_in_row = missing(puzzle[x])
                                elem_not_in_col = missing(get_col(puzzle, y))

                                elem_not_in_block = missing(block_to_array(local_block))
                                elem_not_already_contained = common(elem_not_in_row, elem_not_in_col, elem_not_in_block)
                                if elem in elem_not_already_contained:
                                    possible_local += 1

                                for m in range(0, len(vertical_block1.get_col(k))):
                                    if vertical_block1.get_col(k)[m] == '0':
                                        x, y = 0, 0
                                        if relative_vertical_block == 0:
                                            x = i + 3 - relative_row + m
                                            y = j + k - relative_col
                                        elif relative_vertical_block == 1:
                                            x = i - 3 - relative_row + m
                                            y = j + k - relative_col
                                        elif relative_vertical_block == 2:
                                            x = i - 3 - relative_row + m
                                            y = j + k - relative_col

                                        elem_not_in_row = missing(puzzle[x])
                                        elem_not_in_col = missing(get_col(puzzle, y))

                                        elem_not_in_block = missing(block_to_array(vertical_block1))
                                        elem_not_already_contained = common(elem_not_in_row, elem_not_in_col, elem_not_in_block)
                                        if elem in elem_not_already_contained:
                                            possible_block1 += 1

                                for m in range(0, len(vertical_block2.get_col(k))):
                                    if vertical_block2.get_col(k)[m] == '0':
                                        x, y = 0, 0
                                        if relative_vertical_block == 0:
                                            x = i + 6 - relative_row + m
                                            y = j + k - relative_col
                                        elif relative_vertical_block == 1:
                                            x = i + 3 - relative_row + m
                                            y = j + k - relative_col
                                        elif relative_vertical_block == 2:
                                            x = i - 6 - relative_row + m
                                            y = j + k - relative_col

                                        elem_not_in_row = missing(puzzle[x])
                                        elem_not_in_col = missing(get_col(puzzle, y))

                                        elem_not_in_block = missing(block_to_array(vertical_block2))
                                        elem_not_already_contained = common(elem_not_in_row, elem_not_in_col, elem_not_in_block)
                                        if elem in elem_not_already_contained:
                                            possible_block2 += 1

                                if (possible_local + possible_block1 + possible_block2) == 0:
                                    # it is possible to exist, other options exist
                                    remaining -= 1
                            else:
                                # Number already exists
                                remaining -= 1

                        if remaining == 0:
                            print("Added from forward thinking row")
                            puzzle = found(puzzle, i, j, elem)
                            iterations_since_last_found = 0
                            con = True
                            break

                if con:
                    break
                # ENG FORWARD THINKING ROW

                # BEGIN FORWARD THINKING COLUMN
                if i == 0 and j == 4:
                    dasda= "Das"
                for elem in missing_elem:
                    if elem in other_col1 and elem in other_col2:
                        # Begin forward thinking
                        remaining = 2  # other spots it can goto. if zero, number must be here
                        possible_block2

                        for k in range(0, len(local_col_raw)):
                            if k == relative_row:
                                if (len(contain(horizontal_block1.get_row(k))) == 3 or elem in block_to_array(
                                        horizontal_block1)) and \
                                        (len(contain(horizontal_block2.get_row(k))) == 3 or elem in block_to_array(
                                            horizontal_block2)):
                                    remaining -= 1
                                    continue
                            if local_col_raw[k] == '0':
                                possible_local = 0
                                possible_block1 = 0
                                possible_block2 = 0
                                x = i + k - relative_row
                                y = j
                                if not x == i and y == j:
                                    elem_not_in_row = missing(puzzle[x])
                                    elem_not_in_col = missing(get_col(puzzle, y))

                                    elem_not_in_block = missing(block_to_array(local_block))
                                    elem_not_already_contained = common(elem_not_in_row, elem_not_in_col, elem_not_in_block)
                                    if elem in elem_not_already_contained:
                                        possible_local += 1

                                for m in range(0, len(horizontal_block1.get_row(k))):
                                    if horizontal_block1.get_row(k)[m] == '0':
                                        x, y = 0, 0
                                        if relative_horizontal_block == 0:
                                            x = i + k - relative_row
                                            y = j + 3 - relative_col + m
                                        elif relative_horizontal_block == 1:
                                            x = i + k - relative_row
                                            y = j - 3 - relative_col + m
                                        elif relative_horizontal_block == 2:
                                            x = i + k - relative_row
                                            y = j - 3 - relative_col + m

                                        elem_not_in_row = missing(puzzle[x])
                                        elem_not_in_col = missing(get_col(puzzle, y))

                                        elem_not_in_block = missing(block_to_array(horizontal_block1))
                                        elem_not_already_contained = common(elem_not_in_row, elem_not_in_col, elem_not_in_block)
                                        if elem in elem_not_already_contained:
                                            possible_block1 += 1

                                for m in range(0, len(horizontal_block2.get_row(k))):
                                    if horizontal_block2.get_row(k)[m] == '0':
                                        x, y = 0, 0
                                        if relative_horizontal_block == 0:
                                            x = i + k - relative_row
                                            y = j + 6 - relative_col + m
                                        elif relative_horizontal_block == 1:
                                            x = i + k - relative_row
                                            y = j + 3 - relative_col + m
                                        elif relative_horizontal_block == 2:
                                            x = i + k - relative_row
                                            y = j - 6 - relative_col + m

                                        elem_not_in_row = missing(puzzle[x])
                                        elem_not_in_col = missing(get_col(puzzle, y))

                                        elem_not_in_block = missing(block_to_array(horizontal_block2))
                                        elem_not_already_contained = common(elem_not_in_row, elem_not_in_col, elem_not_in_block)
                                        if elem in elem_not_already_contained:
                                            possible_block2 += 1

                                if possible_local + possible_block1 + possible_block2 == 0:
                                    # it is possible to exist, other options exist
                                    remaining -= 1
                            else:
                                # Number already exists
                                remaining -= 1

                        if remaining == 0:
                            print("Added from forward thinking column")
                            puzzle = found(puzzle, i, j, elem)
                            iterations_since_last_found = 0
                            con = True
                            break

                if con:
                    break
                # ENG FORWARD THINKING COLUMN

                break

        # Continue
        j += 1
        if j == 9:
            j = 0
            i += 1
        if i == 9:
            i = 0
        iterations_since_last_found += 1


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
            global boxes
            boxes = 0

            filename = title + str(i)
            puzzle = load_puzzle(filename)
            solve(puzzle)
            if boxes == 81:
                # executed correctly
                correctly_solved += 1
            else:
                print("Had issues with " + filename)

        arr.append(correctly_solved)
        print("Correct solved: " + str(correctly_solved) + " " + title + " out of: " + str(iterations))
        print("--- %s seconds to execute ---" % (time.time() - start_time))
    for val in arr:
        print("Correct solved: " + str(val) + " out of: " + str(iterations))


def main():
    """ Main """
    puzzle = load_puzzle("medium0")
    print_puzzle(puzzle)
    start_time = time.time()
    solve(puzzle)
    #test(100, [1, 2])
    print("--- %s seconds ---" % (time.time() - start_time))
    #print("Done: " + str(complete(puzzle)))


if __name__ == "__main__":
    main()
