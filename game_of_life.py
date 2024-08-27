import pygame
import numpy as np

pygame.init()

# Data

#Pick size of game, edges are "glued" to simulate the infinity of Conways gol
cols, rows = 60, 60
width, height = cols*10, rows*10+50
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")
button_width = 70
button_height = 30
button_padding = 10
total_button_width = (3 * button_width) + (2 * button_padding)
start_x = (width - total_button_width) // 2
button_y = height - 35
cell_size = width // cols

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (112, 128, 144)


grid = np.zeros((cols, rows))

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

def main():
    global grid
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

if __name__ == '__main__':
    main()



