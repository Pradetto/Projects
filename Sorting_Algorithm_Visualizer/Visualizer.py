# npm run deploy on my server to deploy website
# Lookup techwithtim video on generators
# https://github.com/gitname/react-gh-pages


# Remember this is to get the requirements

# source sorting_algorithm_visualizer/venv/bin/activate
# python3 -m venv venv
# pip3 freeze > requirements.txt  
# cd into sorting_algo_visualizer
# activate virtual environment through source venv/bin/activate
# pip3 install -r requirements.txt 


import pygame
import random
import math
pygame.init()



class DrawInformation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    BACKGROUND_COLOR = WHITE

    Shades_Gray = [
        (128,128,128),
        (160,160,160),
        (192,192,192),
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self,width,height,lst):
        self.width = width
        self.height = height
        

        self.window = pygame.display.set_mode((width,height)) #This creates the window
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self,lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst)) #you have the area you can represent the number of blocks in
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val)) # tells you how many distinct numbers you have and weighs in how high and small your blocks are
        self.start_x = self.SIDE_PAD // 2 # bottom left of screen is 0,0






def draw(draw_info, algo_name, ascending): # you redrawn the canvas everytime ... not the most efficient way refer to line 96 for draw info
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2,5)) #43 minute explanation 5 pixels below

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2,45)) #43 minute explanation 5 pixels below

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | TBD - tbd | TBD - tbd", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2,75)) #43 minute explanation 35 pixels below

    draw_list(draw_info)
    pygame.display.update()



def draw_list(draw_info,color_positions = {}, clear_background=False): #refer to line 96 for draw info
    lst = draw_info.lst

    if clear_background:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)

        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst): #enumerate gives index and value of every single item in the list
        x = draw_info.start_x + i * draw_info.block_width # blocks in python are draw from the top left down tot he bottom right this line just adds the width to the previous one before
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height # you need to draw the taller rectangles higher on the screen 29:40 time stamp tells us how much larger we need to be above minimum

        color = draw_info.Shades_Gray[i % 3] #Going to return a 0, 1, 2

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_width,draw_info.height)) #could calculate precise height because this is drawing off the screen 32:57

    if clear_background:
        pygame.display.update()



def generate_start_list(n,min_val,max_val):
    lst = []
    for _ in range(n): #do this n times
        val = random.randint(min_val,max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info,ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]

            if num1 > num2 and ascending or num1 < num2 and not ascending:
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info,{j: draw_info.GREEN, j+1:draw_info.RED}, True)
                yield True #this calls this function for everytime you want the swap to occur it allows you to pass function halfway through and resume at a later time 49:07 program won't respond to anything else unless this is yielding

    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1,len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] > current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i = i-1
            lst[i] = current
            draw_list(draw_info, {i-1: draw_info.GREEN, i: draw_info.RED},True)
            yield True
    return lst

# next() #This is a generator object so this is based of yield in the function above

def main():
    run = True
    clock = pygame.time.Clock()
        
    n = 50
    min_val = 0
    max_val = 100

    lst = generate_start_list(n,min_val,max_val)
    draw_info = DrawInformation(800,600,lst) #This is the draw info line being passed into multiple function
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60) # amount of times it runs higher number the faster it runs can also hide it to run as fast as possible

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info,sorting_algo_name,ascending)


        # draw(draw_info)
        # pygame.display.update() thats to display if you havent draw anything

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r: #this is saying if you press the letter R
                lst = generate_start_list(n,min_val,max_val) # pass gets random numbers between min and max val
                draw_info.set_list(lst) # have to pass back to set the list and create it
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False: #this is saying if you press the letter R
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info,ascending)
            elif event.key == pygame.K_a and not sorting: #this is saying if you press the letter R
                ascending = True
            elif event.key == pygame.K_d and not sorting: #this is saying if you press the letter R
                ascending = False
            elif event.key == pygame.K_i and not sorting: #this is saying if you press the letter R
                sorting_algorithm = insertion_sort
                sorting_algo_name = 'Insertion Sort'
            elif event.key == pygame.K_b and not sorting: #this is saying if you press the letter R
                sorting_algorithm = bubble_sort
                sorting_algo_name = 'Bubble Sort'

    pygame.quit()




if __name__ == "__main__": #look up what this means this is at 19:30 timestamp
    main()
