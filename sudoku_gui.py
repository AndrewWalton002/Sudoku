import pygame
from sudoku_solver import *

pygame.font.init()

WIDTH, HEIGHT = 700, 498

X_INDEX = 0
Y_INDEX = 1

# Dimensions for the creation of the sudoku grid
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


# Define the fonts for sudoku
NUM_FONT = pygame.font.SysFont("Times New Roman", 40)

# RGB form of colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the pygame display and title it
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")


def draw_board():
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

        


def draw_game():
    """
    Draw the display of the game
    """

    WIN.fill(WHITE)
    draw_board()


def fill_grid(grid):
    """
    Fill the known cells in the sudoku with the elements
    param grid: the elements of the grid in a list
    """

    x_coord = OG_X_COORD
    y_coord = OG_Y_COORD

    for i in range(NUM_CELLS):
        
        # If the current cell is filled draw it
        if grid[i]:
            num = NUM_FONT.render(str(grid[i]), 1, BLACK)
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
    


            
    