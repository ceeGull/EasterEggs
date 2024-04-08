# ;The whole purpose of this program is to get any leads to what lore I can gather other than playing the game (the game I am referring to is Doki-Doki Literature Club)
# ;Imports
from GF import *
import pygame # ;It's been a very long time since I played with pygame
import pygame.gfxdraw
# ;INIT
pygame.init()
screen = pygame.display.set_mode((140, 140), 0, depth=1) # ;I was hoping that there is a monochrome options since what we need is just black and white colors which would honestly make it easier for me but I already finished and it works fine
# ;VARS
isRunning = True
black = (0, 0, 0)
# ;CODE

def scan_pixels():
    # LIST
    pixels = []
    x, y = [0, 0]
    # CODE
    for c_y in range(code.get_height()):
        if x == code.get_height():
            x = 0
        for c_x in range(code.get_width()):
            if y == code.get_width():
                y = 0
            color = code.get_at((x, y))[:3] # ;I don't think we need alpha
            color_code = []
            for c in color: # ;Grab each value in the color tuple and determine if it's black or white essentially representing binary
                if c < 240:
                    color_code.append(0)
                else:
                    color_code.append(1)
            color = tuple(color_code)
            # ;print((x, y), color)
            if color == black:
                pixels.append(0)
            else:
                pixels.append(1)
            x += 1
        y += 1
    return pixels

def get_pixels(): # ;Essentially scan_pixels except your given the pixels of the surface
    # LIST
    pixels = []
    x, y = [0, 0]
    # CODE
    for c_y in range(code.get_height()):
        if x == code.get_height():
            x = 0
        pixels.append([])
        for c_x in range(code.get_width()):
            if y == code.get_width():
                y = 0
            color = code.get_at((x, y))[:3] # ;I don't think we need alpha
            pixels[y].append(color)
            x += 1
        y += 1
    return pixels

def crop_pixels():
    # LIST
    min_width, min_height = 330, 330
    max_width, max_height = 470, 470
    x, y = min_width, min_height
    x1, y1 = 0, 0
    pixels = []
    # CODE
    for c_y in range(min_height, max_height):
        if x == max_height:
            x = min_height
        pixels.append([])
        for c_x in range(min_width, max_width):
            if y == max_width:
                y = min_width
            color = code_pixels[y][x] # ;I don't think we need alpha
            pixels[y1].append(color)
            x += 1
            x1 += 1
        y += 1
        y1 += 1
    return pixels

def reconstruct(): # ;Should be called repaint() or paint() but it's fine
    # LIST
    x, y = [0, 0]
    # CODE
    for c_y in range(len(code_pixels)):
        if x == code.get_height():
            x = 0
        for c_x in range(len(code_pixels[y])):
            if y == code.get_width():
                y = 0
            pygame.gfxdraw.pixel(code, x, y, code_pixels[y][x])
            x += 1
        y += 1

# ;if for somehow this is missing then search the whole computer for her mostlikely the it's parents' name are from the game's files
file_list = subprocess.run(["tree", "/", "-f", "-i", "-x", "-P", "monika.*"], capture_output=True, universal_newlines="\n").stdout.split("\n")
for f in file_list:
    if "monika.chr" in f:
        monika_chr_path = f
        break

code = pygame.image.load(monika_chr_path)

# ;Grab surface pixels and crop them so that it can be reconstructed
code_pixels = get_pixels()
code_pixels = crop_pixels()
code = pygame.Surface((140, 140))
reconstruct()

# ;We need only 1 frame
while isRunning:
    screen.blit(code.convert(), (0, 0))
    monika = scan_pixels() # ;Yes, just her
    pygame.display.flip()
    isRunning = False

pygame.quit() # ;We do not need pygame any longer as it fufilled it's purpose

code = ""
ascii_code_sep_exp = len(code)+8
for bit in monika: # ; partition the data to have on byte size be 8 characters each
    code += str(bit)
    if len(code) == ascii_code_sep_exp:
        code += ","
        ascii_code_sep_exp = len(code)+8
if code[len(code)-1] == ",": # ;if this is the last character in the code string then remove it
    code = code[:len(code)-2]
code = code.split(",")
code_ = ""
for c in code: # ;Converts the binary to an integer in which it's converted to an ASCII Character
    code_ += chr(int(c, 2))
code = code_
p(code) # ;moment of truth
