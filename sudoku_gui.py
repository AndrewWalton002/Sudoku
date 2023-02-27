from calendar import c
from tkinter.font import BOLD
from turtle import right
import pygame
from sudoku_solver import *

pygame.font.init()

WIDTH, HEIGHT = 700, 498

X_INDEX = 0
Y_INDEX = 1

# Dimensions for the creation of the sudoku grid
GRID_SIZE = 9
SQUARE_SIZE = math.floor(math.sqrt(GRID_SIZE))
NUM_CELLS = GRID_SIZE ** 2
CELL_DIMENSION = 50
BOLD_WIDTH = 3
LINE_WIDTH = 1
BOARD_PAD = 15
OG_X_COORD = 32
OG_Y_COORD = 20
NUM_BOLD_LINES = 4
NUM_NORMAL_LINES = 6
LINE_LEN = GRID_SIZE * CELL_DIMENSION + NUM_BOLD_LINES * BOLD_WIDTH + \
    NUM_NORMAL_LINES * LINE_WIDTH
BOARD_BOTTOM_EDGE = BOARD_PAD + GRID_SIZE * CELL_DIMENSION + (NUM_BOLD_LINES - 1) * \
    BOLD_WIDTH + NUM_NORMAL_LINES * LINE_WIDTH
BOARD_RIGHT_EDGE = BOARD_PAD + GRID_SIZE * CELL_DIMENSION + (NUM_BOLD_LINES - 1) * \
    BOLD_WIDTH + NUM_NORMAL_LINES * LINE_WIDTH
BOARD_TOP_EDGE = BOARD_PAD + BOLD_WIDTH
BOARD_LEFT_EDGE = BOARD_PAD + BOLD_WIDTH

GIVE_UP_WIDTH = 162
GIVE_UP_HEIGHT = 45
GIVE_UP_COORD_X = BOARD_RIGHT_EDGE + int(0.5 * (WIDTH - BOARD_RIGHT_EDGE - GIVE_UP_WIDTH))
GIVE_UP_COORD_Y = 40
GIVE_UP_TEXT = "GIVE UP"
GIVE_UP_RECT = pygame.Rect(GIVE_UP_COORD_X, GIVE_UP_COORD_Y,GIVE_UP_WIDTH, GIVE_UP_HEIGHT)





# Define the fonts for sudoku
NUM_FONT = pygame.font.SysFont("Times New Roman", 40)

# RGB form of colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

# Create the pygame display and title it
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")


def draw_board(clicked_cell):
    """
    Draw the grid for the sudoku
    """

    cell_coord = BOARD_PAD

    # Draw the grid for the sudoku
    for i in range(GRID_SIZE + 1):
        
        # Create the lines that are used to make up the grid
        bold_horizontal_line = pygame.Rect(BOARD_PAD, cell_coord, LINE_LEN, BOLD_WIDTH)
        bold_verticle_line = pygame.Rect(cell_coord, BOARD_PAD, BOLD_WIDTH,  LINE_LEN)
        normal_horizontal_line = pygame.Rect(BOARD_PAD, cell_coord,LINE_LEN, LINE_WIDTH)
        normal_verticle_line = pygame.Rect(cell_coord, BOARD_PAD, LINE_WIDTH, LINE_LEN)

        # Draw the bold lines between the squares
        if not (i % 3):
            pygame.draw.rect(WIN, BLACK, bold_horizontal_line)
            pygame.draw.rect(WIN, BLACK, bold_verticle_line)

            # Update the coordinate of the reference point of the cell 
            cell_coord += CELL_DIMENSION + BOLD_WIDTH
        
        # Draw the normal lines between the cells
        else:
            pygame.draw.rect(WIN, BLACK, normal_horizontal_line)
            pygame.draw.rect(WIN, BLACK, normal_verticle_line)

            # Update the coordinate of the reference point of the cell
            cell_coord += CELL_DIMENSION + LINE_WIDTH
    
    # If there is a clicked cell highlight it
    if clicked_cell != -1:
        draw_rect(cell_coords(clicked_cell), GREY, BOLD_WIDTH, CELL_DIMENSION, CELL_DIMENSION)

 
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


def draw_game(clicked_cell):
    """
    Draw the display of the game
    """

    WIN.fill(WHITE)
    draw_board(clicked_cell)
    draw_give_up_rect()


def fill_grid(grid, user_filled_grid):
    """
    Fill the known cells in the sudoku with the elements
    param grid: the elements of the grid in a list
    """

    x_coord = OG_X_COORD
    y_coord = OG_Y_COORD

    for i in range(NUM_CELLS):
        
        # Fill in the original grid with black numbers
        if grid[i]:
            num = NUM_FONT.render(str(grid[i]), 1, BLACK)
            WIN.blit(num, (x_coord, y_coord))

        # If the user has put a valid value in the grid draw it in a grey
        elif user_filled_grid[i] != grid[i]:
            num = NUM_FONT.render(str(user_filled_grid[i]), 1, GREY)
            WIN.blit(num, (x_coord, y_coord))


        
        # If there is another element in the row increase the x cooridinate
        if (i + 1) % GRID_SIZE:
            if (i + 1) % SQUARE_SIZE:
                x_coord += CELL_DIMENSION + LINE_WIDTH
            else:
                x_coord += CELL_DIMENSION + BOLD_WIDTH

        # If it is the end of a row reset the x cooridinate and increase 
        # y cooridnate
        else:
            x_coord = OG_X_COORD
            if (i + 1) % (SQUARE_SIZE * GRID_SIZE):
                y_coord += CELL_DIMENSION + LINE_WIDTH
            else:
                y_coord += CELL_DIMENSION + BOLD_WIDTH



    
def find_clicked_cell(pos):
    """
    Determines if the mouse click occured in a cell within the board
    param pos: A tuple of the coordinates of the click
    return -1: If the click is not in a cell
    return grid index: If the click is in a valid cell
    """

    # If the click is outside the boarder of the board return False
    if pos[X_INDEX] >= BOARD_RIGHT_EDGE or pos[Y_INDEX] >= BOARD_BOTTOM_EDGE or \
        pos[X_INDEX] <= BOARD_LEFT_EDGE or pos[Y_INDEX] <= BOARD_TOP_EDGE:
        return -1
    
    # Zero the coordinates to the top left of the 0th cell
    x_coord = pos[X_INDEX] - BOARD_LEFT_EDGE
    y_coord = pos[Y_INDEX] - BOARD_TOP_EDGE
    
    normal_lines_to_left = 0
    normal_lines_above = 0
    bold_lines_to_left = 0
    bold_lines_above = 0

    # Check if the click is on a line within the board
    for i in range(NUM_NORMAL_LINES + NUM_BOLD_LINES - 2):

        # Check if the click is on a bold line
        if not (i + 1) % SQUARE_SIZE:

            lower_bold_check = (i + 1) * CELL_DIMENSION + i
            upper_bold_check = lower_bold_check + (BOLD_WIDTH - 1) * (i % SQUARE_SIZE)

            # Determine if the x coordinate of the click is on a line
            if x_coord >= lower_bold_check and x_coord <= upper_bold_check:
                return -1
            
            # Determine if the y coordinate of the click is on a line
            if y_coord >= lower_bold_check and y_coord <= upper_bold_check:
                return -1
            
            # Update the number of lines to the left and above the click
            if x_coord > upper_bold_check:
                bold_lines_to_left += 1
            if y_coord > upper_bold_check:
                bold_lines_above += 1
        
        # Check if the click is on a normal line
        # COULD MAKE BETTER WITH CHECK ON LINE THICKNESS
        else: 

            line_check = (i + 1) * CELL_DIMENSION + i + (BOLD_WIDTH - 1) * (i % SQUARE_SIZE)

            # If the click is on a normal line return False
            if x_coord == line_check or y_coord == line_check:
               return -1

            # Update the number of normal lines to the left and above the click
            if x_coord > line_check:
                normal_lines_to_left += 1
            if y_coord > line_check:
                normal_lines_above += 1
    
    # Normalise the x and y coordinates to remove the thickness of the lines from the coordinates
    x_norm = x_coord - LINE_WIDTH * normal_lines_to_left - BOLD_WIDTH * bold_lines_to_left
    y_norm = y_coord - LINE_WIDTH * normal_lines_above - BOLD_WIDTH * bold_lines_above

    # Return the cell that the click is in
    return GRID_SIZE * (y_norm // CELL_DIMENSION) + x_norm // CELL_DIMENSION


def cell_coords(cell):
    """
    Determines the top left coordinate of each cell
    param cell: the cell number
    return pos: returns the top left coordinate of the cell
    """

    row = cell // GRID_SIZE
    collumn = cell % GRID_SIZE

    # Calculate the number of different lines above and to the left of the cell
    normal_lines_left = collumn - collumn // SQUARE_SIZE
    bold_lines_left = collumn // SQUARE_SIZE + 1
    normal_lines_above = row - row // SQUARE_SIZE
    bold_lines_above = row // SQUARE_SIZE + 1

    # Calculate the coordinates of the top left corner of the cell
    x_coord = BOARD_PAD + collumn * CELL_DIMENSION + normal_lines_left * LINE_WIDTH + bold_lines_left * BOLD_WIDTH
    y_coord = BOARD_PAD + row * CELL_DIMENSION + normal_lines_above * LINE_WIDTH + bold_lines_above * BOLD_WIDTH

    return [x_coord, y_coord]

def draw_rect(pos, colour, line_width, len, height):
    """
    Draw a rectangle
    param pos: the top left of the rectangle
    param colour: the colour of rectangle
    param line_width: the width of the outline of the rectangle
    param len: the length of the rectangle
    param height: the height of the rectangle
    """

    # Define the lines that outline the rectangle
    top_rect = pygame.Rect(pos[X_INDEX], pos[Y_INDEX], len, line_width)
    left_rect = pygame.Rect(pos[X_INDEX], pos[Y_INDEX], line_width, height)
    bottom_rect = pygame.Rect(pos[X_INDEX], pos[Y_INDEX] + height - line_width, len, line_width)
    right_rect = pygame.Rect(pos[X_INDEX] + len - line_width, pos[Y_INDEX], line_width, height)

    # Draw the rectangle
    pygame.draw.rect(WIN, colour, top_rect)
    pygame.draw.rect(WIN, colour, left_rect)
    pygame.draw.rect(WIN, colour, bottom_rect)
    pygame.draw.rect(WIN, colour, right_rect)

def draw_give_up_rect():
    """
    Create the rectangle that acts as the give up button
    """

    # Draw the rectangle
    draw_rect([GIVE_UP_COORD_X, GIVE_UP_COORD_Y], BLACK, BOLD_WIDTH, GIVE_UP_WIDTH, GIVE_UP_HEIGHT)
    give_up_render = NUM_FONT.render(GIVE_UP_TEXT, 1, BLACK)

    # Draw the text
    WIN.blit(give_up_render, (GIVE_UP_COORD_X + 3, GIVE_UP_COORD_Y))
