import sudoku_solver
import sudoku_gui

import pygame

FPS = 60
MAX_INPUT_LEN = 1
EVENT_KEY_1_OFFEST = 48


def main(grid):
    """
    Runs the sudoku game
    params grid: the sudoku game in a list
    """
    
    clicked_cell = -1
    user_input = ""

    user_grid = [None] * sudoku_gui.NUM_CELLS
    # Create a copy of the unfilled grid
    for i in range(sudoku_gui.NUM_CELLS):
        user_grid[i] = grid[i]

    print(user_grid)

    # Solve the sudoku
    #sudoku_solver.solve_sudoku(grid)
    
    run = True 

    clock = pygame.time.Clock()

    # Run the while loop while the window is open
    while run:
        
        # Update the display 60 times a second
        clock.tick(FPS)

        # Draw the board of the sudoku
        sudoku_gui.draw_game(clicked_cell)
        sudoku_gui.render_user_input(user_input, clicked_cell)

        # Draw the known numbers in the board
        sudoku_gui.fill_grid(user_grid)
    
        for event in pygame.event.get():

            # If the game is quit, close the window and return the function
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            
            # If a mouse was clicked determine if it was in a cell in the board
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                clicked_cell = sudoku_gui.find_clicked_cell(pos)

            # Check if a key was pressed
            if event.type == pygame.KEYDOWN:

                # If backspace is pressed remove the last character
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                # Add the character to the user input if the input isn't already at max length and it is valid
                elif (event.key in range(pygame.K_1, pygame.K_9 + 1)) and (len(user_input) < MAX_INPUT_LEN) \
                    and sudoku_solver.is_insertion_valid(grid, clicked_cell, int(event.key) - EVENT_KEY_1_OFFEST):
                    user_input += event.unicode 

                    # Add the input to the grid
                    grid[clicked_cell] = int(event.key) - EVENT_KEY_1_OFFEST
                    print(grid)

        pygame.display.update()

        


if __name__ == "__main__":
    # Grid input in a nested list
    grid = [0, 1, 8, 0, 0, 2, 3, 0, 4, \
        0, 0, 3, 5, 0, 0, 0, 0, 0, \
        5, 2, 4, 8, 9, 0, 0, 0, 0, \
        1, 0, 5, 0, 7, 0, 4, 0, 6, \
        0, 0, 7, 0, 0, 0, 9, 0, 0, \
        2, 0, 9, 0, 4, 0, 5, 0, 8, \
        0, 0, 0, 0, 8, 9, 6, 4, 3, \
        0, 0, 0, 0, 0, 7, 2, 0, 0, \
        3, 0, 1, 6, 0, 0, 7, 8, 0]

    main(grid)



