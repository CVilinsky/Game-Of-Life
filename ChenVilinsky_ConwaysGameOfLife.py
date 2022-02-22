import os
import random
import sys
import time
import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
BLACK = (0, 0, 0)
screen = pygame.display.set_mode([400, 400], pygame.RESIZABLE)  # the screen everything will be displayed on
base_font = pygame.font.Font(None, 30)

input_rect = pygame.Rect(150, 150, 140, 32)  # 2 left are position, 2 right are size
color = pygame.Color('gray15')


def user_inputs(gets, value_range):
    """
    gets:  String that will show what we want the user to input now
    value_range: The range of the input value
    The function will return the value entered by the user
    """
    user_text = ''
    invalid_flag = False  # flag that will turn the text red in case the user entered an invalid value
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # what happens when the user presses enter
                    temp = int(user_text)
                    if (temp in value_range):
                        return user_text
                    else:
                        user_text = ""
                        invalid_flag = True
                if event.key == pygame.K_BACKSPACE:  # same with backspace
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode  # if none of the above, just add the character to the string
        screen.fill((0, 0, 0))
        if (invalid_flag == False):
            g_text = base_font.render(gets, True, (255, 255, 255))  # string we got in the beginning will be shown
        if (invalid_flag == True):
            g_text = base_font.render(gets, True, (255, 0, 0))
        g_text_rect = g_text.get_rect()  # the text is shown inside a rectangle
        g_text_rect.center = (200, 210)  # the position of the text
        pygame.draw.rect(screen, color, input_rect, 2)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        """
        blit will show the text in it's given rectangle 
        """
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        screen.blit(g_text, g_text_rect)
        input_rect.w = max(100, text_surface.get_width() + 10)  # if the input surpasses the size it will fit itself

        pygame.display.flip()


def draw_block(x, y, alive_color):
    """
    Used to draw each cell in the display
    """
    block_size = 9  # just looks better
    x *= block_size
    y *= block_size
    center_point = ((x + (block_size / 2)), (y + (block_size / 2)))
    pygame.draw.circle(screen, alive_color, center_point, block_size / 2, 0)


def print_grid(grid, rows, cols):
    """
    Used for printing inside the terminal
    the program now works mainly with PyGame
    """
    os.system("cls")
    res = "" + "\n"
    for row in range(rows):
        for col in range(cols):
            if (grid[row][col] == 0):
                res += "-"
            else:
                res += "O"
        res += "\n"
    print(res)


def first_grid(rows, cols):
    """
    Using the initial given rows and cols
    We create a grid, in that grid each cell might be alive or dead
    We return a list of lists that contains 1's,0's in a random pattern
    """
    grid = []
    for row in range(rows):
        temp_row = []
        for col in range(cols):
            # Generate a random number and based on that decide whether to add a live or dead cell to the grid

            if random.randint(0, 5) == 0:
                temp_row += [1]
            else:
                temp_row += [0]
        grid += [temp_row]
    return grid


def blank_grid(rows, cols):
    """
    Creates a blank grid to fill later
    """
    grid = []
    for row in range(rows):
        temp_row = []
        for col in range(cols):
            temp_row += [0]
        grid += [temp_row]
    return grid


def check_neighbors(row, col, grid):
    """
    After being given (row,col) coordinates in the grid
    we calculate the number of live neighbours
    """
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0):  # the cell itself
                pass
            else:
                if ((row + i) >= 0 and (col + j) >= 0):  # make sure the position is not out of bounds
                    try:
                        total += grid[row + i][col + j]  # using try and except here in case we go our of bounds
                    except:
                        pass
                else:
                    pass
    return total


def calculate_next_gen(grid, rows, cols):
    """
    Use the rules of the game to determine if a cell lives or dies
    We return the new matrix after the calculations
    """
    new_grid = blank_grid(rows, cols)  # create a blank grid
    for row in range(rows):
        for col in range(cols):
            live_neighbours = check_neighbors(row, col, grid)  # calls the function to check the cell's neighbours
            if grid[row][col] == 1:  # if the cell is alive
                if live_neighbours == 2 or live_neighbours == 3:
                    new_grid[row][col] = 1
                elif live_neighbours < 2 or live_neighbours > 3:
                    new_grid[row][col] = 0
            else:  # if the cell is dead
                if live_neighbours == 3:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
    return new_grid


def game():
    """
    The main game itself.
    The size of each pixel is 9, so it will be visually more convenient.
    """
    h = 0
    xmax = int(
        user_inputs("Value For X (100-400)", list(range(100, 401))))  # determine the size of the matrix by user input
    ymax = int(user_inputs("Value For Y (100-400)", list(range(100, 401))))
    gen = int(user_inputs("Value For Gen (10-100)", list(range(10, 101))))
    screen.fill('black')
    alive_color = pygame.Color(0, 0, 0)
    alive_color.hsva = [h, 100, 100]
    xlen = int(xmax / 9)
    ylen = int(ymax / 9)
    # random.seed(8)  # used it for debugging
    initial_grid = first_grid(xlen, ylen)
    for i in range(gen):
        pygame.event.get()
        for x in range(xlen):
            for y in range(ylen):
                alive = initial_grid[x][y]
                cell_color = alive_color if alive else BLACK #color each cell in the grid
                draw_block(x, y, cell_color) #use the draw function created to represent
        pygame.display.update()
        h = (h + 2) % 360  # the color will change with every iterations
        alive_color.hsva = (h, 100, 100)
        initial_grid = calculate_next_gen(initial_grid, xlen, ylen)
        time.sleep(0.4)  # wait between each iteration


game()

