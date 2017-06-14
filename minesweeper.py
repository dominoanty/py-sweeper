from sys import argv
from random import randint

UNMARKED=0
CLICKED=1
CLICK_TRIGGERED=5
MARKED=2
RUNNING=-1
GAME_OVER=-2
CLICK=-3
START_STATE=7

class point:
    
    def __init__(self):
        self.state = 0
        self.value = 0
        self.bomb = False

    def __str__(self):
        if self.state == UNMARKED:
            return "M"
        elif self.state == CLICK_TRIGGERED:
            if self.value == 0:
                return " "
            else:
                return str(self.value)
        elif self.state == MARKED:
            return "X"

    def mark(self):
        self.state = 2

    def click(self):
        if self.bomb:
            return GAME_OVER
        else:
            self.state=CLICKED
            return CLICK

def generate_mines(rows, cols, n_mines, click_x, click_y):
    count = n_mines
    generated_mines = {}
    while count:
        new_location = (randint(0,rows-1),randint(0,cols-1))
        if new_location in generated_mines or \
           new_location == (click_x, click_y):
            continue
        generated_mines[new_location] = 1
        count-=1
    return generated_mines.keys()


def print_world(world, mines):
    print("CURRENT STATE OF THE WORLD ")
    print("-------------------------- ")
    for i in world:
        print("\n|", end="")
        for j in i:
            print(j,end="|")
    print("\n")

def guess(world, mines, guess):
    pass

def trigger_click(world,x, y, rows, cols):
    world[x][y].state = CLICK_TRIGGERED
    if world[x][y].value == 0:
        for x_n in [-1,0, 1]:
            for y_n in [-1,0,1]:
                if x_n == y_n and x_n == 0:
                    continue
                if world[(x+x_n)%rows][(y+y_n)%cols].state == CLICK_TRIGGERED:
                    continue
                trigger_click(world, x+x_n, y+y_n, rows, cols)

def calculate_values(world, mines, rows, cols):
    for mine in mines:
        for x_n in [-1,0, 1]:
            for y_n in [-1,0,1]:
                if x_n == y_n and x_n == 0:
                    continue
                world[(mine[0] + x_n)%rows][(mine[1] + y_n)%cols].value+=1

if __name__ == "__main__":
    if len(argv) == 1:
        rows = 10
        cols = 10
        n_mines = 10
    elif len(argv) != 3:
        print( "Usage : "+ argv[0] +  " rows cols mines")
    else:
        rows = argv[0]
        cols = argv[1]
        n_mines = argv[2]

    world = [[point() for x in range(cols)] for x in range(rows)]
    mines = None
    game_state = START_STATE
    print_world(world,None)

    while game_state is not GAME_OVER:
        print_world(world, None)
        print("\n1. Mark ")
        print("\n2. Click")
        print("\n2. Solution ")
        print("\n3. Exit")
        inp = int(input())
        if inp == 1:
            print("\n-> Enter x and y position : ")
            x = int(input())
            y = int(input())
            if game_state is START_STATE:
                mines = generate_mines(rows, cols, n_mines, x-1, y-1) 
                calculate_values(world, mines, rows, cols)
                for mine in mines:
                    world[mine[0]][mine[1]].bomb = True
                game_state = RUNNING

            result = world[x-1][y-1].mark()
        elif inp == 2:
            print("\n-> Enter x and y position : ")
            x = int(input())
            y = int(input())
            result = world[x-1][y-1].click()
            if result == CLICK:
                trigger_click(world, x-1, y-1, rows, cols)
            elif result == GAME_OVER:
                game_state = GAME_OVER
        elif inp == 3:
            for mine in mines:
                world[mine[0]][mine[1]].mark()
            print("FINAL STATE")
            print("-----------")
            print_world(world,None)
            game_state = GAME_OVER
        else:
            game_state = GAME_OVER
                






    
