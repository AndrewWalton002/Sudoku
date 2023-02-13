""""
Functions that are used to solve a sudoku, created by Andrew Walton
"""
import math 
import numpy 

GRID_SIZE = 9
SQUARE_SIZE = math.floor(math.sqrt(GRID_SIZE))
NUM_CELLS = GRID_SIZE ** 2

def print_grid(grid):
    """"
    Print the cuurent state of the   grid
    param grid: the current state of the grid in a list
    """

    print_line()
    
    for i in range(NUM_CELLS):
        if not  (i % GRID_SIZE):
            print("|", end='')

        # Print each element in the row, and the outlines of the square
        print(f" {grid[i]} ", end='')
        if not (i + 1) % 3:
            print("|", end='')
        
        if not (i + 1) % GRID_SIZE:
            print('')

        # Print the horizontal lines between the boxes
        if i and not (((i + 1) % (3 * GRID_SIZE))):
            print_line()


def print_line():
    """
    Print the seperating lines between squares on the horizontal
    """
    print("+", end='')
    for i in range(GRID_SIZE):
        print("---", end='')
        if not (i + 1) % SQUARE_SIZE :
            print("+", end='')
    print('')

    
def is_grid_valid(grid):
    """
    Determine if the state of the grid is a valid state currently
    param grid: the current state of the grid in a list
    return: True if the grid is valid and False if it is not
    """

    # Preallocate memory for a hash map of rows, columns and squares
    row_hash = numpy.zeros(NUM_CELLS)
    column_hash = numpy.zeros(NUM_CELLS)
    square_hash = numpy.zeros(NUM_CELLS)

    # Iterate through each element in the grid
    for i in range(NUM_CELLS):
            if grid[i]:

                # Fill in the hash map for rows and return False if the is a number that 
                # occurs more than once
                row_hash[GRID_SIZE * (i // GRID_SIZE) + grid[i] - 1] += 1
                if row_hash[GRID_SIZE * (i // GRID_SIZE) + grid[i] - 1] > 1:
                    return False

                # Fill in the hash map for columns and return False if the is a number 
                # that occurs more than once
                column_hash[GRID_SIZE * (i % GRID_SIZE) + grid[i] - 1] += 1
                if column_hash[GRID_SIZE * (i % GRID_SIZE) + grid[i] - 1]  > 1:
                    return False

                # Find which square the the current element is in
                square_index = find_square_index(i)

                # Fill in the hash map for squares and return False if the is a number
                # that occurs more than once
                square_hash[GRID_SIZE * square_index + grid[i] - 1] += 1
                if square_hash[GRID_SIZE * square_index + grid[i] - 1] > 1:
                    return False

    # If no errors have been found return True
    return True


def find_square_index(index):
    """
    param index: the index of the cell in the grid
    return: the index of the square that the cell is in
    """
    return 3 * ((index) // (GRID_SIZE * SQUARE_SIZE)) + \
        int(((index) % GRID_SIZE) / 3)


def find_empty_cell(grid):
    """
    Finds the next empty cell in the grid
    param grid: the current state of the grid in a list
    return -1: if the grid is full
    return the cell index:  if there is an empty cell
    """

    # Iterate through the grid to find the first empty cell
    for i in range(NUM_CELLS):
        if not grid[i]:
            return i

    return -1


def is_row_valid(grid, index, num):
    """
    Determine if the attempted insertion into the row is currently valid
    param grid: the current state of the grid in a list
    param index: the index of the cell that is being inserted into in the grid
    param num: the number that is being attempted to insert into the cell
    return True: if the insertion is valid
    return False: if the insertion is invalid
    """

    row = int(index / GRID_SIZE)

    # Iterate through every element in the row and determine if the number is already 
    # in the row
    for i in range(GRID_SIZE):
        if grid[i + row * GRID_SIZE] == num:
            return False
    
    return True


def is_col_valid(grid, index, num):
    """
    Determine if the attempted insertion into the column is currently valid
    param grid: the current state of the grid in a list
    param index: the index of the cell that is being inserted into in the grid
    param num: the number that is being attempted to insert into the cell
    return True: if the insertion is valid
    return False: if the insertion is invalid
    """

    col = int(index % GRID_SIZE)

    # Iterate through every element in the column and determine if the number is already 
    # in the column
    for i in range(GRID_SIZE):
        if grid[col + i * GRID_SIZE] == num:
            return False

    return True

def is_square_valid(grid, index, num):
    """
    Determine if the attempted insertion into the column is currently valid
    param grid: the current state of the grid in a list
    param index: the index of the cell that is being inserted into in the grid
    param num: the number that is being attempted to insert into the cell
    return True: if the insertion is valid
    return False: if the insertion is invalid
    """

    square = find_square_index(index)

    # Iterate through each element in the square and determine if the number is already
    # in the square
    for i in range(SQUARE_SIZE):
        for j in range(SQUARE_SIZE):
            if grid[(3 * (math.floor(square / SQUARE_SIZE)) + i) * GRID_SIZE + \
                (square % SQUARE_SIZE) * SQUARE_SIZE + j] == num:
                return False
    
    return True 


def is_insertion_valid(grid, index, num):
    """
    Determines if the attempted insertion is valid
    param grid: the current state of the grid in a list
    param index: the index of the cell that is being inserted into in the grid
    param num: the number that is being attempted to insert into the cell
    return True: if the insertion is valid
    return False: if the insertion is invalid
    """
    return is_row_valid(grid, index, num) and is_col_valid(grid, index, num) \
        and is_square_valid(grid, index, num)

def solve_sudoku(grid):
    """
    Solves the sudoku using the a recursive backtracking algorithm
    param grid: the current state of the grid in a list
    return True: if the sudoku has been solved
    return Flase: if the sudoku cannot be solved
    """

    index = find_empty_cell(grid)
    
    # If the sudoku is full return True
    if index == -1:
        return True
    
    # Iterate through every possible number that could be inserted in 
    # the empty cell
    for num in range(1, GRID_SIZE + 1):

        # Check if the current number can be inserted in the grid
        if is_insertion_valid(grid, index, num):

            # Try to insert the current number
            grid[index] = num

            # Recursively call the solve sudoku function and return True if 
            # the insertion is correct
            if solve_sudoku(grid):
                return True

            # Reset the current cell back to 0 as the insertion was not correct
            grid[index] = 0    
    
    # Return False if there is no possible insertion that is valid
    return False