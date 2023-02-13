import sudoku_solver
import sudoku_gui

import pygame

FPS = 60


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

    
    # Solve the sudoku
    sudoku_solver.solve_sudoku(grid)
    
    print(user_grid)
    run = True 

    clock = pygame.time.Clock()

    # Run the while loop while the window is open
    while run:
        
        # Update the display 60 times a second
        clock.tick(FPS)

        # Draw the board of the sudoku
        sudoku_gui.draw_game(clicked_cell)
        sudoku_gui.draw_rect(sudoku_gui.INPUT_RECT_COORDS, sudoku_gui.BLACK, sudoku_gui.BOLD_WIDTH, sudoku_gui.INPUT_RECT_LEN, 
                             sudoku_gui.INPUT_RECT_HEIGHT)
        sudoku_gui.render_user_input(user_input)

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
                # Add the character to the user input
                else:
                    user_input += event.unicode 


        
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



