import pygame
import numpy as np
from rle_decoder import *
import sys

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (112, 128, 144)

def draw_grid(screen, grid):
    for i in range(cols):
        for j in range(rows):
            x = i * cell_size
            y = j * cell_size
            if grid[i, j] == 1:
                pygame.draw.rect(screen, WHITE, (x, y, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, BLACK, (x, y, cell_size, cell_size))
            pygame.draw.rect(screen, GREY, (x, y, cell_size, cell_size), 1)

    pygame.draw.rect(screen, GREY, (start_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, GREY, (start_x + button_width + button_padding, button_y, button_width, button_height))
    pygame.draw.rect(screen, GREY, (start_x + 2 * (button_width + button_padding), button_y, button_width, button_height))

    font = pygame.font.Font(None, 24)

    start_text = font.render("Start", True, WHITE)
    pause_text = font.render("Pause", True, WHITE)
    reset_text = font.render("Reset", True, WHITE)

    screen.blit(start_text, (start_x + (button_width - start_text.get_width()) // 2,
                             button_y + (button_height - start_text.get_height()) // 2))
    screen.blit(pause_text, (start_x + button_width + button_padding + (button_width - pause_text.get_width()) // 2,
                             button_y + (button_height - pause_text.get_height()) // 2))
    screen.blit(reset_text, (start_x + 2 * (button_width + button_padding) + (button_width - reset_text.get_width()) // 2,
                             button_y + (button_height - reset_text.get_height()) // 2))


def count_neighbors(grid, x, y): 
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            col = (x + i + cols) % cols
            row = (y + j + rows) % rows
            count += grid[col, row]
    count -= grid[x, y]
    return count


def update_grid(grid):
    new_grid = grid.copy()
    for i in range(cols):
        for j in range(rows):
            state = grid[i, j]
            neighbors = count_neighbors(grid, i, j)

            if state == 1:
                if neighbors < 2:
                    new_grid[i, j] = 0
                if neighbors > 3:
                    new_grid[i, j] = 0
            if state == 0 and neighbors == 3:
                new_grid[i, j] = 1
    return new_grid

def main(grid):
    running = True
    game_running = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if start_x <= x <= start_x + button_width and button_y <= y <= button_y + button_height:
                    print("Start button clicked")
                    game_running = True  
                elif start_x + button_width + button_padding <= x <= start_x + 2 * button_width + button_padding and button_y <= y <= button_y + button_height:
                    print("Pause button clicked")
                    game_running = False  
                elif start_x + 2 * (button_width + button_padding) <= x <= start_x + 3 * button_width + 2 * button_padding and button_y <= y <= button_y + button_height:
                    print("Reset button clicked")
                    if imported_grid is not None and not np.array_equal(grid, imported_grid):
                        grid = imported_grid.copy()
                    else: 
                        grid[:] = 0


                    game_running = False  # Stop the game

                else:
                    i, j = x // cell_size, y // cell_size
                    if i < cols and j < rows:
                        grid[i, j] = not grid[i, j]
                    print("Clicked on grid at position (%s, %s)" % (i, j))

        if game_running:
            grid = update_grid(grid)

        # Drawing the grid
        draw_grid(screen, grid)
        
        # Update the display
        pygame.display.flip()

        # Control the frame rate
        pygame.time.delay(100)


    pygame.quit()


def adjust_screen_size1(width, height, cols, rows):
    infoObject = pygame.display.Info()
    displayWidth = infoObject.current_w
    displayHeight = infoObject.current_h

    # Adjust width and height if they exceed the screen size
    if width > displayWidth:
        width = displayWidth
    if height > displayHeight:
        height = displayHeight

    # Recalculate cell_size to maintain the grid proportions
    cell_size = min(width // cols, height // rows)
    width = cell_size * cols
    height = cell_size * rows + 50  # Add extra height for the buttons or any UI

    return width, height, cell_size

def adjust_screen_size2(cols, rows):
    # Get the display info
    infoObject = pygame.display.Info()
    displayWidth = infoObject.current_w
    displayHeight = infoObject.current_h

    # Calculate the maximum possible cell size that fits the screen
    cell_size = min(displayWidth // cols, displayHeight // (rows + 5))  # 5 for some extra space

    # Calculate the width and height based on the new cell size
    width = cell_size * cols
    height = cell_size * rows + 50  # 50px reserved for UI elements like buttons

    return width, height, cell_size

def adjust_screen_size(cols, rows):

    # Get the display info
    infoObject = pygame.display.Info()
    displayWidth = infoObject.current_w
    displayHeight = infoObject.current_h

    # Calculate the maximum possible cell size that fits the screen
    cell_size = min(displayWidth // cols, displayHeight // (rows + 5))  # Slight adjustment for any UI

    # Calculate the width and height based on the new cell size
    width = cell_size * cols
    height = cell_size * rows + 30  # Reserve only minimal space for UI elements

    return width, height, cell_size


if __name__ == '__main__':


    pygame.display.set_caption("Conway's Game of Life")

    #Pick size of game, edges are "glued" to simulate the infinity of Conways game of life
    cols, rows = 60, 60
    width, height = cols*10, rows*10+50

    cell_size = width // cols

    #buttons
    button_width = 70
    button_height = 30
    button_padding = 10
    total_button_width = (3 * button_width) + (2 * button_padding)
    start_x = (width - total_button_width) // 2
    button_y = height - 35

    if len(sys.argv) == 1:

        width, height, cell_size = adjust_screen_size(cols, rows)
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        grid = np.zeros((cols, rows))
        main(grid)
        sys.exit()

    if sys.argv[1] == '-rle' and sys.argv[2] != None:

        grid, x, y = decode_rle_file(sys.argv[2])
        imported_grid = grid.copy()
        cols, rows = x, y
        width, height = cols*10, rows*10+50

        #buttons
        width, height, cell_size = adjust_screen_size(cols, rows)
        total_button_width = (3 * button_width) + (2 * button_padding)
        start_x = (width - total_button_width) // 2
        button_y = height - 35

        screen = pygame.display.set_mode((width, height))
        main(grid)
        sys.exit()

     



