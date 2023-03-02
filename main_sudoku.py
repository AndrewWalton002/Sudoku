import sudoku_solver
import sudoku_gui
import sudoku_web_scrape

import pygame

FPS = 60
MAX_INPUT_LEN = 1
EVENT_KEY_1_OFFEST = 48


def main():
    """
    Runs the sudoku game
    params grid: the sudoku game in a list
    """
    

    clicked_cell = -1
    user_input = ""

    user_grid = [None] * sudoku_gui.NUM_CELLS
    grid = [None] * sudoku_gui.NUM_CELLS


    grid = sudoku_web_scrape.get_data(sudoku_web_scrape.HARD)


    # Create a copy of the unfilled grid
    for i in range(sudoku_gui.NUM_CELLS):
        user_grid[i] = grid[i]
        #solver_grid[i] = grid[i]

   


    # Solve the sudoku
    #sudoku_solver.solve_sudoku(user_grid)
    
    run = True 

    clock = pygame.time.Clock()

    # Run the while loop while the window is open
    while run:
        
        # Update the display 60 times a second
        clock.tick(FPS)

        # Draw the board of the sudoku
        sudoku_gui.draw_game(clicked_cell)

        # Draw the known numbers in the board
        sudoku_gui.fill_grid(grid, user_grid)
    
        for event in pygame.event.get():

            # If the game is quit, close the window and return the function
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            
            # If a mouse was clicked determine its position
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
            
                # If the mouse was clicked within the give up rectangle, solve the sudoku
                if sudoku_gui.GIVE_UP_RECT.collidepoint(event.pos):
                    # Reset the user grid
                    for i in range(sudoku_gui.NUM_CELLS):
                        user_grid[i] = grid[i]

                    sudoku_solver.solve_sudoku(user_grid)
                    
                # Determine if the mouse was clicked within the grid and which cell it was clicked on
                clicked_cell = sudoku_gui.find_clicked_cell(pos)

                # Reset user input
                user_input = ""

            # Check if a key was pressed
            if event.type == pygame.KEYDOWN:

                # If backspace is pressed remove the last character
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                    user_grid[clicked_cell] = 0

                # Add the character to the user input if the input isn't already at max length and it is valid
                elif (event.key in range(pygame.K_1, pygame.K_9 + 1)) and (len(user_input) < MAX_INPUT_LEN) \
                    and sudoku_solver.is_insertion_valid(grid, clicked_cell, int(event.key) - EVENT_KEY_1_OFFEST):
                    user_input += event.unicode 

                    # Add the input to the grid
                    user_grid[clicked_cell] = int(event.key) - EVENT_KEY_1_OFFEST

        pygame.display.update()

        



if __name__ == "__main__":
    main()



