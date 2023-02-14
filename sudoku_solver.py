""""
Functions that are used to solve a sudoku, created by Andrew Walton
"""
import math 
import numpy 
import sudoku_gui


def find_square_index(index):
    """
    param index: the index of the cell in the grid
    return: the index of the square that the cell is in
    """
    return 3 * ((index) // (sudoku_gui.GRID_SIZE * sudoku_gui.SQUARE_SIZE)) + \
        int(((index) % sudoku_gui.GRID_SIZE) / 3)


def find_empty_cell(grid):
    """
    Finds the next empty cell in the grid
    param grid: the current state of the grid in a list
    return -1: if the grid is full
    return the cell index:  if there is an empty cell
    """

    # Iterate through the grid to find the first empty cell
    for i in range(sudoku_gui.NUM_CELLS):
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

    row = index // sudoku_gui.GRID_SIZE

    # Iterate through every element in the row and determine if the number is already 
    # in the row
    for i in range(sudoku_gui.GRID_SIZE):
        if grid[i + row * sudoku_gui.GRID_SIZE] == num:
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

    col = int(index % sudoku_gui.GRID_SIZE)

    # Iterate through every element in the column and determine if the number is already 
    # in the column
    for i in range(sudoku_gui.GRID_SIZE):
        if grid[col + i * sudoku_gui.GRID_SIZE] == num:
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
    for i in range(sudoku_gui.SQUARE_SIZE):
        for j in range(sudoku_gui.SQUARE_SIZE):
            if grid[(3 * (math.floor(square / sudoku_gui.SQUARE_SIZE)) + i) * sudoku_gui.GRID_SIZE + \
                (square % sudoku_gui.SQUARE_SIZE) * sudoku_gui.SQUARE_SIZE + j] == num:
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
    for num in range(1, sudoku_gui.GRID_SIZE + 1):

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