from pygame.math import Vector2 as vec

WIDTH, HEIGHT = 610, 670
FPS = 60
TOP_BOTTOM_PADDING = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH - TOP_BOTTOM_PADDING, HEIGHT - TOP_BOTTOM_PADDING

ROWS = 30
COLS = 28

BLACK = (0, 0, 0)
BLUE=(138,43,226)
BLUE_LIGHT=(0,0,255)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (190, 194, 15)

def replacer(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]