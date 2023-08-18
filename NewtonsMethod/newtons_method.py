import pygame
import complex_lib as Cx
from random import randint
import os
import pickle
from math import exp
################################################################################
####                        CONSTANTS                                       ####
################################################################################

#COLORS
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (67, 170, 139)
PURPLE = (128, 0, 128)
CORAL = (255, 127, 80)
ORANGE = (255, 111, 89)
LBLUE = (25, 123, 189)
DBLUE = (18, 94, 138)
MBLUE = (32, 75, 87)
CRIMSON = (215, 38, 61)
RASP = (216, 30, 91)
ENGRED = (208, 0, 0)
DPURP = (37, 31, 71)
MINT = (46, 191, 165)


root_colors = [DPURP, LBLUE, RASP, PURPLE, MINT, DBLUE, MBLUE, GREEN, CORAL, ORANGE, RASP, ENGRED, RED, BLUE]

#newton method stuff
ZERO_THRESHOLD = 1 * 10**(-1)
SAME_ROOT_THRESHOLD = 1*10**(-1)
MAX_ITERATIONS = 50

roots_found = [] #format [(root, color), ...]

pygame.init()
s_width, s_height = screen_dimensions = (300,300)
screen = pygame.display.set_mode(screen_dimensions)
#screen.set_at((x,y),color)
display = [
    [BLACK for i in range(s_width)] for i in range(s_height)
]

def generate_fractal():
    scale_rgb = lambda col, alpha: int(col*alpha)
    #generate fractal
    for y, row in enumerate(display):
        os.system('clear')
        progression = int(70*y/s_height)
        print("generating....")
        print("progression: ", end="")
        print("{ " + "#"*progression + " "*(70-progression) + " }")
        for x, pixel in enumerate(row):
            grid_x = x-int(s_width/2)
            grid_y = y-int(s_width/2)

            #perform newtons method iteratively
            if grid_x == 0 and grid_y == 0:
                continue

            guess = Cx.Complex(grid_x,grid_y)
            for i in range(MAX_ITERATIONS):
                if guess.get_real() == 0 and guess.get_im()==0:
                    return
                guess = function.newtons_method(guess)
                if function.eval(guess).mag() <= ZERO_THRESHOLD:
                    #zeroed
                    existing_root = False
                    for root in roots_found:
                        if guess.dist(root[0]) < SAME_ROOT_THRESHOLD:
                            existing_root = True
                            color = root[1]
                            break

                    if not existing_root:
                        #add new root to list of found roots
                        roots_found.append(
                            (guess, root_colors.pop(randint(0,len(root_colors)-1)))
                        )
                        color = roots_found[-1][1]

                    alpha = (1-(i/MAX_ITERATIONS))
                    color = (
                        scale_rgb(color[0], alpha),
                        scale_rgb(color[1], alpha),
                        scale_rgb(color[2], alpha)
                    )
                    display[y][x] = color
                    break



def draw_to_screen():
    for y, row in enumerate(display):
        for x, colour in enumerate(row):
            screen.set_at((x,y), colour)

def write_to_file(filename):
    with open(filename, "wb") as fp:
        pickle.dump(display, fp)


def load_from_file(filePath):
    with open(filePath, "rb") as fp:
        display = pickle.load(fp)

    return display


def main():
    screen.fill(BLACK)
    draw_to_screen()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.flip()


if __name__ == "__main__":
    #bug: dont plug in single terms, always at least add constant to avoid div 0 error
    coefficients = [
         #format (power, coefficient (complex))
        (0, Cx.Complex(1,1)),
        (3,Cx.Complex(1,0)),
    ]
    function = Cx.complex_polynomial(coefficients)


    generate_fractal()
    main()

    #display = load_from_file("connected")
    #main()